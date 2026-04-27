---
title: Data Profiling
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-profiling, data-quality, data-analysis, statistics, metadata, data-assessment]
---

# Data Profiling

## Overview

Data Profiling is the systematic process of examining data sources — tables, files, streams, or entire databases — to understand their structure, content, quality, and interrelationships. It involves applying statistical analysis and pattern detection to discover what data actually looks like in practice, as opposed to what its schema or documentation claims it looks like. Data profiling is the diagnostic foundation of [[data-quality]] management: before you can fix data problems, you need to know what the problems actually are.

Profiling reveals a wide range of data characteristics: the distribution of values in each column, the prevalence of nulls and blanks, the cardinality of categorical fields, the presence of duplicate or near-duplicate records, patterns and formats in string fields (e.g., phone numbers, email addresses), functional dependencies between columns, and anomalies that deviate from expected patterns. Without profiling, data engineers and analysts make assumptions about data that are often wrong — and those wrong assumptions propagate into pipelines, reports, and models.

## Key Concepts

### Column-Level Profiling

The most common form of profiling operates at the column level, computing descriptive statistics for each field:

**Nullability metrics**: The percentage of null, empty string, and whitespace-only values in each column. A column with 40% nulls has very different semantics than one with 0.1% nulls — and downstream consumers need to know this. Profiling also distinguishes between NULL (SQL null), empty string (''), and default/tombstone values that represent null in different ways.

**Value distribution**: The frequency distribution of values — for categorical columns, the top-N most frequent values and their counts; for numeric columns, the min, max, mean, median, standard deviation, and percentile distribution. Distributions reveal whether data is balanced or heavily skewed, whether there are dominant values (possible sentinel values like -1 or "UNKNOWN"), and whether the range is within expected bounds.

**Cardinality**: The count of distinct values relative to the total row count. Low cardinality (few distinct values relative to rows) suggests a categorical field; high cardinality (many distinct values) suggests a free-text or identifier field. Unusually high cardinality in an expected categorical field may indicate data quality problems.

**Pattern detection**: Regular expression matching to identify recurring patterns in string fields — for example, what percentage of values match the format of an email address, phone number, Social Security Number, or UUID. Pattern detection can surface data that was entered inconsistently (e.g., some phone numbers with dashes, some with parentheses, some international).

### Cross-Column Analysis

Beyond single-column statistics, data profiling examines relationships between columns:

**Functional dependencies**: Detecting when the value of one column is fully determined by another (e.g., if `country_code` determines `country_name`, then `country_name` is functionally dependent on `country_code`). Functional dependencies reveal design anomalies — storing derived data — and help with normalization decisions.

**Candidate keys**: Identifying sets of columns that uniquely identify each row (potential primary keys). A candidate key audit tests whether the purported key is truly unique — if a "unique" customer ID has 3% duplicate occurrences, that has major implications for downstream joins.

**Referential integrity**: Checking whether foreign key relationships between tables hold — whether every `customer_id` in the orders table actually exists in the customers table. Referential violations often indicate stale data, integration bugs, or deleted-source-record problems.

**Correlation analysis**: For numeric columns, computing pairwise correlations to identify multicollinearity or unexpected statistical relationships that may indicate data entry errors or systemic biases.

### Content Discovery and Classification

Advanced profiling uses pattern matching, named entity recognition, and classification heuristics to discover what kind of sensitive or regulated data is present:

- **PII detection**: Identifying columns likely containing personally identifiable information — names, email addresses, phone numbers, Social Security Numbers, IP addresses — based on format patterns and content characteristics
- **Financial data**: Detecting columns with monetary values, account numbers, transaction IDs
- **Healthcare data**: Identifying potential HIPAA-regulated data elements (diagnosis codes, procedure codes, prescription drug names)
- **Custom data domains**: Organization-specific classification based on domain dictionaries and rules

This discovery is critical for [[data-governance]] and compliance — you cannot protect or classify data you don't know exists.

## How It Works

Data profiling is typically implemented as a scheduled or on-demand process that runs against data sources:

**Automated profiling jobs** run on a schedule (daily, weekly) against production data, computing the full suite of column statistics and comparing them against established baselines. When a profile deviates significantly from historical norms (e.g., null rate jumps from 2% to 15%), the profiling system triggers an alert. This is often called "schema profiling" or "drift detection."

**On-demand profiling** is triggered by data engineers or analysts investigating a specific dataset — typically when onboarding a new data source, debugging a pipeline failure, or responding to a data quality incident. On-demand profiling is more comprehensive and ad-hoc than automated profiling.

**Integration with [[data-catalog]]**: Profiling results are stored as operational metadata in the catalog, surfacing quality scores and statistics alongside asset descriptions and lineage. When an analyst discovers a table through the catalog, they immediately see whether it has quality issues.

