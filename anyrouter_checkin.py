import os
import asyncio
from playwright.async_api import async_playwright

# import dotenv
# dotenv.load_dotenv()  # 加载 .env 文件中的环境变量

async def auto_sign_in():
    # 1. 从环境变量获取 Cookie
    raw_cookie = os.getenv('ANYROUTER_COOKIE')
    if not raw_cookie:
        print("❌ 错误：未找到环境变量 ANYROUTER_COOKIE")
        return

    # 提取 session 值（因为 Playwright 需要格式化的 Cookie 对象）
    # 假设你的格式是 session=xxxx; acw_tc=xxxx
    cookie_items = {}
    for item in raw_cookie.strip().split(';'):
        if '=' in item:
            k, v = item.strip().split('=', 1)
            cookie_items[k] = v

    async with async_playwright() as p:
        # 启动浏览器（无头模式）
        browser = await p.chromium.launch(headless=True)
        # 模拟真实浏览器上下文
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )

        # 2. 注入 Cookie
        # 阿里云主要校验 session 和 acw_tc，注入后浏览器会自动处理后续的 acw_sc__v2
        cookies = [
            {
                "name": key,
                "value": value,
                "domain": "anyrouter.top",
                "path": "/"
            } for key, value in cookie_items.items()
        ]
        await context.add_cookies(cookies)

        page = await context.new_page()

        print("🚀 正在打开页面并处理 WAF 验证...")
        
        try:
            # 3. 访问首页，让浏览器自动执行 WAF 的 JS 代码
            # wait_until="networkidle" 会等待 JS 执行完毕，计算出 acw_sc__v2
            await page.goto("https://anyrouter.top/user/index", wait_until="networkidle")
            
            print("🔗 正在发起签到 API 请求...")

            # 4. 在当前已通过验证的页面环境下，执行签到请求
            # 使用 page.evaluate 可以在浏览器上下文直接发请求，自带所有通过验证的 Cookie
            script = """
            fetch("/api/user/sign_in", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            }).then(res => res.text())
            """
            result = await page.evaluate(script)

            print("✅ 签到响应结果:")
            print(result)

        except Exception as e:
            print(f"❌ 运行中出错: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(auto_sign_in())