import os
from dotenv import load_dotenv

load_dotenv()


def get_accounts(service_name: str, extra_fields: list[str] | None = None) -> list[dict]:
    """
    从环境变量中解析多账号配置。
    
    约定：
      {SERVICE}_ACCOUNT="account_1#account_2"
      {SERVICE}_COOKIE="cookie_1#cookie_2"
      {SERVICE}_{FIELD}="value_1#value_2"  (extra_fields)
    
    返回 [{"account": "account_1", "cookie": "cookie_1", "field": "value_1"}, ...]
    """
    prefix = service_name.upper()
    raw_accounts = os.getenv(f"{prefix}_ACCOUNT", "")
    raw_cookies = os.getenv(f"{prefix}_COOKIE", "")

    accounts = [a.strip() for a in raw_accounts.split("#") if a.strip()] if raw_accounts else []
    cookies = [c.strip() for c in raw_cookies.split("#") if c.strip()] if raw_cookies else []

    if not cookies:
        return []

    # 如果没有配置 account 名称，自动生成 account_1, account_2, ...
    if not accounts:
        accounts = [f"account_{i + 1}" for i in range(len(cookies))]

    # 解析额外字段
    extras: dict[str, list[str]] = {}
    for field in (extra_fields or []):
        raw = os.getenv(f"{prefix}_{field.upper()}", "")
        extras[field] = [v.strip() for v in raw.split("#") if v.strip()] if raw else []

    if len(accounts) != len(cookies):
        print(f"⚠️ [{prefix}] ACCOUNT 数量({len(accounts)}) 与 COOKIE 数量({len(cookies)}) 不匹配，按最少的配对")

    pairs = []
    for i, (account, cookie) in enumerate(zip(accounts, cookies)):
        entry = {"account": account, "cookie": cookie}
        for field, values in extras.items():
            entry[field] = values[i] if i < len(values) else ""
        pairs.append(entry)

    return pairs
