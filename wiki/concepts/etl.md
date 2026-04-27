---
title: ETL
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data, etl, data-warehousing, data-engineering, batch-processing]
sources: []
---

# ETL (Extract, Transform, Load)

## Overview

ETL stands for Extract, Transform, Load — a three-phase process that moves data from source systems to a destination system, typically a data warehouse or data lake. It has been the dominant pattern for data integration and analytics for decades, and remains foundational to business intelligence, reporting, and data science workflows. The ETL process extracts data from operational source systems (databases, applications, files, APIs), transforms it into a suitable format and structure for analysis (cleaning, deduplicating, aggregating, reshaping), and loads it into a target repository where it can be queried and analyzed.

The "ETL" term became mainstream in the 1970s and 1980s as organizations began building centralized data warehouses. Bill Inmon's data warehouse theory and Ralph Kimball's dimensional modeling approaches both relied heavily on ETL processes to populate analytical models from transaction processing systems. While newer patterns like ELT (load first, then transform in the warehouse) and streaming data pipelines have emerged, ETL remains the right choice for many scenarios, particularly when data needs significant reshaping, cleansing, or when working with legacy systems that can't support complex transformations at load time.

## Key Concepts

**Extract**: The first phase retrieves raw data from source systems. Sources can be homogeneous (multiple SQL databases) or heterogeneous (a mix of databases, SaaS APIs, flat files, and third-party feeds). Extraction strategies include:

- **Full Extraction**: Pulling the entire dataset from a source, used when sources don't support incremental changes or when the dataset is small enough to extract fully
- **Incremental Extraction**: Pulling only new or changed records since the last extraction, using timestamps, sequence numbers, or change data capture (CDC) techniques
- **API Extraction**: Polling REST or GraphQL APIs for data, often with pagination handling and rate limit respect

**Transform**: The middle phase applies business logic and data quality rules to prepare data for analysis. Common transformation operations include:

- **Cleaning**: Handling null values, removing duplicates, standardizing formats (date formats, phone numbers, addresses)
- **Filtering**: Selecting only relevant records or columns, removing records that fail quality checks
- **Joining**: Combining data from multiple sources using common keys
- **Aggregating**: Rolling up detailed transactions into summary metrics (daily sales totals, monthly active users)
- **Pivoting/Unpivoting**: Reshaping data between wide (many columns) and long (many rows) formats
- **Type Conversion**: Converting strings to dates, integers to floats, or parsing JSON from text fields
- **Derived Fields**: Creating calculated columns like gross_margin = (revenue - cost) / revenue

**Load**: The final phase writes transformed data to the destination. Loading strategies include:

- **Append-Only**: Adding new records to a table, typically used for immutable event data
- **Upsert/Merge**: Insert new records and update existing ones based on a primary key
- **Full Refresh**: Truncating the target table and reloading all data from scratch
- **Slowly Changing Dimensions (SCD)**: Handling historical changes in dimension data (type 1: overwrite, type 2: add new row with effective dates)

**Staging**: Many ETL implementations use a staging area — intermediate storage between extraction and transformation. Staging enables validation before loading, rollback on failure, and auditing of what was loaded and when.

## How It Works

A typical batch ETL workflow runs on a schedule (hourly, daily, weekly) and processes data in these stages:

1. **Scheduling and Orchestration**: A scheduler (cron, Airflow, Dagster, Prefect, Oozie) triggers the ETL job at the designated time. Modern orchestration platforms provide dependency management, retry logic, alerting, and UI visibility.

2. **Connection to Sources**: The ETL tool connects to source systems using appropriate connectors (JDBC/ODBC for databases, API clients for SaaS platforms, SFTP for file transfers).

3. **Data Extraction**: Data is extracted from sources and written to staging (often cloud storage like S3 or Azure Blob). Large extracts may be partitioned and processed in parallel.

4. **Validation and Quality Checks**: Extracted data is validated against expected schemas, record counts, and value ranges. Records failing checks may be quarantined for manual review.

5. **Transformation**: Transformation logic runs against staged data. In traditional ETL tools, this is often point-and-click or SQL-based. In custom ETL pipelines, this is Python, Spark, or SQL transformation code.

6. **Data Validation**: Transformed data is validated again before loading — ensuring transformations didn't introduce errors, nulls where they shouldn't be, or row count discrepancies.

7. **Loading to Destination**: Transformed data is loaded into the data warehouse (Snowflake, BigQuery, Redshift, Databricks) or data lake.

8. **Post-Load Verification**: Row counts are verified, data types confirmed, and checksums compared between source and destination.

