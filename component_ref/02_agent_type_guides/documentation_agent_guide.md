# Documentation Agent Guide

A comprehensive guide for building agents that focus on content creation, organization, and client-ready preparation within the Agent C framework.

## When to Use Documentation Agent Type

**Primary Purpose**: Agents designed for creating, organizing, and preparing high-quality documentation and content

**Core Characteristics**:
- Content quality and professional polish focus
- Systematic organization and structure expertise
- Client-ready preparation protocols
- Navigation and usability optimization
- Stakeholder communication standards
- Multi-format content handling
- Comprehensive documentation workflows
- Professional presentation emphasis

**Typical Scenarios**:
- Technical documentation creation and maintenance
- Content organization and information architecture
- Document preparation for client delivery
- Knowledge base development and curation
- Reference material compilation and structuring
- Documentation system design and implementation
- Content quality assurance and refinement
- Strategic document development and planning

**Key Requirements**:
- Must include 'domo' in agent category array
- Should include appropriate core components based on scope
- Optimized for content quality and organization
- Professional documentation standards

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your documentation agent's specific needs:

### 1. Critical Interaction Guidelines Component

**Does this documentation agent access workspaces or file paths?**

- **YES** → Use this component *(Applies to 100% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)

**Why Include**: Documentation agents always work with files and workspaces. This component prevents wasted work on non-existent paths and ensures immediate user feedback on path errors.

**When to Skip**: Never skip for documentation agents - file access is fundamental to their role.

---

### 2. Reflection Rules Component

**Does this documentation agent have access to the ThinkTools?**

- **YES** → Use this component *(Applies to 100% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)

**Why Include**: Documentation requires careful analysis of content, structure, and organization. Systematic thinking ensures comprehensive coverage, proper organization, and quality content creation.

**When to Skip**: Only if the agent doesn't have ThinkTools, but this severely limits documentation quality.

---

### 3. Workspace Organization Component

**Does this documentation agent use workspace tools for file and directory management?**

- **YES** → Use this component *(Applies to 100% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)

**Why Include**: Documentation agents must maintain organized file structures, manage multiple document versions, and support collaborative workflows. This component is essential for systematic documentation management.

**When to Skip**: Never skip for documentation agents - organized file management is core to their function.

---

### 4A. Code Quality Standards Component (Python)

**Does this documentation agent write or modify Python code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)

**Why Include**: For documentation agents that generate code examples, documentation tooling, or automation scripts in Python.

**When to Skip**: Pure content-focused documentation agents without code generation needs.

---

### 4B. Code Quality Standards Component (C#)

**Does this documentation agent write or modify C# code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)

**Why Include**: For documentation agents focused on C# technical documentation with code examples or tooling.

**When to Skip**: Documentation agents not working with C# codebases.

---

### 4C. Code Quality Standards Component (TypeScript)

**Does this documentation agent write or modify TypeScript/JavaScript code?**

- **YES** → Use this component
- **NO** → Skip OR use language-appropriate variant

**Reference**: [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)

**Why Include**: For documentation agents creating TypeScript/JavaScript technical documentation or tooling.

**When to Skip**: Documentation agents not working with TypeScript/JavaScript content.

---

### 5. Planning & Coordination Component

**Does this documentation agent coordinate large documentation projects or multi-phase content development?**

- **YES** → Use this component *(Applies to 75% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)

**Why Include**: Large documentation efforts require systematic planning, progress tracking, and coordination across multiple content pieces. Essential for comprehensive documentation projects.

**When to Skip**: Simple, single-document focused agents without multi-step workflows.

---

### 6. Clone Delegation Component

**Does this documentation agent delegate content creation tasks to clone agents for large projects?**

- **YES** → Use this component *(Applies to 60% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)

**Why Include**: Large documentation projects benefit from delegating specific content sections to focused clones while maintaining overall quality and consistency.

**When to Skip**: Agents handling small to medium documentation tasks that don't require parallel content development.

---

### 7. Human Pairing Component (General Focus)

**Does this documentation agent interact directly with users for content collaboration?**

- **YES** → Use this component *(Applies to 100% of Domo Documentation agents)*
- **NO** → Skip this component

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)

**Why Include**: Documentation agents work closely with users to understand content requirements, gather domain knowledge, and ensure stakeholder alignment. This component establishes clear collaboration protocols.

**When to Skip**: Never skip for domo documentation agents - user collaboration is fundamental to gathering accurate content requirements.

---

### 8. Human Pairing Component (Development Focus)

**Does this documentation agent focus specifically on technical software development documentation?**

