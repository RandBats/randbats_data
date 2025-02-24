import parse
from typing import Optional

from actions import Action
from data_model.battle_state import BattleState
from data_model.pokemon import Pokemon


class Switch(Action):
    action_name: str = "switch"
    action_log: str = "switch"


class SwitchReader:
    def __init__(self):
        self.patterns: dict[str, str] = {
            "p1": "switch|{player_id}a: {name}|{name}, L{level}, {gender}|{start_turn_hp_percentage}\\/{total_hp_percentage}",
            "p2": "switch|{player_id}a: {name}|{name}, L{level}, {gender}|{start_turn_hp_number}\\/{total_hp_number}",
        }

    def _parse_switch_pattern(
        self,
        player_id: str,
        line: str,
    ) -> dict[str, str | int | None]:
        parsed_result = parse.parse(self.patterns[player_id], line)
        data = parsed_result.named
        for int_var in [
            "start_turn_hp_percentage",
            "total_hp_percentage",
            "start_turn_hp_number",
            "total_hp_number",
        ]:
            str_value: Optional[str] = data.get(int_var)
            if str_value is not None:
                data[int_var] = int(str_value)
        return data

    def parse_turn_pattern(
        self, player_id: str, line: str, action_rank: int, current_pokemon: Pokemon
    ) -> Switch:
        pokemon_switched_in_data = self._parse_switch_pattern(
            player_id=player_id,
            line=line,
        )
        switched_in_pokemon = Pokemon(**pokemon_switched_in_data)
        switch = Switch(
            player_id=player_id,
            action_rank=action_rank,
            active_pokemon=switched_in_pokemon,
            passive_pokemon=current_pokemon,
        )
        return switch

    def parse_lead_pattern(
        self, player_id: str, line: str
    ) -> dict[str, str | int | None]:
        data = self._parse_switch_pattern(
            player_id=player_id,
            line=line,
        )
        # start_hp_percentage is always 100
        data["start_turn_hp_percentage"] = 100

        for end_var in [
            "end_turn_hp_percentage",
            "end_turn_hp_number",
        ]:
            start_value = data.get(end_var.replace("end", "start"))
            if start_value is not None:
                data[end_var] = start_value
        return data


def update_battle_state_after_switch(
    battle_state: BattleState, player_id: str, switched_in_pokemon: Pokemon
) -> BattleState:
    if not battle_state.players_state[player_id].is_pokemon_in_team(
        switched_in_pokemon.name
    ):
        battle_state.players_state[player_id].team.append(switched_in_pokemon)
    battle_state.players_state[player_id].current_pokemon = switched_in_pokemon
    return battle_state
