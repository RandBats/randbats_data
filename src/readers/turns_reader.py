from src.actions import TurnActions, create_action_and_subaction_turn_structure
from src.actions.sub_actions import update_actions_to_subactions

from src.actions.lead import LeadReader, update_battle_state_after_lead
from src.actions.switch import SwitchReader, update_battle_state_after_switch

from src.data_model.battle_state import BattleState

from src.utils.get_timestamp import get_timestamp


class TurnsReader:
    def __init__(self, turns_text: list[str], battle_state: BattleState):
        self.turns: dict[int, str] = {
            turn_id: turn for turn_id, turn in enumerate(turns_text)
        }
        self.battle_state = battle_state

        self.player_ids = ["p1", "p2"]

        self.timestamps: dict[int, dict[str, int | str]] = self.get_turns_timestamps()
        self.parsed_turns: dict[str, dict[int, TurnActions]] = {"p1": {}, "p2": {}}

        self.switch_reader = SwitchReader()

    def get_turns_timestamps(self) -> dict[int, dict[str, int | str]]:
        timestamps = dict()
        for turn_idx, turn in self.turns.items():
            timestamp_unix, timestamp_human = get_timestamp(turn=turn)
            timestamps[int(turn_idx)] = {
                "timestamp_unix": timestamp_unix,
                "timestamp_human": timestamp_human,
            }
        return timestamps

    def _read_lead(self) -> None:
        turn_id = 0
        lead_reader = LeadReader(lead_turn_text=self.turns[0])

        lead_p1 = lead_reader.get_lead(player_id="p1")
        self.parsed_turns["p1"][turn_id] = lead_p1
        lead_p2 = lead_reader.get_lead(player_id="p2")
        self.parsed_turns["p2"][turn_id] = lead_p2

        self.battle_state = update_battle_state_after_lead(
            battle_state=self.battle_state, lead_p1=lead_p1, lead_p2=lead_p2
        )
        del self.turns[0]

    @staticmethod
    def _split_into_active_and_end_turn_lines(turn_text: str) -> dict[str, list[str]]:
        turn_lines = turn_text.split("\n|")[1:]
        turn_actions = {
            "active": [],
            "end": [],
        }
        target_list = "active"
        for line in turn_lines:
            if line == "":
                target_list = "end"
            turn_actions[target_list].append(line)
        return turn_actions

    def _parse_active_turn(self, active_turn_actions: list[str]):
        parsed_turn_actions = []

        active_turn_actions = update_actions_to_subactions(active_turn_actions)
        turn_structure = create_action_and_subaction_turn_structure(active_turn_actions)
        for action_rank, action_data in turn_structure.items():
            action_log = action_data["action_log"]
            player_id = action_data["player_id"]

            match action_log:
                case "switch":
                    switch_action = self.switch_reader.parse_turn_pattern(
                        line=action_data["main_action"],
                        player_id=player_id,
                        action_rank=action_rank,
                        current_pokemon=self.battle_state.players_state[
                            player_id
                        ].current_pokemon,
                    )
                    self.battle_state = update_battle_state_after_switch(
                        battle_state=self.battle_state,
                        player_id=player_id,
                        switched_in_pokemon=switch_action.active_pokemon,
                    )
                    parsed_turn_actions.append(switch_action)

    def _read_turns(self):
        for turn_id, turn_text in self.turns.items():
            turn_actions = self._split_into_active_and_end_turn_lines(turn_text)
            self._parse_active_turn(turn_actions["active"])

    def parse_turns(self):
        self._read_lead()
        self._read_turns()
