def _convert_calculator_format(hand: list) -> list:
    for h in hand:
        man = None
        pin = None
        sou = None
        honors = None

        if h['kind'] == 'm':
            man = h['tiles']
        elif h['kind'] == 'p':
            pin = h['tiles']
        elif h['kind'] == 's':
            sou = h['tiles']
        else:
            honors = h['tiles']

        h['man'] = man
        h['pin'] = pin
        h['sou'] = sou
        h['honors'] = honors

    return hand


def convert_calculator_format(hands: list) -> list:
    return [_convert_calculator_format(h) for h in hands]


def convert_cmajiang_format(hand: list, win_tile: str | None = None, exclude_win_tile: bool = False) -> str:
    result = ''
    close_man = ''
    close_pin = ''
    close_sou = ''
    close_honors = ''
    melds = []
    for h in hand:
        if not h['open'] and h['type'] != 'kan':
            if h['kind'] == 'm':
                close_man += h['man']
            elif h['kind'] == 'p':
                close_pin += h['pin']
            elif h['kind'] == 's':
                close_sou += h['sou']
            else:
                close_honors += h['honors']
        elif not h['open'] and h['type'] == 'kan':
            melds.append(f'{h["kind"]}{h["tiles"]}')
        elif h['open']:
            if h['type'] == 'chi':
                melds.append(f'{h["kind"]}{h["tiles"]}-')
            elif h['type'] == 'pon':
                melds.append(f'{h["kind"]}{h["tiles"]}=')
            elif h['type'] == 'kan':
                melds.append(f'{h["kind"]}{h["tiles"]}=')
    
    if close_man != '':
        result += f'm{"".join(sorted(close_man))}'
    if close_pin != '':
        result += f'p{"".join(sorted(close_pin))}'
    if close_sou != '':
        result += f's{"".join(sorted(close_sou))}'
    if close_honors != '':
        result += f'z{"".join(sorted(close_honors))}'

    for m in melds:
        result += ','
        result += m

    if exclude_win_tile:
        target_kind = ''
        for i, s in enumerate(result):
            if s in ['m', 'p', 's', 'z']:
                target_kind = s
                continue
            if s in win_tile and target_kind in win_tile:
                result = result[:i] + result[i + 1:]
                break

    return result
