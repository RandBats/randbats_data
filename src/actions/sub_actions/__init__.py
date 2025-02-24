map_action_to_subactions = {"drag": "-drag"}


def update_actions_to_subactions(active_turn_actions: list[str]) -> list[str]:
    for turn_idx, turn in enumerate(active_turn_actions):
        action = turn.split("|")[0]
        subaction = map_action_to_subactions.get(action)
        if subaction is not None:
            active_turn_actions[turn_idx] = turn.replace(action, subaction)
    return active_turn_actions
