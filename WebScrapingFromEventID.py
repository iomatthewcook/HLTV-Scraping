from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd    

driver = webdriver.Firefox()

eventID = "6973" #Set event ID here, eventually upgrade to from text file.
#Use 7177 for a single match 2-0
hltv_url = 'https://www.hltv.org'
event_url_without_eventID = "https://www.hltv.org/results?event="
driver.get(event_url_without_eventID + eventID)

content = driver.page_source
soup = BeautifulSoup(content, features='html.parser')
match_links = []
map_links = []

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

def remove_extra_spaces(input):
    return ' '.join(input.split())

def remove_brackets(text):
    return text.replace('(', r'').replace(')', r'')

# Gets all links for matches in the event from the event page.
for match_info_box_a in soup.find_all(attrs={'class': 'result-con'}):
    for child in match_info_box_a.children:
        link = child.get('href')
        match_links.append(link)

for match_link in match_links:
    match_url = hltv_url + match_link
    driver.get(match_url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    stats_tags = soup.select('a.results-stats') 
    for a_tag in stats_tags:
        map_links.append(a_tag.get('href'))

for map_link in map_links:
    print(map_link)
    map_url = hltv_url + map_link
    driver.get(map_url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')

    match_info_box_div = soup.select('div.match-info-box')[0]
    stringsContainingMap = match_info_box_div.find_all(string=True, recursive=False)
    mapName = ' '.join(stringsContainingMap[1].split())
    tournamentName = match_info_box_div.a.text
    map_date = match_info_box_div.div.span.text
    
    team1_tag = soup.select('div.team-left')[0]
    team1name = team1_tag.a.text
    team1rounds = team1_tag.div.text

    team2_tag = soup.select('div.team-right')[0]
    team2name = team2_tag.a.text
    team2rounds = team2_tag.div.text

    winning_team_string = ""
    if(team1rounds > team2rounds):
        winning_team_string = team1name
    else:
        winning_team_string = team2name

    map_ID = map_url[46:].split('/')[0]

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
            print("'" + team1name + "' '" + team2name + "'")
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

            playermapdate.append(map_date)                     # Player Map Date
            print("Date: " + map_date)

            playermapID.append(map_ID)                               # Player Map ID
            print("HLTV Map ID: " + map_ID)

            playertournamentID.append(eventID)                       # Player Tournament ID

            if(thead_element_tr_th.text == team1name):
                playeropponent.append(team2name)       # Opponent Team
                print("Opponent Team: " + team2name)
            else:
                playeropponent.append(team1name)
                print("Opponent Team: " + team1name)

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
players_df.to_csv("HLTV-Player-Map-Data.csv", index=False)