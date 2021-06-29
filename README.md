# Relert
### A relatively simple bot that alerts you when your phrase is detected on a certain subreddit post
It's essentially as simple as it sounds. You give it a subreddit to watch, a phrase to monitor, and a discord webhook and it'll alert you if your phrase is found in the title of any post.

## INSTRUCTIONS
1. [Obtain a bot token and secret from reddit.](https://www.reddit.com/prefs/apps). I used a script app type and set the redirect URI to localhost.
2. Set the aforementioned bot token and secret as environmental variables `RELERT_CLIENT_ID` and `RELERT_CLIENT_SECRET`. Relert will not work unless these are set.
3. Make sure praw is installed before you run the script: `pip install praw`
4. Run `bin/set_alert.py` with the appropriate arguments (use `--help` to get a list) to get this bot up and running! You can exit with `Ctrl+C` or any of your other process murdering techniques.


## FAQ

### -Why?
I'm getting tired of missing decent deals on r/homelabsales and r/hardwareswap. Also, I like using PRAW!

### -Can't you just use one of the many reddit bots that already exist?
Of course but that would be smart and efficient, which we don't do here.

### -Is this gonna become a full-fledged program?
Probably not. At most there's gonna be a config that takes your reddit token and whatnot, but I think the rest of the parameters will be supplied as command line options to the program.
