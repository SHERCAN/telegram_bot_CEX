from typing import Optional
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: str = Field(..., alias='_id')
    cex: Optional[str] = ''
    API_key: Optional[str] = ''
    API_secret: Optional[str] = ''
    initBalance: float = 0.0
    enabled: Optional[bool] = False
    address: Optional[str] = ''
    privateKey: Optional[str] = ''
