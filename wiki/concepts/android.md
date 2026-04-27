---
title: Android
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [android, mobile, operating-system, google]
---

# Android

## Overview

Android is Google's open-source mobile operating system designed primarily for smartphones and tablets. Originally developed by Android Inc., which was acquired by Google in 2005, the platform has grown to become the world's most widely used mobile operating system, powering billions of devices across virtually every manufacturer segment from budget devices to flagship smartphones.

Android is built on top of the [[Linux Kernel]] and provides a complete software stack that includes the operating system, middleware, and key mobile applications. The platform uses a modified version of the Linux kernel specifically adapted for mobile hardware, with additions like wakelocks, alarm timers, and the Binder inter-process communication mechanism that facilitate mobile-specific functionality.

The Android Open Source Project (AOSP) serves as the foundation for all Android devices, though most commercial devices run on Google Android which includes proprietary components like the Google Play Services, Chrome browser, and Google's suite of applications. This dual nature—open source core with proprietary extensions—has enabled both customization freedom and a consistent ecosystem that developers can target.

Google Play Store serves as the primary distribution channel for Android applications, though devices can also side-load apps from third-party sources, a flexibility that distinguishes Android from more closed platforms. This openness extends to the hardware layer, where manufacturers can build devices using a wide variety of chipsets, sensors, and form factors without requiring approval from Google.

## Architecture

Android's architecture follows a layered design pattern that separates concerns and provides clear interfaces between components.

At the foundation lies the **Linux Kernel**, which provides core operating system services such as process management, memory management, security, and hardware abstraction. Android uses a forked version of the upstream Linux kernel, modified with mobile-specific enhancements including the Binder driver for inter-process communication, low-memory killer for managing resources under pressure, and power management features optimized for battery operation.

Above the kernel sits the **Hardware Abstraction Layer (HAL)**, which defines standard interfaces that allow higher-level software to interact with hardware components without knowing implementation details. The HAL enables manufacturers to write hardware-specific code that exposes consistent APIs to the Android framework, supporting components like cameras, Bluetooth, Wi-Fi, sensors, and audio. This abstraction is crucial for supporting the diverse hardware ecosystem that characterizes Android devices.

The **Android Framework** forms the application development platform, providing Java/Kotlin-based APIs that developers use to build applications. Key framework components include the Activity Manager (controlling application lifecycle and navigation), Window Manager (handling screen layouts and display), Content Providers (enabling data sharing between applications), View System (building user interfaces), and Package Manager (managing app installation and permissions). The framework also includes the [[Java]] runtime environment adapted for mobile use.

**Native Libraries** sit beneath the framework layer, providing C/C++ libraries for performance-critical operations. These include [[SQLite]] for local database management, OpenGL ES for graphics rendering, the WebKit engine for web content, and various media codecs for audio and video playback.

At the top layer sit **Android Applications**, written primarily in [[Kotlin]] or Java, which run within the Android Runtime (ART) environment. The [[Android Runtime]] compiles application bytecode ahead of time, improving execution performance compared to traditional interpreter-based approaches.

## App Model

Android applications follow a component-based architecture organized around four fundamental building blocks: Activities, Services, Broadcast Receivers, and Content Providers. Each component serves a distinct purpose and can be activated independently, allowing applications to communicate and share functionality through well-defined interfaces.

**Activities** represent individual screens with user interfaces. An application typically consists of multiple activities, and users navigate between them to accomplish tasks. Each activity is a self-contained unit with its own lifecycle managed by the system, which can terminate background activities to reclaim memory when resources become constrained.

**Services** perform background operations without providing a direct user interface. Unlike activities, services continue running when the user switches to another application. They are essential for tasks like music playback, file synchronization, and long-running computations that should not be interrupted by navigation changes.

**Broadcast Receivers** listen for system-wide announcements and messages from other applications. The system uses broadcasts to notify apps of events like incoming SMS messages, network connectivity changes, low battery warnings, or the completion of device boot. This decoupled communication model enables applications to respond to system events without maintaining persistent connections.

**Content Providers** manage shared application data, exposing structured datasets through a consistent interface. They enable inter-application data sharing—for example, accessing the contacts database or photo gallery—without the applications needing direct database implementation knowledge.

The Intent system serves as the messaging infrastructure that connects these components. Intents can explicitly target a specific component, request a specific action from any capable component, or broadcast to all interested receivers. This flexible mechanism enables both tight integration within a single application and loose coupling between different applications.

Android applications run within their own sandbox, a security mechanism that isolates each app from others and from the operating system. By default, applications can only access their own resources and a limited set of system functions. Any capability beyond this requires explicit user permission grants at install time or runtime, depending on the sensitivity of the resource.

## iOS Comparison

Android and [[iOS]] represent the two dominant mobile platforms, each embodying fundamentally different design philosophies and ecosystem approaches.

From a **software perspective**, Android's openness contrasts with iOS's closed model. Android permits side-loading of applications from sources outside the official app store, while iOS restricts installation to the App Store except through developer programs or enterprise deployment. This gives Android users greater flexibility but also exposes them to higher security risks from malicious software. iOS maintains tighter control over its platform, which enables more consistent user experiences and faster optimization across devices.

The **hardware ecosystem** differs dramatically between the platforms. Android runs on devices from hundreds of manufacturers with vastly different specifications, screen sizes, and capability levels. This fragmentation creates challenges for developers who must test across many configurations, but provides consumers with unprecedented choice in price points, designs, and features. iOS, by contrast, runs exclusively on Apple's own devices, enabling precise optimization and consistent behavior.

In terms of **application development**, both platforms offer mature SDKs and robust developer tools, though with different language requirements. Android development traditionally uses Kotlin or Java within Android Studio, while iOS development uses [[Swift]] or Objective-C in Xcode. Cross-platform frameworks like [[React Native]] and [[Flutter]] have emerged to enable code sharing between platforms, though they sacrifice some native performance and integration.

**Security models** take different approaches. iOS implements uniform hardware-backed security across all devices, with features like the Secure Enclave for cryptographic operations and consistent application sandboxing. Android's security varies by device manufacturer and Android version, though recent versions have introduced more consistent security primitives. Both platforms have matured significantly in addressing mobile security threats.

**Ecosystem integration** varies based on platform loyalty. iOS integrates tightly with other Apple products through features like Handoff, AirDrop, and iCloud synchronization. Android connects broadly across manufacturers and works well with Google services, but ecosystem coherence depends on the specific devices and brands involved.

## Related

- [[Linux Kernel]] - The foundational operating system kernel
- [[Kotlin]] - Primary language for Android development
- [[iOS]] - Android's primary mobile competitor
- [[Java]] - Traditional Android development language
- [[Android Runtime]] - Execution environment for Android applications
- [[Mobile Operating Systems]] - Broader category of mobile platforms
- [[Google]] - The company behind Android
- [[Open Source Software]] - Android's development model
