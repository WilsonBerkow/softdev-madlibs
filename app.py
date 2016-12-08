from flask import Flask, request, render_template
import dbutil
from api import reddit, bluemix

dbutil.initdb()

app = Flask(__name__)

def getParam(name):
  if name in request.args:
    return request.args[name]

  return None

def postParam(name):
  if name in request.form:
    return request.form[name]

  return None

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/auth')
def default():
  return '<a href=%s>Authenticate</a>' % reddit.authURL('read')

@app.route('/reddit_callback')
def reddit_callback():
  error = getParam('error')
  code = getParam('code')
  state = getParam('state')

  if error:
    raise('Error: ' + error)

  token = reddit.getToken(code)
  print token
  return 'Token: ' + str(token)

if __name__ == '__main__':
  app.debug = True
  reddit.REDIRECT_URI = 'http://127.0.0.1:5000/reddit_callback'
  app.run()

