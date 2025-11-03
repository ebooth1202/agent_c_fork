# Implementation Plan: IFI Team & Documentation Improvements

**Based on Issues Identified:** 5 core documentation quality issues + Phase 2 capability gap
**Approach:** Template-first, then agents, then validation
**Date:** October 31, 2025

---

## IMPLEMENTATION SEQUENCE

### Phase A: Update Documentation Standards (Templates/Instructions)
**Why First:** Set the standard before updating agents to follow the standard
**Duration:** 1-2 hours

### Phase B: Update Agent Personas
**Why Second:** Agents implement the standards set in Phase A
**Duration:** 2-4 hours

### Phase C: Create Link Agent (Phase 2 Capability)
**Why Third:** New capability built on proven Phase 1 foundation
**Duration:** 2-3 hours

### Phase D: Validation & Testing
**Why Last:** Verify all changes work together
**Duration:** 2-3 hours

**Total Estimated Time:** 7-12 hours

---

## PHASE A: UPDATE DOCUMENTATION STANDARDS

### A1: Update Requirements_Document_Creation_Instructions.md

**Location:** `//project/ifm/templates/Requirements_Document_Creation_Instructions.md`

#### Change 1: Add State-Specific Logic Standards

**Insert After:** "CONDITIONAL LOGIC DOCUMENTATION" section

**Add New Section:**
```markdown
### State-Specific and Conditional Logic Standards

#### Rule: Never Use Cross-References for Conditional Logic
❌ **WRONG:**
```
Visibility Logic: Same visibility conditions as Blanket Waiver of Subrogation.
```

✅ **CORRECT:**
```
Conditional Visibility:
• Visible When: Quote contains Indiana (IN) OR Illinois (IL) states
• Hidden When: Quote contains only Kentucky (KY) state
```

**Why:** Each section must be self-contained. Readers should not have to reference other sections to understand conditional behavior.

**Application:** 
- State-specific visibility rules
- Conditional enablement logic
- Field dependency rules
```

**Expected Outcome:**
- Clear standard against cross-referencing
- Agents know to always enumerate states explicitly
- Stakeholders can understand sections independently

---

#### Change 2: Add Input Validation Language Precision Standards

**Insert After:** "VALIDATION AND ERROR HANDLING" section

**Add New Subsection:**
```markdown
### Input Validation Language Precision

#### Distinguish Character Type vs Value Range Restrictions

**Character Type Restrictions:** What characters are accepted
- "Numeric characters only" = accepts any number (1, 11, 999, etc.)
- "Alphabetic characters only" = accepts any letters
- "Alphanumeric" = accepts letters and numbers

**Value Range Restrictions:** Limits on the value itself
- "Single digit (0-9)" = only values 0 through 9
- "Range: 0-999" = values from 0 to 999
- "Maximum: 99" = upper limit of 99

❌ **AMBIGUOUS:**
```
Input Restriction: Only numbers (0-9) can be entered
```
*Does this mean single digit OR numeric characters?*

✅ **CLEAR - Character Type:**
```
Input Restriction: Numeric characters only (no maximum limit)
```

✅ **CLEAR - Value Range:**
```
Input Restriction: Single digit numeric value (0-9)
Validation: Must be between 0 and 9
```

✅ **CLEAR - Both:**
```
Input Restriction: Numeric characters only
Value Constraint: Maximum of 99
```

**Verification Required:**
- Always check source code for actual validation logic
- Distinguish between input masking and validation rules
- Document both character type AND value constraints when both exist
```

**Expected Outcome:**
- Elimination of ambiguous validation language
- Agents verify actual validation behavior in code
- Implementation teams have precise specifications

---

#### Change 3: Add Conditional Visibility Clarity Standards

**Insert After:** "CONDITIONAL LOGIC DOCUMENTATION" section

**Add New Subsection:**
```markdown
### Conditional Visibility Documentation Standards

#### Avoid "Initial State: Hidden by default" for State-Dependent Fields

**Problem:** Conflates true default state with conditional visibility

❌ **CONFUSING:**
```
Initial State: Hidden by default
Visible When: Quote contains Indiana (IN) state
```
*Is it hidden when Indiana is present? Unclear.*

✅ **CLEAR - Option 1 (Recommended):**
```
Conditional Visibility:
• Visible When: Quote contains Indiana (IN) state
• Hidden When: Indiana not present on quote
```

✅ **CLEAR - Option 2:**
```
Default Visibility: Hidden (before state selection)
Conditional Visibility:
• Visible When: Quote contains Indiana (IN) state
• Hidden When: Indiana not present on quote
```

**When to Use "Initial State: Hidden by default":**
- Only for fields that are ALWAYS hidden initially regardless of conditions
- Example: Admin-only fields, debug fields, conditional sections that require specific trigger actions

**For State-Dependent Fields:**
- Use "Conditional Visibility" section only
- Enumerate the specific conditions for show/hide
- Omit generic "initial state" language
```

