import ConfigParser

scoutTeam = [ "r3cursive",
    "hollowbandit",
    "monchoon",
    "a slippery stick",
    "omegachan01"
]


cparser = ConfigParser.ConfigParser()
cparser.read('config.ini')
lolapi = LeagueOfLegends(cparser.get('lol','API_KEY'))
