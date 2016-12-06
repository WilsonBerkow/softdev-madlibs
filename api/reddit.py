import urllib
import urllib2

CLIENT_ID = "qp8wyjX0Vv2eig" # Fill this in with your client ID
CLIENT_SECRET = "AorBUomwsPPpUd3lXm0cEY46rOs" # Fill this in with your client secret
REDIRECT_URI = None # Define in app.py

def authURL():
  if not REDIRECT_URI:
    raise Error('Redirect URI must be defined!')
    
  params = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'state': 'test',
    'redirect_uri': REDIRECT_URI,
    'duration': 'permanent',
    'scope': 'identity'
  }
  
  url = urllib.urlencode(params)
  return url