```python
# Python ETL example using pandas
import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def etl_daily_sales():
    """
    ETL pipeline for daily sales data.
    Extract from PostgreSQL OLTP database,
    Transform with business logic,
    Load to Snowflake data warehouse.
    """
    
    # --- EXTRACT ---
    logger.info("Extracting sales data from source database...")
    source_engine = create_engine('postgresql://user:pass@oltp-db:5432/sales')
    
    query = """
        SELECT 
            transaction_id,
            customer_id,
            product_id,
            quantity,
            unit_price,
            transaction_date,
            store_id
        FROM transactions
        WHERE transaction_date = CURRENT_DATE - INTERVAL '1 day'
    """
    
    with source_engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
    logger.info(f"Extracted {len(df)} transactions")
    
    # --- TRANSFORM ---
    logger.info("Transforming data...")
    
    # Clean nulls
    df['quantity'] = df['quantity'].fillna(0)
    df['unit_price'] = df['unit_price'].fillna(0)
    
    # Calculate derived fields
    df['total_amount'] = df['quantity'] * df['unit_price']
    
    # Add metadata
    df['etl_timestamp'] = pd.Timestamp.now()
    df['partition_date'] = df['transaction_date']
    
    # Deduplicate (if source might produce duplicates)
    df = df.drop_duplicates(subset=['transaction_id'])
    
    # --- LOAD ---
    logger.info("Loading to data warehouse...")
    warehouse_engine = create_engine(
        'snowflake://user:pass@account/warehouse/db/schema'
    )
    
    # Upsert pattern: merge into target table
    # Using Snowflake's MERGE statement for idempotent loads
    from snowflake.connector.pandas_tools import write_pandas
    
    success, nchunks, nrows, _ = write_pandas(
        warehouse_engine,
        df,
        'fact_sales',
        auto_create_table=True
    )
    
    logger.info(f"Load complete: {nrows} rows written to fact_sales")
    
    return nrows

# Orchestration with Apache Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='etl_daily_sales',
    schedule_interval='0 6 * * *',  # Daily at 6am
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    
    t1 = PythonOperator(
        task_id='extract_transform_load',
        python_callable=etl_daily_sales,
    )
    
    t1
```

## Practical Applications

**Business Intelligence Reporting**: ETL populates data warehouses that feed executive dashboards, operational reports, and ad-hoc analysis. Sales, finance, HR, and operations teams rely on daily or hourly ETL loads to have current data for decision-making.

**Data Migration**: When organizations migrate from legacy systems to modern platforms, ETL pipelines extract data from old systems, transform it to match new schemas, and load it into the replacement platform — often while both systems run in parallel.

**Regulatory Reporting**: Financial institutions use ETL to aggregate transaction data from multiple business lines into regulatory reporting formats required by bodies like the SEC, FCA, or FINRA.

**Master Data Management**: Creating a "single source of truth" customer or product record often requires ETL to combine data from CRM, ERP, and other systems, deduplicating and standardizing along the way.

**Data Science Feature Engineering**: ML pipelines often include ETL steps to extract, clean, and aggregate features from raw operational data into training-ready datasets.

## Examples

**Streaming ETL with Apache Flink** (for real-time use cases):
```java
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;

public class StreamingETL {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Source: Kafka
        KafkaSource<String> source = KafkaSource.<String>builder()
            .setBootstrapServers("kafka:9092")
            .setTopics("raw-events")
            .setGroupId("etl-processor")
            .setStartingOffsets(OffsetsInitializer.latest())
            .build();
        
        env.fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka")
            // Transform: parse, clean, enrich
            .map(new ParseAndEnrichFunction())
            .filter(event -> event.isValid())
            .keyBy(event -> event.getCustomerId())
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .reduce((a, b) -> a.merge(b))
            // Sink: to data warehouse
            .addSink(new JDBCSink());
        
        env.execute();
    }
}
```

## Related Concepts

- [[batch-processing]] — Processing data in discrete chunks rather than continuously, the traditional ETL model
- [[data-warehouse]] — The destination system optimized for analytical queries that ETL typically loads
- [[data-pipeline]] — The broader concept of data movement between systems
- [[airbyte]] — An open-source data integration platform that supports ETL patterns
- [[snowflake]] — A cloud data warehouse commonly used as an ETL destination

## Further Reading

- [The Data Warehouse Toolkit](https://www.kimballgroup.com/books/data-warehouse-toolkit/) — Ralph Kimball's classic guide to dimensional modeling and ETL
- [Apache Airflow Documentation](https://airflow.apache.org/docs/) — Popular open-source workflow orchestration platform
- [dbt (data build tool)](https://www.getdbt.com/) — Transform layer that works with modern ELT patterns
- [Snowflake ETL Best Practices](https://docs.snowflake.com/en/guides-overview) — Guide to loading data into Snowflake

## Personal Notes

ETL vs ELT vs streaming is an ongoing debate in data engineering. My takeaway: batch ETL is still the right choice for complex transformations, heavy regulatory requirements, and when source systems can't handle complex queries. ELT (loading raw data first, transforming with SQL/dbt in the warehouse) is often simpler and more flexible when your warehouse can handle the compute. Streaming (Kafka/Flink) is essential when you need sub-minute latency. The key isn't picking one paradigm — it's understanding which tool fits each specific data movement problem.
