---
title: Notifications
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [notifications, systems, messaging, alerts, push, events]
---

# Notifications

## Overview

Notifications are time-sensitive messages dispatched by a system, application, or service to inform a user — or another system — about an event, state change, or action that requires attention. In consumer technology, notifications appear on phones, watches, laptops, and TVs as banners, badges, sounds, or vibration patterns. In distributed computing and enterprise systems, notifications are the mechanism by which services communicate state changes, trigger workflows, and coordinate loosely coupled components.

The notification concept spans a wide range of implementations, from simple email alerts to sophisticated multi-channel notification engines that coordinate push notifications, SMS, email, and in-app messages through a single pipeline. Regardless of the medium, the core purpose is the same: delivering the right information to the right recipient at the right time, prompting a response or simply keeping them informed.

Modern notification systems must balance competing concerns: being informative enough to be useful, but not so frequent or intrusive that users disable them; delivering timely information while managing battery and network efficiency; and handling delivery failures gracefully when recipients are offline.

## Key Concepts

**Push Notifications** are messages initiated by a server (or notification service) and "pushed" to a client device without the client polling for them. On iOS, push notifications are delivered via APNs (Apple Push Notification service); on Android, via Firebase Cloud Messaging (FCM). Push notifications work even when the target app is not open, making them critical for engagement and real-time alerts. They require device tokens — unique identifiers issued by the platform's push infrastructure — to route messages to specific devices.

**Local Notifications** are scheduled and triggered entirely on the device without a server round-trip. An app schedules a notification for a future time, and the operating system delivers it even if the app is not running. Examples include calendar reminders, alarm clocks, and location-based alerts triggered when entering a geographic region.

**Notification Payloads** contain the data carried by a notification. A typical push notification payload includes a title, body text, a badge count, a sound name, and arbitrary key-value data for custom handling. On iOS, the payload is JSON sent to APNs; on Android, it's JSON sent via FCM. Developers can embed deep links in payloads to take users directly to a specific screen in the app when they tap the notification.

**Do Not Disturb (DND) and Notification Grouping** are OS-level controls that give users agency over notification frequency and presentation. iOS's Notification Center and Android's notification shade group notifications by app or topic, and both platforms allow granular per-app settings (critical, time-sensitive, delivered quietly, etc.). Effective notification design respects these user preferences rather than circumventing them.

**Notification Channels** (Android 8.0+) group notifications by type, allowing users to subscribe or mute entire categories. A messaging app might expose separate channels for direct messages, group chats, and promotional content. This gives users fine-grained control and reduces notification fatigue.

## How It Works

A push notification lifecycle:

1. **Token generation**: When an app installs on a device, it registers with the platform's push service (APNs or FCM) and receives a device token.
2. **Token exchange**: The app sends its device token to the application's backend server, which stores it in a database associated with the user.
3. **Trigger**: Some event occurs — a message is sent, a stock price crosses a threshold, a sensor reads an abnormal value — that warrants notifying the user.
4. **Send**: The backend constructs a notification payload and sends it to APNs/FCM, specifying the device token as the target.
5. **Route**: The push service (APNs/FCM) routes the notification to the correct device across the internet.
6. **Deliver**: The operating system receives the notification, applies user preferences (DND, Focus modes), and presents it to the user.
7. **Tap handling**: If the user taps the notification, the OS wakes the app (if not running) and delivers the payload, allowing the app to navigate to the relevant content.

For in-app notifications (notification feeds inside an app), the pattern is typically pull-based: the client polls an API endpoint or maintains a WebSocket connection to receive real-time updates, which are then rendered in a notification center UI within the app.

## Practical Applications

- **Chat and messaging apps**: WhatsApp, Telegram, Slack — delivering messages in real time
- **E-commerce**: Order confirmation, shipping updates, price drop alerts
- **Healthcare**: Appointment reminders, medication alerts, lab result availability
- **Financial services**: Stock price alerts, transaction fraud warnings, payment reminders
- **IoT and monitoring**: Server downtime alerts, temperature threshold breaches, security camera motion detection

## Examples

Sending a push notification via Firebase Cloud Messaging (HTTP v1 API):

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "token": "DEVICE_TOKEN_HERE",
      "notification": {
        "title": "New Message",
        "body": "Alice sent you a message"
      },
      "data": {
        "chat_id": "12345",
        "deep_link": "myapp://chat/12345"
      }
    }
  }' \
  "https://fcm.googleapis.com/v1/projects/MY_PROJECT_ID/messages:send"
```

## Related Concepts

- [[Messaging]] — The broader field of inter-person and system-to-person communication
- [[MMS]] — Multimedia Messaging Service, a carrier-level notification protocol for mobile
- [[APNs]] — Apple Push Notification service, Apple's infrastructure for iOS/tvOS/watchOS push notifications
- [[Firebase Cloud Messaging]] — Google's cross-platform push notification infrastructure
- [[WebSockets]] — Real-time bidirectional communication often used to supplement or replace polling for in-app notification feeds

## Further Reading

- [Apple Developer: UserNotifications Framework](https://developer.apple.com/documentation/usernotifications)
- [Firebase Cloud Messaging Documentation](https://firebase.google.com/docs/cloud-messaging)
- "Designing Notifications" by Scott Fisher — Essential reading on notification UX

## Personal Notes

Notification design is one of the most ethically nuanced areas of product development. Notifications are a powerful engagement tool, but they can also be manipulative — dark patterns around notification design (fake urgency, social validation loops) can create compulsive usage behaviors. I think deeply about notification frequency and value-per-alert when designing systems that reach users.
