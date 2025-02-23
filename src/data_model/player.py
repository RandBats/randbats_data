from pydantic import BaseModel
from typing import Optional


class Player(BaseModel):
    id: str
    name: str

    start_rating: Optional[int] = None
    end_rating: Optional[int] = None
    delta_rating: Optional[int] = None

    victory: bool = False