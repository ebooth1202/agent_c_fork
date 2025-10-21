# Gatekeeper Agent Guide

A guide for building agents that require strict approval protocols, compliance oversight, and enhanced authority signoff requirements within the Agent C framework.

## When to Use Gatekeeper Agent Type

**Core Characteristics**:
- Authority signoff requirements for key decisions
- Strict scope boundaries and non-negotiable constraints
- Compliance emphasis and regulatory adherence
- Enhanced coordination protocols with oversight
- Professional authority and accountability

**Typical Scenarios**:
- Architecture review and approval authority
- Code review with mandatory approval gates
- Testing strategy validation and sign-off
- Security and compliance reviews
- Production deployment approvals

**Key Requirements**:
- Must include explicit authority protocols
- Must define non-negotiable scope boundaries
- Enhanced coordination and oversight mechanisms

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your gatekeeper agent's specific needs:

### 1. Critical Interaction Guidelines → YES (95% of gatekeepers)
**Decision**: Does this agent access workspaces or file paths?
- **Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)
- **Why**: Prevents wasted work on non-existent paths, ensures consistent workspace verification for compliance documentation and audit trails.

### 2. Human Pairing → NO (Standard for gatekeepers)
**Decision**: Does this agent use traditional human pairing protocols?
- **Why Skip**: Gatekeepers operate under **authority protocols** rather than collaborative pairing. Use custom authority signoff protocols instead.

### 3. Reflection Rules → YES (95% of gatekeepers)
**Decision**: Does this agent have access to ThinkTools?
- **Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)
- **Why**: Critical for systematic evaluation of approval requests, compliance assessments, and risk analysis.

### 4. Workspace Organization → YES (95% of gatekeepers)
**Decision**: Does this agent use workspace tools for file management?
- **Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)
- **Why**: Essential for maintaining audit trails, compliance documentation, approval records, and formal review artifacts.

### 5. Critical Working Rules → YES, Enhanced (100% of gatekeepers)
**Decision**: Does this agent do complex work requiring methodical validation?
- **Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)
- **Why**: Gatekeepers require **enhanced critical working rules** emphasizing validation protocols, approval processes, and compliance verification.
- **Enhancement**: Add strict validation requirements, approval gate protocols, and compliance verification steps.

### 6. Planning & Coordination → YES, Enhanced (90% of gatekeepers)
**Decision**: Does this agent coordinate multi-step validation or manage approval workflows?
- **Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)
- **Why**: Essential for managing complex approval workflows, validation sequences, and compliance verification processes.
- **Enhancement**: Add authority oversight requirements, approval gate tracking, and compliance validation checkpoints.

### 7. Clone Delegation → YES, Enhanced (80% of gatekeepers)
**Decision**: Does this agent delegate validation or analysis tasks to clones?
- **Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)
- **Why**: When delegation is necessary, gatekeepers require **enhanced coordination protocols** with strict validation of clone outputs.
- **Enhancement**: Add mandatory validation of clone outputs and approval requirements for delegated work.

### 8A/B/C. Code Quality Standards → YES, if reviewing code
**Decision**: Does this agent review or approve Python/C#/TypeScript code?
- **Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md), [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md), [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)
- **Why**: Essential for code review gatekeepers to enforce quality standards and compliance requirements.

### 9. Context Management → YES (70% of gatekeepers)
**Decision**: Does this agent manage complex approval workflows that might hit context limits?
- **Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)
- **Why**: Complex approval workflows, comprehensive compliance reviews, and multi-stage validation processes benefit from context management.

### 10. Team Collaboration → YES, Enhanced (90% of gatekeepers)
**Decision**: Is this agent part of a multi-agent team requiring enhanced coordination?
- **Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)
- **Why**: Gatekeeper agents in teams require **enhanced coordination protocols** with clear escalation paths and formal handoff procedures.
- **Enhancement**: Add approval authority boundaries, escalation protocols for conflicts, and formal validation handoffs.

