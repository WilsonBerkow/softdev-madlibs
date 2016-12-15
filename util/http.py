import urllib, urllib2
import base64

def httpBasicAuthStr(username, password):
  return 'Basic ' + base64.b64encode('%s:%s' % (username, password))

def get(url, headers = {}, data = {}):
  req = urllib2.Request(url + '?' + urllib.urlencode(data), headers = headers)
  s = urllib2.urlopen(req)
  return s

def post(url, headers = {}, data = {}):
  req = urllib2.Request(url, data = urllib.urlencode(data), headers = headers)
  s = urllib2.urlopen(req)
  return s
  
