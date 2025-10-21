# Specialist Agent (Assist) Guide

A comprehensive guide for building specialist agents that serve specific technical roles within multi-agent teams, focusing on deep domain expertise and professional deliverables.

## When to Use Specialist Agent Type

**Primary Purpose**: Agents designed for specific technical roles within teams, providing deep domain expertise

**Core Characteristics**:
- Deep domain expertise and specialization
- Team member role (not user-facing)
- Technical specialist focus
- Professional standards emphasis
- Quality deliverables and validation
- Direct agent-to-agent communication
- No human interaction protocols needed
- Assist category designation

**Typical Scenarios**:
- Software architecture and design specialists
- Implementation and coding specialists
- Testing strategy and validation specialists
- Requirements analysis specialists
- Documentation specialists within teams
- Technical review and quality assurance
- Domain-specific analysis and consultation
- Integration and technical coordination

**Key Requirements**:
- Must include 'assist' in agent category array
- Should include team collaboration components
- Optimized for agent-to-agent communication via AgentTeamTools
- Professional technical communication standards
- Deep domain knowledge sections

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your specialist agent's specific needs:

### 1. Critical Interaction Guidelines Component

**Does this specialist agent access workspaces or file paths?**

- **YES** → Use this component *(Applies to 80% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)

**Why Include**: Prevents wasted work on non-existent paths, provides immediate feedback on path errors, ensures consistent workspace verification behavior.

**When to Skip**: Pure analytical specialists without any file system access.

---

### 2. Human Pairing Component

**Does this specialist agent interact directly with users?**

- **YES** → This might not be a specialist (assist) agent - consider Domo type instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md) or [`human_pairing_development_component.md`](../01_core_components/human_pairing_development_component.md)

**Why Skip**: Specialist (assist) agents serve other agents, not end users. They communicate through AgentTeamTools, not conversational interfaces. Human pairing protocols create confusion in agent-to-agent interactions.

**Exception**: If your specialist needs user interaction, it should be categorized as 'domo' not 'assist'.

---

### 3. Reflection Rules Component

**Does this specialist agent have access to the ThinkTools?**

- **YES** → Use this component *(Applies to 90% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)

**Why Include**: Ensures systematic analysis of technical information, improves deliverable quality through structured thinking, creates reasoning logs for complex technical decisions.

**When to Skip**: Simple lookup or data transformation specialists where thinking logs aren't beneficial.

---

### 4. Workspace Organization Component

**Does this specialist use workspace tools for file and directory management?**

- **YES** → Use this component *(Applies to 85% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)

**Why Include**: Standardizes file management, supports team collaboration, provides systematic organization for deliverables, enables effective handoffs between specialists.

**When to Skip**: Specialists without any file management capabilities.

---

### 5. Critical Working Rules Component

**Does this specialist do complex multi-step workflows requiring methodical planning?**

- **YES** → Consider if this should be an orchestrator or domo agent instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)

**Why Skip**: Specialist agents are called by orchestrators or domo agents to perform focused tasks. Complex workflow management is typically the orchestrator's responsibility. Specialists focus on delivering their expertise, not managing workflows.

**Exception**: If your specialist needs complex workflow management, consider whether it should be categorized as 'domo' with orchestration capabilities.

---

### 6. Planning & Coordination Component

**Does this specialist coordinate multi-step workflows or manage complex projects?**

- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for most Specialist agents)*

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)

**Why Skip**: Specialists are typically called to perform specific technical tasks, not coordinate workflows. Orchestrators and domo agents handle planning and coordination.

**When to Include**: Only if the specialist itself needs to break down its own complex analysis into trackable sub-tasks. This is rare for most specialists.

---

### 7. Clone Delegation Component

**Does this specialist delegate work to clone agents?**

- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for most Specialist agents)*

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)

**Why Skip**: Specialists are typically focused executors, not delegators. Clone delegation is an orchestrator responsibility.

**When to Include**: Only if the specialist performs complex analysis that genuinely requires parallel clone work. This is rare and suggests the agent might better fit orchestrator category.

---

### 8A. Code Quality Standards Component (Python)

**Does this specialist write or modify Python code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)

**Why Include**: Ensures consistent Python code quality, prevents technical debt, provides systematic approach to development practices for implementation specialists.

