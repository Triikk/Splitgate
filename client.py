"""
A small API wrapper for Tracker.gg's Splitgate web API

This module only provides methods for searching a Splitgate player and getting a Splitgate
player's profile stats, since these are the only two methods available in the Tracker.gg's API at the moment.

Documentation: https://tracker.gg/developers/docs/titles/splitgate
"""

__author__ = "Triikk"

import requests
import urllib
from os import getenv

class Client():

    def __init__(self, API_KEY: str):
        self.API_KEY = API_KEY
        self.headers = self.get_headers()

    def get_api_key(self):
        return self.API_KEY

    def get_headers(self):
        """
        Providing your API key, the header proves that your application is registered
        """
        return { 
            "TRN-API-Key": self.API_KEY,
            "Accept": "application/json",
            "Accept-Encoding": "gzip"
        }

    def search_player(self, platform: str, query: dict):
        """
        Given a platforms and a query, this method returns a JSON object
        containing useful informations, such as the platformUserIdentifier, the avatar URL exc. (see the documentation to get more informations)

        plaftorm: The platform slug (`steam`, `xbl`, `psn`)
        query: a dictionary with the key-value pairs (example: `{"platform": "steam", "platformUserIdentifier": "76561198085274423"}`)
        """

        query = urllib.urlencode(query)
        response = requests.get("https://public-api.tracker.gg/v2/splitgate/standard/search?{query}", headers=self.headers)
        if response.status_code in range(200, 299):
            return response.json()
        else:
            return response.status_code

    def get_player_stats(self, platform: str, user_identifier: str):
        """
        Return a JSON object with the career stats of the Splitgate player

        platform: The platform slug (`steam`, `xbl`, `psn`)
        user_identifier: The user's handle on the platform (for example Steam ID). If the player is a Steam player, you can obtain by calling `search_player()` and accessing it via `response["data"][0]["platformUserIdentifier"]``, otherwise it's just the XBL/PSN username
        """

        response = requests.get(f"https://public-api.tracker.gg/v2/splitgate/standard/profile/{platform}/{user_identifier}", headers=self.headers)
        if response.status_code in range(200, 300):
            return response.json()
        else:
            return response.status_code