- **YES** → Use this component instead of General Focus
- **NO** → Use General Focus variant

**Reference**: [`human_pairing_development_component.md`](../01_core_components/human_pairing_development_component.md)

**Why Include**: For documentation agents creating API documentation, code documentation, or technical development guides that require close collaboration with developers.

**When to Skip**: Use General Focus variant for non-development-focused documentation agents.

---

### 9. Critical Working Rules Component

**Does this documentation agent perform complex, multi-step documentation work requiring methodical planning?**

- **YES** → Use this component *(Applies to 90% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)

**Why Include**: Documentation quality depends on methodical approaches, thorough analysis, and systematic content development. This component enforces quality-focused workflows.

**When to Skip**: Only for very simple documentation agents with minimal workflows.

---

### 10. Context Management Component

**Does this documentation agent manage large, complex documentation projects that might approach context limits?**

- **YES** → Use this component *(Applies to 50% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)

**Why Include**: Large documentation projects with extensive content, multiple references, and complex organization can approach context limits. This component provides strategies for managing context effectively.

**When to Skip**: Agents working on smaller, focused documentation tasks that don't strain context windows.

---

### 11. Team Collaboration Component

**Is this documentation agent part of a multi-agent documentation team with direct communication?**

- **YES** → Use this component *(Applies to 20% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)

**Why Include**: For documentation agents working in specialized teams with role-specific responsibilities (e.g., technical writer, editor, formatter, publisher).

**When to Skip**: Solo documentation agents that work independently without team coordination.

---

### 12. Quality Gates Component

**Does this documentation agent require formal content quality validation and approval checkpoints?**

- **YES** → Use this component *(Applies to 85% of Documentation agents)*
- **NO** → Skip this component

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)

**Why Include**: Documentation quality requires systematic validation of content accuracy, completeness, formatting, and stakeholder alignment. Quality gates ensure professional polish and client-ready output.

**When to Skip**: Only for informal or draft-stage documentation agents without quality validation requirements.

---

### 13. Domain Knowledge Template Component

**Does this documentation agent specialize in specific documentation domains or methodologies?**

- **YES** → Use this template structure *(Applies to 100% of specialized Documentation agents)*
- **NO** → Skip this component

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)

**Why Include**: Documentation agents benefit from structured domain expertise sections covering documentation methodologies, content standards, organization principles, and quality frameworks specific to their focus area.

**When to Skip**: Only for generic documentation agents without specialized methodologies or domain focus.

---

## Typical Structure and Composition Order

Based on the binary component decisions above, here's the recommended persona organization for documentation agents:

### Component Ordering Principle

**Recommended Order (Foundation → Operations → Expertise → Quality)**:

1. **Core Guidelines First** (Critical Interaction Guidelines, Human Pairing, Reflection Rules)
   - Establishes safety, collaboration protocols, and thinking patterns
   - Foundation for all documentation work

2. **Operational Standards** (Workspace Organization, Critical Working Rules)
   - Defines systematic documentation workflows
   - Sets organizational and methodical standards

3. **Project Management** (Planning & Coordination, Clone Delegation, Context Management)
   - Manages large documentation projects
   - Coordinates content development

4. **Domain Expertise** (Documentation methodologies and standards)
   - Specialized documentation knowledge
   - Content quality frameworks

5. **Quality Assurance** (Quality Gates)
   - Content validation protocols
   - Client-ready preparation standards

6. **Personality Last** (Communication style, approach)
   - Professional, detail-oriented communication
   - Applied across all documentation activities

This ordering ensures that collaboration protocols and systematic approaches are established before adding specialized documentation expertise and quality frameworks.

### Standard Documentation Agent Structure

```markdown
# Agent Identity and Core Purpose
[Custom agent identity, role, and documentation mission]

## Human Pairing Protocol
[General Focus for most documentation agents]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Systematic content analysis and thinking requirements]

## Workspace Organization Guidelines
[Comprehensive documentation file management]

## Critical Working Rules
[Methodical documentation workflow requirements]

## Planning & Coordination
[If large documentation projects - YES/NO decision]

## Clone Delegation Framework
[If large content projects - YES/NO decision]

## Context Management Strategies
[If complex documentation projects - YES/NO decision]

## Documentation Expertise
[Documentation methodologies, standards, and frameworks]

## Quality Gates Framework
[Content quality validation protocols]

# Personality and Communication Style
[Professional, detail-oriented, stakeholder-focused]

# Reference Materials
[Documentation standards, style guides, best practices]
```

