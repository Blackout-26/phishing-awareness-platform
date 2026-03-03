# 📄 Day 2 – Architecture + Mini Threat Modeling

**Objective:** Design the system securely from the very beginning.

Day 2 formalizes how system components interact and embeds defensive engineering decisions directly into the architecture. Security controls are defined at the structural level — not as optional enhancements.

---

# 1. High-Level Architecture Overview

The platform follows a **Modular Layered Monolith** architecture using Django.

### System Interaction Flow

Frontend → Backend → Database → Email Service

Each layer has strict responsibilities and security boundaries.

---

# 2. Component Breakdown

## Frontend (Presentation Layer)

* Admin dashboard (HTML/CSS templates)
* Campaign creation interface
* Analytics and reporting views

Responsibilities:

* Accept validated input
* Display campaign metrics
* Never contain business logic
* Never enforce security rules client-side only

All security validation is enforced server-side.

---

## Backend (Application + Domain Layers)

### Application Layer (Orchestration)

* Campaign lifecycle management (Draft → Authorized → Active → Closed)
* Token generation
* Email dispatch coordination (Celery tasks)
* Authorization enforcement
* Audit log recording

### Domain Layer (Core Intelligence)

* Risk scoring engine
* Click-through rate calculation
* Submission rate calculation
* Human vs Bot interaction classification

#### Interaction Classification Strategy

To prevent analytics pollution from automated email security scanners:

* User-Agent filtering
* Known security gateway pattern detection
* Heuristic detection (multiple clicks within milliseconds)
* Optional JavaScript execution validation for human confirmation

This ensures analytics integrity and reliable risk scoring.

---

## Database (PostgreSQL – Infrastructure Layer)

Stores:

* Organizations
* Users
* Campaigns
* Target Users
* Tracking Tokens
* Interaction Events
* Audit Logs

### Database-Level Data Partitioning

To mitigate data leakage:

* Every record is scoped to an Organization
* All queries enforce organization-level filtering
* Analysts can only access data belonging to their assigned organization
* No global querysets without enforced scoping

Data isolation is structural, not optional.

---

## Email Service (SMTP/API Integration)

* Sends simulation emails
* Uses background processing (Celery + Redis)
* Supports proper DNS configuration (SPF, DKIM, DMARC)

Purpose:

* Reliable delivery
* Reduced spam flagging
* Controlled campaign execution

---

# 3. Secure Tracking Token Design

To prevent predictable token abuse:

### Cryptographic Token Requirements

* Tokens generated using UUID4 or cryptographically secure random functions
* Minimum 128-bit entropy
* Non-sequential and non-predictable
* Associated with campaign + target user
* Validated before event logging
* Expire after campaign closure

This prevents token guessing and analytics poisoning.

---

# 4. Mini Threat Modeling – Abuse Risk Identification

Security risks are identified early and mitigated through engineering guardrails.

---

## Risk 1: Unauthorized Campaign Creation

Threat:
A user could launch phishing campaigns without proper legal authorization.

Impact:
Legal liability and ethical violation.

Engineering Guardrails:

* Campaign default status = Draft
* Mandatory CampaignAuthorization model
* Backend enforcement before activation
* Authorization timestamp + actor ID logged
* Activation blocked unless authorization record exists

---

## Risk 2: Data Leakage

Threat:
Sensitive interaction data exposed to unauthorized users.

Impact:
Privacy violations and regulatory exposure.

Engineering Guardrails:

* Strict Role-Based Access Control (RBAC)
* Organization-level query scoping
* Least-privilege enforcement
* Structural data partitioning at database query level

---

## Risk 3: Misuse by Insiders

Threat:
Privileged users abusing the system for unauthorized phishing.

Impact:
Severe legal and reputational consequences.

Engineering Guardrails:

* Comprehensive audit logging of all sensitive actions
* Append-only audit log design
* No update or delete operations permitted on audit records
* Logs include timestamp, actor ID, and action metadata
* Audit logs ideally stored separately from operational tables

Administrative users cannot modify their own activity history.

---

## Risk 4: Analytics Pollution via Automated Scanners

Threat:
Automated email security systems triggering false interactions.

Impact:
Inaccurate risk measurement.

Engineering Guardrails:

* User-Agent inspection
* IP-based filtering rules (configurable)
* Timing heuristics
* Human-verification logic

---

# 5. Purpose of Day 2

By the end of Day 2:

* Architecture layers are clearly defined.
* Data flow is structured.
* Token security is specified.
* Bot interference mitigation is planned.
* Audit log integrity is enforced by design.
* Database partitioning is structurally defined.

Security is embedded into the architecture — not layered on afterward.

This foundation ensures the platform demonstrates secure system design, not just functional implementation.
