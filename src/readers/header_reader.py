from src.data_model.battle_log import BattleLog
from src.utils.get_timestamp import get_timestamp


class HeaderReader:
    def __init__(self, header: str):
        self.header: str = header

    def parse_header(self) -> dict[str, int | str | dict[str, int]]:
        timestamp_unix, timestamp_human = get_timestamp(turn=self.header)
        return {
            "timestamp_unix": timestamp_unix,
            "timestamp_human": timestamp_human,
        }

    @staticmethod
    def update_battle_log(
        parsed_header: dict[str, int | str | dict[str, int]], battle_log: BattleLog
    ) -> BattleLog:
        battle_log.start_time_unix = parsed_header["timestamp_unix"]
        battle_log.start_time_human = parsed_header["timestamp_human"]

        return battle_log
