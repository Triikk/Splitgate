"""
A small API wrapper for Tracker.gg's Splitgate web API
This module only provides methods for searching a Splitgate player and getting a Splitgate
player's profile stats, since these are the only two methods available in the Tracker.gg's API at the moment.
Documentation: https://tracker.gg/developers/docs/titles/splitgate
"""

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

        def get_platform_info(self, response: dict):
            """
            Return the user's platform informations

            :param response: The dict returned by `get_player_stats()`

            :rtype: dict
            """
            
            platform_info = response["data"]["platformInfo"]
            return {
                "plaftormSlug": platform_info["plaftormSlug"],
                "platformUserId": platform_info["plaftormUserId"],
                "plaftormUserHandle": platform_info["plaftormUserHandle"],
                "platformUserIdentifier": platform_info["platformUserIdentifier"],
                "avatarUrl": platform_info["avatarUrl"],
                "additionalParameters": platform_info["additionalParameters"]
            }

    def get_user_info(self, response: dict):
        """
        Return the user's profile informations 

        :param response: The dict returned by `get_player_stats()`

        :rtype: dict
        """

        user_info = response["data"]["userInfo"]
        return {
            "userId": user_info["userId"],
            "isPremium": user_info["isPremium"],
            "isVerified": user_info["isVerified"],
            "isInfluencer": user_info["isInfluencer"],
            "isPartner": user_info["isPartner"],
            "countryCode": user_info["countryCode"],
            "customAvatarUrl": user_info["customAvatarUrl"],
            "customHeroUrl": user_info["customHeroUrl"],
            "socialAccounts": [x for x in user_info["socialAccounts"]], # platformSlug, platformUserHandle, platformUserIdentifier
            "pageviews": user_info["pageviews"],
            "isSuspicious": user_info["isSuspicious"]
        }

    def get_user_stat(self, response: dict, stat: str):
        """
        Return the user statistic

        :param response: The dict returned by `get_player_stats()`
        :param stat: The stat you are looking for (see the documentation for more informations)

        :rtype: dict
        """

        statistic = response["data"]["segments"][0]["stats"][stat]
        return {
            "rank": statistic["rank"],
            "percentile": statistic["percentile"],
            "displayName": statistic["displayName"],
            "displayCategory": statistic["displayCategory"],
            "category": statistic["category"],
            "metadata": statistic["metadata"], # can contain extra data such as an image url
            "value": statistic["value"],
            "displayValue": statistic["displayValue"],
            "displayType": statistic["displayType"]
        }
