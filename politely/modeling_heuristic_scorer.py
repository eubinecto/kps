from kiwipiepy import Kiwi
from politely import PREFERENCES, CASUAL, POLITE, FORMAL, SEP
from politely.modeling_scorer import Scorer


class HeuristicScorer(Scorer):

    def __call__(self, candidates: list[list[str]], log: dict, kiwi: Kiwi) -> list[list[float]]:
        """
        A naive scoring strategy that relies on the heuristic rules.
        """
        politeness = log['honorify']['in']['politeness']
        original_pairs = log['analyze']['out'].split(SEP)
        if politeness == 0:
            boost_pairs = CASUAL & set(original_pairs)
        elif politeness == 1:
            boost_pairs = POLITE & set(original_pairs)
        elif politeness == 2:
            boost_pairs = FORMAL & set(original_pairs)
        else:
            raise ValueError(f"politeness should be one of (0, 1, 2), but got {politeness}")
        scores = list()
        for pairs in candidates:
            # if it includes priority pairs, it's a good candidate (at least for this scorer)
            pairs = set(pairs)
            score = (len(PREFERENCES & pairs) / len(pairs)) * 0.1
            score += (len(boost_pairs & pairs) / len(pairs)) * 0.9
            scores.append(score)
        return scores
