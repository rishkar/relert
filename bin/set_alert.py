import argparse
import praw

# Define parser and arguments
parser = argparse.ArgumentParser()

parser.add_argument("--token", required=True)
parser.add_argument("-t", "--term", required=True)
parser.add_argument("-s", "--subreddit", required=True)
parser.add_argument("-w", "--webhook", required=True)
parser.add_argument("-f", "--frequency")

args = parser.parse_args()