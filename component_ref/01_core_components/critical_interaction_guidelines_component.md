# Critical Interaction Guidelines Component

A foundational safety pattern that prevents agents from wasting work on non-existent paths through immediate verification requirements.

## Binary Decision

**Does this agent access workspaces or file paths?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: All agents equipped with workspace tools (85% of agents)

**Scenarios**:
- Agents that read/write files
- Agents that navigate directory structures  
- Agents that perform workspace operations
- Multi-agent systems with file sharing
- Any agent that receives file/workspace paths from users

## Component Pattern

```markdown
## CRITICAL INTERACTION GUIDELINES
- **STOP IMMEDIATELY if workspaces/paths don't exist** If a user mentions a workspace or file path that doesn't exist, STOP immediately and inform them rather than continuing to search through multiple workspaces. This is your HIGHEST PRIORITY rule - do not continue with ANY action until you have verified paths exist.
- **PATH VERIFICATION**: VERIFY all paths exist before ANY operation. If a path doesn't exist, STOP and notify the user
- **No Silent Failures**: Never assume a path exists without verification. Always confirm access before proceeding with workspace operations.
```

## Usage Notes

**Positioning**: Place near top of agent persona, after agent identity but before core responsibilities.

**Implementation Notes**:
- "HIGHEST PRIORITY" language maintains binary decision nature
- "ANY action" prevents partial execution on invalid paths
- Universal pattern - no variations across workspace agents

**Integration Tips**:
- Works independently, no dependencies
- Combine with workspace organization for comprehensive file handling
- Essential for agents delegating file operations
- Pairs with reflection rules for complex path analysis

## Example Implementation

Use Component Pattern as-is for all workspace-accessing agents.
