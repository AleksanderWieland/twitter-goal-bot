import tweepy
import random
import constants

# credentials to access Twitter API
API_KEY= str(constants.API_KEY)
API_KEY_SECRET=str(constants.API_KEY_SECRET)

BEARER_TOKEN=str(constants.BEARER_TOKEN)

ACCESS_TOKEN=str(constants.ACCESS_TOKEN)
ACCESS_TOKEN_SECRET=str(constants.ACCESS_TOKEN_SECRET)


# create an OAuthHandler instance
client = tweepy.Client(
    BEARER_TOKEN,
    API_KEY,
    API_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)

# create a tweet
def send_tweet(text):
    try:
        client.create_tweet(text=str(text))
        print(text)
        print("Tweet has been published.")
    except tweepy.errors.Forbidden as e:
        # Check if the error is related to duplicate tweets
        if "You are not allowed to create a Tweet with duplicate content" in str(e):
            print("Error: Duplicate tweet. You cannot send the same tweet twice.")
        else:
            # Other Forbidden errors
            print(f"A Forbidden error occurred: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"Another error occurred: {e}")
