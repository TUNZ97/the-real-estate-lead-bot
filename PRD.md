# Product Requirements Document (PRD)

## 1. Product

**Real Estate Lead Bot — PrimeHomes Realty**

## 2. Problem

Property enquiries arrive as unstructured conversations. Sales teams need to manually extract requirements, identify valuable/urgent prospects, respond quickly and remember follow-ups. This creates inconsistent qualification, delayed responses and lost opportunities.

## 3. Vision

Create a reliable AI-assisted system that turns property enquiries into structured, actionable leads while keeping humans in control of important sales interactions.

## 4. Goals

- Capture leads consistently.
- Understand customer intent and requirements.
- Respond quickly and appropriately.
- Qualify leads using transparent rules.
- Notify sales staff when action is needed.
- Track follow-ups and lifecycle state.
- Provide a useful sales interface.

## 5. Users

- Potential customer.
- Sales agent.
- Sales manager.
- Administrator.

## 6. Functional requirements

### FR-001 Lead intake
Accept customer property enquiries through the supported chat/channel.

### FR-002 Intent detection
Identify buy/rent/sell/property/general enquiry and unknown cases.

### FR-003 Requirement extraction
Extract property type, location, bedrooms, budget, currency, timeframe and contact information where available.

### FR-004 Lead persistence
Create or update a customer, lead and conversation while preserving original messages.

### FR-005 Qualification
Calculate deterministic qualification and urgency from validated information.

### FR-006 Missing information
Identify important missing information and ask targeted questions.

### FR-007 Response
Generate a grounded response without fabricating availability, price or property facts.

### FR-008 Sales notification
Notify sales when configured qualification/urgency/handoff conditions are met.

### FR-009 Human handoff
Allow a customer to request or trigger human assistance.

### FR-010 Follow-up
Create and execute scheduled follow-ups and track their outcome.

### FR-011 Lifecycle
Track lead status from new enquiry through conversion/loss/closure.

### FR-012 Conversation history
Allow sales users to inspect the conversation and relevant structured lead data.

## 7. Non-functional requirements

- Secure authentication and authorization.
- Reliable persistence.
- Idempotent message processing.
- Observable workflows.
- Responsive customer UI.
- Maintainable modular code.
- Testable AI boundary.
- Controlled AI cost/latency.

## 8. MVP

The MVP includes lead intake, extraction, persistence, qualification, customer response, sales notification, basic sales dashboard, follow-up and lifecycle tracking.

## 9. Future scope

Property inventory integration, richer matching, analytics, omnichannel support, advanced sales automation and deeper CRM integrations.

## 10. Success measures

Track lead capture rate, structured extraction completeness, response latency, qualification coverage, human handoff rate, follow-up completion, conversion tracking and AI error/hallucination rate.

## 11. Business rules

- SQL is authoritative.
- AI cannot invent facts.
- Qualification is deterministic.
- Customer data must not leak across leads/users.
- Important automated actions must be auditable.
