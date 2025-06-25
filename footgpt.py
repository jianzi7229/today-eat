import requests
from bs4 import BeautifulSoup
import pandas as pd

# 设置爬取的比赛页面 URL
match_url = "https://www.premierleague.com/stats/top/players/goals?se=489/{}/1/1/".format(489)

# 发送 HTTP 请求获取 HTML 页面内容
response = requests.get(match_url)

# 解析 HTML 页面内容
soup = BeautifulSoup(response.content, "html.parser")

# 找到球员表格
players_table = soup.find("table", {"id": "tech_statistics_1"})

# 使用 pandas 读取表格数据
players_df = pd.read_html(str(players_table))[0]

# 打印表格数据
print(players_df)
