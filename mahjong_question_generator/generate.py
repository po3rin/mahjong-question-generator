import pandas as pd
from mahjong.hand_calculating.hand import HandCalculator

from mahjong_question_generator import generate_hands, convert_calculator_format, convert_cmajiang_format, calculate


def generate_question(n: int = 10):
    calculator = HandCalculator()

    hands = convert_calculator_format(generate_hands(n))
    results = []
    for hand in hands:
        result = calculate(calculator, hand)
        result['hand'] = convert_cmajiang_format(result['hand'], result['win_tile'], exclude_win_tile=True)
        results.append(result)

    df = pd.DataFrame(results)
    return df