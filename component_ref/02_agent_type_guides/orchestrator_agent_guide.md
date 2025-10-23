# Orchestrator Agent Guide

A guide for building agents that coordinate teams and manage complex workflows, focusing on delegation, context management, and quality oversight.

## When to Use Orchestrator Agent Type

**Primary Purpose**: Agents designed to coordinate teams, manage complex workflows, and oversee multi-phase project execution

**Core Characteristics**:
- Team and workflow coordination leadership
- Heavy reliance on clone delegation for work execution
- Critical context window management across workflow phases
- Quality oversight and validation at integration points
- Progress tracking, reporting, and handoff management

**Typical Scenarios**:
- Multi-agent team coordination and orchestration
- Complex multi-phase workflow management
- Large-scale project execution requiring parallel workstreams
- Sequential processing with validation gates between phases
- Long-running processes requiring state preservation and recovery

**Key Requirements**:
- Should NOT include 'domo' in category array (unless user-facing orchestrator)
- Must include appropriate planning and delegation components
- Context management and recovery protocols essential

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision:

### 1. Critical Interaction Guidelines Component

**Does this orchestrator access workspaces or file paths?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)  
**Why Include**: Prevents wasted orchestration work on non-existent paths, ensures verification before delegation.  
**When to Skip**: Theoretical orchestrators without file system access (extremely rare).

---

### 2. Reflection Rules Component

**Does this orchestrator have access to ThinkTools?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)  
**Why Include**: Essential for processing complex requirements, planning delegation strategies, evaluating quality gates.  
**When to Skip**: Only if ThinkTools unavailable (not recommended).

---

### 3. Workspace Organization Component

**Does this orchestrator use workspace tools for file management?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)  
**Why Include**: Critical for managing project state, coordinating handoffs, organizing team outputs.  
**When to Skip**: Only if no workspace access (not recommended).

---

### 4. Code Quality Standards Components

**Does this orchestrator write or modify code directly?**
- **YES** → Use language-appropriate component
- **NO** → Skip this component *(95% of Orchestrators)*

**Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md), [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md), [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)  
**Why Include**: Only if orchestrator performs direct code implementation (rare).  
**When to Skip**: Standard orchestrators that delegate coding to specialist agents or clones.

---

### 5. Human Pairing Protocol Component

**Does this orchestrator interact directly with users?**
- **YES** → Use General Human Pairing component
- **NO** → Skip this component *(90% of Orchestrators)*

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)  
**Why Include**: Only for user-facing orchestrators that coordinate work directly with users.  
**When to Skip**: Standard orchestrators that operate as backend coordination engines.

---

### 6. Critical Working Rules Component

**Does this orchestrator manage complex multi-step workflows requiring methodical planning?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)  
**Why Include**: Essential for establishing methodical planning, verification protocols, single-step completion discipline.  
**When to Skip**: Only for simplest orchestrators (not recommended).

---

### 7. Planning & Coordination Component

**Does this orchestrator coordinate multi-step work or manage complex workflows?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)  
**Why Include**: Absolutely essential - defines workspace planning tools usage, task hierarchies, progress tracking.  
**When to Skip**: Never for orchestrators - this is a defining characteristic.

---

### 8. Clone Delegation Component

**Does this orchestrator delegate tasks to clone agents?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)  
**Why Include**: Absolutely essential - defines proper single focused task delegation, prevents task sequence anti-pattern.  
**When to Skip**: Never for orchestrators - this is a defining characteristic.

---

### 9. Context Management Component

**Does this orchestrator coordinate complex workflows that might hit context limits?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)  
**Why Include**: Essential for progressive summarization, metadata preservation, context burnout recovery protocols.  
**When to Skip**: Only for simplest single-phase orchestrators (rare and not recommended).

---

### 10. Team Collaboration Component

**Is this orchestrator coordinating a multi-agent team with direct communication?**
- **YES** → Use this component *(50% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)  
**Why Include**: For orchestrators managing teams with direct specialist-to-specialist communication via AgentTeamTools.  
**When to Skip**: Orchestrators that only use clone delegation without specialist team members.

---

### 11. Quality Gates Component

**Does this orchestrator need formal validation checkpoints and completion signoff?**
- **YES** → Use this component *(100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)  
**Why Include**: Essential for output validation protocols, completion signoff, quality validation at integration points.  
**When to Skip**: Never for orchestrators - quality oversight is a defining responsibility.

---

### 12. Domain Knowledge Template Component

**Is this orchestrator specialized for a specific domain?**
- **YES** → Use this template structure *(75% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)  
**Why Include**: For domain-specialized orchestrators needing specific expertise to make coordination decisions.  
**When to Skip**: Generic orchestrators that coordinate workflows without domain-specific knowledge.

## Structure Templates

### Standard Orchestrator Structure

```markdown
# Orchestrator Identity and Strategic Mission
[Custom identity, role, and coordination mission]

## Critical Interaction Guidelines
[Workspace safety and path verification - ALWAYS YES]

## Reflection Rules
[Strategic thinking and analysis requirements - ALWAYS YES]

## Workspace Organization Guidelines
[State management and artifact organization - ALWAYS YES]

## Critical Working Rules
[Methodical planning and verification discipline - ALWAYS YES]

## Planning and Coordination Framework
[Multi-step work coordination using planning tools - ALWAYS YES]

## Clone Delegation Framework
[Proper single-task delegation patterns - ALWAYS YES]

## Context Management Strategies
[Progressive summarization and recovery protocols - ALWAYS YES]

## Quality Gates and Validation Framework
[Output validation and completion signoff - ALWAYS YES]

## [Team Collaboration Protocols]
[If managing specialist team with AgentTeamTools - CONDITIONAL]

## [Domain Name] Expertise
[If domain-specialized orchestrator - CONDITIONAL]

# Custom Orchestration Workflows
[Specific workflow patterns, coordination procedures, handoff protocols]

# Success Metrics and Quality Standards
[Performance criteria, quality expectations]

# Professional Orchestration Personality
[Strategic, methodical, oversight-focused communication style]
```

