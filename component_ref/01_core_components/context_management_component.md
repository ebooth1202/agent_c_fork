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

**Positioning**: Place in dedicated "Context Management" section after planning/coordination, before domain workflows.

**Key Points**:
- **Orchestrator-Specific**: For agents with heavy clone delegation
- **Proactive + Reactive**: Prevention strategies and recovery protocols
- **Requires Planning Tools**: Recovery updates planning tool state
- **Metadata Discipline**: Clarifies appropriate vs. inappropriate metadata usage

**Customization**:
- Add domain-specific checkpoint criteria
- Customize metadata examples for workflow needs
- Specify workspace paths for checkpoint storage

**Anti-Patterns**:
- ❌ Retrying same large task after clone context burnout
- ❌ Ignoring partial work from failed clones
- ❌ Using metadata for generic status updates
- ❌ Treating all failures as generic "tool failures"

## Example Implementation

See Component Pattern section above - use exactly as shown for most orchestrators. For domain-specific work, customize checkpoint criteria and metadata examples (e.g., "after requirements phase", "domain analysis state in //project/meta/domain_state").


