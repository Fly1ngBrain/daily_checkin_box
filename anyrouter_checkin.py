from curl_cffi import requests
import time
import os  # 引入系统模块

# ================= 配置区域 =================
# 指定环境变量的名称
ENV_VAR_NAME = "ANYROUTER_COOKIE"
TARGET_URL = "https://anyrouter.top/"
# ===========================================

def sign_in():
    # 1. 从环境变量获取 Cookie
    cookie_str = os.environ.get(ENV_VAR_NAME)

    # 2. 检查是否成功获取
    if not cookie_str:
        print(f"❌ [{time.strftime('%Y-%m-%d %H:%M:%S')}] 错误: 未找到环境变量 '{ENV_VAR_NAME}'")
        print(f"   -> 请在运行前执行: export {ENV_VAR_NAME}='你的Cookie字符串'")
        return

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在启动 curl_cffi (模拟 Chrome 110)...")
    
    headers = {
        # 注意：curl_cffi 会自动处理大部分 User-Agent，但我们显式指定一下更稳
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Cookie": cookie_str,
        "Referer": TARGET_URL
    }

    try:
        # impersonate="chrome110": 关键参数，模拟真实浏览器 TLS 指纹
        # verify=False: 忽略证书过期 (针对你的 2026 年环境)
        response = requests.get(
            TARGET_URL,
            headers=headers,
            impersonate="chrome110",
            verify=False,
            timeout=15
        )

        # 打印结果
        if response.status_code == 200:
            print(f"✅ [{time.strftime('%Y-%m-%d %H:%M:%S')}] 访问成功 (HTTP 200)")
            # 打印网页标题或一部分内容来验证
            try:
                title_part = response.text[response.text.find('<title>')+7 : response.text.find('</title>')]
                print(f"   -> 网页标题: {title_part}")
            except:
                pass
            print(f"   -> 数据长度: {len(response.text)}")
        elif response.status_code == 403:
            print(f"❌ [{time.strftime('%Y-%m-%d %H:%M:%S')}] 失败 (HTTP 403)")
            print("================ 拦截详情 ================")
            # 打印网页文本，只显示前 500 个字符避免刷屏
            print(response.text[:500]) 
            print("==========================================")
        else:
            print(f"⚠️ [{time.strftime('%Y-%m-%d %H:%M:%S')}] 状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    sign_in()
