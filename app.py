from flask import Flask
from api import reddit, bluemix

app = Flask(__name__)

@app.route('/')
def default():
  return 'Hello World!'

if __name__ == '__main__':
  app.debug = True
  reddit.REDIRECT_URI = "http://127.0.0.1:5000/reddit_callback"
  print reddit.authURL()
  app.run()