### Minimal Documentation Agent Structure

For simple, focused documentation tasks:

```markdown
# Agent Identity and Core Purpose
[Custom agent identity and documentation focus]

## Human Pairing Protocol
[User collaboration for content requirements]

## Critical Interaction Guidelines
[Workspace safety]

## Reflection Rules
[Content analysis]

## Workspace Organization Guidelines
[File management]

## Documentation Standards
[Basic content quality guidelines]

# Personality and Communication Style
[Professional, clear communication]
```

### Comprehensive Documentation Agent Structure

For large-scale, enterprise documentation projects:

```markdown
# Agent Identity and Core Purpose
[Custom agent identity, strategic documentation role]

## Human Pairing Protocol
[Stakeholder collaboration and requirements gathering]

## Critical Interaction Guidelines
[Workspace safety and path verification]

## Reflection Rules
[Comprehensive content and structure analysis]

## Workspace Organization Guidelines
[Enterprise documentation file management and collaboration]

## Critical Working Rules
[Rigorous documentation workflow requirements]

## Planning & Coordination
[Multi-phase documentation project management]

## Clone Delegation Framework
[Large-scale content development coordination]

## Context Management Strategies
[Complex documentation project context handling]

## Documentation Architecture Expertise
[Information architecture and documentation system design]

## Content Quality Standards
[Comprehensive quality frameworks and validation]

## Quality Gates Framework
[Multi-level content validation and stakeholder approval]

# Personality and Communication Style
[Strategic, professional, stakeholder-focused]

# Reference Materials
[Enterprise documentation standards, compliance guidelines]
```

## Customization Guidance

### Focus Area Adaptations

**Technical Documentation Agents**:
- Include appropriate Code Quality Standards component for technical domains
- Emphasize accuracy and technical precision
- Focus on developer-friendly organization
- Consider Development-Focused Human Pairing component

**User-Facing Documentation Agents**:
- Emphasize clarity and accessibility
- Focus on user journey and task orientation
- Include navigation and findability optimization
- Prioritize stakeholder communication protocols

**Strategic Documentation Agents**:
- Include Planning & Coordination component
- Emphasize document architecture and information design
- Focus on stakeholder alignment and business value
- Include Clone Delegation for large initiatives

**Content Quality Agents**:
- Include Quality Gates component
- Focus on editorial standards and professional polish
- Emphasize consistency and brand alignment
- Include validation and approval protocols

### Domain-Specific Considerations

**Add Custom Sections For**:
- Industry-specific documentation standards (regulatory, compliance)
- Specialized documentation methodologies (DITA, docs-as-code)
- Domain-specific style guides and terminology
- Client-specific documentation requirements
- Professional certification or compliance standards

**Adapt Components For**:
- **Documentation Expertise**: Customize for specific documentation domains (API docs, user guides, training materials)
- **Workspace Organization**: Adapt for documentation toolchains and publishing workflows
- **Quality Gates**: Tailor validation criteria for content type and audience
- **Planning & Coordination**: Adjust for documentation project complexity and stakeholder requirements

### Personality Customization

**Communication Style Options**:
- **Strategic Architect**: High-level, information design focused, stakeholder-oriented
- **Technical Writer**: Precise, detailed, accuracy-focused, developer-friendly
- **Content Curator**: Organized, systematic, consistency-focused, quality-oriented
- **Document Consultant**: Collaborative, advisory, best-practice focused, process-oriented

**Maintain Documentation Agent Characteristics**:
- Always quality and accuracy focused
- Clear, professional communication
- Systematic and methodical approaches
- Stakeholder-aligned and collaborative
- Detail-oriented with professional polish
- Client-ready output emphasis

## Real Examples from the Ecosystem

### Strategic Documentation Agent
**Agent**: `alexandra_strategic_document_architect.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Human Pairing Protocol (General Focus)
- ✅ Reflection Rules
- ✅ Workspace Organization
- ✅ Critical Working Rules
- ✅ Planning & Coordination
- ✅ Clone Delegation
- ✅ Quality Gates
- ✅ Documentation Expertise
- ❌ Code Quality Standards (content focus)
- ❌ Context Management (not explicitly included)
- ❌ Team Collaboration (independent work)

**Characteristics**: Strategic document planning, high-level content architecture, stakeholder-focused, comprehensive project coordination

---

### Documentation Preparation Specialist
**Agent**: `diana_doc_prep_specialist.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Human Pairing Protocol (General Focus)
- ✅ Reflection Rules
- ✅ Workspace Organization
- ✅ Critical Working Rules
- ✅ Planning & Coordination
- ✅ Clone Delegation
- ✅ Quality Gates
- ✅ Documentation Expertise
- ❌ Code Quality Standards (content focus)
- ✅ Context Management (large document handling)
- ❌ Team Collaboration (independent work)

