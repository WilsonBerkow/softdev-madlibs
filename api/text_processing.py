from util import http
import json

def getSentiment(text):
  url = 'http://text-processing.com/api/sentiment/'

  data = {
    'text': text
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


  
  
