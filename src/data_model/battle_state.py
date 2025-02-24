from pydantic import BaseModel

from data_model.pokemon import Pokemon


class PlayerBattleState(BaseModel):
    player_id: str
    team: list[Pokemon] = None
    current_pokemon: Pokemon = None

    def is_pokemon_in_team(self, pokemon_name: str) -> bool:
        for pokemon in self.team:
            if pokemon.name == pokemon_name:
                return True
        return False

    def get_pokemon_from_team(self, pokemon_name: str) -> Pokemon:
        for pokemon in self.team:
            if pokemon.name == pokemon_name:
                return pokemon
        raise ValueError(f"No Pokemon found with name: {pokemon_name}")

    @property
    def number_of_revealed_pokemons(self) -> int:
        return len(self.team)

    @property
    def number_of_fainted_pokemons(self) -> int:
        return len([pokemon for pokemon in self.team if pokemon.fainted])


class BattleState:
    players_state: dict[str, PlayerBattleState] = {
        "p1": PlayerBattleState(player_id="p1"),
        "p2": PlayerBattleState(player_id="p2"),
    }
