#---------------------------------------------------------------------------
"""
코드 흐름:
check_point(player)을 실행하면 메이드 검사> 메이드 되면 족보검사 아니면 0 리턴
족보검사 리턴 형식은 카드 패 (메이드 족보, 섯다 족보)형태의 리스트

광 표시에 따라 족보중 38광땡 리스트의 수정이 필요합니다.
"""
#---------------------------------------------------------------------------
from itertools import combinations
from collections import Counter
from Card import *
# import random

flower_deck = [Card(i, None) for i in range(1, 11) for _ in range(4)]
#---------------------------------------------------------------------------

made_digree = {
    "콩콩팔": [1, 1, 8],
    "삐리칠": [1, 2, 7],
    "물삼육": [1, 3, 6],
    "삥새오": [1, 4, 5],
    "삥구장": [1, 9, 10],
    "니니육": [2, 2, 6],
    "이삼오": [2, 3, 5],
    "이판장": [2, 8, 10],
    "삼삼새": [3, 3, 4],
    "삼칠장": [3, 7, 10],
    "삼빡구": [3, 8, 9],
    "살살이": [4, 4, 2],
    "사륙장": [4, 6, 10],
    "사칠구": [4, 7, 9],
    "꼬꼬장": [5, 5, 10],
    "오륙구": [5, 6, 9],
    "오천평": [5, 7, 8],
    "쭉쭉팔": [6, 6, 8],
    "칠칠육": [7, 7, 6],
    "팍팍싸": [8, 8, 4],
    "구구리": [9, 9, 2]
}
digree = {
    0: "망통",
    1: "한끗",
    2: "두끗",
    3: "세끗",
    4: "네끗",
    5: "다섯끗",
    6: "여섯끗",
    7: "일곱끗",
    8: "여덟끗",
    9: "아홉끗",
    "일땡": 1,
    "이땡": 2,
    "삼땡": 3,
    "사땡": 4,
    "오땡": 5,
    "육땡": 6,
    "칠땡": 7,
    "팔땡": 8,
    "구땡": 9,
    "장땡": 10,
    "13광땡": [1.1, 3.1],
    "18광땡": [1.1, 8.1],
    "38광땡": [3.1, 8.1]
}


#메이드 된 카드들 제외하기 위한 리스트
made_list = []
#결과 리스트
result = []
#메이드 검사 후 점수 계산


def check_point(deck):
    global made_list
    global result

    made_list = []
    result = []

    new_deck = [c.score for c in deck]
    if is_made(new_deck):
        c1 = Counter(new_deck)
        c2 = Counter(made_list)
        new_deck = list((c1-c2).elements())
        lefts = []
        for c in deck:
            if c.score not in new_deck:
                lefts.append(c)

        if lefts[0].light and lefts[1].light:
            lefts.sort(key=lambda x: x.score)
            lval = str(lefts[0]) + str(lefts[1]) + '광땡'
            result.append(lval)

        else:
            new_lefts = [c.score for c in lefts]
            show_digree(new_lefts)
            # if lefts[0].score == lefts[1].score:
            #     lval = str(lefts[0].score) + '땡'
            # elif (lefts[0].score + lefts[1].score) % 10 == 0:
            #     lval = '망통'
            # else:
            #     lval = str((lefts[0].score+lefts[1].score) % 10) + '끗'

        for key, value in made_digree.items():
            if value[0] in made_list and value[1] in made_list and value[2] in made_list:
                result.append(key)

        print('result: '+str(result))
        return result
    else:
        print("노메이드")
        return []


#메이드 검사
def is_made(deck):
    global made_list
    for cards in combinations(deck, 3):
        if sum(cards) == 10 or sum(cards) == 20:
            made_list = list(cards)
            # print(made_list)
            return True
    else:
        return False


#족보검사
def show_digree(deck):
    global result
    for i in range(1, 11):
        if deck.count(i) == 2:
            for key, value in digree.items():
                if value == i:
                    result.append(key)
    if len(result) == 1:
        for i in range(0, 10):
            if sum(deck) % 10 == i:
                result.append(digree[i])


# ---------------------------------------------------------------------------
#디버그를 위한 임시코드

# player_deck=random.sample(flower_deck, 5)
# for c in player_deck:
#     print(c.score, c.light, end='  ')
# print()
# check_point(player_deck)
#---------------------------------------------------------------------------
