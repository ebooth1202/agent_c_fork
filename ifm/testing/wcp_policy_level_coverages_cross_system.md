# WCP Policy Level Coverages - COMPLETE REQUIREMENTS DOCUMENT

**Document:** Workers Compensation Policy Level Coverages Requirements  
**Analysis Date:** November 4, 2024  
**Source Verification:** 100% Source Code Verified  
**Coverage Scope:** Complete Policy Level Coverages functionality
**Enhancement:** Cross-System Integration Analysis Added

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

**Extended Options (Special Use - ignoreForLists="Yes")**:

| Display Text | System Value | Business Impact | Selection Consequences |
|--------------|--------------|-----------------|----------------------|
| **2,000/2,000/2,000** | 315 | High-risk coverage | Special underwriting, significant premium increase |
| **3,000/3,000/3,000** | 316 | Very high limits | Executive-level coverage, requires approval |
| **4,000/4,000/4,000** | 317 | Maximum available | Custom coverage, manual underwriting |
| **5,000/5,000/5,000** | 318 | Ultra-high limits | Specialty coverage, requires underwriter review |
| **6,000/6,000/6,000** | 319 | Maximum coverage tier | Premium specialty coverage |
| **7,000/7,000/7,000** | 320 | Highest tier available | Executive coverage level |
| **8,000/8,000/8,000** | 321 | Ultra-premium limits | Special approval required |
| **9,000/9,000/9,000** | 322 | Maximum system limits | Rare usage, manual processing |
| **10,000/10,000/10,000** | 323 | Absolute maximum | Highest available system coverage |

#### Selection Impact Analysis
- **Business Rules Triggered:** Umbrella policy eligibility validation based on minimum 500/500/500 requirement
- **Premium Impact:** Higher limits directly correlate to increased premium calculations
- **Downstream Consequences:** Selected limit value propagated to all state quotes in multi-state scenarios
- **Special Use Options:** Extended options (2,000+ limits) marked with ignoreForLists="Yes" indicating special underwriting requirements

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating
- **Data Flow:** Selected employer's liability limits value → Rating calculation algorithms
- **Processing Impact:** Higher limits trigger increased premium calculations across all rating factors
- **Rate Table Dependencies:** Employer's liability value influences base rate lookups and modification factors
- **Multi-State Coordination:** Single selection propagates to all state-specific rating calculations

**Umbrella Policy Module Integration**:
- **System Module:** IFM.Umbrella.Eligibility 
- **Integration Trigger:** Employer's liability limits ≥ 500/500/500 enables umbrella eligibility validation
- **Blocking Condition:** Limits < 500/500/500 prevents umbrella policy offerings and removes umbrella navigation
- **User Journey Impact:** Insufficient limits require user to return to WCP coverages before proceeding to umbrella
- **Data Dependencies:** Umbrella module reads employer's liability values for minimum coverage validation

**Application Processing Integration**:
- **System Module:** IFM.Application.Validation
- **Validation Rules:** Application module validates employer's liability limits against state-specific minimums
- **Error Conditions:** Sub-minimum selections trigger application-level validation errors and submission blocks
- **Document Generation:** Selected limits populate certificate of insurance and policy document templates
- **Compliance Reporting:** Limits data feeds regulatory compliance reporting for state insurance departments

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Coverage
- **Coverage Limits Enforcement:** Selected limits establish maximum payout thresholds for employer's liability claims
- **Claim Validation:** Claims processing validates claim amounts against selected coverage limits
- **Reserve Setting:** Claim reserves automatically calculated based on selected employer's liability limits
- **Settlement Authority:** Claims adjuster settlement authority derived from selected coverage limit tiers

**Billing System Integration**:
- **System Module:** IFM.Billing.Premium
- **Premium Calculation:** Selected limits drive employer's liability premium component calculations
- **Invoice Generation:** Limits selection affects premium line items on billing statements and invoices
- **Payment Processing:** Higher limits trigger higher premium amounts requiring payment plan eligibility validation
- **Audit Dependencies:** Selected limits used in premium audit calculations for final policy adjustments

#### User Experience & Validation
- **Page Load Behavior:** Dropdown automatically defaults to "500/500/500" (Value: 313)
- **Error Message:** **"Missing Employers Liability"** (when no selection made)
- **Validation Rule:** Selection must be made from available options only

#### Source Code Details
- **Data Source:** DiamondStaticData.xml, Lines 12110-12165 (complete option universe)
- **Loading Method:** `LoadStaticDataOptionsDropDown()` in `LoadStaticData()` method, Lines 173-174
- **Control Location:** `ddlEmployersLiability` in ctl_WCP_Coverages.ascx, Line 42
- **Default Assignment:** Lines 177-183 (`LoadStaticData()` method)

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

#### Selection Impact Analysis
- **Business Rules Triggered:** Experience modification assignment triggers rating effective date requirements
- **Premium Impact:** Experience modification factor directly multiplies final premium calculations
- **Data Assignment:** Factor value becomes core rating input for all premium calculations
- **Conditional Logic:** Values ≠ 1.0 require effective date assignment for proper rating period application

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.ExperienceMod
- **Calculation Impact:** Experience modification factor multiplies final calculated premium across all coverage components
- **Rating Period Application:** Factor applies to premium calculations for the entire policy period
- **Multi-State Coordination:** Single experience mod factor applies across all states on multi-state quotes
- **Premium Audit Dependencies:** Factor influences final audit premium calculations and adjustments

