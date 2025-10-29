# Specialist Agent (Assist) Guide

A guide for building specialist agents that serve specific technical roles within multi-agent teams, focusing on deep domain expertise.

## When to Use Specialist Agent Type

**Primary Purpose**: Agents designed for specific technical roles within teams, providing deep domain expertise

**Core Characteristics**:
- Deep domain expertise and specialization
- Team member role (not user-facing)
- Technical specialist focus
- Professional standards emphasis
- Direct agent-to-agent communication

**Typical Scenarios**:
- Software architecture and design specialists
- Implementation and coding specialists
- Testing strategy and validation specialists
- Requirements analysis specialists
- Technical review and quality assurance

**Key Requirements**:
- Must include 'assist' in agent category array
- Should include team collaboration components
- Optimized for agent-to-agent communication via AgentTeamTools

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision:

### 1. Critical Interaction Guidelines Component

**Does this specialist agent access workspaces or file paths?**
- **YES** → Use this component *(80% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)  
**Why Include**: Prevents wasted work on non-existent paths, ensures workspace verification.  
**When to Skip**: Pure analytical specialists without file system access.

---

### 2. Human Pairing Component

**Does this specialist agent interact directly with users?**
- **YES** → This might not be a specialist (assist) agent - consider Domo type instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)  
**Why Skip**: Specialist (assist) agents serve other agents, not end users.  
**When to Include**: If specialist needs user interaction, it should be categorized as 'domo' not 'assist'.

---

### 3. Reflection Rules Component

**Does this specialist agent have access to ThinkTools?**
- **YES** → Use this component *(90% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)  
**Why Include**: Ensures systematic analysis, improves deliverable quality through structured thinking.  
**When to Skip**: Simple lookup or data transformation specialists.

---

### 4. Workspace Organization Component

**Does this specialist use workspace tools for file management?**
- **YES** → Use this component *(85% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)  
**Why Include**: Standardizes file management, supports team collaboration, enables handoffs between specialists.  
**When to Skip**: Specialists without file management capabilities.

---

### 5. Critical Working Rules Component

**Does this specialist do complex multi-step workflows requiring methodical planning?**
- **YES** → Consider if this should be an orchestrator or domo agent instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)  
**Why Skip**: Specialists are called to perform focused tasks, not manage workflows.  
**When to Include**: Only if specialist needs complex workflow management (rare - consider orchestrator category).

---

### 6. Planning & Coordination Component

**Does this specialist coordinate multi-step workflows or manage complex projects?**
- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for most Specialist agents)*

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)  
**Why Skip**: Specialists perform specific technical tasks, not coordinate workflows.  
**When to Include**: Only if specialist breaks down its own complex analysis into sub-tasks (rare).

---

### 7. Clone Delegation Component

**Does this specialist delegate work to clone agents?**
- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for most Specialist agents)*

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)  
**Why Skip**: Specialists are focused executors, not delegators.  
**When to Include**: Only if specialist performs complex analysis requiring parallel clone work (rare).

---

### 8A. Code Quality Standards Component (Python)

**Does this specialist write or modify Python code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)  
**Why Include**: Ensures consistent Python code quality for implementation specialists.  
**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 8B. Code Quality Standards Component (C#)

**Does this specialist write or modify C# code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)  
**Why Include**: Ensures consistent C# code quality, follows .NET best practices for implementation specialists.  
**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 8C. Code Quality Standards Component (TypeScript)

**Does this specialist write or modify TypeScript/JavaScript code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)  
**Why Include**: Ensures consistent TypeScript development practices for implementation specialists.  
**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 9. Context Management Component

**Does this specialist coordinate complex workflows that might hit context limits?**
- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)  
**Why Skip**: Context management is primarily an orchestrator concern.  
**When to Include**: Only if specialist performs genuinely complex analysis requiring context window management (rare).

---

### 10. Team Collaboration Component

**Is this specialist part of a multi-agent team with direct communication?**
- **YES** → Use this component *(100% of team-based Specialist agents)*
- **NO** → Skip this component

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)  
**Why Include**: Defines clear role boundaries, establishes handoff protocols, enables agent-to-agent communication.  
**When to Skip**: Standalone specialists not integrated into teams (rare).

---

### 11. Quality Gates Component

**Does this specialist produce formal deliverables requiring validation?**
- **YES** → Use this component *(90% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)  
**Why Include**: Ensures deliverable quality, provides validation criteria, establishes completion signoff protocols.  
**When to Skip**: Simple lookup or data transformation specialists without formal deliverables.

---

### 12. Domain Knowledge Template Component

**Is this agent a specialist that needs structured domain expertise?**
- **YES** → Use this template structure *(100% of Specialist agents)*
- **NO** → This might not be a true specialist agent

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)  
**Why Include**: This is the CORE of specialist agents - deep domain expertise is their defining characteristic.  
**When to Skip**: Never for true specialists - domain expertise is essential.

## Structure Templates

### Standard Specialist Agent Structure

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, domain focus, technical responsibilities]

## Critical Interaction Guidelines
[If workspace access - YES/NO decision]