**Characteristics**: Client-ready document preparation, professional polish focus, systematic content refinement, multi-format handling

---

### Documentation Refinement Specialist
**Agent**: `doc_documentation_refiner.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines
- ✅ Human Pairing Protocol (General Focus)
- ✅ Reflection Rules
- ✅ Workspace Organization
- ✅ Quality Gates
- ✅ Documentation Expertise
- ❌ Code Quality Standards (content focus)
- ❌ Planning & Coordination (refinement focus)
- ❌ Clone Delegation (focused scope)
- ❌ Context Management (smaller scope)
- ❌ Team Collaboration (independent work)

**Characteristics**: Content quality refinement, editorial excellence, consistency focus, professional polish

---

## Component Integration Benefits

### Why Binary Decisions Work for Documentation Agents

**For Documentation Agents Specifically**:
- **Clear Scope Definition**: Binary choices establish precise documentation capabilities
- **Quality Baseline**: Components ensure consistent documentation quality standards
- **Efficient Composition**: YES/NO decisions speed up documentation agent creation
- **Predictable Workflows**: Agents with similar components follow consistent documentation processes

**Quality Outcomes**:
- **Professional Output**: Component standards maintain client-ready quality
- **Systematic Approaches**: Components enforce methodical documentation workflows
- **Organized Content**: Workspace and planning components ensure structured documentation
- **Stakeholder Alignment**: Human pairing and quality gates maintain user focus

### Integration Patterns

**Essential Component Combinations**:
- Workspace Organization + Critical Interaction Guidelines = Safe documentation file operations
- Reflection Rules + Documentation Expertise = Thoughtful content creation
- Planning & Coordination + Clone Delegation = Scalable documentation projects
- Quality Gates + Documentation Expertise = Professional, validated output

**Core Integration Benefits**:
- **Safe Operations**: Critical Interaction Guidelines prevent documentation file errors
- **Quality Content**: Documentation Expertise + Quality Gates ensure professional output
- **Organized Projects**: Workspace Organization + Planning support large documentation efforts
- **Systematic Workflows**: Critical Working Rules + Reflection Rules improve documentation quality

## Getting Started

### Step-by-Step Documentation Agent Creation

1. **Define Documentation Scope**: Clearly identify the agent's documentation focus and content domain
2. **Make Binary Decisions**: Go through each component with clear YES/NO choices based on project scope
3. **Choose Code Variants**: Select appropriate Code Quality component only if generating technical code examples
4. **Structure the Persona**: Use the typical structure as a template and arrange selected components logically
5. **Add Documentation Expertise**: Include specific documentation methodologies, standards, and quality frameworks
6. **Customize for Domain**: Adapt components for documentation type (technical, user, strategic, etc.)
7. **Define Quality Standards**: Establish clear content quality criteria and validation protocols
8. **Set Collaboration Protocols**: Define stakeholder interaction and approval workflows
9. **Validate Composition**: Ensure component selections support the documentation mission
10. **Test with Sample Content**: Verify agent produces quality documentation output

### Quality Checklist

**Required for All Documentation Agents**:
- ✅ Includes 'domo' in category array
- ✅ Professional, detail-oriented communication style
- ✅ Clear documentation quality standards
- ✅ Appropriate component selection based on project scope

**Recommended Best Practices**:
- ✅ Safe workspace operations (Critical Interaction Guidelines - always include)
- ✅ Systematic content analysis (Reflection Rules - always include)
- ✅ Organized documentation management (Workspace Organization - always include)
- ✅ Quality validation protocols (Quality Gates for professional output)
- ✅ Methodical workflows (Critical Working Rules for complex projects)
- ✅ Project coordination (Planning & Coordination for large efforts)

**Documentation-Specific Quality Validation**:
- ✅ Component selections match documentation project scope
- ✅ Quality gates align with content validation requirements
- ✅ Documentation expertise covers necessary methodologies
- ✅ Workspace organization supports documentation workflows
- ✅ Stakeholder collaboration protocols clearly defined
- ✅ Content quality standards explicitly established

This binary component approach ensures that every Documentation agent provides consistent, professional, and high-quality content creation while maintaining the flexibility to specialize for specific documentation domains, project scales, and organizational requirements using the core components currently available.
