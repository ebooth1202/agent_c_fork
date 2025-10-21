# Documentation Agent Guide

A guide for building agents that focus on content creation, organization, and client-ready preparation within the Agent C framework.

## When to Use Documentation Agent Type

**Core Characteristics**:
- Content quality and professional polish focus
- Systematic organization and structure expertise
- Client-ready preparation protocols
- Navigation and usability optimization
- Stakeholder communication standards

**Typical Scenarios**:
- Technical documentation creation and maintenance
- Content organization and information architecture
- Document preparation for client delivery
- Knowledge base development and curation
- Reference material compilation and structuring

**Key Requirements**:
- Must include 'domo' in agent category array
- Should include appropriate core components based on scope
- Optimized for content quality and organization

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your documentation agent's specific needs:

### 1. Critical Interaction Guidelines → YES (100% of documentation agents)
**Decision**: Does this documentation agent access workspaces or file paths?
- **Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)
- **Why**: Documentation agents always work with files and workspaces. Prevents wasted work on non-existent paths.

### 2. Reflection Rules → YES (100% of documentation agents)
**Decision**: Does this documentation agent have access to ThinkTools?
- **Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)
- **Why**: Documentation requires careful analysis of content, structure, and organization. Ensures comprehensive coverage and quality.

### 3. Workspace Organization → YES (100% of documentation agents)
**Decision**: Does this documentation agent use workspace tools for file management?
- **Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)
- **Why**: Essential for maintaining organized file structures, managing document versions, and supporting collaborative workflows.

### 4A/B/C. Code Quality Standards → YES, if generating code
**Decision**: Does this documentation agent write or modify Python/C#/TypeScript code?
- **Reference**: [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md), [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md), [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)
- **Why**: For documentation agents that generate code examples, documentation tooling, or automation scripts.

### 5. Planning & Coordination → YES (75% of documentation agents)
**Decision**: Does this documentation agent coordinate large documentation projects or multi-phase content development?
- **Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)
- **Why**: Large documentation efforts require systematic planning, progress tracking, and coordination across multiple content pieces.

### 6. Clone Delegation → YES (60% of documentation agents)
**Decision**: Does this documentation agent delegate content creation tasks to clones for large projects?
- **Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)
- **Why**: Large documentation projects benefit from delegating specific content sections while maintaining overall quality and consistency.

### 7. Human Pairing (General Focus) → YES (100% of domo documentation agents)
**Decision**: Does this documentation agent interact directly with users for content collaboration?
- **Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)
- **Why**: Documentation agents work closely with users to understand content requirements, gather domain knowledge, and ensure stakeholder alignment.

### 8. Human Pairing (Development Focus) → YES, if technical development docs
**Decision**: Does this documentation agent focus specifically on technical software development documentation?
- **Reference**: [`human_pairing_development_component.md`](../01_core_components/human_pairing_development_component.md)
- **Why**: For documentation agents creating API documentation, code documentation, or technical development guides requiring close collaboration with developers.

### 9. Critical Working Rules → YES (90% of documentation agents)
**Decision**: Does this documentation agent perform complex, multi-step documentation work?
- **Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)
- **Why**: Documentation quality depends on methodical approaches, thorough analysis, and systematic content development.

### 10. Context Management → YES (50% of documentation agents)
**Decision**: Does this documentation agent manage large, complex documentation projects that might approach context limits?
- **Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)
- **Why**: Large documentation projects with extensive content, multiple references, and complex organization can approach context limits.

### 11. Team Collaboration → YES (20% of documentation agents)
**Decision**: Is this documentation agent part of a multi-agent documentation team with direct communication?
- **Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)
- **Why**: For documentation agents working in specialized teams with role-specific responsibilities (e.g., technical writer, editor, formatter).

### 12. Quality Gates → YES (85% of documentation agents)
**Decision**: Does this documentation agent require formal content quality validation and approval checkpoints?
- **Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)
- **Why**: Documentation quality requires systematic validation of content accuracy, completeness, formatting, and stakeholder alignment.

### 13. Domain Knowledge Template → YES (100% of specialized documentation agents)
**Decision**: Does this documentation agent specialize in specific documentation domains or methodologies?
- **Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)
- **Why**: Documentation agents benefit from structured domain expertise covering documentation methodologies, content standards, organization principles, and quality frameworks.

## Typical Structure and Composition

