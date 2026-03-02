Project Scope & Ethical Charter
Project Name: Phishing Awareness Simulation Platform
Architecture: Modular Layered Monolith (Django-Based)
Status: Day 1 – Scope Defined
Project Type: Portfolio Project with Real-World Applicability
________________________________________
1. Executive Summary
The Phishing Awareness Simulation Platform is a professional cybersecurity system designed to measure and quantify human vulnerability to social engineering attacks within an organization.
Organizations face significant financial and reputational damage due to phishing attacks that exploit employee behaviour rather than technical weaknesses. However, this human risk is often invisible and unmeasured.
This platform transforms that unknown vulnerability into structured, measurable security intelligence by executing controlled, authorized phishing simulations. The system records user interactions, filters automated email security scanners, calculates risk exposure metrics, and generates executive-ready reports.
The objective is not exploitation — it is education, measurement, and prevention.
This project will be built as a modular layered monolith using Django, structured in a way that reflects production-grade architectural discipline while remaining manageable for a solo engineer.
________________________________________
2. Core Problem Statement
Human susceptibility to phishing is a critical but unquantified security risk.
Organizations invest heavily in firewalls, antivirus systems, and endpoint protection, yet the "human firewall" remains weak and largely unmeasured.
This platform aims to:
•	Measure employee susceptibility to phishing attacks.
•	Provide quantifiable risk metrics.
•	Deliver actionable remediation recommendations.
•	Support leadership decision-making with structured reporting.
________________________________________
3. System Objectives
1.	Build a secure phishing simulation engine for authorized testing.
2.	Accurately track and log user interactions (clicks and simulated submissions).
3.	Differentiate human interactions from automated security scanners.
4.	Calculate meaningful awareness and risk metrics.
5.	Generate executive-level security reports.
6.	Demonstrate clean architectural design in a modular layered monolith structure.
________________________________________
4. What the Platform DOES (In-Scope)
To maintain engineering discipline and prevent scope creep, the system will include:
4.1 Simulation Management
•	Creation and management of phishing campaigns.
•	Target user assignment.
•	Email template management.
•	Controlled campaign execution.
4.2 Interaction Intelligence
•	Unique tokenized tracking links.
•	Click event logging.
•	Simulated credential submission logging (without storing real credentials).
•	Bot-filtering logic to exclude automated email gateway scanners.
4.3 Risk Measurement Engine
•	Click-through rate calculation.
•	Submission rate calculation.
•	Awareness scoring formula.
•	Risk exposure classification.
4.4 Executive Reporting
•	Campaign performance summaries.
•	Risk exposure interpretation.
•	Training recommendations.
•	Exportable executive-ready PDF reports.
4.5 Compliance & Data Governance
•	Explicit authorization requirement.
•	Data retention policy framework.
•	Anonymization capability.
•	Secure storage of sensitive metadata.
________________________________________
5. What the Platform DOES NOT Do (Out-of-Scope)
To prevent unethical drift and misuse, the following are strictly prohibited:
•	❌ No real credential harvesting.
•	❌ No storage of plaintext passwords.
•	❌ No malware delivery.
•	❌ No unauthorized phishing campaigns.
•	❌ No external target attacks.
•	❌ No bypassing security controls for malicious intent.
This platform is an awareness and measurement system — not an offensive exploitation toolkit.
________________________________________
6. Target Users
Primary Users:
•	Small-to-Medium Enterprises (SMEs)
•	Internal Security Teams
•	Security Consultants performing authorized assessments
Secondary Purpose:
•	Portfolio demonstration of secure system architecture
•	Showcasing engineering maturity and cybersecurity knowledge
________________________________________
7. Architectural Direction (Modular Layered Monolith)
The system will follow a clean modular layered structure:
Presentation Layer
•	Django templates (HTML/CSS-based dashboard UI)
•	Campaign dashboards
•	Analytics visualizations
Application Layer
•	Campaign orchestration logic
•	Email sending workflows
•	Background task processing
Domain Layer
•	Risk engine logic
•	Scoring algorithms
•	Bot filtering intelligence
Infrastructure Layer
•	PostgreSQL database
•	Email integration
•	Logging and audit mechanisms
•	Docker containerization (later phase)
This approach ensures:
•	Clean separation of concerns
•	Maintainability
•	Scalability potential
•	Professional architectural demonstration
________________________________________
8. Ethical Charter
This project operates under the following ethical principles:
1.	Explicit Written Authorization Required.
2.	No real credential storage.
3.	Data minimization and secure handling.
4.	Transparency with participating organizations.
5.	Educational intent over punitive exposure.
The platform exists to strengthen organizations, not exploit them.
________________________________________
9. Long-Term Vision
Although initially built as a portfolio project, the system is designed with real-world applicability in mind. The architecture, compliance awareness, and reporting capability are structured to allow future transformation into a production-ready commercial tool if desired.
________________________________________
Day 1 Completion Criteria
Day 1 is considered complete when:
•	The system purpose is clearly defined.
•	Scope boundaries are established.
•	Ethical constraints are documented.
•	Architectural direction is selected.
•	Long-term vision is clarified.
This document serves as the foundation for all future development decisions.
Any feature not aligned with this scope must be intentionally reviewed before implementation.

