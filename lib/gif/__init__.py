import giphy_client
from giphy_client.rest import ApiException
from tecdimisiones import logger
from os import environ

# create an instance of the API class
api_instance = giphy_client.DefaultApi()
api_key = environ["GIF_TOKEN"]

# random_busca = random.choice(["no", "nah", "nope"])


fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)


def random_gif(tag: str = "broken computer"):
    try:
        # Random Endpoint
        api_response = api_instance.gifs_random_get(api_key, tag=tag, fmt=fmt)
        gif = api_response.data.fixed_height_downsampled_url
        return gif

    except ApiException as e:
        logger.log("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)
