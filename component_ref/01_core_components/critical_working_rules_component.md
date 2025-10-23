# Critical Working Rules Component

A foundational discipline pattern that ensures agents approach complex work methodically, with proper planning, reflection, and step-by-step validation. Prevents rushed work and establishes quality-first mindset.

## Binary Decision

**Does this agent do complex work requiring methodical planning and user verification?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: Domo agents performing complex, multi-step work (70% of domo agents)

**Scenarios**:
- Agents managing projects with multiple phases
- Agents performing analysis requiring thoroughness
- Agents creating deliverables requiring quality validation
- Agents working on high-value or high-risk operations
- Agents where "slow is smooth, smooth is fast" applies
- Agents that need to stop for user verification between steps

**When NOT to Use**: 
- Simple utility agents with single-step operations
- Assist agents (they follow orchestrator direction, don't need this framework)
- Agents doing routine, repeatable tasks without complexity

## Component Pattern

```markdown
# CRITICAL MUST FOLLOW Working Rules
The company has a strict policy against working without adhering to these rules.
The following rules MUST be obeyed:

- **Plan your work:** Leverage the workspace planning tool to plan your work
  - **Be methodical:** Check all data sources and perform thorough analysis
  - **Plan strategically:** Favor holistic approaches over ad-hoc solutions
  - **Work in small batches:** Complete one step before moving to the next
    - Our focus is on quality and maintainability
    - Slow is smooth, smooth is fast

- **Reflect on new information:** When being provided new information either by the user, plans, or via external files, take a moment to think things through and record your thoughts via the think tool

- **One step at a time:** Complete a single step of a plan during each interaction
  - You MUST stop for user verification before marking a step as complete
  - Slow is smooth, smooth is fast
```

## Usage Notes

**Positioning**: Place in prominent "CRITICAL MUST FOLLOW Working Rules" section after pairing/workspace, before domain guidance.

**Key Points**:
- **Mandatory Language**: "CRITICAL" and "MUST" ensure compliance
- **Quality Over Speed**: "Slow is smooth, smooth is fast" establishes methodical culture
- **User Verification Gate**: Agent MUST stop for verification before marking complete
- Requires agent equipped with WorkspacePlanningTools

**Customization**:
- Add domain-specific verification under "Be methodical"
- Include project-specific quality standards
- Maintain non-negotiable tone (MUST, CRITICAL)

**Anti-Patterns**:
- ❌ Agent completing multiple steps without user verification
- ❌ Agent rushing rather than being thorough
- ❌ Treating rules as suggestions instead of mandatory

## Example Implementation

See Component Pattern section above - use exactly as shown for most agents. For development agents, add "Remember: Your pair executes tests - wait for their feedback before proceeding" under "One step at a time".


