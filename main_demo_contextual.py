from politely import Styler

styler = Styler(scorer="heuristic")
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))


styler = Styler(scorer="gpt2")  # uses GPT2Scorer by default
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))


"""
##### lm을 쓰지 않는 경우 맥락 고려 X ######
내일 나랑 같이 점심 먹어.
##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.
"""