# IFI Requirements Documentation Standards

**Reference Document for Requirements Documentation**  
**Version:** 1.0  
**Last Updated:** 2025-10-31  
**Used By:** Mason IFI Requirements Extractor

---

## Overview

This document contains the professional documentation standards for creating IFI requirements documents. All requirements documents must adhere to these standards to ensure stakeholder readiness and implementation clarity.

## PROHIBITED CONTENT - DO NOT INCLUDE

**Client Requirements - These sections are strictly forbidden:**
- ❌ **Executive Summaries** of any kind
- ❌ **Business Purpose** explanations or sections
- ❌ **Insurance Compliance** frameworks or regulatory guidance
- ❌ **Modernization Recommendations** or architectural strategy
- ❌ **Agent Involvement** explanations or process descriptions
- ❌ **Business Impact** analysis or operational recommendations

**Focus Requirements:**
- ✅ Document ONLY what currently exists in the system
- ✅ Provide technical specifications for implementation
- ✅ Include source code evidence for all claims
- ✅ Use business-friendly language for field descriptions

---

## Document Structure Standards

### Standard Document Header Format

```markdown
# [SYSTEM AREA] - COMPLETE REQUIREMENTS DOCUMENT

**Document:** [Line of Business] [System Area] Requirements  
**Analysis Date:** [Current Date]  
**Source Verification:** 100% Source Code Verified  
**Coverage Scope:** Complete [System Area] functionality
```

### Section Structure Template (Repeat for Each Functional Area)

```markdown
# Section X.X - [Functional Area Name]

## Field Specifications
### Basic Field Configuration
- **Field Type:** [Input type]
- **Business Label:** "[Label text]" (include asterisk notation if required)
- **Position:** [Location in interface]
- **Character Limit:** [Limit details if applicable]
- **Required Status:** [Required/Optional with business context]

### Complete Option Set (REQUIRED for dropdown/selection fields)
- **Available Options:** [ALL possible values with source evidence]
- **Business Meaning:** [What each option represents in business terms]
- **Selection Dependencies:** [Options available only under certain conditions]
- **Value Ranges:** [Acceptable value ranges for inputs]

### Selection Impact Analysis (REQUIRED for user-selectable options)
- **Business Rules Triggered:** [What logic fires when each option selected]
- **Additional Requirements:** [Fields that become required/visible per selection]
- **Premium/Calculation Impact:** [Effect on calculations or pricing per option]
- **Downstream Consequences:** [What happens elsewhere in system per selection]
- **Conditional Behavior:** [How selection affects other field availability]

## User Experience & Validation
### User Action Scenarios
- **User Action:** [Specific user action]
- **System Response:** [System behavior]
- **Error Message:** **"[Exact Error Text]"** (ALWAYS BOLD + QUOTES)
- **User Must Do:** [Required user response]

### UI Alert Messages (MANDATORY - If Applicable)

For any section where UI alerts appear, include this subsection:

```markdown
#### UI Alert Messages

