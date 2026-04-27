---
title: "Threat Hunting"
created: 2026-04-20
updated: 2026-04-20
type: concept
tags: [threat-hunting, cybersecurity, detection, siem, mitre-attack]
sources: [MITRE ATT&CK, CAR, Elastic SIEM documentation, Splunk documentation]
---

# Threat Hunting

Threat hunting is a proactive cybersecurity practice that involves proactively searching through networks, endpoints, and datasets to detect and isolate advanced threats that evade traditional signature-based security tools. Unlike reactive detection, which waits for alerts or anomalies to trigger investigation, threat hunting assumes that adversaries are already present in the environment and actively seeks them out. This hunter mindset shifts the security paradigm from "prevent everything" to "find the threats that have already slipped through."

## Proactive Hunting vs Reactive Detection

Traditional security operations centers (SOCs) operate primarily in reactive mode: SIEMs generate alerts based on predefined rules, EDR tools flag known malicious behaviors, and analysts respond to these triggers. This approach has a fundamental limitation—it can only detect threats that match existing detection logic.

Proactive threat hunting inverts this assumption. Hunters operate under the hypothesis that a skilled adversary has already bypassed preventive controls and may be dwelling in the environment undetected. They use behavioral analysis, anomaly detection, and hypothesis-driven investigations to uncover indicators of compromise (IOCs) and attacker tactics that automated tools have missed. The output of a successful hunt is often new detection logic, updated rules, and enhanced monitoring that strengthens the organization's overall security posture.

Reactive detection excels at known-bad scenarios with clear signatures. Proactive hunting excels at finding unknown unknowns—novel attack patterns, fileless malware, living-off-the-land techniques, and persistent threats that have been operational for extended periods. Mature security programs integrate both approaches, using hunting insights to continuously improve reactive detection capabilities.

## Hypothesis-Driven Hunting

The scientific method underpins effective threat hunting. Hunters formulate hypotheses about potential adversary activity based on threat intelligence, environmental risk factors, and known attack patterns. A hypothesis might be as specific as "an attacker is using PowerShell-based keyloggers on finance department workstations" or as broad as "lateral movement is occurring via legitimate administrative tools."

This structured approach prevents hunting from becoming a random or inefficient exercise. The hunter selects a hypothesis, identifies relevant data sources, develops hunt queries or analytics, executes the investigation, and documents findings. If the hypothesis is unsupported, that is a valid outcome—the hunt still validates the absence of that particular threat. If the hypothesis is confirmed, the hunter escalates for incident response, develops new detections, and may uncover additional leads for further investigation.

Popular frameworks for hypothesis generation include the MITRE ATT&CK framework, which catalogs adversary tactics and techniques, and the Cyber Analytics Repository (CAR), which provides analytic specifications for detecting specific techniques.

## MITRE ATT&CK Framework

The MITRE ATT&CK framework has become the de facto taxonomy for describing adversary behavior. It organizes attack techniques across fourteen tactical categories—from initial access through impact—and provides detailed information about how each technique works, what data sources can reveal it, and what mitigations exist.

Threat hunters use ATT&CK in several ways. It serves as a checklist for coverage assessment: if hunters can map their detections to ATT&CK techniques, they can identify gaps in visibility. It enables threat-intelligence-driven hunting: when a new APT group is reported, hunters can study the group's known ATT&CK technique preferences and search their environment for those same patterns. It also provides a common language for sharing findings with peers and integrating new detections into security operations workflows.

ATT&CK Navigator is a commonly used tool that allows hunting teams to visualize coverage, annotate hunts, and track detection development over time. Organizations often maintain an internal ATT&CK coverage matrix that reflects their specific environment, data sources, and detection priorities.

## Cyber Analytics Repository (CAR)

While ATT&CK describes what adversaries do, CAR (Cyber Analytics Repository) describes how to detect those behaviors programmatically. CAR is a MITRE-hosted knowledge base of analytics aligned to ATT&CK techniques, each with a specification that includes data requirements, logic implementation, and example detections.

CAR analytics are particularly valuable for threat hunters because they reduce the time required to move from hypothesis to query. A hunter investigating potential credential dumping can reference CAR's implementation of LSASS memory access detection, understand what Windows security event logs are needed, and adapt the analytic logic to their specific SIEM or detection platform. CAR also provides a foundation for validation—hunters can test analytics against known-bad simulation data to confirm they function as intended before deploying to production.

## Threat Intelligence and TTPs

Cyber Threat Intelligence (CTI) provides the contextual knowledge that makes hunting efficient. CTI ranges from raw IOC feeds (malware hashes, C2 IP addresses, phishing domains) to strategic intelligence about adversary campaigns and motivations. For threat hunting, the most actionable CTI focuses on tactics, techniques, and procedures (TTPs)—the behavioral patterns that survive changes in specific malware, infrastructure, or campaigns.

When a threat intelligence report describes a new attack cluster, hunters extract the TTPs and immediately begin searching for them. This is the essence of intelligence-driven hunting: rather than waiting for an alert, hunters proactively test whether reported adversary behaviors are present in their environment. Sharing groups like ISACs, MISP, and commercial threat intelligence platforms provide access to TTP-based intelligence that directly informs hunt planning.

The quality of threat intelligence varies significantly. Hunters must evaluate intelligence for credibility, relevance, and timeliness. Stale or inaccurate intelligence can waste hunt resources or lead to false conclusions. Integrating threat intelligence with a hypothesis-driven workflow ensures that intelligence informs hunting without dictating it.

