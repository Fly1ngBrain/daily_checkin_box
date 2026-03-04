from playwright.async_api import async_playwright

from checkin import register
from checkin.base import BaseCheckin


@register
class AnyRouterCheckin(BaseCheckin):
    """AnyRouter (anyrouter.top) 自动签到"""

    service_name = "anyrouter"

    async def run(self, account: dict) -> str:
        raw_cookie = account["cookie"]

        # 解析 cookie 字符串
        cookie_items = {}
        for item in raw_cookie.strip().split(";"):
            if "=" in item:
                k, v = item.strip().split("=", 1)
                cookie_items[k] = v

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/121.0.0.0 Safari/537.36"
            )

            # 注入 Cookie
            cookies = [
                {
                    "name": key,
                    "value": value,
                    "domain": "anyrouter.top",
                    "path": "/",
                }
                for key, value in cookie_items.items()
            ]
            await context.add_cookies(cookies)

            page = await context.new_page()

            try:
                # 访问首页，通过 WAF 验证
                await page.goto(
                    "https://anyrouter.top/user/index",
                    wait_until="networkidle",
                )

                # 发起签到请求
                script = """
                fetch("/api/user/sign_in", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({})
                }).then(res => res.text())
                """
                result = await page.evaluate(script)
                return result
            finally:
                await browser.close()
