---
title: "HTTP SMS API"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [sms, api, http, telecommunications, messaging, webhooks]
---

# HTTP SMS API

> This page was auto-created by [[self-healing-wiki]] to fill a broken link.
> Please expand with real content.

## Overview

An HTTP SMS API is a web service interface that enables developers to send and receive SMS text messages through programmatic HTTP requests. Rather than interacting directly with carrier networks or SMS gateways, developers use a standardized HTTP-based API to integrate SMS capabilities into applications. This abstraction layer handles the complexity of telecommunications protocols, carrier relationships, and message routing, allowing developers to focus on application logic.

HTTP SMS APIs typically support both outbound messaging (sending SMS from an application to end users) and inbound messaging (receiving SMS from users and routing them to applications via webhooks). They are the backbone of two-factor authentication (2FA), appointment reminders, marketing campaigns, customer notifications, and many other modern communication workflows.

## Key Concepts

**RESTful Endpoints** form the core of most HTTP SMS APIs. Standard operations include sending a message (POST), checking delivery status (GET), and managing opt-outs. Authentication is typically via API keys passed in headers.

**Webhooks** are HTTP callbacks that notify your application when an inbound message arrives or when the status of a sent message changes (delivered, failed, etc.). Your server must expose a publicly accessible endpoint to receive these notifications.

**Phone Number Formats** matter significantly. APIs generally accept E.164 formatted numbers (e.g., +14155552671) which include country codes. Proper formatting ensures messages reach the correct recipients globally.

**Message Segments** and **Character Encoding** affect SMS delivery. Standard SMS is limited to 160 characters using GSM-7 encoding. Longer messages are concatenated and split into multiple segments (using UDH headers), each charged as a separate message. Unicode characters use UCS-2 encoding, reducing the single-message limit to 70 characters.

**DLR (Delivery Receipt)** is the confirmation that a message was delivered to the carrier, not just accepted by the SMS gateway. Real DLR tracking requires proper configuration and patience—delivery can take seconds to hours.

## How It Works

The typical flow for sending an SMS via HTTP API:

1. Your application constructs an HTTP POST request with the recipient's phone number, message content, and your API credentials
2. The SMS provider validates credentials, checks for opt-out lists, and formats the message
3. The provider submits the message to upstream carriers/gateways
4. The carrier delivers to the recipient's device
5. The carrier sends a DLR back to the provider, who may webhook this to your application

For receiving SMS, the flow reverses:

1. A user sends an SMS to one of your dedicated numbers or a shared short code
2. The carrier delivers this to the SMS provider
3. The provider forwards it to your registered webhook URL via HTTP POST
4. Your application processes the inbound message and can respond by returning an HTTP response with outbound content

## Practical Applications

**Two-Factor Authentication (2FA)** uses SMS APIs to send verification codes during login. While SMS 2FA has known security weaknesses (SIM swapping), it remains widely deployed due to its accessibility—nearly every phone can receive SMS.

**Appointment Reminders** in healthcare, automotive service, and hospitality reduce no-shows by sending automated reminders 24-48 hours before appointments. These typically include the option to confirm or reschedule via reply.

**E-commerce Notifications** inform customers about order confirmation, shipping updates, and delivery windows. These transactional messages have high open rates (98% within 3 minutes).

**Marketing Campaigns** reach customers with promotions, loyalty rewards, and new product announcements. Compliance with regulations like TCPA and GDPR is critical—proper opt-in and opt-out mechanisms are mandatory.

## Examples

Sending an SMS with Python using the Twilio API:

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Your appointment is confirmed for tomorrow at 2:00 PM. Reply HELP for assistance or STOP to unsubscribe.",
    from_="+14155552671",
    to="+14155552672"
)

print(f"Message SID: {message.sid}")
print(f"Status: {message.status}")
```

Handling incoming SMS via a Flask webhook:

```python
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/webhook/sms", methods=["POST"])
def handle_sms():
    from_number = request.form.get("From")
    body = request.form.get("Body")
    
    # Process the incoming message
    response = process_message(from_number, body)
    
    # Return TwiML response for auto-reply
    return Response(
        f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>{response}</Message>
        </Response>""",
        mimetype="application/xml"
    )

if __name__ == "__main__":
    app.run(port=5000)
```

Checking message delivery status:

```python
message = client.messages("SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()
print(f"Status: {message.status}")  # queued, sent, delivered, failed, undelivered
print(f"Error code: {message.error_code}")  # Null if no error
print(f"Date sent: {message.date_sent}")
```

## Related Concepts

- [[self-healing-wiki]]
- [[REST API Design]] - Underlying architectural style for HTTP SMS APIs
- [[Webhooks]] - Callback mechanism for inbound SMS and status updates
- [[Two-Factor Authentication]] - Common use case for SMS APIs
- [[Telco Protocols]] - SS7, SMPP underlying carrier networks
- [[E.164 Phone Number Format]] - International standard for phone numbers

## Further Reading

- Twilio API Documentation — Industry-leading SMS API reference
- RFC 5724 (SMS URL Scheme) — URI scheme for SMS resources
- TCPA Compliance Guidelines — Legal requirements for US SMS campaigns

## Personal Notes

One surprising gotcha: SMS delivery is never guaranteed, and even "delivered" status from the carrier doesn't mean the user actually read the message—they might have it silenced or delivered to an archive. Also, testing is harder than other APIs because you need real phone numbers; you can't easily unit test SMS flows without using a service like ngrok to expose local webhooks.
