---
title: "Etl Processes"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, data-processing, pipelines, analytics, integration]
---

# ETL Processes

## Overview

ETL (Extract, Transform, Load) is a data integration paradigm that moves data from source systems into a destination data warehouse or data lake for analysis, reporting, and downstream consumption. The three stages are: **Extract** (reading data from source systems), **Transform** (cleaning, filtering, enriching, and reshaping data), and **Load** (writing data to the destination). ETL processes have been the backbone of data warehousing since the 1970s and remain essential for organizations seeking to unify disparate data sources into coherent analytical assets.

Traditional ETL was designed for batch processing—collecting data over hours or days, processing it in nightly or weekly batches, and loading it into data warehouses for business intelligence. This approach worked when data volumes were manageable and analytical needs were predictable. However, the exponential growth of data and the demand for real-time analytics have driven evolution toward stream processing and ELT (Extract, Load, Transform) patterns that shift transformation to the destination platform using powerful query engines like Snowflake or BigQuery.

Modern data stacks often distinguish between "old-school ETL" and contemporary approaches like data pipelines, data flow processing, and event streaming architectures. Regardless of terminology, the fundamental operations—extracting data from sources, applying business logic, and loading results—remain core to data integration. Understanding ETL provides the foundation for designing any data movement architecture.

## Key Concepts

Mastering ETL requires understanding several technical concepts that determine how data integration pipelines are designed, implemented, and operated.

**Change Data Capture (CDC)** is a technique for efficiently extracting only changed data from source systems rather than performing full extractions. CDC methods include timestamp-based polling (watching for updated_at timestamps), log-based CDC (reading transaction logs, used by tools like Debezium), and trigger-based CDC (database triggers record changes to shadow tables). CDC dramatically reduces source system load and pipeline latency compared to full table scans.

**Slowly Changing Dimensions (SCD)** handle reference data that changes over time in ways that matter analytically. Type 1 SCD overwrites old values (no history). Type 2 SCD adds new rows with effective date ranges, preserving complete history. Type 6 SCD (hybrid) combines previous approaches. Dimension tables in data warehouses typically implement Type 2 SCD to support historical analysis—understanding what product prices were, or which customer addresses were valid, at any point in time.

**Idempotency** ensures pipeline runs produce consistent results regardless of repetition. An idempotent operation can be safely retried—if a pipeline step fails mid-execution and is rerun, it produces the same final state as if it had succeeded the first time. Achieving idempotency typically requires deterministic operations, upsert semantics (INSERT UPDATE), or delete-then-reload patterns. Idempotency is essential for reliable, observable data pipelines.

**Schema Evolution** addresses the challenge of changing data structures over time. Sources may add columns, rename fields, or change data types. Destination schemas must accommodate these changes without breaking downstream consumers. Strategies include adding columns with defaults, using variant/JSON columns for flexible schema, versioned schemas, and backward-compatible changes. Schema registries provide centralized schema management and validation.

## How It Works

A typical ETL pipeline orchestrates data movement through a sequence of stages, with each stage handling specific aspects of the integration workflow.

**Extraction Phase** connects to source systems and retrieves data. Sources might be transactional databases (Oracle, PostgreSQL, MySQL), SaaS applications (Salesforce, SAP, Workday), files (CSV, Parquet, JSON on S3/GCS), or streaming sources (Kafka, Kinesis). Connection methods include JDBC/ODBC for databases, API calls for SaaS platforms, and file protocols for storage systems. Extraction strategies range from full table extracts to incremental pulls based on timestamps or cursor positions to CDC from transaction logs.

**Staging and Validation** often occurs between extraction and transformation. Raw data lands in a staging area (schema or separate database) in its original form before transformation. This staging enables debugging (inspecting what was actually extracted), reprocessing (rerunning transformations from raw data), and auditing (proving what data existed at extraction time). Validation checks might include schema verification, null checks, and referential integrity confirmation.

**Transformation Phase** applies business logic to raw data. Common transformations include:

- **Data Cleansing**: Removing duplicates, standardizing formats, handling nulls
- **Filtering**: Selecting relevant rows based on criteria
- **Enrichment**: Joining with reference data, lookup tables, or external sources
- **Aggregation**: Summarizing transactions into daily, weekly, or monthly metrics
- **Pivoting/Unpivoting**: Reshaping data between wide and long formats
- **Type Conversion**: Converting strings to dates, integers to floats, etc.

Transformation can occur in-memory (using tools like dbt, Spark, or Pandas), in-database (using SQL), or through code-based frameworks. The ELT pattern loads raw data first then transforms within the destination platform using its native compute.

**Load Phase** writes transformed data to the destination. Load strategies include:

- **Full Load**: Truncate and reload entire tables—simple but expensive for large tables
- **Incremental Load**: Append new records and update changed records based on keys
- **Upsert**: Insert new records, update existing records based on primary key conflicts
- **History Preservation**: Maintain SCD Type 2 with effective dates

**Error Handling and Recovery** must address various failure modes: source system unavailability, network interruptions, transformation errors, constraint violations, and destination system issues. Robust pipelines implement retry logic, dead letter queues for malformed records, and checkpoint/restart capability to resume from failure points rather than restart entirely.

## Practical Applications

ETL processes underpin data-driven organizations across virtually every industry, enabling analytics, reporting, machine learning, and operational data sharing.

