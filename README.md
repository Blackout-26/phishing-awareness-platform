# Phishing Awareness Simulation Platform

## Executive Summary

The **Phishing Awareness Simulation Platform** is a professional cybersecurity system designed specifically for **authorized security testing and employee awareness measurement**.

The platform converts otherwise invisible human susceptibility to phishing attacks into **measurable security intelligence** through controlled and ethical phishing simulations.

Its primary goal is to help organizations:

* Measure human security risk
* Identify awareness gaps
* Provide actionable remediation guidance
* Deliver executive‑level security reporting

By transforming user interaction data into structured metrics, the system strengthens what is commonly referred to as the organization's **"human firewall"**.

---

# System Architecture

The platform follows a **Modular Layered Monolith architecture**, providing strong separation of responsibilities while maintaining operational simplicity and maintainability.

### Frontend

Administrative dashboards and analytics interfaces built using Django templates.

Responsibilities:

* Campaign creation and management
* Visualization of campaign metrics
* Executive reporting dashboards

### Backend

Core application logic powered by Django.

Responsibilities:

* Campaign lifecycle management
* Tracking token generation and validation
* Interaction logging
* Risk scoring and analytics processing

### Database

PostgreSQL using a **multi‑tenant relational schema**.

Key design goal:

* Ensure strict structural data isolation between different organizations using the platform.

### Task Queue

Celery combined with Redis handles asynchronous processing.

Responsibilities:

* High‑volume email dispatch
* Background analytics tasks
* Scheduled maintenance jobs

### Deployment

The system is fully containerized using Docker and Docker Compose to ensure consistent development and production environments.

---

# Security & Defensive Engineering

Security controls are embedded directly into the architecture rather than layered on later.

### Multi‑Tenant Data Isolation

Every major database record is scoped to an **Organization** entity. This ensures strict separation between tenants and prevents accidental cross‑organization data access.

### Cryptographic Tracking Tokens

All tracking identifiers use **UUID4 cryptographically secure random tokens** (minimum 128‑bit entropy). This prevents attackers from guessing tokens and injecting fraudulent interaction data.

### Immutable Audit Logging

All sensitive administrative actions are recorded in an **append‑only audit log**. This design ensures full forensic traceability and prevents modification of historical activity records.

### Bot & Email Security Scanner Detection

Modern email gateways often pre‑scan links automatically. The platform records interaction metadata (IP address and User‑Agent) to support logic that distinguishes between:

* Human interactions
* Automated email security scanners
* Suspicious automated activity

This ensures that campaign metrics remain accurate and trustworthy.

---

# Ethics & Compliance

The platform is designed with a **privacy‑first mindset**, aligning with modern regulatory principles similar to GDPR and CCPA.

### No‑Plaintext Credential Policy

The system never stores:

* Passwords
* Form field values
* Any sensitive user input

Only the **event of a submission** is recorded, never the content of the submission itself.

### Authorization Enforcement

No phishing simulation campaign can be activated without a verified **digital authorization record** from an approved organizational stakeholder.

### Data Retention Controls

Sensitive interaction data is governed by automated retention policies including:

* Limited active retention
* Scheduled anonymization
* Permanent deletion after defined time windows

These controls reduce long‑term privacy and compliance risk.

---

# The 65‑Day Engineering Journey

The system is being developed through a structured **13‑week engineering roadmap** designed to simulate a real production development cycle.

### Week 1 – Foundation & System Design (Completed)

Day 1 — Scope Definition and Ethical Boundaries
Day 2 — High‑Level Architecture and Threat Modeling
Day 3 — Multi‑Tenant Database Schema Design
Day 4 — Tracking Flow and Token Lifecycle Design
Day 5 — Legal Authorization, Consent, and Data Retention Policy

This early phase establishes the **security, legal, and architectural foundation** for the entire system.

---

# Technology Stack

**Language**
Python 3.x

**Framework**
Django

**Database**
PostgreSQL

**Task Processing**
Celery + Redis

**Infrastructure**
Docker and Docker Compose

---

# ⚠️Legal Disclaimer

This platform is intended **strictly for authorized security awareness training, internal testing, and cybersecurity research**.

Any attempt to use this tool to target individuals or organizations **without explicit written authorization** is strictly prohibited and may violate applicable laws.

Users of this platform are responsible for ensuring that all simulations are conducted with proper consent and within the scope of organizational security programs.
