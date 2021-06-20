import argparse
import sys
import praw
import os

# Define parser and arguments
import prawcore
import requests

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--term", required=True)
parser.add_argument("-s", "--subreddit", required=True)
parser.add_argument("-w", "--webhook", required=True)
parser.add_argument("-f", "--frequency")

args = parser.parse_args()

# Preflight Checks
# Do we have our environmental variables set?
if os.environ['RELERT_CLIENT_ID'] is None:
    print("ERROR: RELERT_CLIENT_ID environment variable not set.")
    sys.exit(1)

if os.environ['RELERT_CLIENT_SECRET'] is None:
    print("ERROR: RELERT_CLIENT_SECRET environment variable not set.")
    sys.exit(1)

# Establish our reddit connection for future use
reddit_con = praw.Reddit(client_id=os.environ['RELERT_CLIENT_ID'], client_secret=os.environ['RELERT_CLIENT_SECRET'],
                         user_agent='windows:com.rishkar.relert:v0.0.1b')

# Does the subreddit exist?
try:
    reddit_con.subreddit(args.subreddit).id
except prawcore.exceptions.NotFound or prawcore.exceptions.Redirect:
    print("ERROR: Subreddit not found.")
    sys.exit(1)

# Is the webhook valid?
if not requests.post(args.webhook, {"content": "Relert is starting..."}):
    print("ERROR: Failed to communicate with your Discord webhook. Is the URL correct?")
    sys.exit(1)
