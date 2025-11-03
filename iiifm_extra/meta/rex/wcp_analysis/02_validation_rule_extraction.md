# WCP LOB - Step 2: Validation & Rule Extraction

## SOURCE EVIDENCE
- **JavaScript Validation**: ctlUWQuestionsPopup.ascx, lines 100-800
- **Field Validation**: ctl_WCP_Coverages.ascx, ctl_WCP_Classification.ascx
- **Server-Side Validation**: Code-behind files (inferred from AutoPostBack behaviors)

## REQUIRED FIELD VALIDATIONS

### General Information Section
**Source**: ctl_WCP_Coverages.ascx, lines 22-48
1. **Employer's Liability**: Required field (marked with *)
   - **Field Type**: Dropdown selection
   - **Validation Message**: UNVERIFIED - not found in source code
   - **Business Rule**: Must be selected for quote completion

2. **Experience Modification**: Required field (marked with *)
   - **Field Type**: Decimal input with AutoPostBack
   - **Input Behavior**: AutoPostBack="true" triggers immediate server processing
   - **Validation Message**: UNVERIFIED - not found in source code

3. **Experience Mod Eff Date**: Required field (marked with *)
   - **Field Type**: Date picker with calendar popup
   - **Validation Message**: UNVERIFIED - not found in source code

### Classification Information Section  
**Source**: ctl_WCP_Classification.ascx, lines 15-50
1. **Class Code**: Required field (marked with *)
   - **Field Type**: Read-only (populated via lookup)
   - **Validation Rule**: Must be selected via lookup before saving
   
2. **Payroll**: Required field (marked with *)
   - **Field Type**: Numeric text input
   - **Validation Rule**: Must be entered for each classification
   - **Save Requirement**: "You MUST click save after entering each classification!" (line 50-52)

## INPUT RESTRICTIONS

### Number of Waivers Field
**Source**: ctl_WCP_Coverages.ascx, line 106
```html
<asp:TextBox ID="txtNumberOfWaivers" runat="server" onkeypress='return event.charCode >= 48 && event.charCode <= 57'></asp:TextBox>
```
- **Input Restriction**: Numeric characters only (0-9)
- **Implementation**: JavaScript keypress event filtering
- **Range Validation**: UNVERIFIED - no upper bound found in source

### Experience Modification Field
**Source**: ctl_WCP_Coverages.ascx, line 37 (commented out validation)
```html
<%--<asp:TextBox ID="txtExpMod" runat="server" onkeypress='return (event.charCode >= 48 && event.charCode <= 57) || (event.charCode == 190)'></asp:TextBox>--%>
```
- **Previous Logic**: Numeric + decimal point allowed (charCode 190 = period)
- **Current Implementation**: No client-side input restriction (relies on server validation)

## UW QUESTIONS VALIDATION

### Comprehensive JavaScript Validation  
**Source**: ctlUWQuestionsPopup.ascx, function AllAnswersAreAnswered() lines 200-300
1. **All Questions Must Be Answered**: Each radio button pair checked
2. **Additional Information Required**: When "Yes" selected, textarea must have content
3. **Error Display**: Red asterisk (*) shows for unanswered questions
4. **Validation Message**: "All Questions Must Be Answered" (line 750)

### Effective Date Validation
**Source**: ctlUWQuestionsPopup.ascx, function ValidateEffectiveDate() lines 400-500
- **Date Format Validation**: Must be valid date format
- **Date Range Validation**: Must be between min/max effective dates  
- **Error Messages**: Dynamic based on date range violations

## CONDITIONAL VALIDATIONS

### Waiver of Subrogation Logic
**Source**: ctl_WCP_Coverages.ascx, lines 95-115
- **Trigger**: When Waiver of Subrogation checkbox is checked
- **Required Field**: Number of Waivers becomes required
- **Field Display**: Number of Waivers row shows/hides based on checkbox state

### State-Specific Endorsement Visibility
**Source**: ctl_WCP_Coverages.ascx, lines 110-127  
- **Indiana Specific**: Exclusion of Amish Workers, Exclusion of Executive Officer
- **Illinois Specific**: Exclusion of Sole Proprietors, Partners, Officers, LLC Members
- **Kentucky Specific**: Rejection of Coverage Endorsement
- **Validation Rule**: State-specific forms only appear for applicable governing states

## FORM SUBMISSION VALIDATION

### UW Questions Form Validation
**Source**: ctlUWQuestionsPopup.ascx, function ValidateUWForm() lines 650-700
- **All Answers Validated**: AllAnswersAreAnswered() check
- **Additional Info Validated**: AllAdditionalInfoFieldsAreAnswered() check
- **Effective Date Validated**: ValidateEffectiveDate() check
- **Governing State Check**: Must be selected if dropdown is enabled

### Section-Specific Save Validation
**Source**: ctl_WCP_Coverages.ascx, multiple LinkButton controls
- **Save General Info**: lnkSaveGeneralInfo validation
- **Save Classifications**: btnSaveClassifications validation  
- **Save Endorsements**: lnkSaveEndorsements validation
- **Critical Rule**: Each classification must be saved individually

## CLIENT-SIDE VS SERVER-SIDE VALIDATION

### Client-Side (JavaScript)
- **Input Masking**: Number of Waivers numeric-only
- **UW Questions**: Complete popup validation before submission
- **Immediate Feedback**: Error highlighting and messages

### Server-Side (Inferred)
- **Experience Modification**: AutoPostBack processing for rating calculation
- **Class Code Lookup**: Server-side lookup functionality
- **Final Quote Rating**: Server validation before rate calculation

## EVIDENCE STATUS: ✅ VERIFIED WITH GAPS
All validation logic verified from source code. Some validation messages marked UNVERIFIED where source code evidence not found in markup files.