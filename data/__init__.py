import os
import time
import sqlite3

# database connection
dbcon = None

def initdb():
    '''
    Connect to data/wutangerine.db. If the db didn't already exist, create
    the `mashes' and `posts' tables.
    '''
    fname = "data/wutangerine.db"
    existed = os.path.isfile(fname)
    print "Conneting to data/wutangerine.db"
    if existed:
        print "which already existed"
    global dbcon
    dbcon = sqlite3.connect(fname)
    if not existed:
        cursor = dbcon.cursor()
        # post_A and post_B are the URLs of the respective posts
        cursor.execute("CREATE TABLE mashes (datetime INTEGER, post_A TEXT, post_B TEXT, mashed TEXT)")
        cursor.execute("CREATE TABLE posts (url TEXT, subreddit TEXT, title TEXT)")
        dbcon.commit()

def add_mash(postA, postB, mashed):
    cursor = dbcon.cursor()
    now = int(time.time())
    cursor.execute("INSERT INTO mashes VALUES (?, ?, ?, ?)", (now, postA, postB, mashed))
    dbcon.commit()

# Offer the 5 most recent mashes
RECENT_MASHES_N = 5

def recent_mashes():
    cursor = dbcon.cursor()
    cursor.execute("SELECT datetime, post_A, post_B, mashed FROM mashes")
    # Sort mashes descending by first element (datetime)
    mashes = sorted(cursor.fetchall(), key=lambda x: -x[0])

    # Return the first RECENT_MASHES_N mashes
    print mashes[0:RECENT_MASHES_N]

