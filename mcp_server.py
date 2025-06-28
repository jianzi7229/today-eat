#!/usr/bin/env python3
"""
MCP Server for Food Recommendation and Football Stats
"""

import json
import sys
import subprocess
import os
from typing import Dict, Any, List, Optional
import importlib.util

# 导入食物推荐模块
sys.path.append('.')
from food_recommendation import get_food_options, add_recent_food, read_recent_foods, clear_recent_foods

class MCPServer:
    def __init__(self):
        self.server_name = "food-recommendation-server"
        self.version = "1.0.0"
        
    def send_response(self, response: Dict[str, Any]):
        """发送响应到标准输出"""
        print(json.dumps(response), flush=True)
        
    def read_request(self) -> Optional[Dict[str, Any]]:
        """从标准输入读取请求"""
        try:
            line = input()
            return json.loads(line)
        except EOFError:
            return None
        except json.JSONDecodeError:
            return None
            
    def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理初始化请求"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.server_name,
                    "version": self.version
                }
            }
        }
        
    def handle_list_tools(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具列表请求"""
        tools = [
            {
                "name": "get_food_recommendation",
                "description": "根据天气、预算和健康度要求推荐食物",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "weather": {
                            "type": "string",
                            "enum": ["晴天", "雨天", "炎热", "寒冷"],
                            "description": "当前天气类型"
                        },
                        "budget": {
                            "type": "number",
                            "description": "预算金额（元）"
                        },
                        "min_health": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                            "description": "最低健康度要求（1-10）"
                        }
                    },
                    "required": ["weather", "budget", "min_health"]
                }
            },
            {
                "name": "add_recent_food",
                "description": "添加已食用的食物到记录中",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "food_name": {
                            "type": "string",
                            "description": "食物名称"
                        }
                    },
                    "required": ["food_name"]
                }
            },
            {
                "name": "get_recent_foods",
                "description": "获取最近食用的食物记录",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "clear_recent_foods",
                "description": "清空最近的食物记录",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_football_stats",
                "description": "获取英超球员进球数据",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "season_id": {
                            "type": "integer",
                            "description": "赛季ID（默认719）",
                            "default": 719
                        }
                    }
                }
            },
            {
                "name": "get_file_content",
                "description": "读取指定文件的内容",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": tools
            }
        }
        
    def handle_call_tool(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理工具调用请求"""
        params = request.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if name == "get_food_recommendation":
                result = self.get_food_recommendation(arguments)
            elif name == "add_recent_food":
                result = self.add_recent_food(arguments)
            elif name == "get_recent_foods":
                result = self.get_recent_foods()
            elif name == "clear_recent_foods":
                result = self.clear_recent_foods()
            elif name == "get_football_stats":
                result = self.get_football_stats(arguments)
            elif name == "get_file_content":
                result = self.get_file_content(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
                
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    def get_food_recommendation(self, args: Dict[str, Any]) -> str:
        """获取食物推荐"""
        weather = args.get("weather")
        budget = args.get("budget")
        min_health = args.get("min_health")
        
        food_options = get_food_options()
        recent_foods = set(read_recent_foods())
        
        # 筛选符合条件的食物
        suitable_options = [
            food for food in food_options
            if (food.min_price <= budget and 
                food.health_rating >= min_health and 
                food.name not in recent_foods)
        ]
        
        # 根据天气优先筛选
        weather_options = [food for food in suitable_options if weather in food.tags]
        if weather_options:
            suitable_options = weather_options
            
        if not suitable_options:
            return "抱歉，没有找到符合您要求的食物。请调整预算或健康度要求，或清空近期饮食记录。"
            
        import random
        recommendation = random.choice(suitable_options)
        
        # 添加到最近记录
        add_recent_food(recommendation.name)
        
        result = f"""🌞 今天推荐：**{recommendation.name}** 😋

📊 推荐详情：
- **价格范围**: ¥{recommendation.min_price}-{recommendation.max_price}
- **健康度评分**: {'🍎' * recommendation.health_rating}{'⭐' * (10-recommendation.health_rating)} ({recommendation.health_rating}分)
- **推荐理由**: {recommendation.description}
- **适合天气**: {', '.join(recommendation.tags)}

🎯 为什么推荐这个？
- 符合你的预算要求（¥{budget}以内）
- 健康度{recommendation.health_rating}分，超过你的{min_health}分要求
- 适合{weather}天气
- 营养均衡，口感佳

今天是个好天气，来一份{recommendation.name}吧！既满足了你的健康要求，又不会超出预算。😋"""
        
        return result
    
    def add_recent_food(self, args: Dict[str, Any]) -> str:
        """添加最近食物记录"""
        food_name = args.get("food_name")
        add_recent_food(food_name)
        return f"已成功添加 '{food_name}' 到食物记录中"
    
    def get_recent_foods(self) -> str:
        """获取最近食物记录"""
        foods = read_recent_foods()
        if not foods:
            return "暂无食物记录"
        return f"最近食用的食物：\n" + "\n".join([f"- {food}" for food in foods])
    
    def clear_recent_foods(self) -> str:
        """清空最近食物记录"""
        clear_recent_foods()
        return "已清空食物记录"
    
    def get_football_stats(self, args: Dict[str, Any]) -> str:
        """获取足球统计数据"""
        try:
            result = subprocess.run(
                ["python3", "football_stats.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"获取足球数据失败: {result.stderr}"
        except Exception as e:
            return f"执行足球数据脚本失败: {str(e)}"
    
    def get_file_content(self, args: Dict[str, Any]) -> str:
        """读取文件内容"""
        file_path = args.get("file_path")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"
    
    def run(self):
        """运行 MCP 服务器"""
        print("MCP Food Recommendation Server is starting...", file=sys.stderr)
        
        while True:
            request = self.read_request()
            if request is None:
                break
                
            method = request.get("method")
            
            if method == "initialize":
                response = self.handle_initialize(request)
            elif method == "tools/list":
                response = self.handle_list_tools(request)
            elif method == "tools/call":
                response = self.handle_call_tool(request)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            self.send_response(response)

if __name__ == "__main__":
    server = MCPServer()
    server.run() 