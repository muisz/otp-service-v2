from datetime import datetime
from pydantic import BaseModel
from typing import Union


class OTP(BaseModel):
    id: Union[int, None] = None
    code: str
    session_code: str
    destination: str
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
