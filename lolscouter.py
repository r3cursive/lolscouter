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

    usersheet.update_cell(1, 1, 'champion')
    usersheet.update_cell(1, 2, 'outcome')
    usersheet.update_cell(1, 3, 'length')
    usersheet.update_cell(1, 4, 'kills')
    usersheet.update_cell(1, 5, 'deaths')
    usersheet.update_cell(1, 6, 'assists')
    usersheet.update_cell(1, 7, 'kda')
    usersheet.update_cell(1, 8, 'id')
    # i dont know a better way to track these :(
    sheet_Y = len(usersheet.col_values(1)) + 1
    test_cell = "I1"
    for key in user_matches.keys():
        for match in user_matches[key]:
            usersheet.update_acell(test_cell, match['id'])
            #import ipdb; ipdb.set_trace()
            if len(usersheet.findall(usersheet.acell(test_cell).value)) < 2:
                usersheet.update_cell(sheet_Y, 1, match['champion'])
                usersheet.update_cell(sheet_Y, 2, match['outcome'])
                usersheet.update_cell(sheet_Y, 3, match['length'])
                usersheet.update_cell(sheet_Y, 4, match['kills'])
                usersheet.update_cell(sheet_Y, 5, match['deaths'])
                usersheet.update_cell(sheet_Y, 6, match['assists'])
                usersheet.update_cell(sheet_Y, 7, match['kda-stats'])
                usersheet.update_cell(sheet_Y, 8, match['id'])
                sheet_Y += 1
