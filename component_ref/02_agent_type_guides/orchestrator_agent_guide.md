# Orchestrator Agent Guide

A comprehensive guide for building agents that coordinate teams and manage complex workflows, focusing on delegation, context management, and quality oversight within the Agent C framework.

## When to Use Orchestrator Agent Type

**Primary Purpose**: Agents designed to coordinate teams, manage complex workflows, and oversee multi-phase project execution

**Core Characteristics**:
- Team and workflow coordination leadership
- Heavy reliance on clone delegation for work execution
- Critical context window management across workflow phases
- Quality oversight and validation at integration points
- Progress tracking, reporting, and handoff management
- Strategic planning and decomposition expertise
- Recovery and fallback protocol implementation
- Metadata and state management for resumability

**Typical Scenarios**:
- Multi-agent team coordination and orchestration
- Complex multi-phase workflow management
- Large-scale project execution requiring parallel workstreams
- Sequential processing with validation gates between phases
- Context-intensive operations requiring strategic decomposition
- Quality-critical workflows requiring oversight and validation
- Long-running processes requiring state preservation and recovery
- Cross-functional coordination requiring specialist integration

**Key Requirements**:
- Should NOT include 'domo' in category array (unless user-facing orchestrator)
- Must include appropriate planning and delegation components
- Optimized for coordination, delegation, and oversight
- Context management and recovery protocols essential
- Quality gates and validation frameworks critical

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your orchestrator's specific needs:

### 1. Critical Interaction Guidelines Component

**Does this orchestrator access workspaces or file paths?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)

**Why Include**: Prevents wasted orchestration work on non-existent paths, provides immediate feedback on path errors, ensures consistent workspace verification before delegation.

**When to Skip**: Theoretical orchestrators without any file system access (extremely rare).

---

### 2. Reflection Rules Component

**Does this orchestrator have access to the ThinkTools?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)

**Why Include**: Essential for processing complex requirements, planning delegation strategies, evaluating progress and quality gates, analyzing coordination patterns, and making strategic decisions.

**When to Skip**: Only if ThinkTools are unavailable (not recommended for orchestrators).

**Orchestrator-Specific Triggers**: Include triggers for "reading project requirements," "planning team coordination strategies," "analyzing progress and quality gates," "coordinating between team members," and "evaluating delegation strategies."

---

### 3. Workspace Organization Component

**Does this orchestrator use workspace tools for file and directory management?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)

**Why Include**: Critical for managing project state, coordinating handoffs between phases, preserving work artifacts, organizing team outputs, and maintaining resumable workflow state.

**When to Skip**: Only if no workspace access (not recommended for orchestrators).

**Orchestrator-Specific Usage**: Emphasize scratchpad usage for handoff notes, metadata storage for coordination state, and organized artifact management for team outputs.

---

### 4. Code Quality Standards Components

**Does this orchestrator write or modify code directly?**

- **YES** → Use language-appropriate component
- **NO** → Skip this component *(Applies to 95% of Orchestrators)*

**Reference**: 
- [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)
- [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)
- [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)

**Why Include**: Only if orchestrator performs direct code implementation (rare - typically delegates to specialists).

**When to Skip**: Standard orchestrators that delegate coding to specialist agents or clones.

---

### 5. Human Pairing Protocol Component

**Does this orchestrator interact directly with users?**

- **YES** → Use General Human Pairing component
- **NO** → Skip this component *(Applies to 90% of Orchestrators)*

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)

**Why Include**: Only for user-facing orchestrators that coordinate work directly with users.

**When to Skip**: Standard orchestrators that operate as backend coordination engines.

**Note**: Most orchestrators are NOT user-facing and should NOT include this component. User interaction typically happens through a separate domo agent that delegates to the orchestrator.

---

### 6. Critical Working Rules Component

**Does this orchestrator manage complex multi-step workflows requiring methodical planning?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)

**Why Include**: Essential for establishing methodical planning, verification protocols, and single-step completion discipline critical for orchestration work.

**When to Skip**: Only for the simplest orchestrators (not recommended).

