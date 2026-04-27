---
title: Virtual Machine
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [virtualization, hypervisor, cloud-computing, containers, emulation]
---

## Overview

A virtual machine (VM) is a software-computed representation of a physical computer that can run its own operating system and applications as if it were a dedicated piece of hardware. The physical machine running the VM is called the **host**, and the VM itself is the **guest**. This abstraction layer enables multiple isolated guest systems to run concurrently on a single physical host, each with its own virtualized CPU, memory, storage, and network devices.

Virtual machines are the foundational technology behind cloud computing as we know it. When you spin up an instance on AWS EC2, Google Cloud, or Azure, you're typically getting a VM. They provide strong isolation boundaries between workloads, allowing different operating systems and application environments to coexist safely on the same hardware. This isolation is enforced by a combination of hardware assist features (Intel VT-x, AMD-V) and the hypervisor software layer.

## Key Concepts

**Type 1 Hypervisor (Bare-Metal)** runs directly on the hardware without a host operating system. Examples include VMware ESXi, Microsoft Hyper-V, and the Xen hypervisor used by Amazon Web Services. Type 1 hypervisors offer the best performance and security because they have minimal overhead and a smaller attack surface. Google Cloud and AWS both use customized Type 1 hypervisors to power their VM offerings.

**Type 2 Hypervisor (Hosted)** runs as an application within a conventional host operating system. VirtualBox, VMware Workstation, and QEMU in userspace mode are Type 2 hypervisors. They're primarily used for local development, testing, and running legacy applications on incompatible host systems. Performance is slightly lower than Type 1 due to the extra OS layer, but they're much easier to set up and manage.

**Emulation** goes a step further than virtualization: it allows code written for one architecture (e.g., ARM) to run on a different architecture (e.g., x86). QEMU is the most widely used general-purpose emulator. Rosetta 2 on Apple Silicon Macs uses emulation to run x86_64 applications. Emulation has more overhead than native virtualization but enables scenarios like running Windows binaries on Linux or iOS apps on macOS.

**Para-virtualization** is a technique where the guest OS is modified to be aware it's running in a VM, allowing it to communicate with the hypervisor more efficiently than through full hardware emulation. Modern hypervisors use this for specific devices (block and network drivers) to reduce emulation overhead.

## How It Works

When a VM is started, the hypervisor allocates a portion of the host's physical resources—CPU cores, RAM, disk space, and network interfaces—and presents them to the guest as virtualized or emulated hardware. The guest OS boots from a **virtual disk image**, which is typically a file or block device on the host.

The hypervisor intercepts privileged CPU instructions from the guest that would normally require hardware-level access. Rather than letting the guest directly manipulate hardware (which could destabilize other VMs), the hypervisor handles these calls. Hardware-assisted virtualization (Intel VT-x / AMD-V) provides CPU modes specifically for this, making the interception fast and secure.

VMs use **snapshots** to capture the complete state of a VM at a point in time, including memory, CPU state, and disk contents. This is invaluable for testing—you can snapshot a VM, experiment freely, and revert to the clean state in seconds. This capability underpins many CI/CD testing pipelines.

**Live migration** allows a running VM to be moved from one physical host to another with minimal downtime, which is critical for data center operations, load balancing, and hardware maintenance without service interruption.

## Practical Applications

Cloud computing is the most prominent application: every EC2 instance, Google Compute Engine VM, and Azure Virtual Machine is a VM running on a hypervisor in a data center. Cloud providers oversubscribe physical hosts (running more VMs than there are physical cores) because not all VMs run at full capacity simultaneously.

Development and testing environments heavily use VMs. Docker Desktop on macOS runs a Linux VM in the background to power its container runtime. Vagrant is a tool that automates the creation and provisioning of development VMs using VirtualBox or other hypervisors, making it easy to share reproducible environments.

Legacy application support is another use case: organizations running older line-of-business software that only works on Windows Server 2008 or similar can keep it running in a VM long after the hardware would have been decommissioned.

Security research and malware analysis often use VMs to safely execute untrusted code in isolated environments. If malware escapes its VM, it can still be contained—the host and other VMs remain protected.

## Examples

Starting a VM with QEMU:

```bash
# Run a lightweight Linux VM with 2 CPUs, 1GB RAM, and a 10GB disk image
qemu-system-x86_64 \
  -m 1024 \
  -smp 2 \
  -drive file=ubuntu-disk.qcow2,format=qcow2 \
  -net nic -net user,hostfwd=tcp::2222-:22 \
  -nographic
```

The `-drive file=ubuntu-disk.qcow2,format=qcow2` uses QEMU's copy-on-write format (qcow2), which allocates disk space lazily and supports snapshots. The `-net` flags set up NAT networking with port forwarding from host port 2222 to guest port 22.

Creating a VM snapshot with virsh (for KVM/libvirt):

```bash
virsh snapshot-create-as ubuntu-vm --name "before-upgrade" \
  --description "Clean state before kernel upgrade"
```

## Related Concepts

- [[containers]] — Lighter-weight isolation technology (Docker, rkt) that shares the host kernel
- [[hypervisor]] — The software layer that creates and runs VMs
- [[cloud-computing]] — VMs are the foundation of IaaS cloud offerings
- [[emulation]] — Running code for one architecture on another (related but distinct)
- [[kubernetes]] — Container orchestration that often runs on top of VMs

## Further Reading

- Intel's VT-x and AMD-V documentation for hardware-assisted virtualization details
- QEMU's official documentation at qemu.org
- VMware's technical whitepapers on Type 1 hypervisor architecture
- "Virtual Machines" by Smith and Nair (comprehensive academic text)

## Personal Notes

I keep a set of Vagrant VMs for testing different database versions and language runtimes locally. The ability to `vagrant destroy && vagrant up` to get a completely clean environment in under two minutes has saved me countless hours of dependency conflicts. The overhead of a full VM is noticeable compared to containers (you boot an entire OS), but the isolation and compatibility guarantees are worth it for anything that needs to closely mimic a production server environment.
