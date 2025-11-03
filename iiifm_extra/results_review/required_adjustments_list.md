# Required Adjustments List - IFI Team & Templates

**Purpose:** Tracking specific issues and patterns that need to be addressed in agent personas and/or document templates
**Status:** COMPILATION IN PROGRESS - NO CHANGES MADE YET
**Date Started:** October 31, 2025

---

## DOCUMENTATION PATTERN ISSUES

### Issue 1: State-Specific Logic Must Be Explicit
**Location:** Section 4.4 - Waiver of Subrogation Field
**Current Problem:**
```
Visibility Logic: Same visibility conditions as Blanket Waiver of Subrogation.
```

**Client Feedback:** "It would be useful to call out/identify the different states, specifically as it pertains to the 'Visibility Logic' section"

**Required Change Pattern:**
- ❌ **NEVER:** Use "same as" references for state-specific or condition-specific logic
- ✅ **ALWAYS:** Explicitly spell out states/conditions even if duplicated elsewhere
- **Example:** Should explicitly state "Visible When: Quote contains Indiana (IN) OR Illinois (IL) states"

**Impact on Agents:**
- Agents must recognize state-specific patterns and ALWAYS make them explicit
- Agents should not create cross-references for visibility/conditional logic
- Each section must be self-contained with complete state information

---

### Issue 2: Input Validation Accuracy
**Location:** Section 4.4 - Number of Waivers Field
**Current Problem:**
```
Input Restriction: Only numbers (0-9) can be entered
```

**Client Feedback:** "The client advises that they were able to enter a rate with 11"
**Related Comment:** [TS14] "I was able to enter and rate with 11. Code source?"

**Analysis:**
- Documented restriction suggests single-digit only (0-9)
- Actual behavior allows multi-digit numbers (11+)
- Either:
  - Restriction statement is inaccurate (should say "numeric values only")
  - OR no upper bound validation exists
  - OR code verification was insufficient

**Required Change Pattern:**
- ❌ **NEVER:** Document input restrictions without code verification
- ✅ **ALWAYS:** Verify actual validation logic in source code
- ✅ **ALWAYS:** Test actual behavior if possible or flag for testing
- **If uncertain:** Document what IS verified and note what needs confirmation

**Impact on Agents:**
- Agents must distinguish between:
  - Character type restrictions (numeric only)
  - Value range restrictions (0-9 specific range)
  - Upper/lower bound validations
- When documenting "Only numbers (0-9)" agents must verify if this means:
  - Single digit restriction (0 through 9)
  - OR numeric character type (any number)

---

## GENERAL PRINCIPLES EMERGING

### Principle 1: Self-Contained Sections
**Rule:** Each section must contain complete information without requiring readers to reference other sections for critical details

**Applies To:**
- State-specific visibility logic
- Conditional behavior rules
- Validation requirements

**Why It Matters:** Stakeholders and developers should be able to understand requirements from reading a single section

---

### Principle 2: Precision in Validation Language
**Rule:** Distinguish clearly between character type restrictions and value range restrictions

**Language Standards:**
- "Numeric only" = accepts any number
- "0-9" = single digit from 0 to 9
- "Range: 0-999" = specific value bounds
- "Maximum: 99" = upper limit validation

**Why It Matters:** Implementation teams need precise validation specifications

---

### Principle 3: Code Verification Over Assumption
**Rule:** When actual behavior contradicts documentation, flag for source code verification

**Red Flags:**
- Tester reports behavior different from documented
- Comments indicate uncertainty ("Code source?")
- Logic seems unclear or incomplete

**Why It Matters:** Zero-assumption mandate requires all statements backed by verified source

---

### Principle 4: Complete Conditional Scenario Matrix
**Rule:** When field behavior depends on multiple conditions, document ALL meaningful condition combinations

**Applies To:**
- Fields with enablement conditions + value population logic
- Fields with state-dependent behavior + data conditions
- Any field where multiple factors affect behavior

**Matrix Approach:**
1. Identify all conditional factors (enablement, value state, data presence, etc.)
2. Identify all possible values for each factor
3. Document behavior for each meaningful combination
4. Create separate scenarios rather than generic statements

