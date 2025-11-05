# Endorsement Analysis Template

**Reference Template for Standardized Endorsement Documentation**
**Used By:** All IFI Analysis Agents (Rex, Mason, Aria, Rita)
**Applies To:** All LOBs (Workers Comp, General Liability, BOP, etc.)

---

## Template Structure

```markdown
## X.X {ENDORSEMENT_NAME}

### X.1 Field Specifications
[Keep existing Field Specifications format - no changes to this section]

### X.2 User Selections/User Interactions

X.21 When the endorsement checkbox for "{ENDORSEMENT_NAME}" is selected, [system behavior description in business terms].

X.22 [Additional field behavior if applicable - progressive disclosure, count fields, etc.]

X.23 [Validation behavior and confirmation dialogs]

X.24 [Save/data storage behavior in business terms]

### X.25 UI Alert Messages (If Applicable)

**Alert 1: [Alert Type]**
- **Location:** [Where alert appears]
- **Trigger:** [What causes it]
- **Alert Text:** **"[Exact message text]"**

[Repeat for additional alerts in this endorsement]

### X.3 Downstream Impacts

#### X.31 Applications Page

X.311 When the {ENDORSEMENT_NAME} endorsement has been selected, [application page behavior].

X.312 [User data entry requirements in application module].

X.313 [Validation requirements and error messages].

#### X.32 {OTHER_MODULE}

X.321 [Module-specific impact description].

X.322 [Additional impacts within same module].

## Source Code Details:
**Primary Location:** [Main files with specific line references] + [Main Control]

**Secondary Location:** [Supporting files] + [Main Control] OR "NA"

**External Dependencies:** [External systems] + [Main Control] OR "NA"
```

---

## Template Variables

**{ENDORSEMENT_NAME}** - Replace with actual endorsement name:
- Waiver of Subrogation
- Exclusion of Amish Workers  
- Additional Insured
- Blanket Contractual Liability
- etc.

**{LOB_NAME}** - Line of Business:
- Workers Compensation (WCP)
- General Liability (CGL)
- Business Owner's Policy (BOP)
- Commercial Property (CPP)

**{APPLICATION_MODULE}** - Common application requirements:
- Named Individuals
- Additional Interests
- Location Details
- Coverage Extensions

**{OTHER_MODULE}** - Common downstream modules:
- Rating Engine
- Claims Processing  
- Billing System
- Underwriting
- Regulatory Compliance

---

## Example: Waiver of Subrogation (WCP)

```markdown
## 2.1 Waiver of Subrogation Endorsement

### 2.1 Field Specifications
- **Field Type:** Checkbox with progressive disclosure
- **Business Label:** "Waiver of Subrogation (WC 04 03 06)(IN/IL)"
- **Position:** Endorsements section
- **Required Status:** Optional (user choice)
- **Progressive Field:** "Number of Waivers" text input appears when checked

### 2.2 User Selections/User Interactions

2.21 When the endorsement checkbox for "Waiver of Subrogation" is selected, the "Number of Waivers" text input field becomes visible and available for user entry.

2.22 The "Number of Waivers" field becomes required for form validation when the checkbox is checked, requiring a numeric value greater than zero.

2.23 When the checkbox is unchecked, the system displays confirmation dialog "Are you sure you want to delete this coverage?" before clearing the waiver data and hiding the Number of Waivers field.

2.24 During save operations, the system stores both the checkbox selection state and the waiver count value for use in downstream processing.

### 2.3 Downstream Impacts

#### 2.31 Applications Page

2.311 When the Waiver of Subrogation endorsement has been selected, the Application page displays the "Waiver of Subrogation" section for data entry.

2.312 Users must add individual waiver records equal to the number specified on the coverage page, each containing a mandatory name field.

2.313 The system validates each waiver name is not empty with error message "Missing Name" if validation fails.

#### 2.32 Claims Processing

2.321 Waiver records are referenced during claims processing to determine subrogation rights limitations based on the named waivers.

2.322 Claims processing validates claim subrogation against the specific waiver names stored in the application module to determine recovery rights.

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 370-380 (CheckWaiverOfSubro method), Lines 598-612 (Save method) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 25-50 (WaiverOfSubrogation enum), Lines 200-250 (Save method) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 100-150 (Populate method) + ctl_AppSection_WCP
```

---

## Language Guidelines

### ✅ USE (Business-Friendly)
- "When the endorsement checkbox is selected"
- "The system stores the selection"
- "The Application page displays the section"
- "Users must add individual records"
- "The system validates each entry"

### ❌ AVOID (Technical Methods)
- `CheckWaiverOfSubro()` method calls
- `govStateQuote.HasWaiverOfSubrogation` properties
- `ValidateControl()` function references
- `lnkNew_Click` event handlers
- Technical property assignments

### Error Message Format
**"Missing Name"** - Always bold and quoted

### Confirmation Dialog Format  
"Are you sure you want to delete this coverage?" - Always quoted

---

## Cross-LOB Adaptation Examples

### Workers Compensation
- **Endorsements:** Waivers, Exclusions, Coverage Extensions
- **Application Module:** Named Individuals
- **Common Downstream:** Rating, Claims, Regulatory Compliance

### General Liability  
- **Endorsements:** Additional Insureds, Blanket Contractual, Professional Liability
- **Application Module:** Additional Interests, Contractual Liability
- **Common Downstream:** Rating, Claims, Certificate Generation

### Business Owner's Policy
- **Endorsements:** Equipment Breakdown, Cyber Liability, Employment Practices
- **Application Module:** Coverage Extensions, Equipment Schedules  
- **Common Downstream:** Rating, Claims, Property Valuation

---

## Quality Standards

### Mandatory Requirements
- ✅ Field Specifications section unchanged from original format
- ✅ Business-friendly language throughout
- ✅ Source code evidence for all statements
- ✅ Hierarchical numbering (X.1, X.2, X.21, X.311)
- ✅ New source code format with separate lines

### Data Exclusion Requirements
- ❌ Exclude `IgnoreForLists="Yes"` dropdown options
- ❌ No static configuration data without user access verification
- ❌ No technical method calls in business descriptions
- ❌ No assumptions without source code evidence

---

**End of Template**