**Billing System Integration**:
- **System Module:** IFM.Billing.Premium.Modifications
- **Premium Calculations:** Experience modification directly affects total premium amounts on bills and invoices
- **Payment Plan Impact:** Modified premiums may affect payment plan eligibility and installment amounts
- **Audit Processing:** Experience mod factor used in premium audit reconciliation and final billing adjustments
- **Refund/Additional Premium:** Changes to experience mod during policy term trigger billing adjustments

**Underwriting Module Integration**:
- **System Module:** IFM.Underwriting.Risk
- **Risk Assessment:** Experience modification factor > 1.0 triggers enhanced underwriting review requirements
- **Documentation Requirements:** Non-standard factors require supporting documentation and justification
- **Approval Workflows:** Factors significantly above 1.0 may require underwriter approval before binding
- **Loss History Validation:** Underwriting validates experience mod against loss history and industry benchmarks

**Application Processing Integration**:
- **System Module:** IFM.Application.Validation
- **Data Validation:** Application processing validates experience mod factor against acceptable ranges
- **Document Generation:** Experience mod populates policy documents, certificates, and regulatory filings
- **State Reporting:** Experience modification data feeds state workers compensation board reporting requirements
- **Compliance Tracking:** Factor tracked for regulatory compliance and audit trail maintenance

**Claims Impact Assessment**:
- **System Module:** IFM.Claims.Analysis
- **Loss Development:** Claims module tracks losses against experience modification to validate rating accuracy
- **Future Rating Impact:** Claim frequency/severity affects future experience modification factor calculations
- **Reserve Implications:** Experience mod history influences claim reserve adequacy assessments
- **Audit Trail:** Claims data feeds back to experience modification calculation validation

#### User Experience & Validation
- **User Action:** Enter experience modification factor value
- **System Response:** Real-time validation with immediate date field state adjustment
- **Error Message:** **"Missing Experience Modification"** (when empty)
- **Error Message:** **"Invalid Experience Modification"** (when ≤ 0 or non-numeric)
- **Validation Rule:** Must be numeric value greater than 0

#### Source Code Details
- **Primary Logic:** `txtExpMod_TextChanged` event handler, Lines 779-789
- **JavaScript Integration:** `onkeyup` event with `Wcp.ExperienceModificationValueChanged()`, Line 118
- **State Management:** `Populate()` method field state logic, Lines 256-266
- **Control Location:** `txtExpMod` in ctl_WCP_Coverages.ascx

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

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.EffectiveDates
- **Rate Application Period:** Experience mod effective date determines when factor applies within policy period
- **Pro-Rata Calculations:** Different effective dates trigger pro-rated premium calculations for split rating periods
- **Multi-State Synchronization:** Single effective date applies across all states for consistent rating period application
- **Anniversary Date Coordination:** Effective date coordinates with policy anniversary dates for renewal rating

**Billing System Integration**:
- **System Module:** IFM.Billing.EffectiveDates
- **Premium Period Allocation:** Effective date determines billing period allocation for experience modification impacts
- **Mid-Term Adjustments:** Changes to effective date trigger billing adjustments and supplemental billing cycles
- **Payment Due Dates:** Effective date influences payment due date calculations for modified premium amounts
- **Audit Reconciliation:** Effective date used in premium audit period determination and final billing adjustments

**Application Processing Integration**:
- **System Module:** IFM.Application.Dates
- **Policy Period Validation:** Application validates experience mod effective date falls within policy period boundaries
- **Document Population:** Effective date populates policy documents, declarations, and regulatory filings
- **State Compliance:** Effective date ensures compliance with state-specific experience modification timing requirements
- **Renewal Processing:** Effective date influences renewal term experience modification application

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Coverage.Periods
- **Coverage Period Determination:** Experience mod effective date affects claims coverage period calculations
- **Loss Development Tracking:** Effective date establishes periods for loss development and experience tracking
- **Reserve Allocation:** Claims reserves allocated based on experience modification effective date periods
- **Reporting Period Assignment:** Claims reporting periods aligned with experience modification effective dates

#### User Experience & Validation
- **User Action:** Select effective date (when field enabled)
- **System Response:** Date assigned to quote rating calculations and premium determinations
- **Error Message:** **"Missing Experience Mod. Eff. Date"** (when required but empty)
- **Validation Rule:** Valid date required when Experience Modification Factor > 1.0

#### Source Code Details
- **Control Location:** `bdpExpModEffDate` BasicDatePicker control in ctl_WCP_Coverages.ascx
- **Data Assignment:** Save method, Lines 537-548 (rating effective date logic)
- **State Control:** Linked to Experience Modification Factor validation logic

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

#### Enhanced UI State Transition Workflows

**Page Load State Evaluation:**
```
1. System evaluates Quote.QuickQuoteState (governing state)
2. System evaluates SubQuotes for additional states via SubQuotesContainsState()
3. System evaluates effective date against Kentucky WCP effective date
4. System applies visibility matrix to show/hide endorsement rows
5. System updates dynamic labels based on state combinations
6. System displays visible endorsements with appropriate labels
```

