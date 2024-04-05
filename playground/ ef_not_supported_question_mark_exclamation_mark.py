
from politely import Styler

sent = "삶은 어떠세요?"

styler = Styler(scorer="sbg", strict=True)

print(styler(sent, 0))
