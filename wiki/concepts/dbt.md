---
title: "Dbt"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, analytics, sql, transformation, data-warehouse]
---

# dbt (data build tool)

## Overview

dbt (data build tool) is an open-source transformation framework that enables data analysts and engineers to transform, shape, and validate data within a data warehouse. Pronounced "dee-bee-tee" or sometimes just "dbt," the tool has become a foundational component of the modern data stack. Unlike traditional ETL tools that focus on extracting and loading data, dbt focuses specifically on the transformation step, applying software engineering best practices—version control, testing, documentation, and modularity—to analytics code.

dbt works by taking SQL SELECT statements defined in the analytics codebase and executing them against the data warehouse. This "SQL-first" approach means anyone familiar with SQL can contribute to data transformation logic, dramatically lowering the barrier to entry for data engineering work. Models are defined as `.sql` files, and dbt compiles these into the appropriate SQL dialect for the target warehouse (Snowflake, BigQuery, Redshift, Databricks, Postgres, etc.).

## Key Concepts

**Models** are the core building blocks in dbt. Each model is a single SQL SELECT statement that defines a transformation. Models are typically organized in a directory structure and can reference other models to build up a DAG (Directed Acyclic Graph) of dependencies. When you run `dbt run`, dbt compiles and executes these models in dependency order.

**Materializations** determine how model results are stored in the data warehouse. The four main materialization types are:

- **Table**: Creates a table by running the full SELECT and storing results
- **View**: Stores no data; the view is created and queries run against it each time
- **Incremental**: Appends or updates new records since the last run, much faster for large fact tables
- **Ephemeral**: Not directly created in the database; CTEs that other models reference

**Seeds** are CSV files committed to the repository that dbt loads into the warehouse as reference tables. They're useful for small, relatively static dimension data that doesn't warrant a full ETL process.

**Tests** in dbt validate data quality and integrity. Schema tests define expected constraints (uniqueness, not null, foreign key relationships), while custom tests run arbitrary SQL to check business logic. Tests produce pass/fail results and can be integrated into CI/CD pipelines to prevent bad data from reaching production.

**Documentation** is first-class in dbt. The `dbt docs generate` command creates a documentation site from descriptions in YAML files and column-level lineage. This auto-generated documentation reflects the actual state of the codebase, reducing drift between code and documentation.

## How It Works

dbt follows a workflow: write models in SQL (or Python for dbt Core 1.0+), run `dbt run` to execute them against the warehouse, and use `dbt test` to validate results. During `dbt run`, dbt builds a dependency graph from `ref()` calls between models, determines execution order, and compiles each model to the target warehouse's SQL dialect.

The `ref()` function is fundamental—it's how models reference each other, creating dependencies and enabling dbt to manage the DAG. The `source()` function references raw tables that exist in the warehouse, making it clear where upstream data enters the pipeline.

```sql
-- Example: A dbt model (staging_orders.sql)
-- This model cleans and shapes raw orders data

{{ config(materialized='view') }}

SELECT
    order_id,
    customer_id,
    order_date,
    
    -- Clean up null amounts and cast to numeric
    COALESCE(amount, 0)::NUMERIC(10,2) AS order_amount,
    
    -- Extract date parts for easier aggregation
    DATE_TRUNC('month', order_date) AS order_month,
    DATE_TRUNC('year', order_date) AS order_year,
    
    -- Normalize status values
    LOWER(TRIM(status)) AS order_status,
    
    -- Flag high-value orders
    CASE 
        WHEN amount > 1000 THEN true 
        ELSE false 
    END AS is_high_value

FROM {{ source('ecommerce', 'raw_orders') }}

WHERE 
    order_date >= '2020-01-01'  -- Only process recent orders
    AND customer_id IS NOT NULL
```

```yaml
# Example: Schema.yml defining tests and documentation
version: 2

models:
  - name: staging_orders
    description: Cleaned and normalized order data from e-commerce platform
    columns:
      - name: order_id
        description: Primary key for orders
        tests:
          - unique
          - not_null
      - name: customer_id
        description: Foreign key to customers table
        tests:
          - not_null
          - relationships:
              to: ref('staging_customers')
              field: customer_id
      - name: order_amount
        description: Total order amount in USD
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min: 0
              max: 100000
```

## Practical Applications

dbt is used extensively for:

- Building and maintaining data transformation pipelines in analytics engineering teams
- Creating reusable and testable business logic definitions (customer lifetime value, revenue calculations)
- Establishing data quality standards with automated testing
- Generating documentation that serves as a single source of truth for data definitions
- Enabling collaborative data development through version control and code review

## Related Concepts

- [[data-warehouse]] - The analytical database system where dbt operates
- [[etl]] - Extract, Transform, Load - dbt focuses on the T portion
- [[sql]] - The primary language used to define dbt models
- [[analytics-engineering]] - The role that typically works with dbt
- [[data-transformation]] - The act of reshaping data that dbt facilitates

## Further Reading

- [getdbt.com](https://getdbt.com) - Official documentation and community resources
- "Analytics Engineering" guide from dbt Learn
- dbt Community Slack and Discourse forums

## Personal Notes

dbt doesn't move data—it only transforms data that already exists in your warehouse. This is both a strength (simplicity, leverage of SQL skills) and a limitation. For organizations starting with dbt, resist the urge to over-engineer your model graph early. Start simple, add complexity only when needed for performance or reusability, and invest in testing from day one. The real power of dbt isn't just the tool—it's the discipline it encourages around documentation, version control, and testing of data code.
