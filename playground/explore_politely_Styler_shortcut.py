from politely import Styler
from pprint import pprint


def main():
    styler = Styler()
    print(styler.log)
    print(styler.log)
    print(styler("나한테 왜 그런거야?", 2))
    pprint(styler.log)


if __name__ == "__main__":
    main()
