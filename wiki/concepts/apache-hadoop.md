---
title: "Apache Hadoop"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [big-data, distributed-systems, data-engineering, open-source]
---

# Apache Hadoop

## Overview

Apache Hadoop is an open-source framework for storing, processing, and analyzing massive datasets across distributed clusters of commodity hardware. Originally developed by Doug Cutting and Mike Cafarella and inspired by Google's MapReduce and Google File System papers, Hadoop provides a reliable, scalable platform for batch processing of structured and unstructured data at scale. It is the foundational technology that spawned the modern big data ecosystem, enabling organizations to extract value from data volumes that would overwhelm traditional relational database systems.

Hadoop's core innovation is the idea that failures are normal in large集群 computing environments, and the software should handle them transparently rather than requiring operators to manage them manually. This design philosophy, combined with its ability to run on inexpensive hardware, dramatically reduced the cost of large-scale data processing and democratized access to big data technologies across industries.

## Key Concepts

The Hadoop ecosystem is built around four core modules that work together to provide distributed data storage and processing capabilities.

**Hadoop Distributed File System (HDFS)** is a Java-based, fault-tolerant file system designed to store large files across multiple machines. It splits files into large blocks (typically 128MB or 256MB) and replicates them across the cluster to ensure durability against hardware failures. HDFS uses a master-slave architecture with NameNode (managing metadata) and DataNodes (storing actual blocks).

**MapReduce** is Hadoop's original programming model for parallel data processing. Jobs are divided into a Map phase (filtering and sorting data) and a Reduce phase (aggregating results). While MapReduce has largely been superseded by newer engines in recent years, it established the foundational programming paradigm for distributed batch processing.

**YARN (Yet Another Resource Negotiator)** acts as the cluster operating system, managing resources and scheduling jobs across the Hadoop cluster. It separates resource management from application logic, allowing diverse processing frameworks to run on the same cluster.

**Hadoop Common** provides shared utilities, libraries, and APIs used across all other Hadoop modules.

## How It Works

When a MapReduce job is submitted to a Hadoop cluster, the YARN ResourceManager allocates container resources on appropriate NodeManagers. The ApplicationMaster negotiates with the ResourceManager for containers and assigns Map tasks to nodes holding the relevant data blocks (data locality). Each Map task processes its input split and writes intermediate results to local disk. The shuffle phase transfers these results to Reduce nodes, which aggregate outputs and write final results back to HDFS.

HDFS achieves fault tolerance through block replication. By default, each block is replicated three times across different nodes. If a DataNode fails, the NameNode detects the missing replicas and schedules re-replication on healthy nodes. This automatic recovery is fundamental to Hadoop's reliability.

The ResourceManager uses a scheduling queue system to prioritize jobs and allocate cluster resources fairly among users and applications. Common schedulers include FIFO, Fair Scheduler, and Capacity Scheduler.

## Practical Applications

Hadoop is used for large-scale batch processing workloads including log analysis, data warehousing, machine learning feature engineering, and ETL pipelines. Enterprises use it to process clickstream data, analyze customer behavior, and generate business intelligence reports from historical data. Genomics research organizations use Hadoop to process and analyze DNA sequencing data. Financial institutions use it for fraud detection and risk analysis on transaction histories.

## Examples

A typical word count MapReduce job in Python using the `mrjob` library:

```python
from mrjob.job import MRJob

class WordCount(MRJob):
    def mapper(self, _, line):
        for word in line.split():
            yield word, 1

    def reducer(self, word, counts):
        yield word, sum(counts)

if __name__ == '__main__':
    WordCount.run()
```

To run this on Hadoop:
```bash
hadoop jar hadoop-streaming.jar \
  -mapper python_mapper.py \
  -reducer python_reducer.py \
  -input /data/text/* \
  -output /output/wordcount
```

## Related Concepts

- [[Kafka]] — Real-time data streaming often paired with Hadoop for lambda architecture
- [[file-formats]] — Understanding Parquet, ORC, and Avro formats used with Hadoop
- [[data-analytics]] — Broader context of analytics pipelines that may include Hadoop
- [[storage]] — Distributed storage concepts related to HDFS

## Further Reading

- Tom White, *Hadoop: The Definitive Guide* (4th Edition, O'Reilly)
- Apache Hadoop Documentation: https://hadoop.apache.org/docs/
- "The Hadoop Distributed File System" — Shvachko et al., IEEE (2010)

## Personal Notes

Hadoop feels somewhat legacy in 2026 given the rise of cloud-native data platforms like Snowflake and Databricks, but understanding it remains foundational because many enterprise systems still run on it and its design patterns influence newer tools. The MapReduce model, while limited, is still a useful mental model for thinking about distributed computation.