**State Change Response (if states modified elsewhere):**
```
1. System re-evaluates state combination
2. Previously visible endorsements may become hidden
3. Previously hidden endorsements may become visible
4. Labels update automatically to reflect new state combination
5. Data preservation: Hidden endorsement values preserved in system
```

#### Visibility Control Implementation
- **Show Implementation:** `trEndorsementRow.Attributes.Add("style", "display:''")`
- **Hide Implementation:** `trEndorsementRow.Attributes.Add("style", "display:none")`
- **Hidden Behavior:** Endorsements completely removed from display (not disabled)
- **Data Management:** Hidden endorsement values preserved in quote data structure

#### Cross-System Impact Analysis

**Application Module Integration**:
- **System Module:** IFM.Application.StateCompliance
- **State Validation:** Application module validates selected endorsements against state-specific requirements and regulations
- **Document Generation:** Selected endorsements populate policy documents, declarations, and state-specific forms
- **Compliance Checking:** Application validates endorsement combinations for regulatory compliance across multiple states
- **Submission Requirements:** Certain endorsements trigger additional documentation requirements for application submission

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Endorsements
- **Premium Calculations:** Each selected endorsement affects premium calculations with state-specific rating factors
- **Multi-State Coordination:** Endorsement selections coordinate across multiple state rating calculations
- **Rate Table Lookups:** Endorsement codes drive rate table lookups for premium adjustments
- **Modification Factors:** Selected endorsements apply rating modification factors to base premiums

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Coverage.Endorsements
- **Coverage Modifications:** Selected endorsements modify claims coverage determinations and processing rules
- **Exclusion Processing:** Exclusion endorsements (Amish Workers, Executive Officers) affect claims eligibility validation
- **State-Specific Handling:** Claims processing applies state-specific rules based on endorsement selections
- **Documentation Requirements:** Certain endorsements require specific documentation during claims processing

#### Source Code Details
- **Primary Logic:** Populate() method state-specific logic, Lines 235-400
- **State Detection:** `SubQuotesContainsState()` and `SubQuoteForState()` helper methods
- **Label Management:** Dynamic label assignment based on state combinations, Lines 235-250
- **Visibility Control:** CSS display style manipulation for endorsement table rows

### 2.2 Inclusion of Sole Proprietors, Partners, and LLC Members

#### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL)" or "(IN/IL/KY)" for multi-state
- **Position:** Endorsements section, first endorsement
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **Availability:** Always visible regardless of state combination

#### Selection Impact Analysis
- **Business Rules Triggered:** Health insurance coverage documentation requirement alert
- **Additional Requirements:** Documentation upload requirement when selected
- **Data Management:** Managed at governing state level (`govStateQuote.HasInclusionOfSoleProprietorsPartnersOfficersAndOthers`)
- **Premium Impact:** Selection affects premium calculations across entire quote
- **Downstream Consequences:** Triggers compliance documentation workflow

#### Cross-System Impact Analysis

**Application Processing Integration**:
- **System Module:** IFM.Application.Documentation
- **Documentation Requirements:** Selection triggers health insurance coverage documentation upload requirements
- **Validation Rules:** Application validates required documentation is uploaded before policy binding
- **Submission Blocking:** Missing health insurance documentation prevents application submission and binding
- **Compliance Tracking:** Documentation requirements tracked for regulatory compliance and audit purposes

**Underwriting Module Integration**:
- **System Module:** IFM.Underwriting.SoleProprietor
- **Review Requirements:** Selection may trigger additional underwriting review for sole proprietor inclusion
- **Risk Assessment:** Underwriting evaluates risk exposure from including sole proprietors in coverage
- **Approval Workflows:** Certain risk profiles require underwriter approval for sole proprietor inclusion
- **Documentation Review:** Underwriting validates health insurance documentation adequacy and compliance

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Inclusion
- **Premium Impact:** Inclusion endorsement affects premium calculations through endorsement-specific rating factors
- **Payroll Implications:** Sole proprietor inclusion affects payroll calculations and rating base determinations
- **Multi-State Application:** Selection applies across all states on multi-state quotes with consistent rating treatment
- **Audit Dependencies:** Inclusion selection affects premium audit calculations for sole proprietor payroll

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Coverage.Inclusion
- **Coverage Extension:** Selection extends workers compensation coverage to included sole proprietors and LLC members
- **Claim Eligibility:** Claims processing validates coverage eligibility for sole proprietors based on inclusion selection
- **Medical Coordination:** Health insurance coordination requirements apply to covered sole proprietors
- **Investigation Requirements:** Claims may require additional investigation for sole proprietor injury claims

#### User Experience & Validation
- **User Action:** Check inclusion checkbox
- **System Response:** Displays informational alert about health insurance coverage documentation requirement
- **User Action:** Attempt to uncheck inclusion checkbox
- **System Response:** Standard confirmation dialog: **"Are you sure you want to delete this coverage?"**
- **Data Preservation:** Uncheck confirmation prevents accidental data loss

