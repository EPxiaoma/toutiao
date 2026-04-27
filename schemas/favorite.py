from pydantic import BaseModel, Field

# 收藏状态响应模型类
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

# 添加收藏的请求体参数
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")