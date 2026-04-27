---
title: Data Cleansing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-cleansing, data-quality, data-preparation, data-transformation, etl, data-remediation]
---

# Data Cleansing

## Overview

Data Cleansing (also called data cleaning, data scrubbing, or data cleaning) is the process of detecting and correcting — or removing — corrupt, inaccurate, incomplete, duplicated, or improperly formatted data from a dataset. It is the operational arm of [[data-quality]] management: once [[data-profiling]] has identified what is wrong with a dataset, data cleansing performs the remediation. Cleansing is not a one-time activity but a continuous process embedded in data pipelines, since new dirty data arrives continuously from source systems.

The scope of data cleansing ranges from simple, rule-based corrections (standardizing date formats, trimming whitespace, filling nulls with default values) to complex, probabilistic transformations (fuzzy matching to identify and merge duplicate records, predictive models to infer missing values, regex-based pattern normalization). The appropriate cleansing strategy depends on the type and severity of the quality problem, the use case for the data, and the cost of over-cleansing (removing legitimate signal along with noise).

## Key Concepts

### Data Quality Problems and Cleansing Strategies

**Missing values** (nulls, blanks, empty strings) are among the most common quality issues. Strategies for handling them include:

- **Deletion**: Remove rows or columns with excessive missing data. Appropriate when the missing data is random and the affected records are a small fraction.
- **Default imputation**: Fill nulls with a sentinel value (e.g., "UNKNOWN", -1, "1970-01-01"). Simple but can introduce biases if downstream systems treat the default as a legitimate value.
- **Statistical imputation**: Fill nulls with mean, median, or mode values from the non-null distribution. Preserves aggregate statistics but distorts distributions.
- **Predictive imputation**: Use ML models (e.g., regression, KNN) to infer null values from related columns. More accurate but computationally expensive.
- **Flag-and-keep**: Add a boolean column indicating whether a value was originally null (e.g., `has_null_country_code`), preserving the information that data was missing without losing the record.

**Duplicate records** occur when the same entity is represented by multiple rows — due to integration bugs, re-submissions, or entity resolution failures. Strategies include:

- **Deduplication**: Identify and merge/remove exact duplicates (all column values identical). Simple but rare in practice.
- **Fuzzy matching**: Use string similarity metrics (Levenshtein distance, Jaro-Winkler, phonetic matching) to identify near-duplicates. Requires tuning similarity thresholds and deciding merge strategies.
- **Deterministic matching**: Match on a subset of high-confidence fields (e.g., email address + date of birth) to identify duplicates without probabilistic scoring.

**Inconsistent formats and values** arise when the same concept is represented differently across records:

- **Date format normalization**: "2026-04-13", "04/13/2026", "13-APR-2026", and "April 13, 2026" all represent the same date — cleansing standardizes them to a canonical format.
- **Address standardization**: "123 Main St.", "123 Main Street", and "123 MAIN ST" can be normalized to a standard representation using address verification services.
- **Categorical value standardization**: "NY", "New York", and "N.Y." are unified; "active", "Active", and "ACTIVE_STATUS=1" are mapped to consistent codes.
- **Unit conversion**: Prices stored in mixed currencies or measurement units are converted to a canonical unit before storage.

**Outliers and invalid values** are data points that fall outside expected ranges or violate integrity constraints:

- **Range validation**: Rejecting or flagging values outside defined bounds (e.g., negative prices, ages over 150, future dates for birthdate).
- **Type validation**: Rejecting values that cannot be parsed as the declared data type.
- **Pattern validation**: Rejecting values that don't match expected formats (e.g., a phone number field containing alphabetic characters).
- **Outlier handling**: Statistical outliers (values beyond 3 standard deviations) may be genuine anomalies worth investigating, not just noise.

### Cleansing in ETL Pipelines

In the ETL (Extract, Transform, Load) model, cleansing is typically the "T" — transformation logic applied during data movement from source to destination. Well-designed pipelines apply cleansing as close to the source as possible, so downstream consumers benefit from clean data without needing to re-implement corrections.

Modern data stacks distinguish between **early-stage cleansing** (performed in staging/raw layers, preserving original source records for auditability) and **late-stage cleansing** (applied in analytical models, where business logic is encoded). The pattern `raw_` -> `staging_` -> `mart_` or `final_` in table naming often reflects these stages.

