from pydantic import BaseModel, Field

# 收藏状态响应模型类
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")
