---
title: "Hadoop"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [hadoop, big-data, distributed-computing, apache, data-engineering]
---

# Hadoop

## Overview

Apache Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of computers. Originally designed to handle massive amounts of structured and unstructured data, Hadoop provides scalable, fault-tolerant storage (HDFS) and parallel processing capabilities (MapReduce). It emerged from Google's research papers on MapReduce and Google File System in 2003-2004, with the open-source implementation being developed by Yahoo engineers and released as Apache Hadoop in 2007.

Hadoop enables organizations to store and process petabytes and exabytes of data using commodity hardware, dramatically reducing the cost of big data analytics compared to traditional high-performance computing solutions. The ecosystem has expanded beyond MapReduce to include many specialized tools for different data processing tasks, making it the foundation for modern [[data engineering]] and [[big data]] architectures.

## Key Concepts

**HDFS (Hadoop Distributed File System)** is the storage layer of Hadoop. It splits large files into blocks (typically 128MB or 256MB) and distributes them across the cluster nodes. Each block is replicated multiple times (usually 3) for fault tolerance. NameNodes manage metadata about file locations and block placement, while DataNodes store the actual data blocks.

**MapReduce** is the original processing paradigm for Hadoop. It divides processing into Map tasks that process data in parallel across cluster nodes and Reduce tasks that aggregate results. The programming model is designed for batch processing of large datasets, though it has been largely superseded by more user-friendly engines in modern deployments.

**YARN (Yet Another Resource Negotiator)** is the resource management layer introduced in Hadoop 2. It separates cluster resource management from application execution, allowing multiple processing engines (MapReduce, Spark, Tez) to share the same cluster resources. YARN manages node allocation, job scheduling, and cluster utilization.

## How It Works

Hadoop clusters consist of master nodes and worker nodes. The master node runs NameNode and ResourceManager services, coordinating data storage and task scheduling. Worker nodes run DataNode and NodeManager services, actually storing data and executing tasks. This distributed architecture allows linear scaling by adding more worker nodes.

Data processing in Hadoop follows a write-once, read-many pattern. Data is loaded into HDFS, then various processing jobs analyze it without modifying the source. This immutability simplifies fault tolerance, as failed tasks can simply be rerun on the same or different nodes without worrying about data consistency.

```java
// Example: Simple MapReduce word count program
public class WordCount {
    
    public static class TokenizerMapper 
            extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }
    
    public static class IntSumReducer 
            extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        
        public void reduce(Text key, Iterable<IntWritable> values,
                          Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
}
```

## Practical Applications

Hadoop powers numerous enterprise big data use cases:

- **Log Processing**: Analyzing application logs, clickstreams, and system metrics at scale
- **Data Warehousing**: Storing and analyzing historical data for business intelligence
- **Machine Learning**: Feature engineering and model training on large datasets
- **Data Lakes**: Centralized repositories for storing structured and unstructured data
- **ETL Pipelines**: Extracting, transforming, and loading data from various sources

## Examples

Components of the Hadoop ecosystem include:

- **Apache Spark**: In-memory processing engine much faster than MapReduce for many workloads
- **Apache Hive**: SQL-like query layer for data analysis on Hadoop
- **Apache HBase**: NoSQL database built on HDFS for random read/write access
- **Apache Kafka**: Distributed event streaming platform often used with Hadoop
- **Apache Zookeeper**: Coordination service for distributed systems

## Related Concepts

- [[Big Data]] - Datasets too large for traditional processing systems
- [[Distributed Computing]] - Computation across multiple machines
- [[MapReduce]] - Original batch processing model for Hadoop
- [[Data Engineering]] - Building data infrastructure and pipelines
- [[Spark]] - Next-generation processing engine often used with Hadoop

## Further Reading

- Apache Hadoop Documentation: hadoop.apache.org
- "Hadoop: The Definitive Guide" by Tom White
- Cloudera and Hortonworks tutorials (now combined)
- Hadoop community resources and mailing lists

## Personal Notes

Hadoop represents a pivotal technology that made big data processing accessible to organizations without massive supercomputer budgets. While MapReduce has been largely replaced by faster engines like Spark in new deployments, HDFS remains a cornerstone of data lake architectures. Understanding Hadoop's architectural decisions around fault tolerance and data distribution provides insight into distributed systems design principles that apply across many modern computing frameworks. The ecosystem continues to evolve, with cloud providers offering managed Hadoop services that reduce operational overhead while maintaining compatibility with existing applications.
