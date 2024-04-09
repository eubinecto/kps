# Politely

[![PyPI version](https://badge.fury.io/py/politely.svg)](https://badge.fury.io/py/politely)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://politely.streamlit.app)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Feubinecto%2Fpolitely&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
[![Downloads](https://pepy.tech/badge/politely)](https://pepy.tech/project/politely)
[![Downloads](https://pepy.tech/badge/politely/week)](https://pepy.tech/project/politely)

A hybrid politeness styler for the Korean language | 
--- | 
<img width="1010" alt="image" src="https://user-images.githubusercontent.com/56193069/168471756-084409db-5d72-48b7-820f-05e1de6b1f5a.png">  | 



## Quick Start 🚀
### 1️⃣ Install `politely`

```python3
pip3 install politely
```

### 2️⃣ Split your text into sentences
Split your text into sentences with whatever tools you prefer. Here, we use [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) for the sake of demonstration:
```python3
from kiwipiepy import Kiwi
# an excerpt from 동백꽃 (김유정)
text = """잔소리를 두루 늘어놓다가 남이 들을까봐 손으로 입을 틀어막고는 그 속에서 깔깔댄다. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 계집애가 미쳤나 하고 의심하였다.
게다가 조금 뒤에는 제 집께를 할금할금 돌아보더니 행주치마의 속으로 꼈던 바른손을 뽑아서 나의 턱밑으로 불쑥 내미는 것이다. 
언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였다. "느 집엔 이거 없지?" 하고 생색있는 큰소리를 하고는 제가 준 것을 남이 알면은 큰일날테니 여기서 얼른 먹어 버리란다.
그리고 또 하는 소리가, "너 봄감자가 맛있단다." "난 감자 안 먹는다. 너나 먹어라." 나는 고개도 돌리지 않고 일하던 손으로 그 감자를 도로 어깨 너머로 쑥 밀어 버렸다.
그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상치 않게 숨소리가 점점 거칠어진다. 이건 또 뭐야 싶어서 그때에야 비로소 돌아다보니 나는 참으로 놀랐다.
우리가 이 동네에 들어온 것은 근 삼년째 되어오지만 여태껏 가무잡잡한 점순이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었다.
게다가 눈에 독을 올리고 한참 나를 요렇게 쏘아보더니 나중에는 눈물까지 어리는 것이 아니냐.
그리고 바구니를 다시 집어들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 횡하게 달아나는 것이다."""
kiwi = Kiwi()
sents = [sent.text.strip() for sent in kiwi.split_into_sents(text)]
```

### 3️⃣ Speak `politely` with `Styler` 

Instantiate an object of `Styler`, and style your sentences in a polite or formal manner with it:

```python3
from politely import Styler
from pprint import pprint
styler = Styler()
pprint(" ".join([styler(sent, 1) for sent in sents]))  # 1 = polite
```
```text
('잔소리를 두루 늘어놓다가 남이 들을까 봐 손으로 입을 틀어막고는 그 속에서 깔깔대요. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 '
 '계집애가 미쳤나 하고 의심했어요. 게다가 조금 뒤에는 제 집께를 할 금할 금 돌아보더니 행주치마의 속으로 꼈던 바른 손을 뽑아서 제 턱 '
 '밑으로 불쑥 내미는 게에요. 언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였어요. "느 집에는 이 거 없죠? '
 '"하고 생색 있는 큰 소리를 하고는 제가 준 것을 남이 알면은 큰일 날 테니 여기서 얼른 먹어 버리래요. 그리고 또 하는 소리가,"당신 '
 '봄 감자가 맛있어요. ""난 감자 안 먹어요. 당신이나 먹어요. "저는 고개도 돌리지 않고 일하던 손으로 그 감자를 도로 어깨 너머로 쑥 '
 '밀어 버렸어요. 그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상하지 않게 숨소리가 점점 거칠어져요. 이거는 또 뭐야 '
 '싶어서 그 때에야 비로소 돌아다보니 저는 참으로 놀랐어요. 저희가 이 동네에 들어온 것은 근 삼 년째 돼 오지만 여태껏 가무잡잡한 점수는 '
 '이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었어요. 게다가 눈에 독을 올리고 한참 저를 요렇게 쏘아보더니 나중에는 눈물까지 어리는 '
 '게 아녀요. 그리고 바구니를 다시 집어 들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 횡하게 달아나는 게에요.')
 ```
 
 ```python3
pprint(" ".join([styler(sent, 2) for sent in sents]))  # 2 = formal
```
```text
('잔소리를 두루 늘어놓다가 남이 들을까 봐 손으로 입을 틀어막고는 그 속에서 깔깔댑니다. 별로 우스울 것도 없는데 날씨가 풀리더니 이 놈의 '
 '계집애가 미쳤나 하고 의심했습니다. 게다가 조금 뒤에는 제 집께를 할 금할 금 돌아보더니 행주치마의 속으로 꼈던 바른 손을 뽑아서 제 턱 '
 '밑으로 불쑥 내미는 겝니다. 언제 구웠는지 더운 김이 홱 끼치는 굵은 감자 세 개가 손에 뿌듯이 쥐였습니다. "느 집에는 이 거 '
 '없습니까? "하고 생색 있는 큰 소리를 하고는 제가 준 것을 남이 알면은 큰일 날 테니 여기서 얼른 먹어 버리랍니다. 그리고 또 하는 '
 '소리가,"당신 봄 감자가 맛있습니다. ""난 감자 안 먹습니다. 당신이나 먹십시오. "저는 고개도 돌리지 않고 일하던 손으로 그 감자를 '
 '도로 어깨 너머로 쑥 밀어 버렸습니다. 그랬더니 그래도 가는 기색이 없고, 뿐만 아니라 쌔근쌔근하고 심상하지 않게 숨소리가 점점 '
 '거칠어집니다. 이거는 또 뭐야 싶어서 그 때에야 비로소 돌아다보니 저는 참으로 놀랐습니다. 저희가 이 동네에 들어온 것은 근 삼 년째 돼 '
 '오지만 여태껏 가무잡잡한 점수는 이의 얼굴이 이렇게까지 홍당무처럼 새빨개진 법이 없었습니다. 게다가 눈에 독을 올리고 한참 저를 요렇게 '
 '쏘아보더니 나중에는 눈물까지 어리는 게 아닙디다. 그리고 바구니를 다시 집어 들더니 이를 꼭 악물고는 엎어질 듯 자빠질 듯 논둑으로 '
 '횡하게 달아나는 겝니다.')
```

### 4️⃣ `add_rules` of your own

you can add your own rules with `add_rules` method. Use `politely.SELF` to keep `MASK` as-is. Use `politely.NULL` to remove `MASK`.
```python3
from politely import SELF, NULL
styler.add_rules(
        {
            "이🏷VCP🔗(?P<MASK>다🏷EF)": (
             {SELF},
             {"예요🏷EF"},   # 에요 (X) 예요 (O)
             {"입니다🏷EF"},
            ),
            "(?P<MASK>이🏷VCP)🔗다🏷EF": (
             {SELF},
             {NULL},  # 지우기
             {NULL}   # 지우기
            )
        })
sent = "한글은 한국의 글자이다."
print(styler(sent, 1))
```
```text 
한글은 한국의 글자예요.
```
Here is another example of adding rules.`styler.logs['guess']['out']` keeps track of all the candidates with scores.
```python3
from politely import SELF
styler.add_rules(
    {
        r"(?P<MASK>(아빠|아버지|아버님)🏷NNG)": (
            {f"아빠🏷NNG"},
            {f"아버지🏷NNG", f"아버님🏷NNG"},
            {f"아버지🏷NNG", f"아버님🏷NNG"}
        ),
        r"(아빠|아버지|아버님)🏷NNG🔗(?P<MASK>\S+?🏷JKS)": (
            {SELF},  #  no change, replace with the original
            {f"께서🏷JKS"},
            {f"께서🏷JKS"}
        ),
        r"(?P<MASK>ᆫ다🏷EF)": (
            {SELF},  # no change, replace with the original
            {"시🏷EP🔗어요🏷EF"},
            {"시🏷EP🔗습니다🏷EF"},
        )
    }
)
sent = "아빠가 정실에 들어간다."
print(styler(sent, 1))
from pprint import pprint
pprint(styler.logs['guess']['out'])
```
```text
아버지께서 정실에 들어가셔요.
[(['아버지🏷NNG', '께서🏷JKS', '정실🏷NNG', '에🏷JKB', '들어가🏷VV', '시🏷EP', '어요🏷EF', '.🏷SF'],
  0.0125),
 (['아버님🏷NNG', '께서🏷JKS', '정실🏷NNG', '에🏷JKB', '들어가🏷VV', '시🏷EP', '어요🏷EF', '.🏷SF'],
  0.0125)]
```

### 5️⃣ Take contexts into account with language models

`heuristic` scorer is fast, but it is purely rule-based. It falls short at taking contexts into account:
```python
styler = Styler(scorer="heuristic")
print("##### lm을 쓰지 않는 경우 맥락 고려 X ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
```

```
##### lm을 쓰지 않는 경우 맥락 고려 X ######
내일 나랑 같이 점심 먹어.
```

`sbg` scorer (SkipBigram) is a bit slower, but does take context into account. Useful for most cases.

```python
from politely.modeling_gpt2_scorer import GPT2Scorer
styler = Styler(scorer="sbg")  # uses GPT2Scorer by default
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
```

```
##### lm을 쓰는 경우 맥락 고려 O ######
내일 나랑 같이 점심 먹자.  # 권유가 아닌 청유이므로 이게 맞음
```

`gpt2` scorer is the most accurate, but it is also the slowest. This is an experimental option as of right now. If you want to use `gpt2` as the scorer, you first need to install the optional dependencies for `gpt2` scorer:

```shell
# need to install optional dependency
pip3 install "politely[gpt2]"
```

```python
styler = Styler(scorer="gpt2")
print("##### lm을 쓰는 경우 맥락 고려 O ######")
print(styler("내일 저랑 같이 점심 먹어요.", 0))
```

```
##### lm을 쓰는 경우 맥락 고려 O ######
내일 저랑 같이 점심 먹으러 가요.  # 권유이므로 이게 맞음
```


## An interactive demo 

Try politely by visiting [the demo we are hosting](https://politely.streamlit.app) | 
--- |
![alt text](image.png) | 



## By whom? 👏
- funded by: [Faculty of Oriental Studies](https://www.orinst.ox.ac.uk) at the University of Oxford 
- led & developed by: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) (Associate Professor of Korean Language and Linguistics at the University of Oxford)
- co-developed by: Research assistant Eu-Bin KIM (Msc. in Applied Linguistics at the University of Oxford, Bsc. in AI at the University of Manchester )