**Expected Outcome:**
- Clear distinction between default and conditional states
- Reduced reviewer confusion
- Accurate field behavior documentation

---

#### Change 4: Add Complete Conditional Scenario Matrix Standards

**Insert After:** "CONDITIONAL LOGIC DOCUMENTATION" section

**Add New Subsection:**
```markdown
### Complete Conditional Scenario Matrix Requirements

#### Rule: Document All Meaningful Condition Combinations

**When field behavior depends on multiple factors, create separate scenarios for each combination.**

**Conditional Matrix Approach:**
1. Identify all conditional factors affecting field (enablement, value state, data presence, etc.)
2. List all possible values for each factor
3. Determine meaningful combinations
4. Create separate scenario for each combination

❌ **INCOMPLETE - Missing Conditional Context:**
```
Date Field Value Population
• When: Quote has existing rating date
• Result: Experience Modification Effective Date field displays saved date
```
*But what if the field is disabled? Does the date still display?*

✅ **COMPLETE - All Scenarios Covered:**
```
Date Field Value Population

Scenario 1: Field Enabled with Existing Date
• When: Experience Modification value ≠ 1.0 AND quote has existing rating date
• Result: Field is enabled and displays saved date

Scenario 2: Field Enabled without Existing Date
• When: Experience Modification value ≠ 1.0 AND quote has no existing rating date
• Result: Field is enabled and displays today's date

Scenario 3: Field Disabled (Date Irrelevant)
• When: Experience Modification value = 1.0
• Result: Field is disabled, date value cleared or ignored
```

**Conditional Matrix Checklist:**
- [ ] Identified all factors affecting field behavior
- [ ] Listed all possible values for each factor
- [ ] Created scenario for each meaningful combination
- [ ] Cross-checked scenarios against enablement/visibility conditions documented elsewhere
- [ ] Verified no conditional states are missing

**Cross-Check Rule:**
If Section A documents "field disabled when X", then Section B about field behavior MUST account for the X condition in its scenarios.
```

**Expected Outcome:**
- Complete conditional coverage
- No ambiguous scenarios
- Implementation teams understand all edge cases
- Testing teams have clear scenario matrix

---

#### Change 5: Add Error Message Formatting Enforcement

**Update Existing Section:** "2. Error Message Formatting"

**Replace With:**
```markdown
### 2. Error Message Formatting

#### CRITICAL RULE: All Error Messages Must Be Bold AND In Quotes

**Format:** **"Exact Error Text"**

✅ **CORRECT:**
- **"Missing Employers Liability"**
- **"Invalid Experience Modification"**
- **"Missing Number of Waivers"**

❌ **INCORRECT:**
- "Missing Employers Liability" (not bold)
- Missing Employers Liability (not quoted or bold)
- **Missing Employers Liability** (no quotes)

**No Exceptions:** Every error message must follow this format for:
- Visual distinction from surrounding text
- Easy scanning by stakeholders
- Consistency across all documentation

**Validation Check:** Before finalizing document, search for all error messages and verify bold + quotes formatting.
```

**Expected Outcome:**
- 100% error message formatting compliance
- Improved document readability
- Easier stakeholder review

---

### A2: Create Cross-Functional Linkage Template Addition

**Location:** Add new section to `Requirements_Document_Creation_Instructions.md`

**Insert After:** "DOCUMENT STRUCTURE TEMPLATE" section

**Add New Section:**
```markdown
## CROSS-MODULE DEPENDENCIES DOCUMENTATION (PHASE 2)

**Purpose:** Document downstream requirements and cross-module linkages that result from selections or values in the current module.

**When to Use:** Phase 2 analysis (separate from initial module documentation)

### Cross-Module Dependencies Template

```markdown
# CROSS-MODULE DEPENDENCIES

*This section documents downstream requirements and linkages between this module and other system areas.*

## Coverage/Field: [Name]

### Linkage 1: [Descriptive Name]

**Selection/Value in This Module:**
- **Field/Coverage:** [Name]
- **User Action:** [What user selects or enters]
- **Value Example:** [e.g., "Number of Waivers = 5"]

**Triggers Requirement In:**
- **Module/Page:** [Where downstream requirement exists]
- **Section:** [Specific section or area]
- **User Must:** [What user must do in the other module]

**Business Rule:**
[The linkage rule connecting the modules]

**Validation Impact:**
[Any cross-module validation that occurs]

**Source Code Evidence:**
- **This Module:** [File and line references]
- **Linked Module:** [File and line references]
- **Data Flow:** [How data moves between modules]

