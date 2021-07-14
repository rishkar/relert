import os
import sys
import argparse
import re
from time import sleep

import requests
import praw
import prawcore

# Define parser and arguments
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--regex", required=True, help="The regexes, separated by commas, to run against the post"
                                                         " titles")
parser.add_argument("-s", "--subreddit", required=True, help="The subreddit to search.")
parser.add_argument("-w", "--webhook", required=True, help="The Discord webhook to send messages to.")
parser.add_argument("--retries", default=5, help="Number of times to retry upon a failed connection to reddit. Defaults"
                                                 " to 5.")

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

# Start listening to the stream and let us know if something shows up.
num_retries = 0
wait_seconds = 15
while True:
    try:
        for submission in subreddit_con.stream.submissions():
            num_retries = 0
            wait_seconds = 15
            # If the submission matches our term, let's send an alert!
            for regex in str(args.regex).split(','):
                if re.search(regex, submission.title) is not None:
                    print("Submission title \"%s\" matches specified regex \"%s\". Sending to discord..." %
                          (submission.title, regex))
                    message = "-----\nRELERT: Regex *\"%s\"* match found in Subreddit *\"r/%s\"*:\n\n" \
                              "**Submission Title:** %s\n**Link:** %s" % \
                              (regex, args.subreddit, submission.title, submission.url)
                    requests.post(args.webhook, {"content": message, "username": "r/"+args.subreddit})
    except prawcore.exceptions.ServerError as e:
        num_retries += 1
        print(e)
        if num_retries > args.retries:
            print("Max number of retries reached, shutting down for now.")
            sys.exit(1)
        else:
            print("Sleeping for %d seconds. I will make %d more attempts before shutting down." %
                  (wait_seconds, args.retries - num_retries))
            wait_seconds *= 2
            sleep(wait_seconds)
