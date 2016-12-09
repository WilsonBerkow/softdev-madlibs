from util import http, util
import datetime
import urllib
import urllib2
import json
import os.path

CLIENT_ID = 'jwTgn4ggRNAGiw' # Fill this in with your client ID
CLIENT_SECRET = '4yphEGmjvuEEYBXyulBMjSj2uJs' # Fill this in with your client secret
REDIRECT_URI = None # Define in app.py
USER_AGENT = 'Web:madlibs_for_reddit:v0.1 (by /u/teamredteam)'
AUTH_CODE = None
CURRENT_TOKEN = None
TOKEN_EXPIRATION = None
REFRESH_TOKEN = None
TOKEN_FILE = 'token'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def init():
  global CURRENT_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN
  
  if os.path.isfile(TOKEN_FILE):
    s = open(TOKEN_FILE).read().split('\n')
    CURRENT_TOKEN = s[0]
    TOKEN_EXPIRATION = datetime.datetime.strptime(s[1], DATETIME_FORMAT)
    REFRESH_TOKEN = s[2]    

def authURL(scope):
  if not REDIRECT_URI:
    raise Exception('Redirect URI must be defined!')

  print REDIRECT_URI
    
  params = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'state': 'test',
    'redirect_uri': REDIRECT_URI,
    'duration': 'permanent',
    'scope': scope
  }

  return 'https://www.reddit.com/api/v1/authorize?' + urllib.urlencode(params)

def getToken():
  global AUTH_CODE, CURRENT_TOKEN, TOKEN_EXPIRATION, REFRESH_TOKEN
  
  if not REDIRECT_URI:
    raise Exception('Redirect URI must be defined!')

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
      
    params = {
      'grant_type': 'refresh_token',
      'refresh_token': REFRESH_TOKEN
    }

    results = http.post(url, headers, params)
    obj = json.loads(results.read())

    CURRENT_TOKEN = obj['access_token']
    TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(seconds = obj['expires_in'])
    f = open('token', 'w')
    f.write('%s\n%s\n%s' % (CURRENT_TOKEN, TOKEN_EXPIRATION.strftime(DATETIME_FORMAT), REFRESH_TOKEN))
    f.close()
    return CURRENT_TOKEN
  elif AUTH_CODE:
    print 'Acquiring token with authentication code...'
    
    params = {
      'grant_type': 'authorization_code',
      'code': AUTH_CODE,
      'redirect_uri': REDIRECT_URI
    }

    results = http.post(url, headers, params)
    obj = json.loads(results.read())

    CURRENT_TOKEN = obj['access_token']
    REFRESH_TOKEN = obj['refresh_token']
    TOKEN_EXPIRATION = datetime.datetime.utcnow() + datetime.timedelta(seconds = obj['expires_in'])
    
    f = open('token', 'w')
    f.write('%s\n%s\n%s' % (CURRENT_TOKEN, TOKEN_EXPIRATION.strftime(DATETIME_FORMAT), REFRESH_TOKEN))
    f.close()

    return CURRENT_TOKEN
  else:
    print 'Unable to get token! Please authenticate with Reddit first.'
    return None

def getPostsFromSubreddit(subreddit):
  token = getToken()

  if not token:
    return {}
  
  headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': USER_AGENT
  }

  url = 'https://oauth.reddit.com/r/%s/top/.json?sort=top&t=all' % subreddit
  results = http.get(url, headers)
  return json.loads(results.read())

