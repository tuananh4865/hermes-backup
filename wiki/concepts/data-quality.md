---
title: Data Quality
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-quality, data-management, data-governance, data-reliability, data-assurance]
---

# Data Quality

## Overview

Data Quality is the measure of a dataset's fitness for its intended purpose — the degree to which data is accurate, complete, consistent, timely, unique, and valid. Poor data quality is not merely an inconvenience; it is a root cause of incorrect business decisions, failed analytics, regulatory violations, and direct financial losses. Studies consistently estimate that dirty data costs organizations tens of millions of dollars annually in wasted engineering time, incorrect reporting, and missed opportunities. High-quality data, by contrast, is a force multiplier: reliable data enables confident decision-making, effective [[machine-learning]] models, and streamlined operations.

Data quality is not a property of a dataset alone — it is relative to its use case. A dataset with 5% null rates in a non-critical field may be perfectly adequate for aggregate reporting but entirely unacceptable for per-record decision-making. This context-dependency is why [[data-profiling]] is essential to quality assessment: you must understand what the data actually looks like before you can judge whether it meets the bar for a given purpose.

Quality is also not static — data degrades over time as source systems change, upstream schemas evolve, integration bugs creep in, and business context shifts. Effective data quality management is therefore a continuous, automated process — not a one-time audit — embedded into data pipelines and operational workflows.

## Key Concepts

### The Six Dimensions of Data Quality

The data quality field has converged on a commonly-cited framework of six primary dimensions:

**Accuracy** measures whether data values reflect the real-world state they are meant to represent. An address that matches a USPS verification is accurate; a customer's age of 999 is not. Accuracy is the most intuitively obvious quality dimension but also the hardest to measure objectively, because it requires ground truth that is often unavailable. In practice, accuracy is often validated indirectly — by cross-referencing against authoritative external sources, by checking referential integrity between related tables, and by applying range and format checks.

