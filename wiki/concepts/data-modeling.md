---
title: Data Modeling
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-modeling, database-design, dimensional-modeling, data-warehouse, star-schema, data-engineering]
sources: []
---

# Data Modeling

## Overview

Data modeling is the process of creating a structured representation of data that defines how data is organized, stored, and accessed. A data model serves as a blueprint for information systems, specifying the entities (things we want to track like customers, orders, products), their attributes (properties like name, price, date), and the relationships between them (a customer places many orders, an order contains many line items). Good data models make systems easier to build, maintain, and query — they are the foundation upon which reliable data pipelines and analytics are built.

Data modeling operates at multiple levels of abstraction. Conceptual data models capture high-level business requirements — what entities matter and how they relate, without technical detail. Logical data models add detail: attribute names, data types, primary and foreign keys, and normalization rules. Physical data models map the logical model to specific database technology: table structures, indexes, partitioning schemes, and storage parameters.

The choice of data modeling approach depends heavily on the use case. Transactional systems (OLTP) use normalized models to minimize redundancy and ensure data integrity. Analytical systems (OLAP/data warehouses) often use denormalized models like star schema to optimize query performance. Modern data lakehouse architectures introduce new tradeoffs, sometimes combining medallion architectures (bronze/silver/gold layers) with both normalized and denormalized structures at different tiers.

