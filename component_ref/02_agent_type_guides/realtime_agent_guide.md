# Realtime Agent Guide

A comprehensive guide for building voice-optimized agents that interact naturally through conversational interfaces, focusing on simplified components that support natural speech patterns and real-time interaction.

## When to Use Realtime Agent Type

**Primary Purpose**: Voice-optimized agents designed for natural, conversational real-time interaction with users

**Core Characteristics**:
- Voice and conversational interface optimization
- Natural speech pattern support
- Real-time responsive interaction
- Simplified component structure (less complex than standard domo)
- Streamlined workflows for quick responses
- Tuned for spoken conversation dynamics
- Must also include 'domo' category (all realtime agents are user-facing)
- Voice-specific behavioral guidelines

**Typical Scenarios**:
- Voice-based user assistance and conversation
- Real-time problem-solving and quick consultations
- Conversational guidance and support
- Voice-driven information lookup and retrieval
- Spoken tutorial and educational support
- Quick technical consultations via voice
- Real-time collaborative brainstorming

**Key Requirements**:
- Must include both 'realtime' AND 'domo' in agent category array
- Must use simplified versions of all components (shorter, more conversational)
- Optimized for natural speech patterns and voice interaction
- Streamlined decision-making for real-time responsiveness
- Professional yet conversational communication

**Key Differences from Standard Domo Agents**:
- **Simplified Components**: All instruction blocks are shorter and more conversational
- **Reduced Complexity**: Eliminate complex workflows like planning hierarchies and clone delegation
- **Voice Optimization**: Language tuned for spoken delivery and understanding
- **Faster Response Cycles**: Streamlined processes for real-time interaction
- **Natural Language Focus**: Less technical, more conversational phrasing

## Binary Component Decisions

For each component, make a clear **YES** or **NO** decision based on your realtime agent's specific needs. **Critical**: All "YES" components should use SIMPLIFIED, voice-optimized versions.

### 1. Critical Interaction Guidelines Component

**Does this agent access workspaces or file paths?**

- **YES** → Use SIMPLIFIED version *(Applies to 60% of realtime agents)*
- **NO** → Skip this component

**Reference**: [`critical_interaction_guidelines_component.md`](../01_core_components/critical_interaction_guidelines_component.md)

**Why Include**: Prevents wasted work on non-existent paths, but uses more conversational language for voice interaction.

**When to Skip**: Pure conversational agents without any file system access.

**Realtime Simplification**: Use shorter, more conversational version:
```markdown
## Critical Guidelines
- **Verify paths first**: If a user mentions a workspace or file path, check that it exists before doing any work with it. If it doesn't exist, let them know right away.
```

---

### 2. Reflection Rules Component

**Does this agent have access to the ThinkTools?**

- **YES** → Use SIMPLIFIED version with fewer triggers *(Applies to 70% of realtime agents)*
- **NO** → Skip this component

**Reference**: [`reflection_rules_component.md`](../01_core_components/reflection_rules_component.md)

**Why Include**: Ensures quality responses, but with simplified trigger list appropriate for real-time interaction.

**When to Skip**: Simple conversational agents or when thinking logs aren't beneficial for voice interaction.

**Realtime Simplification**: Use shorter trigger list focused on common voice scenarios:
```markdown
## When to Think
Use the `think` tool to reflect when:
- Processing unfamiliar information
- Considering multiple possible solutions
- Evaluating impacts of suggestions
- After reading files or data
```

---

### 3. Workspace Organization Component

**Does this agent use workspace tools for file and directory management?**

- **YES** → Use SIMPLIFIED version *(Applies to 50% of workspace-enabled realtime agents)*
- **NO** → Skip this component

**Reference**: [`workspace_organization_component.md`](../01_core_components/workspace_organization_component.md)

**Why Include**: Standardizes file management, but uses simplified organization for real-time contexts.

**When to Skip**: Agents without any file management capabilities.

**Realtime Simplification**: Use basic, conversational version:
```markdown
## Workspace Basics
- Use the designated workspace for all files
- Use `.scratch` folder for temporary work
- Use `workspace_mv` to move old files to `.scratch/trash`
```

---

### 4. Code Quality Standards Components

**Does this agent write or modify code?**

- **YES** → Use simplified language-appropriate variant *(RARE for realtime agents)*
- **NO** → Skip this component *(Typical for realtime agents)*

