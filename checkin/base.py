from abc import ABC, abstractmethod


class BaseCheckin(ABC):
    """签到服务基类"""

    service_name: str = ""

    @abstractmethod
    async def run(self, account: dict) -> str:
        """
        执行单个账号的签到。
        
        Args:
            account: {"account": "名称", "cookie": "cookie值"}
        
        Returns:
            签到结果消息
        """
        ...

    async def run_all(self, accounts: list[dict]) -> list[str]:
        """遍历所有账号执行签到，返回结果列表"""
        results = []
        for acc in accounts:
            label = acc.get("account", "unknown")
            try:
                msg = await self.run(acc)
                result = f"  ✅ [{label}] {msg}"
            except Exception as e:
                result = f"  ❌ [{label}] 签到失败: {e}"
            print(result)
            results.append(result)
        return results
