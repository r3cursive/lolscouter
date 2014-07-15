"""
Python Library for League of Legends
"""
__author__ = 'r3cursive'
import json
import urllib


class PyLeague:
    api_endpoint = 'https://na.api.pvp.net/api/lol'

    def __init__(self, api_key, api_version='1.4', api_reigon='na'):
        self.api_key = api_key
        self.api_version = api_version
        self.api_reigon = api_reigon
        self.api_url = self.api_endpoint + '/' + api_reigon + '/' + 'v' + api_version + '/'

    def summoner_by_name(self, summoner_name=''):
        if summoner_name == '':
            return
        url = self.api_url + 'summoner/by-name/%s?api_key=%s' % (summoner_name, self.api_key)
        response = json.loads(urllib.urlopen(url).read())
        # print response
        return response[response.keys()[0]]['id']

    def get_summoners_id_by_names(self,summoner_names=[]):
        if not summoner_names:
            return
        summoner_array = []
        for summoner in summoner_names:
            summoner_array.append(self.summoner_by_name(summoner))
        return summoner_array