---

### 7. Planning & Coordination Component

**Does this orchestrator coordinate multi-step work or manage complex workflows?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)

**Why Include**: Absolutely essential for all orchestrators - defines how to use workspace planning tools, create task hierarchies, track progress, and manage delegation state.

**When to Skip**: Never for orchestrators - this is a defining characteristic.

---

### 8. Clone Delegation Component

**Does this orchestrator delegate tasks to clone agents?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)

**Why Include**: Absolutely essential for all orchestrators - defines how to properly delegate single focused tasks, avoid task sequences, validate clone outputs, and recover from failures.

**When to Skip**: Never for orchestrators - this is a defining characteristic.

**Critical Importance**: This component prevents the single most common orchestration failure mode (task sequence anti-pattern). Always include.

---

### 9. Context Management Component

**Does this orchestrator coordinate complex workflows that might hit context limits?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)

**Why Include**: Essential for all orchestrators managing complex workflows - defines progressive summarization, metadata preservation, checkpoint creation, context burnout recovery protocols, and proper metadata usage.

**When to Skip**: Only for the simplest single-phase orchestrators (rare and not recommended).

---

### 10. Team Collaboration Component

**Is this orchestrator coordinating a multi-agent team with direct communication?**

- **YES** → Use this component *(Applies to 50% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)

**Why Include**: For orchestrators managing teams with direct specialist-to-specialist communication using AgentTeamTools. Defines team member directory, coordination principles, and escalation protocols.

**When to Skip**: Orchestrators that only use clone delegation without specialist team members.

---

### 11. Quality Gates Component

**Does this orchestrator need formal validation checkpoints and completion signoff?**

- **YES** → Use this component *(Applies to 100% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)

**Why Include**: Essential for all orchestrators - defines output validation protocols, completion signoff procedures, and quality validation criteria at integration points between workflow phases.

**When to Skip**: Never for orchestrators - quality oversight is a defining responsibility.

---

### 12. Domain Knowledge Template Component

**Is this orchestrator specialized for a specific domain (e.g., insurance underwriting, software development)?**

- **YES** → Use this template structure *(Applies to 75% of Orchestrators)*
- **NO** → Skip this component

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)

**Why Include**: For domain-specialized orchestrators that need specific expertise in a particular field to make coordination decisions.

**When to Skip**: Generic orchestrators that coordinate workflows without domain-specific knowledge requirements.

---

## Typical Structure and Composition Order

Based on the binary component decisions above, here's the recommended persona organization for orchestrators:

### Component Ordering Principle

**Recommended Order (Foundation → Coordination → Domain → Quality)**:

1. **Core Safety and Thinking** (Critical Interaction Guidelines, Reflection Rules)
   - Establishes safe operations and strategic thinking patterns
   - Foundation for all orchestration decisions

2. **Operational Infrastructure** (Workspace Organization, Critical Working Rules)
   - Defines how the orchestrator manages state and artifacts
   - Sets methodical working discipline

3. **Core Orchestration Capabilities** (Planning & Coordination, Clone Delegation)
   - Defines the essential coordination and delegation patterns
   - Central to orchestrator function

4. **Advanced Orchestration** (Context Management, Quality Gates)
   - Adds sophisticated context handling and quality oversight
   - Ensures scalability and reliability

5. **Team Coordination** (Team Collaboration - if applicable)
   - Defines specialist team integration patterns
   - Built on top of core orchestration

6. **Domain Expertise** (Domain Knowledge - if applicable)
   - Specialized knowledge for domain-specific orchestration
   - Applied through the orchestration framework

7. **Custom Workflows and Success Metrics**
   - Specific workflow patterns and coordination procedures
   - Performance and success criteria

This ordering ensures that fundamental safety and coordination patterns are established before adding team collaboration, domain expertise, and custom workflows.

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
[Performance criteria, quality expectations, coordination effectiveness measures]

# Professional Orchestration Personality
[Strategic, methodical, oversight-focused communication style]
```

### Minimal Orchestrator Structure

For simple coordination orchestrators (rare):

```markdown
# Orchestrator Identity and Strategic Mission
[Custom identity and coordination mission]

