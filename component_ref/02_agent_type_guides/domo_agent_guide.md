# Domo Agent Guide

A guide for building agents that interact directly with users, focusing on core components available in the Agent C framework.

## When to Use Domo Agent Type

**Primary Purpose**: Agents designed for direct user interaction and collaboration

**Core Characteristics**:
- Direct user interaction and conversation
- Safe workspace and path handling
- Structured thinking and reflection
- Organized file and workspace management
- Professional, approachable personality

**Typical Scenarios**:
- General-purpose user assistance and consultation
- Development pair programming and code collaboration
- Documentation creation and content development
- Code review and quality assurance
- Technical analysis and consultation

**Key Requirements**:
- Must include 'domo' in agent category array
- Should include appropriate core components based on capabilities
- Professional communication standards

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision:

### 1. Critical Interaction Guidelines Component

**Does this agent access workspaces or file paths?**
- **YES** → Use this component *(85% of Domo agents)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)  
**Why Include**: Prevents wasted work on non-existent paths, provides immediate feedback on errors.  
**When to Skip**: Pure conversational agents without file system access.

---

### 2. Reflection Rules Component

**Does this agent have access to ThinkTools?**
- **YES** → Use this component *(80% of Domo agents)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)  
**Why Include**: Ensures systematic processing, improves response quality through structured thinking.  
**When to Skip**: Simple conversational agents where thinking logs aren't beneficial.

---

### 3. Workspace Organization Component

**Does this agent use workspace tools for file management?**
- **YES** → Use this component *(90% of workspace-enabled Domo agents)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)  
**Why Include**: Standardizes file management, supports user collaboration, enables workspace handoffs.  
**When to Skip**: Agents without file management capabilities.

---

### 4A. Code Quality Standards Component (Python)

**Does this agent write or modify Python code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)  
**Why Include**: Ensures consistent Python code quality, prevents technical debt.  
**When to Skip**: Non-coding agents or agents working in other languages.

---

### 4B. Code Quality Standards Component (C#)

**Does this agent write or modify C# code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)  
**Why Include**: Ensures consistent C# code quality, follows .NET best practices.  
**When to Skip**: Non-coding agents or agents working in other languages.

---

### 4C. Code Quality Standards Component (TypeScript)

**Does this agent write or modify TypeScript/JavaScript code?**
- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)  
**Why Include**: Ensures consistent TypeScript development practices, maintains modern JavaScript standards.  
**When to Skip**: Non-coding agents or agents working in other languages.

## Structure Templates

### Standard Domo Agent Structure

```markdown
# Agent Identity and Core Purpose
[Custom agent identity, role, and primary mission]

## Critical Interaction Guidelines
[If workspace access - YES/NO decision]

## Reflection Rules
[If ThinkTools access - YES/NO decision]

## Workspace Organization Guidelines  
[If workspace tools - YES/NO decision]

## Code Quality Requirements
[If coding agent - Choose Python/C#/TypeScript variant]

## [Domain Name] Expertise
[Custom domain knowledge and specialized skills]

# Personality and Communication Style
[Custom personality traits and user interaction style]

# Reference Materials
[Links to relevant documentation or resources]
```

### Minimal Domo Agent Structure

```markdown
# Agent Identity and Core Purpose
[Custom agent identity and mission]

# Personality and Communication Style  
[Custom personality and communication approach]
```

### Development-Focused Domo Agent Structure

```markdown
# Agent Identity and Core Purpose
[Custom agent identity, role, and technical focus]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules  
[Systematic thinking and analysis requirements]

## Workspace Organization Guidelines
[Comprehensive file and collaboration management]

## Code Quality Requirements - [Language]
[Language-specific development standards]

## [Technical Domain] Expertise
[Specialized technical knowledge and methodologies]

# Personality and Communication Style
[Professional, collaborative, technically precise]

# Reference Materials
[Technical standards, best practices, development resources]
```

## Customization Guidance

**General Purpose Domo Agents**:
- Focus on communication and collaboration skills
- Include broad problem-solving approaches
- Emphasize user guidance and support
- Consider Critical Interaction Guidelines if workspace access needed

**Development-Focused Domo Agents**:
- Include appropriate Code Quality Standards component
- Emphasize technical precision and standards
- Include Critical Interaction Guidelines for safe workspace operations
- Use Reflection Rules for systematic code analysis

**Documentation-Focused Domo Agents**:
- Include Workspace Organization component
- Emphasize content quality and organization
- Use structured approaches to document creation
- Consider Reflection Rules for comprehensive analysis

**Domain-Specific Considerations**:
- Add industry-specific knowledge and compliance requirements
- Include specialized tools and methodologies
- Adapt components for domain-specific workspace patterns
- Customize for professional communication protocols

**Personality Options**:
- Professional Consultant: Formal, analytical, recommendation-focused
- Collaborative Partner: Friendly, supportive, guidance-oriented  
- Technical Expert: Precise, detailed, standards-focused
- Creative Collaborator: Innovative, exploratory, idea-generating

## YAML Configuration Structure

**CRITICAL**: Agent YAML files must follow the exact field order shown below to prevent loading failures.

```yaml
version: 2
key: your_agent_key_here
name: "Your Agent Display Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of agent's purpose and capabilities.
tools:
  - ThinkTools
  - WorkspaceTools
  # Additional tools as needed
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
category:
  - "domo"
  - "your_domain"
persona: |
  # The persona content MUST be LAST
  # Contains all component selections and custom instructions
```

**Critical Rules**:
- Field order matters - fields must appear in exact order shown
- Persona must be LAST field in YAML file
- Category array must include "domo" for user-facing agents

## Getting Started

**Step-by-Step Creation**:
1. Define agent purpose and user interaction model
2. Make binary decisions for each component (YES/NO)
3. Choose language-appropriate Code Quality component if applicable
4. Create proper YAML structure with correct field order
5. Structure persona using template, arrange components logically
6. Add domain expertise and custom sections as needed
7. Customize personality while maintaining Domo characteristics

**Quality Checklist**:
- ✅ Includes 'domo' in category array
- ✅ Clear user-focused communication style
- ✅ Professional interaction standards
- ✅ Safe workspace operations (Critical Interaction Guidelines for workspace agents)
- ✅ Structured thinking (Reflection Rules for complex agents)
- ✅ Organized file management (Workspace Organization for file operations)
- ✅ Code quality standards (Language-appropriate components for development agents)
