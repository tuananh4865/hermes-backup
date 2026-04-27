---
title: "Operating Systems"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [operating-systems, kernel, processes, memory-management, linux, windows]
---

## Overview

An operating system (OS) is system software that manages computer hardware resources and provides services to application programs. It acts as an intermediary between users and the computer hardware, enabling application software to execute without needing to understand the details of underlying hardware. The operating system is the fundamental software layer that makes modern computing practical and accessible.

The concept of an operating system emerged as computers evolved from running single programs to supporting multiple concurrent applications. Early computers required operators to manually load programs using front panel switches. As hardware became more capable, monitor programs emerged to handle program loading, I/O operations, and resource allocation—these evolved into modern operating systems.

Today's operating systems like Windows, macOS, Linux, iOS, and Android are extraordinarily complex software systems managing everything from keyboard input to network packets, from memory allocation to security permissions. They represent some of the largest and most thoroughly tested software ever created, with Linux containing over 30 million lines of code.

## Key Concepts

**Kernel** is the core of the operating system, running in privileged mode and controlling all hardware access. The kernel manages CPU time (scheduling), memory (virtual memory management), and I/O devices (drivers). Modern kernels are modular, allowing driver loading without rebooting. Linux has a monolithic kernel design, while Windows uses a hybrid kernel, and macOS uses a hybrid of XNU (Mach + BSD).

**Processes** are executing programs instances. Each process has its own memory space, file descriptors, and system resources. The OS performs context switching to share CPU time among processes, giving the illusion of parallelism on single-core systems and enabling true parallelism on multi-core systems.

**Virtual Memory** abstracts physical memory into a logical address space for each process. This isolation prevents processes from accessing each other's memory and allows using more memory than physically available via paging to disk. Virtual memory also enables memory-mapped files and copy-on-write fork operations.

**File Systems** organize data on storage devices. They provide hierarchical directory structures, files with metadata, and operations for reading, writing, and seeking. Common file systems include NTFS and exFAT (Windows), APFS (macOS), ext4 and XFS (Linux), and the cross-platform ISO 9660 and UDF.

**System Calls** (syscalls) are the controlled entry points from user space into kernel space. When a program needs kernel services—reading a file, allocating memory, creating a network connection—it executes a syscall. The kernel verifies the request, performs the operation, and returns results to user space.

**Scheduling** determines which process runs at any given time. Modern schedulers use complex algorithms balancing responsiveness (for interactive applications), throughput (for batch jobs), and fairness. The Completely Fair Scheduler (CFS) in Linux divides CPU time proportionally among processes.

## How It Works

When a computer boots, the BIOS or UEFI firmware initializes hardware and loads the operating system's kernel from storage into memory. The kernel initializes internal data structures, discovers and probes hardware, starts essential system processes (daemons in Unix, services in Windows), and finally presents a login interface to users.

```c
// Conceptual example of system call flow
// User space code requesting kernel service
int fd = open("/home/user/data.txt", O_RDONLY);
// This triggers:
// 1. User code places syscall number and arguments in registers
// 2. Software interrupt or syscall instruction transfers to kernel
// 3. Kernel handler validates arguments and permissions
// 4. Kernel performs operation (reads file from disk, caches in memory)
// 5. Kernel returns file descriptor to user space
// 6. User code continues with file descriptor
```

The kernel maintains several key data structures:
- **Process Control Block (PCB)** - Per-process information including registers, scheduling state, memory map
- **File Descriptor Table** - Maps file descriptors to open file objects
- **Inode Table** - Metadata for files on disk
- **Page Tables** - Virtual to physical memory mappings

## Practical Applications

Understanding operating systems is essential for:

**Software Development** - Debugging memory leaks, understanding performance characteristics, and writing efficient code requires knowing how processes, memory, and I/O work.

**System Administration** - Configuring servers, managing users, tuning performance, and troubleshooting issues all depend on OS knowledge.

**DevOps and Cloud** - Containerization (Docker, Kubernetes), virtual machines, and cloud infrastructure all rely on OS concepts like namespaces, cgroups, and virtualization.

**Security** - Operating system security features (selinux, AppArmor, Windows Defender), vulnerability analysis, and exploit development require deep OS understanding.

**Embedded Systems** - IoT devices, microcontrollers, and specialized hardware run operating systems (often Linux or RTOS) with real-time constraints.

## Examples

**Linux Process Management:**
```bash
# List all processes
ps aux

# Tree view of processes
pstree

# Monitor process activity
top    # or htop for interactive version

# View process file descriptors
ls -la /proc/$PID/fd/

# Check system limits
ulimit -a
```

**Windows System Information:**
```powershell
# List running services
Get-Service

# Check system information
systeminfo

# View event logs
Get-EventLog -LogName System -Newest 20

# Resource Monitor
resmon
```

**Memory Management in Linux:**
```bash
# View memory usage
free -h

# Detailed memory info
cat /proc/meminfo

# Memory pressure
vmstat 1

# Check for memory leaks (RSS growth over time)
ps -o pid,rss,vsz,cmd -p $(pgrep -f myprocess)
```

## Related Concepts

- [[Linux]] - The open-source Unix-like operating system kernel
- [[Windows]] - Microsoft's operating system family
- [[Processes]] - Executing program instances managed by the OS
- [[Virtual Memory]] - Memory abstraction provided by the OS
- [[File Systems]] - Data organization on storage
- [[Containers]] - OS-level virtualization (Docker, Podman)
- [[Kernel]] - The core of the operating system
- [[Shell Scripting]] - Scripting for Unix/Linux system administration

## Further Reading

- ["Operating System Concepts" by Silberschatz, Galvin, Gagne](https://www.os-book.com/)
- ["Linux Kernel Documentation"](https://www.kernel.org/doc/html/latest/)
- ["Windows Internals" by Russinovich, Solomon, Ionescu](https://docs.microsoft.com/en-us/sysinternals/resources/windows-internals)

## Personal Notes

The operating system is where software meets hardware. When debugging issues, I often start by checking OS-level metrics (CPU, memory, disk I/O, network) before examining application logs. Understanding `/proc` on Linux or Task Manager on Windows gives visibility into what's actually happening. For any serious software work, know your OS internals—virtual memory, process lifecycle, file descriptor management, and system call interfaces are universally relevant concepts.
