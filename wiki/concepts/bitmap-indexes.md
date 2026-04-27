---
title: "Bitmap Indexes"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database, indexing, data-structures, OLAP]
---

# Bitmap Indexes

## Overview

Bitmap indexes are a specialized database indexing technique designed for efficient querying on low-cardinality columns in large datasets. Unlike traditional B-tree indexes, bitmap indexes store a bitmap (bit array) for each distinct value in a column, where each bit corresponds to a row in the table. This structure allows for extremely fast bitwise operations during query execution, making bitmap indexes particularly effective for analytical workloads in data warehouses and OLAP systems.

The key advantage of bitmap indexes lies in their ability to perform set operations (AND, OR, NOT) directly on the compressed bit arrays, enabling the database to evaluate complex WHERE clauses with minimal CPU overhead. They are most efficient when applied to columns with a small number of distinct values relative to the total row count—such as status fields, categories, geographic regions, or boolean flags.

## Key Concepts

**Bitmap Structure**: For each distinct value in a column, the index maintains a bitmap of length equal to the number of rows in the table. If a row contains the value, its corresponding bit is set to 1; otherwise, it is 0. This sparse representation is highly compressible using run-length encoding (RLE) or word-aligned hybrid (WAH) compression.

**Cardinality Considerations**: Bitmap indexes excel on low-cardinality columns. For high-cardinality columns (e.g., unique identifiers or timestamps), the bitmap approach becomes inefficient because the number of bitmaps grows large and each bitmap becomes sparse, degrading performance and increasing storage requirements.

**Encoding Strategies**: Several encoding variants exist including equality encoding (simple bitmap per value), range encoding (bitmaps for value ranges), and interval encoding. Some systems also use bitmap vectors with offset encoding for sorted data.

**B-tree vs. Bitmap**: Traditional B-tree indexes are optimal for point queries and range searches on high-cardinality data. Bitmap indexes sacrifice some write performance (due to locking during updates) but provide superior read performance for multi-dimensional filtering in analytical scenarios.

## How It Works

When a query filters on a bitmap-indexed column, the database performs the following steps:

1. **Index Lookup**: The database locates the bitmap(s) corresponding to the filter values.
2. **Bitwise Operations**: If multiple conditions exist (e.g., `status = 'Active' AND region = 'West'`), the relevant bitmaps are loaded into memory and combined using bitwise AND.
3. **Result Materialization**: The resulting bitmap identifies matching rows, which are then retrieved or used for further joins.
4. **Compression**: Modern implementations compress bitmaps before storing them. WAH compression, for example, stores runs of consecutive 0s or 1s as (type, length) pairs, achieving 10-100x compression ratios on typical data.

The bitwise operations are performed using CPU-native word operations, making them extremely fast—processing millions of rows per second is common on modern hardware.

## Practical Applications

Bitmap indexes are widely used in:

- **Data Warehouses**: Query engines like Apache Spark, Oracle Exadata, and PostgreSQL (via extensions) leverage bitmap indexes for fast aggregations and filtering.
- **OLAP Systems**: Multi-dimensional analytics where users filter on dimensions like time, geography, and product category.
- **Search Engines**: Inverted indexes share conceptual similarities with bitmap indexes for document retrieval.
- **Scientific Data**: Genomic databases and sensor networks where boolean filtering is common.
- **Caching Layers**: Bloom filters use bitmap-like structures for fast membership testing.

## Examples

Consider a table `orders` with columns `(order_id, status, region, amount)`:

```sql
CREATE BITMAP INDEX idx_status ON orders(status);
CREATE BITMAP INDEX idx_region ON orders(region);
```

Query: Find all "completed" orders in the "West" region with amount > 1000:

```sql
SELECT * FROM orders 
WHERE status = 'completed' 
  AND region = 'West' 
  AND amount > 1000;
```

The database loads the "completed" bitmap and "West" bitmap, performs bitwise AND to find rows matching both conditions, then applies the amount filter. This approach can evaluate the status and region conditions in microseconds, even on tables with billions of rows.

## Related Concepts

- [[B-tree Indexes]] - Traditional database indexing using balanced trees
- [[Columnar Databases]] - Storage format that pairs well with bitmap indexes
- [[Data Warehousing]] - The domain where bitmap indexes are most prevalent
- [[Run-length Encoding]] - Compression technique commonly used with bitmap indexes
- [[Bloom Filters]] - Probabilistic data structures related to bitmap operations

## Further Reading

- "Bitmap Index Design and Evaluation" - Original research on bitmap index tradeoffs
- Apache ORC/Parquet documentation - Columnar formats with bitmap support
- Oracle Bitmap Index documentation - Enterprise implementation details

## Personal Notes

Bitmap indexes taught me that the "right" data structure depends entirely on your access patterns. I initially over-indexed high-cardinality columns in an analytics project, bloating storage without improving query latency. Switching to bitmap indexes on low-cardinality dimensions (status codes, category tags) reduced our typical dashboard query time from 30 seconds to under 2 seconds. The key insight: understand your cardinality distribution before choosing an index type.
