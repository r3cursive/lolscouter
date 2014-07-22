"""
Python Library for League of Legends with elophant match history
"""
__author__ = 'r3cursive'
import json
import urllib
from lxml import etree

class PyLeague:
    api_endpoint = 'https://na.api.pvp.net/api/lol'

    def __init__(self, api_key, api_version='1.4', api_reigon='na'):
        self.api_key = api_key
        self.api_version = api_version
        self.api_reigon = api_reigon
        self.api_url = self.api_endpoint + '/' + api_reigon + '/' + 'v' + api_version + '/'

    def get_summoner_by_name(self, summoner_name=''):
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

    def get_elophant_match_history(self, summoner_id):
        if not summoner_id:
            return
        etparser = etree.HTML(urllib.urlopen('http://www.elophant.com/league-of-legends/summoner/na/%s/recent-games' %
                                             summoner_id).read())
        recent_boxes = etparser.xpath('//div[@id="tab-recent-matches"]/div[@class="box"]')
        champhist = {}
        for box in recent_boxes:
            match = {}
            #TODO: ignore if match isn't ranked / normal / teambuilder
            match['champion'] = box.xpath('./div/div[@class="pic"]/a/div[@class="title"]')[0]\
                .text
            match['outcome'] = \
                box.xpath('./div/div[@class="desc self-clear"]/div[@class="game-info"]/div/span')[0]\
                    .text
            match['length'] = \
                box.xpath('./div/div[@class="desc self-clear"]/div[@class="game-info"]/div/span')[1]\
                    .text
            match['kills'] = \
                box.xpath('./div/div[@class="desc self-clear"]/div[@class="kda-stats"]/div/div[@class="kills"]/span')[0]\
                    .text.split(' ')[0]
            match['deaths'] = \
                box.xpath('./div/div[@class="desc self-clear"]/div[@class="kda-stats"]/div/div[@class="deaths"]/span')[0]\
                    .text.split(' ')[0]
            match['assists'] = \
                box.xpath('./div/div[@class="desc self-clear"]/div[@class="kda-stats"]/div/div[@class="assists"]/span')[0]\
                    .text.split(' ')[0]
            try:
                match['kda-stats'] = \
                    float((int(match['kills'])+int(match['assists']))/int(match['deaths']))
            except ZeroDivisionError:
                match['kda-stats'] = int(match['kills'])+int(match['assists'])

            match['id'] = hash(frozenset(match.items()))

            if match['champion'] in champhist:
                champhist[match['champion']].append(match)
            else:
                matcharray = []
                matcharray.append(match)
                champhist[match['champion']] = matcharray

        return champhist