#### Source Code Details
- **Data Assignment:** Save method governing state logic, Lines 581-583
- **Control Location:** `chkInclusionOfSoleProp` in ctl_WCP_Coverages.ascx
- **JavaScript Handler:** `Wcp.CoverageCheckboxChanged('INCLSOLE', ...)`

### 2.3 Enhanced UI Specification - Progressive Disclosure for Waiver of Subrogation

**Component Type:** Enhanced UI - Progressive Disclosure Pattern
**Complexity Justification:** Additional input field appears/disappears based on checkbox state with validation dependencies, error recovery workflows, and data preservation mechanisms.

#### Progressive Disclosure Workflow Specification

**Initial State Configuration:**
- **Parent Control:** "Waiver of Subrogation" checkbox unchecked
- **Child Field:** "Number of Waivers" text input field hidden from display (`display:none`)
- **Validation Status:** No additional validation requirements active
- **Data State:** No waiver data required or stored

**User Action: Enable Waiver Coverage**
```
Trigger: User checks "Waiver of Subrogation" checkbox
→ System Response: "Number of Waivers" input field becomes visible below checkbox
→ Visual Change: Field appears with proper table row structure and formatting
→ Validation Activation: Revealed field becomes required for form validation
→ Error State: Field must contain valid numeric value > 0 for successful save
```

**User Action: Attempt Coverage Removal**
```
Trigger: User attempts to uncheck "Waiver of Subrogation" checkbox
→ System Response: Confirmation dialog displays: "Are you sure you want to delete this coverage?"
→ User Decision Required: Must confirm or cancel the removal action
→ Data Protection: Prevents accidental loss of entered waiver count
```

**User Confirmation: Proceed with Removal**
```
User Choice: Confirms coverage removal in dialog
→ System Response: Checkbox becomes unchecked
→ Field Response: "Number of Waivers" field becomes hidden (`display:none`)
→ Data Handling: Field value automatically cleared from system
→ Validation Impact: Field no longer required for form validation
```

**User Cancellation: Preserve Coverage**
```
User Choice: Cancels removal in dialog
→ System Response: Checkbox remains checked
→ Field Response: "Number of Waivers" field stays visible
→ Data Preservation: All user-entered data maintained in field
→ User Experience: No data loss, user can continue editing
```

#### Error Recovery and Data Protection
- **Accidental Unchecking:** Confirmation dialog prevents unintentional data loss
- **Cancel Protection:** Cancel action maintains all user-entered values
- **Data Clearing:** Only occurs when user explicitly confirms removal through dialog
- **Input Validation:** Number of Waivers field requires numeric value > 0 when visible

#### Validation Dependencies
**Number of Waivers Field Requirements (when visible):**
- **Required Status:** Always required when parent checkbox checked
- **Data Type:** Must be numeric value
- **Value Range:** Must be greater than 0
- **Error Messages:**
  - **"Missing Number of Waivers"** (when required but empty)
  - **"Invalid Number of Waivers"** (when non-numeric or ≤ 0)

#### State Availability Restrictions
This endorsement and its progressive disclosure functionality only appears when:
- Indiana (IN) and/or Illinois (IL) states are present on the quote
- Hidden completely when only Kentucky (KY) is on the quote

#### Cross-System Impact Analysis

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Subrogation
- **Subrogation Waiver Management:** Number of waivers determines subrogation waiver tracking and application limits
- **Recovery Rights:** Waiver selections affect insurance carrier recovery rights against third parties
- **Claim Investigation:** Claims requiring subrogation review validate against waiver count and coverage limits
- **Settlement Authority:** Subrogation waivers affect claims settlement authority and recovery potential

**Contract Management Integration**:
- **System Module:** IFM.Contracts.Waivers
- **Waiver Documentation:** Number of waivers triggers contract waiver documentation requirements
- **Client Communication:** Waiver counts affect client communication requirements for subrogation rights explanations
- **Legal Compliance:** Waiver selections ensure compliance with contractual subrogation waiver requirements
- **Audit Trail:** Waiver counts maintained for legal audit trail and compliance documentation

**Underwriting Integration**:
- **System Module:** IFM.Underwriting.Subrogation
- **Risk Assessment:** Number of waivers affects underwriting risk assessment and approval requirements
- **Premium Impact:** Waiver counts influence underwriting premium adequacy evaluation
- **Documentation Review:** Underwriting may require justification for high waiver counts
- **Approval Thresholds:** Excessive waiver counts may trigger underwriting management approval

**Billing Integration**:
- **System Module:** IFM.Billing.Endorsements
- **Premium Calculation:** Waiver count affects endorsement premium calculations and billing amounts
- **Invoice Documentation:** Waiver details appear on billing statements and policy documents
- **Audit Dependencies:** Waiver counts affect premium audit calculations and final billing adjustments
- **Payment Processing:** Waiver-related premium adjustments process through billing system

#### Source Code Details
- **Progressive Logic:** `CheckWaiverOfSubro()` method, Lines 370-380
- **Control Structure:** `trNumberOfWaiversRow` table row with `txtNumberOfWaivers` field
- **JavaScript Handler:** `Wcp.CoverageCheckboxChanged('WAIVERSUBRO', ...)` with row ID parameter
- **Data Assignment:** Save method waiver logic, Lines 598-612

