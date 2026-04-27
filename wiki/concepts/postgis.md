---
title: PostGIS
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [postgis, postgresql, geospatial, databases, gis, spatial-analysis]
---

# PostGIS

## Overview

PostGIS is a powerful open-source extension for PostgreSQL that adds comprehensive support for geographic objects and spatial data types, enabling PostgreSQL to function as a full-featured Geographic Information System (GIS) database. By storing geometry types like points, lines, and polygons directly in database tables, PostGIS allows developers and analysts to perform complex spatial queries and analyses using standard SQL syntax, all while leveraging PostgreSQL's robustness, ACID compliance, and ecosystem of tools.

The extension was developed by Refractions Research and first released in 2001, becoming a cornerstone of the open-source GIS ecosystem. PostGIS implements the OpenGIS Simple Features specification, ensuring compatibility with industry-standard spatial data formats and enabling interoperability with desktop GIS applications like QGIS and commercial tools like Esri ArcGIS. Today, PostGIS is used by organizations ranging from small mapping startups to global enterprises and government agencies that need to store, query, and analyze massive volumes of spatial data.

Beyond simple geometry storage, PostGIS provides hundreds of spatial functions for geometry construction, testing relationships between spatial objects, transformations, and aggregations. This makes it possible to answer questions like "find all customers within 10 kilometers of store locations" or "calculate the total area of forest cover affected by a wildfire" directly in SQL, often with performance that outperforms external GIS processing tools.

## Key Concepts

**Spatial Data Types** in PostGIS include `GEOMETRY` (flexible type that can hold any spatial type), `POINT`, `LINESTRING`, `POLYGON`, `MULTIPOINT`, `MULTILINESTRING`, and `MULTIPOLYGON`. There are also geography types that perform calculations on the Earth's curved surface using meters as units, as opposed to geometry types that assume a flat plane and use coordinate units.

**Spatial Reference Systems** are coordinate reference systems (CRS) that define how coordinates map to locations on Earth. PostGIS supports thousands of SRIDs (Spatial Reference System Identifiers). The most common is 4326 (WGS 84), used by GPS satellites and standard for most web mapping. Calculations can be performed in one SRID and results stored in another.

**Spatial Indexes** are critical for performance. PostGIS uses GiST (Generalized Search Tree) indexes on spatial columns to accelerate spatial queries. Without a spatial index, queries like "find all points in polygon" would require scanning every record; with an index, the database quickly identifies candidate matches.

**Spatial Functions** are the operations that make spatial databases useful. These include distance functions (`ST_Distance`), relationship functions (`ST_Contains`, `ST_Intersects`, `ST_Within`), measurement functions (`ST_Area`, `ST_Length`), and transformation functions (`ST_Transform` for converting between coordinate systems).

## How It Works

PostGIS extends PostgreSQL by adding new data types, operators, functions, and indexes. When you install PostGIS and add the extension to a database (`CREATE EXTENSION postgis;`), PostgreSQL gains awareness of spatial concepts.

Spatial data is stored in tables with geometry columns. Each geometry value includes both coordinates and a spatial reference system identifier. For example, a point might be stored as `SRID=4326;POINT(-122.4194 37.7749)` representing San Francisco's coordinates in WGS 84.

```sql
-- Create a table with a spatial column
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location GEOMETRY(Point, 4326)
);

-- Insert spatial data
INSERT INTO stores (name, location) VALUES 
    ('Downtown Store', ST_GeomFromText('POINT(-122.4194 37.7749)', 4326)),
    ('Airport Store', ST_GeomFromText('POINT(-122.3789 37.6213)', 4326));

-- Create spatial index for performance
CREATE INDEX idx_stores_location ON stores USING GIST(location);

-- Find stores within 5km of a given point
SELECT name, ST_Distance(location, ST_GeomFromText('POINT(-122.4 37.7)', 4326)) as dist_meters
FROM stores
WHERE ST_DWithin(location, ST_GeomFromText('POINT(-122.4 37.7)', 4326), 5000)
ORDER BY dist_meters;
```

Spatial queries use a two-phase approach for complex operations: the spatial index rapidly narrows candidate rows, then precise spatial functions evaluate the exact relationship. This combination enables PostGIS to efficiently handle millions of spatial records.

## Practical Applications

**Logistics and Routing** applications use PostGIS to store delivery zones, calculate distances, find optimal routes, and assign orders to nearby vehicles. E-commerce platforms calculate shipping zones and delivery estimates based on customer location stored as PostGIS points.

**Real Estate Platforms** store property boundaries as polygons and use PostGIS to perform queries like "find all houses within this school district" or "calculate the area of each property listing." Demographic overlays can be joined to spatial queries for market analysis.

**Environmental Management** organizations track wildlife habitats, monitor deforestation, and analyze the spread of pollution using PostGIS. Conservation groups calculate the intersection of protected areas with land ownership records to assess conservation effectiveness.

**Mobile Applications** increasingly rely on PostGIS backends for location-based features. Ride-sharing apps find nearby drivers, social networks suggest venues within a radius, and fitness apps track workouts on actual terrain.

## Examples

A food delivery company might store restaurant locations as points and delivery zones as polygons. When an order arrives, the system queries PostGIS to find restaurants that can serve the customer's location and calculates estimated delivery times based on distance and typical traffic patterns.

An urban planning department might maintain a PostGIS database of all parcels in a city. When rezoning a neighborhood, planners use `ST_Intersects` to identify all parcels affected, calculate total area with `ST_Area`, and generate maps by joining zoning data with parcel geometry.

A telecommunications company managing cell tower coverage might store tower locations as points with signal strength as a property. Using `ST_Distance`, they identify underserved areas, and by calculating convex hulls or Voronoi polygons around towers, they model coverage boundaries.

## Related Concepts

- [[PostgreSQL]] — The database system PostGIS extends
- [[SQL]] — The query language used to interact with PostGIS
- [[Geospatial Analysis]] — The broader field of analyzing spatial data
- [[GIS]] — Geographic Information Systems in general
- [[GeoJSON]] — Common format for encoding spatial data
- [[Shapefile]] — Another common spatial data format

## Further Reading

- PostGIS documentation at postgis.net
- "PostGIS in Action" by Regina Obe and Leo Hsu
- Boundless PostGIS tutorial materials

## Personal Notes

PostGIS transforms PostgreSQL into something that feels like magic for anyone building location-aware applications. The performance surprises people—the index strategies matter enormously. Always create spatial indexes on geometry columns you filter by, and use `EXPLAIN ANALYZE` to verify index usage on spatial queries.
