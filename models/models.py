from typing import Optional
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: str = Field(..., alias='_id')
    cex: str = ''
    API_key: str = ''
    API_secret: str = ''
    initBalance: float = 0.0
    enabled: Optional[bool] = False
    address: str = ''
    privateKey: str = ''
