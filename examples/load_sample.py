#!/usr/bin/env python3
"""
Load one receipt image + its annotation JSON by sample ID.

Usage (local folders):
  python3 examples/load_sample.py --id sroie_X51005442346

Usage (from archive):
  python3 examples/load_sample.py --id sroie_X51005442346 --archive receipt_dataset_2781.tgz

Notes:
- Default expects:
    receipts/<id>.jpg
    annotations/<id>.json
- If your images use mixed extensions, this script tries common ones.
"""

import argparse
import io
import json
import os
import tarfile
from typing import Optional, Tuple

# Optional dependency: Pillow (only needed if you want to open/display images)
try:
    from PIL import Image  # type: ignore
except Exception:
    Image = None  # Pillow not installed; still works for JSON loading

COMMON_IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"]


def find_existing_image_path(receipts_dir: str, sample_id: str) -> Optional[str]:
    """Try common extensions and return the first existing image path."""
    for ext in COMMON_IMAGE_EXTS:
        p = os.path.join(receipts_dir, sample_id + ext)
        if os.path.exists(p):
            return p
    return None


def load_local(sample_id: str, receipts_dir: str, annotations_dir: str) -> Tuple[Optional[bytes], dict, str]:
    """Load image bytes + JSON from local folders."""
    ann_path = os.path.join(annotations_dir, sample_id + ".json")
    if not os.path.exists(ann_path):
        raise FileNotFoundError(f"Annotation not found: {ann_path}")

    with open(ann_path, "r", encoding="utf-8") as f:
        ann = json.load(f)

    img_path = find_existing_image_path(receipts_dir, sample_id)
    img_bytes = None
    if img_path:
        with open(img_path, "rb") as f:
            img_bytes = f.read()

    return img_bytes, ann, (img_path or "(image not found)")


def load_from_archive(sample_id: str, archive_path: str) -> Tuple[Optional[bytes], dict, str]:
    """
    Load image bytes + JSON from a .tgz archive that contains:
      receipts/<id>.<ext>
      annotations/<id>.json
    """
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    img_bytes = None
    ann = None

    # Build candidate member names
    ann_member = f"annotations/{sample_id}.json"
    img_members = [f"receipts/{sample_id}{ext}" for ext in COMMON_IMAGE_EXTS]

    with tarfile.open(archive_path, "r:*") as tar:
        # Load JSON
        try:
            m = tar.getmember(ann_member)
        except KeyError:
            raise FileNotFoundError(f"Annotation not found in archive: {ann_member}")

        with tar.extractfile(m) as f:  # type: ignore[arg-type]
            if f is None:
                raise RuntimeError(f"Failed to read {ann_member} from archive")
            ann = json.loads(f.read().decode("utf-8"))

        # Load image (optional)
        img_member_found = None
        for cand in img_members:
            try:
                mimg = tar.getmember(cand)
                img_member_found = cand
                with tar.extractfile(mimg) as fimg:  # type: ignore[arg-type]
                    if fimg is None:
                        continue
                    img_bytes = fimg.read()
                break
            except KeyError:
                continue

    return img_bytes, ann, (img_member_found or "(image not found in archive)")


def print_summary(sample_id: str, ann: dict, image_ref: str) -> None:
    merchant = ann.get("merchant", {}) or {}
    tx = ann.get("transaction", {}) or {}
    items = ann.get("items", []) or []

    mname = merchant.get("name", "")
    date = tx.get("date", "")
    currency = tx.get("currency", "")
    total = tx.get("total", None)

    print("✅ Loaded sample")
    print(f"- id: {sample_id}")
    print(f"- image: {image_ref}")
    print(f"- merchant.name: {mname}")
    print(f"- transaction.date: {date}")
    print(f"- transaction.total: {total} {currency}".strip())
    print(f"- items: {len(items)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True, help="Sample ID without extension (e.g. cord_000001)")
    ap.add_argument("--receipts-dir", default="receipts", help="Path to receipts/ folder")
    ap.add_argument("--annotations-dir", default="annotations", help="Path to annotations/ folder")
    ap.add_argument("--archive", default=None, help="Path to .tgz archive (loads from archive instead of folders)")
    ap.add_argument("--show", action="store_true", help="Open the image with Pillow (requires pillow)")
    args = ap.parse_args()

    sample_id = args.id.strip()

    if args.archive:
        img_bytes, ann, image_ref = load_from_archive(sample_id, args.archive)
    else:
        img_bytes, ann, image_ref = load_local(sample_id, args.receipts_dir, args.annotations_dir)

    print_summary(sample_id, ann, image_ref)

    if args.show:
        if Image is None:
            raise RuntimeError("Pillow is not installed. Install with: python3 -m pip install pillow")
        if not img_bytes:
            raise RuntimeError("No image bytes found for this sample.")
        img = Image.open(io.BytesIO(img_bytes))
        img.show()


if __name__ == "__main__":
    main()
