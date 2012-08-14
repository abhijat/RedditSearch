import urllib2, json, time
from pymongo import Connection
import tagger, index

def log_error(error, log_file="errors"):
    errors = open(log_file, 'w')
    errors.write("%s: %s" % (time.ctime(), error))
    errors.close()
    return

def get_reddit_json(index_handle, posts, id_date):
    
    headers = {
            'User-Agent' : 'Search engine project by /u/fjellfras'
    }
    
    link = 'http://www.reddit.com/r/all.json'
    ids = []
    tags = Connection()["reddit"]["tags"]
    while True:
        request = urllib2.Request(link, headers=headers)
        try:
            link_handle = urllib2.urlopen(request)
            raw_txt = link_handle.read()
        except urllib2.URLError, e:
            log_error("URL Error: ", e.reason)
        except urllib2.HTTPError, e:
            log_error("HTTP Error: ", e.code)
        except Exception, e:
            log_error("Unknown error: ", e)

        top_dict = json.loads(raw_txt)
        data = top_dict['data']

        for c in data['children']:
            if c['data']['id'] not in ids:
                ids.append(c['data']['id'])
                if len(ids) > 100:
                    ids.pop(0)

                post = c["data"]    
                title = post["title"]
                tag_list = tagger.make_tags(title)
                post["tokens"] = tag_list
                posts.insert(post)
                
                if "created_utc" in post:
                    id_date.insert({
                        post["id"]:post["created_utc"]
                        })
                print "Added", post['id']
                index.update_index(post["id"], tag_list)
        
        time.sleep(10)

def main():
    index = open('index.txt','w')
    conn = Connection()
    coll = conn["reddit"]
    posts = coll["posts"]
    id_date = coll["ids"]
    get_reddit_json(index, posts, id_date)
    index.close()
    return

if __name__ == '__main__':
    main()