### Master Data Management

For entities like customers, products, and suppliers that are referenced across many systems, cleansing extends to **master data management** (MDM) — the practice of establishing a "single source of truth" for key business entities. MDM involves identity resolution (determining which records refer to the same entity), golden record creation (merging best-of-breed attributes from multiple sources into a master record), and ongoing synchronization (propagating master changes back to consuming systems).

## How It Works

A practical data cleansing workflow typically follows a detect-profile-clean-validate cycle:

```python
# Example: A data cleansing pipeline using Python and pandas
import pandas as pd
import numpy as np
import re
from typing import Callable

def standardize_phone(phone: str) -> str:
    """Normalize US phone numbers to (XXX) XXX-XXXX format."""
    if pd.isna(phone):
        return None
    # Strip all non-digits
    digits = re.sub(r'\D', '', str(phone))
    # Handle 10-digit US numbers (ignore country code 1)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return None  # Invalid format

def clean_email(email: str) -> str:
    """Standardize email to lowercase and strip whitespace."""
    if pd.isna(email):
        return None
    cleaned = str(email).lower().strip()
    # Basic format validation
    if '@' in cleaned and '.' in cleaned.split('@')[1]:
        return cleaned
    return None

def impute_age(age: int) -> int:
    """Impute reasonable age ranges for invalid values."""
    if pd.isna(age):
        return None
    if age < 0 or age > 150:
        return None  # Flag as invalid rather than imputing
    return age

def deduplicate_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate customers based on email + name fuzzy match."""
    # Exact duplicates first
    df = df.drop_duplicates(subset=['email', 'full_name'], keep='first')
    
    # For fuzzy matching, we'd use recordlinkage or rapidfuzz library
    # Example with simple blocking: same postal code + similar name
    # blocked = df.groupby('postal_code')
    # for block in blocked:
    #     records = block[1]
    #     if len(records) > 1:
    #         compute pairwise similarity on 'full_name'
    #         merge pairs above threshold
    
    return df

def cleanse_customer_data(input_path: str, output_path: str) -> dict:
    df = pd.read_csv(input_path)
    original_count = len(df)
    
    # Clean phone numbers
    df['phone_clean'] = df['phone'].apply(standardize_phone)
    
    # Clean emails
    df['email_clean'] = df['email'].apply(clean_email)
    
    # Impute ages
    df['age_imputed'] = df['age'].apply(impute_age)
    
    # Normalize status codes
    status_map = {
        'active': 'ACTIVE',
        'Active': 'ACTIVE', 
        'ACTIVE_STATUS=1': 'ACTIVE',
        'inactive': 'INACTIVE',
        'inactive_user': 'INACTIVE',
        'churned': 'CHURNED',
    }
    df['status_clean'] = df['status'].map(status_map).fillna('UNKNOWN')
    
    # Remove exact duplicates
    df = deduplicate_customers(df)
    
    # Report statistics
    final_count = len(df)
    return {
        'original_rows': original_count,
        'final_rows': final_count,
        'duplicates_removed': original_count - final_count,
        'nulls_filled': {
            'phone': df['phone_clean'].notna().sum() - df['phone'].notna().sum(),
            'email': df['email_clean'].notna().sum() - df['email'].notna().sum(),
        }
    }
```

## Practical Applications

### CRM Data Hygiene

A retail company's CRM system has accumulated 5 years of customer records with significant dirty data: duplicate customer records (same person registered multiple times with slight variations in name/email), obsolete address records (customer moved but old addresses not archived), and inconsistent lead sources (the same marketing campaign tracked with 47 different UTM parameter variations). A cleansing pipeline normalizes addresses using a postal verification API, runs fuzzy matching to identify duplicate records for manual review, and standardizes UTM parameters to a canonical set of campaign names. After cleansing, the marketing team sees a 30% reduction in audience size (removing duplicates) but a 45% improvement in campaign attribution accuracy.

### Financial Transaction Reconciliation

A payment processor processes millions of transactions daily across multiple acquiring banks. Each bank's raw feed has slightly different schemas, date formats, currency codes, and status values. A cleansing layer normalizes all feeds to a common schema: ISO 4217 currency codes, ISO 8601 timestamps in UTC, ISO 20022 status codes. A reconciliation engine then matches transactions between the processor's internal ledger and bank settlement files — cleansing first ensures that formatting differences don't cause legitimate transactions to fail matching.

