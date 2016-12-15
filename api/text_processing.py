from util import http, util
import json

def getSentiment(text):
  url = 'http://text-processing.com/api/sentiment/'

  data = {
    'text': util.sanitize(text)
  }

  results = http.post(url, data = data)
  d = json.loads(results.read())
  return d['label']

def tagText(text):
  url = 'http://text-processing.com/api/tag/'

  data = {
    'text': text
  }

  results = http.post(url, data = data)
  d = json.loads(results.read())
  return d['text']


  
  