## Critical Interaction Guidelines
[Workspace safety]

## Reflection Rules
[Strategic thinking]

## Workspace Organization Guidelines
[State management]

## Planning and Coordination Framework
[Multi-step coordination]

## Clone Delegation Framework
[Task delegation]

## Quality Gates and Validation Framework
[Output validation]

# Custom Workflows
[Specific coordination patterns]
```

### Domain-Specialized Orchestrator Structure

For orchestrators with domain expertise (common):

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
  ### [Domain] Risk Management

## Team Collaboration Protocols
[If managing specialist team]

## Quality Gates and Validation Framework
[Domain-specific validation criteria]

# [Domain] Orchestration Workflows
[Domain-specific coordination patterns and procedures]

# Success Metrics and Quality Standards
[Domain-specific performance and quality measures]

# Professional Orchestration Personality
[Strategic, methodical, domain-expert communication style]
```

### Team Orchestrator Structure

For orchestrators managing specialist teams with direct communication:

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
  ### Escalation Protocols
  [Conflict resolution and quality issue handling]

## Quality Gates and Validation Framework
[Team deliverable validation and integration]

# Team Orchestration Workflows
[Team coordination patterns, specialist handoffs, integration procedures]

# Success Metrics and Quality Standards
[Team performance, integration quality, coordination effectiveness]

# Professional Team Leadership Personality
[Strategic, collaborative, oversight-focused communication style]
```

## Customization Guidance

### Focus Area Adaptations

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
- Include domain-specific coordination workflows

**Team Coordination Orchestrators**:
- Include comprehensive team collaboration protocols
- Define clear role boundaries for specialists
- Emphasize handoff and integration procedures
- Add escalation and conflict resolution protocols
- Focus on team performance and coordination metrics

**User-Facing Orchestrators** (Rare):
- Add human pairing protocol component
- Include user communication and reporting patterns
- Emphasize user-friendly progress updates
- Add appropriate domo category

### Domain-Specific Considerations

**Add Custom Sections For**:
- Industry-specific compliance and regulatory requirements
- Domain-specific risk assessment and mitigation protocols
- Specialized quality standards and validation criteria
- Domain-specific workflow patterns and coordination procedures
- Professional standards and certification requirements

**Adapt Components For**:
- **Planning & Coordination**: Customize for domain-specific workflow phases
- **Clone Delegation**: Adapt task sizing for domain work complexity
- **Context Management**: Tailor summarization for domain artifacts
- **Quality Gates**: Define domain-specific validation criteria
- **Team Collaboration**: Customize for domain specialist roles

### Personality Customization

**Communication Style Options**:
- **Strategic Coordinator**: High-level, mission-focused, delegation-oriented
- **Methodical Overseer**: Detailed, verification-focused, quality-driven
- **Team Leader**: Collaborative, integration-focused, coordination-expert
- **Domain Expert**: Specialized, standards-focused, compliance-oriented

**Maintain Orchestrator Characteristics**:
- Always coordination and oversight focused
- Strategic rather than tactical execution
- Quality-driven validation and verification
- Context-aware and recovery-capable
- Methodical and disciplined in workflow management
- Clear delegation boundaries and responsibilities

## Real Examples from the Ecosystem

### Domain-Specialized Team Orchestrator
**Agent**: `douglas_bokf_orchestrator.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Reflection Rules
- ✅ Workspace Organization
- ❌ Human Pairing Protocol (backend orchestrator)
- ✅ Critical Working Rules
- ✅ Planning & Coordination
- ✅ Clone Delegation
- ❌ Code Quality Standards (delegates coding)
- ✅ Context Management
- ✅ Team Collaboration
- ✅ Quality Gates
- ✅ Domain Knowledge (insurance underwriting)

**Characteristics**: Complex team coordination with insurance domain expertise, sequential processing with validation gates, heavy clone delegation with specialist team integration, sophisticated context management and recovery protocols

