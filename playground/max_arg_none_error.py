from politely import Styler


styler = Styler(strict=True)


sents = [
    "당신이 정말 놀라운 존재라는 것을 알아차리는 데 깃발이 필요하지 않아요.",
    "저는 그냥 당신 자체를 사랑해요."
]


for sent in sents:
    print(styler(sent, 1))