**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 8B. Code Quality Standards Component (C#)

**Does this specialist write or modify C# code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)

**Why Include**: Ensures consistent C# code quality, follows .NET best practices, maintains enterprise-grade development standards for implementation specialists.

**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 8C. Code Quality Standards Component (TypeScript)

**Does this specialist write or modify TypeScript/JavaScript code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)

**Why Include**: Ensures consistent TypeScript development practices, maintains modern JavaScript standards, supports full-stack development quality for implementation specialists.

**When to Skip**: Non-coding specialists or specialists working in other languages.

---

### 9. Context Management Component

**Does this specialist coordinate complex workflows that might hit context limits?**

- **YES** → Consider if this should be an orchestrator agent instead
- **NO** → Skip this component *(Standard for Specialist agents)*

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)

**Why Skip**: Context management is primarily an orchestrator concern. Specialists perform focused tasks that typically stay within context limits.

**When to Include**: Only if the specialist performs genuinely complex analysis that requires context window management. This is rare for focused specialists.

---

### 10. Team Collaboration Component

**Is this specialist part of a multi-agent team with direct communication?**

- **YES** → Use this component *(Applies to 100% of team-based Specialist agents)*
- **NO** → Skip this component

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)

**Why Include**: Defines clear role boundaries, establishes handoff protocols between specialists, provides escalation paths, enables efficient agent-to-agent communication via AgentTeamTools.

**When to Skip**: Standalone specialists not integrated into teams (rare).

---

### 11. Quality Gates Component

**Does this specialist produce formal deliverables requiring validation?**

- **YES** → Use this component *(Applies to 90% of Specialist agents)*
- **NO** → Skip this component

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)

**Why Include**: Ensures deliverable quality, provides validation criteria, establishes completion signoff protocols, maintains professional standards for specialist outputs.

**When to Skip**: Simple lookup or data transformation specialists without formal deliverables.

---

### 12. Domain Knowledge Template Component

**Is this agent a specialist that needs structured domain expertise?**

- **YES** → Use this template structure *(Applies to 100% of Specialist agents)*
- **NO** → This might not be a true specialist agent

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)

**Why Include**: This is the CORE of specialist agents. Deep domain expertise is what makes a specialist valuable. The template provides consistent structure for organizing and presenting expertise.

**When to Skip**: Never for true specialists - domain expertise is their defining characteristic.

---

## Typical Structure and Composition Order

Based on the binary component decisions above, here's the recommended persona organization for specialist agents:

### Component Ordering Principle

**Recommended Order (Foundation → Domain Expertise → Team Integration)**:

1. **Identity and Specialization** (Custom)
   - Clear statement of domain expertise
   - Role within team or workflow
   - Primary deliverables and responsibilities

2. **Core Guidelines** (Critical Interaction Guidelines, Reflection Rules)
   - Establishes safety and thinking patterns
   - Foundation for technical work

3. **Operational Standards** (Workspace Organization, Code Quality)
   - Defines how the specialist performs technical work
   - Sets quality and organizational standards

4. **Deep Domain Expertise** (Domain Knowledge sections - EXTENSIVE)
   - The heart of the specialist agent
   - Methodologies, frameworks, best practices
   - Technical standards and validation criteria
   - This should be the LARGEST section

5. **Team Integration** (Team Collaboration, Quality Gates)
   - Defines how specialist works with other agents
   - Establishes deliverable standards
   - Provides handoff and escalation protocols

6. **Professional Personality** (Communication style, approach)
   - Technical precision and professionalism
   - Applied across all specialist activities

This ordering ensures technical foundation is established, deep expertise is central, and team integration wraps the specialist capabilities.

### Standard Specialist Agent Structure

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, domain focus, and primary technical responsibilities]

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

### Minimal Specialist Agent Structure

For simple technical lookup or transformation specialists:

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity and technical focus]

## [Domain Name] Expertise
[Focused domain knowledge and technical capabilities]

## Team Collaboration Protocols
[Basic team integration and communication]

# Professional Personality
[Technical, professional approach]
```

### Implementation-Focused Specialist Agent Structure

For coding and development specialists:

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, technical role, and implementation focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules  
[Systematic thinking and technical analysis requirements]

## Workspace Organization Guidelines
[Comprehensive file and code management]

## Code Quality Requirements - [Language]
[Language-specific development standards and practices]

## [Implementation Domain] Expertise
[EXTENSIVE implementation knowledge, patterns, and practices]
### Implementation Philosophy
### Design Patterns and Approaches
### Code Construction Best Practices
### Quality Standards and Validation
### Testing Integration
### Implementation Deliverables

## Team Collaboration Protocols
[Handoffs with architects, integration with testers, escalation to orchestrator]

## Quality Gates and Validation Framework
[Code quality validation, completion criteria, deliverable standards]

# Professional Personality and Communication Style
[Technically precise, standards-focused, quality-driven]
```

