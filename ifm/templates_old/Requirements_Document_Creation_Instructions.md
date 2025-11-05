# REQUIREMENTS DOCUMENT CREATION INSTRUCTIONS

**Purpose:** Complete instructions for creating professional, stakeholder-ready requirements documents with zero tolerance for assumptions and complete source code verification.

**Application:** Use these instructions to generate requirement documents for any functional area of IFI VelociRator requiring analysis and documentation.

---

## DOCUMENT STRUCTURE TEMPLATE

### Standard Document Header Format
```markdown
# [SYSTEM AREA] - COMPLETE REQUIREMENTS DOCUMENT

**Document:** [Line of Business] [System Area] Requirements  
**Analysis Date:** [Current Date]  
**Source Verification:** 100% Source Code Verified  
**Coverage Scope:** Complete [System Area] functionality

---

## Executive Summary

[2-3 paragraph summary covering business scope, functional areas, and verification approach]

**Business Scope:** [Brief description of what the system area covers]
```

### Section Structure Template (Repeat for Each Functional Area)
```markdown
# Section X.X - [Functional Area Name]

## Business Purpose

[2-3 sentences explaining why this functional area exists and its business value]

**Business Requirement:** [Single sentence stating the core business requirement]

## Field Specifications

### Basic Field Configuration
- **Field Type:** [Input type]
- **Business Label:** "[Label text]" (include asterisk notation if required)
- **Position:** [Location in interface]
- **Character Limit:** [Limit details if applicable]
- **Required Status:** [Required/Optional with business context]
- **Navigation Order:** [Tab order if applicable]

## User Experience & Validation

### User Action Scenarios

#### [Scenario Name]
- **User Action:** [Specific user action]
- **System Response:** [System behavior]
- **Error Message:** **"[Exact Error Text]"** (if applicable - ALWAYS BOLD)
- **User Must Do:** [Required user response]
- **Application Scope:** [When this applies]

[Repeat for all user scenarios]


### Document Completion Template
```markdown
## Document Completeness Verification

This comprehensive requirements document covers all major functional areas of the [System Area]:

✅ **[Area 1]** - [Brief description]  
✅ **[Area 2]** - [Brief description]  
[Continue for all areas covered]

## Overall Source Code Reference

**Primary Implementation Files:**
- **[Main File]:** [Description and line count if known]
- **[Secondary File]:** [Description]

**Supporting Systems:**
- **[System 1]:** [Purpose and scope]
- **[System 2]:** [Purpose and scope]

**Validation and Business Logic Framework:**
- **Location:** [Framework location]
- **Purpose:** [Framework purpose]
- **Integration:** [Integration scope]
```

---

## MANDATORY FORMATTING REQUIREMENTS

### 1. Markdown Structure Standards
- **Main Title:** Single # (H1)
- **Major Sections:** Double ## (H2) 
- **Subsections:** Triple ### (H3)
- **Sub-subsections:** Quadruple #### (H4)
- **Consistent Hierarchy:** Maintain logical header progression

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

### 3. Source Code Details Format
**MANDATORY END-OF-SECTION FORMAT:**
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

## CONTENT REQUIREMENTS

### 1. Zero-Assumption Mandate
- **Source Code Evidence:** Every statement must be backed by verified source code
- **No Speculation:** Remove any content that cannot be verified
- **Mark Unknowns:** If something cannot be verified, do not include it
- **Exact Behavior:** Document only what is proven to exist in code

### 2. Business-Friendly Language
- **Convert Technical Terms:** Change "txtBusinessName" to "Business Name field"
- **Explain Purpose:** Always explain WHY a field or rule exists
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

## SECTIONS TO AVOID

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
- **Implementation Notes:** Convert to business purpose or remove

---

## VALIDATION AND ERROR HANDLING

### Error Message Documentation
- **Exact Text:** Use precise error message text from source
- **Bold Formatting:** **"All error messages in bold"**
- **User Context:** Explain when error appears
- **Resolution:** Explain what user must do to resolve

### Validation Rules Documentation
- **Trigger Conditions:** When validation fires
- **Validation Logic:** What is being validated
- **Business Purpose:** Why validation exists
- **Source Evidence:** Line references for validation code

---

## INPUT VALIDATION LANGUAGE PRECISION

### Distinguish Character Type vs Value Range Restrictions

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

---

## CONDITIONAL LOGIC DOCUMENTATION

### Field Dependencies
- **Trigger Conditions:** What causes field to show/hide/change
- **Dependent Fields:** Which fields are affected
- **Business Logic:** Why dependency exists
- **User Impact:** How user experience changes

### Dynamic Behavior
- **State Changes:** Document field state changes
- **Visibility Rules:** When fields appear/disappear
- **Validation Changes:** How validation changes based on conditions
- **Data Impact:** What happens to data during state changes

---

## ADVANCED CONDITIONAL LOGIC STANDARDS

### State-Specific Logic Standards

#### Rule: Never Use Cross-References for Conditional Logic

**Each section must be self-contained.** Readers should not have to reference other sections to understand conditional behavior.

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

**Application:**
- State-specific visibility rules
- Conditional enablement logic
- Field dependency rules
- Any conditional behavior tied to specific states or conditions

**Why This Matters:** Each section must be readable independently. Always enumerate specific states/conditions even if duplicated elsewhere.

---

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
- Example: Admin-only fields, debug fields

**For State-Dependent Fields:**
- Use "Conditional Visibility" section only
- Enumerate the specific conditions for show/hide
- Omit generic "initial state" language

---

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

---

## QUALITY CONTROL CHECKLIST

### Before Finalizing Any Document

#### Structure Verification
- [ ] Proper markdown header hierarchy (H1, H2, H3, H4)
- [ ] No bold formatting in headers
- [ ] Consistent bullet point formatting
- [ ] Source Code Details at end of each section

#### Content Verification  
- [ ] Every error message is bold and in quotes
- [ ] All statements backed by source code evidence
- [ ] No assumption-based content included
- [ ] Business-friendly language used throughout
- [ ] User action scenarios properly formatted

#### Coverage Verification
- [ ] All fields in functional area documented
- [ ] All validation rules covered
- [ ] All LOB-specific behavior included
- [ ] All conditional logic documented
- [ ] Complete source code traceability provided

#### Exclusion Verification
- [ ] No Quality Assurance sections
- [ ] No Testing Guidance sections
- [ ] No Modernization Considerations
- [ ] No Technical Implementation Details
- [ ] No duplication between sections

---

## SUCCESS CRITERIA

### Document Quality Indicators
A successful requirements document will have:
- **Complete Functional Coverage** - All areas of the system documented
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

---

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
```

### Example Cross-Module Documentation:

```markdown
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

**Phase 2 Checklist:**
- [ ] Identified all selections that trigger downstream requirements
- [ ] Documented application/module linkages
- [ ] Traced data usage across modules
- [ ] Documented cross-module validation rules
- [ ] Identified user workflow implications

---

**REMEMBER:** These instructions ensure consistent, high-quality requirements documentation that serves both business stakeholders and technical implementation teams. Every requirements document created using this methodology should be immediately usable for stakeholder review, technical implementation, and modernization planning.