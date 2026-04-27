---
title: ELT
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, elt, data-warehouse, cloud-data, sql-transform]
sources: []
---

# ELT (Extract, Load, Transform)

## Overview

ELT stands for Extract, Load, Transform — a data integration pattern that reverses the traditional ETL sequence by loading raw data into a destination system first, then performing transformations using the computational power of that destination platform. Unlike ETL, which transforms data before loading, ELT assumes the destination (typically a modern cloud data warehouse or data lakehouse) has sufficient processing capability to handle transformation logic efficiently. This approach has gained massive popularity in the 2010s and 2020s with the rise of Snowflake, BigQuery, Redshift, and Databricks, which provide scalable compute separate from storage.

The key advantage of ELT is that it simplifies the data pipeline by removing transformation logic from the ingestion layer. Data is extracted from sources and loaded directly into the warehouse in its raw form, preserving the original data for multiple use cases and future reprocessing. Transformations are then expressed as SQL queries or data pipeline tools like dbt (data build tool), which run within the warehouse. This separation of concerns makes pipelines easier to maintain and allows analysts to modify transformations without changing pipeline code.

ELT represents a philosophical shift from "process then store" to "store everything, process on demand." By retaining raw data, organizations can recreate any previous state, test new transformation logic against historical data, and support use cases that weren't anticipated when the original pipeline was built.

## Key Concepts

**Raw Layer (Bronze/Silver/Gold)**: Many ELT architectures organize data into tiers. The raw or bronze layer contains data exactly as it arrived from source systems — unchanged, unfiltered, with all original fields. The silver layer applies cleaning, deduplication, and basic standardization. The gold layer contains business-ready datasets optimized for analytics and reporting. This medallion architecture allows tracing any result back to raw source data.

**Transformation in the Warehouse**: The core of ELT is performing data transformation using SQL within the warehouse platform. Snowflake's Snowflake SQL, BigQuery's BigQuery SQL, or Redshift's Amazon Redshift SQL handle complex joins, aggregations, and window functions at scale. dbt has become the de facto standard for organizing and managing these transformations, treating them as code with version control, testing, and documentation.

**Data Lakehouse Convergence**: Modern platforms like Databricks combine data lake storage with data warehouse capabilities, enabling ELT patterns on both structured and unstructured data. This convergence allows organizations to load raw files (JSON, Parquet, images) alongside structured tabular data and transform everything in one platform.

**Schema-on-Read vs Schema-on-Write**: Traditional ETL applies schema during loading (schema-on-write), while ELT often uses schema-on-read — data is loaded in raw form and schema is applied when queries run. This provides flexibility but requires careful data management to avoid "schema chaos."

**Reverse ETL**: An emerging pattern that complements ELT. After data is transformed in the warehouse, reverse ETL pushes selected results back to operational systems (CRMs, marketing tools) to enable actions based on analytical insights.

## How It Works

A typical ELT workflow using dbt follows a structured pattern:

1. **Connect Sources**: An ingestion tool (Fivetran, Airbyte, Stitch, or custom) connects to source systems using pre-built connectors. These tools handle API pagination, rate limiting, and incremental extraction.

2. **Load to Raw Layer**: Data is extracted and loaded directly to the raw/bronze layer of the warehouse. Loading is typically append-only or uses CDC (Change Data Capture) to track updates. The warehouse stores data in columnar formats optimized for analytical queries.

3. **Stage and Clean**: SQL-based staging models in dbt clean the raw data — casting types, renaming fields, handling nulls consistently. These are typically one-to-one mappings from source tables.

4. **Build Intermediate Models**: Intermediate transformation layers join multiple sources, apply business logic, and create derived fields. This is where the analytical semantics live.

5. **Create Final Marts**: Final models in the gold/marts layer are optimized for specific analytical use cases — fact tables for metrics, dimension tables for filtering and grouping.

6. **Test and Document**: dbt runs data tests (uniqueness, referential integrity, value ranges) and generates documentation automatically.

```sql
-- dbt example: staging raw orders data
{{ config(materialized='view') }}

SELECT
    -- Surrogate key for the order
    {{ dbt_utils.generate_surrogate_key(['order_id']) }} AS order_key,
    
    -- Natural keys
    order_id,
    customer_id,
    store_id,
    
    -- Dates
    order_date :: DATE AS order_date,
    created_at :: TIMESTAMP AS created_at,
    
    -- Measures
    ROUND(total_amount :: NUMERIC(10,2), 2) AS total_amount,
    quantity :: INT AS quantity,
    
    -- Metadata
    CURRENT_TIMESTAMP() AS dbt_loaded_at

FROM {{ source('source_db', 'raw_orders') }}

WHERE order_id IS NOT NULL
```

