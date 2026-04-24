import pytest

from business_logic import (
    calculate_character_probability_with_carryover,
    calculate_gacha_probability,
    calculate_weapon_gacha_probability,
)


def test_character_carryover_integration_flow():
    """集成测试：验证跨期保底继承与基础角色池概率计算一致。"""
    previous_session_pulls = 45
    for current_session_pull in range(1, 46):
        carryover_prob = calculate_character_probability_with_carryover(
            previous_session_pulls,
            current_session_pull,
        )
        direct_prob = calculate_gacha_probability(
            previous_session_pulls + current_session_pull
        )
        assert carryover_prob == direct_prob


def test_character_and_weapon_system_independent():
    """集成测试：角色池与武器池计算应互不影响。"""
    character_prob = calculate_character_probability_with_carryover(73, 1)
    weapon_prob = calculate_weapon_gacha_probability(63)

    assert character_prob == pytest.approx(0.066)
    assert weapon_prob == pytest.approx(0.077)
