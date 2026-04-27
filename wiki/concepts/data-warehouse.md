---
title: "Data Warehouse"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-warehouse, etl, analytics, business-intelligence, snowflake, bigquery]
---

# Data Warehouse

## Overview

A data warehouse is a large-scale electronic storage system designed to consolidate and manage data from multiple sources for analytical reporting and business intelligence. Unlike operational databases optimized for transaction processing (OLTP), data warehouses are optimized for query performance across large datasets—a pattern called Online Analytical Processing (OLAP).

The fundamental purpose of a data warehouse is to provide a single source of truth for organizational data. Business analysts, data scientists, and decision-makers can query the warehouse to understand trends, measure KPIs, generate reports, and inform strategic decisions. The warehouse integrates data from disparate operational systems—CRM, ERP, e-commerce, marketing platforms—into a unified, consistent format.

Modern data warehouses have evolved significantly. Traditional on-premise warehouses (Oracle Exadata, Teradata) have been joined by cloud-native solutions (Snowflake, BigQuery, Redshift, Databricks SQL) that offer elastic scaling, separation of compute and storage, and consumption-based pricing. This evolution has democratized access to analytical infrastructure, reducing the capital investment required to build enterprise-grade analytics.

## Key Concepts

**Star Schema**: A dimensional modeling technique with a central fact table surrounded by dimension tables. Fact tables contain measurable, quantitative metrics (sales amounts, order counts) while dimension tables describe the context (customer, product, time, location). The schema resembles a star, with the fact table at the center.

**Snowflake Schema**: An extension of star schema where dimension tables are normalized into multiple related tables, reducing data redundancy. More normalized but requires more complex joins.

**Fact Tables**: The primary tables in a data warehouse containing quantitative business metrics. Each row represents an event or transaction, and columns contain the measures and foreign keys to dimensions. Facts are typically additive (can be summed) but can also be semi-additive (account balances) or non-additive (ratios).

**Dimension Tables**: Descriptive tables that provide context for facts. They contain attributes like customer name, product category, or geographic region. Dimensions are typically denormalized for query performance and readability.

**Slowly Changing Dimensions (SCD)**: Strategies for handling attribute changes in dimension tables over time. Type 1 overwrites historical values. Type 2 maintains version history with effective date ranges. Type 3 maintains both old and new values in separate columns.

**Data Mart**: A subset of the data warehouse focused on a specific business function or department (e.g., marketing analytics, financial reporting). Data marts enable department-specific optimization and access control while drawing from the central warehouse.

## How It Works

The typical data warehouse architecture involves several stages:

1. **Data Sources**: Operational systems, external data, log files, streaming data
2. **Ingestion/ETL**: Extract data from sources, transform to warehouse format, load into tables
3. **Storage**: Managed storage (S3, Blob Storage) with metadata and indexing
4. **Compute**: Query engines that execute analytical workloads
5. **Metadata/Governance**: Schema definitions, data lineage, access controls
6. **Consumption**: BI tools, analytics notebooks, SQL clients, APIs

```sql
-- Typical star schema query joining fact and dimensions
SELECT 
    d.time_year,
    d.time_quarter,
    p.product_category,
    g.geography_region,
    SUM(f.sales_amount) as total_sales,
    COUNT(f.order_id) as order_count
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_time d ON f.time_key = d.time_key
JOIN dim_geography g ON f.geography_key = g.geography_key
WHERE d.time_year = 2025
GROUP BY d.time_year, d.time_quarter, p.product_category, g.geography_region
ORDER BY total_sales DESC;
```

Modern cloud warehouses separate storage and compute, allowing each to scale independently. You can have massive storage with minimal compute for low-frequency reporting, or burst compute for ad-hoc analysis without duplicating data.

## Practical Applications

**Business Intelligence**: Executive dashboards, operational reports, and self-service analytics querying consistent, curated datasets. Tools like Tableau, Looker, and Power BI connect directly to warehouses.

**Financial Reporting**: Revenue recognition, P&L statements, and regulatory reporting require aggregating data across products, regions, and time periods. Data warehouses provide the foundation for CFO dashboards and audit trails.