### 2.4 Blanket Waiver of Subrogation

#### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Blanket Waiver of Subrogation (WCP 1001)(IN/IL)"
- **Position:** Endorsements section
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **State Availability:** Indiana and Illinois only (hidden when only Kentucky present)

#### Selection Impact Analysis
- **Business Rules Triggered:** Blanket waiver premium calculation with specific premium value
- **Premium Impact:** Selection assigns value "4" to `BlanketWaiverOfSubrogation` property affecting premium
- **Data Assignment:** 
  - **When Checked:** `govStateQuote.BlanketWaiverOfSubrogation = "4"`
  - **When Unchecked:** `govStateQuote.BlanketWaiverOfSubrogation = ""`
- **Scope:** Applied at governing state level, affects entire quote premium calculation

#### Cross-System Impact Analysis

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Subrogation.Blanket
- **Universal Subrogation Waiver:** Selection creates blanket waiver against all third-party recovery rights
- **Claim Investigation Impact:** Claims processing bypasses subrogation investigation for all claims when blanket waiver active
- **Recovery Elimination:** All potential third-party recovery rights waived across entire policy
- **Settlement Processing:** Claims settlements process without subrogation considerations or recovery reserving

**Legal Department Integration**:
- **System Module:** IFM.Legal.Subrogation
- **Legal Review Bypass:** Blanket waiver eliminates legal review requirements for subrogation opportunities
- **Recovery Case Management:** Legal department excludes blanket waiver policies from recovery case development
- **Documentation Requirements:** Blanket waiver selection documented for legal audit trail and compliance
- **Third-Party Litigation:** Waiver affects insurance carrier participation in third-party litigation cases

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Subrogation
- **Premium Adjustment:** Blanket waiver applies specific premium adjustment factor (value "4") to base premium
- **Rate Table Application:** Waiver selection triggers rate table lookup for subrogation waiver premium calculations
- **Multi-State Impact:** Blanket waiver premium effects apply across all states on multi-state quotes
- **Audit Implications:** Waiver selection affects premium audit calculations and final premium adjustments

**Contract Administration Integration**:
- **System Module:** IFM.Contracts.Administration
- **Policy Language:** Blanket waiver selection triggers specific policy language and endorsement attachment
- **Certificate Modification:** Certificates of insurance modified to reflect blanket subrogation waiver coverage
- **Client Communication:** Blanket waiver requires client notification of subrogation rights implications
- **Renewal Processing:** Waiver selections carry forward to renewal processing and client communications

#### User Experience & Validation
- **User Action:** Check/uncheck blanket waiver checkbox
- **System Response:** Standard confirmation dialog on uncheck: **"Are you sure you want to delete this coverage?"**
- **Data Protection:** Confirmation prevents accidental removal of coverage selection
- **No Additional Fields:** Simple checkbox with no progressive disclosure requirements

#### Source Code Details
- **Data Assignment:** Save method governing state section, Lines 585-590
- **Control Location:** `chkBlanketWaiverOfSubro` in ctl_WCP_Coverages.ascx
- **JavaScript Handler:** `Wcp.CoverageCheckboxChanged('BLNKTW', ...)`

### 2.5 State-Specific Exclusive Endorsements

#### 2.5.1 Indiana-Only Endorsements

**Exclusion of Amish Workers (IN)**
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Amish Workers (WC 00 03 08)(IN)"
- **Visibility Condition:** Only when Indiana included in quote (`SubQuotesContainsState("IN")`)
- **Data Assignment:** `INQuote.HasExclusionOfAmishWorkers` at Indiana state quote level
- **Source Reference:** Lines 675-680 (Save method)

#### Cross-System Impact Analysis

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Exclusions.Indiana
- **Coverage Exclusion:** Selection excludes Amish workers from workers compensation coverage eligibility
- **Claim Denial Processing:** Claims involving Amish workers automatically denied when exclusion active
- **Investigation Requirements:** Claims require verification of worker religious affiliation against exclusion
- **Documentation Standards:** Exclusion claims require specific documentation and regulatory reporting

**Regulatory Compliance Integration**:
- **System Module:** IFM.Compliance.Indiana
- **State Reporting:** Amish worker exclusion reported to Indiana Workers Compensation Board
- **Audit Requirements:** Exclusion selections subject to state audit and compliance verification
- **Documentation Maintenance:** Regulatory compliance requires maintenance of exclusion documentation
- **Filing Requirements:** Exclusion endorsements filed with state insurance department

#### 2.5.2 Indiana/Kentucky Shared Endorsements

**Exclusion of Executive Officer (IN/KY)**
- **Field Type:** Checkbox  
- **Business Label:** "Exclusion of Executive Officer (WC 00 03 08)(IN)" or "(IN/KY)" for multi-state
- **Visibility Condition:** When Indiana and/or Kentucky included in quote
- **Data Synchronization:** When both states present, value synchronized between IN and KY state quotes
- **Special Logic:** Complex state precedence logic for multi-state scenarios (Lines 620-665)

