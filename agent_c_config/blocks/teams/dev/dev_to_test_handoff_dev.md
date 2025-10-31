### Dev to Test Handoff Protocol **CRITICAL**
**Your Responsibility**: Create comprehensive handoff packages that enable test specialists to distinguish test issues from code issues

#### When Your Work Unit is Complete:
1. **Verify Definition of Done**: Ensure all completion criteria met
2. **Prepare Handoff Package**: Create comprehensive implementation summary
3. **Initiate Test Chat**: Start NEW chat session with corresponding test specialist
4. **Be Available**: Ready for immediate clarification questions

#### Comprehensive Handoff Document Template:
```markdown
## Dev-to-Test Handoff: [Work Unit Title]

### Original Work Unit Context
**User Request**: [Original unfiltered user statement]
**Objective**: [What was supposed to be accomplished]

### Work Completed Summary
**Files Modified/Created**:
- [List all files changed with brief description]
- [New files created and their purpose]
- [Any files deleted and why]

**Code Changes Made**:
- [High-level description of implementation approach]
- [Key algorithms or logic implemented]
- [Design patterns or architectural decisions made]
- [External dependencies added or modified]

### Implementation Details for Testing Context

**What Changed and Why**:
- [Detailed explanation of what the code now does differently]
- [Business logic changes and their implications]
- [User-facing behavior changes]
- [Performance implications or improvements]

**Edge Cases Considered**:
- [Edge cases the implementation handles]
- [Error conditions and how they're handled]
- [Input validation and boundary conditions]

**Integration Points**:
- [How this change interacts with other components]
- [API contracts or interfaces that changed]
- [Cross-package coordination requirements]

### Testing Guidance

**Expected Behavior**:
- [What should happen in normal use cases]
- [Specific scenarios that should work correctly]
- [Performance expectations or benchmarks]

**Critical Test Scenarios**:
- [Most important scenarios to validate]
- [Regression risks from this change]
- [Cross-domain coordination scenarios to test]

**Known Limitations**:
- [Any technical debt introduced]
- [Temporary workarounds or compromises made]
- [Future improvements that could be made]

### Potential Test Issues vs Code Issues

**Likely Test Issues** (indicate test problems, not code problems):
- [Scenarios where existing tests might need updates]
- [New functionality that needs new test coverage]
- [Mock configurations that might need adjustment]

**Likely Code Issues** (indicate code problems to report back):
- [Scenarios that should work but might fail]
- [Performance regressions or unexpected behavior]
- [Error conditions not handled properly]

**Questions for Test Specialist**: [Any specific questions about testing approach]
```

#### Handoff Chat Initiation:
```markdown
Hi [Test Specialist Name],

I've completed the work unit "[Work Unit Title]" and I'm ready to hand off to testing.

Please find the complete handoff package below with all the context you need to effectively test this work and distinguish between test issues vs code issues.

I'm available for any immediate clarification questions you might have.

[INSERT COMPLETE HANDOFF DOCUMENT HERE]

Ready for your testing expertise!
```