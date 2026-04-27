---
title: "Apache Spark"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [big-data, distributed-computing, data-processing, scala, python, machine-learning]
---

# Apache Spark

## Overview

Apache Spark is an open-source distributed computing framework designed for large-scale data processing. It provides high-level APIs in Python (PySpark), Scala, Java, and R that abstract away the complexity of distributed systems, allowing data engineers and scientists to write parallelized code that automatically executes across a cluster of machines.

Spark emerged as a successor to Hadoop MapReduce, addressing MapReduce's limitations: MapReduce required writing multiple passes to disk between map and reduce phases, making iterative algorithms and interactive queries painfully slow. Spark keeps data in memory between operations when possible, delivering order-of-magnitude speedups for many workloads—10x to 100x faster for typical batch processing jobs.

The framework handles the hard parts of distributed computing automatically: distributing data and computation across nodes, scheduling work across the cluster, handling node failures, and aggregating results. Developers focus on the data transformation logic; Spark handles the distributed systems engineering underneath.

Spark has evolved beyond batch processing into a unified platform supporting stream processing (Spark Streaming, Structured Streaming), machine learning (MLlib), graph analysis (GraphX), and SQL analytics. This "one platform for everything" approach reduces the operational complexity of maintaining separate systems.

## Key Concepts

**Resilient Distributed Datasets (RDDs)**: The fundamental data abstraction in Spark. An RDD is an immutable, distributed collection of objects that can be processed in parallel across the cluster. RDDs automatically track lineage (the transformations that created them), enabling fault tolerance without replication.

**DataFrames**: Higher-level abstraction resembling a relational database table or pandas DataFrame. DataFrames have named columns and support SQL-like operations. They're generally preferred over RDDs for structured data because the Spark SQL engine can optimize execution plans.

**Transformations and Actions**: Transformations (map, filter, groupBy, join) create a new RDD/DataFrame but don't execute immediately—they build a logical plan. Actions (count, collect, save) trigger execution and return results to the driver. This lazy evaluation enables Spark to optimize the full execution plan before running.

**DAG Execution**: Spark converts the sequence of transformations into a Directed Acyclic Graph (DAG) of stages and tasks. The DAG scheduler breaks the plan into stages based on shuffle boundaries; tasks within a stage execute in parallel.

**Partitions**: Data is divided into partitions, each processed by a single task on a single executor. Partition count affects parallelism—too few partitions leaves cores idle; too many creates overhead. Partition count should typically be 2-4x the number of cores.

**Shuffle**: When a transformation requires data from multiple partitions (like a groupBy), Spark must redistribute data across the network—a shuffle. Shuffles are expensive and should be minimized. They create stage boundaries in the DAG.

## How It Works

A Spark application runs as a standalone program (driver) that connects to a cluster manager (Spark's built-in standalone, YARN, Mesos, or Kubernetes). The driver distributes work to executor processes on worker nodes.

```python
# PySpark: Word count example
from pyspark.sql import SparkSession

# Initialize Spark session (entry point to Spark functionality)
spark = SparkSession.builder \
    .appName("WordCount") \
    .master("spark://master:7077") \
    .getOrCreate()

# Read text file, creating a DataFrame with one row per line
lines = spark.read.text("hdfs://data/input/*.txt")

# Split lines into words and count
word_counts = (
    lines
    .selectExpr("explode(split(value, ' ')) as word")  # Split and flatten
    .groupBy("word")                                   # Group by word
    .count()                                            # Count occurrences
)

# Show results (triggers execution)
word_counts.show()

# Save to output
word_counts.write.parquet("hdfs://data/output/wordcounts")

# Stop Spark session
spark.stop()
```

The same job written using lower-level RDD API:

```python
from pyspark import SparkContext

sc = SparkContext(appName="WordCountRDD")

# Read file, split into words, create (word, 1) pairs, reduce by key
result = (
    sc.textFile("hdfs://data/input/*.txt")
    .flatMap(lambda line: line.split())
    .map(lambda word: (word, 1))
    .reduceByKey(lambda a, b: a + b)
)

result.saveAsTextFile("hdfs://data/output/wordcounts")
sc.stop()
```

## Practical Applications

**ETL and Data Pipelines**: Spark excels at extracting data from multiple sources (databases, S3, Kafka), applying complex transformations, and loading into data warehouses. The same code runs on your laptop for testing and on a 100-node cluster for production.

**Large-Scale ETL**: Processing terabytes of log data daily to extract metrics, sessionize user behavior, and aggregate for analytics dashboards.

**Machine Learning at Scale**: MLlib provides common algorithms (regression, classification, clustering, recommendation) that train on data that doesn't fit in memory on a single machine. Spark's DataFrame API integrates with pandas for simpler experimentation.

**Graph Processing**: GraphX enables analysis of graphs like social networks, fraud detection patterns, and route optimization at scale.

**Stream Processing**: Structured Streaming processes live data streams with the same APIs as batch jobs, enabling real-time analytics, anomaly detection, and alerting.

## Examples

Machine learning with MLlib:

```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

spark = SparkSession.builder.appName("ChurnPrediction").getOrCreate()

# Load training data
training_data = spark.read.parquet("s3://data/customer_features/")

# Define feature pipeline
feature_cols = ["tenure_months", "monthly_charges", "total_charges", "support_tickets"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
indexer = StringIndexer(inputCol="churned", outputCol="label")

# Train logistic regression model
lr = LogisticRegression(maxIter=100, regParam=0.01)
pipeline = Pipeline(stages=[assembler, indexer, lr])

model = pipeline.fit(training_data)

# Make predictions
predictions = model.transform(training_data)
predictions.select("customer_id", "probability", "prediction").show()

spark.stop()
```

## Related Concepts

- [[Hadoop]] - Predecessor distributed framework; Spark can run on Hadoop clusters
- [[Data Lake]] - Often stores data processed by Spark
- [[Distributed Computing]] - The broader paradigm Spark implements
- [[Machine Learning]] - MLlib extends Spark with ML algorithms
- [[PySpark]] - Python API for Spark
- [[Scala]] - Spark's native language implementation

## Further Reading

- [Spark Documentation](https://spark.apache.org/docs/latest/) - Official docs
- [Learning Spark (O'Reilly)](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/) - Comprehensive book
- [Databricks Spark Tutorials](https://docs.databricks.com/en/getting-started/spark-tutorials/index.html) - Hands-on notebooks
- [Spark Summit Presentations](https://www.youtube.com/user/TheApacheSpark) - Conference talks

## Personal Notes

Spark has a steep learning curve that isn't just about APIs—it's about understanding distributed systems behavior. I've seen engineers write code that works perfectly on small test data but crashes on production-scale data due to shuffles that explode memory, partition counts that create too many small files, or collect() calls that try to bring terabytes to the driver. My advice: always test on data at production scale before going to production. Spark's UI (port 4040 on the driver) is invaluable for understanding what's happening—watch the stage timeline, identify skew (some tasks taking much longer than others), and monitor shuffle read/write sizes. The single biggest performance win is often just increasing partition count to better utilize cluster resources.
