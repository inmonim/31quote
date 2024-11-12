import os
from datetime import date

import pandas as pd
from config import _engine

today = date.today()

def dump_csv(table):
    df = pd.read_sql_table(table_name=table, schema="31quote", con=_engine)
    df.to_csv(f"./data_dump/{today}/{table}_{today}.csv", encoding="utf-8", index=False)

if not os.path.exists(f"./data_dump/{today}"):
    os.mkdir(f"./data_dump/{today}")

table_names = ["quotes", "speakers", "categories", "references", "reference_types", "speaker_careers"]

for tn in table_names:
    dump_csv(tn)