```sql
-- dbt example: intermediate model joining orders to customers
{{ config(materialized='view') }}

SELECT
    o.order_key,
    o.order_id,
    o.order_date,
    o.total_amount,
    
    -- Customer attributes at time of order
    c.customer_key,
    c.customer_name,
    c.customer_tier,
    c.region,
    
    -- Order metrics
    o.total_amount * (1 - COALESCE(p.discount_rate, 0)) AS net_amount

FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_customers') }} c 
    ON o.customer_id = c.customer_id
LEFT JOIN {{ ref('stg_promotions') }} p
    ON o.promotion_id = p.promotion_id

WHERE o.order_date >= '2024-01-01'
```

## Practical Applications

**Cloud Data Warehouse Population**: Organizations migrating to Snowflake, BigQuery, or Redshift use ELT to quickly get data flowing. They load raw data first, then build transformations incrementally — unlike ETL which requires upfront transformation logic.

**Self-Service Analytics Enablement**: By maintaining raw data in the warehouse, analysts can write their own queries without waiting for pipeline changes. The raw layer serves as a "time machine" for ad-hoc analysis.

**Regulatory and Audit Requirements**: Financial services firms load raw transaction data first to meet regulatory requirements for data retention and auditability. Transformations are additive — original data is never modified.

**ML Feature Engineering**: Machine learning workflows benefit from ELT's raw data preservation. Data scientists can experiment with different feature transformations against the same underlying data without rerunning ingestion.

**Cross-Platform Analytics**: When combining data from multiple SaaS tools (Salesforce, HubSpot, Stripe) with operational databases, ELT simplifies the architecture by loading everything to one platform first.

## Examples

**Fivetran + Snowflake + dbt Pipeline**:

```
[Salesforce] ──┐
[Stripe]      ──┼──> [Fivetran] ──> [Snowflake Raw] ──> [dbt] ──> [Analytics]
[PostgreSQL] ──┘                (CDC Extract/Load)      (Transform)
                                       │
                                       └── Incremental loads, schema detection
```

Fivetran handles the extract and load phases with automatic schema migration. Snowflake stores raw data. dbt models transform the data through staged layers into analytics-ready tables.

**Airbyte Open-Source ELT**:

```yaml
# airbyte source config (extract + load)
version: '1.0'
sources:
  - name: postgres_source
    type: postgres
    config:
      host: "{{ env_var('POSTGRES_HOST') }}"
      port: 5432
      database: sales
      username: "{{ env_var('POSTGRES_USER') }}"
      password: "{{ env_var('POSTGRES_PASSWORD') }}"
      replication_method: CDC
  - name: stripe_source
    type: stripe
    config:
      api_key: "{{ env_var('STRIPE_API_KEY') }}"
```

## Related Concepts

- [[etl]] — The traditional pattern that inspired ELT; ETL transforms before loading
- [[data-warehouse]] — The destination platform where ELT transformations typically run
- [[data-pipelines]] — The broader category of data movement between systems
- [[dbt]] — Data build tool, the dominant transformation layer for ELT
- [[snowflake]] — Popular cloud data warehouse commonly used for ELT
- [[data-lakehouse]] — Modern architecture combining data lake and warehouse capabilities
- [[reverse-etl]] — Emerging pattern that complements ELT by pushing warehouse data back to operational systems

## Further Reading

- [dbt Documentation](https://docs.getdbt.com/) — Official dbt docs and guides
- [Fivetran's ELT explained](https://www.fivetran.com/blog/elt-explained) — Commercial perspective on ELT
- [The Rise of ELT in the Cloud Era](https://www.montecarlodata.com/) — Blog on modern ELT patterns
- Snowflake's [ELT guide](https://docs.snowflake.com/en/guides-overview) — Vendor documentation
- [Data Build Tool (dbt) Guide](https://www.startdataengineering.com/) — Tutorial on dbt fundamentals

## Personal Notes

The ETL vs ELT distinction used to be a hot debate in data engineering. Now it feels largely settled: ELT is the default for cloud-native architectures, ETL remains valid when you need complex transformations before storage (compliance filtering, PII masking, or legacy system constraints).

What surprises teams new to ELT is the discipline required in the "T" layer. Because the warehouse is powerful and SQL is expressive, there's a temptation to write increasingly complex dbt models. Without governance, you end up with hundreds of models that no one understands. I've found that treating the staging layer as 1:1 with sources (no business logic) and reserving business logic for intermediate/gold layers keeps things maintainable.

The raw/bronze layer is your insurance policy. I've seen organizations regret not preserving raw data when they later needed to investigate data quality issues, audit past states, or support new analytical use cases. The marginal cost of storing raw data in a data lake or external stage is low; the value of having it is often very high.