### 11. Quality Gates → YES, Strict (100% of gatekeepers)
**Decision**: Does this agent require formal validation checkpoints and strict approval processes?
- **Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)
- **Why**: Quality gates are **fundamental to gatekeeper function**. All gatekeepers enforce validation checkpoints and approval requirements.
- **Enhancement**: Implement strictest validation protocols, mandatory approval gates, and comprehensive compliance verification.

### 12. Domain Knowledge Template → YES (100% of specialist gatekeepers)
**Decision**: Is this agent a specialist gatekeeper with domain expertise?
- **Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)
- **Why**: Specialist gatekeepers (architecture, testing, security, etc.) require deep domain knowledge to make informed approval decisions.

### 13. Authority Signoff Protocol (CUSTOM) → YES, MANDATORY (100% of gatekeepers)
**Decision**: Is this a gatekeeper agent?
- **Why MANDATORY**: This is the **core defining component** of gatekeeper agents. Establishes authority boundaries, approval protocols, signoff requirements, and accountability mechanisms.

**Component Pattern**:
```markdown
## Authority Signoff Protocol
### Authority Boundaries
**This agent has approval authority for**: [Specific domains]
**This agent DOES NOT have authority for**: [Out-of-scope decisions]

### Approval Requirements
1. Thorough Review: Systematic evaluation using domain expertise
2. Compliance Verification: Ensure all applicable standards are met
3. Risk Assessment: Identify and evaluate potential risks
4. Documented Rationale: Provide clear reasoning
5. Formal Signoff: Use `completion_signoff_by` to record approval

### Rejection Protocols
- Provide specific, actionable feedback on deficiencies
- Reference applicable standards not met
- Suggest concrete remediation steps

### Escalation Protocols
**When to escalate**: Requests outside authority, conflicts, novel situations, high-risk decisions
**Escalation Path**: [Define specific chain]
```

### 14. Scope Boundaries (CUSTOM) → YES, NON-NEGOTIABLE (100% of gatekeepers)
**Decision**: Is this a gatekeeper agent?
- **Why NON-NEGOTIABLE**: Establishes **strict operational boundaries** preventing scope creep and ensuring compliance.

**Component Pattern**:
```markdown
## Critical Scope Boundaries (NON-NEGOTIABLE)
### Operational Constraints
**This agent WILL**: ✅ Review and approve/reject, ✅ Validate compliance, ✅ Provide documented rationale
**This agent WILL NOT**: ❌ Make decisions outside authority, ❌ Implement changes directly, ❌ Bypass protocols

### Compliance Requirements
All approval decisions must document compliance, include risk assessment, and maintain audit trail.

### Accountability
**This agent is accountable for**: Quality of reviews, accuracy of assessments, appropriateness of decisions
**This agent is NOT responsible for**: Implementation of approved changes, results of decisions, upstream requirements
```

## Typical Structure and Composition

### Standard Gatekeeper Agent Structure
```markdown
# Agent Identity and Authority Role
## Authority Signoff Protocol (MANDATORY)
## Critical Scope Boundaries (NON-NEGOTIABLE)
## Critical Interaction Guidelines
## Reflection Rules
## Workspace Organization Guidelines
## Critical Working Rules (Enhanced)
## Planning & Coordination (Enhanced)
## Clone Delegation (Enhanced - if applicable)
## Code Quality Requirements - [Language] (if coding gatekeeper)
## Context Management (if complex workflows)
## Team Collaboration (Enhanced)
## Quality Gates (Strict Validation)
## [Domain Name] Expertise (if specialist)
# Personality and Communication Style
# Reference Materials
```

### Minimal Gatekeeper Agent Structure
```markdown
# Agent Identity and Authority Role
## Authority Signoff Protocol (MANDATORY)
## Critical Scope Boundaries (NON-NEGOTIABLE)
## Quality Gates (Strict Validation)
# Personality and Communication Style
```

### Specialist Domain Gatekeeper Structure
```markdown
# Agent Identity and Authority Role
## Authority Signoff Protocol (MANDATORY)
## Critical Scope Boundaries (NON-NEGOTIABLE)
## Critical Interaction Guidelines
## Reflection Rules
## Workspace Organization Guidelines
## Critical Working Rules (Enhanced)
## Planning & Coordination (Enhanced)
## Clone Delegation (Enhanced)
## Code Quality Requirements - [Language] (if applicable)
## Team Collaboration (Enhanced)
## Quality Gates (Strict Validation)
## [Domain Name] Expertise
# Personality and Communication Style
# Reference Materials
```

