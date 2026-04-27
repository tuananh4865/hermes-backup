---
title: Data Lineage
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-lineage, data-governance, data-traceability, pipeline-analysis, impact-analysis]
---

# Data Lineage

## Overview

Data Lineage is the practice of tracking the complete lifecycle and movement of data as it flows through an organization's systems — from original sources through transformation pipelines, intermediate processing steps, and final destinations such as reports, dashboards, and ML models. It answers the fundamental question: "Where did this data come from, and what happened to it along the way?" Data lineage is a cornerstone of [[data-governance]], enabling impact analysis, regulatory compliance, error debugging, and trust establishment in analytical systems.

Lineage can be captured at multiple granularities. **System-level lineage** shows which systems exchange data (e.g., "the Salesforce CRM feeds into the customer data platform, which feeds into the Snowflake data warehouse"). **Process-level lineage** drills into the transformation logic within a pipeline (e.g., "dbt model `stg_orders__enriched` joins `raw_orders` with `raw_customers` to produce the enriched output"). **Column-level lineage** tracks the derivation path of individual fields (e.g., "the `lifetime_value` column in `customer_features` is computed from `SUM(order_total)` divided by `COUNT(DISTINCT orders)` in the orders source").

Without lineage, data teams operate in a fog of unknown dependencies — pipeline failures cause cascading downstream breakage with no clear root cause, schema changes silently corrupt outputs, and compliance auditors cannot reconstruct how a specific number in a regulatory report was derived.

## Key Concepts

### Lineage Graph Structure

Data lineage is naturally represented as a directed acyclic graph (DAG), where nodes represent data assets (tables, files, streams, columns, reports) and edges represent transformation or propagation relationships. In a typical ETL pipeline:

```
raw_orders (source) 
    -> staging_orders_cleaned (dbt staging model)
    -> dim_orders (dbt dimension model)
    -> orders_revenue_analytics (reporting table)
    -> Executive Revenue Dashboard (BI report)
```

Each edge carries metadata about the transformation: the SQL or logic used, the execution timestamp, the data volume processed, and any business rules applied. Column-level edges extend this to show which output columns derive from which input columns.

### Capture Methods

Lineage can be captured through several mechanisms, each with trade-offs:

**Query parsing** instruments SQL queries to extract source-table to target-table relationships. Tools like Apache Calcite, dbt's lineage generation, and SQL parsing libraries (sqlgloss, moz-sql-parser) can extract lineage from SELECT ... INSERT statements. This approach works well for SQL-based pipelines but cannot capture non-SQL transformations (Python UDFs, binary formats, streaming joins).

**Execution tracing** instruments pipeline execution engines (Airflow, Spark, Flink) to record which tasks read from which inputs and wrote to which outputs during each execution. Modern observability platforms (Datadog, Honeycomb, OpenTelemetry) can be extended to emit lineage events alongside performance metrics.

**Schema matching** infers lineage by comparing table and column names across systems, using naming conventions and fuzzy matching to guess relationships. This is error-prone but useful for "dark data" — systems without instrumentation — and initial bootstrap of lineage graphs.

**Event-level lineage** uses structured event logs from message bus systems (Kafka, Pulsar) to track record-level provenance. Each record carries provenance metadata (source system, event time, processing steps) that accumulates as it moves through stream processing stages.

### Use Cases

Lineage serves multiple critical business functions:

**Impact analysis** ("what breaks if I change this?") is essential before modifying production data assets. A data engineer changing a column's data type in a source table needs to know which downstream tables, reports, and models will be affected — and which ones are business-critical. Without lineage, this requires manual investigation across dozens of systems.

**Root cause analysis** ("where did this bad data come from?") dramatically accelerates incident response. When a dashboard shows anomalous numbers, lineage enables investigators to trace the data flow backward from the symptom to the source of corruption.

**Regulatory compliance** (GDPR, SOX, BCBS 239) often requires organizations to explain how specific data points in reports were derived and to reproduce the exact transformations applied. Lineage provides the audit trail that makes this tractable.

**Data quality attribution** helps isolate which upstream pipeline stage introduced a quality problem, enabling the right team to be notified and the issue to be remediated at its source.

## How It Works

In a modern data platform, lineage collection happens at multiple integration points:

**Pipeline Orchestration Layer**: Workflow schedulers like Airflow, Prefect, or Dagster emit lineage events as tasks execute. These events include task inputs, outputs, execution metadata, and for SQL-based tasks, the parsed query structure.

**Transformation Layer**: dbt automatically generates column-level lineage from the DAG of ref() calls — when model A references model B via `ref('B')`, an edge is created. Custom lineage can be added using dbt's meta object or hooks. For Spark, lineage can be extracted from query plans via the Catalyst optimizer.

**Query Engines and Warehouses**: Cloud data warehouses like Snowflake, BigQuery, and Redshift can log query execution graphs that reveal which base tables contributed to which query results. Some organizations enable query logging and post-process these logs to build warehouse-internal lineage graphs.

**Stream Processing**: Apache Flink and Kafka Streams can propagate lineage context as part of record headers. When a Flink job processes a Kafka record, it can annotate the output record with the processing step's identity, enabling end-to-end event-level lineage.

**Catalog Integration**: Lineage graphs are typically stored in or indexed by a [[data-catalog]], where they are surfaced alongside asset metadata during discovery, impact analysis, and compliance workflows.

