# WCP LOB - Step 1: UI & Field Discovery

## SOURCE EVIDENCE
- **Primary Files Analyzed**: 
  - VR3WCP.aspx (main page)
  - ctl_WorkflowMgr_Quote_WCP.ascx (workflow container)
  - ctl_WCP_Coverages.ascx (main UI sections)
  - ctl_WCP_Classification.ascx (classification details)
  - ctl_WCP_Location.ascx (location details)
  - ctlUWQuestionsPopup.ascx (popup questions)

## MAIN UI STRUCTURE
**Workflow-Based Design**: WCP uses tabbed/sectioned workflow manager with 4 main sections:

### Section 1: General Information
**Source**: ctl_WCP_Coverages.ascx, lines 22-48
- **Employer's Liability**: Dropdown (required field marked with *)
  - **Validation Note**: "We require minimum limits of 500/500/500 when quoting an umbrella."
- **Experience Modification**: Text input (required field marked with *)
  - **Behavior**: AutoPostBack="true" for immediate rating impact
- **Experience Mod Eff Date**: Date picker with calendar popup (required field marked with *)

### Section 2: Location Information  
**Source**: ctl_WCP_Location.ascx + ctl_WCP_LocationList.ascx (repeater)
- **Dynamic Structure**: Repeater-based location list
- **Address Fields**: Reuses home insurance property address control
- **Actions**: Add New, Delete, Clear, Save per location

### Section 3: Classification Information
**Source**: ctl_WCP_Classification.ascx, lines 15-50  
- **Dynamic Structure**: Repeater-based classification list with Add New capability
- **Class Code**: Read-only text field populated via lookup
- **Payroll**: Text input field (required field marked with *)
- **Description**: Read-only text field showing class code description
- **Class Code Lookup**: Button opens lookup functionality
- **Critical Requirement**: "You MUST click save after entering each classification!" (line 50-52)

### Section 4: Endorsements
**Source**: ctl_WCP_Coverages.ascx, lines 71-127
**State-Specific Visibility**: Dynamic showing based on governing state
- **Inclusion of Sole Proprietors**: Checkbox + label (IN/IL only)
- **Blanket Waiver of Subrogation**: Checkbox + label (IN/IL only)  
- **Waiver of Subrogation**: Checkbox + label (IN/IL only)
- **Number of Waivers**: Text field (required when waiver selected) - numeric input only
- **Exclusion Options**: State-specific exclusions (IN, IL, KY variations)

### Popup: Underwriting Questions
**Source**: ctlUWQuestionsPopup.ascx, UWQuestions.vb lines 80-88, 1856-2233
**6 Kill Questions** (verified from lessons learned):
1. **Diamond Code 9341**: "Does Applicant own, operate or lease aircraft or watercraft?"
2. **Diamond Code 9086**: "Do/have past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material?"
3. **Diamond Code 9342/9573**: "Do any employees live outside the state of [governing state]?" (varies by multi-state capability)
4. **Diamond Code 9343**: "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"
5. **Diamond Code 9344**: "Is the Applicant involved in the operation of a professional employment organization, employee leasing operation, or temporary employment agency?"
6. **Diamond Code 9107**: "Any tax liens or bankruptcy within the last 5 years?"

**Question Structure**: Each question has Yes/No radio buttons + Additional Information textarea

## DYNAMIC BEHAVIOR
- **Conditional Endorsement Visibility**: Based on governing state selection
- **Multi-Location Support**: Add/remove locations dynamically
- **Multi-Classification Support**: Add/remove class codes dynamically  
- **UW Questions Popup**: Modal dialog with validation requirements

## FIELD TYPES IDENTIFIED
- **Dropdowns**: Employer's Liability limits
- **Text Inputs**: Experience Modification, Payroll, Number of Waivers
- **Date Pickers**: Experience Mod Effective Date
- **Read-Only Fields**: Class Code, Class Code Description  
- **Checkboxes**: All endorsement options
- **Radio Buttons**: UW Questions (Yes/No)
- **Textareas**: UW Questions additional information
- **Lookups**: Class Code lookup functionality

## EVIDENCE STATUS: ✅ VERIFIED FROM SOURCE CODE
All UI structure verified through direct ASCX markup analysis with specific line references provided.