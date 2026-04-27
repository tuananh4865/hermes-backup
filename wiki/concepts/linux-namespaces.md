---
title: Linux Namespaces
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [linux, containers, isolation, kernel, namespaces, cgroups]
---

## Overview

Linux namespaces are a kernel feature that partitions kernel resources so that one set of processes sees one set of resources while another set of processes sees a different set. They are the fundamental isolation mechanism underlying Linux containers (Docker, rkt, LXC) and many other isolation technologies. By wrapping a set of processes in their own namespace, you can give those processes the illusion that they have exclusive access to certain system resources—network interfaces, process trees, mount points, user IDs, hostnames, or inter-process communication channels—when in fact the host system is shared.

Namespaces were introduced incrementally into the Linux kernel starting with kernel 2.4.19 (2002) for the initial IPC namespace, and the feature has been expanded significantly since then. The combination of namespaces for isolation and [[cgroups]] for resource limiting forms the core of the Linux container ecosystem.

## Key Concepts

There are **7 main types of namespaces** in modern Linux:

**PID Namespace** isolates the process ID number space. Processes in different PID namespaces can have the same PID (e.g., PID 1 inside a container is a completely different process from PID 1 on the host). Child PID namespaces are nested within parent namespaces—only the outer (host) namespace contains all processes. This is one reason containers can see a clean "init" process (PID 1) inside them.

**Network Namespace** isolates network resources: network interfaces (eth0, wlan0), routing tables, firewall rules (iptables/nftables), port bindings, and `/proc/net`. Each network namespace has its own independent network stack. This is why multiple containers can each bind to port 80 or 443 without conflict—each sees a different set of ports.

**Mount Namespace** isolates the set of filesystem mount points visible to a process. This is how `chroot` was improved upon: instead of just changing the root directory, mount namespaces allow completely private filesystem views. Containers use this to present their own root filesystem (the container image layers) without seeing the host's filesystem.

**User Namespace** isolates user and group ID mappings. Inside a user namespace, a process can have UID 0 (root) without actually being root on the host. User namespaces are the key to running rootless containers—they allow privilege separation without full root privilege on the host.

**UTS Namespace** isolates hostname and domainname. Processes in a UTS namespace can set their own hostname and domain name, which they see but doesn't affect the host or other namespaces.

**IPC Namespace** isolates System V IPC objects and POSIX message queues. Processes in different IPC namespaces don't see each other's message queues or shared memory segments.

**Cgroup Namespace** (added in Linux 4.6) isolates cgroup membership view, so processes see a different cgroup hierarchy—useful to prevent containers from escaping their resource limits by referencing cgroups on the host.

## How It Works

Namespaces are manipulated through system calls: `clone()` creates a new process with a new namespace, `unshare()` moves the calling process into new namespace(s), and `setns()` joins an existing namespace. The `/proc/[pid]/ns/` directory shows the namespaces a process belongs to, and each namespace has an inode number—processes in the same namespace share the same inode for their namespace file.

```bash
# View namespaces of a running container's init process
ls -la /proc/1/ns/

# Example output showing all 7 namespaces:
# ipc (4026531839) - System V IPC namespace
# mnt (4026531840) - Mount namespace
# net (4026531836) - Network namespace
# pid (4026531834) - PID namespace
# user (4026531837) - User namespace
# uts (4026531838) - UTS namespace
# cgroup (4026531835) - Cgroup namespace

# Enter a container's namespace to inspect it
nsenter --target 1234 --net --pid -- ls -la
```

When a container runtime (Docker, containerd) creates a container, it calls `unshare()` to create new namespaces for the container's processes, then execs the container's main process inside those namespaces. The container runtime typically runs as a privileged process on the host to set up the namespace infrastructure.

## Practical Applications

**Container Runtimes** are the primary consumer of namespaces. Docker creates a new network, PID, mount, UTS, and IPC namespace for each container. The combination of namespaces for isolation and cgroups for resource limiting (CPU, memory, I/O) gives containers many of the properties of virtual machines—strong isolation, reproducibility—without the overhead of a full hypervisor.

**Kubernetes Pods** share several namespaces among containers in the same pod: PID namespace (containers can see each other's processes), network namespace (containers share the same IP and port space), and IPC namespace (containers can communicate via shared memory or signals). This is why containers in a pod can communicate via `localhost`.

**VPN and Network Isolation** can use network namespaces to isolate VPN connections. Run the VPN in one namespace and route specific traffic through it, while other processes on the system remain unaffected. This is more flexible than system-wide VPN configuration.

**Chroot and Pivot Root** are predecessors to mount namespaces, but mount namespaces provide much stronger isolation. Modern container images use overlay filesystems combined with mount namespaces to layer filesystem changes without affecting the base image.

## Examples

Creating a simple isolated environment with unshare:

```bash
# Create a new mount namespace with a private root
unshare --mount --propagation private /bin/bash

# Inside this bash session, mount a new filesystem that won't affect the host
mount -t tmpfs tmpfs /tmp
echo "Isolated /tmp visible only in this namespace" > /tmp/test
cat /tmp/test  # Works inside
# Exit and the mount is gone from the host view
```

Creating a network namespace and assigning an interface:

```bash
# Create a new network namespace
ip netns add isolated_ns

# Create a virtual ethernet pair
ip link add veth0 type veth peer name veth0-peer

# Move one end into the namespace
ip link set veth0-peer netns isolated_ns

# Assign addresses
ip addr add 10.0.1.1/24 dev veth0
ip netns exec isolated_ns ip addr add 10.0.1.2/24 dev veth0-peer

# Bring interfaces up
ip link set veth0 up
ip netns exec isolated_ns ip link set veth0-peer up
```

## Related Concepts

- [[cgroups]] — Control groups that limit and isolate resource usage (CPU, memory)
- [[containers]] — The broader technology built on namespaces and cgroups
- [[docker]] — The most popular container runtime built on Linux namespaces
- [[kubernetes]] — Container orchestration that relies on namespace isolation
- [[chroot]] — Predecessor to mount namespaces

## Further Reading

- `man namespaces` — The official Linux namespace manual page
- `man unshare` — System call documentation for creating namespaces
- The Linux kernel source documentation at kernel.org
- "Linux Namespaces" series by Michael Kerrisk (author of The Linux Programming Interface)

## Personal Notes

I use `ip netns` frequently when debugging container networking issues. Most people don't realize that network namespaces persist on the host even after Docker is stopped—leftover namespaces from improperly cleaned containers can cause confusion. Running `ip netns list` to see what's lingering has saved me hours of debugging "port already in use" errors. Also worth knowing: user namespaces are the key to rootless containers (which run without root on the host), and they've been enabled by default in most distros since around 2015, but they require careful configuration to avoid UID mapping conflicts.
