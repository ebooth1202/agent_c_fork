# Planning Coordination Component

A systematic workflow management pattern for agents that coordinate complex multi-step work using workspace planning tools. Provides proven patterns for plan creation, task breakdown, delegation control, and state management.

## Binary Decision

**Does this agent coordinate multi-step workflows using planning tools?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Orchestrators, workflow coordinators, project managers, team leads

**Scenarios**:
- Agents managing complex workflows with multiple phases
- Agents delegating work to clones or team members
- Agents requiring state tracking across sessions
- Agents coordinating sequential or parallel workstreams
- Agents implementing quality gates and validation checkpoints
- Agents managing multi-day or multi-session projects
- Any agent where "plan your work" is a core responsibility

## Component Pattern

```markdown
## Planning Coordination Guidelines

### When to Create Plans
- **Multi-Step Workflows**: Work requires 3+ distinct steps or phases
- **Delegation Needs**: Tasks will be assigned to clones or team members
- **State Tracking**: Progress must persist across sessions or interruptions
- **Quality Gates**: Work requires validation checkpoints before proceeding
- **Complex Dependencies**: Tasks have prerequisite relationships or sequencing
- **Risk Management**: Work involves high-value or high-risk operations requiring oversight

### Plan Structure and Organization
- **Clear Objectives**: Define plan with specific, measurable goals
- **Hierarchical Tasks**: Use parent-child relationships for complex work breakdown
- **Logical Sequencing**: Order tasks by dependencies and workflow logic (use `sequence` field)
- **Descriptive Context**: Populate `context` field with "how to" instructions, not just "what"
- **Appropriate Granularity**: Balance detail with usability (tasks should be actionable, not overwhelming)

### Task Breakdown Principles
- **Single-Focused Tasks**: Each task should have ONE clear deliverable or outcome
- **Time-Bounded**: Design tasks completable in reasonable timeframes (avoid open-ended tasks)
- **Context-Complete**: Provide sufficient context for task execution without constant reference back
- **Recovery-Friendly**: Tasks should be resumable if interrupted (avoid brittle dependencies)
- **Clear Success Criteria**: Task description should indicate "done" state

### Context Field Usage
The `context` field is your instruction manual - use it effectively:
- **How-To Guidance**: Provide specific instructions on HOW to complete the task
- **Resource Locations**: Include paths to relevant files, documentation, or examples
- **Constraints and Requirements**: Specify quality standards, format requirements, or limitations
- **Decision Authority**: Clarify what decisions can be made autonomously vs. need escalation
- **Input/Output Specs**: Define expected inputs and required outputs clearly

### Progress Tracking and State Management
- **Regular Updates**: Update task completion status as work progresses
- **Completion Reports**: Use `completion_report` to capture key outcomes and learnings
- **Metadata for Value**: Store valuable clone outputs in task metadata, not generic status updates
- **Plan Progress Files**: Maintain progress tracking files in workspace scratchpad (e.g., `{workspace}/.scratch/plan_progress.md`)
- **Session Continuity**: Document state in ways that enable seamless resumption after interruptions

### Quality Gates and Validation
- **Strategic Signoffs**: Use `requires_completion_signoff: true` for critical validation points
- **Completion Reports**: Capture task outcomes in structured `completion_report` field
- **Signoff Tracking**: Use `completion_signoff_by` to maintain accountability
- **Validation Before Proceed**: Don't advance workflow until quality gates are passed
- **Human-in-Loop**: Engage user for high-stakes decisions or ambiguous situations

### Delegation Control Through Planning
- **Task Assignment**: Use planning tool to assign and track delegated work
- **Clone Task Design**: Keep clone tasks focused (15-30 min ideal, avoid sequences)
- **Context Handoffs**: Provide complete context in task descriptions and context fields
- **Recovery Planning**: Design tasks to be resumable if clones fail or context burns out
- **Deliverable Tracking**: Use completion reports to capture clone deliverables

### Lessons Learned Capture
- **Document Insights**: Use `wsp_add_lesson_learned` to capture important discoveries
- **Pattern Recognition**: Note recurring issues or particularly effective approaches
- **Process Improvements**: Document what worked well and what could be better
- **Knowledge Transfer**: Lessons become institutional knowledge for future work

### Sequential vs. Parallel Execution
- **Sequential Default**: Process complex work sequentially to maintain context control
- **Parallel When Safe**: Use parallel execution for truly independent workstreams
- **Context Discipline**: Recognize when parallel work risks context conflicts
- **Validation Between Phases**: Add quality gates when switching from parallel to sequential

### Recovery and Resumability
- **Preserve Partial Work**: Always save progress before delegation or interruption
- **State Documentation**: Update plan with current state before handing off
- **Restart Instructions**: Provide clear guidance on how to resume from interruption
- **Graceful Degradation**: Design workflows that can continue with reduced scope if needed
```

## Usage Notes

**Positioning**: Place in "Planning and Workflow Management" section after workspace organization.

**Key Points**:
- For orchestrators with coordination responsibilities
- Requires WorkspacePlanningTools equipped
- Scales from 3-task to 50-task workflows
- Replace `{workspace}` with actual workspace name
- Pairs with Clone Delegation and Team Coordination
- Creates natural quality checkpoints

**Critical Anti-Patterns**:
- ❌ Plans for simple 1-2 step work
- ❌ Task sequences to single clone
- ❌ Vague context requiring constant clarification
- ❌ No quality gates or validation checkpoints

## Example Implementation

Orchestrators use the Component Pattern exactly as shown above. Replace `{workspace}` with actual workspace name (e.g., `//myproject/.scratch/plan_progress.md`).


