from util import http
import os.path

API_URL = 'https://gateway-a.watsonplatform.net/calls'
API_KEY = None
KEY_FILE = 'bluemix_keys'

class Error(Exception):
  pass

class APIError(Error):
  pass

def init():
  global API_KEY
  
  if os.path.isfile(KEY_FILE):
    API_KEY = open(KEY_FILE, 'r').read()

