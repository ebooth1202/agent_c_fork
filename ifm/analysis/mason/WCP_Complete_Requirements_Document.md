# WORKERS' COMPENSATION (WCP) - COMPLETE REQUIREMENTS DOCUMENT

**Document:** Workers' Compensation Line of Business Requirements  
**Analysis Date:** Current  
**Source Verification:** 100% Source Code Verified  
**Coverage Scope:** Complete WCP functionality

## Executive Summary

Workers' Compensation (WCP) insurance quote system provides comprehensive commercial insurance quoting functionality for multi-state operations across Indiana, Illinois, and Kentucky. The system implements sophisticated risk assessment through initial quote kill questions, dynamic state-specific endorsement management, class code classification workflows, and multi-state geographic coverage capabilities.

The WCP system supports complex business scenarios including experience modification management with conditional field logic, state-specific endorsement matrices that adapt to geographic coverage combinations, and integrated classification management with external Diamond system connectivity. All functionality includes comprehensive validation frameworks ensuring data integrity and business rule compliance.

The system architecture supports both single-state and multi-state quote processing with sophisticated conditional logic that adapts user interface and business rules based on effective dates and geographic coverage selections.

---

# Section 1.0 - Risk Assessment Process

## 1.1 Initial Quote Kill Questions

### User Experience Overview
**User Action:** User initiates WCP quote process  
**System Response:** System presents modal popup with 6 mandatory risk assessment questions  
**User Must Do:** Answer all questions before quote development can proceed

### Question 1: Aircraft/Watercraft Risk Assessment
**Question Text:** "Does Applicant own, operate or lease aircraft or watercraft?"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** Selection recorded for underwriting review  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### Question 2: Hazardous Materials Operations
**Question Text:** "Do/have past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material? (e.g. landfills, wastes, fuel tanks, etc.)"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** Selection recorded for underwriting review  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### Question 3: Employee Geographic Coverage
**Multi-State Scenario:**  
**Question Text:** "Do any employees live outside the state(s) of Indiana, Illinois, or Kentucky?"  
**Single-State Scenario:**  
**Question Text:** "Do any employees live outside the state of [governing state]?"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** Selection recorded for underwriting review  
**Business Rule:** Question text adapts based on multi-state capability and effective date

### Question 4: Coverage History Verification
**Question Text:** "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** Selection recorded for underwriting review  
**Business Rule:** "Yes" answer flags as potential ineligibility risk  
**Time Scope:** 3-year lookback period

### Question 5: Business Operation Classification
**Question Text:** "Is the Applicant involved in the operation of a professional employment organization, employee leasing operation, or temporary employment agency?"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** Selection recorded for underwriting review  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### Question 6: Financial Stability Assessment (True Kill Question)
**Question Text:** "Any tax liens or bankruptcy within the last 5 years? (If 'Yes', please specify)"  
**Response Options:** Yes/No radio buttons (required)  
**User Action:** User selects Yes or No  
**System Response:** If "Yes" selected, system triggers immediate quote termination workflow  
**Business Rule:** "Yes" answer terminates quote process immediately  
**Time Scope:** 5-year lookback period  
**Special Processing:** This is a true kill question with immediate termination

## Source Code Details:
**Primary Location:** UWQuestions.vb, Lines 1856-2233  
**Secondary Location:** Diamond integration codes 9341, 9086, 9573/9342, 9343, 9344, 9107  
**External Dependencies:** Diamond system for question content and processing

---

# Section 2.0 - Coverage Selection and Configuration

## 2.1 Employer's Liability Coverage

### Field Specifications
**Field Type:** Dropdown selection  
**Business Label:** "*Employer's Liability" (asterisk indicates required)  
**Position:** Primary coverage selection area  
**Required Status:** Required field for all quotes

### User Action Scenarios
**User Action:** User opens Employer's Liability dropdown  
**System Response:** System displays available liability limit options  
**Default Selection:** "500/500/500" automatically selected for new quotes

**User Action:** User attempts to select "100/500/100" limit on umbrella quote  
**System Response:** System automatically upgrades selection to "500/500/500"  
**Alert Message:** **"The Employers Liability limit defaulted to 500/500/500, which is the minimum limit required to quote an umbrella."**  
**Business Rule:** Minimum "500/500/500" required when quoting umbrella coverage