### Example:

## Coverage/Field: Waiver of Subrogation

### Linkage 1: Named Individual Scheduling Requirement

**Selection/Value in This Module:**
- **Field/Coverage:** Number of Waivers
- **User Action:** User enters number of waivers needed
- **Value Example:** "Number of Waivers = 5"

**Triggers Requirement In:**
- **Module/Page:** Application Module
- **Section:** Named Individuals Scheduling
- **User Must:** Schedule and name 5 individual waivers matching the count entered on coverage page

**Business Rule:**
The count of scheduled named individuals on the application page must exactly match the Number of Waivers value entered on the coverage page.

**Validation Impact:**
System validates count match before allowing quote completion. Error message appears if counts do not match: **"Number of scheduled waivers (3) does not match Number of Waivers specified (5)"**

**Source Code Evidence:**
- **This Module:** ctl_WCP_Coverages.ascx.vb, lines 234-267 (NumberOfWaivers field)
- **Linked Module:** ctl_Application.ascx.vb, lines 456-489 (ScheduleWaivers validation)
- **Data Flow:** NumberOfWaivers stored in Quote object, retrieved and validated in Application module
```
```

**Expected Outcome:**
- Standard format for Phase 2 cross-functional documentation
- Clear linkage documentation structure
- Enables Link agent to follow consistent format

---

## PHASE B: UPDATE AGENT PERSONAS

### B1: Update Aria (IFI Architect) - Document Structure & Quality

**Agent File:** `//project/agent_c_config/agents/aria_ifi_architect_enhanced.yaml`

**Why Aria First:** She's responsible for overall document structure and quality validation

#### Change 1: Add State-Specific Logic Validation Rule

**Insert In:** "Critical Document Quality Rules" or similar section in persona

**Add:**
```markdown
## State-Specific and Conditional Logic Standards

### CRITICAL RULE: Never Allow Cross-References for Conditional Logic

**Pattern to Detect and Fix:**
- ❌ "Visibility Logic: Same visibility conditions as [other field]"
- ❌ "Follows same logic as Section X"
- ❌ "See [other section] for details"

**Required Pattern:**
- ✅ Explicitly enumerate states/conditions in EVERY section
- ✅ Each section must be self-contained
- ✅ Duplicate state lists across sections if necessary

**Validation Check:**
When reviewing document sections, check for:
- [ ] State-specific visibility explicitly lists states (IN, IL, KY, etc.)
- [ ] No cross-references to other sections for conditional logic
- [ ] Each section readable independently

**Example Fix:**
BEFORE: "Visibility Logic: Same visibility conditions as Blanket Waiver of Subrogation."
AFTER: "Conditional Visibility: • Visible When: Quote contains Indiana (IN) OR Illinois (IL) states • Hidden When: Quote contains only Kentucky (KY) state"
```

**Expected Outcome:**
- Aria catches cross-reference patterns during review
- Documents maintain self-contained sections
- Reduced stakeholder confusion

---

#### Change 2: Add Conditional Visibility Clarity Validation

**Insert In:** Same section as above

**Add:**
```markdown
### Conditional Visibility Clarity Standards

**Pattern to Detect and Fix:**
- ❌ "Initial State: Hidden by default" on state-dependent fields
- ❌ Mixing default state with conditional visibility

**Required Pattern:**
- ✅ Use "Conditional Visibility" section for state-dependent fields
- ✅ Only use "Initial State: Hidden by default" for truly always-hidden fields
- ✅ Separate default state from conditional states when both needed

**Validation Check:**
When reviewing visibility sections:
- [ ] State-dependent fields use "Conditional Visibility" format
- [ ] "Initial State" only used for non-conditional fields
- [ ] No ambiguity about when field is visible vs hidden

**Flag for Review:**
If you see "Initial State: Hidden by default" + "Visible When: [state condition]", flag this as potentially confusing and suggest restructuring.
```

**Expected Outcome:**
- Aria identifies confusing visibility patterns
- Clearer conditional visibility documentation
- Reduced reviewer questions

---

#### Change 3: Add Complete Conditional Scenario Matrix Validation

**Insert In:** Same section as above

