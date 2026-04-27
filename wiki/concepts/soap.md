---
title: "SOAP"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [soap, api, protocol, web-services, xml, soa]
---

# SOAP

## Overview

SOAP (Simple Object Access Protocol) is a messaging protocol specification for exchanging structured information in web services using XML. First introduced by Microsoft in 1998 and later standardized by the W3C, SOAP defines a formal contract between client and server using Web Services Description Language (WSDL) and relies on underlying transport protocols—typically HTTP or SMTP—to carry the XML-encoded messages. SOAP was the dominant web services technology in the early 2000s, particularly in enterprise environments, before the rise of lighter-weight [[rest-api]] approaches.

The "Simple" in Simple Object Access Protocol is somewhat ironic, as SOAP implementations are often anything but simple. The XML message format, strict envelope/header/body structure, and extensive WS-* specification extensions (WS-Security, WS-ReliableMessaging, WS-Addressing, and others) create a powerful but heavyweight framework suitable for enterprise integration scenarios requiring formal contracts, ACID-compliant transactions, and sophisticated security.

SOAP's strict typing and formal service description (via WSDL) make it particularly valuable in environments where contract stability and interoperability across diverse platforms are paramount. Banks, healthcare systems, government agencies, and ERP integrations have historically favored SOAP for these reasons. Despite REST's dominance for public web APIs, SOAP remains deeply embedded in enterprise backend systems, and many legacy integrations—particularly those involving [[xml]]-based data exchange—continue to operate in production today.

## Key Concepts

**SOAP Envelope** is the root element of every SOAP message, containing optional Header elements and a mandatory Body element. The envelope defines the overall message structure and can be extended via the Header for cross-cutting concerns like authentication, transaction management, and routing.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://example.com/order">
  <soap:Header>
    <tns:AuthToken>abc123xyz</tns:AuthToken>
  </soap:Header>
  <soap:Body>
    <tns:GetOrderRequest>
      <tns:orderId>12345</tns:orderId>
    </tns:GetOrderRequest>
  </soap:Body>
</soap:Envelope>
```

**WSDL (Web Services Description Language)** is an XML-based contract language that formally describes a SOAP service's operations, message formats, data types, transport bindings, and endpoint location. WSDL enables service discovery and code generation—tools can consume a WSDL and automatically generate client or server stubs in any supported language.

**SOAP Bindings** define how SOAP messages are transmitted over a network. The most common binding is HTTP, where SOAP messages are POSTed to a specified URL with a `Content-Type: text/xml` header. SMTP bindings are occasionally used for asynchronous, store-and-forward scenarios.

**WS-* Specifications** are a family of extensions built on top of SOAP that address enterprise requirements:
- **WS-Security**: Digital signatures, encryption, and authentication tokens for message-level security
- **WS-ReliableMessaging**: Guaranteed message delivery with ordering and deduplication
- **WS-Addressing**: Metadata in SOAP headers for routing messages to specific endpoints
- **WS-Transaction**: ACID-compliant distributed transaction coordination

**SOAP Faults** are the mechanism for reporting errors. A SOAP Fault element within the Body carries error codes, human-readable messages, and optional application-specific error details.

```xml
<soap:Body>
  <soap:Fault>
    <faultcode>soap:Client</faultcode>
    <faultstring>Invalid order ID format</faultstring>
    <detail>
      <tns:ErrorDetail xmlns:tns="http://example.com/order">
        Expected numeric string, received: abc
      </tns:ErrorDetail>
    </detail>
  </soap:Fault>
</soap:Body>
```

## How It Works

A typical SOAP exchange follows a request-response pattern over HTTP:

1. The client constructs an XML SOAP message according to the service's WSDL contract, populating the Body with operation parameters and any required Header elements (authentication, correlation IDs, etc.).
2. The client POSTs the SOAP message to the server's endpoint URL with appropriate HTTP headers (`Content-Type: text/xml`, `SOAPAction` header specifying the operation).
3. The server receives the message, parses the XML, validates it against the WSDL contract, processes the request, and constructs a response SOAP message (or a SOAP Fault if an error occurred).
4. The server returns the response as an HTTP response with a 200 OK (success) or 500 Internal Server Error (SOAP fault) status code.
5. The client parses the response XML and returns control to the calling application code.

This synchronous request-response model differs from message-oriented middleware or event-driven architectures. Each call blocks until a response is received, which can be problematic in high-latency scenarios or when loose coupling is required.

## Practical Applications

SOAP continues to power critical enterprise integrations:

- **Financial Services**: Payment gateways, banking core systems, and stock trading platforms often expose SOAP interfaces for their reliability, transactional guarantees, and formal contracts.
- **Healthcare**: HL7 v2 and emerging FHIR standards have largely replaced SOAP in healthcare, but legacy integrations with insurance providers and pharmacy systems still run on SOAP.
- **Government**: Many government agencies (tax authorities, customs, business registries) maintain SOAP-based web services for official data exchange.
- **ERP Integration**: SAP, Oracle ERP, and Microsoft Dynamics commonly expose SOAP APIs for integrating with external systems.

## Examples

Calling a SOAP web service from Python using the `zeep` library:

```python
from zeep import Client
from zeep.transports import Transport
from requests import Session

# Configure HTTP session with authentication
session = Session()
session.auth = ('username', 'password')

# Create SOAP client from WSDL
client = Client(
    'https://example.com/services/OrderService?wsdl',
    transport=Transport(session=session)
)

# Call a SOAP operation
response = client.service.GetOrder(orderId='12345')

# Response is a Python object derived from the WSDL schema
print(f"Order Status: {response.status}")
print(f"Total: ${response.totalAmount}")
```

## Related Concepts

- [[rest-api]] — The architectural style that largely supplanted SOAP for public web APIs
- [[web-services]] — The broader category of services accessed over a network
- [[xml]] — The markup language underlying all SOAP messages
- [[wsdl]] — The contract language for describing SOAP services
- [[api-design]] — Principles for designing programmatic interfaces

## Further Reading

- [W3C SOAP Specification](https://www.w3.org/TR/soap/) — The official SOAP 1.2 specification
- [Understanding SOAP](https://www.soapui.org/learn/articles/understanding-soap/) — Practical SOAP guide
- [wsdl4noobs](https://github.com/pedrohb29/wsdl4noobs) — WSDL introduction guide

## Personal Notes

SOAP has an unfairly negative reputation in some circles, partly because the early 2000s saw a lot of over-engineered "enterprise service bus" implementations that made everything SOAP-shaped whether it needed to be or not. The backlash toward REST was partly a correction for that excess. But SOAP's formal contracts (WSDL), message-level security, and transactional support are genuinely valuable for specific integration scenarios. The WSDL-to-client generation story is also underrated—having a machine-readable contract that can generate typed client libraries in any language is powerful for polyglot environments. My take: SOAP is the right tool when you need formal contracts, transactional integrity, and/or WS-Security for an enterprise integration. For everything else, [[rest-api]] with OpenAPI is probably the better choice.
