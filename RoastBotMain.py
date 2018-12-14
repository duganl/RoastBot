# py "RoastBotMain.py"

# Program uses Python-twitter API
# import botconfig as cfg
# impot datetime and time
import twitter
import datetime
import time
# import functions from other files needed to run
from linuxprint import linuxprint
from Servo import servo
from camera import camera


#import and configure the config file

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

#create the actual api
api = twitter.Api(consumer_key = consumer_key,
                  consumer_secret = consumer_secret,
                  access_token_key = access_token,
                  access_token_secret = access_token_secret)


#initialize variables that will be printed by receipt
name_to_print = ""
handle_to_print = ""
tweet_to_print = ""


#create a dictionary to convert Month String into month int
date_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

#initalize the last_time variable
last_time = datetime.datetime.now() - datetime.timedelta(hours = 1)

while (True):
#perform a query for tweets containing the appropriate hashtag & quoted text
    results = api.GetSearch(
            raw_query="q=%23RoastMeIGR&src=typd")
#initialize tweet_to_print, handle_to_print, name_to_print
    handle_to_print = None
    name_to_print = None
    tweet_to_print = None

    for result in results:
        text = result.text
        quote = result.quoted_status
        if text is not None and quote is not None:
            if ("#RoastMeIGR" in text):
#convert the date output from string into datetime datatype
                split_date = result.created_at.split(" ")
                inner_split = split_date[3].split(":")
                create_date = datetime.datetime(year=int(split_date[5]), month=date_dict[split_date[1]], day=int(split_date[2]), hour=int(inner_split[0]), minute=int(inner_split[1]), second=int(inner_split[2]))
                create_date = create_date - datetime.timedelta(hours=5)

#diagnostic methods are below to check the dattime is correct; confirm with twtter:
                # print(create_date)
                # print(last_time)
                # print(text)
                # print(result.user.name)
                # print(quote.user.name)

                if (create_date > last_time):
                    name_to_print = quote.user.name
                    handle_to_print = quote.user_id
                    tweet_to_print = quote.text

                    #Write the tweet to an outfile to be printed
                    with open('Tweet.txt', 'w') as outfile:
                        outfile.write(name_to_print)
                        outfile.write(handle_to_print)
                        outfile.write(tweet_to_print)
                    break

    # Print The Tweet using the linuxprint function
    linuxprint()
    time.sleep(10)
    # Call the Servo Function to move the servo and trigger flames
    servo()
    # Call Camera to take after image
    takeimage()
    # Upload Image to twitter
    status = api.PostUpdate("A tweet from %s has been roasted" % (handle_to_print), media = "/sd/image.jpg")


    last_time = datetime.datetime.now()

    time.sleep(3600)
