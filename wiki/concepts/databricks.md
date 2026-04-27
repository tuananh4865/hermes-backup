---
title: "Databricks"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, machine-learning, analytics, lakehouse, spark]
---

# Databricks

## Overview

Databricks is a unified analytics platform built on top of Apache Spark, designed to handle large-scale data engineering, data science, and machine learning workloads. Founded in 2013 by the original creators of Apache Spark (Matei Zaharia, Ali Ghodsi, and others), Databricks provides a collaborative environment where data teams can write code, execute notebooks, build pipelines, and deploy models—all from a single platform.

The platform is particularly known for popularizing the "lakehouse" architecture, which combines the scalability and cost-efficiency of data lakes with the reliability and ACID transaction support traditionally found in data warehouses. This convergence addresses the historical tradeoff between flexible, cheap storage (data lakes) and structured querying (data warehouses).

## Key Concepts

### Lakehouse Architecture

Databricks championed the lakehouse pattern which delivers:

- **Open Format**: Data stored in Delta Lake format (Parquet-based) accessible by any tool
- **ACID Transactions**: Consistent data operations even with concurrent access
- **Schema Enforcement**: Prevents invalid data from entering the lake
- **Time Travel**: Query historical versions of data for auditing and reprocessing
- **Unified Analytics**: Single platform for BI, ML, and streaming workloads

### Workspace and Assets

Databricks organizes work hierarchically:

- **Workspace**: Top-level container, often aligned with teams or environments
- **Folders**: Organizational units within workspace
- **Notebooks**: Interactive documents for code (Python, SQL, Scala, R)
- **Databricks Runtime**: Pre-configured compute environments with optimized libraries
- **Clusters**: Compute resources—interactive for development, job for automation

### Delta Lake

Delta Lake is the open-source storage layer that powers Databricks' lakehouse capabilities:

```python
# Example: Writing to Delta Lake with PySpark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Write data with ACID guarantees
data.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .save("/mnt/delta/customer_events")

# Time travel query - read data as of yesterday
historical_df = spark.read \
    .format("delta") \
    .option("timestampAsOf", "2026-04-12") \
    .load("/mnt/delta/customer_events")
```

## How It Works

### Compute Tiers

Databricks offers different compute options optimized for use case:

- **Interactive Clusters**: Always-on clusters for exploratory work
- **Job Clusters**: Ephemeral clusters spun up for pipeline execution
- **Serverless**: Fully managed compute (no cluster management)
- **Photon**: Native vectorized execution engine for faster SQL performance

### Unity Catalog

Unity Catalog provides centralized access control and data governance across Databricks workspaces:

- Fine-grained permissions on tables, views, and files
- Audit logging of all data access
- Data lineage tracking across pipelines
- Support for multi-cloud and cross-workspace access

## Practical Applications

Databricks is used for diverse workloads:

- **Data Engineering**: Building production ETL/ELT pipelines at scale
- **Data Science**: Collaborative model development and experimentation
- **Machine Learning**: Training, tuning, and deploying models at scale
- **Streaming Analytics**: Real-time processing with Structured Streaming
- **Business Intelligence**: Ad-hoc querying of large datasets

## Examples

A typical ML workflow on Databricks:
1. Load training data from Delta Lake
2. Use MLflow for experiment tracking
3. Train models using Spark MLlib or integrate with TensorFlow/PyTorch
4. Register best model to MLflow Model Registry
5. Deploy model for batch or real-time inference

## Related Concepts

- [[Apache Spark]] - Underlying distributed computing engine
- [[Lakehouse]] - The architecture pattern Databricks implements
- [[Delta Lake]] - Open-source storage layer
- [[MLflow]] - ML lifecycle platform, often integrated with Databricks
- [[Data Engineering]] - Field Databricks operates in

## Further Reading

- Databricks documentation (docs.databricks.com)
- Delta Lake specification (delta.io)
- Lakehouse paper by Databricks researchers (2020)

## Personal Notes

Databricks excels when data scale demands distributed processing, but it adds complexity and cost compared to simpler solutions. For small datasets, a notebook environment or even a good BI tool may suffice. The platform really shines for organizations with multiple data teams needing collaboration, governance, and production-grade reliability.