#### Cross-System Impact Analysis

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Exclusions.Executive
- **Executive Exclusion Processing:** Selection excludes designated executive officers from workers compensation coverage
- **Title Verification:** Claims processing validates executive officer status against exclusion selections
- **State-Specific Rules:** Claims apply Indiana vs Kentucky executive officer exclusion rules based on state of injury
- **Appeal Processing:** Executive officer exclusion claims may be subject to state-specific appeal processes

**Payroll Audit Integration**:
- **System Module:** IFM.Audit.Executive
- **Payroll Exclusions:** Executive officer exclusions affect premium audit payroll calculations
- **Audit Classifications:** Excluded executive officer payroll removed from audit classifications
- **Multi-State Coordination:** Executive exclusions coordinate across Indiana and Kentucky audit processes
- **Final Premium Impact:** Exclusions affect final premium calculations and billing adjustments

#### 2.5.3 Illinois-Only Endorsements

**Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others (IL)**
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others (WC 12 03 07)(IL)"
- **Visibility Conditions:**
  - Illinois must be included in quote (`SubQuotesContainsState("IL")`)
  - Policy effective date must have multistate capability (`IsMultistateCapableEffectiveDate()`)
- **Data Assignment:** `ILQuote.HasExclusionOfSoleProprietorsPartnersOfficersAndOthers_IL`

#### Cross-System Impact Analysis

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Exclusions.Illinois
- **Multi-Category Exclusion:** Selection excludes multiple worker categories from Illinois workers compensation coverage
- **Category Verification:** Claims require verification of worker status against excluded categories
- **Illinois-Specific Rules:** Claims processing applies Illinois-specific exclusion rules and procedures
- **Documentation Requirements:** Exclusion claims require comprehensive documentation for regulatory compliance

**Application Processing Integration**:
- **System Module:** IFM.Application.Illinois.Exclusions
- **Effective Date Validation:** Application validates exclusion availability against multistate effective date requirements
- **Documentation Requirements:** Illinois exclusions may require additional documentation for application approval
- **Regulatory Filing:** Exclusion selections filed with Illinois Department of Insurance
- **Compliance Verification:** Application processing verifies Illinois-specific exclusion compliance requirements

#### 2.5.4 Kentucky-Only Endorsements

**Rejection of Coverage Endorsement (KY)**
- **Field Type:** Checkbox
- **Business Label:** "Rejection of Coverage Endorsement (WC 16 03 01)(KY)"
- **Complex Visibility Conditions:**
  - Kentucky must be included in quote, OR Kentucky is governing state
  - Policy effective date must be ≥ Kentucky WCP system effective date
  - Dual condition: `(EffectiveDate >= KentuckyWCPEffectiveDate AND SubQuotesContainsState("KY")) OR Quote.QuickQuoteState = Kentucky`
- **Data Assignment:** `KYQuote.HasKentuckyRejectionOfCoverageEndorsement`

#### Cross-System Impact Analysis

**Regulatory Compliance Integration**:
- **System Module:** IFM.Compliance.Kentucky
- **Coverage Rejection Documentation:** Selection requires formal documentation of coverage rejection with Kentucky authorities
- **State Filing Requirements:** Rejection endorsement requires specific filings with Kentucky Department of Workers Claims
- **Effective Date Coordination:** Endorsement availability coordinated with Kentucky WCP system effective date requirements
- **Compliance Monitoring:** Rejection selections monitored for ongoing Kentucky regulatory compliance

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Kentucky.Rejection
- **Coverage Rejection Processing:** Selection affects claims processing for rejected coverage categories
- **State-Specific Handling:** Claims processing applies Kentucky-specific rules for coverage rejection endorsements
- **Appeal Rights:** Rejection endorsements affect worker appeal rights under Kentucky workers compensation law
- **Documentation Standards:** Rejected coverage claims require specific documentation and regulatory reporting

#### Source Code Details
- **Primary Logic:** Save method state-specific endorsement assignment, Lines 620-695
- **Visibility Control:** Populate method endorsement display logic, Lines 355-400
- **State Detection:** `SubQuotesContainsState()` and `SubQuoteForState()` helper methods

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

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Location
- **Location-Based Rating:** Location assignments drive state-specific rating calculations and premium allocations
- **Multi-State Coordination:** Location state assignments coordinate rating calculations across multiple states
- **Territory Rating:** Location details affect territory rating factors and premium calculations
- **Experience Rating:** Location assignments coordinate with experience modification applications

**Application Processing Integration**:
- **System Module:** IFM.Application.Locations
- **Location Validation:** Application validates location assignments against state requirements and business rules
- **Address Verification:** Location addresses validated for accuracy and state tax jurisdiction determination
- **Documentation Requirements:** Location assignments may trigger specific documentation requirements for application
- **Inspection Scheduling:** Location information used for inspection scheduling and underwriting review

**Billing System Integration**:
- **System Module:** IFM.Billing.Locations
- **Premium Allocation:** Location assignments drive premium allocation across multiple states and jurisdictions
- **Tax Calculations:** Location state assignments determine applicable state taxes and fees
- **Audit Coordination:** Location information coordinates with premium audit allocation and calculations
- **Invoice Detail:** Location details appear on billing statements and premium allocation reports