**Alert [#]: [Alert Name/Type]**
- **Location:** [Specific page/section where alert appears]
- **Trigger:** [Specific condition that causes the alert]
- **Alert Text:** **"[Exact message text in bold quotes]"**

[Repeat for each alert in the section]
```

**Alert Types to Document:**
- JavaScript popup alerts
- Validation error messages
- Informational text displays  
- System notifications
- Auto-upgrade notifications
- Warning messages
- Confirmation dialogs

**Formatting Requirements:**
- All alert text MUST be in **bold quotes**: **"Alert message here"**
- Each alert documented separately with its own Alert # designation
- Positioned in same section as related functionality
- Include Location (where it appears), Trigger (what causes it), and exact Alert Text
```

---

## Mandatory Formatting Requirements

### 1. Markdown Structure Standards

- **Main Title:** Single # (H1)
- **Major Sections:** Double ## (H2)
- **Subsections:** Triple ### (H3)
- **Sub-subsections:** Quadruple #### (H4)
- **Consistent Hierarchy:** Maintain logical header progression

### 2. Error Message Formatting (CRITICAL RULE)

**All error messages MUST be bold AND in quotes:** **"Exact Error Text"**

✅ **CORRECT**:
- **"Missing Employers Liability"**
- **"Invalid Experience Modification"**
- **"Missing Number of Waivers"**

❌ **INCORRECT**:
- "Missing Employers Liability" (not bold)
- Missing Employers Liability (not quoted or bold)
- **Missing Employers Liability** (no quotes)

**No Exceptions**: Every error message must follow this format for visual distinction and consistency.

### 3. Source Code Details Format

**MANDATORY END-OF-SECTION FORMAT**:
```markdown
## Source Code Details:
**Primary Location:** [Main files with specific line references]  
**Secondary Location:** [Supporting files] OR "NA"  
**External Dependencies:** [External systems] OR "NA"
```

### 4. List and Bullet Formatting

- **Consistent Bullets:** Use - for all bullet points
- **Proper Indentation:** Maintain consistent indentation
- **No Mixed Formats:** Don't mix bullets with numbers unless specifically needed
- **Clear Separation:** Space between major list items

---

## Content Requirements

### 1. Zero-Assumption Mandate

- **Source Code Evidence:** Every statement backed by verified source code
- **No Speculation:** Remove content that cannot be verified
- **Mark Unknowns:** If something cannot be verified, do not include it
- **Exact Behavior:** Document only proven code behavior

### 2. Business-Friendly Language

- **Convert Technical Terms:** "txtBusinessName" → "Business Name field"
- **User-Focused:** Write from user perspective, not developer perspective
- **Professional Tone:** Suitable for business stakeholders and technical teams

### 3. User Action Focus

- **Specific Scenarios:** "User Action: [specific action]"
- **System Response:** "System Response: [exact behavior]"
- **User Requirements:** "User Must Do: [required action]"
- **Context:** "Application Scope: [when this applies]"

### 4. Complete Coverage

- **All Fields:** Document every field in the functional area
- **All Validation:** Cover all validation rules with source evidence
- **All LOB Behavior:** Include Line of Business specific differences
- **All Conditional Logic:** Document field dependencies and conditional behavior

---

## Sections to Avoid

### 1. Remove These Sections Completely

- **Quality Assurance** sections
- **Testing Guidance** sections
- **Modernization Considerations** sections
- **Technical Implementation Details** sections
- **Future Enhancements** sections

### 2. Transform These Elements

- **Technical Matrices:** Convert to business narrative requirements
- **Technical Properties:** Integrate into field specifications as business requirements
- **Code References:** Move to Source Code Details section only
- **Implementation Notes:** Remove if not directly from source code

---

## Validation and Error Handling Documentation

### Error Message Documentation

- **Exact Text:** Use precise error message text from source
- **Bold Formatting:** **"All error messages in bold and quotes"**
- **User Context:** Explain when error appears
- **Resolution:** Explain what user must do to resolve

### Validation Rules Documentation

- **Trigger Conditions:** When validation fires
- **Validation Logic:** What is being validated
- **Source Evidence:** Line references for validation code

---

## Input Validation Language Precision

### Distinguish Character Type vs Value Range Restrictions

**Character Type Restrictions** (what characters are accepted):
- "Numeric characters only" = accepts any number (1, 11, 999, etc.)
- "Alphabetic characters only" = accepts any letters
- "Alphanumeric" = accepts letters and numbers

**Value Range Restrictions** (limits on the value itself):
- "Single digit (0-9)" = only values 0 through 9
- "Range: 0-999" = values from 0 to 999
- "Maximum: 99" = upper limit of 99

❌ **AMBIGUOUS**:
```
Input Restriction: Only numbers (0-9) can be entered
```
*Does this mean single digit OR numeric characters?*

✅ **CLEAR - Character Type**:
```
Input Restriction: Numeric characters only (no maximum limit)
```

✅ **CLEAR - Value Range**:
```
Input Restriction: Single digit numeric value (0-9)
Validation: Must be between 0 and 9
```

✅ **CLEAR - Both**:
```
Input Restriction: Numeric characters only
Value Constraint: Maximum of 99
```

### Verification Required

- Always check source code for actual validation logic
- Distinguish between input masking and validation rules
- Document both character type AND value constraints when both exist

---

## Conditional Logic Documentation

### Field Dependencies

- **Trigger Conditions:** What causes field to show/hide/change
- **Dependent Fields:** Which fields are affected
- **Dependency Logic:** How fields relate based on source code
- **User Impact:** How user experience changes

### Dynamic Behavior

- **State Changes:** Document field state changes
- **Visibility Rules:** When fields appear/disappear
- **Validation Changes:** How validation changes based on conditions
- **Data Impact:** What happens to data during state changes

---

## Advanced Conditional Logic Standards

### State-Specific Logic Standards

Each section must be self-contained. Never use cross-references for conditional logic.

❌ **WRONG**:
```
Visibility Logic: Same visibility conditions as Blanket Waiver of Subrogation.
```

✅ **CORRECT**:
```
Conditional Visibility:
• Visible When: Quote contains Indiana (IN) OR Illinois (IL) states
• Hidden When: Quote contains only Kentucky (KY) state
```

### Conditional Visibility Documentation Standards

Avoid "Initial State: Hidden by default" for state-dependent fields (conflates true default with conditional visibility).

❌ **CONFUSING**:
```
Initial State: Hidden by default
Visible When: Quote contains Indiana (IN) state
```

✅ **CLEAR - Option 1 (Recommended)**:
```
Conditional Visibility:
• Visible When: Quote contains Indiana (IN) state
• Hidden When: Indiana not present on quote
```

### Complete Conditional Scenario Matrix Requirements

When field behavior depends on multiple factors, create separate scenarios for each combination.

**Conditional Matrix Approach**:
1. Identify all conditional factors affecting field (enablement, value state, data presence, etc.)
2. List all possible values for each factor
3. Determine meaningful combinations
4. Create separate scenario for each combination

❌ **INCOMPLETE - Missing Conditional Context**:
```
Date Field Value Population
• When: Quote has existing rating date
• Result: Experience Modification Effective Date field displays saved date
```
*But what if the field is disabled? Does the date still display?*

✅ **COMPLETE - All Scenarios Covered**:
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

### Conditional Matrix Checklist

- [ ] Identified all factors affecting field behavior
- [ ] Listed all possible values for each factor
- [ ] Created scenario for each meaningful combination
- [ ] Cross-checked scenarios against enablement/visibility conditions
- [ ] Verified no conditional states are missing

---

## Endorsement Analysis Standard (NEW)

### Purpose

Standardized format for documenting endorsement functionality with downstream application requirements. Applies to all LOBs (Workers Comp, General Liability, BOP, etc.).

### Endorsement Documentation Structure

```markdown
## X.X [Endorsement Name]

### X.1 Field Specifications
[Keep existing Field Specifications format - no changes]

### X.2 User Selections/User Interactions

X.21 When the endorsement checkbox for "[Endorsement Name]" is selected, [system behavior description in business terms].

X.22 [Additional field behavior if applicable - progressive disclosure, count fields, etc.]

X.23 [Validation behavior and confirmation dialogs]

X.24 [Save/data storage behavior in business terms]

### X.3 Downstream Impacts

#### X.31 Applications Page

X.311 When the [Endorsement Name] endorsement has been selected, [application page behavior].

X.312 [User data entry requirements in application module].

X.313 [Validation requirements and error messages].

#### X.32 [Other Module - Rating Engine/Claims Processing/Billing/etc.]

X.321 [Module-specific impact description].

X.322 [Additional impacts within same module].

## Source Code Details:
**Primary Location:** [Main files with specific line references] + [Main Control]

**Secondary Location:** [Supporting files] + [Main Control] OR "NA"

**External Dependencies:** [External systems] + [Main Control] OR "NA"
```

### Endorsement Analysis Requirements

**Mandatory Content:**
- ✅ **Field Specifications:** Keep existing format unchanged
- ✅ **User Selections/Interactions:** Business-friendly description of checkbox/field behavior
- ✅ **Downstream Impacts:** Document application page requirements and other module impacts
- ✅ **Source Code Details:** Use new format with separate lines

**Language Requirements:**
- ❌ **No method calls:** Avoid `CheckWaiverOfSubro()`, `govStateQuote.HasWaiverOfSubrogation`
- ❌ **No technical properties:** Avoid `INQuote.HasExclusionOfAmishWorkers`
- ✅ **Business language:** "When the endorsement is selected", "The system stores the selection"
- ✅ **User-focused:** "Users must add individual records", "The Application page displays"

**Hierarchical Numbering:**
- Use X.1, X.2, X.3 for main subsections
- Use X.21, X.22, X.23 for detailed items under subsections
- Use X.311, X.312, X.313 for items under downstream impact modules

**Data Exclusion Rule:**
- ❌ **Exclude `IgnoreForLists="Yes"`:** Any dropdown options marked with this attribute must be excluded
- ✅ **User-accessible options only:** Document only options actually available to users

### Common Downstream Impact Categories

**Applications Page (Most Common):**
- Named individual collection requirements
- Additional data entry forms
- Documentation upload requirements

**Rating Engine:**
- Premium calculation impacts
- Rating factor applications
- Multi-state rating coordination

**Claims Processing:**
- Coverage determination changes
- Exclusion application
- Recovery rights modifications

**Billing System:**
- Premium calculation impacts
- Invoice documentation
- Payment processing changes

**Regulatory Compliance:**
- State reporting requirements
- Filing obligations
- Audit trail maintenance

---

## Cross-Module Dependencies Documentation (Phase 2)

### Purpose

Document downstream requirements and cross-module linkages resulting from selections in the current module.

### Cross-Module Dependencies Template

```markdown
# CROSS-MODULE DEPENDENCIES

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
```

---

## Quality Control Checklist

### Before Finalizing Any Document

**Structure Verification**:
- [ ] Proper markdown header hierarchy (H1, H2, H3, H4)
- [ ] No bold formatting in headers
- [ ] Consistent bullet point formatting
- [ ] Source Code Details at end of each section

**Content Verification**:
- [ ] Every error message is bold and in quotes
- [ ] All statements backed by source code evidence
- [ ] No assumption-based content included
- [ ] Business-friendly language used throughout
- [ ] User action scenarios properly formatted

**Coverage Verification**:
- [ ] All fields in functional area documented
- [ ] All validation rules covered
- [ ] All LOB-specific behavior included
- [ ] All conditional logic documented
- [ ] Complete source code traceability provided

**Option Completeness Verification** (MANDATORY):
- [ ] Every dropdown field lists ALL possible options with source evidence
- [ ] Every selectable option documents business impact when chosen
- [ ] Selection consequences documented (what happens when selected vs not selected)
- [ ] Business meaning provided for all technical values
- [ ] No "various options available" - must specify complete option set

**Exclusion Verification**:
- [ ] No Quality Assurance sections
- [ ] No Testing Guidance sections
- [ ] No Modernization Considerations
- [ ] No Technical Implementation Details
- [ ] No duplication between sections

---

## Enhanced UI Interaction Specifications (Optional)

**When to Use:** For complex UI components requiring detailed user interaction documentation (modals, dynamic forms, multi-step processes, validation-heavy interfaces)

**Standard Format:**
```markdown
### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** [State and appearance conditions]
- **Additional Information Section:** [Initial visibility state]
- **Dynamic Elements:** [Any elements that change based on conditions]

**User Action: [Specific Action Name]**
- **System Response:** [Immediate system behavior]
- **Text Area/Field Specifications:** (if applicable)
  - **Label:** "[Exact label text]"
  - **Text Box Type:** [Input type with technical reference]
  - **Styling:** [Visual appearance and constraints]
  - **Required:** [Requirement conditions]

**User Action: [Error Condition]**
- **Visual Indicator:** [What user sees]
- **Border/Color Changes:** [Visual feedback]
- **Label Changes:** [Dynamic label text]
- **Validation Block:** [Prevention behavior]

**User Action: [Resolution Action]**
- **Visual Recovery:** [How UI returns to normal]
- **Form Status:** [Ready state indicators]

**User Action: [Completion Action]**
- **System Response:** [Final processing behavior]
- **Business Rule:** [Rule that fires]
- **Integration:** [External system calls with codes]
```

### Enhanced UI Documentation Standards

**Apply Enhanced Format When:**
✅ Modal popups with complex validation  
✅ Multi-step user workflows  
✅ Dynamic field interactions (show/hide/enable)  
✅ Progressive disclosure patterns  
✅ Real-time validation with visual feedback

**Use Standard Format When:**
❌ Simple text fields  
❌ Basic dropdowns/checkboxes  
❌ Read-only display areas  
❌ Standard form validation

**Visual State Documentation Requirements:**
- **Color Transitions:** Document specific color changes (black to red, etc.)
- **Border States:** Normal vs error border styling
- **Dynamic Labels:** Exact text changes for different states
- **Icons/Indicators:** Asterisks, checkmarks, error symbols

**Quality Requirements:**
- Source code evidence for UI behavior (JavaScript + backend)
- Complete user interaction workflows documented
- Error recovery patterns with visual feedback
- No mixing enhanced and standard formats in same section

---

## Success Criteria

### Document Quality Indicators

A successful requirements document will have:
- **Complete Functional Coverage** - All areas of system documented
- **Zero Assumptions** - Every statement verified against source code
- **Business Stakeholder Ready** - Professional language suitable for business review
- **Technical Implementation Ready** - Complete source code traceability for development
- **Streamlined Structure** - No unnecessary technical complexity or testing details
- **Professional Formatting** - Clean, consistent markdown structure

### Stakeholder Value Delivery

The final document should provide:
- **Clear Business Understanding** - Stakeholders understand what system does
- **Implementation Guidance** - Technical teams have complete requirements
- **Validation Reference** - QA teams understand expected behavior
- **Regulatory Compliance** - All business rules and validation documented for compliance review

---

**End of Documentation Standards**
