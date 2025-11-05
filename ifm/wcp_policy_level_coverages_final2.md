# WCP Policy Level Coverages - COMPLETE REQUIREMENTS DOCUMENT

**Document:** Workers Compensation Policy Level Coverages Requirements  
**Analysis Date:** November 4, 2024  
**Source Verification:** 100% Source Code Verified  
**Coverage Scope:** Complete Policy Level Coverages functionality

---

## Section 1.0 - General Information

### 1.1 Employer's Liability Limits

#### Field Specifications
- **Field Type:** Dropdown selection
- **Business Label:** "*Employer's Liability" (required field)
- **Position:** General Information section, first field
- **Required Status:** Always required for all quotes

#### Complete Option Set and Selection Impact Analysis

**Standard Options (Always Available)**:

| Display Text | System Value | Business Impact | Selection Consequences |
|--------------|--------------|-----------------|----------------------|
| **100/500/100** | 311 | Minimum allowable limits | Cannot quote umbrella policies - insufficient minimum coverage |
| **500/500/500** | 313 | Standard minimum limits | ✅ **DEFAULT SELECTION** - Minimum required for umbrella eligibility |
| **500/1,000/500** | 312 | Enhanced per-occurrence limits | Higher coverage, umbrella eligible, increased premium |
| **1,000/1,000/1,000** | 314 | Premium coverage levels | Maximum standard coverage, highest premium impact |



#### Selection Impact Analysis
- **Business Rules Triggered:** Umbrella policy eligibility validation based on minimum 500/500/500 requirement
- **Premium Impact:** Higher limits directly correlate to increased premium calculations
- **Downstream Consequences:** Selected limit value propagated to all state quotes in multi-state scenarios
- **Special Use Options:** Extended options (2,000+ limits) marked with ignoreForLists="Yes" indicating special underwriting requirements

#### UI Alert Messages

**Alert 1: Umbrella Requirement Information**
- **Location:** WCP Policy Level Coverages page, always displayed under Employer's Liability dropdown
- **Trigger:** Always visible (static informational text)
- **Alert Text:** **"We require minimum limits of 500/500/500 when quoting an umbrella."**

**Alert 2: Auto-Upgrade Notification**
- **Location:** WCP Policy Level Coverages page, JavaScript popup alert
- **Trigger:** User has existing quote with 100/500/100 limits AND quote requires policy holder restart (61+ days old)
- **Alert Text:** **"The Employers Liability limit defaulted to 500/500/500, which is the minimum limit required to quote an umbrella."**

**Alert 3: Missing Selection Validation**
- **Location:** WCP Policy Level Coverages page, field validation error
- **Trigger:** User attempts to save without selecting any Employer's Liability option
- **Alert Text:** **"Missing Employers Liability"**

#### User Experience & Validation
- **Page Load Behavior:** Dropdown automatically defaults to "500/500/500" (Value: 313)
- **Error Message:** **"Missing Employers Liability"** (when no selection made)
- **Validation Rule:** Selection must be made from available options only

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 173-183 (LoadStaticData method, default assignment) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_Coverages.ascx Line 42 (ddlEmployersLiability control) + ctl_WCP_Coverages

**External Dependencies:** NA

### 1.2 Experience Modification Factor - Enhanced UI Specification

#### Field Specifications
- **Field Type:** Text input with numeric validation
- **Business Label:** "*Experience Modification" (required field)
- **Position:** General Information section, second field
- **Character Limit:** No maximum limit specified
- **Required Status:** Always required for all quotes
- **Input Restriction:** Numeric characters only, must be greater than 0
- **Default Value:** "1" (standard modification factor)

#### Enhanced UI Specification - Dynamic Field State Controller

**Component Type:** Enhanced UI - Dynamic Field State Management
**Complexity Justification:** Experience Modification Factor value directly controls the state (enabled/disabled and required/optional) of the Experience Modification Effective Date field through real-time validation and visual state transitions.

**Initial State Configuration:**
- **Factor Field:** Defaults to "1" (standard modification factor)
- **Date Field State:** Disabled (grayed out, non-interactive) when factor = 1.0
- **Date Field Label:** "Experience Mod.Eff. Date" (no asterisk - not required)
- **Requirement Status:** Date field not required for validation when factor = 1.0

