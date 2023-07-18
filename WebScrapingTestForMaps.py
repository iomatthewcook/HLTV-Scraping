from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd    
import re

driver = webdriver.Firefox()
url = "https://www.hltv.org/stats/matches/mapstatsid/159792/og-vs-g2?event=6973"
driver.get(url) 

# General setup
content = driver.page_source
soup = BeautifulSoup(content, features='html.parser')
match_links = []
map_links = []

# Data lists setup
eventsnames = []
eventsIDs = []
matchdates = []
maps = []
team1name = []
team2name = []
team1rounds = []
team2rounds = []
team1rating = []
team2rating = []
team1firstkills = []
team2firstkills = []
team1clutches = []
team2clutches = []
team1playerskills = []
team2playerskills = []
team1playersassists = []
team2playersassists = []
team1playersdeaths = []
team2playersdeaths = []
team1playersHSpercent = []
team2playersHSpercent = []
team1playersKAST = []
team2playersKAST = []
team1playersKDdiff = []
team2playersKDdiff = []
team1playersADR = []
team2playersADR = []
team1playersFirstKillDiff = []
team2playersFirstKillDiff = []
team1playersRating = []
team2playersRating = []

match_info_box_div = soup.select('div.match-info-box')[0]

stringsContainingMap = match_info_box_div.find_all(string=True, recursive=False)
mapName = ' '.join(stringsContainingMap[1].split())
maps.append(mapName)
print(mapName)                                                      # Map
a = match_info_box_div.a
tournamentName = a.text
eventsnames.append(tournamentName)                                          
print(a.text)                                                       # Event Name
temp = a.get('href')
temp2 = re.sub(r'[^0-9]', '', temp)
temp2 = temp2[:4]
eventsIDs.append(temp2)
print(temp2)                                                        # Event ID
SmallTextDiv = match_info_box_div.div
SpanDate = SmallTextDiv.span
matchdates.append(SpanDate.text)
print(SpanDate.text)                                                # Date

team1_tag_list = soup.select('div.team-left')
team1name_and_score = team1_tag_list[0].text.split()
team1name.append(team1name_and_score[0])
team1rounds = int(team1name_and_score[1])
print(team1name_and_score[0])                                           # Team 1 Name
print(team1name_and_score[1])                                           # Team 1 Rounds

team2_tag_list = soup.select('div.team-right')
team2name_and_score = team2_tag_list[0].text.split()
team2name.append(team2name_and_score[0])
team2rounds = int(team2name_and_score[1])
print(team2name_and_score[0])                                           # Team 2 Name
print(team2name_and_score[1])                                           # Team 2 Rounds

winning_team_string = ""
if(int(team1name_and_score[1]) > int(team2name_and_score[1])):
    winning_team_string = team1name_and_score[0]
else:
    winning_team_string = team2name_and_score[0]    

step1 = url[46:]
mapID = step1.split('/')[0]
print("Step1: " + step1)



df = pd.DataFrame({'Team1Name':team1name,'Team2Name':team2name, 'Map':maps, 'Date':matchdates, 'Tournament':eventsnames, 'EventID':eventsIDs, 
                   'Team1Rounds':team1rounds, 'Team2Rounds':team2rounds })
df.to_csv('HLTV-Data.csv',index=False)

def remove_extra_spaces(input):
    return ' '.join(input.split())

def remove_brackets(text):
    return text.replace('(', r'').replace(')', r'')

playername = []
playerteam = []
playeropponent = []
playerwonmap = [] #True for win map, False for loss
playermapplayed = []
playermapID = []
playerkills = []
playerassists = []
playerdeaths = []
playerflashassists = []
playerheadshotpercentage = []
playerKAST = []
playerkilldeathdiff = []
playerADR = []
playerfirstkilldiff = []
playerrating = []
playermapdate = []
playertournamentname = []
playertournamentID = []