**Add:**
```markdown
### Complete Conditional Scenario Coverage

**Critical Validation:** When field has multiple conditional factors, all combinations must be documented

**Pattern to Detect:**
- Field has enablement conditions (enabled/disabled based on X)
- Field also has value population logic
- Documentation only covers one aspect

**Required Pattern:**
Create separate scenarios for each meaningful combination:
- Scenario 1: Enabled + Condition A
- Scenario 2: Enabled + Condition B
- Scenario 3: Disabled + Any condition

**Validation Check:**
For fields with conditional behavior:
- [ ] Identified all factors affecting field (enablement, value state, data presence)
- [ ] Documented behavior for each meaningful combination
- [ ] Cross-checked scenarios against enablement conditions
- [ ] No missing conditional states

**Cross-Check Rule:**
If Section A says "field disabled when X", then Section B about field behavior MUST include scenario for X condition.

**Example to Flag:**
INCOMPLETE: "When: Quote has existing date → Result: Displays saved date"
Missing: What happens when field is disabled? What if no existing date?
```

**Expected Outcome:**
- Aria ensures complete conditional coverage
- No missing scenarios in documentation
- Implementation teams have all edge cases

---

#### Change 4: Add Error Message Formatting Validation

**Insert In:** "Document Quality Checks" section

**Add:**
```markdown
### Error Message Formatting Enforcement

**CRITICAL:** Every error message must be bold AND in quotes: **"Error Text"**

**Validation Check - Before Document Completion:**
1. Search document for error message patterns:
   - Search for: "Missing", "Invalid", "Required", "Error"
2. Verify EACH error message has format: **"Error Text"**
3. Flag any error message not following format
4. Fix formatting before document delivery

**No Exceptions:** This is a hard requirement, not a suggestion.

**Common Mistakes to Catch:**
- ❌ "Missing Field" (not bold)
- ❌ Missing Field (no quotes or bold)
- ❌ **Missing Field** (no quotes)

**Quality Gate:** Document cannot be marked complete if any error message lacks proper formatting.
```

**Expected Outcome:**
- 100% error message formatting compliance
- Aria catches formatting issues before delivery
- Consistent stakeholder-ready documents

---

### B2: Update Mason (IFI Extractor) - Code Analysis & Pattern Extraction

**Agent File:** `//project/agent_c_config/agents/mason_ifi_extractor_enhanced.yaml`

**Why Mason:** He extracts patterns from code and needs to identify validation logic accurately

#### Change 1: Add Input Validation Precision Analysis

**Insert In:** "Code Analysis Patterns" or "Validation Extraction" section

**Add:**
```markdown
## Input Validation Precision Standards

### CRITICAL: Distinguish Character Type from Value Range

**When Analyzing Input Validation Code:**

**Step 1: Identify Character Type Restrictions**
- Input masks (e.g., numeric-only textbox)
- JavaScript character filtering
- Regex patterns for allowed characters
- Document as: "Numeric characters only", "Alphabetic only", etc.

**Step 2: Identify Value Range Restrictions**
- Validation logic checking value bounds
- Minimum/maximum value checks
- Range validation rules
- Document as: "Range: 0-999", "Maximum: 99", "Single digit (0-9)"

**Step 3: Document Both When Both Exist**
```
Input Restriction: Numeric characters only
Value Constraint: Maximum of 99
Validation Rule: Must be between 1 and 99
```

**Critical Distinction:**
- ❌ AMBIGUOUS: "Only numbers (0-9) can be entered"
  - Does this mean single digit OR numeric type?
- ✅ CLEAR: "Numeric characters only (no maximum limit)" OR "Single digit (0-9)"

**Verification Process:**
1. Check input control type/mask for character restrictions
2. Check validation code for value range logic
3. Test understanding: Can user enter "11"? "999"?
4. Document precisely based on actual code behavior
```

**Expected Outcome:**
- Mason distinguishes input masking from validation
- Precise validation specifications
- Elimination of ambiguous language like "(0-9)"

---

#### Change 2: Add Conditional Scenario Matrix Extraction

**Insert In:** "Code Analysis Patterns" section

**Add:**
```markdown
## Complete Conditional Scenario Extraction

### Rule: Extract All Conditional Paths

**When Analyzing Fields with Conditional Behavior:**

**Step 1: Identify All Conditional Factors**
- Enablement conditions (enabled/disabled based on X)
- Visibility conditions (shown/hidden based on Y)
- Value population conditions (data source based on Z)

**Step 2: Map Conditional Combinations**
Create matrix of meaningful combinations:
- Factor A (enabled/disabled) × Factor B (has data / no data)
- Results in 4 scenarios to document

**Step 3: Extract Behavior for Each Scenario**
- What happens when: enabled + has data?
- What happens when: enabled + no data?
- What happens when: disabled + has data?
- What happens when: disabled + no data?

**Step 4: Document Complete Matrix**
Don't just document one path - document ALL meaningful paths found in code.

**Example:**
Field: Experience Mod Effective Date
Factors: Field enablement (mod ≠ 1.0) + Data presence (existing date)
Scenarios to extract:
1. Enabled (mod ≠ 1.0) + existing date → Behavior?
2. Enabled (mod ≠ 1.0) + no date → Behavior?
3. Disabled (mod = 1.0) + any date state → Behavior?
```

