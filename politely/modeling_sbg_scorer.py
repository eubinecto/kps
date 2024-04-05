from politely.rules import TAG
from .modeling_scorer import Scorer
from kiwipiepy import Kiwi



class SkipBigramScorer(Scorer):
    """
    This is better than heuristic scorer, but slightly less accurate than gpt2 scorer. 
    Good for most cases. 
    """

    def __call__(self, candidates: list[list[str]], log: dict, kiwi: Kiwi) -> list[float]:
        # first, join the pairs into a sentence
        sents = [
            kiwi.join(tuple(pair.split(TAG)) for pair in candidate)
            for candidate in candidates
        ]
        # then analyze the scores
        results = kiwi.analyze(sents, top_n=1)
        scores = [res[0][1] for res in  results]
        return scores

        
        
         