### Architecture-Focused Specialist Agent Structure

For design and architecture specialists:

```markdown
# Agent Identity and Domain Specialization
[Custom specialist identity, architectural role, and design focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Systematic architectural thinking and design analysis]

## Workspace Organization Guidelines
[Design document and diagram management]

## [Architecture Domain] Expertise
[EXTENSIVE architectural knowledge, methodologies, and frameworks]
### Architecture Philosophy
### Design Methodologies and Process
### Pattern Selection and Application
### Technology Evaluation and Selection
### Architecture Validation Frameworks
### Design Deliverables and Documentation Standards

## Team Collaboration Protocols
[Handoffs to implementers, coordination with testers, escalation protocols]

## Quality Gates and Validation Framework
[Design validation, architecture review criteria, deliverable standards]

# Professional Personality and Communication Style
[Strategic, comprehensive, pattern-focused, validation-driven]
```

## Customization Guidance

### Focus Area Adaptations

**Requirements Analysis Specialists**:
- Extensive requirements methodologies section
- Discovery and extraction techniques
- Classification and refinement frameworks
- Stakeholder analysis approaches
- No code quality components needed

**Architecture and Design Specialists**:
- Deep design pattern and methodology knowledge
- Technology evaluation frameworks
- Architecture validation approaches
- Design document standards
- Typically no code quality components (unless hands-on architect)

**Implementation and Coding Specialists**:
- Appropriate Code Quality Standards component
- Implementation patterns and practices
- Code construction methodologies
- Testing integration protocols
- Technical precision emphasis

**Testing Strategy Specialists**:
- Testing methodologies and frameworks
- Strategy development approaches
- Coverage and validation criteria
- Quality assurance standards
- May include code quality for test code

**Integration Specialists**:
- Integration patterns and approaches
- System coordination methodologies
- Interface design standards
- Handoff and validation protocols
- May include code quality for integration code

### Domain Expertise Depth

**Critical Success Factor**: The domain expertise section should be the LARGEST and most detailed part of specialist agents.

**Depth Indicators**:
- **Light Specialist** (300-500 words): Basic methodologies and patterns
- **Standard Specialist** (500-1000 words): Comprehensive approaches and frameworks
- **Deep Specialist** (1000-2000+ words): Extensive methodologies, validation frameworks, quality criteria

**Expertise Organization**:
```markdown
## [Domain Name] Expertise

### [Domain] Philosophy
[Core beliefs and approaches to the domain - 100-200 words]

### [Domain] Methodologies  
[Key methodologies and when to apply them - 200-400 words]

### [Domain] Best Practices
[Proven patterns and standards - 200-400 words]

### [Domain] Tools and Techniques
[Specific tools and when to use them - 200-300 words]

### [Domain] Quality Standards
[Validation criteria and quality frameworks - 200-400 words]

### [Domain] Deliverables
[What the specialist produces and standards - 100-200 words]
```

### Team Integration Patterns

**Specialist-to-Specialist Communication**:
- Use AgentTeamTools for direct communication
- List other team specialist agent keys in Team Collaboration section
- Define clear handoff protocols between specialists
- Establish validation checkpoints

**Specialist-to-Orchestrator Escalation**:
- Define clear escalation triggers
- Establish conflict resolution protocols
- Provide progress reporting guidelines
- Set quality gate signoff requirements

**Specialist Deliverable Standards**:
- Clear output format specifications
- Quality validation criteria
- Completeness requirements
- Integration readiness checks

### Communication Style Customization

**Technical Precision Focus**:
- Detailed, specific technical language
- Standards-driven communication
- Validation-focused approach
- Professional, authoritative tone

**Analytical Depth Focus**:
- Comprehensive analysis style
- Systematic exploration approach
- Evidence-based recommendations
- Thorough documentation

**Quality Assurance Focus**:
- Validation-centric communication
- Risk identification emphasis
- Standards compliance focus
- Quality gate enforcement

