---
title: "LDAP"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ldap, directory-service, authentication, active-directory, identity, networking, devops]
---

# LDAP

## Overview

LDAP (Lightweight Directory Access Protocol) is an open, vendor-neutral protocol for accessing and maintaining distributed directory information services. A directory service is a specialized database optimized for reading, searching, and browsing operations rather than frequent writes. LDAP provides a standard way for applications to query and modify information about users, groups, computers, and other resources in a hierarchical directory structure.

LDAP is the protocol that powers Microsoft's [[Active Directory]] and many other enterprise identity management systems. It serves as the backbone for single sign-on (SSO) authentication, centralized user management, and address book services in organizations ranging from small businesses to large enterprises. Whether you're logging into a workstation, accessing corporate resources, or authenticating to a VPN, LDAP is often working behind the scenes to verify your identity.

The protocol was developed in the early 1990s as a lighter-weight alternative to the complex X.500 directory access standard. LDAP v3, the current version, has been an IETF standard since 1997 and adds important features like SASL authentication, TLS encryption, and the ability to extend the protocol with custom operations.

## Key Concepts

**Directory Structure (DIT)**: LDAP directories organize data in a hierarchical tree structure called the Directory Information Tree (DIT). At the top is the root, followed by country nodes (dc=com), organization nodes (dc=example, dc=com), and finally organizational units (ou=users, ou=groups) containing actual entries.

**Distinguished Names (DN)**: Every entry has a unique identifier called a Distinguished Name that represents its full path in the directory tree:

```
dn: uid=jsmith,ou=users,dc=example,dc=com
dn: cn=admins,ou=groups,dc=example,dc=com
```

**LDAP Attributes**: Entries consist of attributes that hold data. Common attributes include:

| Attribute | Description |
|-----------|-------------|
| `uid` | User ID |
| `cn` | Common Name |
| `mail` | Email address |
| `sn` | Surname |
| `givenName` | First name |
| `memberOf` | Group memberships |
| `userPassword` | Encrypted password |

**Object Classes**: Entries are defined by object classes that specify which attributes are required and optional:

```ldif
# Example LDAP entry
dn: uid=jsmith,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jsmith
cn: John Smith
sn: Smith
givenName: John
mail: jsmith@example.com
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/jsmith
```

**LDAP Schemas**: Schemas define the rules for what object classes and attributes exist in the directory. Multiple schemas can be combined, and organizations often create custom schemas for their specific needs.

## How It Works

LDAP follows a client-server model where clients connect to a directory server (such as OpenLDAP, Microsoft Active Directory, or 389 Directory Server) to perform operations:

1. **Connection Establishment**: The client initiates a [[TCP]] connection to the LDAP server, typically on port 389 (unencrypted) or port 636 (LDAPS - LDAP over SSL/TLS).

2. **Binding (Authentication)**: Before accessing directory data, the client must bind to the server. Simple bind transmits username and password in plaintext; SASL (Simple Authentication and Security Layer) supports stronger mechanisms like Kerberos, client certificates, or hashed passwords.

3. **Operations**: The client performs operations against the directory:
   - **Search**: Query entries matching criteria
   - **Add**: Create new entries
   - **Modify**: Update existing entries
   - **Delete**: Remove entries
   - **Compare**: Check if an attribute matches a value

4. **Result Processing**: The server returns results, typically multiple entries for search operations.

5. **Unbind**: The client closes the connection.

```bash
# Example LDAP search using ldapsearch
ldapsearch -x -H ldap://ldap.example.com:389 \
           -b "ou=users,dc=example,dc=com" \
           -D "uid=admin,ou=users,dc=example,dc=com" \
           -W \
           "(uid=jsmith)"

# Add a new user
ldapadd -x -H ldap://ldap.example.com:389 \
        -D "cn=admin,dc=example,dc=com" \
        -W <<EOF
dn: uid=newuser,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: newuser
cn: New User
sn: User
mail: newuser@example.com
userPassword: secretpassword
EOF
```

## Practical Applications

**Active Directory**: Microsoft Windows networks rely on LDAP (via AD-specific extensions) for authenticating users to domain-joined computers, managing group policies, and controlling access to network resources like file shares and printers.

**Single Sign-On (SSO)**: Centralized authentication systems use LDAP to validate credentials across multiple applications. When you log into one application and gain access to others without re-authenticating, LDAP is often the underlying directory being queried.

**Centralized User Management**: Instead of maintaining separate user accounts on every server and application, organizations create a central LDAP directory. New employees get one account that grants them access to all authorized resources.

**Address Book Services**: LDAP directories store contact information for email clients, VoIP systems, and corporate directories. Many email clients can query LDAP servers to autocomplete recipient addresses.

**System Authentication**: Linux and Unix systems use LDAP (via PAM and NSS) to authenticate users against a central directory instead of local `/etc/passwd` files.

## Examples

**LDAP Authentication in Python**:

```python
import ldap

# Connect to LDAP server
conn = ldap.initialize('ldap://ldap.example.com:389')
conn.protocol_version = ldap.VERSION3
conn.set_option(ldap.OPT_REFERRALS, 0)

# Bind (authenticate)
try:
    user_dn = "uid=jsmith,ou=users,dc=example,dc=com"
    conn.simple_bind_s(user_dn, 'userpassword')
    print("Authentication successful")
except ldap.INVALID_CREDENTIALS:
    print("Invalid username or password")

# Search for user
results = conn.search_s(
    "ou=users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=jsmith)",
    ["mail", "cn", "memberOf"]
)
for dn, attrs in results:
    print(f"DN: {dn}")
    print(f"Email: {attrs.get('mail', [b'N/A'])[0].decode()}")
    print(f"Groups: {attrs.get('memberOf', [])}")

conn.unbind_s()
```

**OpenLDAP Server Configuration** (`/etc/openldap/slapd.conf`):

```bash
# Basic OpenLDAP configuration excerpt
include /etc/openldap/schema/core.schema
include /etc/openldap/schema/inetorgperson.schema
include /etc/openldap/schema/posixaccount.schema

database bdb
suffix "dc=example,dc=com"
rootdn "cn=admin,dc=example,dc=com"
rootpw {SSHA}encrypted_password_here
directory /var/lib/ldap
index objectClass eq
```

## Related Concepts

- [[Active Directory]] - Microsoft's directory service built on LDAP
- [[Authentication]] - The general concept LDAP is used for
- [[Kerberos]] - Often used alongside LDAP in enterprise environments
- [[Single Sign-On]] - Authentication systems that may use LDAP
- [[DNS]] - Used for LDAP server discovery via SRV records
- [[TLS]] - Encrypts LDAP traffic (LDAPS)
- [[PAM]] - Pluggable Authentication Modules can use LDAP
- [[NSS]] - Name Service Switch can use LDAP for user lookups
- [[Identity Management]] - The broader field LDAP serves

## Further Reading

- [RFC 4511 - Lightweight Directory Access Protocol (LDAP)](https://tools.ietf.org/html/rfc4511)
- [OpenLDAP Documentation](https://www.openldap.org/documentation/)
- [Active Directory LDAP Schema Documentation](https://docs.microsoft.com/en-us/windows/win32/ad/active-directory-schema)

## Personal Notes

LDAP can seem intimidating at first with its hierarchical structure and cryptic attribute names, but once the model clicks—it's essentially a specialized read-heavy database organized like a file system—everything becomes clearer. I recommend starting with understanding DN paths and object classes before diving into replication, access controls, and schema design. When debugging LDAP issues, `ldapsearch` is your best friend; being able to manually query the directory often reveals whether the problem is in the application or the directory configuration itself.
