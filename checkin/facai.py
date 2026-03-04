import json

from playwright.async_api import async_playwright

from checkin import register
from checkin.base import BaseCheckin
from config import get_accounts as _get_accounts


@register
class FacaiCheckin(BaseCheckin):
    """Facai (ai.facai.cloudns.org) 自动签到 — New-API 后端"""

    service_name = "facai"
    extra_fields = ["userid"]

    async def run(self, account: dict) -> str:
        raw_cookie = account["cookie"]
        userid = account.get("userid", "")

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
                    "domain": "ai.facai.cloudns.org",
                    "path": "/",
                }
                for key, value in cookie_items.items()
            ]
            await context.add_cookies(cookies)

            page = await context.new_page()

            try:
                # 访问首页，通过 WAF 验证
                await page.goto(
                    "https://ai.facai.cloudns.org",
                    wait_until="networkidle",
                )

                # 发起签到请求
                script = f"""
                fetch("/api/user/checkin", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json",
                        "New-Api-User": "{userid}"
                    }},
                    credentials: "include",
                    body: JSON.stringify({{}})
                }}).then(res => res.text())
                """
                result = await page.evaluate(script)

                # 检查响应中的 success 字段
                try:
                    data = json.loads(result)
                    if not data.get("success", False):
                        raise RuntimeError(data.get("message", result))
                    return data.get("message", result)
                except json.JSONDecodeError:
                    return result
            finally:
                await browser.close()
