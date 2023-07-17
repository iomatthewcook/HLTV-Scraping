from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd    
import re

driver = webdriver.Firefox()

driver.get("https://www.hltv.org/stats/matches/mapstatsid/159792/og-vs-g2?event=6973") 

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

for div in soup.findAll('div', attrs={'class':'match-info-box'}):
    stringsContainingMap = div.find_all(string=True, recursive=False)
    mapName = ' '.join(stringsContainingMap[1].split())
    maps.append(mapName)
    print(mapName)                                                      # Map
    a = div.a
    eventsnames.append(a.text)                                          
    print(a.text)                                                       # Event Name
    temp = a.get('href')
    temp2 = re.sub(r'[^0-9]', '', temp)
    temp2 = temp2[:4]
    eventsIDs.append(temp2)
    print(temp2)                                                        # Event ID
    SmallTextDiv = div.div
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
    

#for div in soup.findAll('div', attrs={'class':'match-info-box'}):



df = pd.DataFrame({'Team1Name':team1name,'Team2Name':team2name, 'Map':maps, 'Date':matchdates, 'Tournament':eventsnames, 'EventID':eventsIDs, 
                   'Team1Rounds':team1rounds, 'Team2Rounds':team2rounds })
df.to_csv('HLTV-Data.csv',index=False)