**Why It Matters:** Incomplete conditional logic causes implementation ambiguity and testing gaps

---

## AGENT ADJUSTMENT AREAS (Preliminary)

### Area 1: State-Specific Logic Documentation
**Affected Agents:** 
- Mason (IFI Extractor) - Pattern extraction
- Rita (Insurance Specialist) - Business logic interpretation
- Aria (IFI Architect) - Document structure

**Needed Adjustments:**
- Add explicit rule: Never use "same as" for state/condition visibility
- Add pattern: Always enumerate states explicitly
- Add validation: Check for cross-references in conditional logic

---

### Area 2: Input Validation Specification
**Affected Agents:**
- Mason (IFI Extractor) - Code analysis
- Rex (Pattern Miner) - Validation pattern extraction
- Vera (Validator) - Requirements verification

**Needed Adjustments:**
- Add distinction between character type vs value range
- Add verification requirement for input restrictions
- Add flagging protocol when behavior contradicts documentation

---

### Area 3: Section Self-Containment
**Affected Agents:**
- Aria (IFI Architect) - Document structure
- Douglas (Orchestrator) - Quality oversight

**Needed Adjustments:**
- Add self-containment validation rule
- Add cross-reference detection
- Add completeness check for each section

---

### Area 4: Conditional Visibility Clarity
**Affected Agents:**
- Mason (IFI Extractor) - Code analysis for visibility logic
- Rita (Insurance Specialist) - Business rule interpretation
- Aria (IFI Architect) - Visibility section structure

**Needed Adjustments:**
- Add distinction between true default state vs conditional visibility
- Avoid "hidden by default" for state-dependent fields
- Add pattern: Focus on conditional triggers rather than default states
- Add clarity rule: Separate initial state (before interaction) from conditional states (after interaction)

---

### Area 5: Complete Conditional Scenario Coverage
**Affected Agents:**
- Mason (IFI Extractor) - Code analysis for all conditional paths
- Rita (Insurance Specialist) - Business logic scenario identification
- Aria (IFI Architect) - Scenario structure and organization
- Rex (Pattern Miner) - Conditional pattern extraction

**Needed Adjustments:**
- Add conditional matrix thinking: identify all factors affecting behavior
- Add combination analysis: document behavior for each meaningful combination
- Add validation: Check that all conditional states mentioned elsewhere are covered in behavior sections
- Add pattern: When field has enablement logic, apply that condition to ALL behavior descriptions
- Add cross-check rule: If section A says "field disabled when X", section B about field behavior must account for X condition

---

### Area 6: Cross-Functional Dependency Analysis
**Affected Agents:**
- Rex (Pattern Miner) - Data flow pattern extraction across modules
- Mason (IFI Extractor) - Cross-module code tracing
- Rita (Insurance Specialist) - Business process linkage identification
- Douglas (Orchestrator) - Scope management for multi-module analysis
- Aria (IFI Architect) - Cross-functional linkage documentation structure

**Scope Decision:**
✅ **SEPARATE ANALYSIS PHASE** - Cross-functional analysis will be conducted as a separate phase after initial module documentation

**Phased Approach:**
- **Phase 1:** Module-centric documentation (current approach)
- **Phase 2:** Cross-functional dependency analysis and linkage documentation

**Needed Adjustments:**
- Design separate Phase 2 workflow for cross-functional analysis
- Create cross-module thinking prompts: "Where else is this data used?"
- Add downstream requirement identification capability
- Add data flow tracing capability (may require new tools/approaches)
- Add "Cross-Module Dependencies" section template for Phase 2 output
- Add linkage validation patterns
- Determine if Phase 2 needs:
  - New specialized agent(s) for cross-functional analysis
  - OR enhancement to existing team with Phase 2 mode
  - Different code analysis tools (data flow analysis, database query tools, etc.)

**Phase 2 Design Considerations:**
- **Invocation:** User-initiated only (after reviewing Phase 1 accuracy)
- **Input:** Completed Phase 1 module documentation
- **Process:** Trace data usage across modules, identify downstream requirements
- **Output:** Cross-functional linkage addendum or integrated update to Phase 1 docs
- **Tooling:** Current source code (grep-based tracing)
- **Rationale:** User validates Phase 1 before Phase 2 investment, prevents wasted work

