import random
import time
import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

RECENT_FILE = 'recent_foods.txt'

class FoodOption:
    """食物选项数据结构"""
    def __init__(self, name, min_price, max_price, health_rating, description, tags=None):
        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.health_rating = health_rating
        self.description = description
        self.tags = tags or []

def get_food_options():
    """
    获取食物选项列表。
    优先从 foods.csv 加载，否则使用内置数据。
    """
    csv_path = 'foods.csv'
    if os.path.exists(csv_path):
        logging.info('从 foods.csv 加载食物数据...')
        df = pd.read_csv(csv_path, encoding='utf-8')
        options = []
        for _, row in df.iterrows():
            options.append(FoodOption(
                name=row['菜品名'],
                min_price=row['价格'],
                max_price=row['价格'],
                health_rating=row.get('健康度', 5),
                description=row.get('备注', ''),
                tags=[str(row.get('适合天气', ''))]
            ))
        return options
    else:
        logging.info('使用内置食物数据...')
        return [
            # 中式炒菜/快餐类
            FoodOption("青椒肉丝", 22, 32, 7, "清淡可口，营养均衡", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("宫保鸡丁", 25, 35, 6, "经典川菜，荤素搭配", ["晴天", "秋季", "冬季"]),
            FoodOption("鱼香肉丝", 25, 35, 6, "经典川菜，适中搭配", ["晴天", "春季", "秋季"]),
            FoodOption("糖醋里脊", 28, 38, 5, "口感酸甜，适量食用", ["晴天", "春季", "夏季"]),
            FoodOption("麻婆豆腐", 20, 30, 7, "高蛋白低脂，开胃下饭", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("回锅肉", 30, 40, 4, "重口味，高脂肪", ["阴天", "雨天", "冬季"]),
            FoodOption("黄焖鸡米饭", 20, 30, 6, "蛋白质搭配碳水，稍油腻", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("酸菜鱼", 35, 40, 8, "酸爽可口，蛋白质丰富", ["阴天", "雨天", "冬季"]),
            FoodOption("水煮鱼", 35, 40, 8, "富含蛋白质，适量辣味开胃", ["阴天", "雨天", "冬季"]),
            FoodOption("麻辣香锅", 30, 40, 4, "口感丰富，但油量较大", ["阴天", "雨天", "冬季"]),
            
            # 快餐/西式
            FoodOption("三明治", 20, 30, 6, "便携快捷，营养尚可", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("墨西哥卷饼", 25, 35, 6, "蔬菜肉类均衡搭配", ["晴天", "春季", "夏季"]),
            FoodOption("意大利面", 30, 40, 5, "碳水为主，酱料决定健康度", ["晴天", "春季", "秋季"]),
            FoodOption("炸鸡汉堡", 25, 35, 3, "高热量，碳水蛋白质为主", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("披萨", 30, 40, 4, "奶酪提供钙质，但热量较高", ["阴天", "雨天", "冬季"]),
            FoodOption("肯德基", 25, 35, 2, "高热量，高脂肪", ["阴天", "雨天", "冬季"]),
            FoodOption("麦当劳", 25, 35, 2, "高热量，高脂肪", ["阴天", "雨天", "冬季"]),
            FoodOption("烤肉拼盘", 35, 40, 4, "高蛋白，但要注意脂肪", ["阴天", "雨天", "冬季"]),
            
            # 日韩料理
            FoodOption("寿司", 30, 40, 7, "生鱼片富含蛋白质和omega-3", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("拉面", 25, 35, 5, "汤底营养，面食为主", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("韩式炸鸡", 30, 40, 3, "口感极佳，但高热量", ["阴天", "雨天", "冬季"]),
            FoodOption("石锅拌饭", 30, 40, 8, "营养均衡，种类丰富", ["晴天", "春季", "秋季"]),
            FoodOption("寿喜烧", 35, 40, 7, "肉类蔬菜搭配均衡", ["阴天", "雨天", "冬季"]),
            FoodOption("天妇罗", 30, 40, 4, "油炸食品，偶尔食用", ["晴天", "春季", "夏季"]),
            FoodOption("韩式部队锅", 35, 40, 5, "口感浓郁，注意钠含量", ["阴天", "雨天", "冬季"]),
            FoodOption("冷面", 25, 35, 7, "低热量，清爽开胃", ["晴天", "炎热", "夏季"]),
            
            # 火锅/烧烤
            FoodOption("火锅外卖", 35, 40, 5, "食材多样，可荤可素", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("烤肉", 35, 40, 4, "高蛋白，注意脂肪", ["阴天", "雨天", "冬季"]),
            FoodOption("串串香", 25, 35, 4, "品种丰富，油盐偏高", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("麻辣烫", 20, 30, 5, "食材多样，但油盐偏高", ["阴天", "雨天", "秋季", "冬季"]),
            
            # 面食/米饭类
            FoodOption("兰州拉面", 20, 30, 6, "面食为主，汤料营养", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("炸酱面", 20, 30, 5, "传统面食，口感浓郁", ["晴天", "春季", "秋季"]),
            FoodOption("扬州炒饭", 20, 30, 6, "蛋白质碳水均衡", ["晴天", "春季", "秋季"]),
            FoodOption("螺蛳粉", 25, 35, 4, "重口味，营养适中", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("酸辣粉", 20, 30, 4, "开胃爽口，注意辣度", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("重庆小面", 20, 30, 5, "面食为主，调味适中", ["晴天", "春季", "秋季"]),
            FoodOption("牛肉面", 25, 35, 7, "优质蛋白，汤料滋补", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("粤式炒饭", 25, 35, 6, "粮油适中，配料丰富", ["晴天", "春季", "秋季"]),
            
            # 健康轻食
            FoodOption("凉皮", 20, 30, 7, "低脂肪，碳水适中", ["晴天", "炎热", "夏季"]),
            FoodOption("沙拉", 25, 35, 9, "富含膳食纤维和维生素", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("水果捞", 20, 30, 9, "维生素充足，新鲜健康", ["晴天", "炎热", "夏季"]),
            FoodOption("鸡胸肉饭", 25, 35, 9, "高蛋白低脂，健身首选", ["晴天", "春季", "秋季"]),
            FoodOption("藜麦鸡肉碗", 30, 40, 9, "超级食物，营养全面", ["晴天", "春季", "秋季"]),
            FoodOption("蔬菜汤面", 20, 30, 8, "低热量，营养均衡", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("杂粮饭", 20, 30, 8, "膳食纤维丰富，营养均衡", ["晴天", "春季", "秋季"]),
            FoodOption("豆腐套餐", 20, 30, 8, "植物蛋白，低脂健康", ["晴天", "春季", "秋季"]),
            
            # 特色小吃
            FoodOption("肠粉", 20, 30, 6, "口感滑嫩，早餐优选", ["晴天", "春季", "夏季"]),
            FoodOption("煎饼果子", 20, 30, 5, "传统小吃，早餐首选", ["晴天", "春季", "夏季"]),
            FoodOption("生煎包", 20, 30, 5, "口感独特，适量食用", ["晴天", "春季", "秋季"]),
            FoodOption("锅贴", 20, 30, 5, "外酥内软，经典小吃", ["晴天", "春季", "秋季"]),
            FoodOption("饺子", 25, 35, 6, "传统美食，营养可控", ["晴天", "春季", "秋季"]),
            FoodOption("馄饨", 20, 30, 6, "清淡营养，开胃可口", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 中式炒菜
            FoodOption("蒜蓉西兰花", 20, 30, 8, "高纤维，维生素丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("红烧茄子", 20, 30, 6, "软糯可口，下饭神器", ["晴天", "春季", "秋季"]),
            FoodOption("干煸豆角", 20, 30, 7, "香辣开胃，营养均衡", ["晴天", "春季", "秋季"]),
            FoodOption("醋溜白菜", 20, 30, 8, "清爽解腻，维生素C丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("蒜苗炒肉", 25, 35, 7, "荤素搭配，营养丰富", ["晴天", "春季", "秋季"]),
            FoodOption("韭菜炒蛋", 20, 30, 7, "蛋白质丰富，开胃下饭", ["晴天", "春季", "秋季"]),
            FoodOption("蒜苔炒肉", 25, 35, 7, "清脆爽口，营养均衡", ["晴天", "春季", "夏季"]),
            FoodOption("清炒小白菜", 20, 30, 8, "清淡爽口，维生素丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("红烧豆腐", 20, 30, 8, "植物蛋白，低脂健康", ["晴天", "春季", "秋季"]),
            FoodOption("蒜蓉空心菜", 20, 30, 8, "清热解暑，纤维丰富", ["晴天", "炎热", "夏季"]),
            
            # 新增食物 - 西式简餐
            FoodOption("凯撒沙拉", 25, 35, 8, "经典西式沙拉，营养均衡", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("意式通心粉", 25, 35, 6, "口感丰富，酱料浓郁", ["晴天", "春季", "秋季"]),
            FoodOption("法式吐司", 20, 30, 5, "香甜可口，早餐优选", ["晴天", "春季", "夏季"]),
            FoodOption("美式汉堡", 25, 35, 4, "经典美式快餐", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("希腊沙拉", 25, 35, 9, "地中海风味，健康美味", ["晴天", "炎热", "夏季"]),
            FoodOption("意式千层面", 30, 40, 5, "层次丰富，口感浓郁", ["阴天", "雨天", "冬季"]),
            FoodOption("法式可颂", 20, 30, 4, "酥脆可口，早餐首选", ["晴天", "春季", "夏季"]),
            FoodOption("美式热狗", 20, 30, 3, "经典美式小吃", ["阴天", "雨天", "秋季", "冬季"]),
            
            # 新增食物 - 日韩料理
            FoodOption("日式咖喱饭", 25, 35, 6, "浓郁咖喱，营养丰富", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("韩式泡菜汤", 25, 35, 7, "酸辣开胃，益生菌丰富", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("日式乌冬面", 25, 35, 6, "滑嫩爽口，汤底鲜美", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("韩式辣炒年糕", 25, 35, 5, "甜辣可口，口感独特", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("日式茶泡饭", 20, 30, 7, "清淡养生，日式传统", ["晴天", "春季", "夏季"]),
            FoodOption("韩式海带汤", 20, 30, 8, "营养丰富，韩式传统", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("日式亲子丼", 25, 35, 7, "鸡肉鸡蛋，营养均衡", ["晴天", "春季", "秋季"]),
            FoodOption("韩式拌饭", 25, 35, 8, "蔬菜丰富，营养全面", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 东南亚料理
            FoodOption("泰式炒河粉", 25, 35, 6, "酸甜辣香，口感丰富", ["晴天", "春季", "夏季"]),
            FoodOption("越南春卷", 20, 30, 8, "清爽可口，低脂健康", ["晴天", "炎热", "夏季"]),
            FoodOption("新加坡炒米粉", 25, 35, 6, "海鲜味浓，口感丰富", ["晴天", "春季", "夏季"]),
            FoodOption("马来西亚咖喱", 25, 35, 6, "椰香浓郁，口感丰富", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("泰式青咖喱", 25, 35, 7, "清香微辣，营养丰富", ["晴天", "春季", "夏季"]),
            FoodOption("越南河粉", 25, 35, 7, "清淡鲜美，营养均衡", ["晴天", "春季", "夏季"]),
            
            # 新增食物 - 面食类
            FoodOption("阳春面", 20, 30, 6, "清淡爽口，传统面食", ["晴天", "春季", "夏季"]),
            FoodOption("担担面", 25, 35, 5, "麻辣鲜香，川式经典", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("热干面", 20, 30, 5, "芝麻香浓，武汉特色", ["晴天", "春季", "秋季"]),
            FoodOption("刀削面", 25, 35, 6, "口感独特，山西特色", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("炸酱面", 20, 30, 5, "传统面食，口感浓郁", ["晴天", "春季", "秋季"]),
            FoodOption("臊子面", 25, 35, 6, "配料丰富，陕西特色", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 米饭类
            FoodOption("蛋炒饭", 20, 30, 6, "经典炒饭，简单美味", ["晴天", "春季", "秋季"]),
            FoodOption("扬州炒饭", 20, 30, 6, "蛋白质碳水均衡", ["晴天", "春季", "秋季"]),
            FoodOption("咖喱炒饭", 25, 35, 5, "咖喱香浓，口感丰富", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("菠萝炒饭", 25, 35, 6, "酸甜可口，营养丰富", ["晴天", "春季", "夏季"]),
            FoodOption("海鲜炒饭", 30, 40, 7, "海鲜鲜美，营养丰富", ["晴天", "春季", "夏季"]),
            FoodOption("鸡肉炒饭", 25, 35, 7, "蛋白质丰富，营养均衡", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 汤类
            FoodOption("紫菜蛋花汤", 20, 30, 7, "清淡鲜美，营养丰富", ["晴天", "春季", "夏季"]),
            FoodOption("番茄蛋汤", 20, 30, 8, "维生素丰富，开胃爽口", ["晴天", "炎热", "夏季"]),
            FoodOption("冬瓜排骨汤", 25, 35, 8, "清热解暑，营养丰富", ["晴天", "炎热", "夏季"]),
            FoodOption("玉米排骨汤", 25, 35, 8, "香甜可口，营养丰富", ["晴天", "春季", "秋季"]),
            FoodOption("萝卜排骨汤", 25, 35, 8, "滋补养生，冬季首选", ["阴天", "雨天", "冬季"]),
            FoodOption("莲藕排骨汤", 25, 35, 8, "滋补养生，秋季佳品", ["阴天", "雨天", "秋季"]),
            
            # 新增食物 - 健康轻食
            FoodOption("藜麦沙拉", 25, 35, 9, "超级食物，营养全面", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("鸡胸肉沙拉", 25, 35, 9, "高蛋白低脂，健身首选", ["晴天", "春季", "秋季"]),
            FoodOption("三文鱼沙拉", 30, 40, 9, "omega-3丰富，营养全面", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("牛油果沙拉", 25, 35, 9, "健康脂肪，营养丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("希腊酸奶", 20, 30, 9, "蛋白质丰富，益生菌", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("燕麦粥", 20, 30, 9, "膳食纤维丰富，早餐首选", ["阴天", "雨天", "秋季", "冬季"]),
            
            # 新增食物 - 特色小吃
            FoodOption("小笼包", 25, 35, 6, "汤汁丰富，上海特色", ["晴天", "春季", "秋季"]),
            FoodOption("灌汤包", 25, 35, 6, "汤汁浓郁，口感独特", ["晴天", "春季", "秋季"]),
            FoodOption("烧卖", 20, 30, 6, "糯米香浓，广式特色", ["晴天", "春季", "秋季"]),
            FoodOption("叉烧包", 20, 30, 5, "甜咸适中，广式经典", ["晴天", "春季", "秋季"]),
            FoodOption("奶黄包", 20, 30, 4, "香甜可口，早餐优选", ["晴天", "春季", "夏季"]),
            FoodOption("豆沙包", 20, 30, 5, "传统甜点，营养丰富", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 甜品饮品
            FoodOption("双皮奶", 20, 30, 6, "滑嫩香甜，广式甜品", ["晴天", "炎热", "夏季"]),
            FoodOption("杨枝甘露", 25, 35, 7, "清爽解暑，港式甜品", ["晴天", "炎热", "夏季"]),
            FoodOption("红豆沙", 20, 30, 7, "传统甜品，营养丰富", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("绿豆汤", 20, 30, 8, "清热解暑，夏季必备", ["晴天", "炎热", "夏季"]),
            FoodOption("银耳莲子汤", 20, 30, 8, "滋补养生，美容养颜", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("冰糖雪梨", 20, 30, 8, "润肺止咳，秋季佳品", ["阴天", "雨天", "秋季"]),
            
            # 新增食物 - 素食类
            FoodOption("素炒三丝", 20, 30, 8, "蔬菜丰富，营养均衡", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("素炒豆芽", 20, 30, 8, "清脆爽口，维生素丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("素炒青菜", 20, 30, 9, "清淡爽口，纤维丰富", ["晴天", "炎热", "春季", "夏季"]),
            FoodOption("素炒茄子", 20, 30, 7, "软糯可口，营养丰富", ["晴天", "春季", "秋季"]),
            FoodOption("素炒豆腐", 20, 30, 8, "植物蛋白，低脂健康", ["晴天", "春季", "秋季"]),
            FoodOption("素炒蘑菇", 25, 35, 8, "菌类营养，口感丰富", ["晴天", "春季", "秋季"]),
            
            # 新增食物 - 特色菜系
            FoodOption("白切鸡", 30, 40, 8, "清淡鲜美，粤式经典", ["晴天", "春季", "夏季"]),
            FoodOption("口水鸡", 25, 35, 6, "麻辣鲜香，川式经典", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("叫花鸡", 30, 40, 7, "香气四溢，江南特色", ["晴天", "春季", "秋季"]),
            FoodOption("盐焗鸡", 30, 40, 7, "咸香可口，客家特色", ["晴天", "春季", "秋季"]),
            FoodOption("辣子鸡", 25, 35, 5, "麻辣鲜香，川式经典", ["阴天", "雨天", "秋季", "冬季"]),
            FoodOption("黄焖鸡", 25, 35, 6, "软烂入味，营养丰富", ["阴天", "雨天", "秋季", "冬季"])
        ]

def read_recent_foods():
    if not os.path.exists(RECENT_FILE):
        return []
    with open(RECENT_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def add_recent_food(food_name):
    foods = read_recent_foods()
    foods.append(food_name)
    # 只保留最近7天的记录
    foods = foods[-7:]
    with open(RECENT_FILE, 'w', encoding='utf-8') as f:
        for food in foods:
            f.write(food + '\n')

def clear_recent_foods():
    if os.path.exists(RECENT_FILE):
        os.remove(RECENT_FILE)

def show_recent_foods():
    foods = read_recent_foods()
    if not foods:
        logging.info("\n近期未录入任何食品。\n")
    else:
        logging.info("\n你最近吃过的食品有：")
        for food in foods:
            logging.info("-", food)
        logging.info()

def get_food_recommendation():
    food_options = get_food_options()
    logging.info("\n=== 今天吃什么？让我帮你决定！===\n")
    # 获取天气类型
    weather_types = ["晴天", "雨天", "炎热", "寒冷"]
    logging.info("天气类型可选：", ", ".join(weather_types))
    while True:
        weather = input("请输入当前天气类型: ")
        if weather in weather_types:
            break
        logging.warning("请输入有效的天气类型！")
    # 获取用户预算
    while True:
        try:
            budget = float(input("请输入您的预算（元）: "))
            if budget > 0:
                break
            logging.warning("预算必须大于0元")
        except ValueError:
            logging.warning("请输入有效的数字")
    # 获取最低健康度要求
    logging.info("健康度评分说明：")
    logging.info("1-2：高热量、高油脂、重口味（如炸鸡、快餐）")
    logging.info("3-4：一般快餐、重口味、油脂偏高")
    logging.info("5-6：普通家常菜、主食搭配，营养适中")
    logging.info("7-8：清淡、荤素搭配、蛋白质丰富")
    logging.info("9-10：高纤维、低脂肪、蔬菜水果、健身餐")
    while True:
        try:
            min_health = int(input("请输入最低健康度要求（1-10）："))
            if 1 <= min_health <= 10:
                break
            logging.warning("健康度必须在1-10之间")
        except ValueError:
            logging.warning("请输入有效的数字")
    # 读取近期饮食
    recent_foods = set(read_recent_foods())
    # 筛选符合条件的食物
    suitable_options = [
        food for food in food_options
        if food.min_price <= budget and food.health_rating >= min_health and food.name not in recent_foods
    ]
    # 根据天气优先筛选
    weather_options = [food for food in suitable_options if weather in food.tags]
    if weather_options:
        suitable_options = weather_options
    if not suitable_options:
        logging.warning("\n抱歉，没有找到符合您要求的食物。请调整预算或健康度要求，或清空近期饮食记录。")
        return None
    logging.info("\n思考中", end="")
    for _ in range(3):
        time.sleep(0.5)
        logging.info(".", end="", flush=True)
    recommendation = random.choice(suitable_options)
    logging.info(f"\n\n今天推荐您吃: {recommendation.name}! 😋")
    logging.info(f"预计价格范围: ¥{recommendation.min_price}-{recommendation.max_price}")
    logging.info(f"健康度评分: {'🍎' * recommendation.health_rating}{'⭐' * (10-recommendation.health_rating)}")
    logging.info(f"推荐理由: {recommendation.description}")
    logging.info(f"适合天气: {', '.join(recommendation.tags)}\n")
    add_recent_food(recommendation.name)
    return recommendation

def guess_you_like():
    food_options = get_food_options()
    food = random.choice(food_options)
    logging.info("\n=== 猜你今天会喜欢 ===\n")
    logging.info(f"{food.name}  (预计价格: ¥{food.min_price}-{food.max_price})")
    logging.info(f"健康度评分: {'🍎' * food.health_rating}{'⭐' * (10-food.health_rating)}")
    logging.info(f"推荐理由: {food.description}")
    logging.info(f"适合天气: {', '.join(food.tags)}\n")

def main():
    while True:
        logging.info("\n主菜单：\n1. 推荐今天吃什么\n2. 录入今天已吃食品\n3. 查看近期饮食记录\n4. 清空近期饮食记录\n5. 猜你喜欢\n6. 退出\n")
        choice = input("请选择功能（1-6）：")
        if choice == '1':
            get_food_recommendation()
        elif choice == '2':
            food = input("请输入你今天已吃的食品名称：").strip()
            if food:
                add_recent_food(food)
                logging.info("已录入。\n")
        elif choice == '3':
            show_recent_foods()
        elif choice == '4':
            clear_recent_foods()
            logging.info("已清空近期饮食记录。\n")
        elif choice == '5':
            guess_you_like()
        elif choice == '6':
            logging.info("\n祝您用餐愉快！👋\n")
            break
        else:
            logging.warning("无效选择，请重新输入。\n")

if __name__ == "__main__":
    main()