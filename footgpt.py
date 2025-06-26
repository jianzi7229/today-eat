import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_premier_league_goals(season_id=489):
    url = f"https://www.premierleague.com/stats/top/players/goals?se={season_id}/1/1/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    players_table = soup.find("table", {"id": "tech_statistics_1"})
    if not players_table:
        print("未找到球员数据表格，可能网页结构已变更。")
        return

    try:
        players_df = pd.read_html(str(players_table))[0]
    except Exception as e:
        print(f"表格解析失败: {e}")
        return

    print("英超球员进球榜：")
    print(players_df.head(20))  # 只显示前20名

    # 保存为CSV
    csv_filename = f"premier_league_goals_season_{season_id}.csv"
    players_df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"数据已保存为 {csv_filename}")

if __name__ == "__main__":
    fetch_premier_league_goals()
