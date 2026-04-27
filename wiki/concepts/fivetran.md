---
title: "Fivetran"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-integration, elt, etl, analytics, cloud-data]
---

# Fivetran

## Overview

Fivetran is a cloud-based data integration platform that automates the process of extracting data from operational databases and SaaS applications, transforming it, and loading it into a data warehouse. Founded in 2012, Fivetran pioneered the concept of fully-managed connectors that require zero maintenance once configured. The platform handles schema migration automatically, adapting when source systems change, which distinguishes it from traditional ETL tools that demand significant engineering attention.

Fivetran's value proposition centers on eliminating the tedious, ongoing maintenance burden of data pipelines. Instead of writing custom integration code that breaks when upstream APIs change, teams configure connectors once and let Fivetran handle ongoing synchronization. This approach enables data teams to focus on analytics rather than plumbing.

## Key Concepts

### Managed Connectors

Fivetran provides 300+ pre-built connectors to popular sources:

- **Databases**: MySQL, PostgreSQL, Oracle, SQL Server, MongoDB
- **SaaS Applications**: Salesforce, HubSpot, Stripe, Shopify, Google Ads
- **Cloud Services**: AWS S3, Google Cloud Storage, Azure Blob
- **Event Platforms**: Segment, Amplitude, Mixpanel

Each connector is maintained by Fivetran—API changes are handled transparently without customer intervention.

### ELT Architecture

Fivetran follows an ELT (Extract, Load, Transform) rather than traditional ETL approach:

- **Extract**: Data is copied from source systems, often using change data capture (CDC)
- **Load**: Raw data lands in the warehouse in staging tables
- **Transform**: SQL-based transformations happen in the warehouse using tools like dbt

This separation means the warehouse handles transformation compute, not Fivetran.

### Synchronization Modes

Fivetran offers different sync strategies:

- **Historical Sync**: Loads all available historical data
- **Incremental Sync**: Only new or changed records since last sync
- **CDC (Change Data Capture)**: For databases, reads transaction logs for near-real-time replication
- **Fivetran REST API**: Custom connectors for unsupported sources

## How It Works

```sql
-- Example: Fivetran automatically creates staging tables
-- Table created by Fivetran for Stripe charges source
CREATE TABLE stripe_charges_staging (
    _fivetran_id TEXT,
    _fivetran_synced TIMESTAMP,
    id TEXT,
    amount INTEGER,
    currency TEXT,
    created TIMESTAMP,
    customer_id TEXT,
    status TEXT,
    -- Plus 30+ more columns from Stripe API
);

-- Transformations typically happen in dbt, referencing staging:
CREATE TABLE mart_revenue_daily AS
SELECT 
    DATE(created) AS revenue_date,
    SUM(amount) / 100.0 AS daily_revenue,
    COUNT(*) AS transaction_count
FROM stripe_charges_staging
WHERE status = 'succeeded'
GROUP BY 1;
```

### Schema Management

Fivetran automatically discovers source schema and creates corresponding destination tables. When sources change—when an API adds new fields or tables—Fivetran migrates the destination schema without customer action, a capability called "schema evolution."

## Practical Applications

Fivetran is essential for modern data stack architectures:

- **Analytics Engineering**: Teams use Fivetran + dbt + BI tools to build analytics
- **Operational Analytics**: Replicating CRM, support, and billing data for cross-functional analysis
- **Data Migration**: Moving from legacy systems to modern cloud data warehouses
- **Compliance & Audit**: Maintaining synchronized copies of operational data

## Examples

A typical modern data stack using Fivetran:
- **Source**: Salesforce (CRM), Stripe (Payments), PostgreSQL (Product DB)
- **Integration**: Fivetran for all connectors
- **Warehouse**: Snowflake or BigQuery
- **Transformation**: dbt Cloud
- **Visualization**: Looker or Tableau

## Related Concepts

- [[ETL]] - Traditional extract-transform-load approach
- [[Data Warehouse]] - Destination for Fivetran data
- [[Snowflake]] - Popular data warehouse platform
- [[dbt]] - Data transformation tool often paired with Fivetran
- [[Segment]] - Customer data platform with complementary use case

## Further Reading

- Fivetran Documentation (fivetran.com/docs)
- "The Modern Data Stack" - Overview of integrated tools

## Personal Notes

Fivetran's pricing model (based on consumed credits per row) can be surprising for high-volume use cases. Large tables with frequent updates can drive significant costs. Despite this, the total cost of ownership typically beats building and maintaining custom integrations. The key limitation is vendor lock-in to Fivetran's connector behavior and sync schedules.
