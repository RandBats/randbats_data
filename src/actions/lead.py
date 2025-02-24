from src.actions import Action, TurnActions
from src.actions.switch import SwitchReader

from src.data_model.battle_state import BattleState
from src.data_model.pokemon import Pokemon


class Lead(Action):
    action_name: str = "lead"
    action_rank: int = 1
    action_log: str = "switch"


class LeadReader:
    def __init__(self, lead_turn_text: str):
        self.turn: list[str] = lead_turn_text.split("\n|")

        self.switch_reader = SwitchReader()

    def get_lead(self, player_id: str) -> TurnActions:
        for line in self.turn:
            if player_id in line:
                pokemon_lead_data = self.switch_reader.parse_lead_pattern(
                    player_id=player_id, line=line
                )
                pokemon = Pokemon(**pokemon_lead_data)
                lead = Lead(player_id=player_id, active_pokemon=pokemon.model_dump())
                turn_actions = TurnActions(actions=[lead])
                return turn_actions
        raise ValueError(f"Lead pokemon not found for player {player_id}")


def update_battle_state_after_lead(
    battle_state: BattleState, lead_p1: TurnActions, lead_p2: TurnActions
) -> BattleState:
    battle_state.players_state["p1"].team = [lead_p1[1].active_pokemon]
    battle_state.players_state["p2"].team = [lead_p2[1].active_pokemon]

    for player in ["p1", "p2"]:
        battle_state.players_state[player].current_pokemon = battle_state.players_state[
            player
        ].team[0]

    return battle_state
