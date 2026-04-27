from typing import Any

import redis.asyncio as redis
from pydantic import json

REDIS_HOST = "192.168.163.164"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = 123456

# 创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,            # Redis 服务器的主机地址
    port=REDIS_PORT,            # Redis 端口号
    db=REDIS_DB,                # Redis 数据库编号，0~15
    password=REDIS_PASSWORD,    # Redis 密码
    decode_responses=True       # 是否将字节数据解码为字符串
)

# 设置 和 读取（字符串 和 列表或字典）"[{}]"
# 读取：字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None

# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            # 将字典或列表转换为 JSON 字符串
            value = json.dumps(value, ensure_ascill=False) # 中文正常保存
        await redis_client.set(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False