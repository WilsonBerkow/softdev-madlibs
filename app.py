from flask import Flask, request, redirect, render_template
import data
from api import reddit, text_processing
from util import util, mash

app = Flask(__name__)

@app.route('/')
def home():
  post1 = None
  post2 = None
  sub1 = None
  sub2 = None
  if 'sub1' in request.args and 'sub2' in request.args and request.args['sub1'] != "" and request.args['sub2'] != "":
    sub1 = request.args['sub1']
    sub2 = request.args['sub2']
    try:
      post1 = reddit.getSubredditRandomPost(sub1, 30)
      post2 = reddit.getSubredditRandomPost(sub2, 30)
      if post1 != None and post2 != None:
        comments = []
        grams = mash.ngramsFromSubreddits(sub1, sub2)
        for _ in xrange(10):
          comments += [mash.getComment(grams).encode('utf-8')]
      return render_template('home.html', post1 = post1, post2 = post2, sub1 = sub1, sub2 = sub2, comments=comments)
    except reddit.APIError:
      return redirect('auth')
  else:
    return render_template('home.html', noposts = True)

@app.route('/auth')
def auth():
  return '<a href=%s>Authenticate</a>' % reddit.authURL('read')

@app.route('/posts/')
def posts():
  try:
    posts = reddit.getSubredditPosts('AskReddit')
    titles = [post['title'] for post in posts]
    ret = '<br><br>'.join(titles)
    return ret
  except reddit.APIError:
    return redirect('auth')

@app.route('/comments/')
def comments():
  try:
    posts = reddit.getSubredditPosts('AskReddit', 1)
    postID = posts[0]['id']
    comments = reddit.getTopLevelComments('AskReddit', postID)
    bodies = [comment['body'] for comment in comments]
    ret = '<br><br>'.join(bodies)
    return ret
  except reddit.APIError:
    return redirect('auth')

@app.route('/reddit_callback')
def reddit_callback():
  error = util.getValue(request.args, 'error')
  code = util.getValue(request.args, 'code')
  state = util.getValue(request.args, 'state')

  if error:
    raise Exception('Error: ' + error)

  print 'Authenticated successfully!'
  reddit.AUTH_CODE = code
  return redirect('posts')

def init():
  data.initdb()
  reddit.init(redirect_uri = 'http://127.0.0.1:5000/reddit_callback')

if __name__ == '__main__':
  init()
  app.debug = True
  app.run()