## Customization Guidance

**Authority Protocol Customization**:
- Define specific authority boundaries for domain (architecture, code, testing, security)
- Establish clear approval and rejection criteria
- Create domain-appropriate escalation paths
- Set accountability expectations specific to role

**Scope Boundary Customization**:
- Identify domain-specific operational constraints
- Define compliance requirements for domain
- Establish what gatekeeper WILL and WILL NOT do
- Create clear accountability boundaries

**Enhanced Component Adaptations**:
- **Critical Working Rules**: Add strict validation and approval gate protocols
- **Planning & Coordination**: Include authority oversight checkpoints and compliance verification
- **Clone Delegation**: Add mandatory validation of clone outputs and approval requirements
- **Team Collaboration**: Define approval authority boundaries and formal handoff procedures
- **Quality Gates**: Implement strictest validation protocols

**Personality Customization**:
- **Authoritative Expert**: Professional, definitive, standards-focused
- **Constructive Reviewer**: Emphasis on actionable feedback and improvement guidance
- **Compliance Guardian**: Formal, regulation-focused, risk-aware
- **Technical Authority**: Precise, technically rigorous, standards-driven

## Proper YAML Configuration Structure

**CRITICAL**: Agent YAML files must follow the exact field order shown below to prevent agent loading failures.

```yaml
version: 2
key: your_gatekeeper_agent_key_here
name: "Your Gatekeeper Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of the gatekeeper's authority and approval responsibilities.
tools:
  - ThinkTools
  - WorkspaceTools
  - WorkspacePlanningTools  # If complex approval workflows
  - AgentTeamTools  # If part of team
category:
  - "assist"  # Gatekeepers are typically assist agents
  - "gatekeeper"  # Identifies gatekeeper role
  - "your_domain"  # Architecture, testing, security, etc.
  - "orchestrator_key"  # If part of a team
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
persona: |
  # MUST BE LAST
  # MUST include Authority Signoff Protocol
  # MUST include Critical Scope Boundaries
```

**Critical Structure Rules**:
1. Field Order Matters: Fields must appear in exact order shown
2. Persona Must Be LAST: Always final field in YAML file
3. Required Fields: All fields shown above required
4. Category Array: Must include "gatekeeper"
5. Authority Components: Persona MUST include Authority Signoff Protocol and Critical Scope Boundaries

## Getting Started

**Step-by-Step Creation**:
1. Define Authority Domain: Identify approval authority and domain
2. Establish Authority Boundaries: Define what gatekeeper HAS authority to approve
3. Define Scope Constraints: Establish what gatekeeper WILL and WILL NOT do
4. Make Binary Decisions: Go through components with clear YES/NO choices
5. Create Proper YAML Structure: Use exact field order with "gatekeeper" category
6. Structure the Persona: Start with Authority Signoff Protocol and Critical Scope Boundaries (MANDATORY)
7. Add Enhanced Components: Include enhanced versions with strict validation
8. Validate YAML Structure: Verify fields in correct order with persona LAST

**Quality Checklist**:
- ✅ Includes 'gatekeeper' in category array
- ✅ Authority Signoff Protocol component (MANDATORY)
- ✅ Critical Scope Boundaries component (NON-NEGOTIABLE)
- ✅ Clear authority boundaries defined
- ✅ Approval and rejection protocols established
- ✅ Escalation paths defined
- ✅ Professional authority communication style
- ✅ Reflection Rules for systematic evaluation (95%)
- ✅ Quality Gates with strict validation (100%)
- ✅ Workspace Organization for audit trails (95%)
- ✅ Enhanced Team Collaboration if part of team (90%)
- ✅ Domain Knowledge for specialist gatekeepers (100% of specialists)
- ✅ Code Quality Standards if reviewing code (100% of code gatekeepers)
- ✅ Authority boundaries are clear and enforceable
- ✅ Component selections match gatekeeper capabilities and tools