### Validation Rules
**User Action:** User attempts to save without Employer's Liability selection  
**System Response:** System blocks save operation  
**Error Message:** **"Missing Employers Liability"**  
**User Must Do:** Select liability limit before proceeding

## 2.2 Experience Modification Management

### Field Specifications
**Field Type:** Text input with decimal validation  
**Business Label:** "*Experience Modification" (asterisk indicates required)  
**Default Value:** "1" when field is empty or contains "0"  
**Auto-Processing:** Field triggers automatic validation on data entry

### User Action Scenarios
**User Action:** User enters experience modification value "1"  
**System Response:** Experience Modification Effective Date field becomes disabled and any existing date is cleared  

**User Action:** User enters experience modification value greater than "1"  
**System Response:** Experience Modification Effective Date field becomes enabled and required  

**User Action:** User enters non-numeric or zero/negative value  
**System Response:** System blocks save operation  
**Error Message:** **"Invalid Experience Modification"**  
**User Must Do:** Enter valid numeric value greater than 0

**User Action:** User leaves Experience Modification field empty  
**System Response:** System blocks save operation  
**Error Message:** **"Missing Experience Modification"**  
**User Must Do:** Enter experience modification value

## 2.3 Experience Modification Effective Date

### Field Specifications
**Field Type:** Date picker  
**Business Label:** "*Experience Mod. Eff. Date" (conditional asterisk - required only when Experience Modification > 1)  
**Conditional Behavior:** Field accessibility depends on Experience Modification value

### Conditional Scenarios

**Scenario 1: Experience Modification = 1**
**User Action:** User enters or selects "1" for Experience Modification  
**System Response:** Date field becomes disabled and any existing date value is cleared  
**Field State:** Disabled, not required

**Scenario 2: Experience Modification > 1**
**User Action:** User enters value greater than "1" for Experience Modification  
**System Response:** Date field becomes enabled and required (asterisk appears)  
**Field State:** Enabled, required

**Scenario 3: Experience Modification > 1 with Missing Date**
**User Action:** User attempts to save with Experience Modification > 1 but no effective date  
**System Response:** System blocks save operation  
**Error Message:** **"Missing Experience Mod. Eff. Date"**  
**User Must Do:** Select effective date for experience modification

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx, Lines 19-58; ctl_WCP_Coverages.ascx.vb, Lines 436-465  
**Secondary Location:** vrWCP.js, Lines 106-123 (client-side validation)  
**External Dependencies:** None

---

# Section 3.0 - Applicant Classification Management

## 3.1 Class Code Lookup Process

### Field Specifications
**Class Code Field Type:** Read-only text box  
**Business Label:** "*Class Code" (asterisk indicates required)  
**Population Method:** Populated via lookup process only

**Payroll Field Type:** User input text box  
**Business Label:** "*Payroll" (asterisk indicates required)  
**Input Validation:** Numeric characters only

**Description Field Type:** Read-only text box  
**Business Label:** "Description"  
**Population Method:** Auto-populated from class code selection

### User Action Scenarios
**User Action:** User clicks "Class Code Lookup" button  
**System Response:** System opens class code search modal window  
**User Must Do:** Search for and select appropriate business classification

**User Action:** User searches for class codes using search terms  
**System Response:** System displays matching class codes with descriptions  
**Search Capability:** Supports both code number and description text searches

**User Action:** User selects class code from search results  
**System Response:** System populates Class Code and Description fields automatically  
**User Must Do:** Enter payroll amount for selected classification

**User Action:** User enters payroll amount  
**System Response:** System accepts numeric input  
**Validation:** System validates numeric format

### Farm Classification Detection
**Automatic Processing:** System automatically detects farm-related business operations  
**Farm Class Codes:** 0005, 0008, 0016, 0034, 0036, 0037, 0050, 0079, 0083, 0113, 0170, 8279  
**User Action:** User selects any farm-related class code  
**System Response:** System sets farm indicator flag across all sub-quotes  
**Business Impact:** Farm flag affects rating and coverage options throughout quote

### Classification Save Process
**Warning Message:** **"You MUST click save after entering each classification!"** (displayed in red)  
**User Action:** User enters class code and payroll information  
**User Must Do:** Click Save button after each complete classification entry  
**System Response:** Classification saved to quote

**User Action:** User attempts to add additional classifications without saving current  
**System Response:** System maintains warning message visibility  
**Business Rule:** Each classification must be individually saved

