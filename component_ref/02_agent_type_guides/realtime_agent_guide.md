# Realtime Agent Guide

A guide for building voice-optimized agents that interact naturally through conversational interfaces, focusing on simplified components that support natural speech patterns and real-time interaction.

## When to Use Realtime Agent Type

**Core Characteristics**:
- Voice and conversational interface optimization
- Natural speech pattern support
- Real-time responsive interaction
- Simplified component structure (less complex than standard domo)
- Streamlined workflows for quick responses

**Typical Scenarios**:
- Voice-based user assistance and conversation
- Real-time problem-solving and quick consultations
- Conversational guidance and support
- Voice-driven information lookup and retrieval
- Spoken tutorial and educational support

**Key Requirements**:
- Must include both 'realtime' AND 'domo' in agent category array
- Must use simplified versions of all components (shorter, more conversational)
- Optimized for natural speech patterns and voice interaction

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision. **Critical**: All "YES" components should use SIMPLIFIED, voice-optimized versions.

### 1. Critical Interaction Guidelines → YES, Simplified (60% of realtime agents)
**Decision**: Does this agent access workspaces or file paths?
- **Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)
- **Why**: Prevents wasted work, but uses conversational language for voice.
- **Simplification**: "Verify paths first: If a user mentions a path, check it exists before working with it."

### 2. Reflection Rules → YES, Simplified (70% of realtime agents)
**Decision**: Does this agent have access to ThinkTools?
- **Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)
- **Why**: Ensures quality responses, but with simplified trigger list appropriate for real-time interaction.
- **Simplification**: Shorter trigger list focused on common voice scenarios (processing unfamiliar info, considering multiple solutions).

### 3. Workspace Organization → YES, Simplified (50% of workspace-enabled realtime agents)
**Decision**: Does this agent use workspace tools for file management?
- **Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)
- **Why**: Standardizes file management with simplified organization.
- **Simplification**: "Use designated workspace, use `.scratch` for temporary work, move old files to `.scratch/trash`."

### 4. Code Quality Standards → NO (Typical for realtime agents)
**Decision**: Does this agent write or modify code?
- **Why Skip**: Voice coding is rare use case. Nearly all realtime agents skip this.
- **If YES**: Use condensed version focused on core principles only (methods under 25 lines, use type hints).

### 5. Human Pairing → YES, Simplified (90% of realtime agents)
**Decision**: Does this agent collaborate with users in real-time?
- **Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)
- **Why**: Establishes collaborative expectations in conversational language.
- **Simplification**: "I'll handle: analysis, creating content, managing files. You'll handle: reviewing suggestions, final decisions, letting me know if something doesn't sound right."

### 6. Critical Working Rules → YES, Condensed (40% of realtime agents)
**Decision**: Does this agent do work requiring methodical planning and verification?
- **Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)
- **Why**: For realtime agents that need structure, in simpler conversational form.
- **Simplification**: "Take things one step at a time, think through complex questions, check in before major steps, quality over speed."

### 7. Planning & Coordination → NO (NOT RECOMMENDED for realtime)
**Decision**: Does this agent coordinate complex multi-step workflows?
- **Why Skip**: Complex planning hierarchies are too heavy for real-time voice interaction. Realtime agents focus on simpler, immediate tasks.

### 8. Clone Delegation → NO (NOT RECOMMENDED for realtime)
**Decision**: Does this agent delegate tasks to clone agents?
- **Why Skip**: Clone delegation adds complexity inappropriate for real-time conversational flow.

### 9. Context Management → NO (NOT RECOMMENDED for realtime)
**Decision**: Does this agent manage complex long-running conversations?
- **Why Skip**: Complex context management strategies are too heavyweight for real-time interaction.

### 10. Team Collaboration → NO (NOT RECOMMENDED for realtime)
**Decision**: Is this agent part of a multi-agent team?
- **Why Skip**: Team coordination protocols add unnecessary complexity for voice-optimized interaction.

### 11. Quality Gates → NO (NOT RECOMMENDED for realtime)
**Decision**: Does this agent need formal validation checkpoints?
- **Why Skip**: Formal quality gates slow down real-time interaction. Use conversational verification instead.

### 12. Domain Knowledge Template → YES, Simplified (for specialist realtime agents)
**Decision**: Is this agent a specialist with domain expertise?
- **Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)
- **Why**: For specialist realtime agents, but with simplified, conversational domain explanations.
- **Simplification**: Use 2-3 short sections with conversational language, focus on practical guidance over formal methodology.

## Component Modifications for Realtime

**Core Simplification Principles**:
- **Shorter**: 30-50% less text than standard domo versions
- **More Conversational**: Written as if speaking, not writing
- **Action-Oriented**: Focus on what to do, not extensive reasoning
- **Voice-Friendly**: Use natural speech patterns and phrasing
- **Streamlined**: Remove formal structure and complex hierarchies

**What to Remove for Realtime**:
- Complex planning hierarchies
- Formal task decomposition frameworks
- Clone delegation protocols
- Multi-agent coordination procedures
- Context management strategies
- Formal quality gate processes
- Extensive methodology descriptions
- Lengthy best practices lists

