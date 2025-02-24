from typing import Optional

from pydantic import BaseModel

from data_model.pokemon import Pokemon


class SubAction(BaseModel):
    action_name: str
    action_rank: int

    sub_action_name: str
    sub_action_log: str
    sub_action_rank: int

    active_pokemon: Pokemon
    passive_pokemon: Optional[Pokemon] = None


class Action(BaseModel):
    action_name: str
    action_rank: int
    action_log: str

    player_id: str
    active_pokemon: Pokemon
    passive_pokemon: Optional[Pokemon] = None

    sub_actions: Optional[list[SubAction]] = None


class TurnActions(BaseModel):
    actions: list[Action]

    def __getitem__(self, action_rank: int) -> Action:
        for action in self.actions:
            if action.action_rank == action_rank:
                return action
        raise KeyError(f"Action not found with action rank: {action_rank}")


def create_action_and_subaction_turn_structure(
    active_turn_actions: list[str],
) -> dict[int, dict[str, str | list[str]]]:
    turn_structure = {}
    action_idx = 0
    for line in active_turn_actions:
        split_line = line.split("|")
        action_log = split_line[0]
        player_id = split_line[1].split(":")[0][:2]
        is_action: bool = not action_log.startswith("-")

        if is_action:
            action_idx += 1
            turn_structure[action_idx] = {
                "action_log": action_log,
                "player_id": player_id,
                "main_action": line,
                "sub_actions": [],
            }
        else:
            turn_structure[action_idx]["sub_actions"].append(line)

    return turn_structure