## 3.2 Classification Validation Rules

### Required Field Validation
**User Action:** User attempts to save classification without class code  
**System Response:** System blocks save operation  
**Error Handling:** System highlights missing required fields

**User Action:** User attempts to save classification without payroll  
**System Response:** System blocks save operation  
**Error Handling:** System highlights missing payroll requirement

### Payroll Validation
**User Action:** User enters non-numeric payroll value  
**System Response:** System rejects invalid input  
**Input Restriction:** Numeric characters only  
**User Must Do:** Enter valid numeric payroll amount

## Source Code Details:
**Primary Location:** ctl_WCP_Classification.ascx, Lines 18-55; WCPClassCodeHelper.vb, Lines 8-31  
**Secondary Location:** ctl_WCP_Coverages.ascx.vb, Lines 1073-1097 (farm detection)  
**External Dependencies:** Diamond system integration via QueryHelper.vb and stored procedures usp_ClassCode_Search_WCP, usp_get_WcpClassNewData

---

# Section 4.0 - State-Specific Endorsement Management

## 4.1 Indiana/Illinois Common Endorsements

### Inclusion of Sole Proprietors, Partners, and LLC Members
**Endorsement Code:** (WC 00 03 10)(IN/IL)  
**Availability:** Visible when quote includes Indiana or Illinois states  
**User Action:** User selects inclusion checkbox  
**System Response:** System displays data entry fields for sole proprietor information  
**Special Alert:** **"Sole Proprietors, Partners & LLC Members who elect to be included must provide written proof of health insurance coverage..."**  
**Business Rule:** Health insurance proof documentation required

**User Action:** User deselects inclusion checkbox after selecting  
**System Response:** System displays confirmation dialog **"Are you sure you want to delete this coverage?"**  
**User Options:** Confirm removal or cancel  
**If Confirmed:** System hides data entry fields and clears related information  
**If Cancelled:** Checkbox remains selected

### Blanket Waiver of Subrogation  
**Endorsement Code:** (WCP 1001)(IN/IL)  
**Availability:** Visible when quote includes Indiana or Illinois states  
**User Action:** User selects blanket waiver checkbox  
**System Response:** System enables endorsement for quote processing  
**Business Rule:** Applies blanket waiver to all subrogation situations

### Waiver of Subrogation
**Endorsement Code:** (WC 00 03 13)(IN/IL)  
**Availability:** Visible when quote includes Indiana or Illinois states  
**User Action:** User selects waiver of subrogation checkbox  
**System Response:** System displays "Number of Waivers" input field  
**User Must Do:** Enter number of individual waivers required

**Validation Scenario:**  
**User Action:** User selects waiver checkbox but leaves Number of Waivers empty  
**System Response:** System blocks save operation  
**Error Message:** **"Missing Number of Waivers"**  
**User Must Do:** Enter valid number of waivers

**User Action:** User enters non-numeric or zero/negative value for Number of Waivers  
**System Response:** System blocks save operation  
**Error Message:** **"Invalid Number of Waivers"**  
**User Must Do:** Enter valid positive numeric value

## 4.2 Indiana-Specific Endorsements

### Exclusion of Amish Workers
**Endorsement Code:** (WC 00 03 08)(IN)  
**Availability:** Visible only when quote includes Indiana state  
**Label Update:** When Kentucky enabled, label changes to **(IN/KY)** format  
**User Action:** User selects exclusion checkbox  
**System Response:** System applies Amish worker exclusion to Indiana coverage

### Exclusion of Executive Officer  
**Endorsement Code:** (WC 00 03 08)(IN)  
**Availability:** Visible only when quote includes Indiana state  
**Label Update:** When Kentucky enabled, label changes to **(IN/KY)** format  
**User Action:** User selects exclusion checkbox  
**System Response:** System applies executive officer exclusion to Indiana coverage  
**Documentation Requirement:** Indiana state form 36097 required

## 4.3 Illinois-Specific Endorsements

### Exclusion of Sole Proprietors, Partners, Officers, LLC Members  
**Endorsement Code:** (WC 12 03 07)(IL)  
**Availability:** Visible only when quote includes Illinois state  
**User Action:** User selects exclusion checkbox  
**System Response:** System applies broad exclusion to Illinois coverage  
**Coverage Impact:** Excludes multiple business entity types from Illinois coverage