## Typical Structure and Composition

### Standard Realtime Agent Structure
```markdown
# [Agent Name] - [Role]
[2-3 sentence introduction in conversational tone]

## How We Work Together
[Simplified human pairing - what I do, what you do]

## Critical Guidelines
[Simplified path verification if workspace access]

## Workspace Basics
[Simplified file organization if workspace tools]

## Working Approach
[Condensed working rules if complex work]
[Brief reflection triggers if ThinkTools]

## [Domain] Expertise
[2-3 short sections if specialist, conversational language]

## Communication Style
[Warm, conversational, voice-optimized approach]
```

### Minimal Realtime Agent Structure
```markdown
# [Agent Name] - [Role]
[2-3 sentence introduction in conversational tone]

## How We Work Together
[Brief collaboration framework]

## Communication Style
[Warm, conversational approach]
```

### Specialist Realtime Agent Structure
```markdown
# [Agent Name] - [Domain Specialist]
[2-3 sentence introduction in conversational tone]

## How We Work Together
[Simplified human pairing]

## Critical Guidelines
[Simplified path verification if needed]

## Working Approach
[Brief working rules and thinking triggers]

## [Domain] Expertise
[2-3 conversational sections with practical guidance]

## Communication Style
[Professional but conversational, voice-optimized]
```

## Customization Guidance

**Focus Area Adaptations**:
- **General Purpose**: Minimal structure (identity + collaboration + style), warm helpful communication
- **Information Lookup**: Add simplified workspace organization, basic path verification, efficient retrieval
- **Specialist**: Include 2-3 simplified domain expertise sections, add condensed working approach

**Voice Optimization Techniques**:
- Use "I'll" and "you'll" instead of "Agent will" and "User will"
- Use "Let me" instead of "I will perform"
- Use "Check in with you" instead of "Require user validation"
- Short paragraphs (2-3 sentences maximum)
- Bullet points over long explanations
- Natural speech rhythm

**Personality Customization**:
- **Helpful Assistant**: Friendly, supportive, quick to help
- **Expert Consultant**: Professional, knowledgeable, conversational
- **Collaborative Partner**: Warm, encouraging, team-oriented
- **Problem Solver**: Focused, efficient, solution-driven

## Proper YAML Configuration Structure

**CRITICAL**: Realtime agent YAML files must include both 'realtime' and 'domo' in categories.

```yaml
version: 2
key: your_realtime_agent_key
name: "Your Realtime Agent Name"
model_id: "claude-3.5-sonnet"
agent_description: |
  Brief description emphasizing voice/conversational capabilities.
tools:
  - ThinkTools
  - WorkspaceTools
  # Minimal tool set - only what's essential
category:
  - "realtime"  # REQUIRED for realtime agents
  - "domo"      # REQUIRED - all realtime agents are domo agents
agent_params:
  type: "claude_reasoning"
  budget_tokens: 10000  # Lower for faster responses
  max_tokens: 32000
persona: |
  # MUST BE LAST
  # Use SIMPLIFIED, conversational versions of all components
```

**Critical Structure Rules**:
1. Field Order Matters: Fields must appear in exact order shown
2. Persona Must Be LAST: Always final field
3. Dual Category Requirement: Must include BOTH "realtime" AND "domo" categories
4. Simplified Persona Content: All components use simplified, conversational versions
5. Lower Token Budgets: Consider lower budgets for faster real-time responses

## Getting Started

**Step-by-Step Creation**:
1. Define Agent Purpose: Identify voice interaction focus and primary conversational role
2. Make Binary Decisions: Go through components with YES/NO choices, defaulting to NO for complex components
3. Simplify Selected Components: For each YES component, create simplified, conversational version
4. Create Proper YAML Structure: Use exact field order with both 'realtime' and 'domo' categories
5. Structure the Persona: Use typical realtime structure with simplified components only
6. Add Domain Expertise: If specialist, include 2-3 brief, conversational domain sections
7. Optimize for Voice: Ensure all language is natural speech, conversational tone
8. Test Conversational Flow: Read persona aloud to verify natural speech patterns

**Quality Checklist**:
- ✅ Includes both 'realtime' and 'domo' in category array
- ✅ Uses SIMPLIFIED versions of all components
- ✅ All language is conversational and voice-friendly
- ✅ Structure supports natural speech flow
- ✅ Warm, approachable communication style
- ✅ Brief, focused persona (shorter than standard domo)
- ✅ Simplified critical guidelines (if workspace access)
- ✅ Conversational human pairing framework
- ✅ Minimal formal structure and methodology
- ✅ Action-oriented, practical guidance
- ✅ All text reads naturally when spoken aloud
- ✅ No complex hierarchies or formal frameworks
- ✅ Short paragraphs and simple bullet points
- ✅ Conversational phrasing throughout ("I'll" vs "I will")
- ✅ Component selections match agent capabilities
- ✅ Domain expertise appropriately simplified (if specialist)
- ✅ Lower token budgets for faster responses
