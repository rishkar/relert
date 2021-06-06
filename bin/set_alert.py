import argparse
import sys
import praw
import os

# Define parser and arguments
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--term", required=True)
parser.add_argument("-s", "--subreddit", required=True)
parser.add_argument("-w", "--webhook", required=True)
parser.add_argument("-f", "--frequency")

args = parser.parse_args()

# Preflight Checks
if os.environ['RELERT_CLIENT_ID'] is None:
    print("ERROR: RELERT_CLIENT_ID environment variable not set.")
    sys.exit(1)

if os.environ['RELERT_CLIENT_SECRET'] is None:
    print("ERROR: RELERT_CLIENT_SECRET environment variable not set.")
    sys.exit(1)