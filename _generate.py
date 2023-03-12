import pandas as pd
import os
import sys
import shutil
import requests
import yaml

template = """---
layout: object
iden: {iden}
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

    manifest_data = {}

    for index, row in df_data.iterrows():
        if row["Access"] == "access_public":
            manifest_url = row["PURL"].replace("/r/", "/iiif/") + "/manifest"
            manifest = requests.get(manifest_url).json()

            item = manifest["items"][0]

            thumbnail = item["thumbnail"][0]["id"]

            # Get annotations
            annotations = []
            if len(item["annotations"]) > 0:
                for annot in item["annotations"][0]["items"]:
                    time = annot["target"].split("=")[-1].split(",")

                    minutes = float(time[0]) // 60
                    seconds = float(time[0]) - (minutes * 60)

                    annotations.append({
                        "value": annot["body"][0]["value"],
                        "start_minutes": int(minutes),
                        "start_seconds": int(seconds),
                    })

            # Metadata
            metadata = []
            for item in manifest["metadata"]:
                metadata.append({
                    "key": item["label"]["en"][0],
                    "value": item["value"]["en"][0],
                })

            manifest_data[row["aviary ID"]] = {
                "thumbnail": thumbnail,
                "annotations": annotations,
                "metadata": metadata,
                "date": row["Date"],
                "title": row["Title"],
                "media": row["Embed"],
                "media2": row["Media Embed 1"],
            }

            new = template.format(
                iden=fix(row["aviary ID"]),
            )

            with open(f"objects/{row['aviary ID']}.md", "w+") as f:
                print(new, file=f)

    with open("_data/objects.yml", "w+") as f:
        yaml.dump(manifest_data, f)
