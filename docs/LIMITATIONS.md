## Deduplication

During dataset preparation, exact duplicate receipt images were detected across upstream sources using SHA-256 hashing.

In cases where duplicates were found:
- a single canonical copy was retained,
- corresponding annotations were preserved,
- redundant image–annotation pairs were removed.

This was done to reduce training bias and prevent over-representation of identical samples.
