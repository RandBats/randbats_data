from datetime import datetime

from src.data_model.battle_log import BattleLog


class HeaderReader:
    def __init__(self, header: str):
        self.header = header

    def _get_battle_start_time(self) -> tuple[int, str]:
        for line in self.header.split("\n"):
            if line.startswith("|t:|"):
                timestamp = int(line.split("|t:|")[1])
                return timestamp, datetime.fromtimestamp(timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        raise ValueError("Timestamp not found in header")

    def parse_header(self) -> dict[str, int | str | dict[str, int]]:
        timestamp_unix, timestamp_human = self._get_battle_start_time()
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
