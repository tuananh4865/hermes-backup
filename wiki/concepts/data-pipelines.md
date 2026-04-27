---
title: Data Pipelines
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, data-pipelines, etl, elt, data-warehousing, workflow-orchestration]
sources: []
---

# Data Pipelines

## Overview

A data pipeline is a series of processes that move data from one system to another, transforming and processing it along the way. Unlike a simple data transfer, a pipeline implies multiple stages of extraction, transformation, loading, and validation — often connecting multiple source systems to multiple destinations. Data pipelines form the circulatory system of modern data infrastructure, feeding analytics platforms, machine learning systems, and operational applications with the data they need to function.

Data pipelines can be categorized by their processing model: [[batch-processing]] handles data in discrete chunks at scheduled intervals, [[stream-processing]] handles data continuously as it arrives, and hybrid approaches combine both patterns. The choice of processing model determines everything from latency characteristics to infrastructure requirements to operational complexity.

Modern data pipelines are rarely simple point-to-point connections. They often involve multiple stages, branching flows, and fan-out patterns where one source feeds multiple destinations. Orchestration frameworks like [[apache-airflow]], Prefect, and Dagster manage these complex dependency graphs, handling scheduling, retries, monitoring, and alerting. The pipeline definition itself has become code — version-controlled, testable, and deployable through CI/CD.

The maturity of data pipeline infrastructure has enabled the modern data stack: a collection of specialized tools that each handle a specific part of the data lifecycle. This composability reduces the need for monolithic, hand-built data systems while raising new challenges around data quality, lineage, and governance.

## Key Concepts

**Data Sources**: Pipelines begin with one or more data sources — operational databases (PostgreSQL, MySQL, Oracle), SaaS applications (Salesforce, HubSpot, Stripe), event streams (Kafka, Kinesis), flat files (CSV, JSON, Parquet on S3), or APIs (REST, GraphQL). Each source type requires different extraction strategies and connector technology.

**Data Sinks/Destinations**: Processed data flows to destinations including data warehouses (Snowflake, BigQuery, Redshift), data lakes (S3, Azure Data Lake, GCS), analytics platforms (Tableau, Looker, Mode), operational databases, or event-driven systems. The destination's capabilities often influence pipeline design decisions.

**Transformation**: The processing logic between source and destination. Transformations can be SQL-based (SELECT, JOIN, aggregate), programmatic (Python, Spark), or use specialized tools (dbt for warehouse transformations). Common operations include filtering, deduplication, schema mapping, type conversion, aggregation, and enrichment with reference data.

**Data Quality**: Ensuring data is accurate, complete, and reliable. Quality checks validate schema conformance, value ranges, referential integrity, and uniqueness. Bad data is either rejected (with alerting) or routed to a quarantine area for investigation. SLA expectations for data quality typically align with downstream analytical or operational requirements.

**Data Freshness/Latency**: How quickly data arrives at the destination determines whether a pipeline uses batch or streaming architecture. Batch pipelines may have latency measured in hours; streaming pipelines measure latency in seconds or milliseconds. Latency requirements drive infrastructure complexity and cost.

**Idempotency**: A critical property where running the same pipeline multiple times with the same inputs produces the same outputs. Idempotent pipelines can be safely retried after failure without creating duplicate data or inconsistent state. Achieving idempotency typically requires careful use of primary keys, upsert patterns, or snapshot-based loading.

**Lineage**: Tracking data as it flows through the pipeline — understanding what source data contributed to what output, what transformations were applied, and what downstream systems consume the data. Lineage is essential for debugging, auditing, and impact analysis when source systems change.

## How It Works

A well-designed data pipeline follows a consistent architectural pattern:

```
[Source System] --> [Extract] --> [Stage/Raw] --> [Transform] --> [Validate] --> [Load] --> [Destination]
                        |              |              |              |           |
                        v              v              v              v           v
                    [Logging]     [Audit Log]   [Metrics]    [Quality Check] [Row Count]
```

**Stage 1 — Extraction**: Connect to source systems and retrieve data. Extraction can be full (complete snapshot) or incremental (only new or changed records). Incremental extraction uses timestamps, sequence numbers, or change data capture (CDC) to identify what to extract. Extractors must handle source system limitations — rate limits, pagination, connection pooling.

**Stage 2 — Staging/Raw Storage**: Write extracted data to intermediate storage. This raw layer preserves original data before any transformation, enabling reprocessing if transformation logic changes. Cloud storage (S3, GCS, Azure Blob) or distributed file systems are typical staging locations.

**Stage 3 — Transformation**: Apply business logic and data quality rules. This may happen in the pipeline itself (Spark, Python, SQL) or in a transformation layer like dbt that runs within the warehouse. Transformations must be carefully designed for correctness, performance, and restartability.

**Stage 4 — Validation**: Verify transformed data meets quality expectations. Checks include row counts (did we lose records?), value ranges (are all amounts positive?), uniqueness (are keys truly unique?), and referential integrity (do foreign keys exist?). Validation failures should block loading and trigger alerts.

**Stage 5 — Loading**: Write validated data to destination. Loading patterns include append-only (for immutable events), upsert (insert or update based on key), or full refresh (truncate and reload). The pattern depends on the destination schema and consumption pattern.

**Stage 6 — Monitoring**: Track pipeline execution — run duration, record counts, error rates, resource utilization. Monitoring enables alerting on failures and provides data for SLA reporting.