**Business Intelligence and Reporting** relies on ETL to consolidate data from operational systems (CRM, ERP, e-commerce platforms) into data warehouses. A typical business intelligence ETL pipeline might extract sales transactions from an e-commerce platform, customer records from Salesforce, and inventory levels from SAP, then transform and load them into a unified schema enabling cross-functional reporting on revenue, customer acquisition, and stock levels.

**Data Warehousing** for analytics uses star or snowflake schema designs where fact tables record business events (sales, orders, shipments) and dimension tables provide descriptive context (customers, products, time, geography). ETL pipelines must correctly dimension fact records with appropriate dimension keys, handle SCD changes in dimensions, and maintain referential integrity across the schema.

**Regulatory Reporting and Compliance** in financial services, healthcare, and other regulated industries requires accurate, auditable data pipelines. ETL processes must maintain complete lineage—tracking data from source to destination—and support reconciliation against source systems. SOX, HIPAA, GDPR, and MiFID II compliance often mandate specific data handling, retention, and audit trail requirements that ETL pipelines must enforce.

**Machine Learning Feature Engineering** increasingly uses ETL patterns to prepare training datasets. Data engineers build pipelines that extract raw events, transform them into ML features (aggregating user behavior, calculating ratios, encoding categoricals), and load features into feature stores for model training and inference. Modern ML platforms often use streaming ETL (using Kafka Streams, Apache Flink) to compute features in real-time.

## Examples

A Python ETL pipeline using Pandas for transformation:

```python
import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_orders(db_connection):
    """Extract orders from transactional database"""
    query = """
        SELECT order_id, customer_id, product_id, 
               quantity, unit_price, order_date
        FROM orders
        WHERE order_date >= '2024-01-01'
    """
    return pd.read_sql(query, db_connection)

def transform_orders(orders_df):
    """Transform orders into analytical format"""
    # Calculate total amount
    orders_df['total_amount'] = orders_df['quantity'] * orders_df['unit_price']
    
    # Clean customer_id
    orders_df['customer_id'] = orders_df['customer_id'].str.strip().str.upper()
    
    # Convert order_date to date type
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
    
    # Calculate derived fields
    orders_df['order_year'] = orders_df['order_date'].dt.year
    orders_df['order_month'] = orders_df['order_date'].dt.month
    orders_df['order_quarter'] = orders_df['order_date'].dt.quarter
    
    return orders_df

def load_to_warehouse(orders_df, warehouse_connection):
    """Load to data warehouse with upsert logic"""
    # Create staging table
    orders_df.to_sql('orders_staging', warehouse_connection, 
                     if_exists='replace', index=False)
    
    # Upsert into main table
    upsert_sql = """
        MERGE INTO orders_target t
        USING orders_staging s
        ON t.order_id = s.order_id
        WHEN MATCHED THEN UPDATE SET
            quantity = s.quantity,
            unit_price = s.unit_price,
            total_amount = s.total_amount
        WHEN NOT MATCHED THEN INSERT
            (order_id, customer_id, product_id, quantity, 
             unit_price, total_amount, order_date, 
             order_year, order_month, order_quarter)
        VALUES
            (s.order_id, s.customer_id, s.product_id, s.quantity,
             s.unit_price, s.total_amount, s.order_date,
             s.order_year, s.order_month, s.order_quarter)
    """
    
    with warehouse_connection.cursor() as cursor:
        cursor.execute(upsert_sql)
    warehouse_connection.commit()

def run_etl_pipeline():
    """Execute full ETL pipeline with error handling"""
    try:
        src_db = create_engine('postgresql://source:password@src-db:5432/orders')
        dest_db = create_engine('postgresql://warehouse:password@dest-db:5432/analytics')
        
        logger.info("Extracting orders from source...")
        raw_orders = extract_orders(src_db)
        logger.info(f"Extracted {len(raw_orders)} orders")
        
        logger.info("Transforming orders...")
        transformed = transform_orders(raw_orders)
        logger.info(f"Transformed {len(transformed)} records")
        
        logger.info("Loading to warehouse...")
        load_to_warehouse(transformed, dest_db)
        logger.info("ETL pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_etl_pipeline()
```

## Related Concepts

- [[data-warehouse]] — Analytical data storage systems
- [[data-pipelines]] — Automated data movement and processing
- [[data-engineering]] — Discipline of building data infrastructure
- [[change-data-capture]] — Efficient incremental data extraction
- [[data-quality]] — Ensuring data meets accuracy and completeness standards
- [[data-modeling]] — Designing data structures for analytical use

## Further Reading

- "The Data Warehouse Toolkit" by Ralph Kimball — Classic data warehousing principles
- "Fundamentals of Data Engineering" by Joe Reis — Modern data engineering practices
- Apache Airflow Documentation — Popular workflow orchestration platform
- dbt (data build tool) — SQL-based transformation framework
- "Streaming Systems" by Tyler Akidau et al. — Stream processing concepts

## Personal Notes

ETL taught me that data integration is never "done"—it's an ongoing operational concern requiring monitoring, alerting, and documentation. Early in my data career, I underestimated the complexity of production ETL: handling schema changes, managing failing sources, debugging data quality issues at 2 AM. My key lessons: invest heavily in data observability from day one, make pipeline failures visible and actionable, and treat data quality tests as first-class citizens alongside unit tests for application code. The best ETL pipelines are boring—they run reliably, fail loudly when they don't, and produce trustworthy data.