**Decisions Made:**
✅ **Tracing Depth:** High-level initially (see if client needs deeper)
✅ **Tools/Resources:** Current source code (no new database tools)

**Open Questions:**
- ❓ **Implementation Approach:** New specialized agent(s) vs enhance existing team?
  - See: `//project/ifm/results_review/phase2_approach_comparison.md` for detailed comparison

---

## TEMPLATE ADJUSTMENT AREAS (Preliminary)

### Template Issue 1: Visibility Logic Standards
**Current Template Section:**
```markdown
### Conditional Visibility
•  Visible When: [condition]
•  Hidden When: [condition]
```

**Needed Enhancement:**
- Add explicit instruction: "Always enumerate specific states/conditions. Never use 'same as' references."
- Add example of good vs bad visibility documentation

---

### Template Issue 2: Input Restriction Standards
**Current Template Section:**
```markdown
### Field Specifications
- **Field Type:** [Input type]
```

**Needed Enhancement:**
- Add subsection for input validation with clear language distinctions:
  - Character type restrictions
  - Value range restrictions
  - Upper/lower bounds
  - Format requirements

---

### Template Issue 3: Conditional Visibility Standards
**Current Template Section:**
```markdown
### Conditional Visibility
•  Visible When: [condition]
•  Hidden When: [condition]
```

**Needed Enhancement:**
- Remove or clarify "Initial State" guidance for state-dependent fields
- Add instruction: For state-dependent visibility, focus on conditional triggers
- Add pattern distinction:
  - Use "Default Visibility: Hidden" only for fields that are truly always hidden initially
  - Use "Conditional Visibility" with explicit trigger conditions for state-dependent fields
- Add example:
  ```
  GOOD:
  Conditional Visibility:
  • Visible When: Quote contains Indiana (IN) state
  • Hidden When: Indiana not present on quote
  
  CONFUSING:
  Initial State: Hidden by default
  Visible When: Quote contains Indiana (IN) state
  ```

---

### Template Issue 4: Conditional Scenario Matrix Standards
**Current Template Section:**
```markdown
### User Action Scenarios

#### [Scenario Name]
- **User Action:** [Specific user action]
- **System Response:** [System behavior]
```

**Needed Enhancement:**
- Add instruction: When field has multiple conditional factors, create separate scenarios for each combination
- Add conditional matrix checklist:
  - [ ] Identified all factors affecting field behavior
  - [ ] Listed all possible values for each factor
  - [ ] Created scenario for each meaningful combination
  - [ ] Cross-checked scenarios against enablement/visibility conditions
- Add example:
  ```
  INCOMPLETE:
  Date Field Value Population
  • When: Quote has existing rating date
  • Result: Field displays saved date
  
  COMPLETE:
  Date Field Value Population
  
  Scenario 1: Enabled with Existing Date
  • When: Mod value ≠ 1.0 AND quote has existing rating date
  • Result: Field enabled and displays saved date
  
  Scenario 2: Enabled without Existing Date  
  • When: Mod value ≠ 1.0 AND quote has no existing rating date
  • Result: Field enabled and displays today's date
  
  Scenario 3: Disabled State
  • When: Mod value = 1.0 (regardless of existing date)
  • Result: Field disabled, date value cleared/ignored
  ```

---

### Template Issue 5: Cross-Functional Linkage Documentation
**Current Template:** No section for cross-module dependencies

**Needed Addition:**
```markdown
## Cross-Module Dependencies

### Downstream Requirements
**Coverage/Field:** [Name of coverage or field]
**Selection/Value:** [What user selects or enters]
**Triggered Requirement:** [What becomes required elsewhere]
**Location:** [Where the requirement exists - module/page/section]
**Business Rule:** [The linkage rule]
**Example:** When "Number of Waivers" is set to 5, user must schedule 5 named individuals on Application side

### Data Usage in Other Modules
**Field/Value:** [Field name]
**Used By:** [Other module/page names]
**Usage Purpose:** [Why other module needs this data]
**Validation Impact:** [Any cross-module validation rules]
```

