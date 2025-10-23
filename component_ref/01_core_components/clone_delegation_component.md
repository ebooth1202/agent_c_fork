# Clone Delegation Component

A systematic delegation pattern for agents that delegate work to clones effectively. Provides proven patterns for task design, context management, recovery protocols, and avoiding common pitfalls that lead to clone failures.

## Binary Decision

**Does this agent delegate tasks to clones?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Orchestrators, team leads, workflow coordinators, project managers

**Scenarios**:
- Agents managing complex workflows requiring distributed execution
- Agents that need to parallelize work across multiple sessions
- Agents coordinating development work through clones
- Agents with workloads exceeding single-session context capacity
- Agents implementing quality control through clone review cycles
- Any agent where "delegate to clones" is a core capability

## Component Pattern

```markdown
## Clone Delegation Guidelines

### When to Delegate to Clones
- **Context Management**: Your context window is approaching capacity
- **Parallel Execution**: Independent tasks can be executed simultaneously
- **Specialized Execution**: Task requires focused, uninterrupted attention
- **Time-Bounded Work**: Task has clear start/end and fits 15-30 minute window
- **Repeatable Patterns**: Similar tasks benefit from consistent clone execution
- **Fresh Context**: Task benefits from starting with clean context slate

### Clone Task Design Principles (CRITICAL)

#### The Golden Rule: Single-Focused Tasks
**✅ CORRECT**: "Analyze the UserService class and document its public API"  
**❌ WRONG**: "Analyze UserService, identify issues, document API, and create test plan"

**Why**: Task sequences cause context burnout and unclear stopping points.

#### Task Characteristics
- **One Clear Deliverable**: Task produces ONE specific output or outcome
- **Time-Bounded**: Completable in 15-30 minutes (context burnout prevention)
- **Self-Contained**: All context needed is provided in task description or references
- **Clear Success Criteria**: Clone knows unambiguously when task is "done"
- **Resumable Design**: If interrupted, task can be picked up without full restart

#### Context Window Discipline
- **Context Burnout Prevention**: Keep clone tasks small and focused
- **Single Deliverable Focus**: Avoid multi-phase work in single clone session
- **Proactive Management**: Don't wait for context failures to adjust approach
- **Fresh Start Advantage**: New clones have full context capacity for focused work

### Task Sequences: The Fatal Anti-Pattern

**❌ NEVER DO THIS**:
```
"Complete these steps:
1. Analyze the codebase
2. Identify integration points
3. Document findings
4. Create summary report"
```

**✅ INSTEAD DO THIS**:
- **Task 1**: "Analyze codebase and extract key integration points"
- **Task 2**: "Review integration points document and create technical documentation"
- **Task 3**: "Create stakeholder summary from technical documentation"

**Why This Matters**:
- Task sequences lead to context burnout (clone runs out of capacity mid-sequence)
- Unclear stopping points cause confusion about "done" state
- Recovery is complicated (which step failed? where to resume?)
- Single-focused tasks are more reliable and easier to validate

### Process Context and Handoffs
- **Clear Instructions**: Provide specific "how to" guidance with resource references and quality standards
- **Decision Authority**: Define what clone can decide vs. needs to escalate
- **Workspace Handoffs**: Create handoff documents in `{workspace}/.scratch/` with descriptive names
- **State Capture**: Document current state, completed work, and context for continuity

### Session Management
- **Start New Sessions**: When task complete, context reset needed, or parallel work required
- **Continue Existing**: For iterative refinement or when clone has relevant context
- **Track Session IDs**: Link to planning tool tasks for continuity and recovery support

### Recovery and Resumability

**When Clones Fail or Context Burns Out**:
1. **Recognize Failure Type**: Context exhaustion, tool failure, or quality issue?
2. **Preserve Partial Work**: Save any useful outputs before abandoning
3. **Update Planning State**: Mark progress in planning tools
4. **Decompose Remaining Work**: Break remaining work into smaller tasks
5. **Resume with Fresh Context**: Start new clone with adjusted task scope

### Metadata Capture (Not Status Tracking)

**✅ DO CAPTURE**: Key findings, important decisions, deliverable links, technical insights, blockers

**❌ DON'T CAPTURE**: Generic status updates, information already in files, redundant summaries

**Completion Reports**: Focus on outcomes accomplished, deliverable references, key decisions, and escalations

### Clone vs Specialist Delegation
- **Clones**: Temporary sessions for time-bounded focused tasks; provide full context each time
- **Specialists**: Persistent agents with domain expertise via AgentTeamTools; use for complex specialized work

### Delegation Control Through Planning
- **Task Assignment**: Create tasks in planning tool with clone instructions in `context` field
- **Progress Tracking**: Update task status and capture outcomes in completion reports
- **Quality Gates**: Use `requires_completion_signoff` for critical deliverables
- **State Management**: Planning tool is source of truth for all delegated work and recovery


```

## Usage Notes

**Positioning**: Place in "Clone Delegation" section after planning coordination.

**Key Points**:
- For orchestrators delegating to clones (requires act_chat/act_oneshot)
- Pairs with Planning Coordination component
- Context discipline CRITICAL - violations cause systematic failures
- Replace `{workspace}` with actual workspace name

**Critical Anti-Patterns**:
- ❌ Task sequences ("do steps 1, 2, 3...") - MOST COMMON FAILURE
- ❌ Open-ended exploration without deliverable
- ❌ Assuming clones remember previous sessions

**Success Factors**: Single-focused tasks, 15-30 min time-bounded, complete context, resumable design

## Example Implementation

Orchestrators use the Component Pattern exactly as shown above. Customize workspace paths (e.g., `//myproject/.scratch/`) as needed.


