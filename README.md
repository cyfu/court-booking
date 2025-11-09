# 🎾 Court Booking System

一个用于自动检查和预订 Angus Glen Tennis Centre 网球场地的 Python 系统。

## ✨ 主要功能

- ✅ **检查场地可用性** - 检查所有4个网球场的可用时间段
- ✅ **SMS 通知** - 通过 Twilio 将查询结果发送到手机
- ✅ **认证管理** - 自动处理 PerfectMind 系统的认证和会话管理
- ✅ **预订模拟** - 模拟预订流程（需要进一步开发真实预订功能）
- ✅ **错误处理** - 完善的错误处理和状态报告

## 🚀 快速开始

### 安装依赖
```bash
# 安装 uv (如果还没有安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync
```

### 检查场地可用性
```bash
# 检查所有场地的可用性（会自动发送 SMS 通知，如果已配置）
uv run python check_availability.py

# 或者使用预订系统检查
uv run python book_court.py check
```

### 配置 SMS 通知（可选）

1. 按照 [TWILIO_SETUP.md](TWILIO_SETUP.md) 的说明设置 Twilio 账号
2. 在项目根目录创建 `.env` 文件并配置 Twilio 凭证
3. 运行 `check_availability.py` 时，查询结果会自动通过 SMS 发送到配置的手机号码

### 预订功能（模拟）
```bash
# 自动预订下一个可用时间段
uv run python book_court.py book

# 交互式模式
uv run python book_court.py
```

## 📁 项目结构

- `PerfectMindSession.py` - 核心会话管理类
- `check_availability.py` - 可用性检查脚本（集成 SMS 通知）
- `sms_notifier.py` - Twilio SMS 通知模块
- `book_court.py` - 预订系统脚本
- `debug_api.py` - API 调试工具
- `court-info.json` - 场地配置信息
- `DOCUMENTATION.md` - 详细文档
- `TWILIO_SETUP.md` - Twilio SMS 配置指南

## 🏟️ 场地信息

| 场地 | Facility ID | 状态 |
|------|-------------|------|
| Court 1 | fb8d7c62-2760-48a9-9ecb-b89d8a6e02c2 | ✅ |
| Court 2 | d99a2d25-dcc1-4bdf-a3bf-d9e0024fc623 | ✅ |
| Court 3 | 02753035-ffab-4b9d-8f97-6fff7c46b88c | ✅ |
| Court 4 | a80258b8-9b5b-4349-addf-3da3e80d9292 | ✅ |

## 🔧 开发工具

### 添加依赖
```bash
# 添加运行时依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name
```

### 测试和代码检查
```bash
# 运行测试
uv run pytest

# 代码格式化
uv run autopep8 --in-place --recursive .
uv run flake8 .
```

### API 调试
```bash
# 查看原始 API 响应
uv run python debug_api.py
```

## 📖 详细文档

查看 [DOCUMENTATION.md](DOCUMENTATION.md) 获取完整的技术文档和 API 分析。

## 🚧 下一步开发

- 🔐 用户认证系统
- 💳 支付处理集成
- 📱 Web 界面
- ⏰ 定时自动预订

## ⚠️ 注意事项

- 预订需要 Angus Glen Tennis Centre Player's Card
- 当前版本为模拟预订，需要进一步开发真实预订功能
- API 响应格式可能会变化

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！