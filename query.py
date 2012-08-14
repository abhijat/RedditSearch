from pymongo import Connection

if __name__ == "__main__":
    col = Connection()["reddit"]["posts"]
    count = 0
    for row in col.find():
        if "loft" in row["tokens"]:
            print row
        count += 1
    print count    