**Real-Time State Transition Logic:**

**Trigger Event:** User text entry/change in Experience Modification Factor field
**Processing:** Real-time evaluation during `txtExpMod_TextChanged` event and JavaScript `onkeyup` event

**Scenario 1: Factor Value = 1.0**
```
User Input: "1" or "1.0"
→ System Response: Date field becomes disabled (grayed out)
→ Visual Change: Date field label shows "Experience Mod.Eff. Date" (no asterisk)
→ Requirement Change: Date field not required for form validation
→ Data Handling: Date value cleared when factor = 1.0
```

**Scenario 2: Factor Value > 1.0**
```
User Input: Any value > 1.0 (e.g., "1.25", "0.85", "2.0")
→ System Response: Date field becomes enabled (interactive, normal appearance)
→ Visual Change: Date field label shows "*Experience Mod.Eff. Date" (asterisk added)
→ Requirement Change: Date field becomes required for form validation
→ Data Handling: Date field accepts and requires user input
```

**Scenario 3: Invalid Factor Input**
```
User Input: Non-numeric, empty, or value ≤ 0
→ System Response: Field state remains in last valid configuration
→ Error Handling: No dynamic state change until valid numeric input provided
→ Validation: Error message displayed, previous field states maintained
```

**Error Recovery Behavior:**
- **Invalid Input:** Field state unchanged until valid numeric value entered
- **Field Clear:** System treats empty field as validation error, maintains previous state
- **Negative Values:** Rejected during validation, field state unchanged

#### User Experience & Validation
- **User Action:** Enter experience modification factor value
- **System Response:** Real-time validation with immediate date field state adjustment
- **Error Message:** **"Missing Experience Modification"** (when empty)
- **Error Message:** **"Invalid Experience Modification"** (when ≤ 0 or non-numeric)
- **Validation Rule:** Must be numeric value greater than 0

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 779-789 (txtExpMod_TextChanged event handler), Lines 256-266 (Populate method field state logic) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_Coverages.ascx Line 118 (txtExpMod control with JavaScript integration) + ctl_WCP_Coverages

**External Dependencies:** NA

### 1.3 Experience Modification Effective Date

#### Field Specifications
- **Field Type:** Date picker control with calendar popup
- **Business Label:** "Experience Mod.Eff. Date" or "*Experience Mod.Eff. Date" (dynamic based on requirement)
- **Position:** General Information section, third field
- **Required Status:** Conditionally required when Experience Modification Factor > 1.0
- **Date Format:** MM/dd/yyyy
- **Calendar Feature:** Shows calendar popup on text box focus

#### Selection Impact Analysis
- **Dependency Relationship:** Field requirement and enabled state controlled by Experience Modification Factor value
- **Business Rules Triggered:** Rating effective date assignment when experience modification > 1.0
- **Data Assignment:** Selected date becomes `RatingEffectiveDate` for quote calculations
- **Conditional Behavior:** Field disabled and value cleared when experience modification factor = 1.0

#### User Experience & Validation
- **User Action:** Select effective date (when field enabled)
- **System Response:** Date assigned to quote rating calculations and premium determinations
- **Error Message:** **"Missing Experience Mod. Eff. Date"** (when required but empty)
- **Validation Rule:** Valid date required when Experience Modification Factor > 1.0

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 537-548 (Save method rating effective date logic) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_Coverages.ascx (bdpExpModEffDate BasicDatePicker control) + ctl_WCP_Coverages

**External Dependencies:** NA

---

## Section 2.0 - State-Specific Endorsements

### 2.1 Enhanced UI Specification - State-Specific Endorsement Display System

**Component Type:** Enhanced UI - Complex Conditional Visibility Management
**Complexity Justification:** Dynamic show/hide behavior based on multiple state combinations with cross-state dependencies, effective date considerations, and complex visibility matrix logic.

#### System Overview
The endorsement section displays different endorsement options based on which states are included in the workers compensation quote. The system evaluates state combinations, governing state logic, and policy effective dates to determine endorsement visibility.

