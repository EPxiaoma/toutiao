from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, func, update
from sqlalchemy.engine import result
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cache_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category, News
from schemas.base import NewsItemBase


# 获取新闻分类
async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    # 先尝试从缓存中获取数据
    cache_categories = await get_cache_categories()
    if cache_categories:
        return cache_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all() # ORM 类型数据

    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    # 返回数据
    return categories

# 获取新闻列表
async def get_new_list(db: AsyncSession, category_id: int, skip: int=0, limit: int = 10):
    # 先尝试从缓存获取列表
    # skip = (页码 - 1) * 每页数量 -> 页码 = 跳过的数量 / 每页数量 + 1
    page = skip // limit + 1
    cached_list = await get_cache_news_list(category_id, page, limit)   # 缓存数据 json
    if cached_list:
        return [News(**item) for item in cached_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把 ORM 数据转换成 字典才能写入缓存
        # ORM 转换成 Pydantic，再转换成 字典
        # by_alias=False 不使用别名，保持 Python 风格，因为 Redis 数据给后端用的
        news_list = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_list)

    return news_list

# 查询指定分类下的新闻数量
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() # 只能有一个结果，否则就报错

# 获取新闻详情
async def get_new_detail(db: AsyncSession, new_id: int):
    stmt = select(News).where(News.id == new_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 增加新闻浏览量
async def increase_news_views(db: AsyncSession, new_id: int):
    stmt = update(News).where(News.id == new_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的命中了数据 -> 命中了返回 True
    return result.rowcount > 0

# 获取新闻的相关新闻
async def get_related_news(db: AsyncSession, new_id: int, category_id: int ,limit: int = 5):
    # order_by 排序 -> 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != new_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    result_news = result.scalars().all()
    # 列表推导式，推导出新闻的核心数据，然后在 return
    return [{
        "id": new_detail.id,
        "title": new_detail.title,
        "content": new_detail.content,
        "image": new_detail.image,
        "author": new_detail.author,
        "publishTime": new_detail.publish_time,
        "categoryId": new_detail.category_id,
        "views": new_detail.views,
    } for new_detail in result_news]