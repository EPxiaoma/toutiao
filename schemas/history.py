from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict

from schemas.base import NewsItemBase


# 添加浏览历史请求参数模型类
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

# 浏览历史列表中的新闻项响应模型类
class HistoryNewsItemResponse(NewsItemBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True)

# 浏览历史列表响应模型类
class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )