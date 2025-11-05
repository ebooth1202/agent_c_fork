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

#### Complete Option Set
- **Data Source:** Static data loaded from QuickQuote system options via `LoadStaticDataOptionsDropDown()` method
- **Available Options:** All employer's liability limit combinations from system configuration
- **Default Selection:** "500/500/500" (automatically selected on page load)
- **Business Meaning:** Standard insurance liability limit combinations for workers compensation coverage

#### Selection Impact Analysis
- **Business Rules Triggered:** Umbrella policy eligibility validation
- **Minimum Requirements:** 500/500/500 minimum limits required for umbrella quoting
- **Premium Impact:** Selection affects premium calculation for employer's liability coverage
- **Downstream Consequences:** Selected limit value saved to all state quotes for multi-state scenarios
- **Conditional Behavior:** No additional fields become visible/required based on selection

#### User Experience & Validation
- **User Action:** Page loads
- **System Response:** Dropdown automatically defaults to "500/500/500" option
- **Error Message:** **"Missing Employers Liability"** (when no selection made)
- **User Must Do:** Select an employer's liability limit from available options

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 190-205 (`LoadStaticData()` method)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Line 42 (`ddlEmployersLiability` control)
- **External Dependencies:** QuickQuote system options data

### 1.2 Experience Modification Factor - Enhanced UI Specification

#### Field Specifications
- **Field Type:** Text input with numeric validation
- **Business Label:** "*Experience Modification" (required field)
- **Position:** General Information section, second field
- **Character Limit:** No maximum limit specified
- **Required Status:** Always required for all quotes
- **Input Restriction:** Numeric characters only
- **Value Constraint:** Must be greater than 0

#### Enhanced UI Specification - Dynamic Field State Management

**Component Type:** Dynamic Field State Controller
**Complexity Justification:** Experience Modification Factor value directly controls the state (enabled/disabled and required/optional) of the Experience Modification Effective Date field through real-time validation and visual feedback.

**Initial State:**
- **Factor Field:** Defaults to "1" (standard modification factor)
- **Date Field State:** Disabled when factor = 1.0
- **Date Field Label:** "Experience Mod.Eff. Date" (no asterisk - not required)

**User Action: Text Entry/Change**
- **Trigger:** User enters or modifies Experience Modification Factor value
- **System Response:** Real-time evaluation occurs during text change event
- **Validation Logic:** System checks if numeric value equals 1.0

**Dynamic State Transitions:**

**Scenario 1: Factor Value = 1.0**
- **Date Field State:** Becomes disabled (grayed out, non-interactive)
- **Date Field Label:** "Experience Mod.Eff. Date" (no asterisk)
- **Requirement Status:** Date field not required for validation
- **Data Handling:** Date value cleared when factor = 1.0

**Scenario 2: Factor Value > 1.0**
- **Date Field State:** Becomes enabled (interactive, normal appearance)
- **Date Field Label:** "*Experience Mod.Eff. Date" (asterisk added - now required)
- **Requirement Status:** Date field becomes required for form validation
- **Data Handling:** Date field accepts and requires user input

**Scenario 3: Invalid Factor Input**
- **Date Field State:** Maintains previous valid state until valid input provided
- **System Response:** Field remains in last valid configuration
- **Error Handling:** No dynamic change occurs until valid numeric input entered

**Error Recovery Behavior:**
- **Invalid Input:** Field state remains unchanged until valid numeric value entered
- **Clear Field:** System treats empty field as validation error, maintains previous state
- **Negative Values:** Rejected during validation, field state unchanged

#### User Experience & Validation
- **User Action:** Enter experience modification factor value
- **System Response:** Real-time validation and date field state adjustment
- **Error Message:** **"Missing Experience Modification"** (when empty)
- **Error Message:** **"Invalid Experience Modification"** (when ≤ 0 or non-numeric)
- **User Must Do:** Enter numeric value greater than 0

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 160-170 (`txtExpMod_TextChanged` event handler)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 310-320 (Populate method field state logic)
- **External Dependencies:** JavaScript integration via `vrWCP.js` for client-side behavior

### 1.3 Experience Modification Effective Date

#### Field Specifications
- **Field Type:** Date picker control
- **Business Label:** "Experience Mod.Eff. Date" or "*Experience Mod.Eff. Date" (depending on requirement status)
- **Position:** General Information section, third field
- **Required Status:** Required only when Experience Modification Factor > 1.0
- **Date Format:** MM/dd/yyyy
- **Calendar Feature:** Shows calendar on text box focus

#### Selection Impact Analysis
- **Dependency Relationship:** Field requirement and state controlled by Experience Modification Factor value
- **Business Rules Triggered:** Rating effective date assignment when experience modification > 1.0
- **Data Assignment:** Selected date becomes `RatingEffectiveDate` for quote when applicable
- **Conditional Behavior:** Field disabled and value cleared when experience modification factor = 1.0

#### User Experience & Validation
- **User Action:** Select effective date (when field enabled)
- **System Response:** Date assigned to quote rating calculations
- **Error Message:** **"Missing Experience Mod. Eff. Date"** (when required but empty)
- **User Must Do:** Select valid date when Experience Modification Factor > 1.0

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 540-560 (Save method date assignment)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Line 58 (`bdpExpModEffDate` control)
- **External Dependencies:** BasicDatePicker control library

---

## Section 2.0 - State-Specific Endorsements

### 2.1 Enhanced UI Specification - State-Specific Endorsement Display System

**Component Type:** Complex Conditional Visibility Management
**Complexity Justification:** Dynamic show/hide behavior based on multiple state combinations with cross-state dependencies and effective date considerations.

#### System Overview
The endorsement section displays different endorsement options based on which states are included in the workers compensation quote. The system evaluates state combinations and shows/hides endorsements accordingly.

#### State Detection Logic
- **Quote States:** System evaluates all states included in the quote
- **Governing State:** Primary state determined by quote setup
- **Sub-States:** Additional states included in multi-state quotes
- **Effective Date Consideration:** Some endorsements depend on policy effective dates

#### Endorsement Visibility Matrix

| Endorsement Name | Indiana (IN) | Illinois (IL) | Kentucky (KY) | Display Rule |
|------------------|--------------|---------------|---------------|--------------|
| Inclusion of Sole Proprietors | Always | Always | Always | Visible for all state combinations |
| Blanket Waiver of Subrogation | ✅ | ✅ | ❌ | Visible only when IN and/or IL present |
| Waiver of Subrogation | ✅ | ✅ | ❌ | Visible only when IN and/or IL present |
| Exclusion of Amish Workers | ✅ | ❌ | ❌ | Visible only when IN present |
| Exclusion of Executive Officer | ✅ | ❌ | ✅ | Visible only when IN and/or KY present |
| Exclusion of Sole Proprietors (IL) | ❌ | ✅ | ❌ | Visible only when IL present and multistate effective date |
| Rejection of Coverage Endorsement | ❌ | ❌ | ✅ | Visible only when KY present and effective date ≥ KY WCP effective date |

#### Dynamic Label Updates
Some endorsement labels change based on state combinations:
- **Base Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL)"
- **Multi-State Label:** "Inclusion of Sole Proprietors, Partners, and LLC Members (WC 00 03 10)(IN/IL/KY)"
- **Kentucky-Only Label:** Labels updated when Kentucky is governing state

#### User Experience Behavior
1. **Page Load:** System evaluates quote states and displays appropriate endorsements
2. **State Changes:** If user modifies states elsewhere in system, endorsement section updates dynamically
3. **Visual Consistency:** Hidden endorsements completely removed from display (not disabled)
4. **Information Preservation:** When endorsements become hidden, their values are preserved in the system

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 240-380 (Populate method state-specific logic)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 140-160 (state detection methods)
- **External Dependencies:** `SubQuotesContainsState()` and `SubQuoteForState()` helper methods

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
- **Data Management:** Managed at governing state level, applies to entire quote
- **Downstream Consequences:** Triggers compliance documentation workflow

#### User Experience & Validation
- **User Action:** Check inclusion checkbox
- **System Response:** Displays informational alert about health insurance coverage documentation requirement
- **User Action:** Uncheck inclusion checkbox
- **System Response:** Standard confirmation dialog to prevent accidental data loss
- **User Must Do:** Provide health insurance coverage documentation when selected

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 580-590 (Save method governing state logic)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Line 110 (`chkInclusionOfSoleProp` control)
- **External Dependencies:** JavaScript handler `Wcp.CoverageCheckboxChanged('INCLSOLE', ...)`

### 2.3 Enhanced UI Specification - Progressive Disclosure for Waiver of Subrogation

**Component Type:** Progressive Disclosure Pattern
**Complexity Justification:** Additional input field appears/disappears based on checkbox state with validation dependencies and error recovery workflows.

#### Progressive Disclosure Workflow

**Initial State:**
- **Checkbox State:** "Waiver of Subrogation" checkbox unchecked
- **Additional Field:** "Number of Waivers" input field hidden from display
- **Validation:** No additional validation requirements

**User Action: Enable Waiver Coverage**
- **Trigger:** User checks "Waiver of Subrogation" checkbox
- **System Response:** "Number of Waivers" input field becomes visible below checkbox
- **Field Revelation:** Field appears with table row structure for proper formatting
- **Validation Activation:** Revealed field becomes required for form validation

**User Action: Attempt to Disable Coverage**
- **Trigger:** User attempts to uncheck "Waiver of Subrogation" checkbox
- **System Response:** Displays confirmation dialog: **"Are you sure you want to delete this coverage?"**
- **User Choice Required:** User must confirm or cancel the removal action

**User Action: Confirm Coverage Removal**
- **System Response:** Checkbox becomes unchecked, "Number of Waivers" field hides
- **Data Handling:** Field value automatically cleared from system
- **Validation Impact:** Field no longer required for validation

**User Action: Cancel Coverage Removal**
- **System Response:** Checkbox remains checked, field stays visible
- **Data Preservation:** All entered data preserved in "Number of Waivers" field
- **User Experience:** No data loss, user can continue editing

#### Error Recovery Behavior
- **Accidental Unchecking:** Confirmation dialog prevents unintentional data loss
- **Data Preservation:** Cancel action maintains all user-entered values
- **Field Clearing:** Only occurs when user explicitly confirms removal

#### Validation Dependencies
- **Number of Waivers Field Requirements:**
  - Required when parent checkbox checked
  - Must be numeric value
  - Must be greater than 0
  - Error Message: **"Missing Number of Waivers"** or **"Invalid Number of Waivers"**

#### State Availability
This endorsement only appears when Indiana and/or Illinois states are present on the quote.

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 360-380 (`CheckWaiverOfSubro()` method)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Lines 135-150 (checkbox and progressive field structure)
- **External Dependencies:** JavaScript handler `Wcp.CoverageCheckboxChanged('WAIVERSUBRO', ...)`

### 2.4 Blanket Waiver of Subrogation

#### Field Specifications
- **Field Type:** Checkbox
- **Business Label:** "Blanket Waiver of Subrogation (WCP 1001)(IN/IL)"
- **Position:** Endorsements section
- **Required Status:** Optional (user choice)
- **Default State:** Unchecked
- **State Availability:** Indiana and Illinois only

#### Selection Impact Analysis
- **Business Rules Triggered:** Blanket waiver premium calculation
- **Premium Impact:** Affects premium when selected (value "4" in system)
- **Data Assignment:** Sets `BlanketWaiverOfSubrogation = "4"` when checked, cleared when unchecked

#### User Experience & Validation
- **User Action:** Check/uncheck blanket waiver checkbox
- **System Response:** Standard confirmation dialog on uncheck to prevent accidental removal
- **User Must Do:** Confirm removal if attempting to uncheck

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 591-598 (Save method assignment logic)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Line 125 (`chkBlanketWaiverOfSubro` control)
- **External Dependencies:** JavaScript handler `Wcp.CoverageCheckboxChanged('BLNKTW', ...)`

### 2.5 State-Specific Endorsements

#### 2.5.1 Indiana-Only Endorsements

**Exclusion of Amish Workers**
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Amish Workers (WC 00 03 08)(IN)"
- **Visibility:** Only when Indiana included in quote
- **State Assignment:** Value saved to Indiana state quote only

#### 2.5.2 Indiana/Kentucky Endorsements

**Exclusion of Executive Officer**
- **Field Type:** Checkbox  
- **Business Label:** "Exclusion of Executive Officer (WC 00 03 08)(IN)" or "(IN/KY)" for multi-state
- **Visibility:** When Indiana and/or Kentucky included in quote
- **Special Behavior:** When both states present, value synchronized between IN and KY state quotes

#### 2.5.3 Illinois-Only Endorsements

**Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others**
- **Field Type:** Checkbox
- **Business Label:** "Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others (WC 12 03 07)(IL)"
- **Visibility:** Only when Illinois included in quote AND multistate effective date enabled
- **Effective Date Dependency:** Only available for multistate-capable effective dates

#### 2.5.4 Kentucky-Only Endorsements

**Rejection of Coverage Endorsement**
- **Field Type:** Checkbox
- **Business Label:** "Rejection of Coverage Endorsement (WC 16 03 01)(KY)"
- **Visibility Conditions:**
  - Kentucky must be included in quote
  - Policy effective date must be ≥ Kentucky WCP system effective date
- **Governing State Logic:** Also appears when Kentucky is the governing state

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 620-680 (state-specific endorsement logic in Save method)
- **Secondary Location:** `ctl_WCP_Coverages.ascx`, Lines 155-195 (state-specific endorsement controls)
- **External Dependencies:** Kentucky WCP effective date configuration, multistate capability checks

---

## Section 3.0 - Location Management Integration

### 3.1 Location List Component Integration

#### Component Integration
- **Control Name:** `ctl_WCP_LocationList` integrated within Policy Level Coverages
- **Position:** Embedded between General Information and Classification sections
- **Function:** Manages location setup for state determination

#### Functional Relationship
- **State Dependency:** Policy-level coverages depend on location setup for state determination
- **Multi-State Validation:** Each state on the quote must have at least one location
- **Endorsement Impact:** Location state assignments drive endorsement availability

