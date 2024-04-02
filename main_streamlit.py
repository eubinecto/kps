"""
It's okay to write dirty stuff, at least as of right now.
"""

from copy import deepcopy
import pprint
import streamlit as st
import pandas as pd 
import yaml
import openai
from politely import Styler, SEP
from politely.errors import SFNotIncludedError, EFNotSupportedError
from dotenv import load_dotenv
from loguru import logger
load_dotenv()


# --- constants --- #
RULES_YAML_STR = """friends and junior:
  comfortable & informal:
    politeness: 0
    reason: A comfortable and informal situation is a very relaxed situation for all, so you may speak to your friends and juniors in a casual style (`-어`).
  formal:
    politeness: 1
    reason: If there are observers around or the situation is rather formal, then you and your listener may not find it completely relaxing. If so, you should speak in a polite style (`-어요`) even when you are speaking to your friends and juniors.
boss at work:
  comfortable & informal:
    politeness: 1
    reason: If you are in an informal situation with your boss, e.g. a company dinner, then you and your boss may find it a little more relaxing than at the work place. Therefore, it is not necessary to speak in a formal style, and you may speak to your boss in a polite style (`-어요`).
  formal:
    politeness: 2
    reason: If you are in a highly formal environment, e.g. an important meeting, you should always speak in a formal style (`-읍니다`). This shows the appropriate respect to your listeners in a high-profile context.
adult family:
  comfortable & informal:
    politeness: 0
    reason: If you are in a relaxed setting, it is customary and allowed to speak to your family members in a casual style (`-어`) even when they are older than you.
  formal:
    politeness: 1
    reason: If someone outside of your family, e.g. a neighbour, is partaking the conversation too, then it is customary to speak to your family in a polite style (`-어요`) so that you and your family come acorss polite to the outsiders."""
RULES = yaml.safe_load(RULES_YAML_STR)
LISTENERS = pd.DataFrame(RULES).transpose().index.tolist()
ENVIRONS = pd.DataFrame(RULES).transpose().columns.tolist()

# change the papago API with GPT-3.5-turbo

SYSTEM_PROMPT = """
you are a masterful translator of English to Korean.
Translate the following English sentence(s) given by the user to Korean sentence(s).
When more than one sentence is given as an input, give your translation in multiple sentences accordingly (merge them to one if appropriate).
"""

def translate(text: str) -> str:
    r = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": text}
        ]
    )
    translated_text = r.choices[0].message.content
    return translated_text


def explain(logs: list[dict], eng: str):
    # CSS to inject contained in a string
    hide_table_row_index = """
                       <style>
                       tbody th {display:none}
                       .blank {display:none}
                       </style>
                       """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # --- step 1 ---
    msg = "### 1️⃣ Translate the sentence to Korean"
    st.markdown(msg)
    for log in logs:
        before = eng
        logger.debug(pprint.pformat(log.keys()))
        after: str = log["preprocess"]["in"]["sent"]
        df = pd.DataFrame([(before, after)], columns=["before", "after"])
        st.markdown(df.to_markdown(index=False))
    # --- step 2 ---
    msg = "### 2️⃣ Determine politeness"
    log = logs[0]  #  anything will suffice
    politeness = log["honorify"]["in"]["politeness"]
    politeness = (
    "casual style (-어)"
    if politeness == 1
    else "polite style (-어요)"
    if politeness == 2
    else "formal style (-습니다)"
    )
    reason = log["case"]["reason"]
    msg += (
        f"\nYou should speak in a `{politeness}` to your `{log['listener']}`"
        f" when you are in a `{log['environ']}` environment."
    )
    msg += f"\n\n Why so? {reason}"
    st.markdown(msg)
    # --- step 3 ---
    msg = f"### 3️⃣ Analyze morphemes"
    st.markdown(msg)
    for log in logs:
        before = " ".join(log["preprocess"]["in"]["sent"])
        after = " ".join(log["analyze"]["out"]).replace(SEP, " ")
        df = pd.DataFrame([(before, after)], columns=["before", "after"])
        st.markdown(df.to_markdown(index=False))
    # --- step 4 ---
    msg = f"### 4️⃣ Apply honorifics"
    st.markdown(msg)
    for log in logs:
        st.markdown("Honorifics applied:")
        before = log["analyze"]["out"]
        print("elect - out", log["elect"]["out"])
        after = SEP.join(log["elect"]["out"][0])
        df = pd.DataFrame(
            [(before, after)], columns=["before", "after"]
        )
        st.markdown(df.to_markdown(index=False))
        st.markdown("Top candidates:")
        top_3_candidate_pairs = list(sorted(log['guess']['out'], key= lambda x: x[1], reverse=True))[:2]
        top_3_candidates = [SEP.join(candidate) for candidate, _ in top_3_candidate_pairs]
        top_3_scores = [score for _, score in top_3_candidate_pairs]
        df = pd.DataFrame(list(zip(top_3_candidates, top_3_scores)), columns=["candidate", "score"])
        st.markdown(df.to_markdown(index=False))
        st.markdown("---")
        
    # # --- step 5 ---
    msg = "### 5️⃣ Conjugate morphemes"
    st.markdown(msg)
    for log in logs:
        before = SEP.join(log["elect"]["out"][0])
        after = " ".join(log["conjugate"]["out"])
        df = pd.DataFrame([(before, after)], columns=["before", "after"])
        st.markdown(df.to_markdown(index=False))


