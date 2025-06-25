import random
import time
import os

RECENT_FILE = 'recent_foods.txt'

class FoodOption:
    def __init__(self, name, min_price, max_price, health_rating, description, tags=None):
        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.health_rating = health_rating
        self.description = description
        self.tags = tags or []

def get_food_options():
    return [
        # 中式炒菜/快餐类
        FoodOption("水煮鱼", 45, 68, 8, "富含蛋白质，适量辣味开胃", ["寒冷", "雨天"]),
        FoodOption("麻辣香锅", 35, 50, 4, "口感丰富，但油量较大", ["寒冷", "雨天"]),
        FoodOption("黄焖鸡米饭", 20, 30, 6, "蛋白质搭配碳水，稍油腻", ["雨天", "寒冷"]),
        FoodOption("宫保鸡丁", 25, 35, 6, "经典川菜，荤素搭配", ["晴天"]),
        FoodOption("青椒肉丝", 22, 32, 7, "清淡可口，营养均衡", ["晴天", "炎热"]),
        FoodOption("糖醋里脊", 28, 38, 5, "口感酸甜，适量食用", ["晴天"]),
        FoodOption("麻婆豆腐", 20, 30, 7, "高蛋白低脂，开胃下饭", ["寒冷"]),
        FoodOption("鱼香肉丝", 25, 35, 6, "经典川菜，适中搭配", ["晴天"]),
        FoodOption("回锅肉", 30, 45, 4, "重口味，高脂肪", ["寒冷"]),
        FoodOption("酸菜鱼", 40, 60, 8, "酸爽可口，蛋白质丰富", ["雨天", "寒冷"]),
        # 快餐/西式
        FoodOption("炸鸡汉堡", 25, 40, 3, "高热量，碳水蛋白质为主", ["雨天"]),
        FoodOption("披萨", 40, 80, 4, "奶酪提供钙质，但热量较高", ["雨天"]),
        FoodOption("肯德基", 30, 50, 2, "高热量，高脂肪", ["雨天"]),
        FoodOption("麦当劳", 30, 50, 2, "高热量，高脂肪", ["雨天"]),
        FoodOption("三明治", 15, 25, 6, "便携快捷，营养尚可", ["晴天", "炎热"]),
        FoodOption("意大利面", 35, 55, 5, "碳水为主，酱料决定健康度", ["晴天"]),
        FoodOption("墨西哥卷饼", 25, 40, 6, "蔬菜肉类均衡搭配", ["晴天"]),
        FoodOption("烤肉拼盘", 50, 80, 4, "高蛋白，但要注意脂肪", ["寒冷"]),
        # 日韩料理
        FoodOption("寿司", 30, 60, 7, "生鱼片富含蛋白质和omega-3", ["炎热", "晴天"]),
        FoodOption("拉面", 25, 40, 5, "汤底营养，面食为主", ["寒冷", "雨天"]),
        FoodOption("韩式炸鸡", 40, 60, 3, "口感极佳，但高热量", ["雨天"]),
        FoodOption("石锅拌饭", 35, 50, 8, "营养均衡，种类丰富", ["晴天"]),
        FoodOption("寿喜烧", 45, 70, 7, "肉类蔬菜搭配均衡", ["寒冷"]),
        FoodOption("天妇罗", 40, 60, 4, "油炸食品，偶尔食用", ["晴天"]),
        FoodOption("韩式部队锅", 45, 75, 5, "口感浓郁，注意钠含量", ["寒冷", "雨天"]),
        FoodOption("冷面", 28, 40, 7, "低热量，清爽开胃", ["炎热"]),
        # 火锅/烧烤
        FoodOption("火锅外卖", 50, 100, 5, "食材多样，可荤可素", ["寒冷", "雨天"]),
        FoodOption("烤肉", 60, 100, 4, "高蛋白，注意脂肪", ["寒冷"]),
        FoodOption("串串香", 30, 50, 4, "品种丰富，油盐偏高", ["寒冷", "雨天"]),
        FoodOption("麻辣烫", 20, 35, 5, "食材多样，但油盐偏高", ["寒冷", "雨天"]),
        # 面食/米饭类
        FoodOption("兰州拉面", 15, 25, 6, "面食为主，汤料营养", ["寒冷"]),
        FoodOption("炸酱面", 18, 28, 5, "传统面食，口感浓郁", ["晴天"]),
        FoodOption("扬州炒饭", 20, 35, 6, "蛋白质碳水均衡", ["晴天"]),
        FoodOption("螺蛳粉", 25, 35, 4, "重口味，营养适中", ["雨天"]),
        FoodOption("酸辣粉", 15, 25, 4, "开胃爽口，注意辣度", ["雨天"]),
        FoodOption("重庆小面", 15, 25, 5, "面食为主，调味适中", ["晴天"]),
        FoodOption("牛肉面", 20, 35, 7, "优质蛋白，汤料滋补", ["寒冷"]),
        FoodOption("粤式炒饭", 25, 40, 6, "粮油适中，配料丰富", ["晴天"]),
        # 健康轻食
        FoodOption("凉皮", 15, 25, 7, "低脂肪，碳水适中", ["炎热"]),
        FoodOption("沙拉", 25, 45, 9, "富含膳食纤维和维生素", ["炎热"]),
        FoodOption("水果捞", 20, 35, 9, "维生素充足，新鲜健康", ["炎热"]),
        FoodOption("鸡胸肉饭", 25, 40, 9, "高蛋白低脂，健身首选", ["晴天"]),
        FoodOption("藜麦鸡肉碗", 35, 50, 9, "超级食物，营养全面", ["晴天"]),
        FoodOption("蔬菜汤面", 20, 30, 8, "低热量，营养均衡", ["寒冷"]),
        FoodOption("杂粮饭", 15, 25, 8, "膳食纤维丰富，营养均衡", ["晴天"]),
        FoodOption("豆腐套餐", 20, 30, 8, "植物蛋白，低脂健康", ["晴天"]),
        # 特色小吃
        FoodOption("肠粉", 12, 20, 6, "口感滑嫩，早餐优选", ["晴天"]),
        FoodOption("煎饼果子", 8, 15, 5, "传统小吃，早餐首选", ["晴天"]),
        FoodOption("生煎包", 15, 25, 5, "口感独特，适量食用", ["晴天"]),
        FoodOption("锅贴", 15, 25, 5, "外酥内软，经典小吃", ["晴天"]),
        FoodOption("饺子", 20, 35, 6, "传统美食，营养可控", ["晴天"]),
        FoodOption("馄饨", 15, 25, 6, "清淡营养，开胃可口", ["晴天"])
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
        print("\n近期未录入任何食品。\n")
    else:
        print("\n你最近吃过的食品有：")
        for food in foods:
            print("-", food)
        print()

def get_food_recommendation():
    food_options = get_food_options()
    print("\n=== 今天吃什么？让我帮你决定！===\n")
    # 获取天气类型
    weather_types = ["晴天", "雨天", "炎热", "寒冷"]
    print("天气类型可选：", ", ".join(weather_types))
    while True:
        weather = input("请输入当前天气类型: ")
        if weather in weather_types:
            break
        print("请输入有效的天气类型！")
    # 获取用户预算
    while True:
        try:
            budget = float(input("请输入您的预算（元）: "))
            if budget > 0:
                break
            print("预算必须大于0元")
        except ValueError:
            print("请输入有效的数字")
    # 获取最低健康度要求
    print("健康度评分说明：")
    print("1-2：高热量、高油脂、重口味（如炸鸡、快餐）")
    print("3-4：一般快餐、重口味、油脂偏高")
    print("5-6：普通家常菜、主食搭配，营养适中")
    print("7-8：清淡、荤素搭配、蛋白质丰富")
    print("9-10：高纤维、低脂肪、蔬菜水果、健身餐")
    while True:
        try:
            min_health = int(input("请输入最低健康度要求（1-10）："))
            if 1 <= min_health <= 10:
                break
            print("健康度必须在1-10之间")
        except ValueError:
            print("请输入有效的数字")
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
        print("\n抱歉，没有找到符合您要求的食物。请调整预算或健康度要求，或清空近期饮食记录。")
        return None
    print("\n思考中", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    recommendation = random.choice(suitable_options)
    print(f"\n\n今天推荐您吃: {recommendation.name}! 😋")
    print(f"预计价格范围: ¥{recommendation.min_price}-{recommendation.max_price}")
    print(f"健康度评分: {'🍎' * recommendation.health_rating}{'⭐' * (10-recommendation.health_rating)}")
    print(f"推荐理由: {recommendation.description}")
    print(f"适合天气: {', '.join(recommendation.tags)}\n")
    add_recent_food(recommendation.name)
    return recommendation

def guess_you_like():
    food_options = get_food_options()
    food = random.choice(food_options)
    print("\n=== 猜你今天会喜欢 ===\n")
    print(f"{food.name}  (预计价格: ¥{food.min_price}-{food.max_price})")
    print(f"健康度评分: {'🍎' * food.health_rating}{'⭐' * (10-food.health_rating)}")
    print(f"推荐理由: {food.description}")
    print(f"适合天气: {', '.join(food.tags)}\n")

def main():
    while True:
        print("\n主菜单：\n1. 推荐今天吃什么\n2. 录入今天已吃食品\n3. 查看近期饮食记录\n4. 清空近期饮食记录\n5. 猜你喜欢\n6. 退出\n")
        choice = input("请选择功能（1-6）：")
        if choice == '1':
            get_food_recommendation()
        elif choice == '2':
            food = input("请输入你今天已吃的食品名称：").strip()
            if food:
                add_recent_food(food)
                print("已录入。\n")
        elif choice == '3':
            show_recent_foods()
        elif choice == '4':
            clear_recent_foods()
            print("已清空近期饮食记录。\n")
        elif choice == '5':
            guess_you_like()
        elif choice == '6':
            print("\n祝您用餐愉快！👋\n")
            break
        else:
            print("无效选择，请重新输入。\n")

if __name__ == "__main__":
    main()