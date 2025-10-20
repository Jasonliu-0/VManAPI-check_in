#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VManAPI 自动签到脚本
支持本地运行和 GitHub Actions 定时任务
功能:
- 请求头随机化,保护隐私
- 多账号轮询签到
"""

import os
import sys
import random
import time
import requests
from datetime import datetime
from typing import List, Dict


class UserAgentGenerator:
    """User-Agent 随机生成器"""

    # 主流浏览器版本池
    BROWSERS = [
        # Chrome
        {
            "name": "Chrome",
            "versions": ["120.0.0.0", "121.0.0.0", "122.0.0.0", "123.0.0.0", "124.0.0.0"],
            "ua_template": "Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
        },
        # Edge
        {
            "name": "Edge",
            "versions": ["120.0.0.0", "121.0.0.0", "122.0.0.0", "123.0.0.0"],
            "ua_template": "Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 Edg/{version}"
        },
        # Firefox
        {
            "name": "Firefox",
            "versions": ["121.0", "122.0", "123.0", "124.0", "125.0"],
            "ua_template": "Mozilla/5.0 ({os}; rv:{version}) Gecko/20100101 Firefox/{version}"
        }
    ]

    OS_CONFIGS = [
        {
            "platform": "Windows",
            "os_string": "Windows NT 10.0; Win64; x64",
            "sec_ch_ua_platform": '"Windows"'
        },
        {
            "platform": "Windows",
            "os_string": "Windows NT 11.0; Win64; x64",
            "sec_ch_ua_platform": '"Windows"'
        },
        {
            "platform": "macOS",
            "os_string": "Macintosh; Intel Mac OS X 10_15_7",
            "sec_ch_ua_platform": '"macOS"'
        },
        {
            "platform": "macOS",
            "os_string": "Macintosh; Intel Mac OS X 13_5_0",
            "sec_ch_ua_platform": '"macOS"'
        }
    ]

    @classmethod
    def generate(cls) -> Dict[str, str]:
        """
        生成随机 User-Agent 和相关请求头

        Returns:
            dict: 包含 User-Agent 和其他浏览器特征头
        """
        browser = random.choice(cls.BROWSERS)
        os_config = random.choice(cls.OS_CONFIGS)
        version = random.choice(browser["versions"])

        # 构建 User-Agent
        if browser["name"] == "Edge":
            chrome_ver = random.choice(cls.BROWSERS[0]["versions"])
            ua = browser["ua_template"].format(
                os=os_config["os_string"],
                chrome_ver=chrome_ver,
                version=version
            )
            sec_ch_ua = f'"Microsoft Edge";v="{version.split(".")[0]}", "Chromium";v="{chrome_ver.split(".")[0]}", "Not?A_Brand";v="8"'
        elif browser["name"] == "Chrome":
            ua = browser["ua_template"].format(
                os=os_config["os_string"],
                version=version
            )
            sec_ch_ua = f'"Google Chrome";v="{version.split(".")[0]}", "Chromium";v="{version.split(".")[0]}", "Not?A_Brand";v="8"'
        else:  # Firefox
            ua = browser["ua_template"].format(
                os=os_config["os_string"],
                version=version
            )
            sec_ch_ua = None  # Firefox 不使用 Sec-CH-UA

        return {
            "user_agent": ua,
            "sec_ch_ua": sec_ch_ua,
            "sec_ch_ua_platform": os_config["sec_ch_ua_platform"],
            "browser": browser["name"]
        }


class VManAPICheckIn:
    """VManAPI 签到类"""

    # Accept-Language 语言池
    ACCEPT_LANGUAGES = [
        "zh-CN,zh;q=0.9,en;q=0.8",
        "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "zh-CN,zh;q=0.9",
        "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    ]

    def __init__(self, authorization: str, account_name: str = "默认账号"):
        """
        初始化签到客户端

        Args:
            authorization: Authorization token (从浏览器开发者工具中获取)
            account_name: 账号名称 (用于日志显示)
        """
        self.authorization = authorization
        self.account_name = account_name
        self.base_url = "https://donate.avman.ai"
        self.check_in_url = f"{self.base_url}/api/check_in"

    def _generate_headers(self) -> dict:
        """
        生成随机化的请求头

        Returns:
            dict: 请求头字典
        """
        # 获取随机 UA 和浏览器特征
        ua_info = UserAgentGenerator.generate()

        # 基础请求头
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": random.choice(self.ACCEPT_LANGUAGES),
            "Authorization": self.authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/checkIn?_userMenuKey=checkIn",
            "User-Agent": ua_info["user_agent"]
        }

        # 仅 Chromium 系列添加 Sec-CH-UA 头
        if ua_info["sec_ch_ua"]:
            headers.update({
                "Sec-Ch-Ua": ua_info["sec_ch_ua"],
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": ua_info["sec_ch_ua_platform"],
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            })

        return headers

    def check_in(self) -> dict:
        """
        执行签到操作

        Returns:
            dict: 签到结果
        """
        try:
            print(f"\n{'='*60}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 账号: {self.account_name}")
            print(f"开始执行签到...")

            # 生成随机请求头
            headers = self._generate_headers()
            print(f"使用 User-Agent: {headers['User-Agent'][:50]}...")

            response = requests.post(
                self.check_in_url,
                headers=headers,
                timeout=30
            )

            print(f"响应状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"响应内容: {result}")
                print(f"✅ 【{self.account_name}】签到成功!")
                return {
                    "success": True,
                    "account": self.account_name,
                    "message": "签到成功",
                    "data": result
                }
            else:
                print(f"响应内容: {response.text}")
                print(f"❌ 【{self.account_name}】签到失败: HTTP {response.status_code}")
                return {
                    "success": False,
                    "account": self.account_name,
                    "message": f"签到失败: HTTP {response.status_code}",
                    "error": response.text
                }

        except requests.exceptions.RequestException as e:
            print(f"❌ 【{self.account_name}】网络请求异常: {str(e)}")
            return {
                "success": False,
                "account": self.account_name,
                "message": f"网络请求异常: {str(e)}"
            }
        except Exception as e:
            print(f"❌ 【{self.account_name}】未知错误: {str(e)}")
            return {
                "success": False,
                "account": self.account_name,
                "message": f"未知错误: {str(e)}"
            }


def parse_accounts(env_value: str) -> List[Dict[str, str]]:
    """
    解析环境变量中的多账号配置

    支持格式:
    1. 单账号: token
    2. 多账号 (逗号分隔): token1,token2,token3
    3. 多账号 (带名称): name1:token1,name2:token2

    Args:
        env_value: 环境变量值

    Returns:
        list: 账号列表 [{"name": "账号1", "token": "xxx"}, ...]
    """
    accounts = []

    # 按逗号分割多个账号
    tokens = [t.strip() for t in env_value.split(',') if t.strip()]

    for idx, token_str in enumerate(tokens, 1):
        # 检查是否包含账号名称
        if ':' in token_str and not token_str.startswith('eyJ'):
            # 格式: name:token
            parts = token_str.split(':', 1)
            name = parts[0].strip()
            token = parts[1].strip()
        else:
            # 格式: token (无名称)
            name = f"账号{idx}"
            token = token_str

        accounts.append({
            "name": name,
            "token": token
        })

    return accounts


def main():
    """主函数"""
    print("=" * 60)
    print("VManAPI 自动签到工具")
    print("=" * 60)

    # 从环境变量获取 Authorization token
    authorization = os.getenv("VMAN_AUTHORIZATION")

    if not authorization:
        print("❌ 错误: 未找到 VMAN_AUTHORIZATION 环境变量")
        print("\n使用方法:")
        print("  单账号: export VMAN_AUTHORIZATION='your_token_here'")
        print("  多账号: export VMAN_AUTHORIZATION='token1,token2,token3'")
        print("  多账号(带名称): export VMAN_AUTHORIZATION='账号1:token1,账号2:token2'")
        sys.exit(1)

    # 解析账号配置
    accounts = parse_accounts(authorization)
    print(f"\n📋 共发现 {len(accounts)} 个账号待签到\n")

    # 执行签到
    results = []
    for idx, account in enumerate(accounts):
        client = VManAPICheckIn(
            authorization=account["token"],
            account_name=account["name"]
        )
        result = client.check_in()
        results.append(result)

        # 多账号间随机延迟 2-5 秒,避免请求过快
        if idx < len(accounts) - 1:
            delay = random.uniform(2, 5)
            print(f"⏱️  等待 {delay:.1f} 秒后处理下一个账号...")
            time.sleep(delay)

    # 汇总结果
    print("\n" + "=" * 60)
    print("签到结果汇总")
    print("=" * 60)

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count

    for result in results:
        status = "✅ 成功" if result["success"] else "❌ 失败"
        print(f"{status} - {result['account']}: {result['message']}")

    print(f"\n总计: {len(results)} 个账号, 成功 {success_count} 个, 失败 {fail_count} 个")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 根据结果退出
    if fail_count == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
