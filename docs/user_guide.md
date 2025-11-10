# 用户指南

欢迎使用 Court Booking System！本指南将帮助您快速上手，轻松检查和预订 Angus Glen Tennis Centre 的网球场。

## 1. 系统要求

- Python 3.8+
- `uv` 包管理器

## 2. 安装与配置

### 步骤 1: 安装 `uv`

如果您尚未安装 `uv`，请在终端中运行以下命令：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 步骤 2: 克隆项目并安装依赖

```bash
git clone https://github.com/cyfu/court-booking.git
cd court-booking
uv sync
```

### 步骤 3: 配置环境变量 (可选，用于 SMS 通知)

如果您希望接收场地可用性的 SMS 通知，需要配置 Twilio 凭证。

1.  **获取 Twilio 凭证**:
    *   注册或登录 [Twilio](https://www.twilio.com/) 账户。
    *   获取您的 `Account SID`, `Auth Token` 和一个 Twilio 电话号码。
    *   详细步骤请参考 `TWILIO_SETUP.md`。

2.  **创建 `.env` 文件**:
    在项目根目录创建一个名为 `.env` 的文件，并填入以下内容：

    ```env
    # .env
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TWILIO_AUTH_TOKEN=your_auth_token
    TWILIO_PHONE_NUMBER=+15017122661
    RECIPIENT_PHONE_NUMBER=+1234567890
    ```

    - `RECIPIENT_PHONE_NUMBER`: 替换为您希望接收通知的手机号码。

## 3. 如何使用

### 检查场地可用性

这是系统的核心功能。运行以下命令后，系统将查询所有场地的可用时间段，并将结果打印到控制台。如果配置了 SMS，结果也会发送到您的手机。

```bash
uv run check-availability
```

**示例输出**:

```
Court 1 is available at: 09:00 AM, 10:00 AM
Court 2 has no availability.
Court 3 is available at: 01:00 PM
Court 4 is available at: 04:00 PM
```


## 4. 常见问题

**Q: 我需要有 Angus Glen 的会员卡吗？**
A: 是的，真实的预订流程需要有效的 Player's Card。当前系统主要用于检查可用性。

**Q: 这个工具可以预订场地吗？**
A: 不可以。本项目专注于提供实时的场地可用性信息，不包含预订功能。

**Q: 如果 API 变化了怎么办？**
A: 本项目依赖于非官方 API，可能会随时发生变化。如果脚本运行失败，请提交 Issue，我们会尽快跟进。
