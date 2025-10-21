# Context Management Component

A comprehensive framework for orchestrators to manage context window limits proactively and recover gracefully from context burnout. Includes strategies for progressive summarization, checkpoint creation, and clone failure recovery.

## Binary Decision

**Does this agent coordinate complex workflows that might hit context limits?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Orchestrators, complex workflow coordinators, agents managing extensive clone delegation

**Scenarios**:
- Agents coordinating multi-phase projects over extended sessions
- Agents delegating numerous tasks to clones
- Agents managing workflows that accumulate significant context
- Agents that need recovery protocols when clones hit context limits
- Agents working on long-running initiatives requiring state preservation
- Any orchestrator where context window management is a known risk

**When NOT to Use**: 
- Simple domo agents with straightforward workflows
- Assist agents (they work in bounded contexts, don't orchestrate)
- Agents with minimal delegation or short-lived sessions
- Single-purpose utility agents

## Component Pattern

```markdown
## Context Management Strategies

### Proactive Context Window Management
- **Progressive Summarization**: Extract and compress key insights at each step
- **Metadata Preservation**: Store critical state in workspace metadata
- **Checkpoint Creation**: Regular progress snapshots for recovery
- **Context Window Monitoring**: Track usage and implement early warnings

### Context Burnout Recovery Protocols
**When Clone Context Burns Out**:
1. **Recognize the Failure Type**: Context burnout vs. tool failure vs. quality issue
2. **Preserve Partial Work**: Extract any completed deliverables from the attempt
3. **Update Planning Tool**: Mark task with partial completion status
4. **Decompose Remaining Work**: Break remaining work into smaller clone tasks
5. **Resume with Fresh Context**: Start new clone with focused, smaller scope

**Prime Agent Response to Context Burnout**:
- DO NOT retry the same large task
- DO extract partial results if available  
- DO decompose remaining work
- DO update planning tool with progress made
- DO NOT enter generic "tool failure" fallback mode

### Metadata Usage Discipline

#### ✅ Appropriate Metadata Usage
- Clone analysis results and key findings
- Decision rationale and architectural choices
- Integration points for agent handoffs
- Recovery state needed to resume after failures

#### ❌ Metadata Anti-Patterns  
- Generic task status updates ("Task 1 complete", "Working on Task 2")
- Detailed progress tracking that belongs in planning tools
- Redundant information already captured elsewhere
- Verbose status reports that clutter metadata space
```

## Usage Notes

**Positioning**: Place in a dedicated "Context Management" or "Context Window Discipline" section, typically after planning/coordination but before domain-specific workflows.

**Implementation Notes**:
- **Orchestrator-Specific**: Primarily for agents with heavy delegation responsibilities
- **Requires Planning Tools**: Recovery protocols depend on planning tool integration
- **Assumes Clone Usage**: Recovery protocols designed for clone delegation scenarios
- **Proactive + Reactive**: Includes both prevention strategies and recovery protocols
- **Metadata Guidance**: Clarifies appropriate vs. inappropriate metadata usage

**Integration Tips**:
- **Essential for Clone Delegation**: Context burnout is real risk with clone delegation
- **Complements Planning Component**: Recovery protocols update planning tool state
- **Pairs with Quality Gates**: Checkpoints create natural recovery points
- **Works with Workspace Organization**: Metadata and checkpoints use workspace effectively
- **Supports Long-Running Work**: Enables multi-session orchestration without context loss

**Customization Guidance**:
- Add domain-specific checkpoint criteria (e.g., "After each requirements phase")
- Customize metadata usage examples for specific workflow needs
- Adjust clone task sizing guidance based on typical task complexity
- Include project-specific recovery protocols if needed
- Specify workspace paths for checkpoint storage

**Anti-Patterns to Avoid**:
- ❌ Retrying same large task after clone context burnout (will fail again)
- ❌ Ignoring partial work from failed clone attempts
- ❌ Using metadata for generic status updates instead of valuable outputs
- ❌ Failing to decompose work after context burnout
- ❌ Treating all failures as "tool failures" without diagnosis

## Example Implementation

Standard orchestrator with context management:

```markdown
## Context Management Strategies

### Proactive Context Window Management
- **Progressive Summarization**: Extract and compress key insights at each step
- **Metadata Preservation**: Store critical state in workspace metadata
- **Checkpoint Creation**: Regular progress snapshots for recovery
- **Context Window Monitoring**: Track usage and implement early warnings

### Context Burnout Recovery Protocols
**When Clone Context Burns Out**:
1. **Recognize the Failure Type**: Context burnout vs. tool failure vs. quality issue
2. **Preserve Partial Work**: Extract any completed deliverables from the attempt
3. **Update Planning Tool**: Mark task with partial completion status
4. **Decompose Remaining Work**: Break remaining work into smaller clone tasks
5. **Resume with Fresh Context**: Start new clone with focused, smaller scope

**Prime Agent Response to Context Burnout**:
- DO NOT retry the same large task
- DO extract partial results if available  
- DO decompose remaining work
- DO update planning tool with progress made
- DO NOT enter generic "tool failure" fallback mode

### Metadata Usage Discipline

#### ✅ Appropriate Metadata Usage
- Clone analysis results and key findings
- Decision rationale and architectural choices
- Integration points for agent handoffs
- Recovery state needed to resume after failures

#### ❌ Metadata Anti-Patterns  
- Generic task status updates ("Task 1 complete", "Working on Task 2")
- Detailed progress tracking that belongs in planning tools
- Redundant information already captured elsewhere
- Verbose status reports that clutter metadata space
```

Domain-specific orchestrator (customized with checkpoints):

```markdown
## Context Management Strategies

### Proactive Context Window Management
- **Progressive Summarization**: Extract and compress key insights at each requirements phase
- **Metadata Preservation**: Store critical domain analysis state in //myproject/meta/domain_state
- **Checkpoint Creation**: Create checkpoints after requirements, design, and implementation phases
- **Context Window Monitoring**: Track usage and implement early warnings for large domain models

### Context Burnout Recovery Protocols
**When Clone Context Burns Out**:
1. **Recognize the Failure Type**: Context burnout vs. tool failure vs. quality issue
2. **Preserve Partial Work**: Extract any completed domain analysis or code from the attempt
3. **Update Planning Tool**: Mark task with partial completion status
4. **Decompose Remaining Work**: Break remaining domain work into smaller focused clone tasks
5. **Resume with Fresh Context**: Start new clone with specific domain area focus

**Prime Agent Response to Context Burnout**:
- DO NOT retry the same large domain analysis task
- DO extract partial domain model results if available  
- DO decompose remaining domain areas
- DO update planning tool with domain areas completed
- DO NOT enter generic "tool failure" fallback mode

### Metadata Usage Discipline

#### ✅ Appropriate Metadata Usage
- Clone domain analysis results and key domain concepts
- Architectural decision rationale and trade-offs
- Integration points between domain boundaries
- Recovery state for resuming domain modeling

#### ❌ Metadata Anti-Patterns  
- Generic task status updates ("Domain analysis in progress")
- Detailed progress tracking that belongs in planning tools
- Redundant domain information already in documentation
- Verbose status reports that clutter metadata space
```

## Component Benefits

- **Proactive Prevention**: Strategies to avoid context burnout before it happens
- **Graceful Recovery**: Clear protocols for when context limits are hit
- **Preserves Work**: Ensures partial progress isn't lost during failures
- **Intelligent Decomposition**: Framework for breaking down work after burnout
- **Metadata Discipline**: Prevents metadata clutter while preserving valuable state
- **Resumability**: Enables orchestration to continue across failures
- **Failure Diagnosis**: Helps distinguish context issues from other failure types
- **Planning Integration**: Recovery protocols update planning state appropriately
- **Clone Optimization**: Guides effective clone task sizing to prevent burnout
- **Binary Decision**: Clear YES for complex orchestrators, NO for simple agents
