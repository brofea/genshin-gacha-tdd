def _validate_positive_integer(value, name):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _normalize_pull_index(pull_num, hard_pity):
    return ((pull_num - 1) % hard_pity) + 1


def _calculate_probability_by_rules(
    pull_num,
    hard_pity,
    soft_pity_start,
    base_probability,
    soft_pity_step,
):
    _validate_positive_integer(pull_num, "pull_num")
    normalized_pull = _normalize_pull_index(pull_num, hard_pity)

    if normalized_pull < soft_pity_start:
        return base_probability
    if normalized_pull < hard_pity:
        return (
            base_probability + (normalized_pull - soft_pity_start + 1) * soft_pity_step
        )
    return 1.0


def calculate_gacha_probability(pull_num):
    """计算角色池指定抽数下的五星概率。"""
    return _calculate_probability_by_rules(
        pull_num=pull_num,
        hard_pity=90,
        soft_pity_start=74,
        base_probability=0.006,
        soft_pity_step=0.06,
    )


def calculate_weapon_gacha_probability(pull_num):
    """计算武器池指定抽数下的五星概率。"""
    return _calculate_probability_by_rules(
        pull_num=pull_num,
        hard_pity=80,
        soft_pity_start=63,
        base_probability=0.007,
        soft_pity_step=0.07,
    )


def calculate_character_probability_with_carryover(
    previous_pulls, current_session_pull
):
    """计算角色池跨期保底继承后的当前抽概率。"""
    if not isinstance(previous_pulls, int) or previous_pulls < 0:
        raise ValueError("previous_pulls must be a non-negative integer")
    _validate_positive_integer(current_session_pull, "current_session_pull")

    total_pulls = previous_pulls + current_session_pull
    return calculate_gacha_probability(total_pulls)