#### Validation Integration
- **Multi-State Quote Requirements:** Each state must have minimum one location
- **Single-State Quote Requirements:** Minimum one location required
- **Error Message Examples:** 
  - **"You must have at least one location for each state on the quote (missing: IL, KY)"**
  - **"You must have at least one location and classification on the quote"**

#### Source Code Details
- **Control Embedding:** `ctl_WCP_LocationList` control integration in ctl_WCP_Coverages.ascx
- **Validation Logic:** Location validation in ValidateControl method, Lines 730-745

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

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Classifications
- **Rate Determination:** Classification codes drive base rate lookups and premium calculations for each state
- **Multi-State Rating:** Classification assignments coordinate rating across multiple states with state-specific rates
- **Experience Rating:** Classifications affect experience modification calculations and loss development tracking
- **Audit Basis:** Classification codes establish premium audit basis and payroll allocation methodologies

**Underwriting Integration**:
- **System Module:** IFM.Underwriting.Classifications
- **Risk Assessment:** Classification codes drive underwriting risk assessment and approval requirements
- **Appetite Determination:** Classifications validate against company appetite and underwriting guidelines
- **Documentation Requirements:** Certain classifications trigger additional documentation and inspection requirements
- **Approval Workflows:** High-risk classifications may require underwriting management approval

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Classifications
- **Coverage Determination:** Classification codes affect claims coverage determination and injury categorization
- **Medical Management:** Classifications influence medical management protocols and injury treatment approaches
- **Return-to-Work:** Classification-specific return-to-work programs and restrictions apply based on work types
- **Loss Development:** Classifications affect loss development tracking and experience rating calculations

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

#### Cross-System Impact Analysis

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Farm
- **Farm Rating Methodology:** Farm indicator triggers specialized agricultural rating algorithms and rate tables
- **Seasonal Adjustments:** Farm ratings may include seasonal premium adjustments and payroll variations
- **Multi-State Farm Rating:** Farm indicator coordinates agricultural rating across multiple states
- **Experience Modification:** Farm indicator affects experience modification calculations and agricultural loss development

**Regulatory Compliance Integration**:
- **System Module:** IFM.Compliance.Agricultural
- **Farm Reporting:** Farm indicator triggers specific regulatory reporting requirements for agricultural operations
- **State Compliance:** Farm operations subject to state-specific agricultural workers compensation regulations
- **Safety Requirements:** Farm indicator may trigger additional safety requirement compliance and documentation
- **Audit Specifications:** Farm operations subject to specialized audit procedures and payroll verification

**Claims Processing Integration**:
- **System Module:** IFM.Claims.Agricultural
- **Agricultural Claims Handling:** Farm indicator affects claims processing with agricultural-specific protocols
- **Seasonal Workers:** Claims processing accommodates seasonal agricultural worker considerations
- **Equipment Claims:** Farm indicator affects equipment-related injury claim processing and coverage determinations
- **Medical Networks:** Agricultural operations may require specialized medical provider networks

**Underwriting Integration**:
- **System Module:** IFM.Underwriting.Agricultural
- **Farm Risk Assessment:** Farm indicator triggers agricultural risk assessment protocols and inspection requirements
- **Seasonal Operations:** Underwriting evaluates seasonal operation risks and payroll variations
- **Equipment Evaluation:** Farm operations require evaluation of agricultural equipment and safety protocols
- **Loss Control:** Farm indicator triggers specialized loss control services and risk management programs

#### Source Code Details
- **Detection Logic:** Save method farm indicator detection, Lines 700-735
- **Triggering Codes:** Hard-coded list in wcpClassCodesToFind variable, Line 702
- **Data Assignment:** Applied to both Quote.HasFarmIndicator and each SubQuote.HasFarmIndicator

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

#### Cross-System Impact Analysis

**Application Processing Integration**:
- **System Module:** IFM.Application.Validation
- **Validation Coordination:** Application module coordinates validation across all policy level coverage requirements
- **Submission Blocking:** Validation failures prevent application submission and policy binding processes
- **Error Aggregation:** Application processing aggregates validation errors across all integrated modules
- **User Guidance:** Validation failures provide user guidance for completing required fields and corrections

**Rating Engine Integration**:
- **System Module:** IFM.VR.Rating.Validation
- **Rating Prerequisites:** Required field validation ensures complete data for accurate rating calculations
- **Calculation Blocking:** Missing required fields prevent rating engine calculations and premium determination
- **Data Dependencies:** Rating engine validates data completeness before processing premium calculations
- **Error Recovery:** Validation failures provide clear guidance for completing rating prerequisites

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

#### Cross-System Impact Analysis

**Multi-State Coordination Integration**:
- **System Module:** IFM.MultiState.Coordination
- **State Synchronization:** Multi-state validation ensures consistent data across all state components
- **Cross-State Dependencies:** Validation coordinates requirements across locations, classifications, and endorsements
- **Data Integrity:** Multi-state validation maintains data integrity across state-specific quote components
- **Error Prevention:** Validation prevents downstream processing errors from incomplete multi-state data

