# Dependency: py -m pip install tweepy
# py "Tweepytest.py"


# import botconfig as cfg
import tweepy

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

def getConfig(filePath="botconfig.txt"):
    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret
    with open(filePath, 'r') as config:
        configurations = config.readlines()
        for c in configurations:
            line = c.split("=")
            line = [x.replace(" ","").replace("\n","") for x in line]
            if len(line) != 2:
                continue
            elif line[0] == "consumer_key":
                consumer_key = line[1]
            elif line[0] == "consumer_secret":
                consumer_secret = line[1]
            elif line[0] == "access_token":
                access_token = line[1]
            elif line[0] == "access_token_secret":
                access_token_secret = line[1]

getConfig()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)


# Get the User object for twitter...

user = api.get_user('InternetRoaster')

print (user.screen_name)
print (user.followers_count)

for friend in user.friends():
   print (friend.screen_name)
