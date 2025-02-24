from pydantic import BaseModel
from typing import Optional

from src.data_model.player import Player


class BattleLog(BaseModel):
    id: str
    players: dict[str, Player]

    start_time_unix: Optional[int] = None
    start_time_human: Optional[str] = None
    end_time_unix: Optional[int] = None
    end_time_human: Optional[str] = None

    # raw_battle data
    header: str
    turns: list[str]
    results: str