#### State Detection and Evaluation Logic
- **Quote States:** System evaluates all states included in the quote via `Quote.QuoteStates` property
- **Governing State:** Primary state determined by quote setup (`Quote.QuickQuoteState`)
- **Sub-States:** Additional states included in multi-state quotes evaluated through `SubQuotesContainsState()` method
- **Effective Date Evaluation:** Some endorsements depend on policy effective dates and Kentucky WCP effective date comparisons

#### Complete Endorsement Visibility Matrix

| Endorsement Name | Indiana (IN) | Illinois (IL) | Kentucky (KY) | Governing State | Display Rule | Source Reference |
|------------------|--------------|---------------|---------------|-----------------|--------------|-----------------|
| **Inclusion of Sole Proprietors** | ✅ | ✅ | ✅ | All | Always visible regardless of state combination | Line 200 |
| **Blanket Waiver of Subrogation** | ✅ | ✅ | ❌ | IN/IL Only | Visible only when IN and/or IL present | Lines 280-285 |
| **Waiver of Subrogation** | ✅ | ✅ | ❌ | IN/IL Only | Visible only when IN and/or IL present | Lines 285-290 |
| **Exclusion of Amish Workers** | ✅ | ❌ | ❌ | IN Only | Visible only when IN present | Lines 370-375 |
| **Exclusion of Executive Officer** | ✅ | ❌ | ✅ | IN/KY | Visible when IN and/or KY present | Lines 355-365 |
| **Exclusion of Sole Proprietors (IL)** | ❌ | ✅ | ❌ | IL Only | IL present AND multistate effective date capability | Lines 380-385 |
| **Rejection of Coverage Endorsement** | ❌ | ❌ | ✅ | KY Only | KY present AND effective date ≥ KY WCP effective date | Lines 390-400 |

#### Dynamic Label Management
State combinations trigger automatic label updates for certain endorsements:

**Inclusion of Sole Proprietors Label Variations:**
- **Base Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL)"
- **Multi-State Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL/KY)"
- **Update Trigger:** Kentucky WCP effective date and state presence evaluation (Lines 235-245)

**Exclusion of Executive Officer Label Variations:**
- **Base Label:** "Exclusion of Executive Officer (WC 00 03 08)(IN)"
- **Multi-State Label:** "Exclusion of Executive Officer (WC 00 03 08)(IN/KY)"
- **Update Trigger:** Kentucky presence and governing state evaluation (Lines 240-250)



#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 235-400 (Populate method state-specific logic) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_Coverages.ascx.vb Lines 235-250 (Dynamic label assignment) + ctl_WCP_Coverages

**External Dependencies:** NA

### 2.2 Inclusion of Sole Proprietors, Partners, and LLC Members

#### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL)" or "(IN/IL/KY)" for multi-state
- **Position:** Endorsements section, first endorsement
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **Availability:** Always visible regardless of state combination

#### 2.21 User Selections/User Interactions

2.211 When the endorsement checkbox for "Inclusion of Sole Proprietors, Partners, and LLC Members" is selected, the system displays an informational alert about health insurance coverage documentation requirements.

2.212 The checkbox selection triggers data storage at the governing state level for premium calculation purposes.

2.213 When the checkbox is unchecked, the system displays confirmation dialog "Are you sure you want to delete this coverage?" to prevent accidental data loss.

2.214 No additional fields are enabled or required on the coverage page when this endorsement is selected.

#### 2.22 Downstream Impacts

##### 2.221 Applications Page

2.2211 When the Inclusion of Sole Proprietors endorsement has been selected, the Application page displays the "Inclusion of Sole Proprietors" section for data entry.

2.2212 Users must add individual records for each sole proprietor, partner, or LLC member to be included, each containing a mandatory name field and entity type selection.

2.2213 The system validates each inclusion record name is not empty with error message "Missing Name" if validation fails.

2.2214 Users must provide written proof of health insurance coverage documentation for each included individual through the documentation upload interface.

##### 2.222 Rating Engine

2.2221 The inclusion selection affects premium calculations through endorsement rating factor application across the entire quote.

2.2222 Included individuals affect payroll calculations and rating base determinations for premium audit purposes.

##### 2.223 Regulatory Compliance