```python
# Example: A data profiling implementation using Python and pandas
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class ColumnProfile:
    column_name: str
    data_type: str
    row_count: int
    null_count: int
    null_percent: float
    distinct_count: int
    distinct_percent: float
    top_values: list[tuple[Any, int]]  # (value, count)
    numeric_stats: Optional[dict] = None  # min, max, mean, std, percentiles

def profile_dataframe(df: pd.DataFrame) -> list[ColumnProfile]:
    profiles = []
    row_count = len(df)
    
    for col in df.columns:
        null_count = df[col].isna().sum()
        null_percent = null_count / row_count * 100
        
        distinct_count = df[col].nunique(dropna=False)
        distinct_percent = distinct_count / row_count * 100
        
        top_values = (
            df[col]
            .value_counts(dropna=False)
            .head(10)
            .items()
        )
        
        profile = ColumnProfile(
            column_name=col,
            data_type=str(df[col].dtype),
            row_count=row_count,
            null_count=null_count,
            null_percent=null_percent,
            distinct_count=distinct_count,
            distinct_percent=distinct_percent,
            top_values=top_values,
        )
        
        if pd.api.types.is_numeric_dtype(df[col]):
            profile.numeric_stats = {
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "p25": float(df[col].quantile(0.25)),
                "p50": float(df[col].quantile(0.50)),
                "p75": float(df[col].quantile(0.75)),
                "p95": float(df[col].quantile(0.95)),
            }
        
        profiles.append(profile)
    
    return profiles

# Usage: Profile a customer table
df_customers = pd.read_csv("s3://data/customers.csv")
profiles = profile_dataframe(df_customers)

for p in profiles:
    print(f"Column: {p.column_name} | Type: {p.data_type}")
    print(f"  Nulls: {p.null_count:,} ({p.null_percent:.1f}%)")
    print(f"  Distinct: {p.distinct_count:,} ({p.distinct_percent:.1f}%)")
    print(f"  Top values: {p.top_values[:3]}")
    if p.numeric_stats:
        print(f"  Numeric stats: mean={p.numeric_stats['mean']:.2f}, "
              f"std={p.numeric_stats['std']:.2f}")
    print()
```

## Practical Applications

### New Data Source Onboarding

A data engineering team is integrating a new SaaS platform's API into their data warehouse. Before building pipelines, they run a profiling job against the extracted data. Profiling reveals: one datetime field has three different format variants (ISO 8601, Unix timestamps, US-style mm/dd/yyyy); the "status" column has 12 distinct values, not the documented 4; the "customer_id" field has 1.3% nulls — suggesting some transactions are not tied to accounts. This profiling shapes the pipeline design and informs business stakeholders of data quirks.

### Data Quality Monitoring

A data quality monitoring system runs nightly profiles on key reporting tables. One morning, the profile for `daily_revenue` shows that the distinct count of `store_id` dropped by 60% — all stores are present in the source system, but the ETL job that joins store metadata has been silently failing for two days, producing a Cartesian product instead. The profiling drift detection caught this before any executive dashboards shipped.

### Data Cleansing Prioritization

Before a major data migration, an organization profiles all datasets to be migrated. The profile results are used to prioritize cleansing efforts: tables with high null rates in critical columns are scheduled for remediation first; columns with many format inconsistencies are flagged for standardization; columns with low cardinality that vary significantly across source systems are flagged for schema mapping challenges.

## Examples

A profiling report for a customer table might reveal:

```yaml
# Data profiling report: raw_customers
profiled_at: 2026-04-13T02:00:00Z
row_count: 1_234_567
columns_profile:
  - name: customer_id
    type: string
    null_count: 0
    null_percent: 0.0
    distinct_count: 1_234_567
    distinct_percent: 100.0
    uniqueness_ratio: 1.0  # candidate key: appears valid
    pattern: "^[A-Z]{2}[0-9]{8}$"  # format: 2 letters + 8 digits
    
  - name: email
    type: string
    null_count: 87_234
    null_percent: 7.07
    distinct_count: 1_102_389
    distinct_percent: 89.3
    top_values:
      - ["", 87334]   # empty string (null in disguise)
      - [null, 87234] # actual null
      - ["test@test.com", 234]  # test data to clean
    email_format_match: 91.2%  # 8.8% have invalid email formats
    
  - name: registration_date
    type: timestamp
    null_count: 12_346
    null_percent: 1.0
    distinct_count: 2_847
    distinct_percent: 0.23
    min_value: 2015-01-01
    max_value: 2026-04-12
    date_range_valid: true
    future_dates: 0
    
  - name: country_code
    type: string
    null_count: 0
    null_percent: 0.0
    distinct_count: 198
    distinct_percent: 0.016
    top_values:
      - ["US", 412_345]
      - ["GB", 187_234]
      - ["DE", 98_234]
      - ["(blank)", 45_123]  # blank string, not null
    cardinality_warning: >100 distinct values in a country field

anomalies:
  - column: email
    severity: high
    description: 7% null rate + 8.8% invalid email format suggests data entry quality issues
  - column: country_code
    severity: medium
    description: 45K blank strings mixed with nulls - normalize before analysis
  - column: customer_id
    severity: info
    description: Candidate key appears valid with 100% uniqueness
```

## Related Concepts

- [[data-quality]] — The discipline that profiling supports and informs
- [[data-cleansing]] — Remediation activities that profiling results trigger
- [[data-catalog]] — Where profiling metadata is typically stored and surfaced
- [[data-governance]] — Compliance use cases for profiling (PII discovery)
- [[statistics]] — Statistical foundations of profiling metrics
- [[metadata-management]] — Broader discipline of managing data about data

## Further Reading

- "Data Quality: The_accuracy Dimension" by Thomas C. Redman — Classic text on data quality fundamentals
- "The Data Warehouse Toolkit" by Ralph Kimball — Profiling guidance as part of dimensional modeling
- Apache Griffin project — Open source data quality platform with profiling capabilities
- Great Expectations — Python library for validating and documenting data quality

## Personal Notes

The most common mistake with data profiling is profiling once and treating the results as permanently valid. Data is alive — source systems change, ETL logic evolves, new data sources get added. A profile snapshot from six months ago is almost certainly wrong today. The organizations that maintain genuinely high data quality treat profiling as a continuous, automated process with baseline comparison and drift alerting. Profiling should be invisible to the data team — integrated into pipeline execution, with dashboards showing quality trends over time rather than point-in-time snapshots.
