from pymongo import Connection
import tagger

invalid = ['.', '$']
def update_index(id, words):
    index = Connection()["reddit"]["inverted_index"]
    for w in words:
        for i in invalid:
            if i in w:
                w = w.replace(i,'')
        row = index.find_one({"key" : w})
        if not row:
            index.insert({
                "key" : w,
                "ids" : [id]
                })
        else:
            lst = list(row["ids"])
            if id not in lst:
                lst.append(id)
                new_row = {"key":w, "ids":lst}
                index.update({"key" : w}, new_row)
                
def update_all():
    tags = Connection()["reddit"]["tags"]
    index = Connection()["reddit"]["inverted_index"]

    invalid = ['.', '$']
    for tag in tags.find():
        for key in tag.keys():
            if key != "_id":
                word_list = tag[key]
                for w in word_list:
                    for i in invalid:
                        if i in w:
                            w = w.replace(i,'')
                    row = index.find_one({"key" : w})
                    if not row:
                        index.insert({"key": w, "ids" : [key]})
                    else:
                        print "Updating", w
                        print row, row["ids"]
                        lst = list(row["ids"])
                        print lst, key
                        lst.append(key)
                        new_row = {"key":w, "ids": lst}
                        print new_row
                        index.update({"key":w}, new_row)
