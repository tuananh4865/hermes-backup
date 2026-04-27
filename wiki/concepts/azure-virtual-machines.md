---
title: "Azure Virtual Machines"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [azure, cloud-computing, iaas, virtual-machines, microsoft]
---

# Azure Virtual Machines

## Overview

Azure Virtual Machines (VMs) is Microsoft's Infrastructure-as-a-Service (IaaS) offering that enables users to provision and manage virtualized compute resources in Microsoft's global cloud infrastructure. As one of the foundational services in Azure, VMs provide the maximum level of control over the operating system, storage, and networking configuration—making them suitable for workloads that require custom configurations, legacy applications, or specific licensing terms not available in higher-level platform services.

Azure VMs compete directly with Amazon EC2 and Google Compute Engine, forming the core compute triad of the public cloud market. Organizations choose Azure VMs when they need to lift-and-shift on-premises servers to the cloud, run Windows Server workloads, or deploy Linux environments with granular control. The service spans dozens of VM sizes optimized for compute, memory, storage, GPU, and high-performance computing scenarios.

## Key Concepts

### VM Sizes and Series

Azure offers specialized VM series optimized for different workloads:

| Series | Use Case | Examples |
|--------|----------|----------|
| **D/ds** | General purpose | D2s_v3, D4s_v3 |
| **E/es** | Memory optimized | E4s_v3, E64s_v3 |
| **F/fs** | Compute optimized | F2s_v2, F16s_v2 |
| **N/ND** | GPU/CUDA workloads | NC24s_v3, ND40s_v2 |
| **H/HB** | High performance computing | HB120rs_v2, H44m |

### Disks and Storage

Azure VMs support multiple disk types:
- **OS Disk**: Managed disk hosting the boot volume (up to 4TB)
- **Temporary Disk**: Local SSD storage (data lost on reboot)
- **Data Disks**: Additional managed disks (up to 32TB combined)
- **Ultra Disks**: Low-latency, high-throughput SSD for demanding workloads

### Networking

Each VM includes a network interface (NIC) that connects to an Azure Virtual Network (VNet). VMs can be assigned public IPs, placed behind load balancers, or connected via VPN to on-premises networks.

## How It Works

Provisioning an Azure VM involves selecting an image (Windows or Linux distribution), choosing a size, configuring storage, and networking. Azure handles the underlying hypervisor layer, physical hardware maintenance, and fabric management.

```bash
# Azure CLI example: Create a VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys

# Connect via SSH
ssh azureuser@<public-ip-address>
```

```powershell
# Azure PowerShell example: Create a Windows VM
New-AzVm `
  -ResourceGroupName "myResourceGroup" `
  -Name "myWindowsVM" `
  -Image "Win2019Datacenter" `
  -Size "Standard_D2s_v3" `
  -Location "eastus"
```

The lifecycle of a VM includes: Provisioning → Running → Stopped (deallocated) → Deleted. Stopped VMs don't incur compute charges but may still incur storage charges.

## Practical Applications

- **Lift-and-Shift Migrations**: Moving on-premises Windows or Linux servers to Azure with minimal code changes.
- **Development and Testing**: Rapidly provisioning dev/test environments that can be torn down when not needed.
- **Legacy Application Hosting**: Running applications that require specific OS configurations or older software versions.
- **GPU Computing**: Training ML models or running render farms on GPU-optimized VMs.
- **Disaster Recovery**: Using Azure as a DR site with VMs replicated from on-premises.

## Examples

**Web Server Farm Example**: An e-commerce company deploys 5 Ubuntu VMs behind an Azure Load Balancer, each running Nginx. They use an Availability Set to ensure 99.95% uptime SLA and Azure Database for MySQL for the product catalog.

**Windows Workload Example**: A line-of-business application requiring .NET Framework 4.8 runs on a Windows Server 2019 VM with SQL Server Enterprise. Azure Hybrid Benefit reduces licensing costs by applying existing Windows Server licenses.

**HPC Cluster Example**: A biotech research team provisions 100 NC24s_v3 VMs with InfiniBand networking to run molecular dynamics simulations across a parallel file system.

## Related Concepts

- [[cloud-computing]] — The broader category Azure VMs belong to
- [[iaas]] — Infrastructure as a Service model definition
- [[azure-functions]] — Azure's serverless compute alternative
- [[kubernetes]] — Running containers on Azure VMs via AKS
- [[azure-virtual-network]] — Networking foundation for Azure VMs

## Further Reading

- [Azure Virtual Machines Documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/)
- [Azure VM sizing guide](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)
- [Azure SLA for Virtual Machines](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements)

## Personal Notes

Azure VMs are deceptively simple—anyone can provision one in minutes—but running production workloads requires attention to architecture. Always use Availability Sets or Availability Zones for any production workload requiring SLA guarantees. Don't underestimate storage performance: Standard HDD disks will throttle your database. Azure Premium SSDs are worth the cost for I/O-intensive workloads. Also remember that VMs are your responsibility for patching, backups, and monitoring—Azure manages the hardware and hypervisor, not the guest OS.
