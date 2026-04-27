---
title: Data Warehousing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, analytics, databases, business-intelligence]
---

## Overview

A data warehouse is a centralized repository that stores integrated data from multiple sources for analysis and business intelligence. Unlike operational databases optimized for transaction processing (OLTP), data warehouses are designed for query performance and analytical workloads (OLAP). They form the analytical backbone of data-driven organizations, enabling historical analysis, trend identification, and data-backed decision making across the enterprise.

Data warehousing emerged in the 1990s as businesses recognized that operational systems designed for day-to-day transactions were poorly suited for complex analytical queries. Bill Inmon's "top-down" approach and Ralph Kimball's "bottom-up" data mart approach established foundational architectural patterns that remain relevant today, though modern cloud-native architectures have introduced new variations.

## Key Concepts

### Extract, Transform, Load (ETL)

ETL is the process of moving data from source systems into the data warehouse. **Extract** retrieves data from source databases, applications, and files. **Transform** converts, cleans, and standardizes the data according to warehouse schema requirements. **Load** inserts the transformed data into warehouse tables. Modern alternatives include ELT (Extract, Load, Transform), which leverages cloud data warehouse compute for transformations.

### Star and Snowflake Schemas

Data warehouses use dimensional modeling to organize data for intuitive querying. The **star schema** centers around a fact table (containing quantitative business metrics) surrounded by dimension tables (containing descriptive attributes). The **snowflake schema** normalizes dimension tables into related sub-tables, reducing data redundancy at the cost of query complexity.

### Data Lake vs Data Warehouse

While data warehouses store structured data processed for specific analytical purposes, **data lakes** store raw data in its native format—from structured database exports to semi-structured logs to unstructured text. Modern architectures often combine both, using data lakes for data exploration and machine learning, and data warehouses for structured reporting and BI.

## How It Works

Data flows into a warehouse through scheduled batch jobs or real-time streams. The incoming data passes through data quality checks and validation rules before being loaded into staging tables. From there, transformation logic aggregates, joins, and reformats data into the warehouse's dimensional structure.

**Slowly Changing Dimensions (SCD)** handle historical changes to dimension data. When a customer moves to a new city, SCD strategies determine whether to overwrite the old value, create a new dimension record, or maintain both with effective date ranges.

**Partitioning** divides large fact tables into smaller, manageable segments (by date, region, or other criteria) enabling parallel processing and faster queries. **Clustering** organizes data within partitions based on frequently queried columns.

**Materialized views** pre-compute and store query results for instant retrieval, accelerating common analytical queries while using additional storage.

Modern cloud data warehouses like Snowflake, BigQuery, and Redshift offer automatic scaling, separation of storage and compute, and managed infrastructure. This enables organizations to scale analytical workloads dynamically without managing hardware.

## Practical Applications

Business intelligence platforms connect to data warehouses to generate executive dashboards, operational reports, and ad-hoc analytical queries. Marketing teams analyze campaign performance by joining clickstream data with sales outcomes. Financial analysts build forecasting models using historical transaction patterns.

Data teams use warehouses as the foundation for data marts—purpose-specific subsets optimized for particular business functions. A customer analytics mart might contain denormalized customer, order, and interaction data for the customer success team, while a financial mart aggregates revenue, costs, and forecasts for finance.

## Examples

A simple star schema for an e-commerce analytics warehouse:

```sql
-- Fact table: sales transactions
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    store_id INT,
    date_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

-- Dimension table: products
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    brand VARCHAR(100)
);

-- Query: total sales by category
SELECT 
    p.category,
    SUM(f.total_amount) as revenue
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category;
```

## Related Concepts

- [[ETL]] - Data integration processes for warehouse population
- [[analytics]] - Analytical workloads data warehouses enable
- [[NoSQL]] - Alternative database patterns for different use cases
- [[relational-database]] - Transactional systems that feed warehouses
- [[real-time-analytics]] - Modern streaming-based analytics patterns
- [[data-visualization]] - Visual representation of warehouse data

## Further Reading

- "The Data Warehouse Toolkit" by Ralph Kimball - Definitive guide to dimensional modeling
- "Building the Data Warehouse" by Bill Inmon - Top-down architectural approach
- Snowflake Documentation - Cloud data warehouse patterns

## Personal Notes

Data warehousing taught me that data value increases over time when properly organized and preserved. The investment in clean, well-structured historical data pays dividends for years. When designing warehouse schemas, I always start with the questions stakeholders need answered rather than trying to mirror source systems—denormalization is a feature, not a bug.
