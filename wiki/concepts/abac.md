---
title: ABAC
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [security, access-control, authorization, attributes, rbac]
---

# ABAC (Attribute-Based Access Control)

## Overview

Attribute-Based Access Control (ABAC) is an access control model where authorization decisions are made by evaluating attributes associated with the subject requesting access, the resource being accessed, the action being performed, and the environmental conditions under which access is requested. Unlike simpler models that check only identity or role membership, ABAC can express complex, contextual policies that account for numerous factors simultaneously, enabling fine-grained access control in enterprise environments.

The fundamental insight behind ABAC is that access decisions often depend on more than just who you are. A user might legitimately access certain resources during business hours but not after. A clinician might access patient records for treatment purposes but not for personal research. A contractor might access project resources during an active engagement but lose that access upon project completion. ABAC captures these nuances through attributes that describe the state of subjects, resources, actions, and the environment.

Organizations increasingly adopt ABAC because traditional access control models prove inadequate for modern security requirements. Role-Based Access Control (RBAC), while simpler to administer, creates role explosion in complex organizations where many combinations of permissions are needed. Discretionary Access Control (DAC) relies on resource owners making access decisions, which doesn't scale well in enterprise environments. ABAC provides the flexibility of policy-based control while remaining manageable through automation and attribute federation.

## Key Concepts

**Subject Attributes** describe the entity requesting access. These include attributes of the user such as department, job title, security clearance, location, employment status, and certifications. Subject attributes can also include organizational membership, group affiliations, and relationship to the resource owner.

**Resource Attributes** characterize the object being accessed. For a document, resource attributes might include classification level, owner, creation date, department, project association, and sensitivity tags. For an API endpoint, resource attributes might include the service it belongs to and the data types it handles.

**Action Attributes** specify what the subject wants to do with the resource. Common actions include read, write, delete, execute, and administrative operations. ABAC policies can distinguish between actions at various granularities—accessing a database table versus accessing a specific row within that table.

**Environment Attributes** capture contextual factors unrelated to subject or resource. These include time of day, day of week, geographic location, device security status, network security zone, and current threat level. Environmental attributes enable policies that adapt to changing conditions.

**Policy** is a set of rules that define access decisions. ABAC policies are typically expressed in a policy language like XACML (eXtensible Access Control Markup Language) or AWS's IAM Policy Language. Policies specify conditions under which access is permitted or denied based on attribute combinations.

## How It Works

The ABAC authorization flow begins when a subject attempts to access a resource. The access control decision point—often called the Policy Decision Point (PDP)—receives the authorization request containing the subject's attributes, the resource's attributes, the requested action, and environmental context.

The PDP evaluates applicable policies against the attribute values in the request. Policies may permit, deny, or express no opinion on the request. The PDP applies policy-combining algorithms to resolve conflicts—for example, a deny decision might override permits, or most restrictive interpretations might apply.

ABAC systems often use an attribute provider or identity provider to supply subject attributes, which may be federated from HR systems, directory services, or external identity providers. Resource attributes come from the resource itself or from metadata stores. Environmental attributes are typically generated dynamically by the authorization system based on its monitoring of conditions.

The Policy Administration Point (PAP) manages policy creation, storage, and modification. Policies are often version-controlled and audited. The Policy Enforcement Point (PEP) intercepts access requests and implements the authorization decisions, typically by granting or denying access and potentially logging the attempt.

## Practical Applications

Healthcare organizations use ABAC to implement HIPAA-compliant access controls. A policy might state that a physician can access patient records for treatment purposes if the physician is currently assigned to that patient's care team and is accessing from an authorized device within the hospital network. The ABAC system evaluates attributes of the physician (role, department, current assignment), patient (record contents), action (type of access), and environment (device, location, time).

Cloud computing environments benefit from ABAC's flexibility. AWS IAM policies use attribute-based concepts, allowing policies that grant access based on tags, resource attributes, and conditions. This enables dynamic, policy-driven access control across large-scale cloud infrastructures.

Enterprise resource planning systems use ABAC to manage access to financial data, human resources information, and strategic documents. ABAC enables organizations to implement principle-of-least-privilege by granting access only when all required conditions are satisfied—a user might have read access to budget documents for their department but not others.

## Examples

```json
{
  "policy": {
    "description": "Allow clinicians to access patient records for treatment",
    "target": {
      "subjects": [
        {"attribute": "role", "matches": "clinician|doctor|nurse"}
      ],
      "resources": [
        {"attribute": "type", "matches": "medical-record"}
      ],
      "actions": [
        {"attribute": "type", "matches": "read"}
      ]
    },
    "conditions": [
      {"attribute": "treatment-relationship", "operator": "equals", "value": "true"},
      {"attribute": "access-time", "operator": "between", "value": ["06:00", "22:00"]},
      {"attribute": "device-secure", "operator": "equals", "value": "true"}
    ],
    "effect": "permit"
  }
}
```

```python
# Simple ABAC policy evaluation
from typing import Dict, Any, List

class ABACPolicy:
    def __init__(self, policy_dict: Dict[str, Any]):
        self.description = policy_dict.get("description", "")
        self.target = policy_dict.get("target", {})
        self.conditions = policy_dict.get("conditions", [])
        self.effect = policy_dict.get("effect", "deny")
    
    def matches(self, request: Dict[str, Any]) -> bool:
        # Check if request matches policy target
        for attr_type, patterns in self.target.items():
            request_value = request.get(attr_type, "")
            if not any(p["matches"] in request_value for p in patterns):
                return False
        return True
    
    def evaluate_conditions(self, request: Dict[str, Any]) -> bool:
        # Evaluate all conditions
        for condition in self.conditions:
            request_value = request.get(condition["attribute"])
            if request_value != condition.get("value"):
                return False
        return True
    
    def authorize(self, request: Dict[str, Any]) -> bool:
        if self.matches(request) and self.evaluate_conditions(request):
            return self.effect == "permit"
        return False
```

## Related Concepts

- [[access-control]] — General framework for controlling access to resources
- [[authorization]] — The process of determining if access should be granted
- [[rbac]] — Role-Based Access Control, a simpler alternative
- [[zero-trust]] — Security model that ABAC supports implementing
- [[identity-management]] — Managing identity and attributes in ABAC

## Further Reading

- NIST SP 800-162: "Guide to Attribute Based Access Control (ABAC) Definition and Considerations"
- Ferraiolo, D. F., et al. (2007). "Proposed NIST Standard for Role-Based Access Control"
- OASIS XACML TC: "eXtensible Access Control Markup Language (XACML)"

## Personal Notes

ABAC's complexity is both its strength and weakness. The policy authoring surface is vast, which enables precise access control but also creates opportunities for misconfiguration. I've seen organizations struggle with policy sprawl where dozens of policies interact in unexpected ways. Successful ABAC implementations invest heavily in policy testing, simulation environments, and logging that makes authorization decisions auditable. ABAC works best when attribute sources are well-managed and policies are version-controlled like code.