**References**: 
- [`code_quality_python_component.md`](../01_core_components/code_quality_python_component.md)
- [`code_quality_csharp_component.md`](../01_core_components/code_quality_csharp_component.md)
- [`code_quality_typescript_component.md`](../01_core_components/code_quality_typescript_component.md)

**Why Include**: Only if building a specialized realtime coding assistant.

**When to Skip**: Nearly all realtime agents (voice coding is rare use case).

**Realtime Simplification**: If needed, use condensed version focused on core principles only (methods under 25 lines, use type hints, test your code).

---

### 5. Human Pairing Component

**Does this agent collaborate with users in real-time?**

- **YES** → Use SIMPLIFIED conversational version *(Applies to 90% of realtime agents)*
- **NO** → Skip this component

**Reference**: [`human_pairing_general_component.md`](../01_core_components/human_pairing_general_component.md)

**Why Include**: Establishes collaborative expectations, but in conversational language suitable for voice.

**When to Skip**: Rare for realtime agents (most interact directly with users).

**Realtime Simplification**: Use streamlined, conversational version:
```markdown
## How We Work Together
**I'll handle:**
- Initial analysis and research
- Creating content and organizing information
- Managing files and tools

**You'll handle:**
- Reviewing my suggestions to make sure they fit your goals
- Final decisions and approvals
- Letting me know if something doesn't sound right
```

---

### 6. Critical Working Rules Component

**Does this agent do work that requires methodical planning and verification?**

- **YES** → Use CONDENSED conversational version *(Applies to 40% of realtime agents)*
- **NO** → Skip this component

**Reference**: [`critical_working_rules_component.md`](../01_core_components/critical_working_rules_component.md)

**Why Include**: For realtime agents that need structure, but in simpler, more conversational form.

**When to Skip**: Simple conversational or information lookup agents.

**Realtime Simplification**: Use brief, conversational version:
```markdown
## Working Approach
- Take things one step at a time
- Think through complex questions before answering
- Check in with you before completing major steps
- Quality over speed
```

---

### 7. Planning & Coordination Component

**Does this agent coordinate complex multi-step workflows?**

- **NO** → Skip this component *(NOT RECOMMENDED for realtime agents)*

**Reference**: [`planning_coordination_component.md`](../01_core_components/planning_coordination_component.md)

**Why Skip**: Complex planning hierarchies and formal coordination are too heavy for real-time voice interaction. Realtime agents should focus on simpler, immediate tasks.

**Alternative**: For realtime agents that need basic task tracking, use simplified note-taking in workspace instead of formal planning tools.

---

### 8. Clone Delegation Component

**Does this agent delegate tasks to clone agents?**

- **NO** → Skip this component *(NOT RECOMMENDED for realtime agents)*

**Reference**: [`clone_delegation_component.md`](../01_core_components/clone_delegation_component.md)

**Why Skip**: Clone delegation adds complexity inappropriate for real-time conversational flow. Realtime agents should handle tasks directly or suggest user delegate to non-realtime agents.

---

### 9. Context Management Component

**Does this agent manage complex long-running conversations?**

- **NO** → Skip this component *(NOT RECOMMENDED for realtime agents)*

**Reference**: [`context_management_component.md`](../01_core_components/context_management_component.md)

**Why Skip**: Complex context management strategies are too heavyweight for real-time interaction. Keep conversations focused and simple.

---

### 10. Team Collaboration Component

**Is this agent part of a multi-agent team?**

- **NO** → Skip this component *(NOT RECOMMENDED for realtime agents)*

**Reference**: [`team_collaboration_component.md`](../01_core_components/team_collaboration_component.md)

**Why Skip**: Team coordination protocols add unnecessary complexity for voice-optimized interaction. Realtime agents work best as individual assistants.

---

### 11. Quality Gates Component

**Does this agent need formal validation checkpoints?**

- **NO** → Skip this component *(NOT RECOMMENDED for realtime agents)*

**Reference**: [`quality_gates_component.md`](../01_core_components/quality_gates_component.md)

**Why Skip**: Formal quality gates and signoff protocols slow down real-time interaction. Use conversational verification instead.

---

### 12. Domain Knowledge Template Component

**Is this agent a specialist with domain expertise?**

