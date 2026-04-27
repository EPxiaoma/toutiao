from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user
from starlette import status

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryNewsItemResponse, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])

# 添加浏览历史
@router.post("/add")
async def add_history(data: HistoryAddRequest,
                      user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    result = await history.add_history(db, user.id, data.news_id)
    return success_response(message="添加浏览历史成功", data=result)

# 获取浏览历史列表
@router.get("/list")
async def get_history_list(page: int = Query(1, ge=1),
                           page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    rows, total = await history.get_history_list(db, user.id, page, page_size)

    has_more = total > page * page_size

    history_list = [HistoryNewsItemResponse.model_validate({
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
    }) for news, view_time, history_id in rows]

    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)

    return success_response(message="获取浏览历史列表成功", data=data)

# 删除单条浏览历史
@router.delete("/delete/{history_id}")
async def delete_history(history_id: int,
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    result = await history.delete_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")
    return success_response(message="删除浏览记录成功")