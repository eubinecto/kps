

from politely import Styler

styler = Styler()


sent = "고민하고 있어요?"

print(styler(sent, 0))

"""
고민하고 있어?
"""


sent = "고민하고 계시죠?"

print(styler(sent, 0))

"""
고민하고 있을까?
"""

"""
아... 청유 / 권유 / 어쩌고 등 ... 그런 휴리스틱에 대한 이해도 필요할듯 함. 
그걸 분류 로직에 추가하면 좋을듯함. 
"""