**Customer Analytics**: Unifying customer data from CRM, support tickets, and purchase history. Calculating lifetime value, churn prediction, and segmentation for targeted marketing.

**Supply Chain Optimization**: Integrating inventory, logistics, and supplier data to identify bottlenecks, optimize stock levels, and improve delivery performance.

**Product Analytics**: Tracking feature adoption, conversion funnels, and user behavior patterns. A/B test results are stored in the warehouse for statistical analysis.

## Examples

Creating a fact table in Snowflake:

```sql
CREATE TABLE fact_orders (
    order_key BIGINT IDENTITY(1,1),
    order_date_key INTEGER,
    customer_key INTEGER,
    product_key INTEGER,
    store_key INTEGER,
    order_amount DECIMAL(12,2),
    quantity INTEGER,
    discount_amount DECIMAL(12,2),
    shipped_date_key INTEGER,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE dim_customer (
    customer_key INTEGER IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE,
    customer_name VARCHAR(100),
    customer_email VARCHAR(255),
    customer_segment VARCHAR(50),
    customer_tier VARCHAR(20),
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE
);

-- SCD Type 2: Tracking customer tier changes over time
INSERT INTO dim_customer (customer_id, customer_name, customer_tier, valid_from, valid_to, is_current)
VALUES ('CUST-001', 'Acme Corp', 'Premium', '2024-01-01', '2025-06-30', FALSE);

INSERT INTO dim_customer (customer_id, customer_name, customer_tier, valid_from, valid_to, is_current)
VALUES ('CUST-001', 'Acme Corp', 'Enterprise', '2025-07-01', NULL, TRUE);
```

ETL pipeline concept (extracting from source and loading to warehouse):

```python
import pandas as pd
from sqlalchemy import create_engine

# Extract from source database
source_engine = create_engine('postgresql://source_db:5432/sales')
orders_df = pd.read_sql("""
    SELECT order_id, customer_id, product_id, 
           order_date, amount, quantity
    FROM orders 
    WHERE order_date >= '2025-01-01'
""", source_engine)

# Transform: clean, normalize, derive features
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['order_year'] = orders_df['order_date'].dt.year
orders_df['order_quarter'] = orders_df['order_date'].dt.quarter
orders_df['order_month'] = orders_df['order_date'].dt.month
orders_df['order_day_of_week'] = orders_df['order_date'].dt.day_name()

# Load to warehouse
warehouse_engine = create_engine('snowflake://warehouse.acct/user')
orders_df.to_sql('stg_orders', warehouse_engine, if_exists='replace', index=False)
```

## Related Concepts

- [[ETL]] - Extract, Transform, Load processes
- [[OLAP]] - Online Analytical Processing
- [[Snowflake]] - Cloud data warehouse platform
- [[BigQuery]] - Google's serverless data warehouse
- [[Data Lake]] - Unstructured data storage architecture
- [[Business Intelligence]] - Tools and practices for data analysis
- [[SQL]] - Query language for data warehouses

## Further Reading

- [The Data Warehouse Toolkit (Kimball)](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-toolkit/) - Definitive text on dimensional modeling
- [Snowflake Documentation](https://docs.snowflake.com/)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs/)
- [dbt (data build tool)](https://www.getdbt.com/) - Transformation framework for warehouses

## Personal Notes

The shift to cloud-native warehouses changed everything about how teams approach analytics infrastructure. I remember the days of waiting weeks for Teradata capacity planning and procurement. Now a startup can have a functioning data warehouse by end of day using Snowflake or BigQuery. The practical implication is that the bottleneck shifted from infrastructure acquisition to data modeling and pipeline development. I've seen teams rush to build warehouses without thinking through schema design, and they pay the price in query performance and maintenance headaches. The dimensional modeling principles from Ralph Kimball remain relevant despite being decades old—they solve real problems. My advice: invest in data modeling upfront. A well-designed star schema with proper surrogate keys and SCD handling will serve you for years. A poorly designed "just throw it in a flat table" approach will haunt you through every analytics request.
