import os
import sqlite3

def initdb():
    '''
    Connect to wutangerine.db. If the db didn't already exist, create
    the `mashes' and `posts' tables.
    '''
    fname = "wutangerine.db"
    existed = os.path.isfile(fname)
    print "Conneting to wutangerine.db"
    db = sqlite3.connect(fname)
    if not existed:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE mashes (datetime INTEGER, post_A INTEGER, post_B INTEGER, mashed TEXT)")
        cursor.execute("CREATE TABLE posts (id INTEGER, subreddit TEXT, title TEXT, url TEXT)")
        db.commit()
    return db
