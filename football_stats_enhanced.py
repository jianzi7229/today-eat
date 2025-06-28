#!/usr/bin/env python3
"""
增强版英超数据获取脚本
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime

def fetch_real_premier_league_data():
    """获取真实的英超数据"""
    url = "https://www.premierleague.com/stats/top/players/goals"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        print("🌐 正在连接英超官网...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print("📊 正在解析数据...")
        soup = BeautifulSoup(response.content, "html.parser")
        
        # 查找数据表格
        table = soup.find("table")
        if table:
            df = pd.read_html(str(table))[0]
            print("✅ 成功获取真实数据")
            return format_real_data(df)
        else:
            print("❌ 未找到数据表格")
            return create_mock_data()
            
    except requests.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return create_mock_data()
    except Exception as e:
        print(f"❌ 数据处理失败: {e}")
        return create_mock_data()

def format_real_data(df):
    """格式化真实数据"""
    result = "⚽ 英超球员进球榜 (实时数据)\n"
    result += "=" * 60 + "\n"
    result += f"{'排名':<4} {'球员':<20} {'球队':<20} {'进球':<6} {'助攻':<6}\n"
    result += "-" * 60 + "\n"
    
    for i, row in df.head(15).iterrows():
        # 处理不同的列名格式
        rank = str(row.iloc[0]) if len(row) > 0 else str(i+1)
        player = str(row.iloc[1]) if len(row) > 1 else "未知"
        team = str(row.iloc[2]) if len(row) > 2 else "未知"
        goals = str(row.iloc[3]) if len(row) > 3 else "0"
        assists = str(row.iloc[4]) if len(row) > 4 else "0"
        
        result += f"{rank:<4} {player:<20} {team:<20} {goals:<6} {assists:<6}\n"
    
    result += "\n📊 数据说明：\n"
    result += f"- 数据来源：英超官网 (实时数据)\n"
    result += f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    result += "- 显示前15名球员\n"
    
    return result

def create_mock_data():
    """创建模拟数据（备用方案）"""
    print("🔄 使用模拟数据作为备用方案")
    
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
    return format_mock_data(df)

def format_mock_data(df):
    """格式化模拟数据"""
    result = "⚽ 英超球员进球榜 (模拟数据)\n"
    result += "=" * 60 + "\n"
    result += f"{'排名':<4} {'球员':<20} {'球队':<20} {'进球':<6} {'助攻':<6}\n"
    result += "-" * 60 + "\n"
    
    for _, row in df.iterrows():
        rank = str(row['排名'])
        player = str(row['球员'])
        team = str(row['球队'])
        goals = str(row['进球'])
        assists = str(row['助攻'])
        
        result += f"{rank:<4} {player:<20} {team:<20} {goals:<6} {assists:<6}\n"
    
    result += "\n📊 数据说明：\n"
    result += "- 数据来源：模拟数据 (备用方案)\n"
    result += f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    result += "- 显示前10名球员\n"
    result += "- 注意：这是模拟数据，仅供参考\n"
    
    return result

def get_data_source_info():
    """获取数据源信息"""
    info = {
        "real_data_available": True,
        "last_update": datetime.now().isoformat(),
        "data_source": "Premier League Official Website",
        "fallback_data": "Simulated data based on current season performance",
        "limitations": [
            "Website structure may change",
            "Rate limiting may apply",
            "Network connectivity required"
        ]
    }
    return info

if __name__ == "__main__":
    print("🚀 启动增强版英超数据获取...")
    print("=" * 50)
    
    # 获取数据
    data = fetch_real_premier_league_data()
    print(data)
    
    # 显示数据源信息
    info = get_data_source_info()
    print("\n📋 数据源信息：")
    print(f"- 真实数据可用: {info['real_data_available']}")
    print(f"- 数据源: {info['data_source']}")
    print(f"- 备用方案: {info['fallback_data']}")
    print(f"- 限制: {', '.join(info['limitations'])}") 