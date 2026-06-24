## Agent for Beginners

## OpenAI Chat 协议

OpenAI Chat 协议的核心是 `messages`：程序把一组带 `role` 的消息发给模型，模型根据这些上下文生成下一条 `assistant` 消息。它看起来像聊天记录，但对程序来说更像是一种结构化的请求格式。

### 纯对话

请求：

```json
{
  "model": "gpt-4.1-mini",
  "messages": [
    {
      "role": "developer",
      "content": "你是一个面向初学者的中文编程老师。回答要准确、简洁。"
    },
    {
      "role": "user",
      "content": "用一句话解释什么是函数。"
    }
  ]
}
```

回复：

```json
{
  "role": "assistant",
  "content": "函数是一段可以被重复调用的代码，用来接收输入、执行逻辑，并返回结果。"
}
```

- `developer`：放应用规则、身份设定、输出风格等要求。
- `user`：用户输入的问题或上下文。
- `assistant`：模型生成的回复，也可以放回历史里形成多轮对话。
- `tool`：工具执行结果，只有接入外部工具时才会用到。

### 工具调用

如果模型需要实时数据、数据库查询、计算器、搜索等外部能力，可以在请求里声明 `tools`。模型不会真正执行工具，而是返回要调用哪个工具和参数；程序执行后，再把结果作为 `tool` 消息发回给模型。

请求：

```json
{
  "model": "gpt-4.1-mini",
  "temperature": 0.3,
  "max_tokens": 800,
  "messages": [
    {
      "role": "developer",
      "content": "你是一个面向初学者的中文助手。回答要准确、简洁；如果需要实时数据，先调用工具，不要猜测。"
    },
    {
      "role": "user",
      "content": "北京今天适合夜跑吗？顺便提醒我应该注意什么。"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "查询指定城市的当前天气和空气质量。",
        "parameters": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "城市名称，例如 Beijing、Shanghai。"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["city", "unit"],
          "additionalProperties": false
        }
      }
    }
  ]
}
```

模型回复，要求调用工具：

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_weather_001",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\":\"Beijing\",\"unit\":\"celsius\"}"
      }
    }
  ]
}
```

程序执行工具后，再发一次请求：

```json
{
  "model": "gpt-4.1-mini",
  "messages": [
    {
      "role": "developer",
      "content": "你是一个面向初学者的中文助手。回答要准确、简洁；如果需要实时数据，先调用工具，不要猜测。"
    },
    {
      "role": "user",
      "content": "北京今天适合夜跑吗？顺便提醒我应该注意什么。"
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_weather_001",
          "type": "function",
          "function": {
            "name": "get_weather",
            "arguments": "{\"city\":\"Beijing\",\"unit\":\"celsius\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_weather_001",
      "content": "{\"city\":\"Beijing\",\"temperature\":24,\"condition\":\"clear\",\"aqi\":62,\"wind\":\"light\"}"
    }
  ]
}
```

最终回复：

```json
{
  "role": "assistant",
  "content": "北京当前约 24°C，天气晴，风力较小，AQI 62。可以夜跑，但空气质量一般，建议选择车流少的路线，把强度控制在轻到中等；如果对空气敏感，可以缩短时间或改成室内运动。"
}
```
