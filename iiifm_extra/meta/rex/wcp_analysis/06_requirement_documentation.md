# WCP LOB - Step 6: Requirement Documentation

## BUSINESS-FRIENDLY REQUIREMENTS EXTRACTED FROM WCP SOURCE CODE

### UW QUESTIONS REQUIREMENTS

#### UWQ-001: Kill Questions Validation
**Field Name**: Underwriting Questions Popup
**Field Type**: Modal Dialog with 6 Yes/No Questions
**Visibility Condition**: Always displayed at quote initiation
**Required Condition**: All 6 questions must be answered
**Validation Message**: "All Questions Must Be Answered"
**Source Evidence**: ctlUWQuestionsPopup.ascx, UWQuestions.vb lines 82-88

**Kill Questions List**:
1. "Does Applicant own, operate or lease aircraft or watercraft?" (Diamond Code: 9341)
2. "Do/have past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material?" (Diamond Code: 9086)  
3. "Do any employees live outside the state of [governing state]?" (Diamond Code: 9342/9573 - varies by multi-state capability)
4. "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?" (Diamond Code: 9343)
5. "Is the Applicant involved in the operation of a professional employment organization, employee leasing operation, or temporary employment agency?" (Diamond Code: 9344)
6. "Any tax liens or bankruptcy within the last 5 years?" (Diamond Code: 9107)

#### UWQ-002: Additional Information Requirement
**Field Name**: Additional Information (per kill question)
**Field Type**: Multi-line text area
**Visibility Condition**: Shows when "Yes" selected for any kill question
**Required Condition**: Required when "Yes" is selected
**Validation Message**: "Additional Information Response Required"
**Source Evidence**: ctlUWQuestionsPopup.ascx, AllAdditionalInfoFieldsAreAnswered() function

#### UWQ-003: Multi-State Question Logic
**Field Name**: Employee Residency Kill Question (Question 3)
**Field Type**: Yes/No Radio Buttons
**Visibility Condition**: Always displayed
**Question Text Variation**: 
- Single State: "Do any employees live outside the state of [state name]?"
- Multi-State: "Do any employees live outside the state(s) of [state list]?"
- Kentucky Enhancement: "Do any employees live outside the state(s) of Indiana, Illinois, or Kentucky?"
**Source Evidence**: UWQuestions.vb lines 1894-1925

### GENERAL INFORMATION REQUIREMENTS

#### GEN-001: Employer's Liability Limits
**Field Name**: Employer's Liability  
**Field Type**: Dropdown Selection
**Visibility Condition**: Always displayed
**Required Condition**: Must be selected
**Validation Message**: UNVERIFIED - SOURCE CODE EVIDENCE NOT FOUND
**Business Rule**: "We require minimum limits of 500/500/500 when quoting an umbrella"
**Source Evidence**: ctl_WCP_Coverages.ascx lines 24-30

#### GEN-002: Experience Modification Factor
**Field Name**: Experience Modification
**Field Type**: Text Input (Decimal)
**Visibility Condition**: Always displayed  
**Required Condition**: Must be entered
**Validation Message**: UNVERIFIED - SOURCE CODE EVIDENCE NOT FOUND
**Business Behavior**: AutoPostBack triggers immediate rating recalculation
**Source Evidence**: ctl_WCP_Coverages.ascx line 37

#### GEN-003: Experience Modification Effective Date  
**Field Name**: Experience Mod Eff Date
**Field Type**: Date Picker with Calendar
**Visibility Condition**: Always displayed
**Required Condition**: Must be entered
**Date Format**: MM/dd/yyyy
**Calendar Behavior**: Opens on text field focus
**Source Evidence**: ctl_WCP_Coverages.ascx lines 42-45

### LOCATION REQUIREMENTS

#### LOC-001: Location Information
**Field Name**: Location Address
**Field Type**: Address Control (reused from Home LOB)
**Visibility Condition**: At least one location required
**Required Condition**: Location #1 is required, additional locations optional
**Multiple Locations**: Supported via Add New functionality
**Source Evidence**: ctl_WCP_Location.ascx, ctl_WCP_LocationList.ascx