- **YES** → Use SIMPLIFIED conversational version *(Applies to specialist realtime agents)*
- **NO** → Skip this component

**Reference**: [`domain_knowledge_template_component.md`](../01_core_components/domain_knowledge_template_component.md)

**Why Include**: For specialist realtime agents, but with simplified, more conversational domain explanations.

**When to Skip**: General-purpose conversational agents.

**Realtime Simplification**: Use shorter sections with conversational language, focus on practical guidance over formal methodology descriptions.

## Component Modifications for Realtime

### Core Simplification Principles

**All Realtime Components Should Be**:
- **Shorter**: 30-50% less text than standard domo versions
- **More Conversational**: Written as if speaking, not writing
- **Action-Oriented**: Focus on what to do, not extensive reasoning
- **Voice-Friendly**: Use natural speech patterns and phrasing
- **Streamlined**: Remove formal structure and complex hierarchies

### Specific Simplification Patterns

**Critical Interaction Guidelines** (Simplified):
```markdown
## Critical Guidelines
- **Verify paths first**: If a user mentions a workspace or file path, check that it exists before doing any work with it. If it doesn't exist, let them know right away.
```

**Reflection Rules** (Simplified):
```markdown
## When to Think
Use the `think` tool to reflect when:
- Processing unfamiliar information
- Considering multiple possible solutions
- Evaluating impacts of suggestions
- After reading files or data
```

**Workspace Organization** (Simplified):
```markdown
## Workspace Basics
- Use the designated workspace for all files
- Use `.scratch` folder for temporary work
- Use `workspace_mv` to move old files to `.scratch/trash`
```

**Human Pairing** (Simplified):
```markdown
## How We Work Together
**I'll handle:**
- Initial analysis and research
- Creating content and organizing information
- Managing files and tools

**You'll handle:**
- Reviewing my suggestions to make sure they fit your goals
- Final decisions and approvals
- Letting me know if something doesn't sound right
```

**Critical Working Rules** (Simplified):
```markdown
## Working Approach
- Take things one step at a time
- Think through complex questions before answering
- Check in with you before completing major steps
- Quality over speed
```

**Domain Knowledge** (Simplified):
- Use 2-3 short sections instead of 5-6 detailed ones
- Focus on practical "how-to" guidance
- Write in conversational, natural language
- Avoid formal methodology terminology
- Keep examples brief and voice-friendly

### What to Remove for Realtime

**Always Remove**:
- Complex planning hierarchies
- Formal task decomposition frameworks
- Clone delegation protocols
- Multi-agent coordination procedures
- Context management strategies
- Formal quality gate processes
- Extensive methodology descriptions
- Lengthy best practices lists

**Keep Simple**:
- Basic verification steps
- Essential thinking triggers
- Core file organization
- Simple collaboration patterns
- Brief domain guidance (if specialist)

## Typical Structure and Composition Order

Based on the binary component decisions above, here's the recommended persona organization for realtime agents:

### Component Ordering Principle

**Recommended Order (Foundation → Specialization → Personality)**:

1. **Core Identity** (Custom, brief introduction)
   - Who you are and what you do (2-3 sentences max)
   
2. **Simplified Core Guidelines** (If workspace access)
   - Critical Interaction Guidelines (simplified)
   - Workspace Basics (simplified, if applicable)

3. **Collaboration Framework** (Simplified human pairing)
   - How We Work Together (simplified version)
   
4. **Working Approach** (If complex work)
   - Critical Working Rules (condensed, conversational)
   - When to Think (simplified reflection rules)

5. **Domain Expertise** (If specialist, simplified)
   - 2-3 brief, conversational sections

6. **Personality** (Conversational, warm tone)
   - Communication style for voice interaction

This ordering ensures voice-friendly flow while maintaining essential safety and quality patterns.

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

For simple conversational agents:

```markdown
# [Agent Name] - [Role]
[2-3 sentence introduction in conversational tone]

## How We Work Together
[Brief collaboration framework]

## Communication Style
[Warm, conversational approach]
```

### Specialist Realtime Agent Structure

For domain-focused realtime agents:

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

### Focus Area Adaptations

**General Purpose Realtime Agents**:
- Minimal structure (identity + collaboration + style)
- Focus on warm, helpful communication
- Emphasize quick, accurate responses
- Skip most formal components