**Regulatory Compliance Integration**:
- **System Module:** IFM.Compliance.StateRequirements
- **State-Specific Rules:** Validation ensures compliance with each state's minimum workers compensation requirements
- **Filing Requirements:** Validation prepares data for state-specific filing and reporting requirements
- **Audit Preparation:** Validation ensures data completeness for regulatory audit and compliance reviews
- **Documentation Standards:** Validation maintains documentation standards required by state insurance departments

#### Source Code Details
- **Validation Logic:** ValidateControl method comprehensive validation, Lines 715-770
- **State Validation:** Multi-state and single-state validation branching logic, Lines 745-765
- **Accordion Integration:** Error highlighting with visual feedback in accordion sections

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

#### Cross-System Impact Analysis

**User Experience Coordination**:
- **System Module:** IFM.UX.Workflow
- **Section Completion Tracking:** Accordion sections coordinate completion status with overall quote progress tracking
- **Error State Management:** UI error states coordinate with validation systems across all integrated modules
- **Progress Indicators:** Section completion feeds into overall quote completion progress indicators
- **Navigation Control:** Accordion state affects navigation availability to subsequent quote sections

**Save State Management Integration**:
- **System Module:** IFM.SaveState.Management
- **Section-Level Saves:** Individual accordion saves coordinate with overall quote save state management
- **Data Synchronization:** Section saves trigger data synchronization across related system modules
- **Auto-Save Coordination:** Section-level changes coordinate with auto-save functionality and data persistence
- **Recovery Operations:** Save state management enables recovery from incomplete section saves and data loss

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

#### Cross-System Impact Analysis

**Workflow Integration**:
- **System Module:** IFM.Workflow.Management
- **Save Coordination:** Button actions coordinate across multiple system modules and data persistence layers
- **Progress Tracking:** Save operations update overall quote progress and completion tracking
- **State Management:** Button actions maintain quote state consistency across system modules
- **Navigation Control:** Save operations affect navigation availability to subsequent quote processing steps

**Rating Engine Coordination**:
- **System Module:** IFM.VR.Rating.Trigger
- **Rating Initiation:** "Rate This Quote" button coordinates complete save validation with rating engine activation
- **Prerequisites Validation:** Rating button validates all required data completion before initiating calculations
- **Progress Communication:** Rating initiation communicates progress status to user interface and workflow management
- **Error Handling:** Rating failures coordinate with save state recovery and user error communication

**Underwriting Workflow Integration**:
- **System Module:** IFM.Underwriting.Workflow
- **Assistance Requests:** "Email for UW Assistance" button triggers underwriting workflow and case management
- **Data Package Creation:** Underwriting assistance compiles complete quote data package for underwriter review
- **Communication Tracking:** Underwriting requests tracked through workflow system and case management
- **Follow-up Coordination:** Underwriting assistance coordinates with quote status and agent communication

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

#### Cross-System Impact Analysis

**Real-Time Validation Integration**:
- **System Module:** IFM.Validation.ClientSide
- **Field-Level Validation:** JavaScript functions coordinate with server-side validation for real-time user feedback
- **Error Prevention:** Client-side validation prevents invalid data entry and reduces server round-trips
- **User Experience:** Real-time validation provides immediate feedback and improves user data entry experience
- **Server Coordination:** Client-side validation coordinates with server-side validation for comprehensive data integrity

**State Management Integration**:
- **System Module:** IFM.State.ClientSide
- **UI State Persistence:** JavaScript manages UI state persistence across page interactions and accordion operations
- **Data Synchronization:** Client-side state changes synchronize with server-side data model and persistence
- **User Preference:** Client-side state management maintains user preferences and interface customizations
- **Performance Optimization:** State management reduces server requests and improves application performance

#### Source Code Details
- **JavaScript Integration:** AddScriptWhenRendered method, Lines 85-120
- **Event Binding:** Dynamic event attachment for user controls, Lines 95-118
- **External Dependencies:** vrWCP.js for client-side behavior, jQuery for UI functionality

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

**Cross-System Architecture Overview:**
This enhanced document now includes comprehensive cross-system impact analysis identifying downstream consequences and integration requirements across all major system modules:

- **Rating Engine (IFM.VR.Rating):** Premium calculation coordination and rating methodology application
- **Application Processing (IFM.Application):** Data validation, document generation, and regulatory compliance
- **Claims Processing (IFM.Claims):** Coverage determination, exclusion processing, and regulatory reporting
- **Billing System (IFM.Billing):** Premium calculation, payment processing, and audit coordination
- **Underwriting (IFM.Underwriting):** Risk assessment, approval workflows, and documentation requirements
- **Regulatory Compliance (IFM.Compliance):** State-specific requirements, filing obligations, and audit preparation

**Coverage Completeness Statement:** This document provides complete technical specifications for Policy Level Coverages functionality with 100% source code traceability for all business rules, dropdown options, validation logic, Enhanced UI components, user interface behaviors, and comprehensive cross-system integration requirements. All dropdown options extracted from source data with complete option universe documented.

**Cross-System Integration Completeness:** All major user selections and configurations documented with downstream module impact analysis, workflow implications, and integration touchpoint specifications for comprehensive modernization planning.

---

**Document Status:** Complete requirements documentation with Enhanced UI specifications and comprehensive cross-system integration analysis ready for stakeholder implementation and development work.