# Day 4 – Tracking Flow Design

## Objective

Define the precise lifecycle of a phishing simulation interaction and establish the security boundaries governing token generation, validation, and event logging. This stage translates the previously designed architecture and database schema into a clear runtime interaction model.

Designing this flow early ensures the platform produces reliable metrics while preventing manipulation, data corruption, or unauthorized event injection.

---

# 1. End‑to‑End Interaction Lifecycle

When a phishing simulation campaign is active, the platform processes user interactions through a strictly defined sequence of events.

## Step 1 — Email Dispatch

A background worker (Celery) initiates email delivery for each campaign target.

For every **TargetUser–Campaign pair**, the system:

* Generates a **unique TrackingToken**.
* Associates the token with the TargetUser and Campaign.
* Embeds the token inside a phishing simulation URL within the EmailTemplate.

Example structure:

```
https://simulation-domain.com/track/<token>
```

The email is then sent via the configured SMTP service.

This token acts as the **unique identifier that ties every future interaction back to the campaign and recipient**.

---

## Step 2 — Link Click (Tracking Endpoint)

When the recipient clicks the link inside the email, the request reaches the platform's **tracking endpoint**.

At this stage the backend performs several actions:

1. Extract the token from the request URL.
2. Resolve the token against the database.
3. Capture request metadata including:

   * IP Address
   * User-Agent
   * Timestamp

This information forms the raw interaction dataset used later for analytics and bot filtering.

---

## Step 3 — Token Validation and Click Logging

Before any event is recorded, the system performs strict validation checks.

A click is only accepted if:

* The **TrackingToken exists** in the database.
* The **associated campaign status is ACTIVE**.
* The **token has not expired**.

If validation succeeds:

* A **ClickEvent** is written to the event log.
* The token is marked as **is_used = True**.

The system then redirects the user to the phishing simulation landing page.

If validation fails, the request is discarded without logging a valid interaction.

---

## Step 4 — Landing Page (Credential Simulation)

The user arrives at a simulated login interface designed to replicate a common authentication workflow.

If the user submits the form:

* The token is validated again.
* A **SubmissionEvent** is recorded.

Important security rule:

**No plaintext credentials are ever stored.**

The platform records only the **fact that a submission occurred**, not the contents of the submitted fields.

This ensures the simulation remains ethical and compliant with security best practices.

---

## Step 5 — Educational Disclosure Page

After the interaction completes, the user is redirected to a **training disclosure page** explaining that the interaction was part of a phishing awareness simulation.

The page includes:

* Explanation of phishing risks
* Indicators the email could have revealed the attack
* Security awareness guidance

This step ensures the platform serves its intended role as both **assessment and training tool**.

---

# 2. Secure Token Generation and Validation

Tracking tokens are the core security mechanism that ensures each interaction is uniquely attributable.

## Token Generation

Tokens must be generated using **cryptographically secure randomness**.

The recommended implementation uses:

* UUID4
* or equivalent high‑entropy random identifiers

Key requirements:

* Non‑sequential
* Non‑predictable
* Globally unique

This prevents attackers from guessing valid tokens and injecting fake interaction events.

---

## Token Validation Rules

Before logging any interaction, the platform enforces the following checks:

1. Token must exist.
2. Token must be linked to a valid TargetUser.
3. Campaign must be ACTIVE.
4. Token must not be expired.

Failure of any rule results in the request being rejected.

---

# 3. Reliability and Auditability Guardrails

To maintain reliable analytics and forensic traceability, the platform includes several engineering safeguards.

## Idempotent Click Handling

Users may click the same email link multiple times.

For accurate risk metrics:

* The **first click** is used for primary risk scoring.
* Additional clicks may still be recorded for behavioral analysis.

This prevents metric inflation while preserving useful behavioral data.

---

## Bot Filtering Preparation

Modern email security gateways often pre‑scan links automatically.

To prepare for interaction classification implemented later in development:

The tracking endpoint **must always capture the User‑Agent header**.

This data enables future detection techniques such as:

* Known scanner user‑agent filtering
* Heuristic bot detection
* IP pattern analysis

These mechanisms allow the system to differentiate between **human interactions and automated security scanners**.

---

# Summary

The tracking flow defines how phishing simulation interactions move through the system from email delivery to final educational disclosure.

By combining:

* cryptographically secure tokens
* strict validation rules
* structured event logging
* metadata capture for classification

…the platform ensures that all collected data remains accurate, auditable, and resistant to manipulation.

This interaction model forms the foundation for the **analytics and awareness metrics engine** implemented in later stages of development.
