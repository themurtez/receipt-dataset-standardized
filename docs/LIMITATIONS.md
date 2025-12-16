## Deduplication

During dataset preparation, exact duplicate receipt images were detected across upstream sources using SHA-256 hashing.

In cases where duplicates were found:
- a single canonical copy was retained,
- corresponding annotations were preserved,
- redundant image–annotation pairs were removed.

This was done to reduce training bias and prevent over-representation of identical samples.

# Limitations

- Some receipts are partially unreadable (blur, glare, low resolution, cropping).
- Merchant metadata may be missing (name/address/phone/tax_id/website).
- Date/time/payment method may be missing or ambiguous.
- Some fields (e.g. accounting categories) are **AI-assisted** and include confidence scores.
- This dataset is intended for ML training/evaluation, not audited financial reporting.
