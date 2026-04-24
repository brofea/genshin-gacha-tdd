import time

from business_logic import (
    calculate_character_probability_with_carryover,
    calculate_gacha_probability,
    calculate_weapon_gacha_probability,
)


def test_probability_calculation_performance():
    """性能测试：批量计算应在合理时间内完成。"""
    start = time.perf_counter()

    for idx in range(1, 100001):
        calculate_gacha_probability(idx)
        calculate_weapon_gacha_probability(idx)
        calculate_character_probability_with_carryover(idx % 90, 1)

    elapsed = time.perf_counter() - start
    assert elapsed < 2.5, f"性能测试超时: {elapsed:.4f}s"
