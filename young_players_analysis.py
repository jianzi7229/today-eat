#!/usr/bin/env python3
"""
英超年轻球员潜力分析
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def get_young_players_data():
    """
    获取英超年轻球员数据，结构统一，便于扩展。
    """
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
    """
    分析年轻球员潜力，输出表格化文本。
    """
    players = get_young_players_data()
    logging.info("🔍 英超年轻球员潜力分析报告")
    logging.info("=" * 80)
    logging.info(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("🎯 分析标准: 25岁以下球员，重点关注进球和助攻数据")
    logging.info()
    
    # 按潜力排序
    sorted_players = sorted(players.items(), 
                          key=lambda x: (x[1]['goals'] + x[1]['assists'], x[1]['age']), 
                          reverse=True)
    
    logging.info("🏆 潜力排行榜 (按进球+助攻数据排序)")
    logging.info("-" * 80)
    
    # 表格化输出
    header = f"{'球员':<20}{'年龄':<6}{'球队':<20}{'进球':<6}{'助攻':<6}{'潜力':<8}"
    logging.info(header)
    logging.info("-" * 60)
    for name, data in sorted_players:
        total_contribution = data['goals'] + data['assists']
        row = f"{name:<20}{data['age']:<6}{data['team']:<20}{data['goals']:<6}{data['assists']:<6}{data['potential']:<8}"
        logging.info(row)
    
    return sorted_players

def get_rising_stars():
    """识别冉冉升起的新星"""
    players = get_young_players_data()
    
    logging.info("🚀 冉冉升起的新星")
    logging.info("=" * 50)
    
    rising_stars = []
    for name, data in players.items():
        if data['age'] <= 24 and (data['goals'] + data['assists']) >= 15:
            rising_stars.append((name, data))
    
    rising_stars.sort(key=lambda x: x[1]['age'])
    
    for name, data in rising_stars:
        logging.info(f"🌟 {name} ({data['age']}岁)")
        logging.info(f"   球队: {data['team']}")
        logging.info(f"   数据: {data['goals']}球 {data['assists']}助攻")
        logging.info(f"   潜力: {data['potential']}")
        logging.info()

def get_position_analysis():
    """按位置分析"""
    players = get_young_players_data()
    
    logging.info("📊 位置分析")
    logging.info("=" * 50)
    
    positions = {}
    for name, data in players.items():
        pos = data['position']
        if pos not in positions:
            positions[pos] = []
        positions[pos].append((name, data))
    
    for pos, player_list in positions.items():
        logging.info(f"\n🎯 {pos}位置:")
        for name, data in player_list:
            total = data['goals'] + data['assists']
            logging.info(f"   {name}: {data['goals']}球 {data['assists']}助攻 (总计: {total})")

def get_transfer_targets():
    """转会目标分析"""
    players = get_young_players_data()
    
    logging.info("\n💰 转会市场目标")
    logging.info("=" * 50)
    
    # 按身价排序
    transfer_targets = [(name, data) for name, data in players.items()]
    transfer_targets.sort(key=lambda x: int(x[1]['transfer_value'].replace('€', '').replace('M+', '000')), reverse=True)
    
    for name, data in transfer_targets[:5]:
        logging.info(f"💎 {name}")
        logging.info(f"   身价: {data['transfer_value']}")
        logging.info(f"   年龄: {data['age']}岁")
        logging.info(f"   数据: {data['goals']}球 {data['assists']}助攻")
        logging.info(f"   潜力: {data['potential']}")
        logging.info()

def generate_report():
    """生成完整报告"""
    logging.info("📋 英超年轻球员潜力分析完整报告")
    logging.info("=" * 80)
    
    # 1. 总体分析
    analyze_young_players()
    
    # 2. 冉冉升起的新星
    get_rising_stars()
    
    # 3. 位置分析
    get_position_analysis()
    
    # 4. 转会目标
    get_transfer_targets()
    
    # 5. 总结
    logging.info("\n📝 总结与建议")
    logging.info("=" * 50)
    logging.info("🎯 重点关注球员:")
    logging.info("   1. Cole Palmer (22岁) - 切尔西中场新星")
    logging.info("   2. Bukayo Saka (23岁) - 阿森纳边锋核心")
    logging.info("   3. Alexander Isak (24岁) - 纽卡斯尔前锋")
    logging.info("   4. Phil Foden (24岁) - 曼城中场天才")
    logging.info()
    logging.info("💡 投资建议:")
    logging.info("   - 重点关注英格兰本土球员")
    logging.info("   - 技术型中场价值最高")
    logging.info("   - 25岁以下球员仍有上升空间")
    logging.info("   - 关注伤病情况和稳定性")

def test_analyze_young_players():
    """
    简单单元测试：检查输出和数据结构。
    """
    players = get_young_players_data()
    assert isinstance(players, dict)
    assert all('age' in v and 'team' in v for v in players.values())
    logging.info("✅ 年轻球员数据结构测试通过")

if __name__ == "__main__":
    generate_report() 