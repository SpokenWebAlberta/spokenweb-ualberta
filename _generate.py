import os
import shutil
import pathlib

import json
# import requests
import yaml

template = """---
iden: {iden}
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


def get_all_idens():
    all_objects = set()
    path = pathlib.Path("exhibits")
    for filename in os.listdir(path):
        with (path / filename).open() as f:
            text = f.read().split("---")
            out = yaml.safe_load(text[1])
            all_objects.update(out.get("featured_objects", []))

    return all_objects


def process_csv(path):
    all_objects = get_all_idens()

    with open(path) as f:
        for row in f:
            iden = row.strip()
            if iden in all_objects:
                yield iden


def process_manifest(permanent_id, manifest):
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

    # Get stream link
    stream_link = manifest["items"][0]["items"][0]["items"][0]["body"]["id"]

    # Get thumbnail
    thumbnail = manifest["thumbnail"][0]["id"]

    # Collect metadata
    metadata = {}
    for meta in manifest["metadata"]:
        value = meta["value"]["en"][0].replace("<p>", "").replace("</p>", "").replace('"', "'")
        key = meta["label"]["en"][0].replace(" ", "_").lower()
        metadata[key] = value

    return {
        "iden": permanent_id,
        "thumbnail_small": thumbnail,
        "thumbnail_medium": thumbnail.replace("small", "medium"),
        "annotations": annotations,
        "title": manifest["label"]["en"][0],
        "stream": stream_link.split("?")[0],
        "metadata": metadata,
    }


def create_object_page(permanent_id):
    with open(f"objects/{permanent_id}.md", "w+") as f:
        params = {
            "iden": permanent_id,
        }

        print(template.format(**params), file=f)


def main():
    shutil.rmtree("objects", ignore_errors=True)
    os.makedirs("objects")

    path = "_data/subset.txt"

    # Create manifest data
    manifest_data = {}
    for permanent_id in process_csv(path):
        # manifest_url = f"https://ualberta.aviaryplatform.com/iiif/{permanent_id}/manifest"
        # manifest = requests.get(manifest_url).json()
        try:
            with open(f"manifests/{permanent_id}.json") as f:
                manifest = json.load(f)
        except FileNotFoundError:
            print(permanent_id, "File not scrapped")
            continue

        try:
            thumbnail = manifest["thumbnail"][0]["id"]
        except KeyError:
            print(permanent_id, "data missing")
            continue

        manifest_data[permanent_id] = process_manifest(permanent_id, manifest)
        create_object_page(permanent_id)

    # Create main data index
    with open("_data/objects.yml", "w+") as f:
        yaml.dump(manifest_data, f)


if __name__ == "__main__":
    main()