## Reflection Rules
[If ThinkTools access - YES/NO decision]

## Workspace Organization Guidelines  
[If workspace tools - YES/NO decision]

## Code Quality Requirements
[If coding specialist - Choose Python/C#/TypeScript variant]

## [Domain Name] Expertise
[EXTENSIVE custom domain knowledge sections - This is the CORE]
### [Domain] Philosophy
### [Domain] Methodologies  
### [Domain] Best Practices
### [Domain] Tools and Techniques
### [Domain] Quality Standards
### [Domain] Deliverables

## Team Collaboration Protocols
[Team member directory, coordination principles, escalation protocols]

## Quality Gates and Validation Framework
[Output validation, completion signoff, quality criteria]

# Professional Personality and Communication
[Technical precision, professional standards, collaboration approach]
```

### Implementation-Focused Specialist Structure

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, technical role, implementation focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules  
[Systematic thinking and technical analysis]

## Workspace Organization Guidelines
[Comprehensive file and code management]

## Code Quality Requirements - [Language]
[Language-specific development standards]

## [Implementation Domain] Expertise
[EXTENSIVE implementation knowledge, patterns, practices]
### Implementation Philosophy
### Design Patterns and Approaches
### Code Construction Best Practices
### Quality Standards and Validation
### Testing Integration
### Implementation Deliverables

## Team Collaboration Protocols
[Handoffs with architects, integration with testers]

## Quality Gates and Validation Framework
[Code quality validation, completion criteria]

# Professional Personality and Communication Style
[Technically precise, standards-focused, quality-driven]
```

### Architecture-Focused Specialist Structure

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, architectural role, design focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Systematic architectural thinking and design analysis]

## Workspace Organization Guidelines
[Design document and diagram management]

## [Architecture Domain] Expertise
[EXTENSIVE architectural knowledge, methodologies, frameworks]
### Architecture Philosophy
### Design Methodologies and Process
### Pattern Selection and Application
### Technology Evaluation and Selection
### Architecture Validation Frameworks
### Design Deliverables and Documentation Standards

## Team Collaboration Protocols
[Handoffs to implementers, coordination with testers]

## Quality Gates and Validation Framework
[Design validation, architecture review criteria]

# Professional Personality and Communication Style
[Strategic, comprehensive, pattern-focused, validation-driven]
```

## Customization Guidance

**Requirements Analysis Specialists**:
- Extensive requirements methodologies section
- Discovery and extraction techniques
- Classification and refinement frameworks
- No code quality components needed

**Architecture and Design Specialists**:
- Deep design pattern and methodology knowledge
- Technology evaluation frameworks
- Architecture validation approaches
- Typically no code quality components (unless hands-on architect)

**Implementation and Coding Specialists**:
- Appropriate Code Quality Standards component
- Implementation patterns and practices
- Code construction methodologies
- Testing integration protocols

**Testing Strategy Specialists**:
- Testing methodologies and frameworks
- Strategy development approaches
- Coverage and validation criteria
- May include code quality for test code

**Domain Expertise Depth**:
- Light Specialist (300-500 words): Basic methodologies and patterns
- Standard Specialist (500-1000 words): Comprehensive approaches and frameworks
- Deep Specialist (1000-2000+ words): Extensive methodologies, validation frameworks, quality criteria

**Communication Style Options**:
- Technical Precision Focus: Detailed, specific technical language, standards-driven
- Analytical Depth Focus: Comprehensive analysis, systematic exploration, evidence-based
- Quality Assurance Focus: Validation-centric, risk identification, standards compliance

## YAML Configuration Structure

**CRITICAL**: Specialist agent YAML files must use 'assist' category designation.

```yaml
version: 2
key: your_specialist_key_here
name: "Your Specialist Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of specialist's domain expertise and role.
tools:
  - ThinkTools
  - WorkspaceTools
  - AgentTeamTools  # REQUIRED for team specialists
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
category:
  - "assist"  # REQUIRED for specialist agents
  - "orchestrator_key"  # If part of orchestrator's team
  - "your_domain"
persona: |
  # The persona content MUST be LAST
```

**Critical Rules**:
- Category must include 'assist' (NOT 'domo')
- AgentTeamTools required for team-based specialists
- Include orchestrator or team lead agent key in category array
- Persona must be LAST field in YAML file

## Getting Started

**Step-by-Step Creation**:
1. Define domain expertise and technical deliverables
2. Determine team role and integration with other agents
3. Make binary decisions for each component (YES/NO)
4. Choose language-appropriate Code Quality component if coding specialist
5. Create proper YAML structure with 'assist' category
6. Structure persona with EXTENSIVE domain expertise section (largest part)
7. Detail team integration and collaboration protocols

**Quality Checklist**:
- ✅ Includes 'assist' in category array (NOT 'domo')
- ✅ Extensive domain expertise section (largest part of persona)
- ✅ Clear team integration protocols
- ✅ Professional technical communication style
- ✅ Quality gates for deliverables
- ✅ AgentTeamTools for team-based specialists
- ✅ Focus on delivering expertise, not coordinating work
