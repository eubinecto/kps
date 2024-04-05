

import pandas as pd
from pathlib import Path
from politely import Styler
from politely.errors import EFNotIncludedError

df = pd.read_csv(Path(__file__).resolve().parent / "smg_korean_style.tsv", sep="\t")

# drop rows with NaN values at columns: [formal , informal]
df.dropna(subset=['formal', 'informal'], inplace=True)

styler = Styler(strict=True)

for _, row in df.iterrows():
    formal = row['formal']
    informal = row['informal']
    print(formal)
    print(informal)
    try:
        print(f"{formal} / {styler(formal, 1)}")
        print(f"{informal} / {styler(informal, 0)}")
    except EFNotIncludedError as e: 
        print(e)
        pass 
        

