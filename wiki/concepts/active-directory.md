---
title: "Active Directory"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [active-directory, microsoft, identity, authentication, ldap, windows, enterprise, directory-service]
---

# Active Directory

## Overview

Active Directory (AD) is Microsoft's proprietary directory service, introduced with Windows 2000 Server, that provides centralized identity management, authentication, and authorization services for Windows-based networks. It is the foundational identity and access management system for the majority of enterprise Windows environments, storing information about users, computers, groups, printers, and other network resources, and making this information accessible to authorized users and systems through a hierarchical, structured data store.

Active Directory follows the LDAP (Lightweight Directory Access Protocol) standard, meaning it functions as a directory service that organizes resources in a tree structure with domains and organizational units. It implements [[Kerberos]] as its default authentication protocol (though NTLM is supported for legacy compatibility) and provides single sign-on capabilities so users authenticate once and gain access to all authorized resources within the AD forest.

AD's architecture is built around several key concepts: the **forest** (the top-level logical container representing an organization), **domains** (logical groupings of AD objects that share a common namespace), **organizational units** (OUs, containers within domains used to organize objects for administrative delegation), and **sites** (physical network locations used to optimize replication and client authentication). Understanding these constructs is essential for anyone managing enterprise Windows infrastructure.

## Key Concepts

**Forest** is the top-level container and security boundary in Active Directory. A forest consists of one or more domains that share a common schema (defining object types and attributes), global catalog (enabling cross-domain searches), and trust relationships. Most organizations have a single forest, but larger or more complex organizations may have multiple forests with trust relationships between them.

**Domain** is a logical grouping of network objects (users, computers, groups) that share the same domain database and security policies. Each domain has a unique DNS name (e.g., `corp.example.com`) and is administered as a unit. Domains in the same forest automatically trust each other, allowing users in one domain to access resources in another.

**Organizational Units (OUs)** are containers within domains used to organize objects hierarchically. OUs are the primary delegation boundary in AD — you can assign administrative permissions to a specific OU to delegate management without granting full domain administrator rights. OUs are typically structured to mirror the organization's business structure or administrative responsibilities.

**Sites** represent physical locations or IP subnets in AD, separate from the logical domain structure. Sites control replication traffic between domain controllers and help clients find the nearest domain controller for authentication and LDAP queries. A domain can span multiple sites, and a site can contain multiple domains.

**Trust Relationships** establish authentication sharing between domains or forests. Parent-child trusts connect domains in the same tree. Tree-root trusts connect domains at the top of different trees in the same forest. Cross-forest trusts enable authentication between separate forests. All intra-forest trusts are transitive (if A trusts B and B trusts C, A trusts C).

**Group Policy Objects (GPOs)** are collections of settings that define how computers and users look and behave. GPOs are linked to sites, domains, or OUs and provide centralized management of user environments, security settings, software deployment, and system configuration. This is one of AD's most powerful management capabilities for controlling enterprise desktop configuration at scale.

## How It Works

Active Directory operates as a distributed database with multi-master replication, meaning any domain controller can accept changes and then replicate those changes to other domain controllers. This architecture provides both high availability (if one DC fails, others continue to serve authentication) and fault tolerance (replication ensures all DCs eventually converge to consistent data).

**Authentication Flow**: When a user logs into a Windows workstation joined to a domain, the authentication request goes to a domain controller. In a Kerberos authentication (the default for modern AD), the DC issues a Ticket-Granting Ticket (TGT) that the client uses to request service tickets for specific resources. This process is transparent to the user — they log in once and receive tickets for all resources they are authorized to access.

```powershell
# PowerShell: Common Active Directory administration tasks
# These commands require the RSAT (Remote Server Administration Tools) 
# or being run on a domain controller

# Find a user account
Get-ADUser -Filter {Name -like "*john*"} -Properties DisplayName, EmailAddress

# Create a new user
New-ADUser -Name "Jane Smith" `
    -GivenName "Jane" `
    -Surname "Smith" `
    -SamAccountName "jsmith" `
    -EmailAddress "jsmith@example.com" `
    -Path "OU=Users,OU=Corp,DC=example,DC=com" `
    -Enabled $true `
    -AccountPassword (ConvertTo-SecureString "P@ssw0rd123" -AsPlainText -Force)

# Add a user to a group
Add-ADGroupMember -Identity "Domain Admins" -Members "jsmith"

# List all members of a group
Get-ADGroupMember -Identity "Domain Admins" -Recursive

# Reset a user's password
Set-ADAccountPassword -Identity "jsmith" `
    -NewPassword (ConvertTo-SecureString "NewP@ssw0rd456" -AsPlainText -Force) `
    -Reset $true

# Find computers that haven't authenticated in 30 days
$threshold = (Get-Date).AddDays(-30)
Get-ADComputer -Filter {LastLogonDate -lt $threshold} `
    -Properties LastLogonDate, OperatingSystem
```

**LDAP Operations**: AD supports standard LDAP operations for directory queries and modifications. Applications can use LDAP to search for users, authenticate credentials, look up group memberships, and modify object attributes. Most enterprise applications that integrate with AD do so via LDAP or through higher-level interfaces like [[SAML]] or [[OAuth 2.0]] federated authentication.

