from kiwipiepy import Kiwi



class Scorer:

    def __call__(self,  candidates: list[list[str]], log: dict, kiwi: Kiwi) -> list[float]:
        raise NotImplementedError
