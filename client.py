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
    """Perform requests to Tracker.gg's API services"""

    def __init__(self, API_KEY: str):
        """
        :param API_KEY: the API key provided by Tracker.gg during the
        creation of your application (you MUST not share it with anyone)
        """
        self.API_KEY = API_KEY
        self.headers = self.get_headers()

    def get_api_key(self):
        """ :rtype: string """
        return self.API_KEY

    def get_headers(self):
        """
        Providing your API key, the header proves that your application is registered
        
        :rtype: dict
        """
        return { 
            "TRN-API-Key": self.API_KEY,
            "Accept": "application/json",
            "Accept-Encoding": "gzip"
        }

    def search_player(self, platform: str, query: dict):
        """
        Returns a dictionary containing useful informations
        about the player (see the documentation)
        :param platform: The platform slug (`steam`, `xbl`, `psn`)
        :param query: a dictionary with the key-value pairs (ex: `{"platform": "steam", "platformUserIdentifier": "76561198085274423"}`)
        
        :rtype: dict / int
        """

        query = urllib.urlencode(query)
        response = requests.get("https://public-api.tracker.gg/v2/splitgate/standard/search?{query}", headers=self.headers)
        if response.status_code in range(200, 299):
            return response.json()
        else:
            return response.status_code

    def get_player_stats(self, platform: str, user_identifier: str):
        """
        Return a dictionary with the career stats of the player
        :param platform: The platform slug (`steam`, `xbl`, `psn`)
        :param user_identifier: The user's handle on the platform (for example Steam ID). If the player
        is a Steam player, you can obtain by calling `search_player()` and accessing it via 
        `response["data"][0]["platformUserIdentifier"]``, otherwise it's the XBL/PSN username
        
        :rtype: dict / int
        """

        response = requests.get(f"https://public-api.tracker.gg/v2/splitgate/standard/profile/{platform}/{user_identifier}", headers=self.headers)
        if response.status_code in range(200, 300):
            return response.json()
        else:
            return response.status_code

        def get_platform_info(response: dict):
            """
            Return the user's platform informations

            :param response: The dict returned by `get_player_stats()`

            :rtype: dict
            """
            return {
                "plaftormSlug": response["data"]["platformInfo"]["plaftormSlug"],
                "platformUserId": response["data"]["platformInfo"]["plaftormUserId"],
                "plaftormUserHandle": response["data"]["platformInfo"]["plaftormUserHandle"],
                "platformUserIdentifier": response["data"]["platformInfo"]["platformUserIdentifier"],
                "avatarUrl": response["data"]["platformInfo"]["avatarUrl"],
                "additionalParameters": response["data"]["platformInfo"]["additionalParameters"]
            }

        def get_profile_info(response: dict):
            """
            Return the user's profile informations 

            :param response: The dict returned by `get_player_stats()`

            :rtype: dict
            """
            return {
                "userId": response["data"]["userInfo"]["userId"],
                "isPremium": response["data"]["userInfo"]["isPremium"],
                "isVerified": response["data"]["userInfo"]["isVerified"],
                "isInfluencer": response["data"]["userInfo"]["isInfluencer"],
                "isPartner": response["data"]["userInfo"]["isPartner"],
                "countryCode": response["data"]["userInfo"]["countryCode"],
                "customAvatarUrl": response["data"]["userInfo"]["customAvatarUrl"],
                "customHeroUrl": response["data"]["userInfo"]["customHeroUrl"],
                "socialAccounts": [x for x in response["data"]["userInfo"]["socialAccounts"]], # contains platformSlug, platformUserHandle, platformUserIdentifier
                "pageviews": response["data"]["userInfo"]["pageviews"],
                "isSuspicious": response["data"]["userInfo"]["isSuspicious"]
            }

        def get_stat(response: dict, stat: str):
            """
            Return the user statistic

            :param response: The dict returned by `get_player_stats()`
            :param stat: The stat you are looking for (see the documentation for more informations)

            :rtype: dict
            """
            return {
                "rank": response["data"]["segments"][0]["stats"][stat]["rank"],
                "percentile": response["data"]["segments"][0]["stats"][stat]["percentile"],
                "displayName": response["data"]["segments"][0]["stats"][stat]["displayName"],
                "displayCategory": response["data"]["segments"][0]["stats"][stat]["displayCategory"],
                "category": response["data"]["segments"][0]["stats"][stat]["category"],
                "metadata": response["data"]["segments"][0]["stats"][stat]["metadata"], # can contain extra data such as an image url
                "value": response["data"]["segments"][0]["stats"][stat]["value"],
                "displayValue": response["data"]["segments"][0]["stats"][stat]["displayValue"],
                "displayType": response["data"]["segments"][0]["stats"][stat]["displayType"]
            }
