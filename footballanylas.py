 
import requests
from bs4 import BeautifulSoup

url = "https://sports.qq.com/csocce/csl/"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')


try: 
    table = soup.find_all('table')[0]
except IndexError: 
    print("未找到<table>元素!")
rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 0:
        player_name = cols[1].text.strip()
        team_name = cols[2].text.strip()
        goals = cols[6].text.strip()
        assists = cols[7].text.strip()
        print(player_name, team_name, goals, assists)

