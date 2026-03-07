# Day 5 – Legal, Consent & Data Retention Policy

## Objective

Define the legal authorization workflow and data management policies that ensure the phishing simulation platform operates ethically, responsibly, and in alignment with common privacy and compliance expectations.

Because this platform records sensitive user interaction behavior, it must minimize legal exposure through strict authorization requirements, limited data retention, and transparent educational practices.

Security awareness testing must strengthen organizations — not expose them to unnecessary risk.

---

# 1. Authorization Requirements

To prevent the **Unauthorized Campaign Creation** risk identified in earlier threat modeling, the platform enforces a mandatory authorization workflow before any campaign can be activated.

## 1.1 Written Consent Requirement

No campaign may transition to the **ACTIVE** state unless a verified authorization record exists.

The authorization must come from a legitimate organizational authority such as:

* Chief Information Security Officer (CISO)
* IT Director
* Security Program Manager
* Authorized compliance officer

The system must require one of the following forms of authorization:

* Uploaded signed authorization document
* Digitally approved authorization form
* Secure internal authorization workflow

Campaign activation is programmatically blocked if authorization is missing.

---

## 1.2 Scope Limitation

Each authorization must explicitly define the permitted scope of the simulation.

Required scope attributes include:

* Target organization domain(s)
* Departments or user groups included in the simulation
* Simulation start date
* Simulation end date

This prevents simulations from expanding beyond the approved testing boundaries.

The platform enforces this scope by:

* Linking the authorization record directly to the campaign
* Validating campaign scheduling against authorized dates

---

## 1.3 Authorization Audit Trail

Every authorization record must be fully traceable.

The system records:

* Timestamp of authorization upload
* Administrative user responsible for the upload
* Organization associated with the authorization
* Reference to the linked campaign

These records create an **immutable chain of accountability** between:

* The decision to run the simulation
* The campaign execution
* The responsible administrative user

This ensures that every simulation has a clear and auditable justification.

---

# 2. Data Retention Policy

Phishing simulations generate behavioral interaction data that may include sensitive metadata such as IP addresses and user-agent information.

To reduce privacy risk and regulatory exposure, the platform follows a **data minimization strategy**.

---

## 2.1 Active Data Retention

Raw interaction data is retained only for the period required for analysis and reporting.

Retention window:

* Duration of the campaign
* Plus **30 additional days** for reporting and administrative review

During this period, the system retains:

* ClickEvent records
* SubmissionEvent records
* IP addresses
* User-Agent metadata

This allows analysts to perform accurate campaign analysis and generate reports.

---

## 2.2 Data Anonymization

To reduce long-term privacy risk, identifiable user data is removed after a limited period.

After **90 days**, the system performs an anonymization process that:

* Removes personally identifiable user references
* Retains only aggregated metrics

Examples of retained metrics:

* Department-level click rates
* Organization-wide submission rates
* Historical campaign performance trends

This enables long-term security awareness analytics without retaining identifiable user behavior.

---

## 2.3 Permanent Data Deletion

To further minimize risk, raw event data is not stored indefinitely.

Retention rule:

* All raw **ClickEvent** and **SubmissionEvent** records are permanently deleted after **12 months**.

Exceptions may only occur when:

* Required for formal compliance investigations
* Explicitly extended by authorized security leadership

This deletion process reduces the risk associated with long-term storage of sensitive behavioral data.

---

# 3. Ethical Safeguards

The platform is intentionally designed to support **security awareness and education**, not employee punishment or surveillance.

Several safeguards enforce this principle.

---

## 3.1 The No-Plaintext Rule

Under no circumstances does the system store:

* Real passwords
* Form field values
* Sensitive user input

If a simulated credential form is submitted, the platform records only:

* That a submission event occurred
* The associated campaign and user metadata

The contents of the form are never persisted.

This rule prevents the platform from becoming a credential harvesting system.

---

## 3.2 Mandatory Educational Disclosure

Every phishing simulation must conclude with an educational step.

After a user interaction occurs, the platform redirects the user to an **Educational Disclosure Page** explaining:

* That the interaction was part of a security awareness simulation
* Key indicators that the email could have been suspicious
* Best practices for recognizing phishing attempts

The goal is to transform a mistake into a learning opportunity.

---

# Summary

Day 5 establishes the governance framework that ensures the phishing awareness platform operates responsibly.

By combining:

* mandatory campaign authorization
* strict scope enforcement
* limited data retention
* anonymization policies
* ethical safeguards

…the system ensures that phishing simulations remain a **controlled security training exercise rather than a privacy risk**.

These policies also demonstrate that the platform was designed with **legal accountability and organizational trust in mind**.
