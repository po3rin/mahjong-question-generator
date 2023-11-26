import random
from mahjong_question_generator.validation import hand_validation
from mahjong_question_generator.exceptions import InvalidTehaiError

WIN_PATTERN = ['run', 'triple', 'kan', 'pon', 'chi']
WIN_PATTERN_WEIGHTS = [4,1,1,1,1]


def hand_candidates() -> dict:
    mentsu_list = random.choices(WIN_PATTERN, weights=WIN_PATTERN_WEIGHTS, k=4)

    hand = []

    # 頭以外の生成
    for _type in mentsu_list:
        result = ''
        _open = False
        if _type in ['run']:
            kind = random.choice(['m', 'p', 's'])
            p = random.randint(1, 7)
            _open = False
            result = f'{p}{p+1}{p+2}'
        elif _type in ['chi']:
            kind = random.choice(['m', 'p', 's'])
            p = random.randint(1, 7)
            _open = True
            result = f'{p}{p+1}{p+2}'
        elif _type in ['triple']:
            kind = random.choice(['m', 'p', 's', 'z'])
            if kind == 'z':
                p = random.randint(1, 7)
            else:
                p = random.randint(1, 9)
            _open = False
            result = f'{p}{p}{p}'
        elif _type in ['pon']:
            kind = random.choice(['m', 'p', 's', 'z'])
            if kind == 'z':
                p = random.randint(1, 7)
            else:
                p = random.randint(1, 9)
            _open = True
            result = f'{p}{p}{p}'
        elif _type in ['kan']:
            kind = random.choice(['m', 'p', 's', 'z'])
            if kind == 'z':
                p = random.randint(1, 7)
            else:
                p = random.randint(1, 9)
            _open = bool(random.getrandbits(1))
            result = f'{p}{p}{p}{p}'
        else:
            raise ValueError(f'not supported: {_type}')

        hand.append({'type': _type, 'kind': kind, 'tiles': result, 'open': _open})

    # 頭の生成
    kind = random.choice(['m', 'p', 's'])
    if kind == 'z':
        p = random.randint(1, 7)
    else:
        p = random.randint(1, 9)
    result = f'{p}{p}'
    hand.append({'type': 'head', 'kind': kind, 'tiles': result, 'open': False})

    return hand


def generate_hands(n: int) -> list:
    valid_list = []
    while len(valid_list) < n:
        tehai = hand_candidates()
        try: 
            hand_validation(tehai)
        except InvalidTehaiError as e:
            continue
        valid_list.append(tehai)

    return valid_list