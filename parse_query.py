#!/usr/bin/env python

import re

class Query(object):
    def __init__(self):
        self.query_string = None
        self.nsfw = None
        self.exact_match = False
        self.subreddit = 'all'
        return

    def set_exact_match(self, exact_match):
        self.exact_match = exact_match
        return

    def set_nsfw_match(self, nsfw):
        self.nsfw = nsfw
        return

    def set_subreddit(self, subreddit):
        self.subreddit = subreddit
        return

    def set_query_string(self, query_string):
        self.query_string = query_string
        return

    def __repr__(self):
        return '''
        Query String: %s
        Exact Match: %s
        NSFW Filter: %s
        Subreddit: %s
        ''' % (self.query_string, self.exact_match, 
                self.nsfw, self.subreddit)

def parse(query_string):

    query = Query()
    match = re.search(r'(.*?)"(.+)"(.*)', query_string)
    if match:
        query.set_query_string(match.group(2))
        query.set_exact_match(True)
        query_string = match.group(1) + match.group(3)

    match = re.search(r'\+nsfw', query_string)
    if match:
        query.set_nsfw_match(True)
        query_string = query_string.replace('+nsfw', '')
    else:
        match = re.search(r'\-nsfw', query_string)
        if match:
            query.set_nsfw_match(False)
            query_string = query_string.replace('-nsfw', '')

    match = re.search(r'\bsub:([\w\d]+)', query_string)
    if match:
        query.set_subreddit(match.group(1))
        query_string = query_string.replace(match.group(), '')
    
    if query.query_string == None:
        query_string = ' '.join(query_string.split())
        query.set_query_string(query_string)
    return query

def main(query):
    q = parse(query)
    print q
    return

if __name__ == '__main__':
    import sys
    main(' '.join(sys.argv[1:]))
