import tweepy
import graphics.Config as config


def twitter_post(image_location):
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)

    # Post to twitter
    img = image_location
    api.update_with_media(img, status=config.tweet_status)