**Key Features**:
- Insurance underwriting domain specialization
- Multi-specialist team coordination (Rex, Aria, Mason, Vera)
- Progressive workflow phases with quality gates
- Advanced context management and metadata usage
- Comprehensive recovery protocols
- Domain-specific risk assessment and quality validation

---

## Component Integration Benefits

### Why Binary Decisions Work

**For Orchestrators Specifically**:
- **Clear Coordination Framework**: Binary decisions create consistent orchestration patterns
- **Essential Capabilities**: Components ensure all critical orchestration capabilities are included
- **Scalable Design**: Component-based approach enables complex workflow management
- **Recovery-Ready**: Components enforce resumability and failure recovery patterns

**Quality Outcomes**:
- **Consistent Orchestration**: Agents with similar components coordinate predictably
- **Professional Standards**: Component standards maintain orchestration quality baseline
- **Reduced Complexity**: Binary choices eliminate incomplete implementations
- **Quality Assurance**: Components enforce proven orchestration practices

### Integration Patterns

**Essential Component Combinations for Orchestrators**:
- Planning & Coordination + Clone Delegation = Effective task delegation framework
- Context Management + Clone Delegation = Scalable context-aware orchestration
- Quality Gates + Planning & Coordination = Validated workflow progression
- Team Collaboration + Planning & Coordination = Integrated specialist coordination
- Workspace Organization + Context Management = State preservation and recovery

**Core Integration Benefits**:
- **Strategic Coordination**: Planning and delegation components enable sophisticated workflows
- **Context Resilience**: Context management prevents orchestration failures
- **Quality Oversight**: Quality gates ensure deliverable validation at integration points
- **Team Integration**: Team collaboration enables specialist coordination patterns
- **State Preservation**: Workspace and context management enable resumability

### Orchestrator-Specific Patterns

**Critical Anti-Patterns to Avoid** (Components Help Prevent):
- ❌ Task sequence delegation (prevented by Clone Delegation Component)
- ❌ Context burnout (prevented by Context Management Component)
- ❌ Missing quality validation (prevented by Quality Gates Component)
- ❌ Metadata misuse for status tracking (prevented by Context Management Component)
- ❌ Unclear team handoffs (prevented by Team Collaboration Component)

**Proven Success Patterns** (Components Enforce):
- ✅ Single focused clone tasks (Clone Delegation Component)
- ✅ Progressive context summarization (Context Management Component)
- ✅ Validation gates between phases (Quality Gates Component)
- ✅ Metadata for valuable outputs only (Context Management Component)
- ✅ Clear specialist role boundaries (Team Collaboration Component)

## Proper YAML Configuration Structure

**CRITICAL**: Agent YAML files must follow the exact field order shown below to prevent agent loading failures.

### Required Field Order

```yaml
version: 2
key: your_orchestrator_key_here
name: "Your Orchestrator Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of the orchestrator's coordination mission and workflow focus.
tools:
  - ThinkTools
  - WorkspaceTools
  - WorkspacePlanningTools
  - AgentCloneTools
  # AgentTeamTools if team coordination
  # Additional tools as needed
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
  # Orchestrators typically benefit from reasoning budget for strategic planning
category:
  - "assist"  # Most orchestrators are assist, NOT domo
  - "your_domain"
  # Include specialist keys for team members if using AgentTeamTools
  # Additional categories as needed
persona: |
  # The persona content MUST be LAST
  # This contains all your component selections and custom instructions
```

### Critical Structure Rules for Orchestrators

1. **Field Order Matters**: Fields must appear in the exact order shown above
2. **Persona Must Be LAST**: The persona field must always be the final field in the YAML file
3. **Category = "assist"**: Most orchestrators should use "assist" category, NOT "domo" (unless user-facing)
4. **Required Tools**: ThinkTools, WorkspaceTools, WorkspacePlanningTools, AgentCloneTools are essential
5. **Reasoning Budget**: Orchestrators benefit from reasoning model with adequate budget_tokens

### Orchestrator-Specific Configuration Notes

