import parse

from src.data_model.battle_log import BattleLog


class ResultsReader:
    def __init__(self, results: str):
        self.results = results

    def extract_player_ratings(self) -> dict[str, dict[str, int | str]]:
        result_pattern = r"{player_name}'s rating: {start_rating} &rarr; <strong>{end_rating}<\/strong><br \/>({delta_rating} for {battle_result})"

        ratings = {}
        for line in self.results.split("\n"):
            if line.startswith("|raw|"):
                parts = line.split("|")
                parsed_result = parse.parse(result_pattern, parts[2])
                if not parsed_result:
                    raise ValueError("Could not extract ratings from result")

                player_name = parsed_result["player_name"]
                start_rating = int(parsed_result["start_rating"])
                end_rating = int(parsed_result["end_rating"])
                delta_rating = int(parsed_result["delta_rating"])
                battle_result = parsed_result["battle_result"]
                ratings[player_name] = {
                    "start_rating": start_rating,
                    "end_rating": end_rating,
                    "delta_rating": delta_rating,
                    "battle_result": battle_result,
                }

        return ratings

    def parse_results(self) -> dict[str, dict[str, int | str]]:
        ratings = self.extract_player_ratings()
        return ratings

    @staticmethod
    def _get_player_id_from_player_name(player_name: str, battle_log: BattleLog) -> str:
        for player_id, player in battle_log.players.items():
            if player.name == player_name:
                return player_id
        raise ValueError("Could not get player_id from player_name")

    def update_battle_log(
        self, parsed_results: dict[str, dict[str, int | str]], battle_log: BattleLog
    ) -> BattleLog:
        for player_name, player_result in parsed_results.items():
            player_id = self._get_player_id_from_player_name(player_name, battle_log)

            battle_log.players[player_id].start_rating = player_result["start_rating"]
            battle_log.players[player_id].end_rating = player_result["end_rating"]
            battle_log.players[player_id].delta_rating = player_result["delta_rating"]

            if player_result["battle_result"] == "winning":
                battle_log.players[player_id].victory = True

        return battle_log
