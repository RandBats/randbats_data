from datetime import datetime


def get_timestamp(turn: str) -> tuple[int, str]:
    for line in turn.split("\n"):
        if line.startswith("|t:|"):
            timestamp = int(line.split("|t:|")[1])
            return timestamp, datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    raise ValueError("Timestamp not found")