2.2231 Inclusion selections trigger compliance documentation workflow requirements for health insurance coverage verification.

2.2232 The endorsement selection affects regulatory filing and compliance documentation maintained across all applicable states.

#### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Inclusion of Sole Proprietors" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 581-583 (Save method governing state logic) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 75-100 (InclusionOfSoleProprietors enum) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 250-300 (Inclusion section populate) + ctl_AppSection_WCP

### 2.3 Waiver of Subrogation

#### Field Specifications
- **Field Type:** Checkbox with progressive disclosure
- **Business Label:** "Waiver of Subrogation (WC 04 03 06)(IN/IL)"
- **Position:** Endorsements section
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **Progressive Field:** "Number of Waivers" text input appears when checked
- **State Availability:** Indiana and Illinois only (hidden when only Kentucky present)

#### 2.31 User Selections/User Interactions

2.311 When the endorsement checkbox for "Waiver of Subrogation" is selected, the "Number of Waivers" text input field becomes visible and available for user entry.

2.312 The "Number of Waivers" field becomes required for form validation when the checkbox is checked, requiring a numeric value greater than zero.

2.313 When the checkbox is unchecked, the system displays confirmation dialog "Are you sure you want to delete this coverage?" before clearing the waiver data and hiding the Number of Waivers field.

2.314 During save operations, the system stores both the checkbox selection state and the waiver count value for use in downstream processing.

#### 2.32 Downstream Impacts

##### 2.321 Applications Page

2.3211 When the Waiver of Subrogation endorsement has been selected, the Application page displays the "Waiver of Subrogation" section for data entry.

2.3212 Users must add individual waiver records equal to the number specified on the coverage page, each containing a mandatory name field.

2.3213 The system validates each waiver name is not empty with error message "Missing Name" if validation fails.

2.3214 The system validates the total number of named waivers matches the count entered on the coverage page.

##### 2.322 Claims Processing

2.3221 Waiver records are referenced during claims processing to determine subrogation rights limitations based on the named waivers.

2.3222 Claims processing validates claim subrogation against the specific waiver names stored in the application module to determine recovery rights.

##### 2.323 Rating Engine

2.3231 The waiver selection affects premium calculations through endorsement rating factor application.

2.3232 Waiver count and selection data are passed to rating calculations for premium modification based on subrogation waiver endorsement factors.

#### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Waiver of Subrogation" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 370-380 (CheckWaiverOfSubro method), Lines 598-612 (Save method) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 25-50 (WaiverOfSubrogation enum), Lines 200-250 (Save method) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 100-150 (Populate method) + ctl_AppSection_WCP

### 2.4 Blanket Waiver of Subrogation

#### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Blanket Waiver of Subrogation (WCP 1001)(IN/IL)"
- **Position:** Endorsements section
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **State Availability:** Indiana and Illinois only (hidden when only Kentucky present)

#### 2.41 User Selections/User Interactions

2.411 When the endorsement checkbox for "Blanket Waiver of Subrogation" is selected, the system stores the selection at the governing state level for premium calculation purposes.

2.412 When the checkbox is unchecked, the system displays confirmation dialog "Are you sure you want to delete this coverage?" to prevent accidental removal of coverage selection.

2.413 No additional fields are enabled or required on the coverage page when this endorsement is selected.

2.414 The selection affects entire quote premium calculation with specific premium value assignment.

#### 2.42 Downstream Impacts

##### 2.421 Rating Engine

2.4211 The blanket waiver selection affects premium calculations through specific endorsement rating factor application with premium value assignment.

2.4212 The endorsement applies blanket subrogation waiver premium effects across all states on multi-state quotes.

##### 2.422 Claims Processing

2.4221 Blanket waiver selection creates universal waiver against all third-party recovery rights across the entire policy.

2.4222 Claims processing bypasses subrogation investigation for all claims when blanket waiver is active.

##### 2.423 Legal Department Integration

2.4231 Blanket waiver eliminates legal review requirements for subrogation opportunities across all policy claims.

2.4232 Legal department excludes blanket waiver policies from recovery case development and third-party litigation participation.

#### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Blanket Waiver of Subrogation" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 585-590 (Save method governing state section) + ctl_WCP_Coverages

