import parse
from typing import Optional

from src.utils.raw_data_loader import RawDataLoader
from src.readers.header_reader import HeaderReader
from src.readers.results_reader import ResultsReader


class BattleReader:
    def __init__(self, file_idx: Optional[int] = 0, random: bool = False):
        data_loader = RawDataLoader()
        self.battle_log = data_loader.load_battle(file_idx=file_idx, random=random)

    def read_header(self):
        header_reader = HeaderReader(header=self.battle_log.header)
        parsed_header = header_reader.parse_header()
        header_reader.update_battle_log(
            parsed_header=parsed_header,
            battle_log=self.battle_log
        )
        del self.battle_log.header
    
    def read_results(self):
        results_reader = ResultsReader(results=self.battle_log.results)
        parsed_results = results_reader.parse_results()
        results_reader.update_battle_log(
            parsed_results=parsed_results,
            battle_log=self.battle_log
        )
        del self.battle_log.results




if __name__ == "__main__":
    battle_reader = BattleReader()
    battle_reader.read_header()
    battle_reader.read_results()
    print(battle_reader.battle_log)