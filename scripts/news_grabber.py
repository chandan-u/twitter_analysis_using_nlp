
import tweepy

from grabbers.twitter import MyStreamListener



consumer_key="XndPZDzoIxpVT4rysz81X5OA9"
consumer_secret="LZIhZ56oCwhxFkZGo1sgJMINRYmp2sfkcgcq8CtRQsXTjAGObN"

access_token="278628386-Sns1CwGu0mfQI9MqdwlONY6PXNA5uUKApQRLlDts"
access_token_secret="TdfMvqLREdhkHXSFX4rwltQFMNZRuPSr2AtJHCmY2wZRY"







if __name__ == '__main__':

    # default prefix is News
    myStreamListener = MyStreamListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # stream
    stream = tweepy.Stream(auth, myStreamListener)

    # bounding box: http://www.mapdevelopers.com/geocode_bounding_box.php
    # longitude lattitude pairs with south west corner being first
    #stream.filter(locations=[-86.328121, 39.632177, -85.937379, 39.927392], async=True)
    stream.filter(track =['#News'], languages=['en'], async=True)