### Healthcare Record De-identification

Under HIPAA, a research dataset must remove or mask Protected Health Information (PHI) before being shared with external researchers. A cleansing pipeline identifies and removes direct identifiers (name, SSN, MRN, exact address) and applies the Safe Harbor de-identification method — replacing dates with year-only for patients over 89, generalizing ZIP codes to the first 3 digits, and removing fields that could be combined to re-identify individuals. The cleansed dataset preserves analytical utility while meeting regulatory requirements.

## Examples

A cleansing transformation specification in YAML:

```yaml
# Data cleansing specification: customer_data_cleansing_v3
description: Cleansing rules for raw customer ingestion pipeline
version: "3.0"
last_modified: 2026-04-13

rules:
  - column: email
    operations:
      - transform: lowercase
      - transform: trim_whitespace
      - validate: regex "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        on_failure: set_null
      - deduplicate_strategy: first_non_null  # keep first occurrence

  - column: phone_number
    operations:
      - transform: strip_non_digits
      - transform: normalize_to_e164
        default_region: US
      - validate: length == 10 or length == 11
        on_failure: flag_for_review
      - deduplicate_strategy: keep_most_recent_by_timestamp

  - column: date_of_birth
    operations:
      - transform: parse_multiple_formats
        formats: ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y", "%Y%m%d"]
      - validate: range "1900-01-01" to "2026-04-13"
        on_failure: set_null_flag_age_invalid
      - transform: generalize_to_year_of_birth  # for PHI-safe datasets
        apply_after: 2026-01-01

  - column: address
    operations:
      - transform: standardize_state_abbreviations
        mapping_source: USPS official abbreviations
      - transform: normalize_street_suffixes
        mapping:
          St: Street
          Ave: Avenue
          Blvd: Boulevard
          Rd: Road
          Dr: Drive
      - validate: require_non_empty_city_and_state
        on_failure: flag_for_manual_review

  - column: customer_name
    operations:
      - transform: trim_whitespace
      - transform: capitalize_each_word
      - transform: remove_special_characters
        keep: ["-", "'", "."]
      - deduplicate_strategy: fuzzy_match_threshold
        threshold: 0.95
        fields: [first_name, last_name, date_of_birth]
        on_match: keep_longest_record

quality_gates:
  - name: no_duplicate_emails
    check: SELECT COUNT(DISTINCT email) = COUNT(*) FROM cleansed_customers
    severity: blocking
    
  - name: email_format_valid
    check: percentage of valid email formats > 99%
    severity: warning
    
  - name: null_rate_acceptable
    check: null rate per critical column below threshold
    columns: [email, customer_id, registration_date]
    thresholds:
      email: < 5%
      customer_id: 0%
      registration_date: < 2%
    severity: warning
```

## Related Concepts

- [[data-quality]] — The broader discipline that cleansing is part of
- [[data-profiling]] — The diagnostic step that precedes and informs cleansing
- [[data-transformation]] — The broader category of data manipulation that cleansing falls under
- [[etl]] — The pipeline context where cleansing is commonly applied
- [[master-data-management]] — Advanced cleansing for key business entities
- [[data-governance]] — Governance policies that define what cleansing rules are required
- [[data-catalog]] — Where cleansing rules and their versions are documented

## Further Reading

- "Data Cleaning" by白玉玺 and others — Comprehensive academic survey of cleansing techniques
- "The Quartz guide to bad data" — Practical guide to common data problems and how to address them
- Great Expectations — Python library for data validation and documentation
- Apache Griffin — Open source data quality platform with cleansing capabilities
- "Master Data Management" by David Loshin — MDM and identity resolution concepts

## Personal Notes

The most underappreciated aspect of data cleansing is that cleansing decisions are inherently political — they reflect choices about which source of truth to trust, how to handle ambiguity, and what trade-offs to make between data completeness and accuracy. When two authoritative systems disagree on a customer's address, which one wins? When a phone number is malformed, should we try to parse it or throw it away? These aren't purely technical decisions, and they have business consequences. The best cleansing implementations I've seen involve business stakeholders in defining the rules, with explicit documentation of who made each decision and why. Cleansing without business input tends to either be too aggressive (destroying legitimate signal) or too conservative (leaving problems in place).
