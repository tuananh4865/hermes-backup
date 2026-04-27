---
title: "Apache Airflow"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-engineering, workflow-orchestration, apache, python]
---

## Overview

Apache Airflow is an open-source workflow orchestration platform written in Python. It enables developers to author, schedule, and monitor complex data pipelines and computational workflows. Originally created at Airbnb in 2014 and later donated to the Apache Software Foundation, Airflow has become a de facto standard for orchestrating extract-transform-load (ETL) pipelines, machine learning workflows, and data infrastructure automation.

Unlike simple cron job schedulers, Airflow provides a programmatic approach to workflow definition using Python code. This allows workflows to be version-controlled, tested, and collaborative—properties that are essential in modern data engineering teams. Airflow follows the philosophy that workflows should be defined as code, not YAML or drag-and-drop interfaces.

## Key Concepts

**DAGs (Directed Acyclic Graphs)** are the core data structure in Airflow. A DAG represents a collection of tasks with defined dependencies, organized in a directed graph with no cycles. Each DAG defines the execution order of tasks and the relationships between them. For example, a data pipeline might have tasks for extracting data, validating it, transforming it, and loading it into a data warehouse—with Airflow ensuring tasks execute in the correct order.

**Operators** are the atomic building blocks that define what actually gets executed. Airflow includes many built-in operators for common operations:
- `PythonOperator` - executes a Python function
- `BashOperator` - runs a bash command
- `SSHOperator` - executes commands over SSH
- `MySqlOperator`, `PostgresOperator` - interacts with databases
- `DockerOperator` - runs commands inside Docker containers

**Tasks** are instances of operators within a DAG context. Tasks become executable units when placed within a DAG structure.

**Executors** determine how tasks actually run. Airflow supports several executor types:
- SequentialExecutor - runs one task at a time (default, for testing)
- LocalExecutor - parallel task execution on a single machine
- CeleryExecutor - distributed execution across multiple machines
- KubernetesExecutor - dynamic task allocation in Kubernetes

## How It Works

Airflow's architecture consists of several components working together. The **Scheduler** is the heart of Airflow—it monitors all DAGs and tasks, triggering task instances when their dependencies are satisfied. The scheduler runs continuously as a background process, evaluating DAG runs and deciding what to execute next.

The **Web Server** provides the user interface (Airflow UI) for monitoring and managing workflows. Users can inspect DAG runs, view task logs, manually trigger executions, and configure connections. The UI is built with Flask and provides real-time status updates via a message queue.

**Workers** are the processes that actually execute tasks. Depending on the executor, workers may run on the same machine as the scheduler or across multiple machines in a cluster. Workers pick up tasks from a queue (Redis, RabbitMQ, or another broker) and execute them, reporting results back to Airflow's metadata database.

The **Metadata Database** (typically PostgreSQL or MySQL) stores all Airflow state: DAG definitions, task instances, execution history, connections, and configuration. This is the source of truth for the entire system.

**Message Broker** (Redis, RabbitMQ, Amazon SQS) enables communication between the scheduler and workers in distributed setups.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Daily ETL workflow',
    schedule_interval='0 2 * * *',  # Runs at 2 AM daily
)

def extract_data():
    print("Extracting data from source...")

def transform_data():
    print("Transforming data...")

def load_data():
    print("Loading data to warehouse...")

t1 = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

t3 = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

t1 >> t2 >> t3  # Define task dependencies
```

## Practical Applications

Apache Airflow is widely used across industries for data engineering and MLOps tasks. Common use cases include:

**ETL/ELT Pipelines** - Moving and transforming data between systems. Airflow can orchestrate complex data flows from APIs, databases, and file systems into data warehouses like Snowflake, BigQuery, or Redshift.

**ML Pipelines** - Automating the end-to-end machine learning lifecycle including data preprocessing, model training, evaluation, and deployment. Airflow can trigger model retraining on schedules or in response to data changes.

**Data Quality Monitoring** - Running validation checks on data at various pipeline stages, alerting when data quality degrades.

**Infrastructure Automation** - Managing cloud resources, orchestrating deployments, and automating DevOps workflows.

## Examples

A typical production Airflow setup might look like this:

```bash
# Initialize the Airflow database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start the scheduler in background
airflow scheduler --dag-id etl_pipeline &

# Start the web server
airflow webserver --port 8080
```

In a production Kubernetes environment, you might use the official Helm chart:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow \
    --set executor=CeleryExecutor \
    --set redis.enabled=true \
    --set postgresql.enabled=true
```

## Related Concepts

- [[Data Pipeline]] - General concept of moving and processing data
- [[Workflow Orchestration]] - The practice of coordinating complex task workflows
- [[ETL]] - Extract, Transform, Load pattern commonly implemented with Airflow
- [[Apache Spark]] - Often used alongside Airflow for large-scale data processing
- [[Docker]] - Containerization technology frequently used with Airflow operators
- [[Celery]] - Distributed task queue used by CeleryExecutor

## Further Reading

- [Apache Airflow Official Documentation](https://airflow.apache.org/docs/)
- ["Data Pipelines with Apache Airflow" by Bas Harenslak](https://www.manning.com/books/data-pipelines-with-apache-airflow)
- [Airflow GitHub Repository](https://github.com/apache/airflow)

## Personal Notes

Airflow excels when workflows require complex branching logic, conditional execution, or extensive monitoring. For simpler cron-like jobs, tools like Luigi or even simple cron may be more appropriate. The key learning curve is understanding the distinction between DAG structure (the workflow definition) and task execution (what actually runs). Always design DAGs to be idempotent—tasks should produce the same result regardless of how many times they run.
