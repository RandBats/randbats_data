import os
import parse
from random import randint

from typing import Optional
from AdvancedHTMLParser.Parser import AdvancedHTMLParser
from AdvancedHTMLParser.Tags import AdvancedTag

from src.conf.paths import Paths
from src.data_model.player import Player
from src.data_model.battle_log import BattleLog


class RawDataLoader:
    def __init__(self):
        self.paths = Paths()

        self.files = self._get_raw_data_files()

    def _get_raw_data_files(self) -> list[str]:
        return [f for f in os.listdir(self.paths.raw_data_folder) if f.endswith(".html")]

    def _get_battle_filename(self, file_idx: Optional[int] = 0, random: bool = False):
        if not random:
            return self.files[file_idx]
        else:
            file_idx = randint(0, len(self.files) - 1)
            return self.files[file_idx]

    def _load_battle_parser(self, file_idx: Optional[int] = 0, random: bool = False) \
            -> AdvancedHTMLParser:
        battle_name = self._get_battle_filename(file_idx=file_idx, random=random)
        with open(self.paths.raw_data_folder / battle_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        parser = AdvancedHTMLParser()
        parser.parseStr(html_content)

        return parser

    def _get_battle_id(self, parser: AdvancedHTMLParser) -> str:
        input_elements = parser.getElementsByTagName("input")
        for element in input_elements:
            if element.hasAttribute("name") and element.getAttribute("name") == "replayid":
                return element.getAttribute("value")

        raise ValueError("Replay timestamp not found")

    @staticmethod
    def _create_players(player_names_text: str) -> dict[str, Player]:
        player_name_1, player_name_2 = player_names_text.split("\n")
        player1 = Player(
            id="p1",
            name=player_name_1[4:]
        )
        player2 = Player(
            id="p2",
            name=player_name_2[4:]
        )
        return {"p1": player1, "p2": player2}

    def _get_players_and_raw_battle_data(self, script_element: AdvancedTag) \
            -> tuple[dict[str, Player], dict[str, str | list[str]]]:
        player_names_text, battle_text = script_element.innerHTML.split("\n\n")

        # 1. Get player names from the first chunk of text
        players = self._create_players(player_names_text)

        # 2. Divide the remaining chunks in three groups:
        #   2.1 Header
        #   2.2 Turns
        #   2.3 Results
        battle_chunks = battle_text.split("\n|\n")
        header: str = battle_chunks[0]
        turns: list[str] = battle_chunks[1:-1]
        results: str = battle_chunks[-1]
        battle = {
            "header": header,
            "turns": turns,
            "results": results
        }
        return players, battle

    def load_battle(self, file_idx: Optional[int] = 0, random: bool = False) -> BattleLog:
        parser = self._load_battle_parser(file_idx=file_idx, random=random)

        id: str = self._get_battle_id(parser)

        script_element: AdvancedTag = parser.getElementsByTagName("script")[0]
        players, raw_battle = self._get_players_and_raw_battle_data(script_element)

        return BattleLog(**{
            "id": id,
            "players": players,
            "header": raw_battle["header"],
            "turns": raw_battle["turns"],
            "results": raw_battle["results"],
        })




if __name__ == "__main__":
    data_loader = RawDataLoader()
    battle_log = data_loader.load_battle()
    print(battle_log)