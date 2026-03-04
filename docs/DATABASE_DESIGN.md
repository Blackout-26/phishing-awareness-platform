# 🏛️ Day 3 – Database Design (Multi-Tenant & Security-Enforced Schema)

**Objective:** Translate the architectural decisions from Day 2 into a structurally secure relational database design.

Day 3 formalizes the core entities, relationships, and enforcement constraints that guarantee multi-tenant isolation, data integrity, and analytics reliability.

This schema is designed not just to store data — but to enforce correct system behavior.

---

# 1. Design Philosophy

The database follows a **multi-tenant relational model** where:

* Every critical record is scoped to an Organization.
* All foreign keys are non-nullable.
* Data isolation is structurally enforced.
* Business rules are supported by constraints and indexing.

Security is embedded at the schema level, not left to application logic alone.

---

# 2. Core Entities & Relationships

## 2.1 Organization (Root Tenant Entity)

The top-level entity that ensures complete data isolation between clients.

Fields (conceptual):

* id
* name
* created_at
* updated_at

Design Rules:

* All major entities reference Organization via non-nullable ForeignKey.
* Deleting an Organization cascades to all dependent entities.
* No record exists without an organizational scope.

This is the foundation of multi-tenant security.

---

## 2.2 Campaign

Represents a phishing awareness simulation campaign.

Fields:

* id
* organization (FK → Organization)
* name
* status (DRAFT, AUTHORIZED, ACTIVE, COMPLETED, ARCHIVED)
* start_date
* end_date
* created_at

Lifecycle Enforcement:

* Default status = DRAFT
* Cannot transition to ACTIVE without Authorization record
* Tokens cannot be generated unless status = AUTHORIZED
* Events cannot be logged unless status = ACTIVE

Indexes:

* (organization_id, status)
* (organization_id, id)

The Campaign model controls system state integrity.

---

## 2.3 TargetUser

Represents individuals receiving simulation emails.

Fields:

* id
* organization (FK → Organization)
* email
* first_name
* last_name
* department (optional)
* created_at

Constraints:

* Unique email per organization
* Cannot exist without organizational scope

Indexes:

* (organization_id, email)

This ensures structured target management without cross-tenant overlap.

---

## 2.4 EmailTemplate

Stores reusable phishing simulation content.

Fields:

* id
* organization (FK → Organization)
* subject
* body
* created_at

Constraints:

* Scoped per organization
* Templates cannot be shared across tenants

Purpose:
Maintain clean content management while preserving data isolation.

---

## 2.5 TrackingToken (Security-Critical Entity)

Links a TargetUser to a specific Campaign.

Fields:

* id
* organization (FK → Organization)
* campaign (FK → Campaign)
* target_user (FK → TargetUser)
* token (UUID4, unique, 128-bit entropy minimum)
* created_at
* expires_at
* is_used (boolean)

Security Constraints:

* token must be globally unique
* Unique constraint on (campaign_id, target_user_id)
* Token expires when campaign closes
* Token validation required before event logging

Token Generation Standard:

* UUID4 or cryptographically secure random generator
* Non-sequential
* Non-predictable

This entity protects analytics integrity from token-guessing attacks.

---

## 2.6 Interaction Events

Two separate models for clarity and analytics precision.

### ClickEvent

Fields:

* id
* organization (FK → Organization)
* campaign (FK → Campaign)
* target_user (FK → TargetUser)
* token (FK → TrackingToken)
* ip_address
* user_agent
* classified_as (HUMAN / BOT / UNKNOWN)
* timestamp

### SubmissionEvent

Fields:

* Same structure as ClickEvent

Enforcement Rules:

* Cannot log event unless campaign.status == ACTIVE
* Token must exist and be valid
* Organization must match across related entities

Indexes:

* (organization_id, campaign_id)
* (organization_id, target_user_id)

Metadata Purpose:

* Supports Week 6 Interaction Classification (Bot vs Human)
* Enables forensic traceability

---

## 2.7 AuditLog (Governance Enforcement Entity)

Tracks all sensitive administrative actions.

Fields:

* id
* organization (FK → Organization)
* actor (FK → User)
* action_type
* object_type
* object_id
* metadata (JSONField)
* timestamp

Integrity Rules:

* Append-only design
* No update operations permitted
* No delete operations permitted
* Logs include timestamp + actor ID

Advanced Future Enhancement:

* Optional separation into dedicated logging database

This protects against insider misuse and ensures accountability.

---

# 3. Structural Enforcement Principles

## 3.1 Foreign Key Enforcement

* All relational links are non-nullable.
* Cascade deletion applied carefully at organization level.
* Referential integrity enforced at database layer.

---

## 3.2 Organization-Level Scoping

* Every major entity contains organization_id.
* All queries must filter by organization context.
* No global querysets permitted.

This prevents cross-tenant data leakage.

---

## 3.3 Indexing Strategy

Composite indexes applied to:

* (organization_id, campaign_id)
* (organization_id, target_user_id)
* (organization_id, status)

Purpose:

* Query efficiency
* Structural enforcement of tenant isolation

---

## 3.4 State-Driven Integrity

Business logic constraints supported by schema design:

* Campaign status controls token generation
* Campaign status controls event logging
* Authorization record required before activation

The database structure supports these enforcement mechanisms.

---

# 4. Day 3 Completion Criteria

Day 3 is complete when:

* All core entities are defined.
* Multi-tenant isolation is structurally enforced.
* Security-critical entities (TrackingToken, AuditLog) are designed defensively.
* Indexing strategy is defined.
* Schema supports Week 6 interaction classification without modification.

This schema demonstrates engineering maturity by embedding security, isolation, and governance directly into relational design.

The database is not just a storage layer — it is a security boundary.