**Tools Configuration**:
```yaml
tools:
  - ThinkTools              # Essential for strategic planning
  - WorkspaceTools          # Essential for state management
  - WorkspacePlanningTools  # Essential for coordination
  - AgentCloneTools         # Essential for delegation
  - AgentTeamTools          # Only if coordinating specialist team
```

**Category Configuration**:
```yaml
# Backend orchestrator (most common):
category:
  - "assist"
  - "your_domain"

# User-facing orchestrator (rare):
category:
  - "domo"
  - "your_domain"

# Team orchestrator:
category:
  - "assist"
  - "specialist_agent_1_key"
  - "specialist_agent_2_key"
  - "specialist_agent_3_key"
  - "your_domain"
```

**Agent Params for Orchestrators**:
```yaml
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000      # Higher budget for complex coordination
  max_tokens: 64000         # Large context for workflow management
```

## Getting Started

### Step-by-Step Orchestrator Creation

1. **Define Orchestration Mission**: Clearly identify the workflow coordination responsibility and scope
2. **Determine User-Facing Status**: Is this a backend orchestrator (assist) or user-facing (domo)?
3. **Make Binary Component Decisions**: Go through each component with clear YES/NO choices
4. **Identify Domain Specialization**: Does this orchestrator need domain-specific knowledge?
5. **Assess Team Coordination Needs**: Will this orchestrator manage specialist team members?
6. **Create Proper YAML Structure**: Use the exact field order with appropriate tool configuration
7. **Structure the Persona**: Use the typical structure template and arrange selected components logically
8. **Add Domain Expertise**: Include specialized domain knowledge sections if applicable
9. **Define Team Protocols**: Add team collaboration details if managing specialists
10. **Specify Workflows**: Document custom orchestration workflows and coordination procedures
11. **Define Success Metrics**: Establish quality standards and performance criteria
12. **Customize Personality**: Define strategic, oversight-focused communication style
13. **Validate YAML Structure**: Verify fields are in correct order with persona LAST
14. **Validate Component Composition**: Ensure all essential orchestrator components are included
15. **Test Coordination Patterns**: Verify delegation, validation, and recovery protocols work

### Quality Checklist

**Required for All Orchestrators**:
- ✅ Includes 'assist' in category array (unless user-facing)
- ✅ Critical Interaction Guidelines component (workspace safety)
- ✅ Reflection Rules component (strategic thinking)
- ✅ Workspace Organization component (state management)
- ✅ Critical Working Rules component (methodical discipline)
- ✅ Planning & Coordination component (essential)
- ✅ Clone Delegation component (essential)
- ✅ Context Management component (essential)
- ✅ Quality Gates component (essential)
- ✅ Strategic oversight-focused communication style

**Recommended Best Practices**:
- ✅ Team Collaboration component (if managing specialist team)
- ✅ Domain Knowledge sections (if domain-specialized)
- ✅ Custom workflow documentation (coordination procedures)
- ✅ Success metrics and quality standards defined
- ✅ Recovery and fallback protocols documented
- ✅ Clear delegation boundaries and responsibilities
- ✅ Validation criteria at workflow integration points

**Orchestrator-Specific Validation**:
- ✅ No task sequence anti-patterns in delegation instructions
- ✅ Context management strategies clearly defined
- ✅ Quality gates positioned at phase boundaries
- ✅ Metadata usage discipline documented
- ✅ Recovery protocols for context burnout included
- ✅ Team member roles and handoffs clearly defined (if team orchestrator)
- ✅ Domain validation criteria specified (if domain-specialized)

**YAML Configuration Validation**:
- ✅ Category includes "assist" not "domo" (unless user-facing)
- ✅ Tools include: ThinkTools, WorkspaceTools, WorkspacePlanningTools, AgentCloneTools
- ✅ AgentTeamTools included if managing specialist team
- ✅ Reasoning model with adequate budget_tokens
- ✅ Persona field is LAST in YAML structure

This binary component approach ensures that every orchestrator provides consistent, professional, and effective workflow coordination while maintaining the flexibility to specialize for specific domains, team structures, and coordination patterns using the core components currently available.
