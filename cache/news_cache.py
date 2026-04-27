# 新闻相关的缓存方法：新闻分类的读取和写入
from typing import List, Dict, Any

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"

# 获取新闻分类缓存
async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)

# 写入新闻分类缓存
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)