from util import http, util
import datetime
import urllib
import urllib2
import json
import os.path
import random

CLIENT_ID = None # Read from file
CLIENT_SECRET = None # Read from file
KEY_FILE = 'reddit_keys'

REDIRECT_URI = None # Define in app.py
USER_AGENT = 'Web:madlibs_for_reddit:v0.1 (by /u/teamredteam)'

AUTH_CODE = None
CURRENT_TOKEN = None
TOKEN_EXPIRATION = None
REFRESH_TOKEN = None
TOKEN_FILE = 'reddit_token'
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
  
  if os.path.isfile(TOKEN_FILE):
    s = open(TOKEN_FILE).read().split('\n')
    CURRENT_TOKEN = s[0]
    TOKEN_EXPIRATION = datetime.datetime.strptime(s[1], DATETIME_FORMAT)
    REFRESH_TOKEN = s[2]

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

    CURRENT_TOKEN = obj['access_token']
    TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(seconds = obj['expires_in'])
    f = open(TOKEN_FILE, 'w')
    f.write('%s\n%s\n%s' % (CURRENT_TOKEN, TOKEN_EXPIRATION.strftime(DATETIME_FORMAT), REFRESH_TOKEN))
    f.close()
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

    CURRENT_TOKEN = obj['access_token']
    REFRESH_TOKEN = obj['refresh_token']
    TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(seconds = obj['expires_in'])
    
    f = open(TOKEN_FILE, 'w')
    f.write('%s\n%s\n%s' % (CURRENT_TOKEN, TOKEN_EXPIRATION.strftime(DATETIME_FORMAT), REFRESH_TOKEN))
    f.close()

    return CURRENT_TOKEN
  else:
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
        p = random.choice(posts)
        return {
            'url': 'http://reddit.com' + p[u'permalink'],
            'title': p[u'title'],
            'subreddit': subreddit
        }
    return None

def getTopLevelComments(subreddit, postID, count = 0):
  token = getToken()

  headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': USER_AGENT
  }

  url = 'https://oauth.reddit.com/r/%s/comments/%s/.json' % (subreddit, postID)
  print url
  results = http.get(url, headers)
  d = json.loads(results.read())
  print d
  children = d[1]['data']['children'][:-1]
  n = min(count, len(children)) if count > 0 else len(children)
  comments = [children[i]['data'] for i in range(n)]
  return comments
