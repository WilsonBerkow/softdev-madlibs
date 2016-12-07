import urllib, urllib2
import base64

def httpBasicAuth(username, password):
  return base64.b64encode('%s:%s' % (username, password))

def get(url, headers = {}, params = {}):
  req = urllib2.Request(url + '?' + urllib.urlencode(params), headers = headers)
  s = urllib2.urlopen(req)
  return s

def post(url, headers = {}, params = {}):
  req = urllib2.Request(url, data = urllib.urlencode(params), headers = headers)
  s = urllib2.urlopen(req)
  return s
  