### Domain-Specialized Orchestrator Structure

```markdown
# Orchestrator Identity and Strategic Mission
[Custom identity with domain focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Strategic and domain-specific thinking triggers]

## Workspace Organization Guidelines
[Domain-specific artifact and state management]

## Critical Working Rules
[Methodical planning with domain considerations]

## Planning and Coordination Framework
[Domain-specific workflow coordination]

## Clone Delegation Framework
[Domain-appropriate task delegation]

## Context Management Strategies
[Domain-specific summarization and recovery]

## [Domain Name] Expertise
[Comprehensive domain knowledge sections]
  ### [Domain] Philosophy
  ### [Domain] Methodologies
  ### [Domain] Standards and Compliance
  ### [Domain] Quality Criteria

## Team Collaboration Protocols
[If managing specialist team]

## Quality Gates and Validation Framework
[Domain-specific validation criteria]

# [Domain] Orchestration Workflows
[Domain-specific coordination patterns]

# Success Metrics and Quality Standards
[Domain-specific performance and quality measures]

# Professional Orchestration Personality
[Strategic, methodical, domain-expert communication style]
```

### Team Orchestrator Structure

```markdown
# Orchestrator Identity and Strategic Mission
[Custom identity with team coordination focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Strategic thinking with team coordination triggers]

## Workspace Organization Guidelines
[Team artifact and handoff management]

## Critical Working Rules
[Methodical team coordination discipline]

## Planning and Coordination Framework
[Team-based workflow coordination]

## Clone Delegation Framework
[Balanced clone and specialist delegation]

## Context Management Strategies
[Team coordination context management]

## Team Collaboration Excellence
[Comprehensive team member directory and protocols]
  ### Team Member Directory
  [List all specialists with agent keys]
  ### Team Coordination Principles
  [Clear role boundaries and handoff protocols]

## Quality Gates and Validation Framework
[Team deliverable validation and integration]

# Team Orchestration Workflows
[Team coordination patterns, specialist handoffs]

# Success Metrics and Quality Standards
[Team performance, integration quality]

# Professional Team Leadership Personality
[Strategic, collaborative, oversight-focused style]
```

## Customization Guidance

**Generic Workflow Orchestrators**:
- Focus on clear delegation and quality oversight
- Emphasize context management and recovery protocols
- Include methodical planning and verification patterns
- Minimal domain-specific content

**Domain-Specialized Orchestrators**:
- Include comprehensive domain expertise sections
- Emphasize domain-specific quality criteria and standards
- Add domain compliance and risk management content
- Customize validation criteria for domain deliverables

**Team Coordination Orchestrators**:
- Include comprehensive team collaboration protocols
- Define clear role boundaries for specialists
- Emphasize handoff and integration procedures
- Add escalation and conflict resolution protocols

**Domain-Specific Adaptations**:
- Add industry-specific compliance and regulatory requirements
- Include domain-specific risk assessment protocols
- Customize for domain-specific workflow phases
- Tailor summarization for domain artifacts

**Personality Options**:
- Strategic Coordinator: High-level, mission-focused, delegation-oriented
- Methodical Overseer: Detailed, verification-focused, quality-driven
- Team Leader: Collaborative, integration-focused, coordination-expert
- Domain Expert: Specialized, standards-focused, compliance-oriented

## YAML Configuration Structure

**CRITICAL**: Agent YAML files must follow exact field order to prevent loading failures.

```yaml
version: 2
key: your_orchestrator_key_here
name: "Your Orchestrator Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of orchestrator's coordination mission and workflow focus.
tools:
  - ThinkTools
  - WorkspaceTools
  - WorkspacePlanningTools
  - AgentCloneTools
  # AgentTeamTools if team coordination
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
category:
  - "assist"  # Most orchestrators are assist, NOT domo
  - "your_domain"
  # Include specialist keys for team members if using AgentTeamTools
persona: |
  # The persona content MUST be LAST
```

**Critical Rules**:
- Field order matters - must appear in exact order shown
- Persona must be LAST field
- Category = "assist" (most orchestrators, NOT "domo")
- Essential tools: ThinkTools, WorkspaceTools, WorkspacePlanningTools, AgentCloneTools
- Reasoning budget for strategic planning

## Getting Started

**Step-by-Step Creation**:
1. Define orchestration mission and workflow scope
2. Determine if backend (assist) or user-facing (domo)
3. Make binary component decisions (YES/NO)
4. Identify domain specialization needs
5. Assess team coordination requirements
6. Create proper YAML structure with appropriate tools
7. Structure persona with all essential orchestrator components

**Quality Checklist**:
- ✅ Includes 'assist' in category array (unless user-facing)
- ✅ All essential components: Critical Interaction, Reflection, Workspace Organization, Critical Working Rules, Planning & Coordination, Clone Delegation, Context Management, Quality Gates
- ✅ Strategic oversight-focused communication style
- ✅ Team Collaboration component (if managing specialist team)
- ✅ Domain Knowledge sections (if domain-specialized)
- ✅ Custom workflow documentation
- ✅ Recovery and fallback protocols documented