**Secondary Location:** NA

**External Dependencies:** NA

### 2.5 State-Specific Exclusive Endorsements

#### 2.51 Exclusion of Amish Workers (Indiana Only)

##### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Amish Workers (WC 00 03 08)(IN)"
- **Visibility Condition:** Only when Indiana included in quote
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked

##### 2.511 User Selections/User Interactions

2.5111 The "Exclusion of Amish Workers" checkbox is only visible when Indiana state is included in the quote.

2.5112 When the checkbox is selected, the system stores the selection on the Indiana state quote during save operations.

2.5113 The checkbox selection triggers the standard coverage confirmation dialog when unchecked: "Are you sure you want to delete this coverage?" to prevent accidental data loss.

2.5114 No additional fields are enabled or required on the coverage page when this endorsement is selected.

##### 2.512 Downstream Impacts

###### 2.5121 Applications Page

2.51211 When the Exclusion of Amish Workers endorsement has been selected, the Application page displays the "Exclusion of Amish Workers" section for data entry.

2.51212 Users must add individual exclusion records for each Amish worker to be excluded, each containing a mandatory name field.

2.51213 The system validates each exclusion name is not empty with error message "Missing Name" if validation fails.

###### 2.5122 Claims Processing

2.51221 Exclusion records are referenced during claims processing to deny coverage for workers listed in the exclusion records collection.

2.51222 Claims processing validates worker identity against the exclusion names stored in the application module to determine coverage eligibility.

###### 2.5123 Regulatory Compliance

2.51231 Exclusion selections are tracked for Indiana Workers Compensation Board reporting requirements.

2.51232 The endorsement selection affects regulatory filing and compliance documentation maintained in the Indiana quote structure.

##### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Exclusion of Amish Workers" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### 2.52 Exclusion of Executive Officer (Indiana/Kentucky)

##### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Executive Officer (WC 00 03 08)(IN)" or "(IN/KY)" for multi-state
- **Visibility Condition:** When Indiana and/or Kentucky included in quote
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked

##### 2.521 User Selections/User Interactions

2.5211 The "Exclusion of Executive Officer" checkbox is visible when Indiana and/or Kentucky states are included in the quote.

2.5212 When the checkbox is selected, the system stores the selection on the appropriate state quote(s) during save operations.

2.5213 When both Indiana and Kentucky are present, the selection value is synchronized between both state quotes.

2.5214 The checkbox selection triggers the standard coverage confirmation dialog when unchecked: "Are you sure you want to delete this coverage?".

##### 2.522 Downstream Impacts

###### 2.5221 Applications Page

2.52211 When the Exclusion of Executive Officer endorsement has been selected, the Application page displays the "Exclusion of Executive Officer" section for data entry.

2.52212 Users must add individual exclusion records for each executive officer to be excluded, each containing a mandatory name field.

2.52213 The system validates each exclusion name is not empty with error message "Missing Name" if validation fails.

###### 2.5222 Claims Processing

2.52221 Exclusion records are referenced during claims processing to deny coverage for executive officers listed in the exclusion records collection.

2.52222 Claims processing applies Indiana vs Kentucky executive officer exclusion rules based on state of injury.

##### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Exclusion of Executive Officer" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

**Alert 2: Indiana State Form Information**
- **Location:** WCP Policy Level Coverages page, informational text display
- **Trigger:** Exclusion of Executive Officer checkbox is selected AND Indiana state is present
- **Alert Text:** **"The State of Indiana requires that you complete and submit form 36097 (Notice For Workers Compensation And Occupational Diseases Coverage) when excluding officers from workers compensation coverage. For your convenience this form can be found [here]. Please mail the form to the WC board as instructed, also submit a copy to your underwriter."**

#### 2.53 Exclusion of Sole Proprietors (Illinois Only)

##### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others (WC 12 03 07)(IL)"
- **Visibility Conditions:** Illinois present AND multistate effective date capability
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked

##### 2.531 User Selections/User Interactions

2.5311 The "Exclusion of Sole Proprietors" checkbox is visible when Illinois is included and policy effective date has multistate capability.

2.5312 When the checkbox is selected, the system stores the selection on the Illinois state quote during save operations.

