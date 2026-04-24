import pytest
from business_logic import (
    calculate_character_probability_with_carryover,
    calculate_gacha_probability,
    calculate_weapon_gacha_probability,
)


class TestGachaProbability:
    def test_base_probability(self):
        """测试基础概率：1-73抽应为0.6%"""
        for pull in range(1, 74):
            prob = calculate_gacha_probability(pull)
            assert prob == 0.006, f"第{pull}抽概率错误"

    def test_soft_pity_start(self):
        """测试软保底开始：第74抽概率应为6.6%"""
        prob = calculate_gacha_probability(74)
        assert prob == 0.066, "第74抽概率错误"

    def test_soft_pity_increase(self):
        """测试软保底递增：第74-89抽每抽递增6%"""
        expected_prob = 0.066
        for pull in range(74, 90):
            prob = calculate_gacha_probability(pull)
            assert prob == pytest.approx(expected_prob), f"第{pull}抽概率错误"
            expected_prob += 0.06

    def test_hard_pity_guarantee(self):
        """测试硬保底：第90抽必定获取（概率100%）"""
        prob = calculate_gacha_probability(90)
        assert prob == 1.0, "第90抽概率错误"

    def test_invalid_pull_number(self):
        """测试无效的抽数：0或负数应抛出异常"""
        with pytest.raises(ValueError):
            calculate_gacha_probability(0)

        with pytest.raises(ValueError):
            calculate_gacha_probability(-1)

    def test_pull_over_90(self):
        """测试超过90抽：超过90抽应重置为新一轮保底"""
        prob = calculate_gacha_probability(91)
        assert prob == 0.006, "第91抽（新一轮第1抽）概率错误"


class TestWeaponGachaProbability:
    def test_weapon_base_probability(self):
        """测试武器池基础概率：1-62抽应为0.7%"""
        for pull in range(1, 63):
            assert calculate_weapon_gacha_probability(pull) == 0.007

    def test_weapon_soft_pity_start(self):
        """测试武器池软保底开始：第63抽应为7.7%"""
        assert calculate_weapon_gacha_probability(63) == pytest.approx(0.077)

    def test_weapon_hard_pity(self):
        """测试武器池硬保底：第80抽应为100%"""
        assert calculate_weapon_gacha_probability(80) == 1.0

    def test_weapon_cycle_reset(self):
        """测试武器池超过80抽重置"""
        assert calculate_weapon_gacha_probability(81) == 0.007


class TestCharacterPityCarryover:
    def test_character_pity_with_carryover(self):
        """测试角色池保底继承：上期73抽后，本期第1抽应进入软保底"""
        assert calculate_character_probability_with_carryover(73, 1) == 0.066

    def test_character_carryover_to_hard_pity(self):
        """测试角色池保底继承到硬保底"""
        assert calculate_character_probability_with_carryover(89, 1) == 1.0

    def test_character_carryover_invalid_input(self):
        """测试保底继承函数异常输入"""
        with pytest.raises(ValueError):
            calculate_character_probability_with_carryover(-1, 1)

        with pytest.raises(ValueError):
            calculate_character_probability_with_carryover(10, 0)
