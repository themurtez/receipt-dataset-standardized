# NOTICE — Attribution & Licensing

This repository contains a **derived and augmented dataset** created by curating and standardizing multiple publicly available receipt datasets.

The original images and any original annotations remain the property of their respective creators. Redistribution here is provided in accordance with the licenses listed below.

## Annotation methodology (important)
The JSON annotations in this repo were produced using a combination of:
- original dataset annotations (where available),
- AI-assisted OCR / information extraction using commercial AI models,
- manual review and normalization for schema consistency.

These annotations are **model-assisted labels** intended for research, training, and evaluation — not authoritative financial ground truth.

## Upstream datasets

1. **CORD (Clova Receipt Dataset v2)**
   - License: CC-BY 4.0
   - Citation: Park, S., Lee, J., & Lee, H. (2019). CORD: A Consolidated Receipt Dataset for Post-OCR Parsing [Data set]. Clova AI / NAVER.
   - Source: https://huggingface.co/datasets/naver-clova-ix/cord-v2

2. **SROIE (ICDAR 2019 Scanned Receipt OCR & Information Extraction)**
   - License: CC-BY 4.0
   - Citation: Huang, Z., et al. (2019). ICDAR 2019 Competition on Scanned Receipt OCR and Information Extraction [Dataset]. ICDAR 2019.
   - Source: https://doi.org/10.1109/ICDAR.2019.00244

3. **ExpressExpense SRD (Free Receipt Dataset)**
   - License: MIT
   - Attribution: Free Receipt Images – SRD dataset by ExpressExpense.
   - Source: https://expressexpense.com/blog/free-receipt-images-ocr-machine-learning-dataset/

4. **Zenodo Dataset of Invoices and Receipts**
   - License: CC-BY 4.0
   - Citation: Cruz, F., & Castelli, M. (2022). Dataset of invoices and receipts including annotation of relevant fields [Data set]. Zenodo.
   - Source: https://doi.org/10.5281/zenodo.6371710