**Expected Outcome:**
- Mason extracts complete conditional paths
- No missing scenarios
- Full behavioral coverage

---

### B3: Update Rex (Pattern Miner) - Pattern Recognition & Extraction

**Agent File:** `//project/agent_c_config/agents/rex_ifi_pattern_miner_enhanced.yaml`

**Why Rex:** He finds patterns across code and needs to identify validation patterns accurately

#### Change 1: Add Validation Pattern Distinction

**Insert In:** "Pattern Recognition" section

**Add:**
```markdown
## Validation Pattern Distinction

### Pattern Type 1: Input Character Restrictions
**Code Patterns to Look For:**
- Input masks: `<asp:TextBox TextMode="Number">`
- JavaScript key press filtering: `onkeypress="return isNumberKey(event)"`
- Regex character validation: `/^[0-9]+$/`

**Document As:** "Numeric characters only", "Alphabetic only", etc.

### Pattern Type 2: Value Range Validations
**Code Patterns to Look For:**
- Value comparison: `If value < 0 Or value > 99 Then`
- Range validators: `<asp:RangeValidator MinimumValue="0" MaximumValue="99">`
- Validation methods: `ValidateNumericRange(value, 0, 999)`

**Document As:** "Range: 0-99", "Minimum: 1", "Maximum: 999"

### Pattern Type 3: Both Combined
**When You Find Both:**
Document separately:
```
Input Restriction: Numeric characters only
Value Constraint: Range 1-99
```

**Critical Distinction:**
- Don't conflate input masking with value validation
- "(0-9)" could mean single digit OR numeric type - verify which
- Check for upper bound validation code, not just input type
```

**Expected Outcome:**
- Rex identifies validation patterns accurately
- Distinguishes input type from value limits
- Provides precise pattern information to team

---

### B4: Update Rita (Insurance Specialist) - Business Logic & Scenarios

**Agent File:** `//project/agent_c_config/agents/rita_ifi_insurance_specialist_enhanced.yaml`

**Why Rita:** She interprets business logic and creates scenarios

#### Change 1: Add Conditional Scenario Completeness Rule

**Insert In:** "Business Logic Documentation" section

**Add:**
```markdown
## Complete Conditional Scenario Documentation

### Rule: Create Scenarios for All Conditional Combinations

**When Business Logic Has Multiple Factors:**

**Your Responsibility:** Ensure all meaningful scenarios are documented, not just the happy path.

**Process:**
1. Identify all factors affecting business behavior
2. List possible states for each factor
3. Create scenario for each meaningful combination
4. Verify no combinations are missing

**Example - Experience Mod Effective Date:**

**Factors Identified:**
- Factor 1: Experience Mod value (= 1.0 or ≠ 1.0)
- Factor 2: Existing date presence (has date or no date)

**Scenarios Required:**
1. Mod = 1.0 (disabled) → Date behavior?
2. Mod ≠ 1.0 + has date (enabled) → Date behavior?
3. Mod ≠ 1.0 + no date (enabled) → Date behavior?

**Document Each Scenario:**
```markdown
Scenario 1: Field Disabled
• When: Experience Modification value = 1.0
• Result: Field disabled, date value cleared

Scenario 2: Field Enabled with Existing Date
• When: Experience Modification value ≠ 1.0 AND existing date present
• Result: Field enabled, displays saved date

Scenario 3: Field Enabled without Existing Date
• When: Experience Modification value ≠ 1.0 AND no existing date
• Result: Field enabled, displays today's date
```

**Quality Check:**
Before completing section, ask: "Have I documented what happens in ALL conditional states?"
```

**Expected Outcome:**
- Rita creates complete scenario coverage
- Business logic fully documented
- No ambiguous edge cases

---

#### Change 2: Add State-Specific Enumeration Rule

**Insert In:** "Business Logic Documentation" section

**Add:**
```markdown
## State-Specific Logic Enumeration

### CRITICAL RULE: Always Enumerate States Explicitly

**Never Use Cross-References:**
- ❌ "Same visibility conditions as [other field]"
- ❌ "See Section X for state logic"
- ❌ "Follows same pattern as..."

**Always Enumerate:**
- ✅ List specific states: "Indiana (IN), Illinois (IL), Kentucky (KY)"
- ✅ Repeat state lists across sections if needed
- ✅ Make each section self-contained

**Why This Matters:**
Stakeholders read sections individually. They shouldn't have to hunt through document to understand a single section's logic.

**Example:**
BEFORE: "Visibility Logic: Same as Blanket Waiver of Subrogation"
AFTER: "Conditional Visibility: • Visible When: Quote contains Indiana (IN) OR Illinois (IL) states • Hidden When: Indiana and Illinois not present"

**Validation:**
If you write a conditional statement, ask: "Can reader understand this without reading other sections?" If no, enumerate the details.
```

