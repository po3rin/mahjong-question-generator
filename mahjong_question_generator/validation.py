from mahjong_question_generator.exceptions import InvalidTehaiError

PAI_KIND = [
    '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
    '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
    '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
    '1z', '2z', '3z', '4z', '5z', '6z', '7z',
]

YAMA = PAI_KIND + PAI_KIND + PAI_KIND + PAI_KIND


def hand_validation(hand: list):
    """
    存在しない牌を使っていないかを確認する
    """

    y = YAMA.copy()
    for h in hand:
        for n in h['tiles']:
            pai = n+h['kind']
            if not pai in y:
                raise InvalidTehaiError(f'山にない牌を使っています: {pai}')
            y.remove(pai)