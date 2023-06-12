import math

import pandas as pd
import os
import sys
import shutil
import requests
import yaml
import json
from math import ceil

template = """---
layout: object
iden: {iden}
title: {title}
thumbnail_small: {thumbnail}
{metadata}
---
"""


def fix(value):
    if value != value:
        return ""
    elif isinstance(value, int):
        return value
    elif isinstance(value, str):
        test = value.replace('"', "'")
        return f'"{test}"'
    else:
        raise Exception(f"unknown metadata type: {type(value)}")


if __name__ == "__main__":
    shutil.rmtree("objects", ignore_errors=True)
    os.makedirs("objects")

    df_data = pd.read_csv("_data/data.csv")

    # Create manifest data
    manifest_data = {}
    for index, row in df_data.iterrows():
        if row["Access"] != "access_public":
            continue

        permanent_id = row["PURL"].split("/")[-1]
        manifest_url = f"https://ualberta.aviaryplatform.com/iiif/{permanent_id}/manifest"
        manifest = requests.get(manifest_url).json()

        thumbnail = manifest["thumbnail"][0]["id"]

        # Get annotations
        annotations = []
        annotation_data = manifest["items"][0]["annotations"]
        if len(annotation_data) > 0:
            for annot in annotation_data[0]["items"]:
                time = annot["target"].split("=")[-1].split(",")

                secs = float(time[0])
                hours = int(secs // 3600)
                minutes = int(secs // 60)
                seconds = int(secs % 60)

                annotations.append({
                    "title": annot["body"][0]["value"],
                    "time": secs,
                    "formatted": f"({hours:02}:{minutes:02}:{seconds:02})"
                })

        stream_link = manifest["items"][0]["items"][0]["items"][0]["body"]["id"]

        # Metadata
        metadata = []
        for meta in manifest["metadata"]:
            metadata.append({
                "key": meta["label"]["en"][0],
                "value": meta["value"]["en"][0],
            })

        # Duration
        hours = int(manifest["items"][0]["duration"] // 3600)
        duration = manifest["items"][0]["duration"]

        manifest_data[row["aviary ID"]] = {
            "thumbnail_small": thumbnail,
            "thumbnail_medium": thumbnail.replace("small", "medium"),
            "annotations": annotations,
            "metadata": metadata,
            "title": manifest["label"]["en"][0],
            "stream": stream_link.split("?")[0],
        }

        # Create object page

        metadata_string = ""
        for i in metadata:
            metadata_string += f'{i["key"].replace(" ", "_")}: {fix(i["value"])}\n'

        with open(f"objects/{row['aviary ID']}.md", "w+") as f:
            params = {
                "iden": fix(row["aviary ID"]),
                "title": fix(manifest["label"]["en"][0]),
                "thumbnail": fix(thumbnail),
                "metadata": metadata_string.strip(),
            }

            print(template.format(**params), file=f)

    # Create main data index
    with open("_data/objects.yml", "w+") as f:
        yaml.dump(manifest_data, f)
