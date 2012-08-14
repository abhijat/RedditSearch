from pymongo import Connection
import tagger, sys

class Match:
    def __init__(self, key, id):
        self.id = id
        self.keys = [key]
        self.score = 10
        self.get_post()
    
    def get_post(self):
        posts = Connection()["reddit"]["posts"]
        post = posts.find_one({"id":self.id})
        if post:
            self.post = post
            self.votes = long(post["ups"])
            self.age = long(post["created_utc"])
        else:
            print "Nothing found for", self.id
            self.post = None
    
    def update_score(self, score):
        self.score += score
    
    def match_string(self, query):
        if not self.post:
            return
        tokens = self.post["tokens"]
        title = cleanup_string(self.post["title"])
        query = " ".join(query)
        if query in title:
            self.score += 100
        elif query.lower() in title.lower():
            self.score += 75
    
    def get_link(self):
        return "http://www.reddit.com%s" % self.post["permalink"]

    def __str__(self):
        return cleanup_string(self.get_link())

def compare_post(s, p):
    if not s.post or not p.post:
        return 0
    if p.score == s.score:
        if p.votes == s.votes:
            return int(s.age - p.age)
        else:
            return int(s.votes - p.votes)
    else:
        return s.score - p.score

def search(query):
    if not query:
        return
    orig = query.split()
    query = tagger.make_tags(query)
    idx = Connection()["reddit"]["inverted_index"]
    
    matches = []
    ids = {}
    for q in query:
        row = idx.find_one({"key" : q})
        if not row:
            continue
        for i in row["ids"]:
            if i in ids:
                match = ids[i]
                match.update_score(10)
            else:
                ids[i] = Match(q,i)
                matches.append(ids[i])
                ids[i].match_string(query)

    sorted_matches = sorted(matches, cmp=compare_post, reverse=True)
    for m in sorted_matches:
        print m.score, m.votes, m.age, m

def get_title(id, debug=True):
    posts = Connection()["reddit"]["posts"]
    row = posts.find_one({"id" : id})
    if row:
        title = cleanup_string(row["title"])
        if debug:
            print ">>>> Got title:", title
    return row

def cleanup_string(string):
    return " ".join([w.encode("utf8") for w in string.split()])

def test():
    search(" ".join(sys.argv[1:]))

if __name__ == "__main__":
    test()
