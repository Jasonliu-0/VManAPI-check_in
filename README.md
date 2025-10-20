# VManAPI 自动签到

🤖 基于 Python + GitHub Actions 的 VManAPI 每日自动签到脚本

## ✨ 功能特性

- ✅ **请求头随机化** - 自动随机化 User-Agent、浏览器特征等请求头,保护隐私
- ✅ **多账号支持** - 支持单账号或多账号轮询签到,灵活配置
- ✅ **自动签到** - GitHub Actions 定时自动签到,每天北京时间 8:00 执行
- ✅ **手动触发** - 支持本地运行和 GitHub Actions 手动触发
- ✅ **智能延迟** - 多账号间随机延迟 2-5 秒,避免请求过快
- ✅ **详细日志** - 完整的签到结果日志和汇总报告

## 📋 使用前准备

### 1. 获取 Authorization Token

1. 打开浏览器访问 [VManAPI](https://donate.avman.ai) 并登录您的账号
2. 按 `F12` 打开浏览器开发者工具
3. 切换到 **Network** (网络) 标签
4. 手动执行一次签到操作
5. 在网络请求列表中找到 `check_in` 请求并点击
6. 在右侧面板查看 **请求标头 (Request Headers)**
7. 找到 `Authorization` 字段,复制**整个 token 值**

**重要提示**:
- ✅ **正确格式**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjM4...` (仅复制 token 值)
- ❌ **错误格式**: `Authorization: eyJhbGc...` (不要包含 `Authorization:` 前缀)

**图文参考**: 参见截图中 Network → check_in → Headers → Authorization 字段

### 2. Fork 本仓库

点击右上角 `Fork` 按钮,将本仓库 Fork 到您的 GitHub 账号下

## 🚀 快速开始

### 方式一: GitHub Actions 自动签到 (推荐)

#### 1. 配置 Secret (环境变量)

在您 Fork 的仓库中配置敏感信息:

1. 点击仓库的 **Settings** (设置) 标签
2. 左侧菜单选择 **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 按钮
4. 添加以下配置:
   - **Name (变量名)**: `VMAN_AUTHORIZATION`
   - **Value (变量值)**: 根据您的需求配置单账号或多账号

**单账号配置**:
```
your_token_here
```

**多账号配置 (3种格式)**:
```
# 格式1: 逗号分隔 (自动命名为 账号1、账号2...)
token1,token2,token3

# 格式2: 自定义账号名称
主号:token1,小号:token2,备用:token3

# 格式3: 混合使用
主号:token1,token2,备用号:token3
```

**安全提醒**:
- ⚠️ Token 是您的账号凭证,请勿泄露给他人
- ✅ 使用 GitHub Secrets 可以安全地存储敏感信息
- ✅ 其他人 Fork 您的仓库后需要自行配置他们自己的 token

#### 2. 启用 GitHub Actions

1. 进入仓库的 `Actions` 标签
2. 点击 `I understand my workflows, go ahead and enable them`
3. 启用工作流

#### 3. 测试运行

- **自动运行**: 每天北京时间 8:00 自动执行
- **手动触发**:
  1. 进入 `Actions` 标签
  2. 选择 `VManAPI 每日自动签到` 工作流
  3. 点击 `Run workflow` → `Run workflow`

### 方式二: 本地手动签到

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

**方式 A: 使用 .env 文件 (推荐)**

1. 复制环境变量模板:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件,填写您的 token:

**单账号**:
```bash
VMAN_AUTHORIZATION=your_token_here
```

**多账号**:
```bash
# 格式1: 逗号分隔
VMAN_AUTHORIZATION=token1,token2,token3

# 格式2: 自定义名称
VMAN_AUTHORIZATION=主号:token1,小号:token2

# 格式3: 混合使用
VMAN_AUTHORIZATION=主号:token1,token2,备用:token3
```

**方式 B: 直接设置环境变量**

**Linux/macOS**:
```bash
# 单账号
export VMAN_AUTHORIZATION="your_token_here"

# 多账号
export VMAN_AUTHORIZATION="token1,token2,token3"
```

**Windows (CMD)**:
```cmd
set VMAN_AUTHORIZATION=your_token_here
```

**Windows (PowerShell)**:
```powershell
$env:VMAN_AUTHORIZATION="your_token_here"
```

#### 3. 执行签到

```bash
python check_in.py
```

## 📁 项目结构

```
VManAPI-check_in/
├── .github/
│   └── workflows/
│       └── daily_check_in.yml    # GitHub Actions 工作流配置
├── .env.example                   # 环境变量配置模板
├── .gitignore                     # Git 忽略规则
├── check_in.py                    # 签到主脚本
├── requirements.txt               # Python 依赖
├── LICENSE                        # MIT 开源协议
└── README.md                      # 项目说明
```

## 🔧 高级配置

### 1. 多账号配置示例

**场景 1: 2个账号,无自定义名称**
```bash
VMAN_AUTHORIZATION=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...,eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
输出日志:
```
📋 共发现 2 个账号待签到
[2025-01-20 08:00:00] 账号: 账号1
✅ 【账号1】签到成功!
[2025-01-20 08:00:03] 账号: 账号2
✅ 【账号2】签到成功!
```

**场景 2: 3个账号,自定义名称**
```bash
VMAN_AUTHORIZATION=主账号:token1,工作号:token2,测试号:token3
```
输出日志:
```
📋 共发现 3 个账号待签到
[2025-01-20 08:00:00] 账号: 主账号
✅ 【主账号】签到成功!
[2025-01-20 08:00:03] 账号: 工作号
✅ 【工作号】签到成功!
[2025-01-20 08:00:06] 账号: 测试号
✅ 【测试号】签到成功!
```

### 2. 请求头随机化说明

脚本会自动随机化以下请求头,保护您的隐私:

**浏览器池**:
- Chrome (版本 120-124)
- Microsoft Edge (版本 120-123)
- Firefox (版本 121-125)

**操作系统池**:
- Windows 10 (x64)
- Windows 11 (x64)
- macOS Catalina
- macOS Ventura

每次签到都会随机选择不同的浏览器和系统组合,避免被识别。

### 3. 修改签到时间

编辑 `.github/workflows/daily_check_in.yml`:

```yaml
on:
  schedule:
    # 格式: cron '分 时 日 月 周'
    # 当前: 每天 UTC 0:00 (北京时间 8:00)
    - cron: '0 0 * * *'
```

**时区转换参考**:
- 北京时间 8:00 = UTC 0:00 → `'0 0 * * *'`
- 北京时间 12:00 = UTC 4:00 → `'0 4 * * *'`
- 北京时间 20:00 = UTC 12:00 → `'0 12 * * *'`

### 4. 查看签到日志

1. 进入仓库的 `Actions` 标签
2. 选择最近的工作流运行记录
3. 点击 `check-in` job 查看详细日志

**日志示例**:
```
============================================================
VManAPI 自动签到工具
============================================================

📋 共发现 2 个账号待签到

============================================================
[2025-01-20 08:00:00] 账号: 主账号
开始执行签到...
使用 User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
响应状态码: 200
✅ 【主账号】签到成功!
⏱️  等待 3.2 秒后处理下一个账号...

============================================================
[2025-01-20 08:00:03] 账号: 小号
开始执行签到...
使用 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...
响应状态码: 200
✅ 【小号】签到成功!

============================================================
签到结果汇总
============================================================
✅ 成功 - 主账号: 签到成功
✅ 成功 - 小号: 签到成功

总计: 2 个账号, 成功 2 个, 失败 0 个
完成时间: 2025-01-20 08:00:06
============================================================
```

## ⚠️ 注意事项

1. **Token 安全 (重要)**:
   - ❌ **绝对不要**将 Authorization token 直接写入代码或提交到 Git
   - ✅ **必须使用** GitHub Secrets 或环境变量存储敏感信息
   - ✅ 其他人 Fork 后需要配置**他们自己的 token**,不能使用您的

2. **Token 格式**:
   - ✅ 仅复制 token 值本身,格式如: `eyJhbGciOiJIUzI1NiIs...`
   - ❌ 不要包含前缀如 `authorization:` 或 `Bearer `

3. **Token 有效期**:
   - Token 可能会过期,过期后需要重新获取并更新 Secret
   - 如果签到突然失败,首先检查 token 是否过期

4. **签到频率**:
   - 建议每天签到一次即可
   - 多账号间已自动添加 2-5 秒随机延迟
   - 避免频繁触发,防止被服务器限制或封禁

5. **隐私保护**:
   - Fork 仓库后强烈建议设置为 **Private** (私有仓库)
   - 私有仓库同样可以使用 GitHub Actions
   - 脚本已实现请求头随机化,每次签到使用不同的浏览器特征

## 🐛 故障排查

### 签到失败常见原因

1. **401 Unauthorized**: Token 过期或无效,需重新获取
2. **403 Forbidden**: Token 权限不足或被封禁
3. **网络超时**: GitHub Actions 网络问题,稍后重试
4. **500 Server Error**: 服务器异常,稍后重试

### 调试方法

本地运行脚本查看详细错误信息:
```bash
python check_in.py
```

## 📄 开源协议

本项目采用 MIT 协议开源,详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## ⭐ Star History

如果这个项目对您有帮助,欢迎 Star ⭐

---

**免责声明**: 本项目仅供学习交流使用,请遵守相关服务条款,不得用于违规用途。
