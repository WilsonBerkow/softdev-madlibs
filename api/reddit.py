if __name__ == '__main__':
  import os
  os.chdir('..')
from util import http, util
import datetime
import urllib
import urllib2
import json
import os.path
import random

CLIENT_ID = None # Read from file
CLIENT_SECRET = None # Read from file
KEY_FILE = 'keys'

REDIRECT_URI = None # Define in app.py
USER_AGENT = 'Web:madlibs_for_reddit:v0.1 (by /u/teamredteam)'

AUTH_CODE = None
CURRENT_TOKEN = None
TOKEN_EXPIRATION = None
REFRESH_TOKEN = None
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class Error(Exception):
  pass

class APIError(Error):
  pass

def init():
  global CLIENT_ID, CLIENT_SECRET, CURRENT_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN

  if os.path.isfile(KEY_FILE):
    s = open(KEY_FILE).read().split('\n')
    CLIENT_ID = s[0]
    CLIENT_SECRET = s[1]
    CURRENT_TOKEN = s[2]
    TOKEN_EXPIRATION = datetime.datetime.strptime(s[3], DATETIME_FORMAT)
    REFRESH_TOKEN = s[4]

def authURL(scope):
  if not REDIRECT_URI:
    raise Error('Redirect URI must be defined!')

  data = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'state': 'test',
    'redirect_uri': REDIRECT_URI,
    'duration': 'permanent',
    'scope': scope
  }

  return 'https://www.reddit.com/api/v1/authorize?' + urllib.urlencode(data)

def updateToken(obj):
  global CURRENT_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN
  CURRENT_TOKEN = obj['access_token']
  TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(seconds = obj['expires_in'])
  f = open(KEY_FILE, 'w')
  f.write('\n'.join([CLIENT_ID, CLIENT_SECRET, CURRENT_TOKEN, TOKEN_EXPIRATION.strftime(DATETIME_FORMAT), REFRESH_TOKEN]))
  f.close()

def getToken():
  global AUTH_CODE, CURRENT_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN
  
  url = 'https://www.reddit.com/api/v1/access_token'

  headers = {
    'Authorization': 'Basic ' + http.httpBasicAuth(CLIENT_ID, CLIENT_SECRET),
    'User-Agent': USER_AGENT
  }

  if CURRENT_TOKEN:
    if datetime.datetime.utcnow() < TOKEN_EXPIRATION:
      print 'Using current token...'
      return CURRENT_TOKEN
    
    print 'Refreshing token...'
    
    data = {
      'grant_type': 'refresh_token',
      'refresh_token': REFRESH_TOKEN
    }

    results = http.post(url, headers, data)
    obj = json.loads(results.read())

    if 'access_token' not in obj:
      raise APIError('Token not found! Please authenticate.')
    
    updateToken(obj)
    return CURRENT_TOKEN
  elif AUTH_CODE:
    if not REDIRECT_URI:
      raise Error('Redirect URI must be defined!')

    print 'Acquiring token with authentication code...'
    
    data = {
      'grant_type': 'authorization_code',
      'code': AUTH_CODE,
      'redirect_uri': REDIRECT_URI
    }

    results = http.post(url, headers, data)
    obj = json.loads(results.read())

    if 'access_token' not in obj:
      raise APIError('Token not found! Please authenticate.')
    
    updateToken(obj)
    return CURRENT_TOKEN

  raise APIError('Token not found! Please authenticate.')

def getSubredditPosts(subreddit, count = 0):
  token = getToken()

  headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': USER_AGENT
  }

  url = 'https://oauth.reddit.com/r/%s/top/.json?t=all' % subreddit
  results = http.get(url, headers)
  d = json.loads(results.read())
  children = d['data']['children']
  n = min(count, len(children)) if count > 0 else len(children)
  posts = [children[i]['data'] for i in range(n)]
  return posts

def getSubredditRandomPost(subreddit, count = 0):
  posts = getSubredditPosts(subreddit, count)

  if len(posts) > 0:
    post = random.choice(posts)
    
    return {
      'url': 'http://reddit.com' + post['permalink'],
      'title': post['title'],
      'subreddit': subreddit,
      'id': post['id']
    }

  return None

def getTopLevelComments(subreddit, postID, count = 0):
  token = getToken()

  headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': USER_AGENT
  }

  url = 'https://oauth.reddit.com/r/%s/comments/%s/.json' % (subreddit, postID)
  results = http.get(url, headers)
  d = json.loads(results.read())
  children = d[1]['data']['children'][:-1]
  n = min(count, len(children)) if count > 0 else len(children)
  comments = [children[i]['data'] for i in range(n)]
  return comments

def getLotsOfCommentText(subreddit, numCalls):
  posts = getSubredditPosts(subreddit)
  numCalls -= 1
  lotsOfComments = []
  for post in posts[:numCalls]:
    comments = getTopLevelComments(subreddit, post['id'])
    for comment in comments:
      if comment['author'] != 'AutoModerator':  # madman himself
        lotsOfComments.append(comment['body'])
  return lotsOfComments