**Maintain Specialist Characteristics**:
- Always technically precise
- Professional and authoritative
- Standards and quality focused
- Clear deliverable orientation
- Agent-to-agent communication optimized

## Real Examples from the Ecosystem

### Requirements Analysis Specialist
**Agent**: `rex_requirements_miner.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines  
- ✅ Reflection Rules
- ✅ Workspace Organization
- ❌ Code Quality Standards (not a coding specialist)
- ✅ Team Collaboration
- ✅ Quality Gates
- ✅ Domain Knowledge Template (Requirements Analysis)

**Characteristics**: Deep requirements extraction expertise, systematic analysis approach, stakeholder-focused, team integration for handoffs

---

### Architecture Specialist  
**Agent**: `aria_csharp_architect.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Reflection Rules  
- ✅ Workspace Organization
- ❌ Code Quality Standards (architecture focus, not implementation)
- ✅ Team Collaboration
- ✅ Quality Gates
- ✅ Domain Knowledge Template (Software Architecture)

**Characteristics**: Design pattern expertise, architecture methodologies, validation frameworks, technical precision, strategic thinking

---

### Implementation Specialist
**Agent**: `mason_csharp_craftsman.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Reflection Rules
- ✅ Workspace Organization  
- ✅ Code Quality Standards (C#)
- ✅ Team Collaboration
- ✅ Quality Gates
- ✅ Domain Knowledge Template (Implementation)

**Characteristics**: Code construction expertise, quality focus, implementation patterns, testing integration, professional standards

---

### Testing Strategy Specialist
**Agent**: `vera_test_strategist.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Reflection Rules  
- ✅ Workspace Organization
- ✅ Code Quality Standards (for test code)
- ✅ Team Collaboration
- ✅ Quality Gates
- ✅ Domain Knowledge Template (Testing Strategy)

**Characteristics**: Testing methodologies expertise, strategy development, quality assurance focus, validation frameworks, comprehensive coverage

---

## Component Integration Benefits

### Why Binary Decisions Work for Specialists

**For Specialist Agents Specifically**:
- **Focus on Expertise**: Binary decisions keep focus on domain knowledge, not workflow complexity
- **Clear Team Role**: Component-based approach defines specialist's place in team
- **Professional Standards**: Components maintain quality baseline across specialist outputs
- **Efficient Communication**: Binary choices optimize agent-to-agent interactions

**Quality Outcomes**:
- **Consistent Expertise Delivery**: Specialists with similar components deliver predictably
- **Clear Handoffs**: Team collaboration components ensure smooth specialist-to-specialist transitions
- **Quality Deliverables**: Quality gates enforce professional standards for outputs
- **Reduced Complexity**: Binary choices eliminate workflow management from specialists

### Integration Patterns for Specialists

**Essential Specialist Component Combinations**:
- Domain Knowledge + Quality Gates = Professional deliverables
- Team Collaboration + Quality Gates = Smooth handoffs with validation
- Reflection Rules + Domain Knowledge = Thoughtful expert analysis
- Workspace Organization + Team Collaboration = Effective file-based handoffs

**Team Integration Benefits**:
- **Clear Roles**: Each specialist has defined expertise area
- **Efficient Communication**: AgentTeamTools enable direct specialist communication
- **Quality Validation**: Quality gates ensure deliverable standards
- **Smooth Handoffs**: Team collaboration protocols prevent integration issues

## Proper YAML Configuration Structure for Specialists

**CRITICAL**: Specialist agent YAML files must follow the exact field order and use 'assist' category designation.

### Required Field Order for Specialist Agents

```yaml
version: 2
key: your_specialist_key_here
name: "Your Specialist Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of the specialist's domain expertise and role.
tools:
  - ThinkTools
  - WorkspaceTools
  - AgentTeamTools  # REQUIRED for team specialists
  # Additional tools as needed
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
  # Additional parameters as needed
category:
  - "assist"  # REQUIRED for specialist agents
  - "orchestrator_key"  # If part of an orchestrator's team
  - "your_domain"
  # Additional categories as needed
persona: |
  # The persona content MUST be LAST
  # This contains all your component selections and domain expertise
```

### Critical Specialist Configuration Rules

1. **Category Must Include 'assist'**: Specialist agents use 'assist' category, NOT 'domo'
2. **AgentTeamTools Required**: For team-based specialists, include AgentTeamTools for direct communication
3. **Team Relationships**: Include orchestrator or team lead agent key in category array
4. **Persona Must Be LAST**: The persona field must always be the final field in the YAML file
5. **Required Fields**: All fields shown above are required for proper specialist function

