from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    _id: str = ''
    cex: str = ''
    API_key: str = ''
    API_secret: str = ''
    initBalance: float = 0.0
    enabled: bool = False
    address: str = ''
    private_key: str = ''
