# 新闻相关的缓存方法：新闻分类的读取和写入
from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"

# 获取新闻分类缓存
async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)

# 写入新闻分类缓存
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

# 写入缓存-新闻列表
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int = 1800):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)

# 读取缓存-新闻列表
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)