def describe_case(styler: Styler, eng: str, kor: str, listener: str, environ: str):
    try:
        logs = list()
        tuned_sents = list()
        case = RULES[listener][environ]
        sents = [sent.text for sent in styler.kiwi.split_into_sents(kor)]
        logger.debug(f"listener: {listener}, environ: {environ}, sents: {sents}")
        for sent in sents:
            tuned_sent = styler(sent, case["politeness"])
            tuned_sents.append(tuned_sent)
            styler.log.update({"listener": listener, "environ": environ, "case": case})
            logs.append(deepcopy(styler.log))
    except SFNotIncludedError as e1:
        st.error("ERROR: " + str(e1))
    except EFNotSupportedError as e2:
        st.error("ERROR: " + str(e2))
    else:
        st.write(" ".join(tuned_sents))
        with st.expander("Need an explanation?"):
            explain(logs, eng)


def main():
    # parsing the arguments
    st.title("Politely: an explainable Politeness Styler for the Korean language")
    desc = (
        "- 💡: [Jieun Kiaer](https://www.orinst.ox.ac.uk/people/jieun-kiaer) & [Eu-Bin"
        " KIM](https://github.com/eubinecto) @ the Univerity of Oxford\n- ⚡️:"
        " [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) for analyzing Korean morphemes &"
        " `gpt-3.5-turbo`for"
        " english-to-korean translations\n- The code that runs this website is"
        " [publicly available on Github](https://github.com/eubinecto/kps). Please"
        " leave a ⭐ if you like what we are building!"
    )
    st.markdown(desc)
    eng = st.text_input(
        "Type English sentences to translate with honorifics",
        value="Bring your work to fruition. Done is better than perfect.",
    )
    styler = Styler(strict=True, scorer="gpt2")
    if st.button(label="Translate"):
        with st.spinner("Please wait..."):
            kor = translate(eng)
            # 1
            listener = "friends and junior"
            st.header(f"`{listener}` 👥")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            # 2
            st.markdown("---")
            listener = "boss at work"
            st.header(f"`{listener}` 💼")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            # 3
            st.markdown("---")
            listener = "adult family"
            st.header(f"`{listener}` 👨‍👩‍👧‍👦")  # noqa
            left, right = st.columns(2)
            with left:
                environ = "comfortable & informal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)
            with right:
                environ = "formal"
                st.subheader(f"`{environ}`")
                describe_case(styler, eng, kor, listener, environ)


if __name__ == "__main__":
    main()
