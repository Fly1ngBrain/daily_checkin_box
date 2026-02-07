import os
import requests

def auto_sign_in():
    # 1. 从环境变量获取 Cookie
    cookie_str = os.getenv('ANYROUTER_COOKIE')
    
    if not cookie_str:
        print("❌ 错误：未找到环境变量 ANYROUTER_COOKIE，请先设置后再运行。")
        return

    # 2. 目标 URL
    url = "https://anyrouter.top/api/user/sign_in"

    # 3. 设置请求头
    # 通常 API 请求除了 Cookie，建议带上 User-Agent 以模拟真实浏览器
    headers = {
        "Cookie": cookie_str,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://anyrouter.top/"
    }

    print("🚀 正在发起签到请求...")

    try:
        # 4. 发送 POST 请求 (大多数签到接口为 POST，如果是 GET 请修改为 requests.get)
        response = requests.post(url, headers=headers, timeout=10)
        
        # 5. 结果处理
        if response.status_code == 200:
            print("✅ 请求成功！")
            print(f"响应内容: {response.text}")
        else:
            print(f"⚠️ 请求可能失败，状态码: {response.status_code}")
            print(f"响应信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 发生网络异常: {e}")

if __name__ == "__main__":
    auto_sign_in()