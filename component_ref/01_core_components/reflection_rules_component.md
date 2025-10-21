# Reflection Rules Component

A foundational thinking pattern that ensures agents systematically capture and process new information through structured reflection using the think tool.

## Binary Decision

**Does this agent have access to the ThinkTools?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: All agents equipped with ThinkTools (80% of agents)

**Scenarios**:
- Agents that read and analyze unfamiliar code
- Agents that process planning tool outputs
- Agents performing complex refactoring or enhancements
- Agents analyzing bugs and root causes
- Agents reading scratchpad content from other agents
- Agents evaluating solutions and impacts
- Any agent that needs to process and understand new information systematically

## Component Pattern

```markdown
# MUST FOLLOW: Reflection Rules
You MUST use the `think` tool to reflect on new information and record your thoughts in the following situations:
- Reading through unfamiliar code
- Reading plans from the planning tool
- Planning a complex refactoring or enhancement
- Analyzing potential bugs and their root causes
- After reading scratchpad content.
- When considering possible solutions to a problem
- When evaluating the impact of a proposed change
- When determining the root cause of an issue
- If you find yourself wanting to immediately fix something
```

## Usage Notes

**Positioning**: Place in dedicated "Reflection Rules" section early in persona, after core guidelines.

**Implementation Notes**:
- "MUST FOLLOW" and "MUST use" language ensures consistent application
- Comprehensive triggers cover all major reflection scenarios
- Universal pattern - no variations across ThinkTools agents
- Integrates thinking into natural workflow

**Integration Tips**:
- Works independently, no dependencies
- Essential for agents delegating work to clones
- Combines with planning components for complex workflows
- Valuable for technical agents analyzing code/systems

## Example Implementation

Use Component Pattern as-is for all ThinkTools-equipped agents.
