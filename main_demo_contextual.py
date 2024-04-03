from pprint import pprint
from politely import Styler

styler = Styler(scorer="heuristic")
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
pprint(list(sorted(styler.log['guess']['out'], key=lambda x: x[1], reverse=True))[:3])

"""
##### lm을 쓰지 않는 경우 맥락 고려 X ######
내일 나랑 같이 점심 먹어.
[(['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '어🏷EF', '.🏷SF'],
  0.0125),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '대🏷EF', '.🏷SF'], 0.0),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '지🏷EF', '.🏷SF'], 0.0)]
"""

styler = Styler(scorer="sbg")  
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
pprint(list(sorted(styler.log['guess']['out'], key=lambda x: x[1], reverse=True))[:3])

"""
##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.
[(['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '자🏷EF', '.🏷SF'],
  -33.544471740722656),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '어🏷EF', '.🏷SF'],
  -33.63521194458008),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '는다🏷EF', '.🏷SF'],
"""

styler = Styler(scorer="gpt2")
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
pprint(list(sorted(styler.log['guess']['out'], key=lambda x: x[1], reverse=True))[:3])

"""
##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.
[(['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '자🏷EF', '.🏷SF'],
  -6.211542129516602),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '어🏷EF', '.🏷SF'],
  -6.496356010437012),
 (['내일🏷NNG', '나🏷NP', '랑🏷JKB', '같이🏷MAG', '점심🏷NNG', '먹🏷VV', '는다🏷EF', '.🏷SF'],
  -6.551154613494873)]
"""

"""

##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.
"""