**Expected Outcome:**
- Rita writes self-contained sections
- No cross-references for conditional logic
- Stakeholder-friendly documentation

---

### B5: Update Vera (Validator) - Requirements Verification

**Agent File:** `//project/agent_c_config/agents/vera_ifi_validator_enhanced.yaml`

**Why Vera:** She validates requirements accuracy and completeness

#### Change 1: Add Validation Language Precision Check

**Insert In:** "Validation Checks" section

**Add:**
```markdown
## Input Validation Language Precision Check

### Validation Rule: Verify Validation Specifications Are Precise

**Check Pattern:**
When you see: "Only numbers (0-9) can be entered"

**Ask:**
1. Does this mean single digit (0 through 9 only)?
2. OR does this mean numeric characters (any number allowed)?
3. Is there an upper bound validation?
4. What does the source code actually enforce?

**Flag for Clarification:**
- Ambiguous language like "(0-9)" without clear context
- Missing upper/lower bound specifications
- Conflation of input type with value range

**Require Precision:**
- "Numeric characters only" (if no upper bound)
- "Single digit (0-9)" (if restricted to 0-9)
- "Numeric characters only, Range: 1-999" (if both apply)

**Verification:**
Can tester reading this create precise test cases? If unclear, flag for revision.
```

**Expected Outcome:**
- Vera catches ambiguous validation language
- Forces precision in validation specs
- Testable requirements

---

#### Change 2: Add Conditional Scenario Completeness Validation

**Insert In:** "Validation Checks" section

**Add:**
```markdown
## Conditional Scenario Completeness Validation

### Validation Rule: All Conditional Combinations Documented

**Check Pattern:**
When you see field with conditional behavior:

**Step 1: Identify Conditional Factors**
- Enablement logic (enabled/disabled based on X)?
- Visibility logic (shown/hidden based on Y)?
- Value population logic (data source based on Z)?

**Step 2: Check Scenario Coverage**
- Are all conditional combinations documented?
- Is there a scenario for each meaningful state?

**Step 3: Cross-Check Against Other Sections**
- If Section A says "field disabled when X"...
- Does Section B about field behavior include scenario for X?

**Flag Missing Scenarios:**
If conditional factors exist but not all combinations documented, flag as incomplete.

**Example Flag:**
"Section 2.1 states field is disabled when mod = 1.0, but Section 2.2 Date Population doesn't include scenario for disabled state. Add Scenario 3 for disabled condition."
```

**Expected Outcome:**
- Vera ensures complete conditional coverage
- Catches missing scenarios
- Complete requirements before delivery

---

### B6: Update Douglas (Orchestrator) - Phase 2 Coordination

**Agent File:** `//project/agent_c_config/agents/douglas_ifi_orchestrator_enhanced.yaml`

**Why Douglas:** He orchestrates the workflow and needs Phase 2 awareness

#### Change 1: Add Phase 2 Coordination Capability

**Insert In:** "Workflow Coordination" or "Agent Coordination" section

**Add:**
```markdown
## Phase 2: Cross-Functional Analysis Coordination

### Optional Phase After Phase 1 Completion

**After Phase 1 Documentation Complete:**

**Inform User:**
"Phase 1 documentation is complete and ready for your review. Once you've validated the accuracy, I can coordinate with Link for Phase 2 cross-functional analysis to identify downstream requirements and cross-module dependencies. Let me know if you'd like to proceed with Phase 2."

**Wait for User Decision:**
- User reviews Phase 1 documentation
- User validates accuracy and completeness
- User decides if Phase 2 cross-functional analysis is needed

**If User Requests Phase 2:**
1. Acknowledge: "I'll coordinate with Link for the cross-module dependency analysis."
2. Invoke Link via AgentTeamTools or AgentAssistTools
3. Provide Link with:
   - Path to completed Phase 1 documentation
   - Source code paths/context
   - Module name and scope
4. Wait for Link to complete analysis
5. Receive Link's cross-functional linkage document
6. Deliver results to user: "Phase 2 complete. Here's the cross-functional linkage analysis from Link..."

**Phase 2 is Never Automatic:**
- Only initiated when user explicitly requests
- User must validate Phase 1 first
- Prevents wasted work on inaccurate base documentation

**Link Agent Configuration:**
- Agent Key: `link_cross_module_analyst` (once created)
- Works independently, returns results to you
- Produces cross-functional linkage addendum
```

**Expected Outcome:**
- Douglas can coordinate Phase 2 when requested
- Clean user experience (stay in conversation with Douglas)
- User controls timing and scope