# This contains both teams'
total_stats_table_tags = soup.select('table.stats-table.totalstats')
for tag in total_stats_table_tags:
    thead_element = tag.find_all('thead')[0]
    thead_element_tr = thead_element.find_all('tr')[0]
    thead_element_tr_th = thead_element_tr.find_all('th')[0]
    print(thead_element_tr_th.text)                             
    tbody_element = tag.find_all('tbody')[0]
    playerstats_trs = tbody_element.find_all('tr')
    for tr in playerstats_trs:
        playerstats_tds = tr.find_all('td')
        pname = remove_extra_spaces(playerstats_tds[0].text)
        playername.append(pname)                                # Player name
        print("Player: " + pname)
        playerteam.append(thead_element_tr_th.text)             # Team name
        print("Team: " + thead_element_tr_th.text)

        if(thead_element_tr_th.text == winning_team_string):
            playerwonmap.append(True)
            print(pname + " won the map.")                      # Player Won Map
        else:
            playerwonmap.append(False)
            print(pname + " lost the map.")

        playermapplayed.append(mapName)                         # Player Map Played
        print("Map: " + mapName)

        playertournamentname.append(tournamentName)             # Player Tournament
        print("Tournament: " + tournamentName)

        playermapdate.append(SpanDate.text)                     # Player Map Date
        print("Date: " + SpanDate.text)

        playermapID.append(mapID)                               # Player Map ID
        print("HLTV Map ID: " + mapID)

        playertournamentID.append("6973")                       # Player Tournament ID

        if(thead_element_tr_th.text == team1name_and_score[0]):
            playeropponent.append(team2name_and_score[0])       # Opponent Team
            print("Opponent Team: " + team2name_and_score[0])
        else:
            playeropponent.append(team1name_and_score[0])
            print("Opponent Team: " + team1name_and_score[0])

        kills_and_headshots = playerstats_tds[1].text.split()       # Looks like ['17', '(9)']
        playerkills.append(kills_and_headshots[0])              # Player Kills
        print("Kills: " + kills_and_headshots[0])
        headshots_count = int(remove_brackets(kills_and_headshots[1]))
        hspercent = round((headshots_count/int(kills_and_headshots[0])), 2)
        playerheadshotpercentage.append(hspercent)              # Player Headshot Percentage
        print("Headshots: " + str(hspercent))

        assists_and_flash_assists = playerstats_tds[2].text.split() # Looks like ['5', '(0)']
        playerassists.append(assists_and_flash_assists[0])      # Player Assists
        print("Assists: " + assists_and_flash_assists[0])

        flash_assists_count = remove_brackets(assists_and_flash_assists[1])
        playerflashassists.append(flash_assists_count)          # Player Flash Assists
        print("Flash Assists: " + flash_assists_count)

        playerdeaths.append(playerstats_tds[3].text)            # Player Deaths
        print("Deaths: " + playerstats_tds[3].text)             

        playerKAST.append(playerstats_tds[4].text)              # Player KAST
        print("KAST: " + playerstats_tds[4].text)

        playerkilldeathdiff.append(playerstats_tds[5].text)     # Player Kill-Death Diff
        print("Kill Death Diff: " + playerstats_tds[5].text)

        playerADR.append(playerstats_tds[6].text)               # Player ADR
        print("ADR: " + playerstats_tds[6].text)

        playerfirstkilldiff.append(playerstats_tds[7].text)     # Player First Kill Diff
        print("First Kill Diff: " + playerstats_tds[7].text)

        playerrating.append(playerstats_tds[8].text)            # Player HLTV Rating 2.0
        print("HLTV Rating 2.0: " + playerstats_tds[8].text)


    
    

players_df = pd.DataFrame({'Username':playername, 'Team': playerteam, 'MapName':playermapplayed, 'Date':playermapdate, 'Tournament':playertournamentname,
                            'Opponent':playeropponent, 'MapResult':playerwonmap,'Rating':playerrating, 'Kills':playerkills, 
                            'Assists':playerassists, 'Deaths':playerdeaths, 'HeadshotPercentage':playerheadshotpercentage, 
                            'KAST':playerKAST, 'KillDeathDiff':playerkilldeathdiff, 'ADR':playerADR, 
                            'FirstKillDiff':playerfirstkilldiff, 'FlashAssists':playerflashassists, 'HltvMapID':playermapID,
                            'HltvTournamentID':playertournamentID})
players_df.to_csv("HLTV-Player-Map-Data.csv")
