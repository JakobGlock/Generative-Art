import sys
import os

args = sys.argv

# This is our drawing Context
Context = None

# Some default variables
file_format = 'SVG' if eval(args[2]) else 'PNG'
open_file = True if eval(args[1]) else False
image_folder = "/Images"
script_name = args[0]

# Variables for posting to Twitter
twitter_post = True if eval(args[3]) else False
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')
tweet_status = '#Generative #Art #CreativeCoding #Python #Cornwall #Bot'
