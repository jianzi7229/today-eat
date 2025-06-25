

from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://www.premierleague.com/match/75255'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    match_list = soup.find_all('div', {'class': 'match_list'})
    output = ''
    for match in match_list:
        home_team = match.find('div', {'class': 'team_home'}).text.strip()
        away_team = match.find('div', {'class': 'team_away'}).text.strip()
        score = match.find('div', {'class': 'score'}).text.strip()
        output += f'{home_team} vs {away_team}: {score}<br>'

    return output

if __name__ == '__main__':
    app.run(debug=True)
