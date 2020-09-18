from os import environ as env
import graphics.Config as config
from graphics.Context import DrawContext
from graphics.Twitter import twitter_post


def setup(width, height, **kwargs):
    if config.twitter_post:
        check_env_vars()

    config.DrawContext = DrawContext(
                                     width,
                                     height,
                                     kwargs.get('file_format', config.file_format),
                                     kwargs.get('image_folder', config.image_folder),
                                     kwargs.get('script_name', config.script_name),
                                     kwargs.get('open_file', config.open_file)
                                    )
    config.Context = config.DrawContext.context
    log_info()


def export():
    config.DrawContext.export()

    if config.twitter_post:
        filepath = config.DrawContext.get_fullpath()
        twitter_post(filepath)
        print("INFO: Posted image to twitter")


def log_info():
    print("INFO: Generating image for {}".format(config.script_name))
    print("INFO: Images being saved to directory {}".format(config.image_folder))


def check_env_vars():
    if (not env.get('consumer_key') and
       not env.get('consumer_secret') and
       not env.get('access_token') and
       not env.get('access_token_secret')):
        print("ERROR: You must export consumer_key, consumer_secret, access_token and access_token_secret environment variables")
        exit()