**Checklist to Add:**
- [ ] Identified all selections that trigger downstream requirements
- [ ] Documented application/module linkages
- [ ] Traced data usage across modules
- [ ] Documented cross-module validation rules
- [ ] Identified user workflow implications

---

### Issue 3: Conditional Visibility State Confusion
**Location:** Section 4.5 - Exclusion of Amish Workers (Indiana)
**Current Problem:**
```
Initial State: Hidden by default

State-Specific Availability
•  Visible When: Quote contains Indiana (IN) state
•  Hidden When: Quote does not include Indiana
```

**Client Feedback:** "The initial state is not hidden by default if it's Indiana. So perhaps before any state is selected, it is hidden?"
**Related Comment:** [TS16] "Not hidden if Indiana"

**Analysis:**
- "Initial State: Hidden by default" is confusing/misleading
- The field IS hidden when no states selected (true initial state)
- The field becomes VISIBLE when Indiana is added to quote
- Current wording suggests it's always hidden initially even with Indiana present
- Conflates "default state" with "conditional visibility based on state selection"

**Required Change Pattern:**
- ❌ **NEVER:** Use ambiguous "Initial State: Hidden by default" when visibility is state-dependent
- ✅ **ALWAYS:** Clarify the true initial state vs conditional states
- **Better Pattern:**
  ```
  Default Visibility: Hidden (before states selected)
  Conditional Visibility:
  • Visible When: Quote contains Indiana (IN) state
  • Hidden When: Quote does not include Indiana
  ```
- OR simply omit "Initial State" and rely on Conditional Visibility section

**Impact on Agents:**
- Agents must distinguish between:
  - True initial/default state (before any user actions)
  - Conditional visibility (based on user selections/state)
- "Hidden by default" should only be used for fields that remain hidden regardless of conditions
- State-dependent fields should focus on conditional visibility triggers
- Avoid mixing "default" and "conditional" terminology in same section

---

## ITEMS TO TRACK AS WE CONTINUE

*This section will be updated as the user identifies more specific issues*

### Issue 4: Incomplete Conditional Logic Scenarios
**Location:** Section 2.2 - Experience Modification Effective Date Field
**Current Problem:**
```
Date Field Value Population
Condition 1: Existing Rating Date
  • When: Quote has existing rating effective date
  • Result: Experience Modification Effective Date field displays saved date
```

**Client Feedback:** "If the mod value is or isn't 1, how does it affect that condition? With each condition, it should either specify the value as 1 or not 1 or whatever other value(s) it could be or just create the different sections where values of 1 are in this section and the other values are in this/these sections."
**Related Comment:** [TS3] "Either this is not working as intended, or the requirement laid out here is inaccurate"
**Related Comment:** [TS4R3] "Maybe this is true only if mod is not 1?"

**Analysis:**
- Current documentation shows date population logic without considering the mod value condition
- Field enablement is conditional (disabled when mod = 1.0, enabled when mod ≠ 1.0)
- Date population logic should account for BOTH scenarios:
  - What happens to saved date when mod = 1.0? (field is disabled)
  - What happens to saved date when mod ≠ 1.0? (field is enabled)
- Incomplete conditional matrix - doesn't address all combinations

**Required Change Pattern:**
- ❌ **NEVER:** Document field behavior without considering all conditional states
- ✅ **ALWAYS:** Create separate condition sections for each value/state combination
- **Better Pattern:**
  ```
  Date Field Value Population
  
  Scenario 1: Mod Value = 1.0 (Field Disabled)
    • When: Quote has existing rating date AND mod value = 1.0
    • Result: Field is disabled, date value is cleared/ignored
  
  Scenario 2: Mod Value ≠ 1.0 with Existing Date (Field Enabled)
    • When: Quote has existing rating date AND mod value ≠ 1.0
    • Result: Field displays saved date and is enabled for editing
  
  Scenario 3: Mod Value ≠ 1.0 without Existing Date (Field Enabled)
    • When: Quote has no existing rating date AND mod value ≠ 1.0
    • Result: Field displays today's date and is enabled for editing
  ```

