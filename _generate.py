import pandas as pd
import os
import sys
import shutil

template = """---
layout: object
permalink: /objects/{iden}/
title: "{title}"
date: "{date}"
location: "{location}"
media: "{media}"
rights: "{rights}"
---
"""


def fix(value):
    if value != value:
        return ""
    elif isinstance(value, int):
        return value
    elif '"' in value:
        return value.replace('"', "'")
    return value


if __name__ == "__main__":
    shutil.rmtree("objects", ignore_errors=True)
    os.makedirs("objects")

    df_data = pd.read_csv("_data/data.csv")

    for index, row in df_data.iterrows():
        if index > 5:
            break

        new = template.format(
            iden=fix(row["aviary ID"]),
            title=fix(row["Title"]),
            date=fix(row["Date"]),
            location=fix(row["Event Location"]),
            rights=fix(row["Rights Statement"]),
            media=fix(row["Media Embed 1"]),
        )

        with open(f"objects/{row['aviary ID']}.md", "w+") as f:
            print(new, file=f)
