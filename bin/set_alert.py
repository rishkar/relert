import os
import sys
import argparse
import time
import requests
import praw
import prawcore

# Define parser and arguments
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--term", required=True, help="The term to search for in subreddit post titles")
parser.add_argument("-s", "--subreddit", required=True, help="The subreddit to search.")
parser.add_argument("-w", "--webhook", required=True, help="The Discord webhook to send messages to.")
parser.add_argument("-f", "--frequency", default=60, help="Run a check every X seconds. Defaults to 60.")

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
if not requests.post(args.webhook, {"content": "Relert is starting...", "username": "r/"+args.subreddit}).ok:
    print("ERROR: Failed to communicate with your Discord webhook. Is the URL correct?")
    sys.exit(1)

# Initialize our subreddit object
subreddit_con = reddit_con.subreddit(args.subreddit)

# Make our loops!
while True:
    first = True
    prev_sub = None
    # Let's start iterating thru all the new submissions
    for submission in subreddit_con.stream.submissions():
        # If we've reached the point we were at during the last iteration we don't want to go further
        if prev_sub == submission:
            break
        elif first:
            prev_sub = submission
            first = False

        # If the submission matches our term, let's send an alert!
        if args.term in submission.title:
            message = "ALERT: Term %s in Subreddit %s found:\n**Submission Title:** %s\n**Link:** %s" % \
                      (args.term, args.subreddit, submission.title, submission.url)
            print(message + "\n Sending to discord...")
            requests.post(args.webhook, {"content": message, "username": "r/"+args.subreddit})

    print("Nothing more found. Sleeping for %d seconds..." % args.frequency)
    time.sleep(args.frequency)