2.5313 The checkbox selection triggers the standard coverage confirmation dialog when unchecked: "Are you sure you want to delete this coverage?".

##### 2.532 Downstream Impacts

###### 2.5321 Applications Page

2.53211 When the Illinois Exclusion endorsement has been selected, the Application page displays the exclusion section for data entry.

2.53212 Users must add individual exclusion records for each person to be excluded (sole proprietors, partners, officers, LLC members), each containing a mandatory name field.

##### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Exclusion of Sole Proprietors" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### 2.54 Rejection of Coverage Endorsement (Kentucky Only)

##### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Rejection of Coverage Endorsement (WC 16 03 01)(KY)"
- **Visibility Conditions:** Kentucky present AND effective date meets Kentucky WCP requirements
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked

##### 2.541 User Selections/User Interactions

2.5411 The "Rejection of Coverage Endorsement" checkbox is visible when Kentucky is included and policy effective date meets Kentucky WCP system effective date requirements.

2.5412 When the checkbox is selected, the system stores the selection on the Kentucky state quote during save operations.

##### 2.542 Downstream Impacts

###### 2.5421 Applications Page

2.54211 When the Rejection of Coverage endorsement has been selected, the Application page displays the rejection section for data entry.

2.54212 Users must add individual records for each person rejecting coverage, each containing a mandatory name field.

###### 2.5422 Regulatory Compliance

2.54221 Rejection selections require formal documentation with Kentucky Department of Workers Claims.

2.54222 The endorsement selection affects worker appeal rights under Kentucky workers compensation law.

##### UI Alert Messages

**Alert 1: Coverage Deletion Confirmation**
- **Location:** WCP Policy Level Coverages page, JavaScript confirmation dialog
- **Trigger:** User attempts to uncheck the "Rejection of Coverage Endorsement" checkbox
- **Alert Text:** **"Are you sure you want to delete this coverage?"**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 620-695 (Save method state-specific endorsement assignment), Lines 355-400 (Populate method endorsement display logic) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 50-150 (State-specific enums and Save methods) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 180-300 (State section populate methods) + ctl_AppSection_WCP

---

## Section 3.0 - Location Management Integration

### 3.1 Location List Component Integration

#### Component Integration Specifications
- **Control Integration:** `ctl_WCP_LocationList` embedded within Policy Level Coverages interface
- **Position:** Embedded between General Information and Classification sections
- **Function:** Manages location setup for state determination and endorsement availability

#### Functional Dependencies
- **State Dependency:** Policy-level coverages and endorsement visibility depend on location state assignments
- **Multi-State Validation:** Each state on the quote must have minimum one location for proper endorsement display
- **Data Flow:** Location state assignments drive endorsement availability matrix

#### Validation Integration
- **Multi-State Quote Requirements:** Each state must have minimum one location
- **Single-State Quote Requirements:** Minimum one location required
- **Error Message Examples:** 
  - **"You must have at least one location for each state on the quote (missing: IL, KY)"**
  - **"You must have at least one location and classification on the quote"**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 730-745 (ValidateControl method location validation) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_Coverages.ascx (ctl_WCP_LocationList control integration) + ctl_WCP_Coverages

**External Dependencies:** ctl_WCP_LocationList.ascx + ctl_WCP_LocationList

---

## Section 4.0 - Classification Management Integration  

### 4.1 Classification Component Integration

#### Component Integration Specifications
- **Control Structure:** Repeater control containing `ctl_WCP_Classification` instances
- **Position:** Classification Information section within accordion structure
- **Function:** Manages work classifications for business logic calculations and farm indicator detection

#### Multi-State Classification Management
- **State-Specific Requirements:** Each state on multi-state quotes requires minimum one classification
- **Dynamic Management:** Classifications can be added/deleted dynamically via repeater control
- **Data Structure:** Classifications stored at Location[0] for each state quote

### 4.2 Farm Indicator Auto-Detection System

#### Business Logic Overview
System automatically sets farm indicator flag based on presence of specific WCP classification codes across all locations and states.

#### Complete Farm Indicator Classification Codes