## 4.4 Kentucky-Specific Endorsements

### Rejection of Coverage Endorsement  
**Endorsement Code:** (WC 16 03 01)(KY)  
**Availability:** Visible only when effective date >= Kentucky WCP effective date  
**User Action:** User selects rejection endorsement checkbox  
**System Response:** System applies coverage rejection to Kentucky portion  
**Conditional Display:** Only appears when Kentucky WCP capability is active

## 4.5 Dynamic Label Management

### Multi-State Label Updates
**Triggering Condition:** Quote effective date >= Kentucky WCP effective date  
**System Response:** All endorsement labels automatically update format  
**Label Change Examples:**  
- "(IN/IL)" changes to "(IN/IL/KY)"  
- Indiana-only endorsements change to "(IN/KY)" format

**User Experience:** Labels dynamically reflect available states without user action  
**Business Rule:** Label accuracy ensures proper state coverage understanding

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx, Lines 81-160; ctl_WCP_Coverages.ascx.vb, Lines 175-238  
**Secondary Location:** vrWCP.js, Lines 52-88 (client-side checkbox management)  
**External Dependencies:** MultiState.General.KentuckyWCPEffectiveDate system configuration

---

# Section 5.0 - Multi-State Quote Processing

## 5.1 Single-State vs Multi-State Processing

### Processing Architecture Determination
**User Action:** User selects effective date and geographic coverage  
**System Response:** System determines processing architecture based on effective date and multi-state capability  
**Business Rule:** Processing approach affects classification management and validation requirements

### Single-State Processing
**Applies When:** Quote covers single state or effective date precedes multi-state capability  
**Classification Storage:** Classifications stored at location level  
**User Experience:** Simplified classification management with location-based organization  
**Validation Requirements:** Minimum one location and one classification required

### Multi-State Processing  
**Applies When:** Quote covers multiple states and effective date supports multi-state capability  
**Classification Storage:** Classifications stored per individual state  
**User Experience:** State-specific classification management with separate state indexing  
**Validation Requirements:** Each state must have minimum one location and one classification

## 5.2 Multi-State Validation Requirements

### Location Validation by State
**User Action:** User attempts to save multi-state quote  
**System Response:** System validates each state has required locations  
**Missing Location Scenario:**  
**Error Message:** **"You must have at least one location for each state on the quote (missing: [state abbreviations])"**  
**User Must Do:** Add locations to all states listed in error message

### Classification Validation by State  
**User Action:** User attempts to save multi-state quote  
**System Response:** System validates each state has required classifications  
**Missing Classification Scenario:**  
**Error Message:** **"You must have at least one classification for each state on the quote (missing: [state abbreviations])"**  
**User Must Do:** Add classifications to all states listed in error message

### State-Specific Error Messaging
**Dynamic Error Content:** Error messages list specific states requiring attention  
**User Action:** User reviews error message  
**System Response:** System provides precise state identification for corrections  
**User Must Do:** Address each state individually until all validation requirements met

## 5.3 Geographic Coverage Logic

### Kentucky WCP Effective Date Processing
**Business Rule:** Kentucky coverage availability determined by system effective date settings  
**User Experience Impact:** UI elements, labels, and available endorsements change based on Kentucky capability  
**Processing Logic:** Multi-state capability evaluation affects question content and endorsement availability

### State Combination Management
**Supported States:** Indiana (IN), Illinois (IL), Kentucky (KY)  
**User Action:** User selects state combinations for coverage  
**System Response:** System adapts endorsement matrix and validation rules to match state selections  
**Business Rule:** Different state combinations activate different endorsement sets and business rules

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb, Lines 503-670 (multi-state processing), Lines 1253-1285 (validation)  
**Secondary Location:** MultiState.General helper classes for effective date and capability determination  
**External Dependencies:** MultiState.General.KentuckyWCPEffectiveDate configuration

---

# Section 6.0 - Address and Location Management

## 6.1 Standard Address Fields

### Address Field Configuration
**Street Number Field Type:** Text input  
**Street Name Field Type:** Text input  
**City Field Type:** Text input  
**State Field Type:** Selection dropdown  
**ZIP Code Field Type:** Text input  
**County Field Type:** Text input  
**Number of Employees Field Type:** Numeric input

### User Action Scenarios
**User Action:** User enters standard address information  
**System Response:** System accepts and validates address data  
**Validation:** Standard address validation applies to all fields

