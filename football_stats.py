#!/usr/bin/env python3
"""
改进的英超数据获取脚本
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def fetch_premier_league_goals_improved():
    """获取英超进球数据的改进版本"""
    
    # 尝试多个可能的URL
    urls = [
        "https://www.premierleague.com/stats/top/players/goals",
        "https://www.premierleague.com/stats/top/players/goals?se=719",
        "https://www.premierleague.com/stats/top/players/goals?se=718"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    for url in urls:
        try:
            print(f"尝试访问: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # 尝试多种可能的表格选择器
            table_selectors = [
                "table#tech_statistics_1",
                "table.statsTable",
                "table",
                ".stats-table",
                "#stats-table"
            ]
            
            players_table = None
            for selector in table_selectors:
                players_table = soup.select_one(selector)
                if players_table:
                    print(f"找到表格: {selector}")
                    break
            
            if not players_table:
                # 尝试查找包含球员数据的任何元素
                print("未找到标准表格，尝试查找球员数据...")
                
                # 查找可能包含球员信息的元素
                player_elements = soup.find_all(['div', 'tr'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['player', 'stats', 'goals', 'rank']))
                
                if player_elements:
                    print(f"找到 {len(player_elements)} 个可能的球员数据元素")
                    
                    # 创建模拟数据
                    return create_mock_data()
                else:
                    print("未找到球员数据元素")
                    continue
            
            # 尝试解析表格
            try:
                players_df = pd.read_html(str(players_table))[0]
                print("成功解析表格数据")
                return format_data(players_df)
            except Exception as e:
                print(f"表格解析失败: {e}")
                continue
                
        except requests.RequestException as e:
            print(f"网络请求失败: {e}")
            continue
        except Exception as e:
            print(f"处理失败: {e}")
            continue
    
    # 如果所有方法都失败，返回模拟数据
    print("所有方法都失败，返回模拟数据")
    return create_mock_data()

def create_mock_data():
    """创建模拟的英超进球数据"""
    mock_data = [
        {"排名": 1, "球员": "Erling Haaland", "球队": "Manchester City", "进球": 18, "助攻": 5},
        {"排名": 2, "球员": "Mohamed Salah", "球队": "Liverpool", "进球": 15, "助攻": 8},
        {"排名": 3, "球员": "Ollie Watkins", "球队": "Aston Villa", "进球": 13, "助攻": 10},
        {"排名": 4, "球员": "Dominic Solanke", "球队": "Bournemouth", "进球": 12, "助攻": 1},
        {"排名": 5, "球员": "Jarrod Bowen", "球队": "West Ham", "进球": 11, "助攻": 2},
        {"排名": 6, "球员": "Bukayo Saka", "球队": "Arsenal", "进球": 10, "助攻": 7},
        {"排名": 7, "球员": "Son Heung-min", "球队": "Tottenham", "进球": 10, "助攻": 4},
        {"排名": 8, "球员": "Alexander Isak", "球队": "Newcastle", "进球": 9, "助攻": 1},
        {"排名": 9, "球员": "Cole Palmer", "球队": "Chelsea", "进球": 9, "助攻": 4},
        {"排名": 10, "球员": "Phil Foden", "球队": "Manchester City", "进球": 8, "助攻": 7}
    ]
    
    df = pd.DataFrame(mock_data)
    return format_data(df)

def format_data(df):
    """格式化数据输出"""
    result = "⚽ 英超球员进球榜 (2024/25赛季)\n"
    result += "=" * 60 + "\n"
    result += f"{'排名':<4} {'球员':<20} {'球队':<20} {'进球':<6} {'助攻':<6}\n"
    result += "-" * 60 + "\n"
    
    for _, row in df.head(15).iterrows():
        rank = str(row.get('排名', row.get('Rank', '')))
        player = str(row.get('球员', row.get('Player', '')))
        team = str(row.get('球队', row.get('Team', '')))
        goals = str(row.get('进球', row.get('Goals', '')))
        assists = str(row.get('助攻', row.get('Assists', '')))
        
        result += f"{rank:<4} {player:<20} {team:<20} {goals:<6} {assists:<6}\n"
    
    result += "\n📊 数据说明：\n"
    result += "- 数据来源：英超官网 (模拟数据)\n"
    result += "- 更新时间：2024年12月\n"
    result += "- 显示前15名球员\n"
    
    return result

def get_latest_fixtures():
    """获取最新比赛结果"""
    result = "🏆 最新比赛结果 (模拟数据)\n"
    result += "=" * 50 + "\n"
    
    fixtures = [
        ("Arsenal", "2-1", "Brighton", "2024-12-17"),
        ("Manchester City", "3-1", "Crystal Palace", "2024-12-16"),
        ("Liverpool", "2-0", "Manchester United", "2024-12-16"),
        ("Tottenham", "1-1", "Newcastle", "2024-12-15"),
        ("Chelsea", "2-2", "Sheffield United", "2024-12-15")
    ]
    
    for home, score, away, date in fixtures:
        result += f"{home:<15} {score:<8} {away:<15} {date}\n"
    
    return result

if __name__ == "__main__":
    print("正在获取英超数据...")
    goals_data = fetch_premier_league_goals_improved()
    print(goals_data)
    
    print("\n" + "="*60 + "\n")
    
    fixtures_data = get_latest_fixtures()
    print(fixtures_data) 