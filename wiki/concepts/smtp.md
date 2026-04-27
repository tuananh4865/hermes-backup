---
title: "SMTP"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [smtp, email, networking, protocol, mail-server, devops]
---

# SMTP

## Overview

SMTP (Simple Mail Transfer Protocol) is the standard protocol for transmitting email across IP networks. It defines how email messages are submitted from a mail client to a mail server and how they are relayed between mail servers until they reach their destination. SMTP operates on a client-server model and uses [[TCP]] port 25 for server-to-server communication and port 587 for client-to-server message submission. While HTTP is the protocol that powers the web, SMTP is the protocol that powers email—every email sent across the internet travels through SMTP at some point in its journey.

SMTP was originally designed in 1982 as a simple text-based protocol for sending email between servers. Over time, it has been extended with authentication mechanisms, encryption via [[TLS]], and various commands to handle modern email requirements. Despite its age and some limitations (it was not originally designed with security in mind), SMTP remains the backbone of modern email infrastructure.

## Key Concepts

**SMTP Commands**: The protocol operates through a series of text-based commands sent from client to server:

```
HELO domain.com        # Identify sender's domain
MAIL FROM:<sender>     # Specify sender envelope address
RCPT TO:<recipient>    # Specify recipient envelope address
DATA                  # Begin message content
Subject: Hello        # Email headers
                     # Blank line
Message body...       # Email body
.                    # End with period on own line
QUIT                  # Close connection
```

**Mail Submission**: Modern email clients don't send mail directly to the recipient's server. Instead, they submit messages to a Mail Submission Agent (MSA) on port 587, which then relays to the recipient's server via port 25. This separation allows for proper authentication and spam filtering.

**SMTP Response Codes**: Servers respond with three-digit codes indicating success, failure, or intermediate status:

```
250 - Requested mail action okay, completed
354 - Start mail input; end with <CRLF>.<CRLF>
550 - Requested action not taken; mailbox unavailable
421 - Service not available, closing transmission channel
```

**MIME Encoding**: SMTP was originally designed for ASCII text only. [[MIME]] (Multipurpose Internet Mail Extensions) extends SMTP to handle binary attachments, HTML content, and international character sets by encoding them as ASCII-safe text.

## How It Works

An email's journey from sender to recipient involves multiple SMTP transactions:

1. **Message Submission**: The user's mail client (MUA - Mail User Agent) connects to their mail service provider's submission server on port 587 using SMTP. The client authenticates with a username and password, then sends the message.

2. **Message Relay**: The submission server examines the recipient address. If the recipient is not local, the server looks up the recipient's mail server via DNS [[MX records]]. It then opens a connection to that server on port 25 and relays the message.

3. **Message Delivery**: The recipient's mail server receives the message, performs spam and virus scanning, stores it in a mailbox, and notifies the recipient via [[IMAP]] or [[POP3]] that new mail has arrived.

4. **Delivery Status Notification**: If the message cannot be delivered after a retry period, the sending server generates a bounce message (Delivery Status Notification) and sends it back to the original sender.

```
# Example SMTP conversation
$ telnet mail.example.com 25
220 mail.example.com ESMTP Postfix
HELO client.example.com
250 mail.example.com
AUTH LOGIN
334 VXNlcm5hbWU6
dXNlckBleGFtcGxlLmNvbQ==
334 UGFzc3dvcmQ6
c2VjcmV0cGFzc3dvcmQ=
235 2.7.0 Authentication successful
MAIL FROM:<alice@example.com>
250 2.1.0 Ok
RCPT TO:<bob@recipient.com>
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject: Test Email
From: alice@example.com
To: bob@recipient.com

Hello Bob, this is a test message.
.
250 2.0.0 Ok: queued as 12345
QUIT
221 2.0.0 Bye
```

## Practical Applications

**Mail Server Administration**: System administrators configure and maintain SMTP servers using software like Postfix, Exim, Sendmail, or Microsoft Exchange. Key responsibilities include spam filtering, DKIM signing, SPF and [[DMARC]] configuration, and ensuring proper TLS encryption.

**Transactional Email Services**: Modern applications use SMTP-compatible APIs from services like SendGrid, Mailgun, or Amazon SES to send automated emails (password resets, order confirmations, notifications) without managing their own mail infrastructure.

**Email Marketing Platforms**: Mass email senders must comply with anti-spam regulations (CAN-SPAM, GDPR) and maintain proper authentication (SPF, DKIM, DMARC) to ensure deliverability and avoid being blocked by receiving mail servers.

**Mail Relay and Gateway Solutions**: Organizations often deploy SMTP relay servers or email gateways to add an extra layer of security, archive emails for compliance, or route traffic through specific channels.

## Examples

**Configuring Postfix for Gmail Relay** (`/etc/postfix/main.cf`):

```bash
# Configure Postfix to relay through Gmail
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_tls_security_options = noanonymous
smtp_tls_security_level = encrypt
tls_basic_pairs = allowed = gmail.com
```

**Testing SMTP with OpenSSL**:

```bash
# Test SMTP connection with TLS
openssl s_client -connect smtp.gmail.com:587 -starttls smtp

# Test SMTP authentication
swaks -tls -to recipient@example.com \
     -from sender@gmail.com \
     -server smtp.gmail.com:587 \
     -auth PLAIN \
     -auth-user sender@gmail.com
```

**MX Record Lookup**:

```bash
# Query DNS for mail servers
dig MX example.com
nslookup -type=MX example.com
```

## Related Concepts

- [[Email]] - The broader system of message transfer
- [[TCP]] - The reliable transport protocol SMTP runs on
- [[DNS]] - Used for MX record lookups to locate mail servers
- [[TLS]] - Provides encrypted SMTP connections
- [[IMAP]] - Protocol for retrieving email from a mail server
- [[POP3]] - Alternative protocol for retrieving email
- [[MIME]] - Encoding standard for email attachments and non-ASCII content
- [[SPF]] - Sender Policy Framework for email authentication
- [[DKIM]] - DomainKeys Identified Mail for email signing
- [[DMARC]] - Email authentication policy framework

## Further Reading

- [RFC 5321 - Simple Mail Transfer Protocol](https://tools.ietf.org/html/rfc5321)
- [Postfix Documentation](http://www.postfix.org/documentation.html)
- [Mozilla Developer Network - How SMTP Works](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/How_does_the_Internet_work#email)

## Personal Notes

SMTP is one of those protocols that feels old but remains absolutely critical to internet infrastructure. I find it helpful to think of it in stages: submission (port 587, authenticated), relay (port 25, server-to-server), and delivery (to the mailbox). The text-based nature of SMTP makes debugging with telnet or openssl s_client surprisingly practical. Understanding SMTP becomes essential when debugging email deliverability issues, configuring mail servers, or setting up transactional email services.
