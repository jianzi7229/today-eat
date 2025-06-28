#!/usr/bin/env python3
"""
测试 MCP 服务器功能
"""

import subprocess
import json
import time

def test_mcp_server():
    """测试 MCP 服务器"""
    print("🚀 启动 MCP 服务器测试...")
    
    # 启动 MCP 服务器
    process = subprocess.Popen(
        ["python3", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 发送初始化请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("📤 发送初始化请求...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # 读取响应
        response = process.stdout.readline()
        init_response = json.loads(response)
        print(f"📥 收到初始化响应: {init_response.get('result', {}).get('serverInfo', {}).get('name')}")
        
        # 发送工具列表请求
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("📤 发送工具列表请求...")
        process.stdin.write(json.dumps(list_request) + "\n")
        process.stdin.flush()
        
        # 读取响应
        response = process.stdout.readline()
        list_response = json.loads(response)
        tools = list_response.get('result', {}).get('tools', [])
        print(f"📥 可用工具数量: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # 测试食物推荐功能
        food_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_food_recommendation",
                "arguments": {
                    "weather": "晴天",
                    "budget": 50,
                    "min_health": 7
                }
            }
        }
        
        print("\n🍽️ 测试食物推荐功能...")
        process.stdin.write(json.dumps(food_request) + "\n")
        process.stdin.flush()
        
        # 读取响应
        response = process.stdout.readline()
        food_response = json.loads(response)
        result = food_response.get('result', {}).get('content', [{}])[0].get('text', '')
        print("📥 食物推荐结果:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        print("\n✅ MCP 服务器测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        # 关闭进程
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_mcp_server() 