### Common Specialist Configuration Errors to Avoid

❌ **WRONG - Using 'domo' for specialist:**
```yaml
category:
  - "domo"  # ← WRONG! Specialists use 'assist'
  - "architecture"
```

✅ **CORRECT - Using 'assist' for specialist:**
```yaml
category:
  - "assist"  # ← CORRECT! Specialists are 'assist' category
  - "team_lead_key"  # Team relationship
  - "architecture"  # Domain
```

❌ **WRONG - Missing AgentTeamTools:**
```yaml
tools:
  - ThinkTools
  - WorkspaceTools
  # ← MISSING AgentTeamTools for team communication
```

✅ **CORRECT - Including AgentTeamTools:**
```yaml
tools:
  - ThinkTools
  - WorkspaceTools
  - AgentTeamTools  # ← CORRECT! Enables team communication
```

## Getting Started with Specialist Agents

### Step-by-Step Specialist Creation

1. **Define Domain Expertise**: Clearly identify the specialist's technical domain and deliverables
2. **Determine Team Role**: Identify how this specialist integrates with other agents
3. **Make Binary Decisions**: Go through each component with clear YES/NO choices
4. **Choose Language Variants**: Select appropriate Code Quality component if coding specialist
5. **Create Proper YAML Structure**: Use the exact field order with 'assist' category
6. **Structure the Persona**: Use typical structure with EXTENSIVE domain expertise section
7. **Detail Team Integration**: Define collaboration protocols and handoff points
8. **Establish Quality Gates**: Define deliverable standards and validation criteria
9. **Validate YAML Structure**: Verify 'assist' category, AgentTeamTools, proper field order
10. **Test Team Integration**: Verify specialist works smoothly with team members

### Specialist Quality Checklist

**Required for All Specialist Agents**:
- ✅ Includes 'assist' in category array (NOT 'domo')
- ✅ Extensive domain expertise section (largest part of persona)
- ✅ Clear team integration protocols
- ✅ Professional technical communication style
- ✅ Quality gates for deliverables
- ✅ AgentTeamTools for team-based specialists

**Recommended Best Practices**:  
- ✅ Safe workspace operations (Critical Interaction Guidelines for workspace specialists)
- ✅ Structured thinking for quality analysis (Reflection Rules for complex analysis)
- ✅ Organized file management for collaboration (Workspace Organization for deliverables)
- ✅ Code quality standards (Language-appropriate components for coding specialists)
- ✅ Team collaboration protocols (for all team-based specialists)

**Quality Validation**:
- ✅ Component selections match specialist capabilities and role
- ✅ Domain expertise is deep, comprehensive, and well-organized
- ✅ Team integration clearly defined with handoff protocols
- ✅ Quality gates establish clear deliverable standards
- ✅ Professional technical communication style throughout
- ✅ No workflow management complexity (leave that to orchestrators)
- ✅ Focus remains on delivering expertise, not coordinating work

## Key Differences: Specialist vs. Domo Agents

### When to Choose Specialist (Assist) vs. Domo

**Choose Specialist (Assist) When**:
- ✅ Agent serves other agents, not end users
- ✅ Deep technical expertise is primary value
- ✅ Part of a multi-agent team
- ✅ Focused deliverables to other agents
- ✅ No user conversation interface needed

**Choose Domo When**:
- ✅ Agent interacts directly with users
- ✅ Conversational interface is primary mode
- ✅ User collaboration and guidance needed
- ✅ Human pairing protocols required
- ✅ User-facing personality important

### Configuration Differences

| Aspect | Specialist (Assist) | Domo |
|--------|-------------------|------|
| Category | `assist` | `domo` |
| User Interaction | No | Yes |
| Human Pairing | No | Yes |
| Team Collaboration | Yes (AgentTeamTools) | Optional |
| Domain Expertise | Extensive (Core) | Variable |
| Workflow Management | No (orchestrator does this) | Yes |
| Communication Style | Technical, precise | Conversational, approachable |
| Primary Interface | Agent-to-agent | User-to-agent |

This binary component approach ensures that every Specialist agent provides deep, focused expertise with clear team integration while maintaining professional quality standards. Specialists excel at delivering technical value within multi-agent teams without the complexity of user interaction or workflow orchestration.
