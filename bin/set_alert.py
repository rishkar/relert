import os
import sys
import argparse
import re
import requests
import praw
import prawcore

# Define parser and arguments
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--regex", required=True, help="The regexes, separated by commas, to run against the post"
                                                         " titles")
parser.add_argument("-s", "--subreddit", required=True, help="The subreddit to search.")
parser.add_argument("-w", "--webhook", required=True, help="The Discord webhook to send messages to.")

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
for submission in subreddit_con.stream.submissions():
    # If the submission matches our term, let's send an alert!
    for regex in str(args.regex).split(','):
        if re.search(regex, submission.title) is not None:
            print("Submission title \"%s\" matches specified regex \"%s\". Sending to discord..." % (submission.title, regex))
            message = "-----\nRELERT: Regex *\"%s\"* match found in Subreddit *\"r/%s\"*:\n\n" \
                      "**Submission Title:** %s\n**Link:** %s" % \
                      (regex, args.subreddit, submission.title, submission.url)
            requests.post(args.webhook, {"content": message, "username": "r/"+args.subreddit})