### Standard Documentation Agent Structure
```markdown
# Agent Identity and Core Purpose
## Human Pairing Protocol
## Critical Interaction Guidelines
## Reflection Rules
## Workspace Organization Guidelines
## Critical Working Rules
## Planning & Coordination (if large projects)
## Clone Delegation Framework (if large content projects)
## Context Management Strategies (if complex projects)
## Documentation Expertise
## Quality Gates Framework
# Personality and Communication Style
# Reference Materials
```

### Minimal Documentation Agent Structure
```markdown
# Agent Identity and Core Purpose
## Human Pairing Protocol
## Critical Interaction Guidelines
## Reflection Rules
## Workspace Organization Guidelines
## Documentation Standards
# Personality and Communication Style
```

### Comprehensive Documentation Agent Structure
```markdown
# Agent Identity and Core Purpose
## Human Pairing Protocol
## Critical Interaction Guidelines
## Reflection Rules
## Workspace Organization Guidelines
## Critical Working Rules
## Planning & Coordination
## Clone Delegation Framework
## Context Management Strategies
## Documentation Architecture Expertise
## Content Quality Standards
## Quality Gates Framework
# Personality and Communication Style
# Reference Materials
```

## Customization Guidance

**Focus Area Adaptations**:
- **Technical Documentation**: Include Code Quality Standards, emphasize accuracy and technical precision, consider Development-Focused Human Pairing
- **User-Facing Documentation**: Emphasize clarity and accessibility, focus on user journey and task orientation
- **Strategic Documentation**: Include Planning & Coordination, emphasize document architecture and information design
- **Content Quality**: Include Quality Gates, focus on editorial standards and professional polish

**Domain-Specific Considerations**:
- Industry-specific documentation standards (regulatory, compliance)
- Specialized documentation methodologies (DITA, docs-as-code)
- Domain-specific style guides and terminology
- Client-specific documentation requirements
- Professional certification or compliance standards

**Personality Customization**:
- **Strategic Architect**: High-level, information design focused, stakeholder-oriented
- **Technical Writer**: Precise, detailed, accuracy-focused, developer-friendly
- **Content Curator**: Organized, systematic, consistency-focused, quality-oriented
- **Document Consultant**: Collaborative, advisory, best-practice focused

## Proper YAML Configuration Structure

```yaml
version: 2
key: your_documentation_agent_key
name: "Your Documentation Agent Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description of documentation focus and capabilities.
tools:
  - ThinkTools
  - WorkspaceTools
  - WorkspacePlanningTools  # If large documentation projects
  - AgentTeamTools  # If part of team
category:
  - "domo"  # REQUIRED for documentation agents
  - "documentation"
  - "your_domain"  # Technical, strategic, etc.
  - "orchestrator_key"  # If part of a team
agent_params:
  type: "claude_reasoning"
  budget_tokens: 20000
  max_tokens: 64000
persona: |
  # MUST BE LAST
```

**Critical Structure Rules**:
1. Field Order Matters: Fields must appear in exact order shown
2. Persona Must Be LAST: Always final field in YAML file
3. Required Fields: All fields shown above required
4. Category Array: Must include "domo"

## Getting Started

**Step-by-Step Creation**:
1. Define Documentation Scope: Identify agent's documentation focus and content domain
2. Make Binary Decisions: Go through each component with clear YES/NO choices based on project scope
3. Choose Code Variants: Select appropriate Code Quality component only if generating technical code examples
4. Structure the Persona: Use typical structure as template and arrange selected components logically
5. Add Documentation Expertise: Include specific documentation methodologies, standards, and quality frameworks
6. Customize for Domain: Adapt components for documentation type (technical, user, strategic)
7. Define Quality Standards: Establish clear content quality criteria and validation protocols
8. Set Collaboration Protocols: Define stakeholder interaction and approval workflows

**Quality Checklist**:
- ✅ Includes 'domo' in category array
- ✅ Professional, detail-oriented communication style
- ✅ Clear documentation quality standards
- ✅ Appropriate component selection based on project scope
- ✅ Safe workspace operations (Critical Interaction Guidelines)
- ✅ Systematic content analysis (Reflection Rules)
- ✅ Organized documentation management (Workspace Organization)
- ✅ Quality validation protocols (Quality Gates for professional output)
- ✅ Methodical workflows (Critical Working Rules for complex projects)
- ✅ Project coordination (Planning & Coordination for large efforts)
- ✅ Component selections match documentation project scope
- ✅ Quality gates align with content validation requirements
- ✅ Documentation expertise covers necessary methodologies
- ✅ Workspace organization supports documentation workflows
- ✅ Stakeholder collaboration protocols clearly defined
