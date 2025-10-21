# Quality Gates Component

A validation framework that establishes formal checkpoints and completion signoff protocols for ensuring deliverable quality throughout complex workflows. Integrates with planning tools to enforce quality standards.

## Binary Decision

**Does this agent need formal validation checkpoints and completion signoff?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Quality-focused agents, orchestrators, specialists with formal deliverables, agents managing critical workflows

**Scenarios**:
- Agents producing deliverables requiring validation before proceeding
- Agents coordinating workflows with quality checkpoints
- Agents delegating work requiring completion verification
- Agents managing high-stakes or high-value operations
- Agents where deliverable quality must be formally tracked
- Specialists producing outputs requiring signoff (architecture, testing, etc.)

**When NOT to Use**: 
- Simple utility agents without formal deliverables
- Agents doing exploratory or draft work without validation requirements
- Quick-turnaround agents where formal gates would add unnecessary overhead

## Component Pattern

```markdown
## Quality Gates and Validation Framework

### Output Validation Protocol
- **Immediate Validation**: Validate each deliverable upon completion
- **Completeness Check**: Ensure all required elements are present
- **Quality Assessment**: Verify output meets standards and requirements
- **Integration Readiness**: Confirm output can be used by subsequent steps

### Completion Signoff Protocols
- Use `requires_completion_signoff: true` for critical validation points
- Use `requires_completion_signoff: false` for routine tasks  
- Use `requires_completion_signoff: "human_required"` for human review needs
- Document completion with `completion_report` for key deliverables
- Track accountability with `completion_signoff_by` field

### Quality Validation Criteria
- Deliverables meet defined acceptance criteria
- All required components and sections are present
- Outputs follow established standards and conventions
- Work is complete and ready for next phase or stakeholder use
- Dependencies for downstream work are satisfied
```

## Usage Notes

**Positioning**: Place in a dedicated "Quality Gates" or "Quality Assurance Framework" section, typically after planning/coordination but before domain-specific workflows.

**Implementation Notes**:
- **Requires Planning Tools**: Signoff features are part of WorkspacePlanningTools
- **Three Signoff Levels**: true (agent/team signoff), false (no signoff), "human_required" (human must validate)
- **Completion Reports**: Structured way to capture key outcomes and learnings
- **Accountability Tracking**: `completion_signoff_by` field records who validated
- **Integration with Planning**: Quality gates are implemented as planning tool task properties

**Integration Tips**:
- **Essential for Orchestrators**: Quality gates enable validation before proceeding
- **Pairs with Clone Delegation**: Validate clone outputs before advancing workflow
- **Complements Context Management**: Checkpoints are natural quality gate locations
- **Works with Team Collaboration**: Signoffs support handoffs between team members
- **Supports Critical Working Rules**: "One step at a time" includes validation gates

**Customization Guidance**:
- Replace "Quality Validation Criteria" section with domain-specific criteria
- Add specific standards for your deliverable types (code, architecture, tests, documentation)
- Include examples of what "complete" looks like for your domain
- Specify when to use each signoff level (true vs. false vs. "human_required")
- Add multi-level gates for complex workflows if needed

**Anti-Patterns to Avoid**:
- ❌ Proceeding to next phase without validating previous deliverables
- ❌ Using signoff for routine tasks (creates unnecessary overhead)
- ❌ Skipping completion reports for critical deliverables
- ❌ Generic validation criteria that don't guide actual quality assessment
- ❌ Forgetting to populate `completion_signoff_by` field

## Example Implementation

Standard orchestrator with quality gates:

```markdown
## Quality Gates and Validation Framework

### Output Validation Protocol
- **Immediate Validation**: Validate each deliverable upon completion
- **Completeness Check**: Ensure all required elements are present
- **Quality Assessment**: Verify output meets standards and requirements
- **Integration Readiness**: Confirm output can be used by subsequent steps

### Completion Signoff Protocols
- Use `requires_completion_signoff: true` for critical validation points
- Use `requires_completion_signoff: false` for routine tasks  
- Use `requires_completion_signoff: "human_required"` for human review needs
- Document completion with `completion_report` for key deliverables
- Track accountability with `completion_signoff_by` field

### Quality Validation Criteria
- Deliverables meet defined acceptance criteria
- All required components and sections are present
- Outputs follow established standards and conventions
- Work is complete and ready for next phase or stakeholder use
- Dependencies for downstream work are satisfied
```

Architecture specialist with domain-specific criteria:

```markdown
## Quality Gates and Validation Framework

### Output Validation Protocol
- **Immediate Validation**: Validate architecture deliverables upon completion
- **Completeness Check**: Ensure all architecture views and decisions are documented
- **Quality Assessment**: Verify architecture meets technical and business requirements
- **Integration Readiness**: Confirm architecture is implementable and clear to developers

### Completion Signoff Protocols
- Use `requires_completion_signoff: true` for architecture deliverables and critical decisions
- Use `requires_completion_signoff: false` for routine research or exploration tasks
- Use `requires_completion_signoff: "human_required"` for final architecture approval
- Document completion with `completion_report` capturing key architectural decisions
- Track accountability with `completion_signoff_by` field

### Architecture Quality Validation Criteria
- **Completeness**: All architectural views (context, containers, components, deployment) present
- **Decision Documentation**: Key architectural decisions recorded with rationale
- **Standards Compliance**: Architecture follows established patterns and conventions
- **Technical Feasibility**: Design is implementable with available technology and skills
- **Requirements Traceability**: Architecture addresses all functional and non-functional requirements
- **Stakeholder Clarity**: Documentation is clear and understandable to intended audiences
```

Testing specialist with test-specific criteria:

```markdown
## Quality Gates and Validation Framework

### Output Validation Protocol
- **Immediate Validation**: Validate test strategy and test plans upon completion
- **Completeness Check**: Ensure all test types and coverage areas are addressed
- **Quality Assessment**: Verify tests are comprehensive and follow testing standards
- **Integration Readiness**: Confirm tests can be executed and provide meaningful results

### Completion Signoff Protocols
- Use `requires_completion_signoff: true` for test strategy and critical test suites
- Use `requires_completion_signoff: false` for individual test case creation
- Use `requires_completion_signoff: "human_required"` for test execution results
- Document completion with `completion_report` capturing coverage metrics and key findings
- Track accountability with `completion_signoff_by` field

### Test Quality Validation Criteria
- **Coverage Completeness**: All requirements and risk areas have corresponding tests
- **Test Design Quality**: Tests are independent, repeatable, and maintainable
- **Standards Compliance**: Tests follow established testing patterns and conventions
- **Clarity**: Test intent and expected outcomes are clear
- **Executability**: Tests can be run and provide clear pass/fail results
- **Value**: Tests validate meaningful functionality, not implementation details
```

## Component Benefits

- **Structured Validation**: Formal checkpoints prevent quality issues from propagating
- **Accountability**: Clear tracking of who validated what
- **Completion Documentation**: Captures key outcomes and learnings systematically
- **Flexible Rigor**: Three signoff levels support appropriate oversight without overhead
- **Integration Support**: Planning tool integration makes gates enforceable
- **Quality Culture**: Establishes quality validation as non-negotiable practice
- **Prevents Rushing**: Gates force pause for validation before proceeding
- **Customizable Standards**: Domain-specific criteria ensure relevant quality assessment
- **Supports Handoffs**: Signoffs enable clean handoffs between agents or phases
- **Binary Decision**: Clear YES for formal deliverables, NO for exploratory work
