---
title: Web Services
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web-services, api, distributed-systems, soa, microservices]
---

# Web Services

## Overview

Web services are software systems designed to support interoperable machine-to-machine interaction over a network. They provide a standardized way for applications to expose functionality and data to other applications, regardless of the underlying platforms, programming languages, or architectures involved. Web services form the foundation of modern distributed computing, enabling the rich ecosystem of connected applications and services that characterize today's internet.

The concept of web services emerged from the need to make enterprise software integration easier and more cost-effective. Before standardized web services, integrating different systems required custom point-to-point integrations that were expensive to build and maintain. Web services introduced the idea of a standard contract—WSDL for describing services, SOAP for protocol specification—that allowed any client to interact with any service that implemented the standard.

Today, web services encompass both the original SOAP-based approach and the more lightweight REST and GraphQL approaches that dominate modern web development. The term has become somewhat generic, referring to any service that exposes functionality via web protocols (HTTP/HTTPS). What unites all web services is their use of open, standards-based protocols for request and response handling.

## Key Concepts

**Service-Oriented Architecture (SOA)**: Web services are the building blocks of SOA, an architectural pattern that structures applications as collections of loosely coupled, interoperable services. SOA promotes reusability, maintainability, and flexibility by separating business logic into discrete services that can be combined in different ways.

**WSDL (Web Services Description Language)**: WSDL is an XML-based language that describes web services—what operations they support, what parameters they expect, and what responses they return. WSDL files serve as contracts between service providers and consumers.

**SOAP (Simple Object Access Protocol)**: SOAP is a protocol specification for exchanging structured information in web services. It defines message formats (XML), conventions for representing remote procedure calls, and rules for handling faults. While SOAP is powerful and highly standardized, its complexity led many developers to prefer simpler alternatives.

**REST (Representational State Transfer)**: REST is an architectural style rather than a protocol. RESTful web services use standard HTTP methods, stateless communication, and resource-oriented URLs. They're typically lighter and easier to implement than SOAP services, which led to widespread adoption.

**XML and JSON**: Early web services used XML for all data representation. Modern services often prefer JSON for its lighter weight and better fit with JavaScript. Many services support both formats.

**Service Discovery**: In dynamic environments, services need to find each other without hardcoded addresses. Service discovery mechanisms allow services to register themselves and other services to locate them. This is essential for microservice architectures and containerized deployments.

## How It Works

A typical web service interaction follows these steps:

1. **Service Definition**: The service provider publishes a WSDL or OpenAPI specification describing the service's interface
2. **Service Discovery**: The consumer finds the service through a registry or fixed URL
3. **Service Binding**: The consumer obtains the actual network address (endpoint) of the service
4. **Request Formation**: The consumer constructs a request according to the service specification
5. **Request Transmission**: The request is sent over HTTP/S to the service endpoint
6. **Service Processing**: The service receives, authenticates, validates, and processes the request
7. **Response Generation**: The service creates a response according to its specification
8. **Response Transmission**: The response is sent back to the consumer
9. **Response Processing**: The consumer parses the response and handles the result

```xml
<!-- Example SOAP Request -->
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetWeatherRequest xmlns="http://weather.example.com/wsdl">
      <City>San Francisco</City>
      <Country>USA</Country>
    </GetWeatherRequest>
  </soap:Body>
</soap:Envelope>

<!-- Example SOAP Response -->
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetWeatherResponse xmlns="http://weather.example.com/wsdl">
      <Temperature>18</Temperature>
      <Condition>Partly Cloudy</Condition>
      <Humidity>72</Humidity>
    </GetWeatherResponse>
  </soap:Body>
</soap:Envelope>
```

## Practical Applications

**Enterprise Application Integration (EAI)**: Large organizations use web services to integrate disparate systems—connecting ERP, CRM, and custom applications without custom integration code. This standardization reduces integration costs and makes it easier to swap out components.

**B2B Integration**: Companies exchange data with partners through web services. Order processing, inventory updates, and payment confirmations can flow automatically between trading partners' systems.

**Cloud Services**: Cloud providers expose their capabilities as web services. AWS, Google Cloud, and Azure all provide APIs that let developers programmatically manage cloud resources.

**Mobile Applications**: Mobile apps communicate with backends through web services. The backend logic, database access, and business rules are exposed via APIs that mobile clients consume.

**Internet of Things (IoT)**: IoT devices often communicate with central servers through web services. Sensors publish readings; actuators receive commands—all via standardized web service interfaces.

## Examples

**RESTful Weather Service**:

```http
GET /api/v1/weather?city=San+Francisco&country=USA HTTP/1.1
Host: api.weather.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "location": {
    "city": "San Francisco",
    "country": "USA"
  },
  "current": {
    "temperature": 18,
    "condition": "Partly Cloudy",
    "humidity": 72
  },
  "forecast": [
    { "day": "Monday", "high": 20, "low": 14 },
    { "day": "Tuesday", "high": 22, "low": 15 }
  ]
}
```

**GraphQL Service**:

```graphql
type Query {
  weather(city: String!, country: String): Weather
}

type Weather {
  location: Location!
  current: CurrentWeather!
  forecast: [DayForecast!]!
}

type Location {
  city: String!
  country: String!
}

type CurrentWeather {
  temperature: Int!
  condition: String!
  humidity: Int!
}
```

## Related Concepts

- [[api]] — General API concepts
- [[rest-api]] — RESTful API design
- [[soap]] — SOAP protocol details
- [[microservices]] — Modern architecture that uses web services
- [[wsdl]] — Service description language
- [[distributed-systems]] — Systems built on web services

## Further Reading

- [W3C Web Services Architecture](https://www.w3.org/TR/ws-arch/) — Official W3C specification
- "Service-Oriented Architecture" by Michael Rosen and Boris Lublinsky — Comprehensive SOA guide
- [REST API Tutorial](https://restfulapi.net/) — Practical REST design guide

## Personal Notes

The shift from SOAP/XML to REST/JSON was ultimately a win for developer experience. SOAP's rigor and enterprise features were valuable in certain contexts, but the simplicity of REST lowered the barrier to entry dramatically. Now you can expose a useful API in an afternoon rather than a month. This democratization of API creation has been a huge driver of innovation.
