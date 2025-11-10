# 🎾 Court Booking System

一个用于自动检查和预订 Angus Glen Tennis Centre 网球场地的 Python 系统。

## 🚀 功能特性

### ✅ 已实现功能
1. **检查场地可用性** - 检查所有4个网球场的可用时间段
2. **认证管理** - 自动处理 PerfectMind 系统的认证和会话管理
3. **数据解析** - 解析 API 响应并提取可用时间段信息
4. **预订模拟** - 模拟预订流程（需要进一步开发真实预订功能）

### 🔧 技术实现
- **会话管理**: 自动获取和刷新验证令牌
- **API 集成**: 与 PerfectMind 预订系统集成
- **错误处理**: 完善的错误处理和状态报告
- **数据解析**: 智能解析可用性数据

## 📁 项目结构

```
court-booking/
├── PerfectMindSession.py    # 核心会话管理类
├── check_availability.py    # 可用性检查脚本
├── book_court.py           # 预订系统脚本
├── debug_api.py           # API 调试工具
├── court-info.json        # 场地配置信息
├── pyproject.toml         # 项目配置
└── README.md             # 项目说明
```

## 🛠️ 安装和使用

### 安装依赖
```bash
uv sync
```

### 检查场地可用性
```bash
# 检查所有场地的可用性
uv run python check_availability.py

# 或者使用预订系统检查
uv run python book_court.py check
```

### 预订功能（模拟）
```bash
# 自动预订下一个可用时间段
uv run python book_court.py book

# 交互式模式
uv run python book_court.py
```

## 🔍 API 分析结果

### 认证流程
1. 访问场地页面获取验证令牌 (`__RequestVerificationToken`)
2. 提取会话 ID (`PMSessionId`)
3. 使用令牌进行 API 请求

### API 端点
- **场地页面**: `/Clients/BookMe4LandingPages/Facility`
- **可用性检查**: `/Clients/BookMe4LandingPages/FacilityAvailability`

### 响应格式
```json
{
  "availabilities": [
    {
      "date": "2024-10-06",
      "time": "09:00",
      "duration": 60,
      "facilityId": "fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2",
      "courtId": "...",
      "serviceId": "...",
      "price": 25.00,
      "available": true
    }
  ],
  "extraDaysInfo": null
}
```

## 🏟️ 场地信息

| 场地 | Facility ID | 状态 |
|------|-------------|------|
| Court 1 | fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2 | ✅ 已配置 |
| Court 2 | d99a2d25-dcc1-4bdf-a3bf-d9e0024fc623 | ✅ 已配置 |
| Court 3 | 02753035-ffab-4b9d-8f97-6fff7c46b88c | ✅ 已配置 |
| Court 4 | a80258b8-9b5b-4349-addf-3da3e80d9292 | ✅ 已配置 |

## 🔧 配置说明

### court-info.json
```json
{
  "widgetId": "f3086c1c-7fa3-47fd-9976-0e777c8a7456",
  "calendarId": "7998c433-21f7-4914-8b85-9c61d6392511",
  "url": "https://cityofmarkham.perfectmind.com/Clients/BookMe4LandingPages/Facility",
  "courts": [
    {
      "court": 1,
      "facilityId": "fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2"
    }
    // ... 其他场地
  ]
}
```

## 🚧 下一步开发

### 需要实现的功能
1. **用户认证** - 实现用户登录功能
2. **真实预订** - 实现实际的场地预订 API 调用
3. **支付处理** - 集成支付系统
4. **通知系统** - 预订成功/失败通知
5. **定时检查** - 定期检查可用性并自动预订

### 技术改进
1. **数据库存储** - 存储预订历史和用户偏好
2. **Web 界面** - 创建 Web 界面
3. **移动应用** - 开发移动应用
4. **API 服务** - 提供 REST API 服务

## 🐛 调试工具

### API 调试
```bash
# 查看原始 API 响应
uv run python debug_api.py
```

### 日志文件
- `debug_response.json` - API 响应数据
- `{court}.html` - 场地页面 HTML（如果生成）

## 📝 注意事项

1. **Player's Card 要求**: 预订需要 Angus Glen Tennis Centre Player's Card
2. **API 限制**: 可能存在请求频率限制
3. **数据格式**: API 响应格式可能会变化
4. **认证过期**: 验证令牌会过期，需要定期刷新

## 📅 查询特定日期可用性

你可以使用 `check_availability` 方法的 `date` 参数来查询特定日期的可用性：

```python
from PerfectMindSession import PerfectMindSession

session = PerfectMindSession()

# 查询特定日期的可用性
availability_data = session.check_availability(
    facility_id="fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2",  # Court 1
    date="2025-10-07",  # 特定日期，格式：YYYY-MM-DD
    days_count=7,       # API 需要多天查询
    duration=60         # 持续时间（分钟）
)

# 解析结果
slots = session.parse_availability_data(availability_data)

# 过滤特定日期
target_slots = [slot for slot in slots if slot['date'] == "2025-10-07"]

for slot in target_slots:
    print(f"{slot['time']} ({slot['group']}) - {slot['duration']}")
```

### 命令行使用

使用提供的脚本来查询特定日期：

```bash
# 查询所有场地在特定日期的可用性
uv run python query_specific_date.py 2025-10-07

# 只查询 Court 1 在特定日期的可用性
uv run python query_date.py 2025-10-07
```

### 重要说明

- **日期格式**: 使用 `YYYY-MM-DD` 格式 (例如: `2025-10-07`)
- **API 限制**: API 需要 `days_count=7` 即使只查询单天
- **时区**: 所有日期都使用多伦多时区处理
- **过滤**: 结果会被过滤以只显示请求的日期

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License