#### Validation Rules
- **Multi-State Quotes:** Each state must have minimum one location
- **Single-State Quotes:** Minimum one location required
- **Error Messages:** **"You must have at least one location for each state on the quote (missing: IL, KY)"** (example)

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx`, Line 65 (`ctl_WCP_LocationList` control embedding)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 680-690 (location validation in ValidateControl method)
- **External Dependencies:** `ctl_WCP_LocationList` control for location management

---

## Section 4.0 - Classification Management Integration  

### 4.1 Classification Component Integration

#### Component Integration
- **Control Structure:** Repeater control containing `ctl_WCP_Classification` instances
- **Position:** Classification Information section within accordion structure
- **Function:** Manages work classifications for business logic calculations

#### Functional Relationship
- **State-Specific Classifications:** Each state on multi-state quotes requires minimum one classification
- **Business Impact:** Classification data affects farm indicator status and premium calculations
- **Dynamic Management:** Classifications can be added/deleted dynamically

### 4.2 Farm Indicator Auto-Detection

#### Business Logic
System automatically sets farm indicator flag based on presence of specific WCP class codes.

#### Complete Option Set - Farm Indicator Class Codes
- **Triggering Class Codes:** "0005", "0008", "0016", "0034", "0036", "0037", "0050", "0079", "0083", "0113", "0170", "8279"
- **Business Meaning:** Agricultural and farm-related classification codes that trigger special handling
- **Detection Scope:** System scans all classifications on all locations for these specific codes

#### Selection Impact Analysis
- **Logic Flow:** 
  1. System scans all classifications on all locations during save operations
  2. If any classification matches farm indicator codes, sets `HasFarmIndicator = True`
  3. Farm indicator applies to entire quote (not per state/location)
  4. Calculation occurs during save operations and affects all state quotes

- **Business Rules Triggered:** Farm-specific rating and compliance requirements
- **Premium Impact:** Farm indicator status affects premium calculation methodology
- **Regulatory Impact:** Enables farm-specific regulatory compliance tracking

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 550-580 (Save method farm indicator detection)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 480-520 (classification repeater control management)
- **External Dependencies:** `ctl_WCP_Classification` instances within repeater control

---

## Section 5.0 - Data Validation Requirements

### 5.1 Required Field Validation

#### Always Required Fields
- **Employers Liability Limits:** Dropdown selection must be made
  - Error Message: **"Missing Employers Liability"**
- **Experience Modification Factor:** Numeric value greater than 0 required
  - Error Message: **"Missing Experience Modification"** or **"Invalid Experience Modification"**

#### Conditionally Required Fields
- **Experience Modification Effective Date:** Required when factor > 1.0
  - Error Message: **"Missing Experience Mod. Eff. Date"**
- **Number of Waivers:** Required when Waiver of Subrogation checked
  - Error Message: **"Missing Number of Waivers"** or **"Invalid Number of Waivers"**

### 5.2 State-Specific Validation Rules

#### Multi-State Quote Requirements
- **Location Validation:** Each state must have at least one location
- **Classification Validation:** Each state must have at least one classification
- **Error Message Examples:** 
  - **"You must have at least one location for each state on the quote (missing: IL, KY)"**
  - **"You have entered a multistate quote but have not entered a classification for each state. Each state must have at least one classification."**

#### Single-State Quote Requirements
- **Minimum Requirements:** At least one location and one classification required
- **Error Messages:**
  - **"You must have at least one location and classification on the quote"**
  - **"At least one classification is required."**

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 615-680 (ValidateControl method)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 280-300 (state validation helper methods)
- **External Dependencies:** Accordion integration for error highlighting with visual feedback

---

## Section 6.0 - User Interface Specifications

### 6.1 Accordion Layout Structure

#### Section Organization
1. **General Information:** Employer's Liability and Experience Modification fields
2. **Locations:** Integrated location management (separate control)
3. **Classifications:** Dynamic classification list (separate control)  
4. **Endorsements:** State-specific optional coverages

#### User Experience Features
- **Collapsible Sections:** Each section expandable/collapsible with state persistence
- **Save Button Integration:** Section-specific save buttons prevent accordion collapse during save
- **Visual Headers:** Accordion headers update based on content state and completion status

### 6.2 Save and Action Buttons

#### Button Locations and Functions
- **Section Save Buttons:** Within each accordion panel for focused saves
  - "Save" (General Information)
  - "Save" (Endorsements)  
  - "Save" (Classifications)
- **Global Action Buttons:** At component bottom
  - "Save Coverages" (saves all sections)
  - "Rate This Quote" (saves data and initiates rating)
  - "Email for UW Assistance" (underwriting support)

#### Button Behavior
- **Section Saves:** Update only that section's data without accordion state change
- **Global Save:** Processes all sections and updates complete quote data
- **Rate Button:** Saves all data and initiates rating calculation process

### 6.3 JavaScript Integration Requirements

#### Core JavaScript Dependencies
- **jQuery:** Required for accordion functionality and dynamic interactions
- **vrWCP.js:** Coverage-specific behaviors and validation
- **Event Binding:** Dynamic attachment for real-time field interactions

#### Key JavaScript Functions
- **`Wcp.CoverageCheckboxChanged()`:** Handles endorsement checkbox interactions and confirmation dialogs
- **`Wcp.ExperienceModificationValueChanged()`:** Manages experience modification field states and validation
- **`Wcp.EmployersLiabilityLimitsChanged()`:** Handles liability limit selection events

#### Source Code Details
- **Primary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 120-140 (AddScriptWhenRendered method)
- **Secondary Location:** `ctl_WCP_Coverages.ascx.vb`, Lines 100-115 (JavaScript integration and event binding)
- **External Dependencies:** `vrWCP.js` for client-side behavior, jQuery for UI functionality

---

## Source Code Reference Summary

**Primary Files Analyzed:**
- **`ctl_WCP_Coverages.ascx.vb`** - Main server-side business logic and event handling (750+ lines)
- **`ctl_WCP_Coverages.ascx`** - User interface markup and control definitions
- **Related Integration Files:**
  - `ctl_WCP_Classification.ascx` - Classification management control
  - `ctl_WCP_LocationList.ascx` - Location management integration
  - `vrWCP.js` - Client-side JavaScript behaviors

**Data Integration:**
- **QuickQuote Object Model:** Primary data persistence layer
- **Static Data Loading:** Dropdown population via system configuration
- **Multi-State Coordination:** Cross-state quote management and validation

**Coverage Completeness:** This document provides complete technical specifications for Policy Level Coverages functionality with source code traceability for all business rules, validation logic, and user interface behaviors.

---

**Document Status:** Complete requirements documentation ready for implementation planning and development work.