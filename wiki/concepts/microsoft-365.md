---
title: Microsoft 365
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [microsoft, productivity, cloud, collaboration, saas, office]
---

# Microsoft 365

## Overview

Microsoft 365 (formerly Office 365) is a comprehensive [[SaaS]] platform that bundles productivity applications, collaboration tools, and cloud services into a unified subscription. Where traditional Microsoft Office was a one-time-purchase suite of desktop applications, Microsoft 365 is a continuously updated, cloud-first service that includes always-current versions of Word, Excel, PowerPoint, and Outlook alongside enterprise-grade communication, security, and device management tools.

Microsoft 365 serves both SMB and enterprise markets, providing a single platform for email, document collaboration, video conferencing, calendar scheduling, file storage, identity management, and endpoint security. Its scale is enormous — Microsoft reports over 400 million commercial users as of 2024, making it one of the most widely adopted productivity platforms in the world.

## Key Concepts

**Plans and Licensing:** Microsoft 365 offers multiple tiers — Business Basic, Business Standard, Business Premium, Enterprise E3, and Enterprise E5. Higher tiers add advanced security features (Microsoft Defender), compliance tools (eDiscovery, data loss prevention), and analytics. Choosing the right plan matters significantly for organizations with specific regulatory or security requirements.

**Microsoft Graph:** The underlying API layer that connects all Microsoft 365 services. Graph provides a unified endpoint for accessing data across Teams messages, SharePoint files, Outlook emails, calendar events, and more. Most enterprise Microsoft 365 integrations are built on Microsoft Graph.

**Exchange Online:** Microsoft's hosted email and calendar service. Replaces on-premises Exchange servers, providing automatic archiving, malware/spam filtering, and shared mailboxes. Works seamlessly with the Outlook client across web, desktop, and mobile.

**Identity and Access:** Microsoft 365 relies heavily on [[Azure Active Directory]] (now called Microsoft Entra ID) for identity management. Conditional Access policies, multi-factor authentication, and single sign-on are core security features managed through the identity layer.

## How It Works

Microsoft 365 operates on a shared responsibility model. Microsoft manages the infrastructure, availability, and core service uptime, while customers manage users, permissions, and data governance. The services are accessed via web browsers, desktop clients, and mobile apps, all connected to Microsoft's global cloud infrastructure.

Key architectural layers:

1. **Identity Layer (Microsoft Entra ID):** All users are defined here. Authentication flows through this layer, which enforces MFA, Conditional Access, and SSO policies.
2. **Productivity Layer:** Includes Exchange Online (email), [[SharePoint]] Online (file storage/intranet), [[OneDrive]] (personal file storage), and Teams (communication).
3. **Collaboration Layer:** [[Microsoft Teams]] serves as the hub for chat, video meetings, and integration with third-party apps. Teams is deeply integrated with SharePoint — each team gets a SharePoint site with document libraries.
4. **Security Layer (Microsoft Purview/E5):** Data loss prevention, eDiscovery, audit logs, and information barriers.
5. **Device Management (Intune):** Mobile device management for controlling access from unmanaged devices.

```powershell
# Example: Connect to Microsoft Graph API via PowerShell
# Useful for automating user management and reporting
Connect-MgGraph -Scopes "User.Read.All", "Directory.Read.All"

# Get all licensed users
Get-MgUser -Filter "assignedLicenses/`$count ne 0" `
  -ConsistencyLevel eventual `
  -Select "displayName,mail,assignedLicenses"
```

## Practical Applications

- **Enterprise Email:** Replacing on-premises Exchange with Exchange Online for hosted email and calendar
- **Team Collaboration:** Using Microsoft Teams for internal communication, video calls, and project collaboration
- **Intranet and Document Management:** Building internal portals on SharePoint Online with automated workflows via Power Automate
- **Identity Consolidation:** Using Microsoft Entra ID as the single identity provider for all corporate applications (SSO)
- **Compliance and Governance:** Using Microsoft Purview to classify, retain, and eDiscovery-sensitive corporate data
- **Remote Work Enablement:** Microsoft 365 became central to remote work during COVID-19, with Teams usage surging dramatically

## Examples

- **Enterprise migrations:** Moving a 5,000-person organization from on-premises Exchange and file shares to Microsoft 365
- **Power Platform integration:** Using Power Apps and Power Automate to build custom workflows on top of SharePoint/Teams data
- **Microsoft Loop:** New collaborative workspace for real-time co-authoring, integrated with Teams
- **Copilot for Microsoft 365:** AI assistant integrated across Word, Excel, Teams, and Outlook, built on large language models

## Related Concepts

- [[Azure Active Directory]] (Microsoft Entra ID) — Identity and access management
- [[Microsoft Teams]] — Communication and collaboration hub
- [[SharePoint]] — Document management and intranet platform
- [[OneDrive]] — Personal cloud file storage
- [[SaaS]] — The service delivery model Microsoft 365 operates on
- [[Single Sign-On]] — How Microsoft 365 enables unified authentication
- [[Microsoft Defender]] — Security suite included in E5 plans

## Further Reading

- Microsoft 365 Admin Documentation: https://learn.microsoft.com/en-us/microsoft-365/
- Microsoft Graph API: https://developer.microsoft.com/en-us/graph
- Microsoft 365 Roadmap: https://www.microsoft.com/en-us/microsoft-365/roadmap

## Personal Notes

Microsoft 365 is both a productivity platform and an ecosystem lock-in story. The depth of integration between Teams, SharePoint, and Entra ID is genuinely powerful for enterprises, but it also makes migration away from it extremely costly. The Power Platform (Power Apps, Power Automate, Power BI) adds a significant low-code development layer on top that many organizations underutilize. Worth spending time learning Microsoft Graph — it's the key to automating anything in M365 at scale.
