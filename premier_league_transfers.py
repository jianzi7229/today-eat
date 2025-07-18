#!/usr/bin/env python3
"""
英超球员转会数据抓取脚本（多表格优化版）
抓取转会市场网站的英超转会信息，结构化输出。
支持保存为CSV和按条件筛选。
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sys
import argparse

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

TRANSFER_URL = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_premier_league_transfers():
    """
    抓取英超转会市场的转会数据，返回结构化DataFrame。
    """
    try:
        logging.info(f'正在抓取转会数据: {TRANSFER_URL}')
        response = requests.get(TRANSFER_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        all_tables = soup.find_all('div', class_='responsive-table')
        all_transfers = []
        for table_block in all_tables:
            # 获取俱乐部名
            club_head = table_block.find_previous('h2', class_='content-box-headline')
            club = club_head.get_text(strip=True) if club_head else ''
            # 解析表格
            table = table_block.find('table')
            if not table:
                continue
            # 判断是In还是Out表
            ths = table.find_all('th')
            if not ths:
                continue
            transfer_type = 'In' if ths[0].get_text(strip=True) == 'In' else 'Out' if ths[0].get_text(strip=True) == 'Out' else 'Unknown'
            # 解析每一行
            for row in table.find('tbody').find_all('tr'):
                tds = row.find_all('td')
                if len(tds) < 9:
                    continue
                player = tds[0].get_text(strip=True)
                age = tds[1].get_text(strip=True)
                nationality = tds[2].get_text(strip=True)
                position = tds[3].get_text(strip=True)
                short_pos = tds[4].get_text(strip=True)
                market_value = tds[5].get_text(strip=True)
                from_club = tds[7].get_text(strip=True) if transfer_type == 'In' else club
                to_club = club if transfer_type == 'In' else tds[7].get_text(strip=True)
                fee = tds[8].get_text(strip=True)
                all_transfers.append({
                    '球员': player,
                    '年龄': age,
                    '国籍': nationality,
                    '位置': position,
                    '简写位置': short_pos,
                    '身价': market_value,
                    '原俱乐部': from_club,
                    '新俱乐部': to_club,
                    '转会费': fee,
                    '转会类型': transfer_type,
                    '俱乐部': club
                })
        df = pd.DataFrame(all_transfers)
        return df
    except Exception as e:
        logging.error(f'抓取转会数据失败: {e}')
        return pd.DataFrame()

def print_transfers_table(df, n=20):
    """
    表格化输出转会信息。
    """
    if df.empty:
        logging.info('暂无转会数据可展示。')
        return
    print(df.head(n).to_string(index=False))

def save_transfers_to_csv(df, filename='premier_league_transfers.csv'):
    """
    保存转会数据为CSV文件。
    """
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    logging.info(f'转会数据已保存为 {filename}')

def filter_transfers(df, club=None, transfer_type=None):
    """
    按俱乐部和转会类型筛选数据。
    """
    if club:
        df = df[df['俱乐部'].str.contains(club, case=False, na=False)]
    if transfer_type:
        df = df[df['转会类型'].str.lower() == transfer_type.lower()]
    return df

def main():
    """
    命令行运行入口。
    """
    parser = argparse.ArgumentParser(description='英超转会数据抓取与分析')
    parser.add_argument('--save-csv', action='store_true', help='保存为CSV文件')
    parser.add_argument('--club', type=str, help='按俱乐部筛选（模糊匹配）')
    parser.add_argument('--type', type=str, choices=['In', 'Out'], help='按转会类型筛选')
    parser.add_argument('--top', type=int, default=20, help='显示前N条（默认20）')
    args = parser.parse_args()

    df = fetch_premier_league_transfers()
    df_filtered = filter_transfers(df, club=args.club, transfer_type=args.type)
    print_transfers_table(df_filtered, n=args.top)
    if args.save_csv:
        save_transfers_to_csv(df_filtered)

if __name__ == '__main__':
    main() 