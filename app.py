from flask import Flask, request, redirect, render_template
import data
from api import reddit, bluemix
from util import util

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/auth')
def default():
  return '<a href=%s>Authenticate</a>' % reddit.authURL('read')

@app.route('/posts/')
def posts():
  return str(reddit.getPostsFromSubreddit('test'))

@app.route('/reddit_callback')
def reddit_callback():
  error = util.getValue(request.args, 'error')
  code = util.getValue(request.args, 'code')
  state = util.getValue(request.args, 'state')
  
  if error:
    raise('Error: ' + error)

  print 'Authenticated successfully!'
    
  reddit.AUTH_CODE = code
  return redirect('posts')
  
if __name__ == '__main__':
  data.initdb()
  app.debug = True
  reddit.init()
  reddit.REDIRECT_URI = 'http://127.0.0.1:5000/reddit_callback'
  app.run()

