from pydantic import Field, BaseModel

# 添加浏览历史请求参数模型类
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")