### CLASSIFICATION REQUIREMENTS

#### CLS-001: Class Code Selection
**Field Name**: Class Code
**Field Type**: Read-Only Text (populated via lookup)
**Visibility Condition**: Always displayed for each classification
**Required Condition**: Must be selected via lookup
**Lookup Integration**: "Class Code Lookup" button opens lookup dialog
**Manual Entry**: Prevented (read-only field)
**Source Evidence**: ctl_WCP_Classification.ascx lines 20-25

#### CLS-002: Payroll Entry  
**Field Name**: Payroll
**Field Type**: Text Input (Numeric)
**Visibility Condition**: Always displayed for each classification
**Required Condition**: Must be entered for each class code
**Validation Message**: UNVERIFIED - SOURCE CODE EVIDENCE NOT FOUND
**Source Evidence**: ctl_WCP_Classification.ascx lines 30-33

#### CLS-003: Class Code Description
**Field Name**: Description
**Field Type**: Read-Only Text (auto-populated)
**Visibility Condition**: Displays when class code selected
**Required Condition**: Auto-populated, not user-editable
**Source Evidence**: ctl_WCP_Classification.ascx lines 40-43

#### CLS-004: Classification Save Requirement
**Field Name**: Individual Classification Save
**Field Type**: Business Rule
**Visibility Condition**: Warning always displayed
**Required Condition**: "You MUST click save after entering each classification!"
**Validation Message**: Red warning text
**Business Impact**: Prevents data loss, ensures proper rating
**Source Evidence**: ctl_WCP_Classification.ascx lines 50-52

#### CLS-005: Multiple Classifications Support
**Field Name**: Classification List
**Field Type**: Repeating Section
**Visibility Condition**: Always displayed
**Required Condition**: At least one classification required
**Add New**: "Add New" link creates additional classification sections
**Source Evidence**: ctl_WCP_Coverages.ascx lines 55-65

### ENDORSEMENT REQUIREMENTS

#### END-001: Inclusion of Sole Proprietors
**Field Name**: Inclusion of Sole Proprietors, Partners, and LLC Members
**Field Type**: Checkbox
**Visibility Condition**: Available in IN/IL states only
**Required Condition**: Optional selection
**Form Reference**: (WC 00 03 10)(IN/IL)
**Source Evidence**: ctl_WCP_Coverages.ascx lines 85-90

#### END-002: Blanket Waiver of Subrogation
**Field Name**: Blanket Waiver of Subrogation  
**Field Type**: Checkbox
**Visibility Condition**: Available in IN/IL states only
**Required Condition**: Optional selection
**Form Reference**: (WCP 1001)(IN/IL)
**Source Evidence**: ctl_WCP_Coverages.ascx lines 92-97

#### END-003: Waiver of Subrogation with Count
**Field Name**: Waiver of Subrogation
**Field Type**: Checkbox
**Visibility Condition**: Available in IN/IL states only
**Required Condition**: Optional selection
**Form Reference**: (WC 00 03 13)(IN/IL)
**Dependent Field**: Number of Waivers (required when checked)
**Source Evidence**: ctl_WCP_Coverages.ascx lines 98-115

#### END-004: Number of Waivers
**Field Name**: Number of Waivers
**Field Type**: Text Input (Numeric Only)
**Visibility Condition**: Shows when Waiver of Subrogation selected
**Required Condition**: Required when parent checkbox selected
**Input Restriction**: Numeric characters only (0-9)
**Source Evidence**: ctl_WCP_Coverages.ascx line 106

#### END-005: Indiana-Specific Exclusions
**Field Name**: Exclusion of Amish Workers
**Field Type**: Checkbox  
**Visibility Condition**: Indiana state only
**Required Condition**: Optional selection
**Form Reference**: (WC 00 03 08)(IN)
**Source Evidence**: ctl_WCP_Coverages.ascx lines 110-115