```python
# Example: Emitting lineage events from a Python pipeline using OpenLineage
from openlineage import Client
from openlineage.common.models import (
    Dataset, Job, Run, RunEvent, RunState
)
from datetime import datetime

client = Client(openlineage_url="https://ol-api.acme.corp")

# Define the input dataset (source table)
input_dataset = Dataset(
    namespace="snowflake",
    name="PROD.RAW.orders",
    facets={}
)

# Define the output dataset (target table)
output_dataset = Dataset(
    namespace="snowflake", 
    name="PROD.ANALYTICS.daily_order_summaries",
    facets={}
)

# Define the job that performed the transformation
job = Job(
    namespace="airflow",
    name="daily_order_summary_dag.compute_summary"
)

# Emit the completion event with lineage
run = Run(runId="run-12345")
client.emit(
    event=RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=datetime.utcnow(),
        run=run,
        job=job,
        inputs=[input_dataset],
        outputs=[output_dataset],
    )
)
```

## Practical Applications

### Regulatory Reporting in Banking

A global investment bank must produce daily liquidity risk reports under Basel III regulations. Regulators can request the exact derivation of any number in the report. The bank's data platform uses column-level lineage from all trading systems through risk calculation models to the regulatory report output. When a regulator asks "how did we arrive at this liquidity coverage ratio for this specific derivative position?", analysts can trace the exact calculation path — position data from the trading system, market data from Bloomberg, pricing model outputs, aggregation logic — in minutes rather than days.

### ML Model Debugging

A recommendation engine's accuracy degrades unexpectedly. Data scientists use column-level lineage to trace the model's input features back to source tables. They discover that a recent schema change in the `customer_product_interactions` source table altered the feature computation, causing a silent degradation. The lineage graph identifies the specific upstream change and the affected feature pipeline, enabling rapid remediation.

### ETL Pipeline Refactoring

A data engineering team needs to rewrite a legacy Spark pipeline that has been in production for five years with minimal documentation. Column-level lineage shows which output columns came from which input columns, which transformations were applied, and which downstream consumers depend on which outputs. This enables the team to refactor the pipeline incrementally, running新旧 versions in parallel and comparing outputs to validate correctness before cutover.

## Examples

A lineage graph in YAML format:

```yaml
# Lineage manifest for the orders-enriched data product
lineage_graph:
  direction: upstream_to_downstream
  
  nodes:
    - id: raw_orders
      type: source_table
      location: orders_db.primary.orders
      owner: orders-platform-team
      platform: postgresql
      
    - id: raw_customers
      type: source_table
      location: crm_db.primary.customers
      owner: crm-team
      platform: salesforce
      
    - id: stg_orders__cleaned
      type: transformation
      platform: dbt
      model: stg_orders__cleaned.sql
      description: Cleans raw orders - removes test accounts, standardizes status values
      
    - id: dim_customers__enriched
      type: transformation
      platform: dbt
      model: dim_customers__enriched.sql
      description: Join customers with geographic and demographic attributes
      
    - id: fact_orders__enriched
      type: transformation
      platform: dbt
      model: fact_orders__enriched.sql
      description: Enriched order facts with customer attributes and computed metrics
      
    - id: customer_revenue_ml_features
      type: ml_feature_table
      location: feature_store.customer_revenue_v2
      owner: ml-platform-team
      
  edges:
    - from: raw_orders
      to: stg_orders__cleaned
      columns: ["order_id", "customer_id", "order_date", "total_amount", "status"]
      
    - from: raw_customers
      to: dim_customers__enriched
      columns: ["customer_id", "name", "email", "region", "signup_date"]
      
    - from: stg_orders__cleaned
      to: fact_orders__enriched
      columns: ["order_id", "customer_id", "order_date", "total_amount", "status"]
      
    - from: dim_customers__enriched
      to: fact_orders__enriched
      columns: ["customer_id", "region", "customer_segment"]
      
    - from: fact_orders__enriched
      to: customer_revenue_ml_features
      columns: ["customer_id", "lifetime_value", "avg_order_value", "order_count"]
      
  downstream_consumers:
    - name: Customer Churn Model
      type: ml_model
      input_features: ["customer_id", "lifetime_value", "avg_order_value", "order_count"]
      
    - name: Weekly Revenue Dashboard
      type: bi_report
      metrics: ["revenue", "order_count", "avg_order_value"]
```

## Related Concepts

- [[data-governance]] — Governance discipline where lineage is a core capability
- [[data-catalog]] — Platform that often stores and surfaces lineage information
- [[data-quality]] — Quality monitoring that uses lineage to attribute issues to upstream sources
- [[data-warehouse]] — Analytical store where lineage typically terminates for reporting workloads
- [[apache-spark]] — Execution engine whose query plans can be parsed for lineage
- [[apache-flink]] — Stream processing engine that supports event-level lineage
- [[dbt]] — Transformation tool with built-in lineage generation
- [[access-control]] — Security layer often paired with lineage for compliance auditing

## Further Reading

- "Lineage-Driven Data Quality" — Apache Atlas documentation on lineage-based quality attribution
- "DataOps: The What, Why, and How" — Covers lineage as part of DataOps observability
- "The Data Engineering Lifecycle" — James Denny's framework for understanding data flow architectures
- OpenLineage project — Open standard for lineage event collection

## Personal Notes

The most valuable lineage investment I've seen was column-level lineage integrated into a BI tool's ad-hoc query interface. When a business user sees a number in a report and clicks "show lineage," they get a visual graph of every transformation from source to this cell — not just table-level, but which specific column, which SQL expression, and which pipeline job. This transforms data literacy from "trust the data team" to "understand the data yourself." The key to making this sustainable is making lineage capture automatic — built into pipeline execution rather than requiring manual annotation. Every manual step in lineage maintenance is a step toward staleness.