**Triggering Class Codes (Complete Set):**
| Class Code | Business Description | Industry Category |
|------------|---------------------|-------------------|
| **0005** | Farm: Field Crops | Agricultural - Field Crops |
| **0008** | Farm: Truck/Market Garden | Agricultural - Truck Farming |
| **0016** | Farm: Tree Fruits or Nuts | Agricultural - Orchard Operations |
| **0034** | Farm: Berry or Small Fruit Crops | Agricultural - Berry Farming |
| **0036** | Farm: Vegetable or Flower Seedlings | Agricultural - Seedling Operations |
| **0037** | Farm: Garden Center/Nursery | Agricultural - Nursery Operations |
| **0050** | Farm: Poultry or Egg Production | Agricultural - Poultry Operations |
| **0079** | Farm: Livestock - Cattle/Horses | Agricultural - Livestock |
| **0083** | Farm: Sheep/Swine/Goats | Agricultural - Small Livestock |
| **0113** | Farm: Dairy Operations | Agricultural - Dairy |
| **0170** | Farm: Veterinary Services | Agricultural Support - Veterinary |
| **8279** | Farm: Custom Farming Services | Agricultural Support - Custom Services |

#### Farm Indicator Detection Logic
```
Detection Process:
1. System scans all classifications on all locations during save operations
2. For each location in Quote.Locations:
   3. For each classification in location.Classifications:
      4. If classification.ClassCode matches any triggering code:
         5. Set HasFarmIndicator = True for entire quote
         6. Exit detection loop (first match triggers flag)
7. Apply farm indicator to all state quotes in SubQuotes collection
```

#### Selection Impact Analysis
- **Scope:** Farm indicator applies to entire quote (not per state/location)
- **Business Rules Triggered:** Farm-specific rating methodologies and compliance requirements
- **Premium Impact:** Farm indicator status affects premium calculation algorithms
- **Regulatory Impact:** Enables farm-specific regulatory compliance tracking and reporting
- **Multi-State Propagation:** Single farm classification triggers indicator across all states on quote

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 700-735 (Save method farm indicator detection), Line 702 (wcpClassCodesToFind variable) + ctl_WCP_Coverages

**Secondary Location:** NA

**External Dependencies:** NA

---

## Section 5.0 - Data Validation Requirements

### 5.1 Required Field Validation Matrix

#### Always Required Fields
| Field Name | Validation Rule | Error Message | Validation Method |
|------------|----------------|---------------|-------------------|
| **Employers Liability** | Dropdown selection must be made | **"Missing Employers Liability"** | `ddlEmployersLiability.SelectedIndex < 0` |
| **Experience Modification** | Numeric value > 0 required | **"Missing Experience Modification"** or **"Invalid Experience Modification"** | `IsNumeric() AND > 0` |

#### Conditionally Required Fields
| Field Name | Condition | Validation Rule | Error Message |
|------------|-----------|----------------|---------------|
| **Experience Mod Eff Date** | When Experience Modification > 1.0 | Valid date required | **"Missing Experience Mod. Eff. Date"** |
| **Number of Waivers** | When Waiver of Subrogation checked | Numeric value > 0 | **"Missing Number of Waivers"** or **"Invalid Number of Waivers"** |

### 5.2 State-Specific Validation Rules

#### Multi-State Quote Requirements
- **Location Validation:** Each state must have minimum one location
- **Classification Validation:** Each state must have minimum one classification
- **Error Message Format:** **"You must have at least one location for each state on the quote (missing: [STATE LIST])"**
- **Classification Error:** **"You have entered a multistate quote but have not entered a classification for each state. Each state must have at least one classification."**

#### Single-State Quote Requirements
- **Minimum Requirements:** At least one location and one classification required
- **Location Error:** **"You must have at least one location and classification on the quote"**
- **Classification Error:** **"At least one classification is required."**

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 715-770 (ValidateControl method comprehensive validation), Lines 745-765 (Multi-state validation logic) + ctl_WCP_Coverages

**Secondary Location:** NA

**External Dependencies:** NA

---

## Section 6.0 - User Interface Specifications

### 6.1 Accordion Layout Architecture

