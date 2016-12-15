from flask import Flask, request, redirect, render_template, flash
# import data
from api import reddit, text_processing
from util import util, mash
import urllib2

app = Flask(__name__)

@app.route('/')
def home():
  sub1 = util.getValue(request.args, 'sub1')
  sub2 = util.getValue(request.args, 'sub2')
  error_message = None

  if sub1 and sub2:
    try:
      sentimentMessages = {'neg': 'That\'s not nice.', 'pos': 'Why thank you!', 'neutral': 'What\'s that supposed to mean?'}

      mashed = mash.getMash(sub1, sub2, 10)

      for i in range(len(mashed)):
        text = mashed[i]
        mashed[i] = (text, sentimentMessages[text_processing.getSentiment(text)])
        
      return render_template('home.html', sub1 = sub1, sub2 = sub2, mashed = mashed)
    except urllib2.HTTPError as error:
      error_message = 'An error occurred (code %d).' % error.code
    except reddit.TokenError as error:
      error_message = error.message

  return render_template('home.html', noposts = True, error_message = error_message)

# should never be used in production
@app.route('/auth')
def auth():
  return '<a href=%s>Authenticate</a>' % reddit.authURL('read')

# testing
@app.route('/posts/')
def posts():
  posts = reddit.getSubredditPosts('AskReddit')
  titles = [post['title'] for post in posts]
  ret = '<br><br>'.join(titles)
  return ret

# testing
@app.route('/comments/')
def comments():
  posts = reddit.getSubredditPosts('AskReddit', 1)
  postID = posts[0]['id']
  comments = reddit.getTopLevelComments('AskReddit', postID)
  bodies = [comment['body'] for comment in comments]
  ret = '<br><br>'.join(bodies)
  return ret

# should never be used in production
@app.route('/reddit_callback')
def reddit_callback():
  error = util.getValue(request.args, 'error')
  code = util.getValue(request.args, 'code')
  state = util.getValue(request.args, 'state')

  if error:
    raise Exception('Error: ' + error)

  print 'Authenticated successfully!'
  reddit.AUTH_CODE = code
  return 'Authenticated successfully!'

def init():
  # data.initdb()
  reddit.init(redirect_uri = 'http://127.0.0.1:5000/reddit_callback')

if __name__ == '__main__':
  init()
  app.debug = True
  app.run()