## Hunting Tools and Platforms

Modern threat hunting relies on data aggregation and analysis platforms that provide deep visibility across enterprise environments. Two of the most widely used platforms are Elastic SIEM and Splunk, both of which support hunting through powerful search pipelines, machine-learning-based anomaly detection, and integration with threat intelligence feeds.

Elastic SIEM provides prebuilt detection rules aligned to ATT&CK, interactive investigation timelines, and a flexible query language (KQL) that hunters use to explore data interactively. Its machine learning features can surface behavioral anomalies—such as a user accessing resources they have never touched before—that would be difficult to express in static rules. Elastic also integrates with Elastic Security, enabling hunters to pivot directly from a suspicious event to endpoint telemetry.

Splunk offers similar capabilities through its Search Processing Language (SPL), which allows hunters to construct complex queries across massive datasets. Splunk's Common Information Model (CIM) normalizes data from diverse sources, making hunting queries portable across different data types. The Splunk Security Essentials app provides hunting guidance, prebuilt searches, and detection coverage mapping to ATT&CK.

Beyond SIEMs, dedicated hunting tools include YARA rules for malware pattern matching, Velociraptor for endpoint forensic investigation, and memory forensics frameworks like Volatility for analyzing captured RAM samples. Hunting often involves correlating data across multiple sources—a suspicious network connection might be investigated by cross-referencing endpoint process telemetry, authentication logs, and DNS query history.

## Common Hunting Patterns

Certain hunting patterns recur frequently because adversaries consistently rely on the same underlying techniques to achieve their objectives. Understanding these patterns enables hunters to move efficiently from hypothesis to discovery.

**Lateral Movement**: Adversaries rarely compromise only the initial access point. They move laterally using remote desktop protocol, SMB, PsExec, or stolen credentials to reach high-value assets. Hunting for lateral movement involves analyzing authentication logs for impossible travel scenarios, unusual service creation on remote hosts, and administrative accounts being used across disparate systems. Event codes 4624 and 4672 on Windows, combined with network flow data, provide rich signals for lateral movement hunts.

**Privilege Escalation**: After gaining initial access, adversaries seek elevated privileges to achieve their goals. Hunting for privilege escalation means looking for unusual process injection, unexpected service creation with high privileges, or modifications to privileged group memberships. Windows security event logs capturing account changes, scheduled task creation, and token manipulation are primary data sources. On Linux, hunters monitor for sudo privilege escalations, SUID binary anomalies, and unexpected modifications to the sudoers file.

**Persistence**: Maintaining persistence allows adversaries to retain access despite reboots and credential rotations. Hunters look for unexpected registry modifications (Run keys, services), new scheduled tasks, unusual startup items, and modifications to WMI subscriptions. ATT&CK technique T1547 (Boot or Logon Autostart Execution) and T1050 (New Service) are frequent hunting targets.

**Data Exfiltration**: Exfiltration is often the final stage of an operation. Hunting for exfiltration involves monitoring unusual outbound traffic volumes, suspicious cloud storage uploads, large encrypted transfers over non-standard ports, and database query patterns that indicate bulk record extraction. Network egress monitoring and DLP logs are key data sources for these hunts.

## AI for Threat Hunting

Artificial intelligence is transforming threat hunting by enabling analysis at scales and speeds that human analysts cannot achieve alone. Machine learning models trained on baseline behavior can identify subtle anomalies—deviations in user activity patterns, unusual process behavior, or anomalous network communications—that indicate potential adversary activity.

AI assists threat hunting in several dimensions. Anomaly detection models reduce the hypothesis generation burden by automatically surfacing outliers for investigation. Natural language processing enables hunters to query security data using conversational language, democratizing hunting for less technical analysts. Graph-based machine learning can model relationships between entities—users, devices, applications, and data—and reveal suspicious clusters that would be invisible to linear analysis.

However, AI is a force multiplier for skilled hunters, not a replacement for them. AI models generate leads, but human analysts provide context, evaluate false positive rates, and make judgment calls about investigation priorities. Adversarial evasion is a real concern—sophisticated attackers understand ML model behaviors and may attempt to poison training data or craft attacks that bypass anomaly thresholds. Effective hunting programs use AI to augment human expertise, not to automate away the investigative thinking that makes hunting valuable.

---

## Related Concepts

- [[siem]] — Security Information and Event Management platforms used for data collection and hunting
- [[mitre-attack]] — The ATT&CK framework for adversary behavior taxonomy
- [[threat-intelligence]] — CTI and TTP-based intelligence driving hunt hypotheses
- [[endpoint-detection]] — Endpoint visibility and telemetry for hunting investigations
- [[incident-response]] — The response process following a successful hunt discovery
- [[yara]] — Pattern matching rules for malware and threat hunting

## Further Reading

- [MITRE ATT&CK](https://attack.mitre.org/) — Official ATT&CK framework documentation
- [MITRE CAR](https://car.mitre.org/) — Cyber Analytics Repository for detection analytics
- [Elastic SIEM Hunting Guide](https://www.elastic.co/guide/en/security/current/prebuilt-rules.html) — Prebuilt detection rules aligned to ATT&CK
- [Splunk Security Research](https://splunkbase.splunk.com/) — Hunting apps and detection content for Splunk
- "Threat Hunting in the Cloud" — AWS security blog on cloud-specific hunting patterns
- "The Hunter's Formula" by Robert M. Lee — Foundational reading on hypothesis-driven hunting methodology

---

*Last updated: 2026-04-20*
