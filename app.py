from flask import Flask, request, redirect, render_template
import data
from api import reddit, text_processing
from util import util

app = Flask(__name__)

@app.route('/')
def home():
    if "sub1" in request.args and "sub2" in request.args:
        try:
            sub1 = reddit.getSubredditPosts(request.args['sub1'])
            sub2 = reddit.getSubredditPosts(request.args['sub2'])
        except reddit.APIError:
            return redirect('auth')
        post1url = None
        post2url = None
        post1title = None
        post2title = None
        no_posts = False # False for success, 'sub1' for no posts in sub1, 'sub2' for no posts in sub2
        if len(sub1) == 0:
            no_posts = 'sub1'
        elif len(sub2) == 0:
            no_posts = 'sub2'
        else:
            post1 = sub1[0]
            post2 = sub2[0]
            post1title = post1[u'title']
            post1url = "http://reddit.com" + post1[u'permalink']
            post2title = post2[u'title']
            post2url = "http://reddit.com" + post2[u'permalink']
        # TODO: mash and pass to template
        return render_template('home.html',
                no_posts=no_posts,
                post1title=post1title,
                post1url=post1url,
                post2title=post2title,
                post2url=post2url,
                sub1=request.args['sub1'],
                sub2=request.args['sub2'])
    else:
        return render_template("home.html", no_posts=False)

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
  
if __name__ == '__main__':
  data.initdb()
  app.debug = True
  reddit.init()
  reddit.REDIRECT_URI = 'http://127.0.0.1:5000/reddit_callback'
  app.run()

