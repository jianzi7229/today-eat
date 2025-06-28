#!/usr/bin/env python3
"""
英超年轻球员潜力分析
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

def get_young_players_data():
    """获取年轻球员数据"""
    
    # 定义年轻球员（25岁以下）的数据库
    young_players = {
        "Cole Palmer": {
            "age": 22,
            "team": "Chelsea",
            "position": "Midfielder/Forward",
            "goals": 15,
            "assists": 8,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐⭐",
            "strengths": ["技术细腻", "传球视野", "射门能力", "定位球"],
            "weaknesses": ["身体对抗", "防守意识"],
            "ceiling": "世界级中场",
            "transfer_value": "€80M+"
        },
        "Bukayo Saka": {
            "age": 23,
            "team": "Arsenal",
            "position": "Winger",
            "goals": 10,
            "assists": 7,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐⭐",
            "strengths": ["速度", "盘带", "传中", "射门"],
            "weaknesses": ["头球", "防守"],
            "ceiling": "世界级边锋",
            "transfer_value": "€100M+"
        },
        "Phil Foden": {
            "age": 24,
            "team": "Manchester City",
            "position": "Midfielder",
            "goals": 8,
            "assists": 7,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐⭐",
            "strengths": ["技术", "创造力", "射门", "团队配合"],
            "weaknesses": ["身体对抗", "防守"],
            "ceiling": "世界级中场",
            "transfer_value": "€90M+"
        },
        "Alexander Isak": {
            "age": 24,
            "team": "Newcastle United",
            "position": "Striker",
            "goals": 23,
            "assists": 3,
            "nationality": "Sweden",
            "potential": "⭐⭐⭐⭐⭐",
            "strengths": ["速度", "射门", "技术", "身体"],
            "weaknesses": ["头球", "伤病"],
            "ceiling": "世界级前锋",
            "transfer_value": "€85M+"
        },
        "Yoane Wissa": {
            "age": 27,
            "team": "Brentford",
            "position": "Forward",
            "goals": 19,
            "assists": 4,
            "nationality": "DR Congo",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["速度", "射门", "跑位"],
            "weaknesses": ["传球", "防守"],
            "ceiling": "顶级前锋",
            "transfer_value": "€50M+"
        },
        "Matheus Cunha": {
            "age": 25,
            "team": "Wolves",
            "position": "Forward",
            "goals": 15,
            "assists": 6,
            "nationality": "Brazil",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["技术", "创造力", "射门"],
            "weaknesses": ["稳定性", "防守"],
            "ceiling": "顶级前锋",
            "transfer_value": "€60M+"
        },
        "Jean-Philippe Mateta": {
            "age": 26,
            "team": "Crystal Palace",
            "position": "Striker",
            "goals": 14,
            "assists": 2,
            "nationality": "France",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["身体", "射门", "头球"],
            "weaknesses": ["技术", "传球"],
            "ceiling": "顶级中锋",
            "transfer_value": "€45M+"
        },
        "Dominic Solanke": {
            "age": 26,
            "team": "Bournemouth",
            "position": "Striker",
            "goals": 12,
            "assists": 1,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["身体", "射门", "跑位"],
            "weaknesses": ["技术", "传球"],
            "ceiling": "顶级中锋",
            "transfer_value": "€40M+"
        },
        "Jarrod Bowen": {
            "age": 27,
            "team": "West Ham",
            "position": "Winger",
            "goals": 11,
            "assists": 2,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["速度", "射门", "传中"],
            "weaknesses": ["技术", "防守"],
            "ceiling": "顶级边锋",
            "transfer_value": "€55M+"
        },
        "Ollie Watkins": {
            "age": 28,
            "team": "Aston Villa",
            "position": "Striker",
            "goals": 16,
            "assists": 10,
            "nationality": "England",
            "potential": "⭐⭐⭐⭐",
            "strengths": ["速度", "射门", "助攻"],
            "weaknesses": ["头球", "技术"],
            "ceiling": "顶级前锋",
            "transfer_value": "€65M+"
        }
    }
    
    return young_players

def analyze_young_players():
    """分析年轻球员潜力"""
    players = get_young_players_data()
    
    print("🔍 英超年轻球员潜力分析报告")
    print("=" * 80)
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 分析标准: 25岁以下球员，重点关注进球和助攻数据")
    print()
    
    # 按潜力排序
    sorted_players = sorted(players.items(), 
                          key=lambda x: (x[1]['goals'] + x[1]['assists'], x[1]['age']), 
                          reverse=True)
    
    print("🏆 潜力排行榜 (按进球+助攻数据排序)")
    print("-" * 80)
    
    for i, (name, data) in enumerate(sorted_players, 1):
        total_contribution = data['goals'] + data['assists']
        print(f"{i:2d}. {name:<20} ({data['age']}岁) - {data['team']}")
        print(f"    📊 数据: {data['goals']}球 {data['assists']}助攻 (总计: {total_contribution})")
        print(f"    ⭐ 潜力: {data['potential']}")
        print(f"    🎯 位置: {data['position']}")
        print(f"    💰 身价: {data['transfer_value']}")
        print(f"    🌟 上限: {data['ceiling']}")
        print(f"    ✅ 优势: {', '.join(data['strengths'])}")
        print(f"    ⚠️  弱点: {', '.join(data['weaknesses'])}")
        print()
    
    return sorted_players

def get_rising_stars():
    """识别冉冉升起的新星"""
    players = get_young_players_data()
    
    print("🚀 冉冉升起的新星")
    print("=" * 50)
    
    rising_stars = []
    for name, data in players.items():
        if data['age'] <= 24 and (data['goals'] + data['assists']) >= 15:
            rising_stars.append((name, data))
    
    rising_stars.sort(key=lambda x: x[1]['age'])
    
    for name, data in rising_stars:
        print(f"🌟 {name} ({data['age']}岁)")
        print(f"   球队: {data['team']}")
        print(f"   数据: {data['goals']}球 {data['assists']}助攻")
        print(f"   潜力: {data['potential']}")
        print()

def get_position_analysis():
    """按位置分析"""
    players = get_young_players_data()
    
    print("📊 位置分析")
    print("=" * 50)
    
    positions = {}
    for name, data in players.items():
        pos = data['position']
        if pos not in positions:
            positions[pos] = []
        positions[pos].append((name, data))
    
    for pos, player_list in positions.items():
        print(f"\n🎯 {pos}位置:")
        for name, data in player_list:
            total = data['goals'] + data['assists']
            print(f"   {name}: {data['goals']}球 {data['assists']}助攻 (总计: {total})")

def get_transfer_targets():
    """转会目标分析"""
    players = get_young_players_data()
    
    print("\n💰 转会市场目标")
    print("=" * 50)
    
    # 按身价排序
    transfer_targets = [(name, data) for name, data in players.items()]
    transfer_targets.sort(key=lambda x: int(x[1]['transfer_value'].replace('€', '').replace('M+', '000')), reverse=True)
    
    for name, data in transfer_targets[:5]:
        print(f"💎 {name}")
        print(f"   身价: {data['transfer_value']}")
        print(f"   年龄: {data['age']}岁")
        print(f"   数据: {data['goals']}球 {data['assists']}助攻")
        print(f"   潜力: {data['potential']}")
        print()

def generate_report():
    """生成完整报告"""
    print("📋 英超年轻球员潜力分析完整报告")
    print("=" * 80)
    
    # 1. 总体分析
    analyze_young_players()
    
    # 2. 冉冉升起的新星
    get_rising_stars()
    
    # 3. 位置分析
    get_position_analysis()
    
    # 4. 转会目标
    get_transfer_targets()
    
    # 5. 总结
    print("\n📝 总结与建议")
    print("=" * 50)
    print("🎯 重点关注球员:")
    print("   1. Cole Palmer (22岁) - 切尔西中场新星")
    print("   2. Bukayo Saka (23岁) - 阿森纳边锋核心")
    print("   3. Alexander Isak (24岁) - 纽卡斯尔前锋")
    print("   4. Phil Foden (24岁) - 曼城中场天才")
    print()
    print("💡 投资建议:")
    print("   - 重点关注英格兰本土球员")
    print("   - 技术型中场价值最高")
    print("   - 25岁以下球员仍有上升空间")
    print("   - 关注伤病情况和稳定性")

if __name__ == "__main__":
    generate_report() 