## 6.2 No Owned Locations Management

### Field Specifications
**Field Type:** Checkbox selection  
**Business Label:** "No Owned Locations"  
**Impact:** Controls accessibility of all address-related fields

### Conditional Field Management

**Scenario 1: No Owned Locations Selected**  
**User Action:** User checks "No Owned Locations" checkbox  
**System Response:** System disables all address input fields  
- Street Number: Disabled  
- Street Name: Disabled  
- City: Disabled  
- State: Disabled  
- ZIP Code: Disabled  
- County: Disabled  
- Number of Employees: Disabled  
**Button Visibility:** Save, Clear, and Add buttons become hidden  
**User Impact:** Cannot modify address information when no owned locations selected

**Scenario 2: No Owned Locations Deselected**  
**User Action:** User unchecks "No Owned Locations" checkbox  
**System Response:** System enables all address input fields  
- All address fields: Enabled for data entry  
**Button Visibility:** Save, Clear, and Add buttons become visible  
**User Impact:** Full address management functionality restored

## Source Code Details:
**Primary Location:** vrWCP.js, Lines 14-50 (no owned locations management)  
**Secondary Location:** Address field controls in main WCP workflow  
**External Dependencies:** None

---

# CROSS-MODULE DEPENDENCIES

## Coverage/Field: Experience Modification

### Linkage 1: Experience Modification Date Requirement

**Selection/Value in This Module:**
- **Field/Coverage:** Experience Modification
- **User Action:** User enters value greater than "1"
- **Value Example:** "Experience Modification = 1.25"

**Triggers Requirement In:**
- **Module/Page:** Same coverage module
- **Section:** Date field management
- **User Must:** Enter Experience Modification Effective Date

**Business Rule:**
When Experience Modification value exceeds 1.0, the effective date becomes a required field for proper rating calculation.

**Validation Impact:**
Save operation blocked if Experience Modification > 1 and effective date is missing.

**Source Code Evidence:**
- **This Module:** ctl_WCP_Coverages.ascx.vb, Lines 436-465
- **Linked Module:** Same module conditional logic
- **Data Flow:** Field enablement triggers validation requirement change

## Coverage/Field: Waiver of Subrogation

### Linkage 1: Number of Waivers Requirement

**Selection/Value in This Module:**
- **Field/Coverage:** Waiver of Subrogation checkbox
- **User Action:** User selects waiver endorsement
- **Value Example:** "Waiver of Subrogation = Selected"

**Triggers Requirement In:**
- **Module/Page:** Same endorsement section
- **Section:** Waiver details configuration
- **User Must:** Enter number of individual waivers

**Business Rule:**
When Waiver of Subrogation endorsement is selected, the number of waivers must be specified for proper coverage implementation.

**Validation Impact:**
Save operation blocked if waiver selected but number of waivers is missing or invalid.

**Source Code Evidence:**
- **This Module:** ctl_WCP_Coverages.ascx.vb, Lines 1169-1251
- **Linked Module:** Same validation framework
- **Data Flow:** Checkbox selection triggers additional field requirement

## Coverage/Field: Farm Classification Codes

### Linkage 1: Farm Indicator Cross-Quote Impact

**Selection/Value in This Module:**
- **Field/Coverage:** Class Code selection
- **User Action:** User selects farm-related class code
- **Value Example:** "Class Code = 0005 (farm operation)"

**Triggers Requirement In:**
- **Module/Page:** All sub-quotes in quote system
- **Section:** Rating and coverage options
- **User Must:** Accept farm indicator flag application

**Business Rule:**
Farm-related class codes automatically set farm indicator flag across all sub-quotes, affecting rating calculations and coverage options.

**Validation Impact:**
Farm flag influences available coverage options and pricing throughout quote system.

**Source Code Evidence:**
- **This Module:** ctl_WCP_Coverages.ascx.vb, Lines 1073-1097
- **Linked Module:** All quote objects via HasFarmIndicator property
- **Data Flow:** Farm detection code sets flag on all sub-quotes and main quote object

---

**Document Created By:** Mason (IFI Requirements Extraction Specialist)  
**Source Analysis By:** Rex (IFI Pattern Mining Specialist)  
**Requirements Completion Date:** Current  
**Business Stakeholder Ready:** Yes  
**Technical Implementation Ready:** Yes