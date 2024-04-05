import itertools
import re
from copy import copy, deepcopy
from functools import wraps
from politely.errors import EFNotSupportedError, SFNotIncludedError, EFNotIncludedError
from politely.fetchers import fetch_kiwi
from politely import RULES, SEP, TAG, NULL, SELF
from politely.modeling_gpt2_scorer import GPT2Scorer
from politely.modeling_heuristic_scorer import HeuristicScorer
from politely.modeling_sbg_scorer import SkipBigramScorer
from politely.modeling_scorer import Scorer
from politely.rules import EFS


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # get the function signature
        f_out = f(*args, **kwargs)
        names = f.__code__.co_varnames[: f.__code__.co_argcount]
        styler_instance: Styler = args[0]
        # exclude self
        styler_instance.log[f.__name__] = {
            "in": dict(zip(names[1:], args[1:])),
            "out": copy(styler_instance.out),
        }
        return f_out  # return the out

    return wrapper


class Styler:
    """
    A rule-based Korean Politeness Styler
    """

    def __init__(self, strict: bool = False, scorer: str = "sbg"):
        #  --- object-owned attributes --- #
        if scorer == "heuristic":
            self.scorer: Scorer = HeuristicScorer()
        elif scorer == "sbg":
            self.scorer: Scorer = SkipBigramScorer()
        elif scorer == "gpt2":
            try:
                import torch
            except ImportError:
                raise ImportError(
                    "`torch` (Pytorch) is required to use `GPT2Scorer`. Please install it via `pip3 install torch`."
                )
            else:
                self.scorer: Scorer = GPT2Scorer()
        else:
            raise ValueError(
                f"scorer should be either 'heuristic', `sbg` or 'gpt2', but got {scorer}"
            )
        self.strict = strict
        self.out: any = None
        self.kiwi = fetch_kiwi()
        self.rules = deepcopy(RULES)
        self.log = dict()

    def __call__(self, sent: str, politeness: int) -> str:
        """
        Style a sentence with the given politeness (0, 1, 2)
        """
        self.setup().preprocess(sent).analyze().check().honorify(
            politeness
        ).guess().elect().conjugate()
        return self.out

    def setup(self):
        """
        Reset the out and clear all the logs,
        """
        self.out = None
        self.log.clear()
        self.log.update({"conjugations": set(), "honorifics": set()})
        return self

    @log
    def preprocess(self, sent: str):
        """
        Make sure each sentence ends with a period, if it does not end with any SF.
        We do this to increase the accuracy of `kiwi.join`.
        """
        self.out = re.sub(r"([^!?.]+)$", r"\1.", sent.strip())
        return self

    @log
    def analyze(self):
        """
        Analyze the sentence and generate the output.
        """
        self.out: str
        self.out = [
            f"{token.form}{TAG}{token.tag}" for token in self.kiwi.tokenize(self.out)
        ]
        self.out = SEP.join(self.out)  # to match with the format of the rules
        return self

    def check(self):
        """
        Check if your assumption holds. Raises a custom error if any of them does not hold.
        """
        self.out: str
        # raise exceptions only if you are in debug mode
        if self.strict:
            # assumption 1: every sentence should end with a valid SF. It should be one of: (., !, ?)
            if "SF" not in self.out:
                raise SFNotIncludedError(self.out)
            # assumption 2: every sentence should include a valid EF. It should match the EFS pattern.
            if "EF" not in self.out:
                raise EFNotIncludedError(self.out)
            # assumption 3: all EF's should be supported by politely.
            if not all(
                [re.match(EFS, pair) for pair in self.out.split(SEP) if "EF" in pair]
            ):
                raise EFNotSupportedError(self.out)
        return self

    @log
    def honorify(self, politeness: int):
        """
        Determines all the candidates that would properly honorify the sentence.
        Do this by chain-conjugating sets.
        """
        self.out: str
        pair2honorifics = {}
        for pattern in self.rules.keys():
            match = re.search(pattern, self.out)
            if match:
                # should be only one pair
                pair = match.group("MASK")
                honorifics = {
                    honorific.replace(SELF, pair)
                    for honorific in self.rules[pattern][politeness]
                }
                # progressively narrow down honorifics
                pair2honorifics[pair] = (
                    pair2honorifics.get(pair, honorifics) & honorifics
                )
        # get all possible candidates
        candidates = itertools.product(
            *[
                pair2honorifics.get(
                    pair,
                    {
                        pair,
                    },
                )
                for pair in self.out.split(SEP)  # SEP
            ]
        )
        # remove empty candidates
        candidates = [
            [pair.split(SEP) for pair in candidate if pair != NULL]
            for candidate in candidates
        ]
        # flatten pairs
        candidates = [list(itertools.chain(*candidate)) for candidate in candidates]
        # a list of candidates
        self.out = candidates
        return self

    @log
    def guess(self):
        """
        Guess the scores.
        """
        self.out: list[list[str]]
        scores = self.scorer(candidates=self.out, log=self.log, kiwi=self.kiwi)
        self.out = [(candidate, score) for candidate, score in zip(self.out, scores)]
        return self

    @log
    def elect(self):
        """
        Elect the best candidate.
        """
        self.out: list[tuple[list[str], float]]
        best = max(self.out, key=lambda x: x[1])
        self.out = best
        return self

    @log
    def conjugate(self):
        """
        conjugate the best candidate.
        """
        self.out: tuple[list[str], float]
        sent = self.out[0]
        self.out = self.kiwi.join(
            [(pair.split(TAG)[0], pair.split(TAG)[1]) for pair in sent]
        )
        return self

    def add_rules(self, rules: dict[str, tuple[set, set, set]]):
        """
        Add rules to the existing rules.
        """
        # check if the rules are in proper format
        for key, _ in rules.items():
            # first, check if the key includes a group with the key; (?<MASK>...)
            # e.g. (?P<MASK>(아빠|아버지){TAG}NNG)
            if not re.search(re.escape(r"(?P<MASK>") + r".*" + re.escape(")"), key):
                raise ValueError(
                    f"key should include a group with the key; (?P<MASK>...), but got {key}"
                )
        self.rules.update(rules)
        return self
