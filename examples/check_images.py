import os
import hashlib
from PIL import Image
from collections import defaultdict

RECEIPTS_DIR = os.environ.get("RECEIPTS_DIR", "receipts")
OUT_DIR = os.environ.get("OUT_DIR", "artifacts")

IMG_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}

def sha256_file(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    corrupt = []
    hashes = defaultdict(list)

    files = []
    for f in os.listdir(RECEIPTS_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in IMG_EXTS:
            files.append(f)

    for f in sorted(files):
        p = os.path.join(RECEIPTS_DIR, f)

        # Corrupt check (decode)
        try:
            with Image.open(p) as im:
                im.verify()
        except Exception as e:
            corrupt.append((f, str(e)))
            continue

        # Duplicate check (hash)
        try:
            h = sha256_file(p)
            hashes[h].append(f)
        except Exception as e:
            corrupt.append((f, f"hash_failed: {e}"))

    dup_groups = [v for v in hashes.values() if len(v) > 1]

    with open(os.path.join(OUT_DIR, "corrupt_images.txt"), "w", encoding="utf-8") as out:
        for f, err in corrupt:
            out.write(f"{f}\t{err}\n")

    with open(os.path.join(OUT_DIR, "duplicate_images.txt"), "w", encoding="utf-8") as out:
        for group in dup_groups:
            out.write(", ".join(group) + "\n")

    print("✅ Image checks complete")
    print(f"- Corrupt: {len(corrupt)} (artifacts/corrupt_images.txt)")
    print(f"- Duplicate groups: {len(dup_groups)} (artifacts/duplicate_images.txt)")

if __name__ == "__main__":
    main()
