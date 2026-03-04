# 签到服务注册表
CHECKIN_REGISTRY: dict[str, type] = {}


def register(cls):
    """装饰器：将签到服务类注册到 CHECKIN_REGISTRY"""
    CHECKIN_REGISTRY[cls.service_name] = cls
    return cls