**Completeness** measures the degree to which required data is present. Completeness is typically assessed at the field level (what percentage of a column's values are non-null), the record level (what percentage of expected records exist in a table), and the schema level (are all required tables and columns present?). A 95% complete `customer_email` column is nominally acceptable for aggregate analyses but devastating for a personalized email campaign — context determines whether "complete enough" is actually good enough.

**Consistency** measures whether data values are represented the same way across all systems and contexts. An order status represented as "COMPLETE" in one system, "completed" in another, and "order_completed=true" in a third is inconsistent — and any analysis joining these sources will produce incorrect results without complex mapping logic. Consistency also applies to semantics: does "revenue" mean the same thing in the Finance dashboard and the Sales dashboard? Consistency failures are often the most insidious because they appear correct in isolation and only reveal themselves when data is combined.

**Timeliness** measures whether data is available when needed and reflects the current state of the world. A customer address updated in the CRM six months ago but not yet propagated to the marketing platform is stale for a campaign that needs current addresses. Timeliness requirements vary enormously by use case: a fraud detection model needs near-real-time data (seconds of latency); a regulatory report needs daily batch updates; an annual strategic plan can tolerate weekly data. The key is ensuring that data's refresh cadence is explicitly documented and monitored against its use case requirements.

**Uniqueness** measures whether data records are appropriately deduplicated — that each real-world entity appears exactly once in the relevant context. Too few unique records (duplicates) cause over-counting in aggregates and confusing behavior in user-facing applications. Too many unique records (false uniqueness — the same entity represented with slightly different keys) causes under-counting and fragmented views. Achieving correct uniqueness requires stable, unique identifiers and robust identity resolution logic.

**Validity** measures whether data conforms to defined syntax rules, formats, data types, and business constraints. A date stored as "April 13, 2026" in a column declared as DATE is invalid — it may display correctly in some contexts and fail in others. A numeric column containing "N/A" strings is invalid. A phone number field containing alphabetic characters is invalid. Validity is the easiest dimension to automate checks for, because rules can be expressed as constraints — regex patterns, range checks, enum membership — that can be tested programmatically.

### Data Quality Monitoring

Effective data quality management requires continuous monitoring rather than periodic audits. Monitoring involves:

**Automated checks** that run on every pipeline execution or on a schedule, evaluating defined quality rules and emitting pass/fail signals. Checks should cover all six dimensions and be expressed as executable assertions that can be version-controlled alongside the data pipelines they protect.

**Alerting and escalation** that notifies the responsible team when quality drops below defined thresholds. Alerts should be tiered by severity — a 2% increase in null rate in a non-critical field might generate a warning ticket; a complete pipeline failure causing 0% data freshness triggers an on-call alert.

**Dashboarding and trending** that visualizes quality metrics over time, enabling teams to spot gradual degradation before it becomes a crisis. A null rate that creeps from 0.1% to 2% over six months may indicate a slow data source problem that a point-in-time check would miss.

**Root cause investigation** workflows that guide teams through diagnosing and fixing quality problems at their source, rather than patching downstream effects.

## How It Works

Data quality is implemented through a combination of declarative rules, execution-time checks, and governance processes:

**Quality rules** are defined as code — typically in YAML or JSON configuration files that are version-controlled alongside the data pipeline. Each rule specifies a column or dataset to check, the condition to evaluate, the threshold for pass/fail, and the severity if the check fails.

**Execution-time validation** runs rules against data as it flows through the pipeline. The specific implementation depends on the technology stack — Great Expectations for Python-based pipelines, dbt tests for SQL-based transformations, Apache Griffin for big data environments, or custom SQL queries scheduled in the orchestration layer.

**Data quality metrics** are emitted as metadata alongside the data — row counts, null percentages, distinct value counts, freshness timestamps — and stored in a quality metadata store. These metrics feed into [[data-catalog]] entries, lineage graphs, and monitoring dashboards.

```python
# Example: Data quality checks using Great Expectations
import great_expectations as gx

# Create a checkpoint for a customer table
context = gx.get_context()
datasource = context.sources.add_pandas_filesystem(base_directory="./data")
asset = datasource.add_csv_asset("customers.csv")
batch_request = asset.build_batch_request()

expectation_suite = context.add_or_update_expectation_suite(
    expectation_suite_name="customer_quality_suite"
)

# Completeness: no nulls in primary key
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer_id",
        result_format={"result_format": "COMPLETE"}
    )
)

# Validity: email matches regex pattern
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email",
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        mostly=0.99  # 99% must match
    )
)

# Consistency: country_code is a known value
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="country_code",
        value_set=["US", "CA", "GB", "DE", "FR", "JP", "AU"],
        result_format={"result_format": "COMPLETE"}
    )
)

# Range: age is within plausible bounds
expectation_suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="age",
        min_value=0,
        max_value=120,
        result_format={"result_format": "COMPLETE"}
    )
)

# Run validation
checkpoint = context.add_or_update_checkpoint(
    name="customer_quality_checkpoint",
    expectation_suite_name="customer_quality_suite",
    batch_request=batch_request,
)
result = checkpoint.run()

# Emit metrics to metadata store
quality_store = context.stores["quality_metrics"]
quality_store.emit(
    dataset="customers",
    timestamp=datetime.utcnow(),
    suite="customer_quality_suite",
    passed=result.success,
    metrics=result.metrics,
    failed_expectations=result.failures
)
```

## Practical Applications

### Financial Reporting Compliance

A public company must ensure its quarterly revenue figures are accurate to within a documented tolerance before the CFO certifies them to the board. A data quality framework applies multi-layered checks: completeness of all source system records (no truncated extracts), accuracy of currency conversion rates against a certified external source, timeliness of data from subsidiaries that close at different times, and uniqueness of transaction IDs (no double-counting). The framework generates a quality report alongside the financial data package — if any check fails, the report is flagged and cannot be certified until the issue is resolved.

### Machine Learning Feature Quality

An ML platform serving a credit scoring model has a data quality requirement that input features must be within 1 standard deviation of their 30-day rolling mean. A quality monitoring system runs statistical checks on each feature batch — if any feature's distribution shifts beyond the threshold (indicating potential data pipeline contamination or upstream concept drift), the system automatically quarantines the affected feature and falls back to a prior value. The model continues to serve predictions with a degraded-but-safe feature set rather than producing systematically biased scores.

### Customer Data Platform Hygiene

A marketing platform consolidates customer data from dozens of sources: CRM, e-commerce transactions, support tickets, loyalty program data, and third-party enrichment providers. Each source has different quality characteristics — the loyalty program has complete email addresses but outdated preferences; the support system has rich behavioral data but anonymized customer IDs that don't link to the CRM. A data quality framework defines minimum quality thresholds per use case (marketing emails require valid email + explicit consent; churn prediction requires behavioral history of at least 90 days), scores each customer profile against these thresholds, and automatically excludes low-quality profiles from specific campaigns to prevent wasted spend or compliance violations.

## Examples

A data quality specification YAML document:

```yaml
# Data quality specification: orders_analytics_quality_v2
dataset: analytics.orders_enriched_v2
owner: orders-platform-team
description: Enriched order data for analytics and ML consumption
quality_threshold: 99% overall pass rate required for下游 consumption

dimensions:
  completeness:
    metrics:
      - column: order_id
        required: true
        threshold: 100%
        current: 100%
      - column: customer_id
        required: true
        threshold: 99.5%
        current: 99.2%
      - column: order_total_usd
        required: true
        threshold: 99.9%
        current: 99.95%
      - column: order_date
        required: true
        threshold: 100%
        current: 100%
        
  accuracy:
    metrics:
      - column: order_total_usd
        validation: order_total_usd >= 0 AND order_total_usd < 1_000_000
        threshold: 99.99%
      - column: customer_id
        validation: foreign_key EXISTS (SELECT DISTINCT customer_id FROM dim_customers)
        threshold: 99.5%
        
  consistency:
    metrics:
      - column: status
        allowed_values: [PENDING, CONFIRMED, SHIPPED, DELIVERED, RETURNED, CANCELLED]
        threshold: 100%
      - column: currency_code
        allowed_values: ISO_4217_currency_codes
        threshold: 100%
        
  timeliness:
    metrics:
      - freshness: last_refresh_timestamp
        max_latency: 4 hours
        threshold: 99%
        current: 2.3 hours average
        
  uniqueness:
    metrics:
      - column: order_id
        validation: COUNT(DISTINCT order_id) == COUNT(*)
        threshold: 100%
        
  validity:
    metrics:
      - column: email
        pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        threshold: 99%
      - column: phone
        pattern: "^\+?[1-9]\d{1,14}$"  # E.164 format
        threshold: 95%

alerting:
  on_failure:
    severity: blocking
    notify:
      - orders-platform-team#slack
      - data-quality-oncall
    ticket: auto-create
      
  on_warning:
    severity: warning
    notify:
      - data-quality-dashboard
    ticket: daily digest

quality_trend:
  weekly_report: true
  trend_window: 30 days
  alert_on_degradation: >0.5% degradation week-over-week
```

## Related Concepts

- [[data-profiling]] — The diagnostic process that discovers quality problems
- [[data-cleansing]] — The remediation process that fixes quality problems
- [[data-governance]] — The framework that defines quality requirements and ownership
- [[data-catalog]] — The registry where quality metrics are surfaced to consumers
- [[data-lineage]] — Lineage tracking that attributes quality issues to their source
- [[data-warehouse]] — Storage layer where quality checks are commonly implemented
- [[etl]] — Pipeline context where quality is enforced at data movement points
- [[machine-learning]] — Domain where quality directly impacts model performance

## Further Reading

- "Data Quality: The Accuracy Dimension" by Thomas C. Redman — Foundational text on data quality management
- "The Chief Data Officer's Handbook" — CDO perspective on building enterprise quality programs
- DAMA International's DMBOK — Chapter 4 covers data quality management comprehensively
- Great Expectations documentation — Practical implementation guide for data quality testing
- "The Economics of Data Quality" — Industry research on ROI of data quality investment

## Personal Notes

The single most effective data quality investment I've seen wasn't a tool — it was making data quality everyone's problem rather than the data team's problem. When business stakeholders see quality metrics in their dashboards and understand how their decisions depend on reliable data, they become advocates for quality rather than passive consumers of whatever the data team delivers. The practical mechanism was a "data quality scorecard" that was embedded in weekly business reviews — showing, for each key metric in the review, the underlying data quality and any known limitations. When the VP of Sales sees that the weekly revenue number has a 2% completeness issue in one region's data, they ask the regional manager why. That organizational accountability does more than any automated cleansing tool.