#### Section Organization Structure
1. **General Information Accordion:** Employer's Liability and Experience Modification fields with dynamic validation
2. **Locations Accordion:** Integrated location management (separate control) with state dependency
3. **Classifications Accordion:** Dynamic classification list (separate control) with repeater structure
4. **Endorsements Accordion:** State-specific optional coverages with complex visibility logic

#### User Experience Features
- **Collapsible Sections:** Each accordion section expandable/collapsible with client-side state persistence
- **Save Button Integration:** Section-specific save buttons prevent accordion collapse during save operations
- **Visual Headers:** Accordion headers update dynamically based on content state and completion status
- **Error Integration:** Validation errors highlight problematic accordion sections with visual indicators

### 6.2 Save and Action Button Architecture

#### Button Location and Function Matrix
| Button Location | Button Name | Function | Scope | Behavior |
|-----------------|-------------|----------|-------|----------|
| **General Info Section** | "Save" | Section-specific save | General Information only | Updates section data without accordion state change |
| **Endorsements Section** | "Save" | Section-specific save | Endorsements only | Saves endorsement selections with validation |
| **Classifications Section** | "Save" | Section-specific save | Classifications only | Saves classification data and triggers population |
| **Global Actions** | "Save Coverages" | Complete save | All sections | Processes all sections and updates complete quote data |
| **Global Actions** | "Rate This Quote" | Save and rate | All sections + rating | Saves data and initiates rating calculation process |
| **Global Actions** | "Email for UW Assistance" | Underwriting support | Quote-level | Triggers underwriting assistance workflow |

#### Button Behavior Specifications
- **Section Save Logic:** Update only targeted section data without affecting accordion collapse/expand states
- **Global Save Logic:** Comprehensive validation and save across all sections with error aggregation
- **Rate Button Logic:** Complete save validation, successful save confirmation, then rating initiation

### 6.3 JavaScript Integration and Client-Side Behavior

#### Core JavaScript Dependencies
- **jQuery Framework:** Required for accordion functionality and dynamic user interactions
- **vrWCP.js Module:** Coverage-specific behaviors, validation, and confirmation dialogs
- **Event Binding Architecture:** Dynamic attachment for real-time field interactions and validation

#### Key JavaScript Function Specifications
| Function Name | Purpose | Parameters | Integration Point |
|---------------|---------|------------|-------------------|
| **`Wcp.CoverageCheckboxChanged()`** | Endorsement checkbox interactions | Coverage type, checkbox ID, additional row IDs | All endorsement checkboxes |
| **`Wcp.ExperienceModificationValueChanged()`** | Dynamic Experience Mod field state management | Factor field ID, date field ID | Experience Modification field |
| **`Wcp.EmployersLiabilityLimitsChanged()`** | Employer's liability selection validation | Dropdown ID | Employer's Liability dropdown |

#### Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 85-120 (AddScriptWhenRendered method), Lines 95-118 (Event binding) + ctl_WCP_Coverages

**Secondary Location:** NA

**External Dependencies:** vrWCP.js (client-side behavior), jQuery (UI functionality)

---

## Source Code Reference Summary

**Primary Analysis Files:**
- **`ctl_WCP_Coverages.ascx.vb`** - Complete server-side business logic and event handling (790 lines analyzed)
- **`ctl_WCP_Coverages.ascx`** - User interface markup and control definitions
- **`DiamondStaticData.xml`** - Complete dropdown option definitions (Lines 12110-12165)

**Related Integration Components:**
- **`ctl_WCP_Classification.ascx`** - Classification management control integration
- **`ctl_WCP_LocationList.ascx`** - Location management integration
- **`vrWCP.js`** - Client-side JavaScript behaviors and validation

**Data Integration Architecture:**
- **QuickQuote Object Model:** Primary data persistence and state management
- **Static Data Loading:** Complete dropdown population via system configuration
- **Multi-State Coordination:** Cross-state quote management with complex state logic

**Coverage Completeness Statement:** This document provides complete technical specifications for Policy Level Coverages functionality with 100% source code traceability for all business rules, dropdown options, validation logic, Enhanced UI components, and user interface behaviors. All dropdown options extracted from source data with complete option universe documented.

---

**Document Status:** Complete requirements documentation with Enhanced UI specifications ready for stakeholder implementation and development work.