**Impact on Agents:**
- Agents must identify ALL conditional states that affect field behavior
- When documenting field behavior, check for:
  - Enablement conditions
  - Value conditions
  - State combinations (enabled+hasValue, enabled+noValue, disabled+hasValue, etc.)
- Create separate scenario for each meaningful combination
- Never document partial logic that ignores known conditional states

---

### Issue 5: Cross-Functional Linkages Not Documented
**Location:** Multiple sections - Cross-module dependencies
**Current Problem:**
Documentation covers individual module/page behavior but doesn't capture downstream requirements or cross-functional linkages.

**Client Feedback (Sarah):** 
"I do wonder about the tie in between the coverages/endorsements and the application side and how we could go about finding requirements for that. For example, if you have waiver of subrogation, you have to enter a number of waivers (agent has this all down), but then when navigate to the app side, you would have to schedule out the names of the 5 waivers you said you had. So if the agent was able to say 'If you select this coverage, you will be required to schedule Named Individuals on the application', that would be useful."

**Analysis:**
- Current documentation scope is module/page-centric
- Missing linkages between related functional areas:
  - Coverage selections → Application requirements
  - Field values → Other page/module dependencies
  - Endorsement selections → Downstream data collection
- Example: "Waiver of Subrogation" + "Number of Waivers: 5" triggers requirement to schedule 5 named individuals on application side
- These cross-functional dependencies are critical for:
  - Complete user workflow understanding
  - Data validation across modules
  - Modernization planning (need to know all touchpoints)

**Required Change Pattern:**
- ❌ **INCOMPLETE:** Document coverage selection in isolation
  ```
  Number of Waivers Field
  • User enters number of waivers
  • Validation: Must be numeric
  ```
  
- ✅ **COMPLETE:** Document coverage selection + downstream requirements
  ```
  Number of Waivers Field
  • User enters number of waivers (e.g., 5)
  • Validation: Must be numeric
  
  Downstream Requirements:
  • Application Module Impact: User must schedule named individuals 
    matching the number of waivers entered
  • Location: Application side / Named Individuals scheduling section
  • Business Rule: Number of scheduled individuals must equal number 
    of waivers specified
  ```

**Challenges Identified:**
1. **Scope Expansion:** Requires analysis beyond single module/page source code
2. **Traceability:** Need to identify cross-module dependencies in code or database
3. **Extraction Checklist:** Current checklist may not prompt for cross-functional linkages
4. **Code Analysis:** May require following data flow across multiple files/modules

**Impact on Agents:**
- Agents need to think beyond current module boundaries
- When documenting selections/values, agents should ask:
  - "Does this selection trigger requirements elsewhere?"
  - "Where else is this data used?"
  - "What downstream actions does this create?"
- Need pattern recognition for:
  - Coverage → Application linkages
  - Endorsement → Data collection linkages
  - Selection → Validation in other modules

**Potential Solutions to Explore:**
1. **Add Cross-Functional Section to Template:**
   - "Downstream Requirements" or "Cross-Module Dependencies" subsection
   - Forces agents to consider linkages

2. **Enhance Extraction Checklist:**
   - Add questions about data usage in other modules
   - Add prompt for cross-functional validation rules
   - Add database/data model analysis step

3. **Multi-Pass Analysis:**
   - First pass: Document module in isolation
   - Second pass: Trace data usage across modules
   - Third pass: Document cross-functional requirements

4. **Database/Data Model Analysis:**
   - Analyze where field data is stored
   - Trace where that data is read/validated elsewhere
   - Document dependencies found

**Questions for User:**
- Should extraction scope expand to include cross-module analysis?
- How deep should cross-functional tracing go?
- Should this be a separate analysis phase or integrated into initial extraction?
- Are there existing data flow diagrams or database schemas to aid this?

---

### Next Issues to Document:
- [Waiting for user input]

---

## STATUS: HOLDING FOR MORE INPUT

**Do NOT make changes yet. Continuing to compile adjustment requirements.**
