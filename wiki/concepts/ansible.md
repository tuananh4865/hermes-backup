---
title: Ansible
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ansible, devops, automation, infrastructure]
---

## Overview

Ansible is an open-source IT automation platform that enables configuration management, application deployment, and infrastructure orchestration. Developed by Michael DeHaan and acquired by Red Hat in 2015, Ansible uses a declarative language to describe system configuration and automates repetitive tasks across servers and devices. Its primary distinguishing characteristic is its agentless architecture—unlike traditional automation tools that require software agents installed on target machines, Ansible connects to remote hosts over standard SSH (or WinRM for Windows) and executes tasks without any prior software installation on the target systems.

Ansible is designed with simplicity and ease of use as core principles. It uses human-readable YAML syntax for playbooks, making automation accessible to developers and system administrators who may not have extensive programming backgrounds. The platform handles everything from simple one-line tasks to complex multi-tier application deployments across thousands of machines. Its idempotent nature means that running the same playbook multiple times produces the same result, preventing unintended changes from repeated executions.

The ecosystem includes Ansible Galaxy, a community hub for sharing roles and modules, and Ansible Tower (now part of Red Hat Ansible Automation Platform), which provides enterprise features such as role-based access control, job scheduling, and graphical inventory management. Organizations of all sizes use Ansible to achieve consistent, repeatable deployments, reduce human error, and accelerate DevOps practices.

## How It Works

Ansible operates through a straightforward architecture that connects a control node (where Ansible runs) to managed hosts via standard network protocols.

**Inventory** is the foundation of Ansible's operation. It defines the list of managed hosts and organizes them into groups. Inventories can be static (written in INI, YAML, or as dynamic scripts that query cloud providers) or dynamic (pulling host lists from sources like AWS EC2, VMware, or custom CMDBs). Host patterns allow targeting specific machines or groups using flexible selection criteria, enabling operations on subsets of infrastructure with a single command.

**Modules** are the core building blocks of Ansible automation. They are pre-written programs that perform specific actions on managed hosts—packages, services, files, command execution, cloud resource provisioning, and much more. Ansible ships with thousands of built-in modules covering common system administration tasks, and the community contributes thousands more through Ansible Galaxy. Modules accept arguments, return JSON results, and are idempotent by design. When writing custom automation, modules execute on the target machine and communicate results back to the control node.

**Playbooks** are Ansible's orchestration documents. Written in YAML, they describe a desired state for systems and the steps to achieve that state. A playbook contains one or more plays, each targeting a set of hosts and defining tasks to execute. Tasks invoke modules with specific parameters, and Ansible ensures the system reaches the declared state. Playbooks support variables, templates, conditionals, loops, and error handling, enabling sophisticated automation workflows. Handlers within playbooks respond to task results, typically used to restart services when configuration changes occur.

**The Ansible Engine** coordinates execution. It reads the inventory, parses the playbook, and spawns temporary Python processes on managed hosts via SSH. For each task, Ansible connects to the target, executes the module, collects the JSON output, and reports the result. The engine handles parallelism, connecting to multiple hosts simultaneously to accelerate execution.

## Comparison

Ansible occupies a distinct position among configuration management and infrastructure automation tools, each with its own philosophy and trade-offs.

**Ansible vs. Chef**: Chef uses a procedural approach where recipes describe step-by-step how to configure systems. It requires an agent (chef-client) on every managed node and stores the desired state on a Chef Server. Ansible, by contrast, is agentless and uses declarative YAML that describes the end state rather than the implementation steps. Chef offers deeper programmability through Ruby, while Ansible prioritizes accessibility through simpler syntax. Chef's pull-based model provides strong consistency guarantees, whereas Ansible's push-based model offers simpler setup but requires direct connectivity.

**Ansible vs. Puppet**: Puppet also uses a pull-based agent architecture and enforces a declarative resource model. The primary distinction lies in language and architecture—Puppet uses its own domain-specific language (DSL) based on Ruby, while Ansible uses YAML and Python. Puppet maintains a centralized server (Puppet Master) and compiles catalogs for agents to apply. Ansible executes directly from the command line or via AWX/Ansible Tower without requiring a central server, reducing architectural complexity. Puppet excels in large-scale, continuously compliant infrastructures; Ansible excels in rapid deployment and ad-hoc task execution.

**Ansible vs. Terraform**: While often mentioned together, Ansible and Terraform serve different purposes. Terraform is an infrastructure-as-code tool focused on provisioning cloud resources and managing their lifecycle—it creates servers, networks, databases, and other infrastructure components. Ansible focuses on configuration management after infrastructure exists—installing packages, configuring services, deploying applications. Many organizations use both: Terraform for provisioning and Ansible for post-provisioning configuration. Terraform uses a declarative HCL language and maintains state files, while Ansible operates statelessly (except for facts gathering). The distinction has blurred with Ansible's inclusion of cloud modules, but the philosophical difference remains: provisioning versus configuration.

## Related

- [[Configuration Management]] - The practice of maintaining consistent systems configuration
- [[Infrastructure as Code]] - Managing infrastructure through machine-readable definition files
- [[ci-cd]] - Continuous integration and deployment workflows often integrated with Ansible
- [[DevOps]] - Cultural and technical practices where Ansible is commonly used
- [[SSH]] - The protocol Ansible uses to communicate with Linux/Unix hosts by default
- [[YAML]] - The human-readable data format used for Ansible playbooks
- [[Docker]] - Containerization technology often automated with Ansible
- [[Kubernetes]] - Container orchestration where Ansible can handle cluster provisioning and workload deployment
