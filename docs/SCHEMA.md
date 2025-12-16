# Receipt Annotation Schema

This document defines the **standard JSON annotation format** used in this dataset.
Each receipt image has a corresponding JSON file that follows this schema.

The schema is designed for **document AI, OCR post-processing, receipt parsing, and expense categorization** use cases.

---

## Top-level structure

Each annotation file is a single JSON object with the following top-level fields:

- `merchant`
- `transaction`
- `items`
- `summary`
- `ocr_metadata`
- `ocr_raw`

All top-level fields are expected to be present unless explicitly stated otherwise.

---

## merchant

Information about the merchant issuing the receipt.

### Fields

- **name** *(required)*  
  Merchant or business name as printed on the receipt.

- **address** *(optional)*  
  Full postal address.

- **phone** *(optional)*  
  Contact phone number.

- **tax_id** *(optional)*  
  Merchant tax / GST / VAT identifier.

- **website** *(optional)*  
  Website URL, if present.

---

## transaction

High-level transaction details and monetary totals.

### Fields

- **date** *(required)*  
  Transaction date in ISO-8601 format (`YYYY-MM-DD`).

- **time** *(optional)*  
  Transaction time (`HH:MM:SS`).

- **currency** *(required)*  
  ISO-4217 currency code (e.g. `USD`, `MYR`, `EUR`).

- **payment_method** *(optional)*  
  Payment type (e.g. `CASH`, `CREDIT_CARD`, `DEBIT`).

- **subtotal** *(optional)*  
  Amount before tax and discounts.

- **tax** *(optional)*  
  Total tax amount.

- **tip** *(optional)*  
  Tip or gratuity amount.

- **total** *(required)*  
  Final transaction total.

- **accounting_category** *(optional, AI-assisted)*  
  Inferred high-level expense category.

- **category_confidence** *(optional, AI-assisted)*  
  Confidence score for the inferred category (0.0–1.0).

---

## items

Line-item level purchase information.

### Fields

- **name** *(required)*  
  Item description as printed on the receipt.

- **quantity** *(required)*  
  Quantity purchased.

- **unit_price** *(optional)*  
  Price per unit.

- **total_price** *(required)*  
  Total price for the line item.

- **category** *(optional)*  
  Item-level category.

- **accounting_category** *(optional, AI-assisted)*  
  Accounting-oriented category.

- **category_confidence** *(optional, AI-assisted)*  
  Confidence score (0.0–1.0).

---

## summary

Derived totals and rounding information.

### Fields

- **total_items** *(optional)*  
  Number of distinct line items.

- **rounding** *(optional)*  
  Rounding adjustment applied to the total.

- **change_due** *(optional)*  
  Cash change returned to the customer.

---

## ocr_metadata

Metadata describing how the annotation was generated.

### Fields

- **source_image** *(required)*  
  Filename of the receipt image.

- **extraction_engine** *(required)*  
  OCR / extraction system used.

- **model_version** *(optional)*  
  Model or pipeline version identifier.

- **confidence** *(optional)*  
  Overall extraction confidence score (0.0–1.0).

---

## ocr_raw

Unstructured OCR output.

### Fields

- **full_text** *(required)*  
  Full raw OCR text extracted from the receipt image.

This field preserves the original textual signal and enables:
- re-parsing
- error analysis
- alternative post-processing approaches

---

## Notes on AI-assisted fields

Some fields in this schema are **AI-inferred**, not human-verified ground truth.
They are intended for **training, evaluation, and experimentation**, not authoritative financial reporting.

---

## Design goals

This schema is designed to be:

- Consistent across multiple receipt datasets
- Friendly to ML pipelines and dataset loaders
- Explicit about confidence and uncertainty
- Compatible with OCR, NLP, and LLM workflows
- Easy to validate using JSON Schema
