def welcome():
	return "Welcome to Bardle!"

def game_rules():
	return "For the first three categories, XXX/OOO will tell you if you have the incorrect/correct value.\nFor Divsion, it is not based on the league.\nFor HR, RBIs, and AVG, ↑↑ will tell you that the player you guessed has a higher value than the Bardle\nand ↓↓ will tell you that the player you guessed has a lower value.\nOO means that the player you guessed has the same value as the Bardle.\nThe Bardle had at least 324 PAs in 2021."

def display_board(board):
    os.system('clear')
    print('TM' + '|' + 'LG' + '|' + 'DIV' + '|' + 'HR' + '|' + 'RBI' + '|' + 'AVG')
    print(board[1] + '|' + board[11] + '|' + board[21] + '|' + board[31] + '|' + board[41] + '|' + board[51])
    print(board[101] + '|' + board[201] + '|' + board[301] + '|' + board[401] + '|' + board[501] + '|' + board[601])
    print(board[2] + '|' + board[12] + '|' + board[22] + '|' + board[32] + '|' + board[42] + '|' + board[52])
    print(board[102] + '|' + board[202] + '|' + board[302] + '|' + board[402] + '|' + board[502] + '|' + board[602])
    print(board[3] + '|' + board[13] + '|' + board[23] + '|' + board[33] + '|' + board[43] + '|' + board[53])
    print(board[103] + '|' + board[203] + '|' + board[303] + '|' + board[403] + '|' + board[503] + '|' + board[603])
    print(board[4] + '|' + board[14] + '|' + board[24] + '|' + board[34] + '|' + board[44] + '|' + board[54])
    print(board[104] + '|' + board[204] + '|' + board[304] + '|' + board[404] + '|' + board[504] + '|' + board[604])
    print(board[5] + '|' + board[15] + '|' + board[25] + '|' + board[35] + '|' + board[45] + '|' + board[55])
    print(board[105] + '|' + board[205] + '|' + board[305] + '|' + board[405] + '|' + board[505] + '|' + board[605])
    print(board[6] + '|' + board[16] + '|' + board[26] + '|' + board[36] + '|' + board[46] + '|' + board[56])
    print(board[106] + '|' + board[206] + '|' + board[306] + '|' + board[406] + '|' + board[506] + '|' + board[606])
    print(board[7] + '|' + board[17] + '|' + board[27] + '|' + board[37] + '|' + board[47] + '|' + board[57])
    print(board[107] + '|' + board[207] + '|' + board[307] + '|' + board[407] + '|' + board[507] + '|' + board[607])



def place_stats(board, player, turn, year):
    board[turn] = findplayerstats2(player,year)[0]
    board[turn+10] = findplayerstats2(player,year)[1]
    board[turn+20] = findplayerstats2(player,year)[2]
    board[turn+30] = findplayerstats2(player,year)[3]
    board[turn+40] = findplayerstats2(player,year)[4]
    board[turn+50] = findplayerstats2(player,year)[5]


class InvalidPlayer(Exception):
    pass

def player_choice():
    while True:
        player = input('Please choose a player')
        try:
            playersplit_id2(player)
            break
        except IndexError:
            print('Sorry, but I could not find the player you chose.')
            continue
    return player.lower()



def replay():
    choice = input('Would you like to play again? Yes or No')
    return choice.lower() == 'yes'


def bardletwo(bardle, player, board, turn):
    for x in range(0,3):
        if findplayerstats2(playersplit_id2(player),2021)[x] == findplayerstats2(playersplit_id2(bardle),2021)[x]:
            board[turn+100*(x+1)] = 'OOO'
        else:
            board[turn+100*(x+1)] = 'XXX'
    for x in range(3,6):
            if int(findplayerstats2(playersplit_id2(player),2021)[x]) == int(findplayerstats2(playersplit_id2(bardle),2021)[x]):
                board[turn+100*(x+1)] = 'OO'
            elif int(findplayerstats2(playersplit_id2(player),2021)[x]) > int(findplayerstats2(playersplit_id2(bardle),2021)[x]):
                board[turn+100*(x+1)] = '↑↑'
            else:
                board[turn+100*(x+1)] = '↓↓'
    return display_board(board) 


def player_choice():
    while True:
        player = input('Please choose a player')
        try:
            playersplit_id2(player)
            break
        except IndexError:
            print('Sorry, but I could not find the player you chose.')
            continue
    return player.lower()


def war_lookup(playerid, year):
    df_warlookup = dfwar[dfwar['player_ID'] == playerid][dfwar['year_ID'] == year]
    return round(df_warlookup.iloc[0][16],1)




def div_lookup(team):
    EAST = ['WAS','NYN','ATL','MIA','PHI','BOS','NYA','BAL','TOR','TBA']
    CEN = ['CHN','SLN','PIT','CIN','MIL','CHA','CLE','KCA','MIN','DET']
    WEST = ['LAN','SFN','COL','ARI','SDN','LAA','OAK','SEA','HOU','TEX']
    if team in EAST:
        return 'EST'
    elif team in CEN:
        return 'CEN'
    elif team in WEST:
        return 'WST'
    else:
        'NOT'