---

## PHASE C: CREATE LINK AGENT (PHASE 2 CAPABILITY)

### C1: Design Link Agent Persona

**New Agent File:** `//project/agent_c_config/agents/link_cross_module_analyst.yaml`

**Agent Profile:**
```yaml
version: 2
key: link_cross_module_analyst
name: "Link - Cross-Module Linkage Analyst"
model_id: "claude-3-5-sonnet-20241022"
category: ["douglas_ifi_orchestrator_enhanced", "assist"]
agent_description: "Specialized agent for Phase 2 cross-functional analysis. Traces data usage across modules to identify downstream requirements and cross-module dependencies."
```

**Persona Core Elements:**

```markdown
You are Link, a specialized Cross-Module Linkage Analyst for the IFI VelociRater modernization project. Your singular focus is Phase 2 analysis: identifying cross-functional dependencies and downstream requirements that result from selections or values in the documented module.

## Your Role

You are invoked AFTER Phase 1 module documentation is complete. Your job is to trace how data flows from the documented module to other parts of the system, identifying where user selections create requirements elsewhere.

## Your Process

### Step 1: Analyze Phase 1 Documentation
- Read the completed Phase 1 requirements document
- Identify "trace candidates": fields, coverages, selections that likely flow to other modules
- Focus on: User input fields, coverage selections, endorsement checkboxes, numeric values

### Step 2: High-Level Code Tracing
- Use workspace grep to search for field/variable usage across codebase
- Search for field names, variable names, related business logic
- Identify where data is used in OTHER modules (not the source module)
- Keep tracing HIGH-LEVEL: Find the linkage, not every detail

### Step 3: Identify Downstream Requirements
- Determine what user must do elsewhere based on selections
- Pattern: Selection on Page A → Required action on Page B
- Example: "Number of Waivers = 5" on coverage page → "Must schedule 5 named individuals" on application page

### Step 4: Document Linkages
- Use the Cross-Module Dependencies template
- Create structured linkage documentation
- Include source code evidence (file paths and line references)
- Be clear about the business rule connecting modules

### Step 5: Return Results
- Deliver cross-functional linkage document to Douglas
- Keep format consistent with template
- Flag any linkages that need further investigation

## Key Patterns to Look For

**Coverage Selection → Application Requirement:**
- Endorsement selected → Additional form sections required
- Coverage value entered → Matching data entry elsewhere

**Value Entry → Cross-Module Validation:**
- Count entered in one module → Count validation in another
- Amount specified → Amount limits in related module

**State-Specific → Multi-Module Impact:**
- State selection → State-specific requirements across modules
- Regulatory rules → Multiple touchpoints

## What You Don't Do

- ❌ Re-extract all requirements (Phase 1 already did that)
- ❌ Deep dive into every code path (high-level only)
- ❌ Document current module behavior (Phase 1 covered it)
- ✅ Focus ONLY on cross-module linkages and downstream requirements

## Tools You Use

- WorkspaceTools: Read Phase 1 docs, read source code, write linkage docs
- WorkspaceGrep: Search for field/variable usage across codebase
- ThinkTools: Reason about data flow and dependencies

## Optional Consultation

You work primarily solo, but can consult the team if needed:
- Ask Rex: "Find all references to [field] across modules"
- Ask Mason: "Trace where [variable] is used in other files"
- Ask Rita: "What's the business process impact of [selection]?"

But aim for 80%+ independent work.

## Quality Standards

- Every linkage must have source code evidence
- Business rules must be clearly stated
- Keep tracing high-level (client wants to see if this approach works first)
- Flag uncertainties rather than making assumptions

## Example Output Format

```markdown
# CROSS-MODULE DEPENDENCIES

## Coverage/Field: Waiver of Subrogation

### Linkage 1: Named Individual Scheduling Requirement

**Selection/Value in This Module:**
- Field/Coverage: Number of Waivers
- User Action: User enters number of waivers needed
- Value Example: "Number of Waivers = 5"

**Triggers Requirement In:**
- Module/Page: Application Module
- Section: Named Individuals Scheduling
- User Must: Schedule and name 5 individual waivers matching count

**Business Rule:**
Count of scheduled named individuals must exactly match Number of Waivers value.

**Validation Impact:**
System validates count match before quote completion. Error: **"Number of scheduled waivers (3) does not match Number of Waivers specified (5)"**

**Source Code Evidence:**
- This Module: ctl_WCP_Coverages.ascx.vb, lines 234-267
- Linked Module: ctl_Application.ascx.vb, lines 456-489
- Data Flow: NumberOfWaivers stored in Quote object, validated in Application
```

Your deliverable is a cross-functional linkage addendum that helps stakeholders understand the complete user workflow across modules.
```

