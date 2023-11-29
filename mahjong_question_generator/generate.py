import pandas as pd
from mahjong.hand_calculating.hand import HandCalculator

from mahjong_question_generator.hand import DEFAULT_TILE_PATTERN_WEIGHTS
from mahjong_question_generator import generate_hands, convert_calculator_format, convert_cmajiang_format, hand_to_question


def generate_question(n: int = 10, tile_pattern_weights: list[int] = DEFAULT_TILE_PATTERN_WEIGHTS):
    calculator = HandCalculator()

    hands = convert_calculator_format(generate_hands(n=n, tile_pattern_weights=tile_pattern_weights))
    results = []
    for hand in hands:
        result = hand_to_question(calculator, hand)
        result['hand'] = convert_cmajiang_format(result['hand'], result['win_tile'], exclude_win_tile=True)
        results.append(result)

    df = pd.DataFrame(results)
    return df