**Field Name**: Exclusion of Executive Officer
**Field Type**: Checkbox
**Visibility Condition**: Indiana state only  
**Required Condition**: Optional selection
**Form Reference**: (WC 00 03 08)(IN)
**Regulatory Note**: Requires Indiana state form 36097 submission
**Source Evidence**: ctl_WCP_Coverages.ascx lines 115-125

#### END-006: Illinois-Specific Exclusion  
**Field Name**: Exclusion of Sole Proprietors, Partners, Officers, LLC Members & others
**Field Type**: Checkbox
**Visibility Condition**: Illinois state only
**Required Condition**: Optional selection
**Form Reference**: (WC 12 03 07)(IL)
**Source Evidence**: ctl_WCP_Coverages.ascx (inferred from pattern)

#### END-007: Kentucky-Specific Endorsement
**Field Name**: Rejection of Coverage Endorsement
**Field Type**: Checkbox
**Visibility Condition**: Kentucky state only
**Required Condition**: Optional selection  
**Form Reference**: (WC 16 03 01)(KY)
**Source Evidence**: ctl_WCP_Coverages.ascx (inferred from pattern)

### WORKFLOW REQUIREMENTS

#### WFL-001: Section-Based Save Operations
**Field Name**: Save Operations
**Field Type**: Multiple Save Buttons
**Save General Info**: Saves Experience Mod + Employer's Liability
**Save Classifications**: Saves all classification data
**Save Endorsements**: Saves endorsement selections
**Rate This Quote**: Saves all data + initiates rating
**Source Evidence**: ctl_WCP_Coverages.ascx lines 15-20, 55-60, 125-135

#### WFL-002: UW Assistance Integration
**Field Name**: Email for UW Assistance
**Field Type**: Button
**Visibility Condition**: Always available
**Required Condition**: Optional use
**Function**: Launches email to underwriter
**Source Evidence**: ctl_WCP_Coverages.ascx lines 135-140

#### WFL-003: Navigation Workflow
**Field Name**: Quote Section Navigation
**Field Type**: Tree View Control
**Visibility Condition**: Always displayed on left side
**Required Condition**: Enables section-by-section completion
**Source Evidence**: ctl_WorkflowMgr_Quote_WCP.ascx lines 20-25

### BUSINESS RULES EXTRACTED

#### BR-001: Umbrella Coordination Rule
**Rule**: When quoting umbrella coverage, Employer's Liability must have minimum limits of 500/500/500
**Source Evidence**: ctl_WCP_Coverages.ascx lines 28-30

#### BR-002: Individual Classification Save Rule  
**Rule**: Each classification (class code + payroll combination) must be saved individually before proceeding
**Impact**: Prevents data loss and ensures proper rating calculation
**Source Evidence**: ctl_WCP_Classification.ascx lines 50-52

#### BR-003: State-Specific Endorsement Rule
**Rule**: Endorsement availability varies by governing state (IN/IL/KY have different options)
**Impact**: UI dynamically shows/hides endorsements based on state selection
**Source Evidence**: ctl_WCP_Coverages.ascx conditional row rendering

#### BR-004: Kill Questions Gate Rule
**Rule**: All 6 kill questions must be answered before quote can proceed
**Impact**: Prevents quote progression with incomplete underwriting information
**Source Evidence**: ctlUWQuestionsPopup.ascx validation functions

#### BR-005: Multi-State Question Logic Rule
**Rule**: Employee residency question varies based on policy effective date and multi-state capability
**Impact**: Question text and diamond codes change dynamically
**Source Evidence**: UWQuestions.vb lines 82-85, 1894-1925

## REQUIREMENT DOCUMENTATION STATUS: ✅ COMPLETE
All major WCP functionality converted to business-friendly requirements with source evidence. Items marked UNVERIFIED require stakeholder confirmation for validation message text and dropdown values.