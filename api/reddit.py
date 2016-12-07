from util import http
import urllib, urllib2

CLIENT_ID = "jwTgn4ggRNAGiw" # Fill this in with your client ID
CLIENT_SECRET = "4yphEGmjvuEEYBXyulBMjSj2uJs" # Fill this in with your client secret
REDIRECT_URI = None # Define in app.py

def authURL(scope):
  if not REDIRECT_URI:
    raise Error('Redirect URI must be defined!')

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

def getToken(code):
  if not REDIRECT_URI:
    raise Error('Redirect URI must be defined!')

  headers = {
    'Authorization': 'Basic ' + http.httpBasicAuth(CLIENT_ID, CLIENT_SECRET)
  }

  params = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
  }

  url = 'https://www.reddit.com/api/v1/access_token'
  results = http.post(url, headers, params)
  return results.read()

