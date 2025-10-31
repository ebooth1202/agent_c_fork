# User's Guide to Instruction Blocks

**Building Agents Through Composition**

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Block Structure and Organization](#block-structure-and-organization)
3. [Naming Conventions](#naming-conventions)
4. [Using Blocks in Agent Personas](#using-blocks-in-agent-personas)
5. [Workspace-Specific Customization](#workspace-specific-customization)
6. [Creating Effective Blocks](#creating-effective-blocks)
7. [Composition Strategies](#composition-strategies)
8. [Metadata Variables in Blocks](#metadata-variables-in-blocks)
9. [Common Patterns and Examples](#common-patterns-and-examples)
10. [Troubleshooting and Best Practices](#troubleshooting-and-best-practices)

---

## Core Concepts

### What Are Instruction Blocks?

**Instruction Blocks** are reusable markdown files containing instruction segments that can be referenced and embedded in agent personas and prompt sections using simple substitution variables.

They enable the **composition** of agent intelligence from proven, tested instruction patterns rather than writing everything from scratch.

### The Composition Philosophy

Traditional agent development follows a **writing** paradigm:
```
Agent = Write 3000 lines of instructions (2000 shared + 1000 unique)
```

Instruction Blocks enable a **composition** paradigm:
```
Agent = Reference 2000 lines of shared blocks + Write 1000 lines of unique expertise
```

### Key Benefits

| Benefit                     | Impact                                                  |
|-----------------------------|---------------------------------------------------------|
| **DRY Principles**          | Write instruction patterns once, use everywhere         |
| **Mass Updates**            | Update 1 block file → update all agents using it        |
| **Faster Development**      | 75-85% faster agent creation through composition        |
| **Consistent Quality**      | Shared patterns tested once, used everywhere            |
| **Workspace Customization** | Tailor agents per-workspace without forking             |
| **Clear Architecture**      | Separation between shared patterns and unique expertise |

---

## Block Structure and Organization

### Core Blocks Location

Core instruction blocks are stored in:
```
agent_c_config/blocks/
```

This is the primary location for shared instruction patterns used across all agents.

### Recommended Organization Structure

```
agent_c_config/blocks/
├── core/                          # Universal agent guidelines
│   ├── reflection_rules.md
│   ├── workspace_guidelines.md
│   └── error_handling.md
│
├── agent_c/                       # Framework-specific knowledge
│   ├── event_system.md
│   ├── id_ref.md
│   └── ts/
│       ├── core_types.md
│       ├── event_flow_pipeline.md
│       └── team_workspace.md
│
├── teams/                         # Team-specific patterns
│   ├── dev/
│   │   ├── dev_must_follow.md
│   │   ├── dev_dod.md            # Definition of Done
│   │   ├── procedures_dev.md
│   │   ├── team_communication_patterns_dev.md
│   │   └── qc_dev.md
│   │
│   └── test/
│       ├── test_must_follow.md
│       └── test_procedures.md
│
├── languages/                     # Language-specific standards
│   ├── ts/
│   │   └── dev_standards.md
│   ├── python/
│   │   └── dev_standards.md
│   └── csharp/
│       └── dev_standards.md
│
└── domains/                       # Domain-specific knowledge
    ├── audio/
    │   └── web_audio_patterns.md
    └── security/
        └── auth_patterns.md
```

### Design Principles for Organization

1. **Group by scope**: Core → Framework → Teams → Languages → Domains
2. **Name descriptively**: Filename should clearly indicate content
3. **Keep focused**: Each block should cover one coherent topic
4. **Think reusability**: Will multiple agents need this?
5. **Consider hierarchy**: Organize by increasing specificity

---

## Naming Conventions

### Block ID Generation

Block IDs are automatically generated from the file path using this formula:

```
File Path: agent_c_config/blocks/some/nested/path/filename.md
Block ID:  block_some_nested_path_filename
           └─┬─┘ └────────┬────────────────┘
           prefix      path elements
```

**Rules**:
1. Start with `block_` prefix (or `blocks_` - both work)
2. Remove `agent_c_config/blocks/` from the path
3. Replace path separators (`/`) with underscores (`_`)
4. Remove the `.md` extension
5. Result is all lowercase with underscores

### Examples

| File Path                              | Block ID                           |
|----------------------------------------|------------------------------------|
| `blocks/core/reflection_rules.md`      | `block_core_reflection_rules`      |
| `blocks/agent_c/event_system.md`       | `block_agent_c_event_system`       |
| `blocks/teams/dev/dev_must_follow.md`  | `block_teams_dev_dev_must_follow`  |
| `blocks/languages/ts/dev_standards.md` | `block_languages_ts_dev_standards` |

### File Naming Best Practices

✅ **DO**:
- Use descriptive names: `dev_must_follow.md`, `team_communication_patterns.md`
- Use snake_case for consistency with block IDs
- Group related blocks in subdirectories
- Keep names concise but meaningful

❌ **DON'T**:
- Use spaces in filenames (breaks block ID generation)
- Use special characters beyond underscore
- Make names too generic (`rules.md` - which rules?)
- Make names too long (harder to reference)

---

## Using Blocks in Agent Personas

### Basic Syntax

Reference blocks using substitution variables:

```yaml
persona: |
  You are MyAgent, a specialized assistant.
  
  ${block_core_reflection_rules}
  ${block_teams_dev_dev_must_follow}
  
  ## Your Unique Domain Expertise
  [Custom instructions here...]
```

### Substitution Variable Variants

Both forms work identically:
- `${block_...}` - Singular form
- `${blocks_...}` - Plural form

Choose whichever reads better in context.

### Block Resolution Order

When a block is referenced, the system looks for it in this order:

1. **Workspace blocks** (if active workspace is set): `[workspace]/.agentc/blocks/`
2. **Core blocks**: `agent_c_config/blocks/`

This allows workspace-specific blocks to **override** core blocks with the same name.

### Integration in YAML Configuration

Blocks can be used in any string field that supports metadata substitution:

```yaml
version: 2
name: "Development Specialist"
key: "dev_specialist"
model_id: "claude-sonnet-4"

persona: |
  You are Dev, a development specialist.
  
  ${block_teams_dev_dev_must_follow}
  ${block_languages_ts_dev_standards}
  
  ## Your Expertise
  You specialize in TypeScript development for the Agent C framework.

# Blocks can also be used in other fields:
agent_description: |
  ${block_standard_dev_description}
  Focuses on React components and hooks.
```

### Composition Order Matters

The order you reference blocks determines the structure of the final persona:

**Example: Typical Composition Order**
```yaml
persona: |
  # 1. Identity and Role
  You are AudioDev, the React Audio Specialist.
  
  # 2. Critical Must-Follow Rules (highest priority)
  ${block_teams_dev_dev_must_follow}
  
  # 3. Quality Standards and DoD
  ${block_teams_dev_dev_dod}
  ${block_teams_dev_qc_dev}
  
  # 4. Framework Knowledge
  ${block_agent_c_event_system}
  ${block_agent_c_ts_core_types}
  
  # 5. Language Standards
  ${block_languages_ts_dev_standards}
  
  # 6. Team Coordination
  ${block_teams_dev_team_communication_patterns_dev}
  ${block_teams_dev_procedures_dev}
  
  # 7. Workspace and Reference Material
  ${block_agent_c_ts_team_workspace}
  ${block_agent_c_ts_ref_material}
  
  # 8. Domain-Specific Expertise (unique to this agent)
  ## Audio Development Expertise
  [Your unique audio-specific knowledge...]
  
  ## Your Team Members
  [Specific team information...]
```

**Why This Order Works**:
1. **Critical rules first** - Ensures agents respect boundaries
2. **Standards next** - Quality gates and definitions
3. **Framework knowledge** - Shared technical foundation
4. **Coordination patterns** - How to work with others
5. **Domain expertise last** - Unique specialization builds on foundation

---

## Workspace-Specific Customization

### The Active Workspace System

Every chat session has an **active workspace** that determines which workspace-specific blocks (if any) are loaded.

#### Setting the Active Workspace

**Option 1: Default in Agent Config**
```yaml
# agent config YAML
prompt_metadata:
  default_workspace: "my_project"
```
This sets the default for new sessions with this agent.

**Option 2: During Session**
Use the workspace tool's `workspace_set_active` function:
```
Agent: I'll set the active workspace to 'my_project'
```

**Option 3: User Notification**
The user is notified when the active workspace changes:
```
Active workspace changed to: my_project
```

### Workspace Block Location

Workspace-specific blocks are stored in:
```
[workspace_root]/.agentc/blocks/
```

For example:
```
my_project/
├── .agentc/
│   └── blocks/
│       ├── teams/
│       │   └── dev/
│       │       └── dev_must_follow.md  # Overrides core version
│       └── project_specific/
│           └── architecture_rules.md   # New workspace-only block
├── src/
└── docs/
```

### Override Behavior

When the same block exists in both locations:
- **Workspace block** completely replaces the core block
- No merging occurs - it's an all-or-nothing override

**Example**:
```
Core:      agent_c_config/blocks/teams/dev/dev_must_follow.md
Workspace: my_project/.agentc/blocks/teams/dev/dev_must_follow.md

Result: The workspace version is used (core version is ignored)
```

### Workspace-Only Blocks

You can create blocks that only exist in a workspace:

```
my_project/.agentc/blocks/project/domain_rules.md
```

Reference it like any other block:
```yaml
persona: |
  ${block_project_domain_rules}
```

This block will:
- ✅ Work when `my_project` is the active workspace
- ⚠️ Become an empty string in other workspaces (graceful degradation)

### Use Cases for Workspace Customization

1. **Project-Specific Rules**: Add constraints specific to a project
2. **Client Requirements**: Customize agents for specific client needs
3. **Domain Expertise**: Add specialized knowledge for a particular domain
4. **Team Variations**: Adjust team communication patterns per project
5. **Testing Overrides**: Use different standards in test workspaces

---

## Creating Effective Blocks

### Block Design Principles

#### 1. Single Responsibility
Each block should cover **one coherent topic**:

✅ **Good**: `reflection_rules.md` - Just reflection guidelines
❌ **Bad**: `rules_and_processes.md` - Too broad

#### 2. Reusability Focus
Ask: "Will multiple agents need this?"

If yes → Create a block
If no → Keep it in the agent's unique persona section

#### 3. Self-Contained Context
Blocks should make sense independently:

✅ **Good**:
```markdown
## Reflection Rules
You MUST use the think tool to reflect on:
- Reading through unfamiliar code
- Planning complex refactoring
- Analyzing potential bugs
```

❌ **Bad**:
```markdown
## Rules
You must reflect on these situations:
[Lists situations without explaining reflection or the tool]
```

#### 4. Composability
Design blocks to work well with other blocks:

- Avoid duplicate headings that would conflict
- Use appropriate heading levels (## for main sections)
- Don't assume what comes before or after

### Block Content Guidelines

#### Structure
```markdown
## [Clear Section Title]

[Optional brief introduction to the topic]

### [Subsection if needed]

- **Specific guideline**: Explanation
- **Another guideline**: Explanation

[Optional examples or patterns]
```

#### Writing Style

**DO**:
- Be specific and actionable
- Use clear, directive language
- Include examples where helpful
- Format for scannability (bullets, bold, headings)

**DON'T**:
- Be vague or philosophical
- Use unnecessarily complex language
- Include unrelated topics
- Make it too long (split if needed)

### When to Create a New Block

Ask these questions:

| Question                        | Yes = Create Block | No = Keep in Persona |
|---------------------------------|--------------------|----------------------|
| Will 3+ agents need this?       | ✅                  | ❌                    |
| Is it a common pattern?         | ✅                  | ❌                    |
| Is it framework knowledge?      | ✅                  | ❌                    |
| Is it team coordination?        | ✅                  | ❌                    |
| Is it agent-specific expertise? | ❌                  | ✅                    |
| Is it unique to one agent?      | ❌                  | ✅                    |

### Block Maintenance

#### Version Control
- Keep blocks in version control with agent configs
- Document changes in commit messages
- Consider impact on all agents using the block

#### Evolution
- Start specific, generalize later
- If 3+ agents have similar sections, extract to a block
- Refactor blocks as patterns emerge

#### Testing
After creating or modifying a block:
1. Reload blocks: `!reload_blocks` command
2. Test with an agent that uses it
3. Verify substitution works correctly
4. Check for conflicts with other blocks

---

## Composition Strategies

### Strategy 1: Layered Composition

Build personas in layers from general to specific:

```yaml
persona: |
  You are [Agent Name], [Role].
  
  # Layer 1: Universal Guidelines
  ${block_core_reflection_rules}
  ${block_core_workspace_guidelines}
  
  # Layer 2: Role-Specific Patterns
  ${block_teams_dev_dev_must_follow}
  ${block_teams_dev_procedures}
  
  # Layer 3: Technical Standards
  ${block_languages_ts_dev_standards}
  ${block_agent_c_event_system}
  
  # Layer 4: Unique Domain Expertise
  ## Your Specialization
  [Custom content]
```

**Benefits**:
- Clear hierarchy of rules
- Easy to understand composition
- Predictable override behavior

### Strategy 2: Functional Composition

Group blocks by function rather than layer:

```yaml
persona: |
  You are [Agent Name], [Role].
  
  ## How You Work
  ${block_core_reflection_rules}
  ${block_teams_dev_procedures}
  
  ## Quality Standards
  ${block_teams_dev_dev_dod}
  ${block_teams_dev_qc_dev}
  
  ## Technical Knowledge
  ${block_agent_c_event_system}
  ${block_languages_ts_dev_standards}
  
  ## Your Expertise
  [Custom content]
```

**Benefits**:
- Organized by concern
- Easier to locate specific instruction types
- Better for complex agents with many blocks

### Strategy 3: Minimal Composition

Use only essential blocks, keep most instructions unique:

```yaml
persona: |
  You are [Agent Name], [Role].
  
  ${block_core_critical_rules}
  
  ## Your Complete Domain Expertise
  [Extensive custom instructions...]
```

**When to Use**:
- Agent has truly unique requirements
- Existing blocks don't fit well
- Experimenting with new patterns (extract to blocks later)

### Strategy 4: Team Template Composition

Create team-specific templates using blocks:

```yaml
# Template for all dev team specialists
persona: |
  You are [Agent Name], the [Specialization] Specialist.
  
  ${block_teams_dev_dev_must_follow}
  ${block_teams_dev_dev_dod}
  ${block_agent_c_event_system}
  ${block_agent_c_ts_core_types}
  ${block_languages_ts_dev_standards}
  ${block_teams_dev_team_communication_patterns_dev}
  ${block_teams_dev_procedures_dev}
  
  ## Your Specialization
  [Unique expertise for this specialist]
  
  ## Your Team
  [Team member information]
```

**Benefits**:
- Consistent structure across team members
- Easy to maintain team standards
- Quick to create new team members

### Choosing a Strategy

| Agent Type             | Recommended Strategy | Reason                   |
|------------------------|----------------------|--------------------------|
| **User-Facing (Domo)** | Layered              | Clear priority hierarchy |
| **Orchestrator**       | Functional           | Complex, many concerns   |
| **Specialist**         | Team Template        | Consistency across team  |
| **Experimental**       | Minimal              | Flexibility to evolve    |
| **Simple Task Agent**  | Minimal              | Not much shared          |

---

## Metadata Variables in Blocks

### What Are Metadata Variables?

Blocks can include **metadata variables** that are substituted with actual values when the block is loaded. This allows blocks to be personalized for each agent using them.

### Syntax

Metadata variables use the same syntax as block references:
```markdown
${variable_name}
```

### Common Metadata Variables

| Variable           | Description        | Example Value              |
|--------------------|--------------------|----------------------------|
| `$agent_name`      | Short agent name   | `"Bobb"`                   |
| `$agent_full_name` | Full agent name    | `"Bobb the Agent Builder"` |
| `$agent_key`       | Agent's unique key | `"bobb_agent_builder"`     |
| `$workspace`       | Current workspace  | `"my_project"`             |
| `$session_id`      | Current session ID | `"admin-libra-jaguar"`     |

### Example: Name Verification Block

```markdown
You are $agent_full_name communicating with users via the Agent C chat interface.

If the user addresses you by any name other than "$agent_name" you MUST respond:

:::warning
**Warning**: You have addressed me by the wrong name. My name is "$agent_name". 
Please make sure to select the correct agent from the dropdown menu.
:::
```

When loaded for an agent named "Audi":
```markdown
You are Audi, the React Audio Specialist communicating with users via the Agent C chat interface.

If the user addresses you by any name other than "Audi" you MUST respond:
[...]
```

### Creating Parameterized Blocks

Design blocks to use metadata variables where personalization is needed:

```markdown
## Your Identity

You are $agent_full_name, part of the $team_name team.

Your unique key is `$agent_key` for programmatic references.

## Workspace Context

You are currently working in the **$workspace** workspace.
```

### Benefits of Metadata Variables

✅ **Personalization**: Same block, customized per agent
✅ **Maintainability**: Update the pattern once, personalization happens automatically
✅ **DRY**: Don't repeat the pattern, just parameterize it

### Limitations

- Variables must be defined in the agent's `prompt_metadata` or session metadata
- Undefined variables are replaced with empty strings (graceful degradation)
- No conditional logic (use separate blocks for that)

---

## Common Patterns and Examples

### Pattern 1: Must-Follow Rules Block

**Use Case**: Critical rules every team member must follow

**Location**: `blocks/teams/dev/dev_must_follow.md`

```markdown
## MUST FOLLOW RULES

- **NEW DEPENDENCY INSTALLS REQUIRE USER ACTION**
  - The tools available to you do not allow YOU to install packages
  - If a new package is required, STOP and ask the user to install it
  - NEVER write code to work around the lack of a package

- **NO WORKAROUNDS**
  - If you encounter issues, report them rather than creating workarounds
  
- **NO GOLD PLATING**
  - Implement only what has been specifically requested

- **COMPLETE THE TASK**
  - Focus on the discrete task provided, then report completion
  
- **USE YOUR TEST PARTNER**
  - Use ateam_chat to coordinate with your test partner
```

**Usage**:
```yaml
persona: |
  You are DevAgent.
  ${block_teams_dev_dev_must_follow}
```

### Pattern 2: Framework Knowledge Block

**Use Case**: Share framework-specific knowledge across all agents working with that framework

**Location**: `blocks/agent_c/event_system.md`

```markdown
## Agent C Event System Architecture

The Agent C realtime API uses a structured event system built on a clear inheritance hierarchy:

### BaseEvent Structure
All events inherit from `BaseEvent` which provides the `type` field.

### Event Categories

**Control Events**: Inherit directly from `BaseEvent`
- Handle session management, configuration, and system operations
[More details...]

**Session Events**: Inherit from `SessionEvent`
- Handle chat interactions within active sessions
- Include session context fields: `session_id`, `role`, etc.
[More details...]
```

**Usage**:
```yaml
persona: |
  You are RealtimeAgent.
  ${block_agent_c_event_system}
  
  ## Your Specific Work
  You handle audio streaming events...
```

### Pattern 3: Team Communication Block

**Use Case**: Define how team members communicate and coordinate

**Location**: `blocks/teams/dev/team_communication_patterns_dev.md`

```markdown
## Team Communication Patterns

### Direct Communication via AgentTeamTools
Use `ateam_chat` for direct specialist-to-specialist communication:

**When to use direct communication**:
- Need specific expertise from another specialist
- Coordinating shared component changes
- Resolving technical conflicts

**When to escalate to coordinator**:
- Work assignment changes
- Resource conflicts
- Priority decisions

### Communication Protocol
1. **Be specific**: Clearly state what you need
2. **Provide context**: Share relevant information
3. **Respect boundaries**: Stay in your domain
4. **Track decisions**: Document agreements
```

**Usage**:
```yaml
persona: |
  You are TeamMember.
  ${block_teams_dev_team_communication_patterns_dev}
  
  ## Your Team Members
  - Partner: test_specialist (key: test_spec)
  - Peer: other_dev (key: other_dev_spec)
```

### Pattern 4: Nested Block Composition

**Use Case**: Create hierarchical block structures

**Parent Block**: `blocks/teams/dev/dev_complete.md`
```markdown
## Complete Development Guidelines

${block_teams_dev_dev_must_follow}
${block_teams_dev_dev_dod}
${block_teams_dev_procedures}
${block_languages_ts_dev_standards}

## Additional Dev Guidelines
[More content...]
```

**Usage**:
```yaml
persona: |
  You are DevAgent.
  ${block_teams_dev_dev_complete}
  
  # This expands to all nested blocks plus additional content
```

### Pattern 5: Workspace Override Example

**Core Block**: `agent_c_config/blocks/teams/dev/dev_standards.md`
```markdown
## Development Standards

- Code reviews required before merge
- Minimum 80% test coverage
- Follow TypeScript strict mode
```

**Workspace Override**: `special_project/.agentc/blocks/teams/dev/dev_standards.md`
```markdown
## Development Standards

- Code reviews required before merge
- Minimum 90% test coverage (higher for this project)
- Follow TypeScript strict mode
- Additional requirement: Security review for auth code
```

**Result**: When working in `special_project` workspace, agents use the project-specific standards.

### Pattern 6: Language-Specific Standards

**Use Case**: Share language best practices

**Location**: `blocks/languages/ts/dev_standards.md`

```markdown
## TypeScript Development Standards

### Code Quality
- Use TypeScript strict mode
- Prefer `interface` over `type` for object shapes
- Use explicit return types on functions
- Avoid `any`, prefer `unknown`

### Naming Conventions
- PascalCase for classes and interfaces
- camelCase for functions and variables
- UPPER_SNAKE_CASE for constants

### File Organization
- One class per file
- Co-locate tests with source
- Use barrel exports for public APIs
```

**Usage**:
```yaml
persona: |
  You are TypeScriptDev.
  ${block_languages_ts_dev_standards}
```

---

## Troubleshooting and Best Practices

### Common Issues

#### Issue 1: Block Not Found

**Symptom**: Block reference appears as empty string

**Causes**:
- Typo in block ID
- File doesn't exist at expected path
- Workspace not set correctly (for workspace blocks)

**Solution**:
```bash
# 1. Check the file exists
ls agent_c_config/blocks/path/to/file.md

# 2. Verify the block ID
# Path: blocks/teams/dev/rules.md
# ID should be: block_teams_dev_rules

# 3. Check for typos
${block_teams_dev_rules}  # Correct
${block_team_dev_rules}   # Wrong (missing 's')

# 4. Reload blocks
!reload_blocks
```

#### Issue 2: Metadata Variable Not Substituted

**Symptom**: `$variable_name` appears literally in persona

**Causes**:
- Variable not defined in `prompt_metadata`
- Typo in variable name
- Variable not available in context

**Solution**:
```yaml
# Add to agent config
prompt_metadata:
  agent_name: "MyAgent"
  team_name: "DevTeam"
```

#### Issue 3: Block Content Conflicts

**Symptom**: Duplicate headings, conflicting instructions

**Causes**:
- Multiple blocks with same headings
- Blocks that assume specific order

**Solution**:
- Use unique, descriptive headings in blocks
- Design blocks to be independent
- Review composition order

#### Issue 4: Circular Block References

**Symptom**: Block includes itself (directly or indirectly)

**Causes**:
- Block A includes Block B, Block B includes Block A

**Solution**:
- Review block dependencies
- Restructure to eliminate circular references
- Keep block hierarchies shallow

### Best Practices Summary

#### For Block Creation

✅ **DO**:
- Keep blocks focused on one topic
- Use descriptive filenames and paths
- Include clear headings and structure
- Test blocks with multiple agents
- Document block purpose in comments
- Use metadata variables for personalization
- Keep blocks self-contained

❌ **DON'T**:
- Make blocks too large (split if needed)
- Assume specific composition order
- Include agent-specific information
- Create circular dependencies
- Use spaces or special chars in filenames
- Forget to reload after changes

#### For Block Usage

✅ **DO**:
- Compose in logical order (general → specific)
- Use consistent composition strategies
- Document why blocks are included
- Test composition with !reload_blocks
- Review full expanded persona
- Consider workspace overrides

❌ **DON'T**:
- Over-compose (use blocks for everything)
- Include conflicting blocks
- Forget domain-specific content
- Assume blocks can't change

#### For Workspace Customization

✅ **DO**:
- Use workspace blocks for project-specific rules
- Document workspace overrides
- Keep workspace blocks in version control (with workspace)
- Test with both core and workspace blocks

❌ **DON'T**:
- Create workspace blocks for universal patterns
- Forget to set active workspace
- Assume workspace blocks exist everywhere

### Testing Your Compositions

#### 1. Manual Verification
```bash
# In Agent C chat interface:
!reload_blocks

# Then test the agent:
"Hi [AgentName], can you confirm you understand [rule from block]?"
```

#### 2. Check Expanded Persona
Review the agent's full persona after block substitution to ensure:
- All blocks loaded correctly
- No duplicate or conflicting content
- Logical flow of instructions
- Domain expertise is present

#### 3. Integration Testing
- Test agents with block changes
- Verify behavior matches expectations
- Check team coordination (if multi-agent)

### Performance Considerations

**Block Loading**:
- Blocks are loaded at startup and on `!reload_blocks`
- No performance impact during agent execution
- Substitution happens once when persona is loaded

**Best Practices**:
- Keep individual blocks under 500 lines
- Limit nesting depth to 3 levels
- Total of 10-15 block references per agent is reasonable

---

## Quick Reference

### Block ID Formula
```
Path: agent_c_config/blocks/some/nested/path/file.md
ID:   block_some_nested_path_file
```

### Reference Syntax
```yaml
persona: |
  ${block_path_to_block}
  ${blocks_path_to_block}  # Also works
```

### Workspace Block Location
```
[workspace]/.agentc/blocks/
```

### Commands
```bash
!reload_blocks  # Reload all blocks from disk
```

### Priority Order
1. Workspace blocks (override)
2. Core blocks

### Key Metadata Variables
- `$agent_name`
- `$agent_full_name`
- `$agent_key`
- `$workspace`

---

## Conclusion

Instruction Blocks transform agent development from a writing exercise into a composition exercise. By building a library of proven, reusable instruction patterns, you can:

- **Create agents faster**: Compose from existing blocks
- **Maintain consistency**: Shared patterns used everywhere
- **Update en masse**: Change one block, update all agents
- **Customize per-workspace**: Tailor proven agents to specific needs
- **Build on success**: Every good pattern becomes reusable

Start by exploring the existing blocks in `//project/agent_c_config/blocks/`, study how they're used in agents like `realtime_react_audio_dev`, and begin composing your next agent from proven building blocks.

**Happy composing! 🧩**

---

*For more information, see:*
- [Introducing Instruction Blocks](../.scratch/introducing_instruction_blocks.md) - Quick overview
- [Agent Configuration Documentation](agent_configuration_documentation.md) - Full config reference
- [Multi-Agent Coordination Design Bible](multi_agent_coordination_design_bible.md) - Team patterns