**Replication**: AD uses a multi-master replication model where any domain controller can accept updates. Replication uses change notification to propagate changes between DCs within a site (fast, every 5 minutes by default) and scheduled replication between sites (slower, controlled by site link costs). Conflict resolution handles cases where the same object is modified on multiple DCs simultaneously.

**DNS Integration**: AD is tightly integrated with DNS. Domain controllers register SRV records in DNS that clients use to discover the nearest DC. Without proper DNS configuration, AD authentication and directory lookups fail. This DNS dependency means AD management always involves careful DNS administration.

## Practical Applications

Active Directory is used throughout enterprise Windows environments for:

**Single Sign-On (SSO)** is AD's most visible benefit. Users log in with their domain credentials once and are authenticated for email (Exchange), file shares (SMB/CIFS), internal web applications (via [[Kerberos]] or IWA), and any AD-integrated application. This reduces password fatigue and simplifies credential management.

**Centralized User and Computer Management** allows IT administrators to manage all network resources from a single console. User accounts, computer join requests, group memberships, and security policies are all administered through AD. Tools like Active Directory Users and Computers (ADUC), ADAC (Active Directory Administrative Center), and PowerShell provide different interfaces for AD management.

**Group Policy Management** enables IT to configure and control Windows environments at scale. GPOs can enforce password complexity policies, restrict software execution, configure security settings, map network drives, deploy printers, and set up user environments. A single GPO can apply to thousands of machines, making it a powerful tool for enterprise standardization.

**Access Control** through AD's built-in groups and ACLs (Access Control Lists) determines who can access what resources. Access control entries (ACEs) in ACLs define permissions at the object level. AD's group nesting allows flexible, hierarchical permission structures that mirror organizational structure.

**Application Integration** with [[OAuth 2.0]] and [[SAML]] identity providers: Modern applications often federate with AD via Azure Active Directory (now called Microsoft Entra ID) or directly via AD Federation Services (AD FS). This allows AD credentials to grant access to SaaS applications and cloud services while maintaining centralized identity management. See [[identity-provider]].

## Examples

A practical example of using AD for automated user provisioning:

```powershell
# PowerShell script: New employee onboarding via AD
# This script creates all the AD accounts and group memberships
# needed for a new employee

param(
    [Parameter(Mandatory=$true)]
    [string]$FirstName,
    
    [Parameter(Mandatory=$true)]
    [string]$LastName,
    
    [Parameter(Mandatory=$true)]
    [string]$Department,
    
    [Parameter(Mandatory=$true)]
    [string]$Manager
)

$displayName = "$FirstName $LastName"
$samAccountName = "$($FirstName[0])$LastName".ToLower()
$userPrincipalName = "$samAccountName@corp.example.com"
$email = "$samAccountName@corp.example.com"
$ou = "OU=$Department,OU=Users,DC=corp,DC=example,DC=com"

# Create the user account
New-ADUser -Name $displayName `
    -GivenName $FirstName `
    -Surname $LastName `
    -DisplayName $displayName `
    -SamAccountName $samAccountName `
    -UserPrincipalName $userPrincipalName `
    -EmailAddress $email `
    -Path $ou `
    -Manager $Manager `
    -Enabled $true `
    -AccountPassword (ConvertTo-SecureString "Welcome123!" -AsPlainText -Force) `
    -PasswordNeverExpires $false `
    -ChangePasswordAtLogon $true

# Add to department-specific groups
$groups = @(
    "Domain Users",
    "All Employees",
    "$Department Users"
)
foreach ($group in $groups) {
    try {
        Add-ADGroupMember -Identity $group -Members $samAccountName -ErrorAction Stop
        Write-Host "Added $samAccountName to $group"
    } catch {
        Write-Warning "Could not add to $group : $_"
    }
}

Write-Host "Account created: $samAccountName" -ForegroundColor Green
```

## Related Concepts

- [[LDAP]] — The protocol AD is based on; directory queries and operations
- [[Kerberos]] — The default authentication protocol used by AD
- [[Azure Active Directory]] — Microsoft's cloud identity platform, now called Microsoft Entra ID
- [[Single Sign-On]] — Core capability AD provides to enterprise users
- [[Identity Provider]] — AD acting as the authoritative source for identity
- [[OAuth 2.0]] — Modern authorization framework often federated through AAD/Entra
- [[SAML]] — Enterprise SSO protocol often used with AD Federation Services
- [[Group Policy]] — The system for centralized configuration management via AD
- [[Microsoft 365]] — Often integrated with AD for identity in cloud productivity suites
- [[Identity Management]] — The broader discipline AD serves

## Further Reading

- Microsoft Docs: Active Directory Domain Services — Official documentation
- "Windows Server 2019 Administration Fundamentals" — Practical AD administration guide
- [[ldap]]

## Personal Notes

> The most common AD mistake I see is deeply nested group structures that become impossible to audit — group memberships through 10 levels of nesting, circular group memberships, and security groups mixed with distribution groups. Enforce a flat group structure from the start with clear naming conventions. Also, never underestimate the DNS dependency — any DNS issue manifests immediately as AD authentication failures. Always have redundant, well-monitored DNS infrastructure supporting AD. Finally, test your GPOs in a pilot OU before deploying to all users; GPO loops and misconfigurations can lock users out of their machines en masse.
