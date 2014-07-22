import ConfigParser
import pyleague
import gspread
scout_team = [ "r3cursive",
    "hollowbandit",
    "monchoon",
    "a slippery stick",
    "omegachan01"
]


cparser = ConfigParser.ConfigParser()
cparser.read('config.ini')
lolapi = pyleague.PyLeague(cparser.get('lol', 'api_key'))
gs = gspread.login(cparser.get('google', 'username'),cparser.get('google', 'password'))

sheet = gs.open('ScoutSheet')

teamdict = {}
for user in scout_team:
    user_matches = lolapi.get_elophant_match_history(lolapi.get_summoner_by_name(user))
    try:
        usersheet = sheet.worksheet(user)
    except gspread.WorksheetNotFound:
        usersheet = sheet.add_worksheet(title=user, rows=500, cols=20)
        usersheet = sheet.worksheet(user)

    usersheet.update_cell(0, 0, 'champion')
    usersheet.update_cell(1, 0, 'outcome')
    usersheet.update_cell(2, 0, 'length')
    usersheet.update_cell(3, 0, 'kills')
    usersheet.update_cell(4, 0, 'deaths')
    usersheet.update_cell(5, 0, 'assists')
    usersheet.update_cell(6, 0, 'kda')
    usersheet.update_cell(7, 0, 'id')
    # i dont know a better way to track these :(
    sheet_Y = 1
    import ipdb; ipdb.set_trace()
    for key in user_matches.keys():
        for match in user_matches[key]:
            usersheet.update_cell(0, sheet_Y, match['champion'])
            usersheet.update_cell(1, sheet_Y, match['outcome'])
            usersheet.update_cell(2, sheet_Y, match['length'])
            usersheet.update_cell(3, sheet_Y, match['kills'])
            usersheet.update_cell(4, sheet_Y, match['deaths'])
            usersheet.update_cell(5, sheet_Y, match['assists'])
            usersheet.update_cell(6, sheet_Y, match['kda-stats'])
            usersheet.update_cell(7, sheet_Y, match['id'])
            sheet_Y += 1