```python
# Python data pipeline example using Apache Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Define the DAG
with DAG(
    dag_id='sales_data_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    doc_md=__doc__
) as dag:
    
    # Extract: Pull data from source database
    extract_sales = PythonOperator(
        task_id='extract_sales',
        python_callable=lambda: extract_to_staging(
            query="""
                SELECT order_id, customer_id, product_id, 
                       quantity, unit_price, order_date
                FROM orders 
                WHERE order_date = '{{ ds }}'
            """,
            output_path='/tmp/staging/sales_{{ ds }}.parquet'
        )
    )
    
    # Load: Load staging data to warehouse
    load_sales = PythonOperator(
        task_id='load_sales_to_warehouse',
        python_callable=lambda: load_parquet_to_snowflake(
            input_path='/tmp/staging/sales_{{ ds }}.parquet',
            table='fact_sales',
            schema='analytics'
        )
    )
    
    # Validate: Run data quality checks
    validate_sales = PostgresOperator(
        task_id='validate_sales_data',
        postgres_conn_id='warehouse',
        sql="""
            SELECT COUNT(*) AS row_count,
                   COUNT(DISTINCT customer_id) AS unique_customers,
                   SUM(quantity * unit_price) AS total_revenue
            FROM analytics.fact_sales
            WHERE partition_date = '{{ ds }}';
        """
    )
    
    # Set dependencies
    extract_sales >> load_sales >> validate_sales
```

## Practical Applications

**Analytics Infrastructure**: The most common use case. Pipelines feed data from operational systems (CRM, ERP, e-commerce) into analytical stores (data warehouses, BI platforms). Marketing teams use pipeline data for campaign analytics. Finance teams use it for financial reporting. Product teams use it for user behavior analysis.

**Machine Learning**: ML workflows depend on pipelines to prepare training data. Raw features are extracted, transformed (normalized, encoded, aggregated), and loaded into feature stores. Model training pipelines consume these features. Inference pipelines apply models to new data in production.

**Data Migration**: When organizations migrate from legacy systems, pipelines extract data from old platforms, apply migration logic, and load into new systems — often while running both systems in parallel to validate correctness.

**Operational Analytics**: Real-time dashboards for operations teams showing current inventory levels, fulfillment rates, or customer support metrics. These pipelines often combine batch and streaming patterns.

**Regulatory Reporting**: Financial institutions build pipelines to aggregate data across business units into regulatory reporting formats. These pipelines must maintain strict data lineage and audit trails.

**Data mesh architectures**: In decentralized data mesh organizations, domain teams own their own data products, which are formalized as pipelines that publish data for consumption by other domains.

## Examples

**Fivetran Pipeline (Managed ELT)**:

Fivetran handles extraction and loading, with dbt handling transformation:

```
[MySQL] ──> [Fivetran Connector] ──> [Snowflake Raw] ──> [dbt] ──> [Looker]
              (CDC-based Extract)       (Load raw)        (Transform)
```

Fivetran's connectors continuously replicate data to Snowflake. dbt models transform the raw data through staging and intermediate layers into analytics-ready tables.

**Apache Kafka + Flink Streaming Pipeline**:

```java
// Flink streaming job consuming from Kafka, transforming, writing to data warehouse
DataStream<String> rawEvents = env
    .addSource(new FlinkKafkaConsumer<>("user-events", new SimpleStringSchema(), props));

DataStream<UserEvent> parsed = rawEvents
    .map(JSON::parseObject)
    .filter(e -> e.isValid())
    .keyBy(UserEvent::getUserId);

DataStream<SessionAggregate> sessions = parsed
    .window(SlidingEventTimeWindows.of(Time.minutes(5), Time.minutes(1)))
    .aggregate(new SessionAggregator());

sessions.addSink(
    new JdbcSinkBuilder<SessionAggregate>()
        .withUrl("jdbc:snowflake:...")
        .withInsertStatement("INSERT INTO user_sessions VALUES (?,?,?)")
        .build()
);
```

## Related Concepts

- [[etl]] — Extract, Transform, Load — the classic pipeline pattern
- [[elt]] — Extract, Load, Transform — modern cloud-native variant
- [[batch-processing]] — Processing data in scheduled batches
- [[stream-processing]] — Processing data continuously in real-time
- [[data-warehouse]] — Common destination for analytical pipelines
- [[apache-airflow]] — Popular workflow orchestration for pipelines
- [[dbt]] — Transformation layer commonly used in ELT pipelines
- [[kafka]] — Distributed event streaming platform
- [[data-quality]] — Ensuring pipeline data meets quality standards

## Further Reading

- [Apache Airflow Documentation](https://airflow.apache.org/docs/) — Official Airflow docs
- [Prefect Documentation](https://docs.prefect.io/) — Modern Python-based orchestration
- [dbt (data build tool)](https://www.getdbt.com/) — SQL-based transformation
- [The Data Engineering Cookbook](https://github.com/adamereng/data-engineering-book) — Practical pipeline design
- [Streaming Systems](https://www.oreilly.com/library/view/streaming-systems/9781491983864/) — Deep dive on streaming pipeline design

## Personal Notes

The hardest part of building data pipelines isn't the technical implementation — it's defining the business logic correctly. I see teams spend weeks building pipelines that extract and load perfectly, then discover the transformation logic was wrong because they never validated assumptions with business users.

Idempotency is the property I wish every data engineer internalized early. Every pipeline will fail at some point. An idempotent pipeline can be re-run safely; a non-idempotent one creates duplicate data, inconsistent state, and debugging nightmares. The marginal effort to add idempotency (using upserts, snapshot tables, or deterministic keys) is always worth it.

Monitoring without alerting is useless. A pipeline that logs errors but doesn't page anyone when it fails isn't really monitored. Build alerting into your pipelines from day one, and make sure alerts go to people who can actually fix the problem.