def findplayerstats2(playerID, year):
    attributeslist=[]
    updatedPID = ''
    if playerID == 'ramirjo02':
        updatedPID += 'ramirjo01'
        df_new1 = df[df['playerID'] == updatedPID][df['yearID'] == year]
        attributeslist.append(df_new1.iloc[0][3])
        attributeslist.append(df_new1.iloc[0][4])
        attributeslist.append(div_lookup(df_new1.iloc[0][3]))
        attributeslist.append(str(df_new1.iloc[0][11]))
        attributeslist.append(str(round(df_new1.iloc[0][12])))
        attributeslist.append(str(round(df_new1.iloc[0][8]/df_new1.iloc[0][6]*1000)))
    else:
        updatedPID += playerID
        df_new1 = df[df['playerID'] == updatedPID][df['yearID'] == year]
        attributeslist.append(df_new1.iloc[0][3])
        attributeslist.append(df_new1.iloc[0][4])
        attributeslist.append(div_lookup(df_new1.iloc[0][3]))
        attributeslist.append(str(df_new1.iloc[0][11]))
        attributeslist.append(str(round(df_new1.iloc[0][12])))
        attributeslist.append(str(round(df_new1.iloc[0][8]/df_new1.iloc[0][6]*1000)))
    return attributeslist



def playersplit_id2(playername):
    if len(playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]))>1:
        return playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]).iloc[len(playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]))-1][4]
    elif len(playername.split())>2:
        return playerid_lookup(playername.lower().split()[2],playername.lower().split()[0]+" "+playername.lower().split()[1]).iloc[0][4]
    return playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]).iloc[0][4]

def display_board2(board):
	return(board[1] + '|' + board[11] + '|' + board[21] + '|' + board[31] + '|' + board[41] + '|' + board[51]
	+ "</br>" +
	board[101] + '|' + board[201] + '|' + board[301] + '|' + board[401] + '|' + board[501] + '|' + board[601]
	+ "</br>" +
	board[2] + '|' + board[12] + '|' + board[22] + '|' + board[32] + '|' + board[42] + '|' + board[52]
	+ "</br>" +
	board[102] + '|' + board[202] + '|' + board[302] + '|' + board[402] + '|' + board[502] + '|' + board[602]
	+ "</br>" +
	board[3] + '|' + board[13] + '|' + board[23] + '|' + board[33] + '|' + board[43] + '|' + board[53]
	+ "</br>" +
	board[103] + '|' + board[203] + '|' + board[303] + '|' + board[403] + '|' + board[503] + '|' + board[603]
	+ "</br>" +
	board[4] + '|' + board[14] + '|' + board[24] + '|' + board[34] + '|' + board[44] + '|' + board[54]
	+ "</br>" +
	board[104] + '|' + board[204] + '|' + board[304] + '|' + board[404] + '|' + board[504] + '|' + board[604]
	+ "</br>" +
	board[5] + '|' + board[15] + '|' + board[25] + '|' + board[35] + '|' + board[45] + '|' + board[55]
	+ "</br>" +
	board[105] + '|' + board[205] + '|' + board[305] + '|' + board[405] + '|' + board[505] + '|' + board[605]
	+ "</br>" +
	board[6] + '|' + board[16] + '|' + board[26] + '|' + board[36] + '|' + board[46] + '|' + board[56]
	+ "</br>" +
	board[106] + '|' + board[206] + '|' + board[306] + '|' + board[406] + '|' + board[506] + '|' + board[606]
	+ "</br>" +
	board[7] + '|' + board[17] + '|' + board[27] + '|' + board[37] + '|' + board[47] + '|' + board[57]
	+ "</br>" +
	board[107] + '|' + board[207] + '|' + board[307] + '|' + board[407] + '|' + board[507] + '|' + board[607]
	+ "</br>")

def place_stats2(board, stats, turn):
    board[turn] = stats[0]
    board[turn+10] = stats[1]
    board[turn+20] = stats[2]
    board[turn+30] = stats[3]
    board[turn+40] = stats[4]
    board[turn+50] = stats[5]

def bardletwo_zero(bardle_stats, player_stats, board, turn):
    for x in range(0,3):
        if player_stats[x] == bardle_stats[x]:
            board[turn+100*(x+1)] = '[OO]'
        else:
            board[turn+100*(x+1)] = '[XX]'
    for x in range(3,6):
            if player_stats[x] == bardle_stats[x]:
                board[turn+100*(x+1)] = '[OO]'
            elif player_stats[x] > bardle_stats[x]:
                board[turn+100*(x+1)] = '[↑↑]'
            else:
                board[turn+100*(x+1)] = '[↓↓]'

def bardle_comp(player, bardle):
    comp = []
    for x in range(0,3):
        if findplayerstats2(playersplit_id2(player),2021)[x] == findplayerstats2(playersplit_id2(bardle),2021)[x]:
            comp.append('OOO')
        else:
            comp.append('XXX')
    for x in range(3,6):
            if int(findplayerstats2(playersplit_id2(player),2021)[x]) == int(findplayerstats2(playersplit_id2(bardle),2021)[x]):
                comp.append('OO')
            elif int(findplayerstats2(playersplit_id2(player),2021)[x]) > int(findplayerstats2(playersplit_id2(bardle),2021)[x]):
                comp.append('↑↑')
            else:
                comp.append('↓↓')
    return comp

def player_check2(player):
        try:
            playersplit_id2(player)
        except IndexError:
            return False



def display_guess1(board):
	return(board[1] + '|' + board[11] + '|' + board[21] + '|' + board[31] + '|' + board[41] + '|' + board[51])