**Information Lookup Realtime Agents**:
- Add simplified workspace organization if file access
- Include basic path verification
- Focus on efficient information retrieval
- Keep domain knowledge brief and practical

**Specialist Realtime Agents**:
- Include 2-3 simplified domain expertise sections
- Add condensed working approach
- Include simplified reflection triggers
- Maintain conversational tone throughout

### Voice Optimization Techniques

**Language Choices**:
- Use "I'll" and "you'll" instead of "Agent will" and "User will"
- Use "Let me" instead of "I will perform"
- Use "Check in with you" instead of "Require user validation"
- Use "Think through" instead of "Perform analysis"
- Use conversational phrasing throughout

**Structure Choices**:
- Short paragraphs (2-3 sentences maximum)
- Bullet points over long explanations
- Action verbs and active voice
- Natural speech rhythm

**Avoid in Realtime Agents**:
- Formal section titles (use conversational ones)
- Long methodology descriptions
- Complex hierarchical structures
- Technical jargon unless domain-required
- Extensive lists and frameworks

### Domain-Specific Considerations

**Add Custom Sections For**:
- Specialized knowledge appropriate for voice conversation
- Quick reference guidelines for domain work
- Common scenarios and how to handle them
- Voice-friendly domain terminology

**Keep Domain Sections**:
- Short (3-5 bullet points per section)
- Conversational in tone
- Action-oriented (what to do)
- Practical over theoretical

### Personality Customization

**Communication Style Options**:
- **Helpful Assistant**: Friendly, supportive, quick to help
- **Expert Consultant**: Professional, knowledgeable, conversational
- **Collaborative Partner**: Warm, encouraging, team-oriented
- **Problem Solver**: Focused, efficient, solution-driven

**Maintain Realtime Characteristics**:
- Always conversational and natural
- Voice-optimized phrasing
- Warm and approachable
- Real-time responsive mindset
- Professional yet friendly boundaries

## Real Examples from the Ecosystem

### General Purpose Realtime Agent
**Agent**: `default_realtime.yaml`

**Component Selections**:
- ✅ Critical Interaction Guidelines (simplified)
- ✅ Human Pairing (simplified)
- ✅ Reflection Rules (simplified)
- ✅ Workspace Organization (simplified)
- ❌ Code Quality Standards
- ❌ Planning & Coordination
- ❌ Clone Delegation
- ❌ Context Management
- ❌ Team Collaboration
- ❌ Quality Gates

**Characteristics**: Balanced voice assistance, warm interaction style, streamlined workflows, natural speech patterns

---

## Component Integration Benefits

### Why Binary Decisions Work for Realtime

**For Realtime Agents Specifically**:
- **Voice-Optimized Clarity**: Simplified components maintain conversational flow
- **Real-Time Performance**: Reduced complexity enables faster responses
- **Natural Interaction**: Conversational components feel more human-like
- **User-Friendly**: Simpler patterns make voice interaction more intuitive

**Quality Outcomes**:
- **Consistent Voice Experience**: Simplified components create predictable, pleasant voice interactions
- **Professional Standards**: Even simplified components maintain quality baseline
- **Reduced Cognitive Load**: Shorter, simpler patterns easier for users to understand through voice
- **Responsive Interaction**: Streamlined components enable real-time conversation flow

### Integration Patterns

**Essential Component Combinations for Realtime**:
- Human Pairing (simplified) + Working Approach (condensed) = Clear collaboration
- Critical Guidelines (simplified) + Workspace Basics (simplified) = Safe file operations
- Reflection Rules (simplified) + Domain Expertise (simplified) = Quality specialist responses

**Core Integration Benefits**:
- **Safe Operations**: Simplified critical guidelines prevent errors without complexity
- **Quality Responses**: Brief reflection rules maintain thoughtfulness
- **Clear Collaboration**: Conversational pairing framework sets expectations
- **Natural Flow**: All simplified components support voice conversation dynamics

## Proper YAML Configuration Structure

**CRITICAL**: Realtime agent YAML files must follow the exact field order AND include both 'realtime' and 'domo' in categories.

### Required Field Order

