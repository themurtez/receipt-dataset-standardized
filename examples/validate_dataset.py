import os
import json
import csv
from collections import Counter

RECEIPTS_DIR = os.environ.get("RECEIPTS_DIR", "receipts")
ANNOTATIONS_DIR = os.environ.get("ANNOTATIONS_DIR", "annotations")
OUT_DIR = os.environ.get("OUT_DIR", "artifacts")

IMG_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}

def base_id(filename: str) -> str:
    # cord_000001.jpg -> cord_000001
    return os.path.splitext(filename)[0]

def list_images(path: str):
    if not os.path.isdir(path):
        return []
    out = []
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1].lower()
        if ext in IMG_EXTS:
            out.append(f)
    return sorted(out)

def list_json(path: str):
    if not os.path.isdir(path):
        return []
    return sorted([f for f in os.listdir(path) if f.lower().endswith(".json")])

def safe_read_json(fp: str):
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:
        return None, str(e)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    imgs = list_images(RECEIPTS_DIR)
    anns = list_json(ANNOTATIONS_DIR)

    img_ids = {base_id(f) for f in imgs}
    ann_ids = {base_id(f) for f in anns}

    missing_json = sorted(img_ids - ann_ids)
    missing_img = sorted(ann_ids - img_ids)
    paired = sorted(img_ids & ann_ids)

    # Validate JSON parses + collect simple schema stats
    bad_json = []
    top_level_keys = Counter()
    prefix_counts = Counter()

    for _id in paired:
        prefix = _id.split("_", 1)[0] if "_" in _id else "unknown"
        prefix_counts[prefix] += 1

        ann_path = os.path.join(ANNOTATIONS_DIR, _id + ".json")
        data, err = safe_read_json(ann_path)
        if err:
            bad_json.append({"id": _id, "error": err})
            continue
        if isinstance(data, dict):
            top_level_keys.update(list(data.keys()))

    # Write reports
    def write_list(name, items):
        p = os.path.join(OUT_DIR, name)
        with open(p, "w", encoding="utf-8") as f:
            for x in items:
                f.write(str(x) + "\n")
        return p

    missing_json_path = write_list("missing_json.txt", missing_json)
    missing_img_path = write_list("missing_images.txt", missing_img)

    bad_json_path = os.path.join(OUT_DIR, "bad_json.csv")
    with open(bad_json_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "error"])
        w.writeheader()
        w.writerows(bad_json)

    # MANIFEST.csv (paths relative to repo conventions)
    manifest_path = os.path.join(OUT_DIR, "MANIFEST.csv")
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["id", "source_prefix", "image_path", "annotation_path"]
        )
        w.writeheader()
        for _id in paired:
            prefix = _id.split("_", 1)[0] if "_" in _id else "unknown"
            w.writerow({
                "id": _id,
                "source_prefix": prefix,
                "image_path": f"receipts/{_id}.jpg",
                "annotation_path": f"annotations/{_id}.json",
            })

    # Human-readable summary
    summary_path = os.path.join(OUT_DIR, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"Receipts dir: {RECEIPTS_DIR}\n")
        f.write(f"Annotations dir: {ANNOTATIONS_DIR}\n\n")
        f.write(f"Images found: {len(imgs)}\n")
        f.write(f"Annotations found: {len(anns)}\n")
        f.write(f"Paired: {len(paired)}\n")
        f.write(f"Missing JSON for image: {len(missing_json)} (see {missing_json_path})\n")
        f.write(f"Missing image for JSON: {len(missing_img)} (see {missing_img_path})\n")
        f.write(f"Bad JSON files: {len(bad_json)} (see {bad_json_path})\n\n")
        f.write("Counts by prefix:\n")
        for k, v in prefix_counts.most_common():
            f.write(f"  {k}: {v}\n")
        f.write("\nMost common top-level JSON keys:\n")
        for k, v in top_level_keys.most_common(40):
            f.write(f"  {k}: {v}\n")

    print("✅ Validation complete")
    print(f"- Summary: {summary_path}")
    print(f"- Manifest: {manifest_path}")
    print(f"- Missing JSON list: {missing_json_path}")
    print(f"- Missing image list: {missing_img_path}")
    print(f"- Bad JSON CSV: {bad_json_path}")

if __name__ == "__main__":
    main()
