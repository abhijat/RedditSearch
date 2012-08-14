from pymongo import Connection
from nltk import PorterStemmer

stop_words = []
def make_tags(title_string):
    stemmer = PorterStemmer()
    ret = []
    for word in title_string.split():
        if word not in stop_words:
            ret.append(stemmer.stem_word(word.lower()))
    return ret

def read_titles(collection, field_name, target):
    for row in collection.find():
        if field_name in row:
            string = row[field_name].encode("utf-8")
            lst = make_tags(string)
            target.insert({row["id"] : lst})
    return

def update_tags(collection, key_name, field_name):
    for row in collection.find():
        if field_name in row:
            key = row[key_name]
            string = row[field_name].encode('utf-8')
            tags = make_tags(string)
            row["tokens"] = tags
            print tags
            collection.update({
                key_name : key
                }, row)
            print "Updated", key
    return        

def clear_tags(collection, key_name, field_name):
    for row in collection.find():
        if field_name in row:
            key = row[key_name]
            tokens = row["tokens"]
            row["tokens"] = []
            collection.update({
                key_name : key,
                "tokens" : tokens
                }, row)
            print "Updated", key
    return        

def main():
    collection = Connection()["reddit"]["posts"]
    target = Connection()["reddit"]["tags"]
    field_name = "title"
    #read_titles(collection, field_name, target)
    update_tags(collection, "id", "title")
    #clear_tags(collection, "id", "title")
    return

if __name__ == "__main__":
    main()
