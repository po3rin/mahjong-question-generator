import random

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH


def wind_int_to_str(wind: int) -> str:
     wind_str = ''
     if wind == 27:
          wind_str = '東'
     elif wind == 28:
          wind_str = '南'
     elif wind == 29:
          wind_str = '西'
     elif wind == 30:
          wind_str = '北'
     else:
          raise ValueError('wind {} is not supported')
     return wind_str


def get_tiles(hand: list) -> list:
    man = ''
    pin = ''
    sou = ''
    honors = ''

    for h in hand:
        if h['kind'] == 'm':
            man += h['man']
        elif h['kind'] == 'p':
            pin += h['pin']
        elif h['kind'] == 's':
            sou += h['sou']
        else:
            honors += h['honors']

    for v in [man, pin, sou, honors]:
        if v == '':
            v = None

    return TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)


def get_win_tile(hand: list) -> tuple[list, str]:
    include_win_tile_candidate = []
    for h in hand:
        if h['type'] in ['run', 'triple', 'head']:
            include_win_tile_candidate.append(h)

    include_win_tile = random.choice(include_win_tile_candidate)
    win_tile = random.choice(include_win_tile['tiles'])

    man = None
    pin = None
    sou = None
    honors = None

    if include_win_tile['kind'] == 'm':
        man = win_tile
    elif include_win_tile['kind'] == 'p':
        pin = win_tile
    elif include_win_tile['kind'] == 's':
        sou = win_tile
    else:
        honors = win_tile

    return TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)[0], f'{include_win_tile["kind"]}{win_tile}'


def get_dora() -> tuple[list, str]:
    kind = random.choice(['m', 'p', 's', 'z'])
    if kind in ['m', 'p', 's']:
        n = str(random.randint(1, 9))
    if kind in ['z']:
        n = str(random.randint(1, 7))

    man = None
    pin = None
    sou = None
    honors = None

    if kind == 'm':
        man = n
    elif kind == 'p':
        pin = n
    elif kind == 's':
        sou = n
    else:
        honors = n

    return TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)[0], f'{kind}{n}'


def get_melds(hand: list) -> list:
    melds = []
    for h in hand:
        if h['type'] in ['chi', 'pon', 'kan']:
            melds.append(Meld(h['type'], TilesConverter.string_to_136_array(man=h['man'], pin=h['pin'], sou=h['sou'], honors=h['honors']), h['open']))
    return melds if melds != [] else None



def enable_richi(hand: list) -> bool:
    for h in hand:
        if h['type'] in ['pon', 'chi']:
            return False
        if h['type'] == 'kan' and h['open']:
            return False
    return True


def calculate(calculator: HandCalculator, hand: list) -> any:
    # リーチ
    is_riichi = False
    if enable_richi(hand):
        is_riichi = bool(random.getrandbits(1))

    # ツモ or ロン
    is_tsumo = bool(random.getrandbits(1))

    # 風
    player_wind = random.choice([EAST, SOUTH, WEST, NORTH])
    round_wind = random.choice([EAST, SOUTH])

    #アガリ形(man=マンズ, pin=ピンズ, sou=ソーズ, honors=字牌)
    tiles = get_tiles(hand)

    #アガリ牌
    win_tile, win_tile_str = get_win_tile(hand)

    #鳴き
    melds = get_melds(hand)

    #ドラ
    dora, dora_str = get_dora()
    dora_indicators = [dora]

    is_haitei = False
    is_houtei = False
    config = HandConfig(is_tsumo=is_tsumo, is_riichi=is_riichi, is_haitei=is_haitei, is_houtei=is_houtei, player_wind=player_wind, round_wind=round_wind, options=OptionalRules(has_open_tanyao=True, kiriage=True, kazoe_limit=HandConfig.KAZOE_SANBAIMAN))

    #計算
    hand_value = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    # 薬がなかったら強制的に役をつける
    if str(hand_value) == 'no_yaku':
        is_haitei = is_tsumo and not is_riichi
        is_houtei = not is_tsumo and not is_riichi
        config = HandConfig(is_tsumo=is_tsumo, is_riichi=is_riichi, is_haitei=is_haitei, is_houtei=is_houtei, player_wind=player_wind, round_wind=round_wind, options=OptionalRules(has_open_tanyao=True, kiriage=True, kazoe_limit=HandConfig.KAZOE_SANBAIMAN))
        hand_value = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    return {
        'round_wind': wind_int_to_str(round_wind),
        'player_wind': wind_int_to_str(player_wind),
        'hand': hand,
        'win_tile': win_tile_str,
        'dora_str': dora_str,
        'is_riichi': is_riichi,
        'is_tsumo': is_tsumo,
        'is_haitei': is_haitei,
        'is_houtei': is_houtei,
        'hand_value_han': hand_value.han,
        'hand_value_hu': hand_value.fu,
        'hand_value_cost_additional': hand_value.cost['additional'],
        'hand_value_cost_main': hand_value.cost['main'],
        'hand_value_yaku': [str(y) for y in hand_value.yaku],
    }
