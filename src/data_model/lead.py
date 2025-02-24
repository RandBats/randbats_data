from pydantic import BaseModel
from src.data_model.pokemon import Pokemon


class Lead(BaseModel):
    player_id: str
    pokemon: Pokemon
