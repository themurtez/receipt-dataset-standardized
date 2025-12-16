# Receipt Dataset — Standardized & AI-Assisted Annotations

This repository contains a **curated and standardized receipt image dataset** with corresponding JSON annotations, derived from multiple publicly available receipt datasets.

The primary goal of this project is to provide a **clean, consistent image–annotation format** suitable for training and evaluating document AI / OCR / information extraction models.

---

## Dataset Structure

Each receipt image has a corresponding annotation file with the **same base filename**.

receipts/
cord_000001.jpg
sroie_000145.jpg

annotations/
cord_000001.json
sroie_000145.json

---

## Data quality / completeness

Receipts are real-world scans. Some fields may be **missing, unreadable, cropped, or blurred** (common in OCR datasets).
When information is unavailable, fields may be present but empty (e.g. `""`) or may use placeholders for unknown values (e.g. `"YYYY-MM-DD"` / `"HH:MM:SS"`).

This dataset is intended for **training and evaluation** of document AI systems under realistic conditions, not as perfectly complete ground truth.

---

## Full dataset download

The full dataset is provided as a single archive:

- `receipt_dataset_2780.tgz` (contains `receipts/` and `annotations/`)
- `receipt_dataset_2780.tgz.sha256` (checksum)

Extract:
```bash
tar -xzf receipt_dataset_2780.tgz
```
The dataset is hosted externally to keep this repository lightweight:

👉 https://huggingface.co/datasets/mankind1023/receipt-dataset-standardized

---

## Pairing rule: ##

receipts/<id>.jpg ↔ annotations/<id>.json


The dataset source (e.g. `cord`, `sroie`) is encoded in the filename prefix for traceability.

---

## Annotation Methodology

Annotations were produced using a combination of:
- original dataset annotations (where available),
- AI-assisted OCR and information extraction using commercial AI models,
- manual review and normalization to enforce schema consistency.

The resulting JSON files represent **model-assisted labels** intended for **research, training, and evaluation**, not authoritative financial ground truth.

---

## Data Curation

During preparation, corrupted files, unreadable scans, and duplicate receipts were removed to improve overall dataset quality and training signal.

---

## Schema

The annotation schema is documented in:

- [`docs/SCHEMA.md`](docs/SCHEMA.md)

---

## Licensing & Attribution

This repository redistributes data from multiple upstream datasets under their respective licenses.

- Full attribution and disclosure: [`NOTICE.md`](NOTICE.md)
- Upstream license texts: [`licenses/`](licenses/)
- Repository content (docs, schema, examples) is licensed under MIT (see `LICENSE`)

Please review these files before using the dataset.
