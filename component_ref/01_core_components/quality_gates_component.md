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

**Positioning**: Place in dedicated "Quality Gates" section after planning/coordination, before domain workflows.

**Key Points**:
- **Requires Planning Tools**: Signoff features in WorkspacePlanningTools
- **Three Signoff Levels**: true (agent/team), false (none), "human_required" (human validation)
- **Completion Reports**: Capture outcomes for critical deliverables
- **Accountability**: `completion_signoff_by` tracks who validated

**Customization**:
- Replace "Quality Validation Criteria" with domain-specific criteria
- Specify when to use each signoff level
- Add examples of what "complete" means in your domain

**Anti-Patterns**:
- ❌ Proceeding without validating previous deliverables
- ❌ Using signoff for routine tasks
- ❌ Generic validation criteria that don't guide assessment

## Example Implementation

See Component Pattern section above for standard usage. Customize "Quality Validation Criteria" section with domain-specific standards (e.g., architecture: "All views present, decisions documented"; testing: "Coverage complete, tests independent and repeatable").


