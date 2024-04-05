import os
import random
import numpy as np
from kiwipiepy import Kiwi
from transformers import AutoTokenizer, GPT2LMHeadModel
from politely.modeling_scorer import Scorer
from politely import TAG


class GPT2Scorer(Scorer):
    """
    More accurate than heuristic scorer, but slower. Could be made faster with GPU support. 
    """

    def __init__(self, device: str = "cpu"):
        import torch
        self.gpt2 = GPT2LMHeadModel.from_pretrained(
            "beomi/kykim-gpt3-kor-small_based_on_gpt2"
        ).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "beomi/kykim-gpt3-kor-small_based_on_gpt2"
        )
        self.device = device
        self.gpt2.eval()
        # --- seed everything --- #
        seed = 318
        random.seed(seed)
        os.environ["PYTHONHASHSEED"] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True

    def __call__(
        self,
        candidates: list[list[str]],
        log: dict,
        kiwi: Kiwi,
        # label_smoothing: https://ratsgo.github.io/insight-notes/docs/interpretable/smoothing
        label_smoothing: float = 0.2,
    ) -> list[float]:
        """
        # label_smoothing: https://ratsgo.github.io/insight-notes/docs/interpretable/smoothing
        이걸 batched processing으로 바꾸고 계속하기. device parameter도 추가하기.
        compute the negative log likelihood of the candidates.
        """
        import torch
        from torch.nn import CrossEntropyLoss
        # first, join the pairs into a sentence
        sents = [
            kiwi.join(tuple(pair.split(TAG)) for pair in candidate)
            for candidate in candidates
        ]
        inputs = self.tokenizer(
            sents, return_tensors="pt", padding=True, truncation=True
        ).to(
            self.device
        )  # (N, L)
        with torch.no_grad():
            # output the loss of each instance
            outputs = self.gpt2(**inputs)
        logits = outputs["logits"]  # (N, L, |V|)
        # --- shift them --- #
        shift_logits = logits[:, :-1, :].contiguous()  # (N, L-1, |V|)
        shift_labels = inputs.input_ids[:, 1:].contiguous()  # (N, L-1)
        # flatten the tokens
        # TODO: use weight parameter to increase the losses for canonical ending like -습니다 / -어 / -어요
        loss_fct = CrossEntropyLoss(
            reduction="none",
            ignore_index=self.tokenizer.pad_token_id,
            label_smoothing=label_smoothing,
        )
        loss = loss_fct(
            shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1)
        )
        loss_by_sequence = loss.view(logits.size(0), -1).mean(dim=1)
        # negative log likelihood
        loss_by_sequence = -loss_by_sequence
        return loss_by_sequence.tolist()
