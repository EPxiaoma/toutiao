from sqlalchemy import select, func, update
from sqlalchemy.engine import result
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


# 获取新闻分类
async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取新闻列表
async def get_new_list(db: AsyncSession, category_id: int, skip: int=0, limit: int = 10):
    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

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