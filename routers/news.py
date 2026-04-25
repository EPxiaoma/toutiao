
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import null
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news

# 创建 APIRouter 示例
# prefix 路由前缀（API 路由规范文档）
# tags 分组 标签
router = APIRouter(prefix="/api/news", tags=["news"])

# 获取新闻分类
@router.get("/categories")
async def get_categories(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
    # 获取数据库里面的新闻分类数据 -> 先定义模型类 -> 封装查询数据的方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

# 获取新闻列表
@router.get("/list")
async def get_new_list(
        category_id: int=Query(..., alias="categoryId"),
        page: int=1,
        page_size: int=Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_new_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    # （跳过的 + 当前列表里面的数量） < 总量
    has_more =offset + len(news_list) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }

# 获取新闻详情
@router.get("/detail")
async def get_new_detail(new_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    new_detail = await news.get_new_detail(db, new_id)
    if new_detail is None:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, new_detail.id)
    if views_res is None:
        raise HTTPException(status_code=500, detail="更新新闻浏览量失败")

    related_news = await news.get_related_news(db, new_detail.id, new_detail.category_id)

    return {
      "code": 200,
      "message": "success",
      "data": {
        "id": new_detail.id,
        "title": new_detail.title,
        "content": new_detail.content,
        "image": new_detail.image,
        "author": new_detail.author,
        "publishTime": new_detail.publish_time,
        "categoryId": new_detail.category_id,
        "views": new_detail.views,
        "relatedNews": related_news
      }
    }