```yaml
version: 2
key: your_realtime_agent_key
name: "Your Realtime Agent Name"
model_id: "claude-3.5-sonnet"  # or appropriate realtime-optimized model
agent_description: |
  Brief description emphasizing voice/conversational capabilities.
tools:
  - ThinkTools
  - WorkspaceTools
  # Minimal tool set - only what's essential for realtime
agent_params:
  type: "claude_reasoning"  # or appropriate for realtime
  budget_tokens: 10000  # Lower than standard domo for faster responses
  max_tokens: 32000
  # Consider temperature adjustments for more natural conversation
category:
  - "realtime"  # REQUIRED for realtime agents
  - "domo"      # REQUIRED - all realtime agents are domo agents
  # Additional categories as needed
persona: |
  # The persona content MUST be LAST
  # Use SIMPLIFIED, conversational versions of all components
```

### Critical Structure Rules for Realtime

1. **Field Order Matters**: Fields must appear in the exact order shown above
2. **Persona Must Be LAST**: The persona field must always be the final field
3. **Dual Category Requirement**: Must include BOTH "realtime" AND "domo" categories
4. **Simplified Persona Content**: All persona components should use simplified, conversational versions
5. **Lower Token Budgets**: Consider lower token budgets for faster real-time responses

### Common Structure Errors to Avoid

❌ **WRONG - Missing 'domo' category:**
```yaml
category:
  - "realtime"  # ← WRONG! Must include 'domo' as well
```

✅ **CORRECT - Both categories included:**
```yaml
category:
  - "realtime"
  - "domo"  # ← CORRECT! Both categories required
```

❌ **WRONG - Using full component versions:**
```yaml
persona: |
  # MUST FOLLOW: Reflection Rules
  You MUST use the `think` tool to reflect on new information and record your thoughts in the following situations:
  - Reading through unfamiliar code
  - Reading plans from the planning tool
  - Planning a complex refactoring or enhancement
  # ... [too complex for realtime]
```

✅ **CORRECT - Using simplified component:**
```yaml
persona: |
  ## When to Think
  Use the `think` tool to reflect when:
  - Processing unfamiliar information
  - Considering multiple possible solutions
  - Evaluating impacts of suggestions
  - After reading files or data
```

## Getting Started

### Step-by-Step Realtime Agent Creation

1. **Define Agent Purpose**: Clearly identify the agent's voice interaction focus and primary conversational role
2. **Make Binary Decisions**: Go through each component with clear YES/NO choices, defaulting to NO for complex components
3. **Simplify Selected Components**: For each YES component, create simplified, conversational version
4. **Create Proper YAML Structure**: Use exact field order with both 'realtime' and 'domo' categories
5. **Structure the Persona**: Use typical realtime structure with simplified components only
6. **Add Domain Expertise**: If specialist, include 2-3 brief, conversational domain sections
7. **Optimize for Voice**: Ensure all language is natural speech, conversational tone
8. **Test Conversational Flow**: Read persona aloud to verify natural speech patterns
9. **Validate YAML Structure**: Verify fields in correct order, both categories included, persona LAST
10. **Test Voice Interaction**: Validate agent responds naturally in real-time conversational context

### Quality Checklist

**Required for All Realtime Agents**:
- ✅ Includes both 'realtime' and 'domo' in category array
- ✅ Uses SIMPLIFIED versions of all components
- ✅ All language is conversational and voice-friendly
- ✅ Structure supports natural speech flow
- ✅ Warm, approachable communication style

**Recommended Best Practices**:
- ✅ Brief, focused persona (shorter than standard domo)
- ✅ Simplified critical guidelines (if workspace access)
- ✅ Conversational human pairing framework
- ✅ Minimal formal structure and methodology
- ✅ Action-oriented, practical guidance

**Voice Optimization Validation**:
- ✅ All text reads naturally when spoken aloud
- ✅ No complex hierarchies or formal frameworks
- ✅ Short paragraphs and simple bullet points
- ✅ Conversational phrasing throughout ("I'll" vs "I will")
- ✅ Natural speech rhythm and flow

**Quality Validation**:
- ✅ Component selections match agent capabilities
- ✅ All components properly simplified for voice
- ✅ No conflicting or overly complex instructions
- ✅ Clear, warm communication style defined
- ✅ Domain expertise appropriately simplified (if specialist)
- ✅ Lower token budgets for faster responses
- ✅ Both required categories present

This binary component approach ensures that every realtime agent provides a natural, conversational, and effective voice interaction experience while maintaining the simplicity and responsiveness required for real-time conversation.
