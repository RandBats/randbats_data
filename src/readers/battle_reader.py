from typing import Optional

from data_model.battle_state import BattleState
from src.utils.raw_data_loader import RawDataLoader
from readers.header_reader import HeaderReader
from readers.results_reader import ResultsReader
from readers.turns_reader import TurnsReader


class BattleReader:
    def __init__(self, file_idx: Optional[int] = 0, random: bool = False):
        data_loader = RawDataLoader()
        self.battle_log = data_loader.load_battle(file_idx=file_idx, random=random)
        self.battle_state = BattleState()

    def read_header(self):
        header_reader = HeaderReader(header=self.battle_log.header)
        parsed_header = header_reader.parse_header()
        header_reader.update_battle_log(
            parsed_header=parsed_header, battle_log=self.battle_log
        )
        del self.battle_log.header

    def read_results(self):
        results_reader = ResultsReader(results=self.battle_log.results)
        parsed_results = results_reader.parse_results()
        results_reader.update_battle_log(
            parsed_results=parsed_results, battle_log=self.battle_log
        )
        del self.battle_log.results

    def read_turns(self):
        turns_reader = TurnsReader(
            turns_text=self.battle_log.turns, battle_state=self.battle_state
        )
        turns_reader.parse_turns()
        # turns_reader.update_battle_log(
        #     parsed_turns=parsed_turns, battle_log=self.battle_log
        # )
        # del self.battle_log.turns


if __name__ == "__main__":
    battle_reader = BattleReader()
    battle_reader.read_header()
    battle_reader.read_results()
    battle_reader.read_turns()
    print(battle_reader.battle_log)
