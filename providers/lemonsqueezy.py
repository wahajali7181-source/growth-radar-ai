import requests

from config.settings import (
    LEMON_SQUEEZY_API,
    LEMON_STORE_ID
)


class LemonSqueezy:

    def __init__(self):

        self.api_key = LEMON_SQUEEZY_API

        self.store_id = LEMON_STORE_ID

        self.headers = {

            "Accept": "application/vnd.api+json",

            "Authorization": f"Bearer {self.api_key}",

            "Content-Type": "application/vnd.api+json"

        }