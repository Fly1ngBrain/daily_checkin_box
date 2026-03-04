import asyncio
import argparse

from config import get_accounts
from checkin import CHECKIN_REGISTRY

# 导入所有签到服务模块以触发 @register 注册
import checkin.anyrouter  # noqa: F401
import checkin.facai  # noqa: F401


async def main(services: list[str] | None = None):
    print("=" * 40)
    print("🚀 开始执行签到任务")
    print("=" * 40)

    all_results: dict[str, list[str]] = {}

    for name, cls in CHECKIN_REGISTRY.items():
        if services and name not in services:
            continue

        accounts = get_accounts(name, extra_fields=getattr(cls, "extra_fields", None))
        if not accounts:
            print(f"\n⏭️ [{name}] 未配置账号，跳过")
            continue

        print(f"\n📌 [{name}] 共 {len(accounts)} 个账号")
        instance = cls()
        results = await instance.run_all(accounts)
        all_results[name] = results

    # 汇总
    print("\n" + "=" * 40)
    print("📊 签到结果汇总")
    print("=" * 40)
    for name, results in all_results.items():
        success = sum(1 for r in results if "✅" in r)
        total = len(results)
        print(f"  [{name}] {success}/{total} 成功")

    if not all_results:
        print("  ⚠️ 没有执行任何签到任务")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="聚合签到工具")
    parser.add_argument(
        "--service", "-s",
        nargs="*",
        help="指定要执行的服务名称（空格分隔），不指定则执行全部",
    )
    args = parser.parse_args()
    asyncio.run(main(services=args.service))