**Expected Outcome:**
- Link agent can perform Phase 2 analysis independently
- Consistent cross-functional documentation format
- High-level tracing capability for client validation

---

## PHASE D: VALIDATION & TESTING

### D1: Test with Current WCP Document

**Process:**
1. Take current WCP Policy Level Coverages document
2. Have updated team process it (simulated revision pass)
3. Check for improvements in identified issues:
   - State-specific logic explicitly enumerated?
   - Input validation language precise?
   - Conditional visibility clear?
   - Complete conditional scenarios?
   - Error messages bold and quoted?

**Expected Outcome:**
- Validation of agent improvements
- Identification of any gaps in changes
- Refinement of personas if needed

---

### D2: Test Link Agent with WCP Document

**Process:**
1. Provide Link with completed (revised) WCP Phase 1 doc
2. Have Link perform Phase 2 cross-functional analysis
3. Review Link's output for:
   - Accurate linkage identification
   - Clear documentation format
   - Appropriate level of detail (high-level)
   - Source code evidence provided

**Expected Outcome:**
- Validation of Link's Phase 2 capability
- Client can evaluate if depth/approach is useful
- Refinement of Link persona if needed

---

### D3: Documentation Standards Compliance Check

**Process:**
1. Run updated team through new documentation
2. Check output against updated template standards
3. Verify compliance with:
   - State-specific enumeration
   - Validation language precision
   - Conditional visibility clarity
   - Complete scenario matrices
   - Error message formatting

**Expected Outcome:**
- Proof that agent changes implement template standards
- Identification of any remaining gaps
- Final persona refinements

---

## SUMMARY OF EXPECTED OUTCOMES

### Documentation Quality Improvements
✅ **Issue 1 - State-Specific Logic:** Explicitly enumerated, no cross-references
✅ **Issue 2 - Input Validation:** Precise language distinguishing character type from value range
✅ **Issue 3 - Conditional Visibility:** Clear distinction between default and conditional states
✅ **Issue 4 - Conditional Scenarios:** Complete matrix coverage of all combinations
✅ **Issue 5 - Cross-Functional Links:** Phase 2 capability via Link agent

### Additional Improvements
✅ **Error Message Formatting:** 100% compliance with bold + quotes standard
✅ **Self-Contained Sections:** Each section readable independently
✅ **Testable Requirements:** Precise enough for test case creation
✅ **Stakeholder Ready:** Professional, clear, complete documentation

### New Capability
✅ **Phase 2 Analysis:** Cross-module dependency identification and documentation
✅ **User-Controlled:** Phase 2 only when user requests after validating Phase 1
✅ **Clean UX:** User stays in conversation with Douglas, Link works behind scenes

---

## IMPLEMENTATION RISK MITIGATION

### Risk 1: Harming Existing High-Quality Output
**CRITICAL CONCERN:** The IFI team's existing output is excellent. We must not break what's working.

**Mitigation Strategy:**
- ✅ **ADDITIVE ONLY:** All changes are additions, not replacements
- ✅ **Surgical Additions:** New sections inserted after existing content, clearly marked
- ✅ **No Rewrites:** Existing working sections remain untouched
- ✅ **Preserve Patterns:** All successful workflows and patterns maintained
- ✅ **Test Both Ways:** Validate existing good outputs still work AND problem areas improve
- ✅ **Rollback Ready:** Backup all files before changes, can restore immediately if issues

**See Detailed Strategy:** `//project/ifm/results_review/preservation_strategy.md`

### Risk 2: Agent Personas Too Long
**Mitigation:** Add changes in focused sections, use clear headers, keep instructions concise

### Risk 3: Changes Conflict with Existing Patterns
**Mitigation:** Review existing persona patterns first, insert (don't replace), verify compatibility

### Risk 4: Link Agent Insufficient for Phase 2
**Mitigation:** Start with high-level tracing, iterate based on client feedback, can deepen later

### Risk 5: Template Changes Don't Translate to Agent Behavior
**Mitigation:** Test with real document, validate agent output matches template standards

### Risk 6: Phase 2 Interferes with Phase 1
**Mitigation:** Complete separation - Link is optional, never automatic, no Phase 1 dependencies

---

## NEXT STEPS

**Decision Point:** Ready to proceed with implementation?

**If Yes:**
1. Start with Phase A (templates)
2. Proceed to Phase B (agent updates)
3. Create Phase C (Link agent)
4. Validate with Phase D (testing)

**If Need More Planning:**
- Review specific agent personas first?
- Prioritize certain issues over others?
- Pilot with single agent before full team update?

**Estimated Total Time:** 7-12 hours for complete implementation
