# Twilio SMS 配置指南

## 设置步骤

### 1. 注册 Twilio 账号

1. 访问 [Twilio 官网](https://www.twilio.com/) 注册账号
2. 完成账号验证

### 2. 获取 Twilio 凭证

1. 登录 [Twilio Console](https://console.twilio.com/)
2. 在 Dashboard 中找到以下信息：
   - **Account SID**: 你的账户标识符
   - **Auth Token**: 你的认证令牌（点击眼睛图标显示）

### 3. 设置 Messaging Service（推荐方式）

1. 在 Twilio Console 中，进入 **Messaging** > **Services** > **Create Messaging Service**
2. 创建 Messaging Service 后，你会得到一个 **Messaging Service SID**（格式：`MG...`）
3. 在 Messaging Service 中添加电话号码：
   - 进入你的 Messaging Service
   - 点击 **Phone Numbers** > **Add Phone Number**
   - 选择或购买一个加拿大电话号码

**或者使用直接电话号码方式：**

1. 在 Twilio Console 中，进入 **Phone Numbers** > **Manage** > **Buy a number**
2. 选择一个加拿大电话号码（根据 [Twilio 加拿大定价](https://www.twilio.com/en-us/sms/pricing/ca)）
3. 购买后，你会得到一个格式如 `+1234567890` 的电话号码

### 4. 配置环境变量

在项目根目录创建 `.env` 文件（如果不存在），添加以下内容：

**方式一：使用 Messaging Service（推荐）**
```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_MESSAGING_SERVICE_SID=MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TO_PHONE_NUMBER=+14168546018
```

**方式二：使用直接电话号码**
```bash
# Twilio SMS Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_TO_PHONE_NUMBER=+14168546018
```

**重要提示：**
- **推荐使用 Messaging Service SID**：更灵活，可以自动选择最佳电话号码
- `TWILIO_MESSAGING_SERVICE_SID`: 你的 Messaging Service SID（格式：`MG...`）
- `TWILIO_PHONE_NUMBER`: 你的 Twilio 电话号码（仅在未使用 Messaging Service 时使用）
- `TWILIO_TO_PHONE_NUMBER`: 接收短信的手机号码（格式：+国家代码+号码，例如加拿大：+14168546018）
- 确保 `.env` 文件已添加到 `.gitignore` 中，不要提交到版本控制

### 5. 安装依赖

```bash
uv sync
```

### 6. 测试 SMS 功能

运行场地查询脚本，如果配置正确，查询结果会自动通过 SMS 发送：

```bash
uv run python check_availability.py
```

## 费用说明

根据 [Twilio 加拿大 SMS 定价](https://www.twilio.com/en-us/sms/pricing/ca)：

- **Long Code 发送**: 基础价格 + 运营商费用
- **接收短信**: 免费（某些运营商可能收费）
- **电话号码月租**: Long Code $1.15/月，Toll-free $2.15/月

详细定价请参考 [Twilio 定价页面](https://www.twilio.com/en-us/sms/pricing/ca)

## 故障排除

### SMS 未发送

1. 检查环境变量是否正确设置：
   ```bash
   echo $TWILIO_ACCOUNT_SID
   echo $TWILIO_AUTH_TOKEN
   ```

2. 检查日志输出，查看是否有错误信息

3. 验证电话号码格式是否正确（必须包含国家代码，如 +1）

4. 在 Twilio Console 的 **Monitor** > **Logs** > **Messaging** 中查看发送日志

### 常见错误

- **"Invalid phone number"**: 电话号码格式错误，确保使用 E.164 格式（+国家代码+号码）
- **"Authentication failed"**: Account SID 或 Auth Token 错误
- **"Unverified phone number"**: 在试用账户中，只能发送到已验证的电话号码

