const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

class FoodRecommendationServer {
  constructor() {
    this.server = new Server(
      {
        name: 'food-recommendation-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
  }

  setupToolHandlers() {
    // 获取食物推荐
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'get_food_recommendation',
            description: '根据天气、预算和健康度要求推荐食物',
            inputSchema: {
              type: 'object',
              properties: {
                weather: {
                  type: 'string',
                  enum: ['晴天', '雨天', '炎热', '寒冷'],
                  description: '当前天气类型'
                },
                budget: {
                  type: 'number',
                  description: '预算金额（元）'
                },
                min_health: {
                  type: 'integer',
                  minimum: 1,
                  maximum: 10,
                  description: '最低健康度要求（1-10）'
                }
              },
              required: ['weather', 'budget', 'min_health']
            }
          },
          {
            name: 'add_recent_food',
            description: '添加已食用的食物到记录中',
            inputSchema: {
              type: 'object',
              properties: {
                food_name: {
                  type: 'string',
                  description: '食物名称'
                }
              },
              required: ['food_name']
            }
          },
          {
            name: 'get_recent_foods',
            description: '获取最近食用的食物记录',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'clear_recent_foods',
            description: '清空最近的食物记录',
            inputSchema: {
              type: 'object',
              properties: {}
            }
          },
          {
            name: 'get_football_stats',
            description: '获取英超球员进球数据',
            inputSchema: {
              type: 'object',
              properties: {
                season_id: {
                  type: 'integer',
                  description: '赛季ID（默认719）',
                  default: 719
                }
              }
            }
          },
          {
            name: 'get_file_content',
            description: '读取指定文件的内容',
            inputSchema: {
              type: 'object',
              properties: {
                file_path: {
                  type: 'string',
                  description: '文件路径'
                }
              },
              required: ['file_path']
            }
          }
        ]
      };
    });

    // 处理工具调用
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'get_food_recommendation':
            return await this.getFoodRecommendation(args);
          case 'add_recent_food':
            return await this.addRecentFood(args);
          case 'get_recent_foods':
            return await this.getRecentFoods();
          case 'clear_recent_foods':
            return await this.clearRecentFoods();
          case 'get_football_stats':
            return await this.getFootballStats(args);
          case 'get_file_content':
            return await this.getFileContent(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`
            }
          ]
        };
      }
    });
  }

  async getFoodRecommendation(args) {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', ['food_recommendation.py'], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: output
              }
            ]
          });
        } else {
          reject(new Error(`Python process failed: ${errorOutput}`));
        }
      });

      // 发送参数到Python脚本
      const input = `${args.weather}\n${args.budget}\n${args.min_health}\n`;
      pythonProcess.stdin.write(input);
      pythonProcess.stdin.end();
    });
  }

  async addRecentFood(args) {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', ['-c', `
import sys
sys.path.append('.')
from food_recommendation import add_recent_food
add_recent_food('${args.food_name}')
print('已成功添加食物记录')
      `]);

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: output
              }
            ]
          });
        } else {
          reject(new Error(`Python process failed: ${errorOutput}`));
        }
      });
    });
  }

  async getRecentFoods() {
    try {
      const content = fs.readFileSync('recent_foods.txt', 'utf8');
      const foods = content.split('\n').filter(line => line.trim());
      
      return {
        content: [
          {
            type: 'text',
            text: foods.length > 0 ? 
              `最近食用的食物：\n${foods.map(food => `- ${food}`).join('\n')}` :
              '暂无食物记录'
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: '暂无食物记录'
          }
        ]
      };
    }
  }

  async clearRecentFoods() {
    try {
      if (fs.existsSync('recent_foods.txt')) {
        fs.unlinkSync('recent_foods.txt');
      }
      return {
        content: [
          {
            type: 'text',
            text: '已清空食物记录'
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `清空记录失败: ${error.message}`
          }
        ]
      };
    }
  }

  async getFootballStats(args) {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', ['footgpt.py']);

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: output
              }
            ]
          });
        } else {
          reject(new Error(`Python process failed: ${errorOutput}`));
        }
      });
    });
  }

  async getFileContent(args) {
    try {
      const filePath = path.resolve(args.file_path);
      const content = fs.readFileSync(filePath, 'utf8');
      
      return {
        content: [
          {
            type: 'text',
            text: content
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `读取文件失败: ${error.message}`
          }
        ]
      };
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('MCP Food Recommendation Server is running...');
  }
}

// 启动服务器
const server = new FoodRecommendationServer();
server.run().catch(console.error); 