Effective data modeling requires both technical skills (understanding database internals, query optimization, schema design patterns) and business domain knowledge (understanding what the data represents, how it's used, what questions need answering). A technically perfect model that doesn't reflect business reality is nearly useless.

## Key Concepts

**Entities and Attributes**: Entities are objects or concepts with independent existence — customers, products, transactions, events. Attributes are properties that describe entities: a customer has a name, email, signup date; a product has a SKU, price, category. Entities are typically implemented as tables; attributes become columns.

**Primary Keys and Foreign Keys**: A primary key uniquely identifies each row in a table. Foreign keys establish relationships by referencing primary keys in other tables. Together, they create the referential integrity that keeps data consistent. Surrogate keys (system-generated IDs like UUIDs or auto-incrementing integers) are often preferred over natural keys for their stability and predictability.

**Normalization**: The process of organizing data to reduce redundancy and improve data integrity. Normal forms (1NF, 2NF, 3NF, BCNF) define increasingly strict rules about functional dependencies and key relationships. Highly normalized models store each piece of data in exactly one place, making updates simple but potentially requiring more joins to answer questions.

**Denormalization**: Intentionally introducing redundancy to optimize read performance. Denormalized schemas store duplicated data to avoid expensive joins. Data warehouses commonly use denormalized dimensions attached to fact tables. Trade-offs include larger storage requirements and more complex update logic.

**Star Schema**: A popular dimensional modeling pattern with a central fact table surrounded by dimension tables. Fact tables contain measurable, quantitative business metrics (sales amount, quantity, duration). Dimension tables contain descriptive attributes for filtering and grouping (customer name, product category, store location). The pattern resembles a star — hence the name.

**Snowflake Schema**: A variation of star schema where dimension tables are normalized into sub-dimensions. A product dimension might split into product category and product subcategory tables. This reduces redundancy but increases query complexity.

**Fact Tables**: In dimensional modeling, fact tables store the metrics or measures of business processes. They are typically large (millions to billions of rows), dense with numeric data, and organized around a business process (orders, shipments, payments). Fact tables have foreign keys to dimension tables and degenerate dimensions (transaction IDs, invoice numbers) that don't join to a dimension.

**Dimension Tables**: Dimension tables store the descriptive attributes used to slice and dice fact tables. They are typically smaller than facts, highly denormalized, and rich with descriptive text. Examples: customer dimension (name, segment, region, lifecycle stage), time dimension (date, week, month, quarter, year, holiday flag).

** Slowly Changing Dimensions (SCD)**: Dimension data that changes over time requires special handling. Type 1 SCD overwrites old values with new ones (no history). Type 2 SCD adds new rows with effective dates to preserve history. Type 3 SCD stores both old and new values in the same row. Choosing the right SCD strategy determines what historical analysis is possible.

## How It Works

Data modeling for a data warehouse typically follows a top-down methodology inspired by Ralph Kimball's approach:

**Step 1 — Select Business Process**: Identify the fundamental business process to model. Common processes include: order-to-cash, procurement, fulfillment, customer acquisition, support tickets. Each process yields one or more fact tables.

**Step 2 — Declare the Grain**: Define what each row in the fact table represents. Grain = what is being measured at its most atomic level. An order line item grain means each row represents one product on one order. A daily snapshot grain means each row represents one entity's state at end of day.

**Step 3 — Identify Dimensions**: Determine what dimensions provide context to the facts. Who, what, where, when, why, how. Dimensions should be rich enough to support all expected analytical queries without requiring joins to other tables.

**Step 4 — Identify Facts**: Identify the numeric metrics that make sense at the declared grain. If grain is line item, facts include quantity and unit price (can be multiplied for line revenue). Facts that would require allocation (monthly rent) may not fit this grain.

**Step 5 — Build Physical Model**: Map logical model to database. Define tables, columns, data types, indexes, partitioning. Handle SCD strategies for dimensions. Define constraints and relationships.

```sql
-- Star schema example: Retail sales data warehouse

-- Fact table: one row per order line item
CREATE TABLE fact_sales (
    sale_key        BIGINT IDENTITY PRIMARY KEY,
    order_key       BIGINT NOT NULL REFERENCES dim_orders(order_key),
    customer_key    BIGINT NOT NULL REFERENCES dim_customer(customer_key),
    product_key     BIGINT NOT NULL REFERENCES dim_product(product_key),
    store_key       BIGINT NOT NULL REFERENCES dim_store(store_key),
    date_key        DATE NOT NULL REFERENCES dim_date(date_key),
    
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,
    discount_amount  DECIMAL(10,2) DEFAULT 0,
    sale_amount     DECIMAL(10,2) NOT NULL,  -- quantity * unit_price - discount
    
    -- Audit fields
    load_timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension table: Customer
CREATE TABLE dim_customer (
    customer_key    BIGINT IDENTITY PRIMARY KEY,
    customer_id     VARCHAR(50) NOT NULL UNIQUE,
    customer_name   VARCHAR(200) NOT NULL,
    email           VARCHAR(255),
    phone           VARCHAR(50),
    customer_tier   VARCHAR(20),  -- Gold, Silver, Bronze
    
    -- SCD Type 2 fields for address history
    region          VARCHAR(100),
    effective_date  DATE DEFAULT '1900-01-01',
    expiry_date     DATE DEFAULT '9999-12-31',
    is_current      BOOLEAN DEFAULT TRUE
);

-- Dimension table: Product
CREATE TABLE dim_product (
    product_key     BIGINT IDENTITY PRIMARY KEY,
    product_id      VARCHAR(50) NOT NULL UNIQUE,
    product_name    VARCHAR(200) NOT NULL,
    category        VARCHAR(100),
    subcategory     VARCHAR(100),
    brand           VARCHAR(100),
    unit_cost       DECIMAL(10,2),
    
    -- SCD Type 1 (current values only)
    current_price   DECIMAL(10,2),
    is_active       BOOLEAN DEFAULT TRUE
);

-- Sample queries against star schema

-- Revenue by category, month, customer tier
SELECT 
    p.category,
    d.month_name,
    c.customer_tier,
    SUM(f.sale_amount) AS total_revenue,
    COUNT(*) AS order_line_count
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE d.fiscal_year = 2026
  AND c.is_current = TRUE
GROUP BY p.category, d.month_name, c.customer_tier
ORDER BY total_revenue DESC;

-- Identify customer purchasing patterns (cohort analysis)
WITH customer_first_purchase AS (
    SELECT 
        c.customer_key,
        MIN(f.date_key) AS first_purchase_date
    FROM fact_sales f
    JOIN dim_customer c ON f.customer_key = c.customer_key
    WHERE c.is_current = TRUE
    GROUP BY c.customer_key
)
SELECT 
    DATE_TRUNC('month', cf.first_purchase_date) AS cohort_month,
    COUNT(DISTINCT cf.customer_key) AS cohort_size,
    SUM(CASE WHEN f.date_key <= cf.first_purchase_date + INTERVAL '30 days' THEN 1 ELSE 0 END) AS month_1_retained,
    SUM(CASE WHEN f.date_key <= cf.first_purchase_date + INTERVAL '60 days' THEN 1 ELSE 0 END) AS month_2_retained
FROM customer_first_purchase cf
JOIN fact_sales f ON cf.customer_key = f.customer_key
GROUP BY DATE_TRUNC('month', cf.first_purchase_date)
ORDER BY cohort_month;
```

## Practical Applications

**Data Warehouse Design**: The primary use case. Dimensional modeling (star schema) organizes data for analytical queries, making it easy for business users to write self-service reports without understanding underlying data complexity. Kimball methodology remains influential; Inmon's corporate information factory offers an alternative top-down approach.

**Operational Database Design**: OLTP systems use normalized models to maintain data integrity and support concurrent transactional writes. Third normal form is common, with careful attention to foreign key constraints and indexing for query performance.

**Master Data Management**: Creating "golden records" for core entities (customers, products, locations) requires modeling that reconciles data from multiple source systems, handles matching and merging, and preserves provenance.

**Event Schema Design**: For event-driven architectures and NoSQL databases, modeling how events are structured (JSON schema, Avro schema) determines query flexibility and storage efficiency. Denormalized, self-contained events work well for append-only logs.

**ML Feature Engineering**: Machine learning requires structuring data into feature matrices. Data modeling determines how raw data is transformed into features — handling categorical encoding, time-based aggregations, and categorical interactions.

**Data Lake Organization**: Even schema-on-read data lakes benefit from thoughtful organization — partitioning strategies, file formats (Parquet vs ORC), and naming conventions that make data discoverable and queryable.

## Examples

**Medallion Architecture (Bronze/Silver/Gold)**:

```
┌─────────────────────────────────────────────────────────────┐
│                    RAW / BRONZE LAYER                       │
│  • Schema-on-read: raw as received from sources            │
│  • Full fidelity: includes deleted records, duplicates     │
│  • Enables reprocessing if transformation logic changes    │
│  • Examples: raw_orders.parquet, raw_customers.json        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CLEANED / SILVER LAYER                    │
│  • Applied business rules: deduplication, standardization  │
│  • Type casting, null handling                              │
│  • Matched/merged across sources (customer dedup)          │
│  • Ready for analytical transformations                      │
│  • Examples: orders_cleaned, customers_matched             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS-READY / GOLD LAYER               │
│  • Dimensional models: star schema fact and dimensions      │
│  • Aggregations and metrics pre-computed                    │
│  • Optimized for analytical queries                          │
│  • Examples: fact_monthly_sales, dim_customer              │
└─────────────────────────────────────────────────────────────┘
```

**Data Vault Modeling**: An alternative methodology designed for enterprise data warehouses with three core entity types:

```sql
-- Data Vault structure for Order data

-- Hub: business keys (stable identifiers)
CREATE TABLE hub_order (
    order_hkey      BIGINT PRIMARY KEY,  -- Hash of order_id
    order_id        VARCHAR(50) NOT NULL UNIQUE,
    load_timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source   VARCHAR(100)  -- Source system
);

-- Link: relationships between hubs
CREATE TABLE link_order_customer (
    link_hkey       BIGINT PRIMARY KEY,
    order_hkey      BIGINT REFERENCES hub_order(order_hkey),
    customer_hkey   BIGINT REFERENCES hub_customer(customer_hkey),
    load_timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source   VARCHAR(100)
);

-- Satellite: descriptive attributes that change over time
CREATE TABLE sat_order_details (
    order_hkey      BIGINT REFERENCES hub_order(order_hkey),
    load_timestamp  TIMESTAMP,
    order_status    VARCHAR(50),
    order_total     DECIMAL(10,2),
    shipping_address VARCHAR(500),
    effective_date  DATE,
    expiry_date     DATE DEFAULT '9999-12-31'
);
```

## Related Concepts

- [[data-warehouse]] — The analytical system data models often serve
- [[dimensional-modeling]] — Kimball's methodology for analytical data models
- [[star-schema]] — The common dimensional modeling pattern
- [[etl]] — Pipelines that populate data models from source systems
- [[elt]] — Modern approach loading raw data then transforming in warehouse
- [[normalization]] — The theory of organizing data to reduce redundancy
- [[database-design]] — Physical implementation of data models
- [[slowly-changing-dimensions]] — Handling historical changes in dimension data
- [[dbt]] — Tool commonly used to define and manage data models in modern stacks

## Further Reading

- [The Data Warehouse Toolkit](https://www.kimballgroup.com/books/data-warehouse-toolkit/) — Ralph Kimball's definitive guide to dimensional modeling
- [Data Modeling for Data Warehouses](https://www.amazon.com/) — Comprehensive reference
- [Data Vault 2.0](https://www.datavault2.com/) — Data Vault methodology resources
- [Principles of Data Integration](https://www.amazon.com/) — Academic treatment of data modeling
- [dbt Documentation](https://docs.getdbt.com/) — Modern data transformation and modeling

## Personal Notes

The most common data modeling mistake I see is conflating the source system model with the analytical model. Teams take their operational database schema and directly expose it in the data warehouse, then wonder why queries are slow and business users can't understand the data. The operational model serves transactional integrity; the analytical model should serve query performance and business comprehension.

Star schema isn't always the answer, but it's a strong default for relational data warehouses. The discipline of separating facts (what happened) from dimensions (context around what happened) forces clarity about what you're measuring and how you want to slice it. Even if you end up with a snowflake or a fully normalized model, going through the dimensional modeling exercise reveals gaps in understanding.

I've learned to treat data models as living documents. Business needs change; new data sources arrive; analytical questions evolve. A model that worked perfectly 18 months ago may need restructuring. The raw/bronze layer in a medallion architecture is your escape hatch — by preserving original data, you can always reprocess into new models without re-extracting from sources.
