# WCP LOB - Step 4: Event & Workflow Tracing  

## SOURCE EVIDENCE
- **JavaScript Events**: ctlUWQuestionsPopup.ascx, VR3WCP.aspx script references
- **Server Events**: ctl_WCP_Coverages.ascx LinkButton controls
- **Workflow Structure**: ctl_WorkflowMgr_Quote_WCP.ascx container

## CLIENT-SIDE EVENT TRACING

### JavaScript File Dependencies
**Source**: VR3WCP.aspx, lines 4-11
```html
<script src="~/js/VrMiniClientSearch.js"></script>    
<script src="~/js/VrAllLines.js"></script>
<script src="~/js/VrApplicantSearch.js"></script>    
<script src="~/js/VrRiskGrade.js"></script>
<script src="~/js/vrWCP.js"></script>
<script src="~/js/vrBOP.js"></script>
<script src="~/js/VrClassCodes.js"></script>
<script src="~/js/VrProtectionClassLookup.js"></script>
```
- **WCP-Specific**: vrWCP.js handles WCP-specific client logic
- **Shared Functionality**: Class codes, risk grade, applicant search shared across LOBs
- **Cross-LOB**: vrBOP.js indicates shared commercial functionality

### Input Event Handlers

#### Experience Modification AutoPostBack
**Source**: ctl_WCP_Coverages.ascx, line 37
```html
<asp:TextBox ID="txtExpMod" runat="server" AutoPostBack="true"></asp:TextBox>
```
- **Event**: OnTextChanged (server-side)
- **Trigger**: User input completion (blur event)
- **Action**: Immediate server postback for rating calculation

#### Number of Waivers Input Restriction  
**Source**: ctl_WCP_Coverages.ascx, line 106
```html
<asp:TextBox ID="txtNumberOfWaivers" runat="server" onkeypress='return event.charCode >= 48 && event.charCode <= 57'></asp:TextBox>
```
- **Event**: onkeypress
- **Function**: Character code validation (48-57 = numeric 0-9)
- **Action**: Prevent non-numeric character entry

### UW Questions Popup Events

#### Popup Initialization
**Source**: ctlUWQuestionsPopup.ascx, function InitKillQuestions(), lines 100-120
```javascript
function InitKillQuestions() {
    if (DialogInitedKillQuestions == false) {
        DialogInitedKillQuestions = true;
        $("#divUwQuestions").dialog({
            title: "Underwriting Questions",
            width: popupDialogWidth,              
            draggable: false,
            autoOpen: true,
            dialogClass: "no-close"
        });
    }
}
```
- **Event**: ShowUwQuestions() call
- **Action**: Initialize jQuery dialog popup
- **Behavior**: Modal dialog, non-draggable, no close button

#### Form Validation Events
**Source**: ctlUWQuestionsPopup.ascx, function ValidateUWForm(), lines 650-700
```javascript
function ValidateUWForm() {
    isSubmitting = true;
    var a1 = AllAnswersAreAnswered()
    var a2 = AllAdditionalInfoFieldsAreAnswered();
    var a3 = ValidateEffectiveDate();       
    // ... additional validations
    return (a1 && a2 && a3 && a4 && a5 && a6 && a7 && hasGoverningState && ohCheck);
}
```
- **Event**: btnSave OnClientClick
- **Function**: Comprehensive form validation
- **Return**: Boolean (prevents/allows server submission)

#### Dynamic Question Visibility
**Source**: ctlUWQuestionsPopup.ascx, function ShowHideAdditionalInfo(), lines 300-320
```javascript
function ShowHideAdditionalInfo() {
    $('#tblKillQuestions > tbody  > tr').each(function () {
        if (index % 2 == 0) {
            if ($(this).find('input').first().is(':checked')) {
                $(this).next().show();
            } else {
                $(this).next().hide();
            }
        }
        index += 1;
    });
}
```
- **Event**: Radio button change events
- **Action**: Show/hide additional information textareas
- **Logic**: Show textarea when "Yes" selected, hide when "No" selected

## SERVER-SIDE EVENT TRACING

### Save Operations Workflow

#### Section-Specific Save Events
**Source**: ctl_WCP_Coverages.ascx, lines 15-20, 55-60, 125-130
```html
<asp:LinkButton ID="lnkSaveGeneralInfo" runat="server">Save</asp:LinkButton>
<asp:LinkButton ID="btnSaveClassifications" runat="server">Save</asp:LinkButton>  
<asp:LinkButton ID="lnkSaveEndorsements" runat="server">Save</asp:LinkButton>
```
- **General Info Save**: Experience Mod + Employer's Liability data
- **Classifications Save**: All classification data collectively
- **Endorsements Save**: Checkbox selections and waiver counts

#### Classification Individual Save Requirement
**Source**: ctl_WCP_Classification.ascx, lines 5-10, 50-52
```html
<asp:LinkButton ID="lnkSave" runat="server">Save</asp:LinkButton>
<!-- Warning Text -->
<td>You <b><u>MUST</u></b> click save after entering each classification!</td>
```
- **Event**: Individual classification save
- **Business Rule**: Each class code + payroll pair must be saved individually
- **Workflow Impact**: Prevents data loss, ensures proper rating

### Quote Processing Workflow

#### Rate This Quote Events
**Source**: ctl_WCP_Coverages.ascx, lines 130-135
```html
<asp:Button ID="btnSaveAndRate" runat="server" Text="Rate This Quote" CssClass="StandardSaveButton" />
```
- **Event**: btnSaveAndRate Click
- **Action**: Save all WCP data + initiate rating process
- **Workflow**: Final step in WCP data entry before quote results

#### Email UW Assistance  
**Source**: ctl_WCP_Coverages.ascx, lines 135-140
```html
<input type="button" id="btnEmailForUWAssistance" runat="server" onclick="InitEmailToUW();" title="Email for UW Assistance" value="Email for UW Assistance" class="StandardSaveButton" />
```
- **Event**: onclick client-side event
- **Function**: InitEmailToUW() JavaScript function
- **Action**: Launch underwriter assistance email workflow

### Class Code Lookup Workflow
**Source**: ctl_WCP_Classification.ascx, lines 25-30
```html
<asp:Button ID="btnClassCodeLookup" CssClass="standardSaveButton" runat="server" Text="Class Code Lookup" />
```
- **Event**: Server-side click event
- **Action**: Open class code lookup dialog/popup
- **Integration**: Connects to VrClassCodes.js functionality

## WORKFLOW ORCHESTRATION

### WCP Quote Workflow Sequence
**Source**: ctl_WorkflowMgr_Quote_WCP.ascx overall structure
1. **UW Questions Popup**: First interaction - kill questions validation
2. **General Information**: Experience mod and employer's liability entry
3. **Location Information**: Address entry (can be multiple)
4. **Classification Entry**: Class code lookup + payroll entry (iterative)
5. **Endorsement Selection**: State-specific endorsement options
6. **Final Rating**: Save all sections + rate quote

### Validation Gates
- **UW Questions**: Must pass all 6 kill questions to continue
- **Required Fields**: All starred fields must be completed
- **Classification Save**: Each classification must be individually saved
- **Final Validation**: All sections validated before rating

## CROSS-SYSTEM INTEGRATIONS

### TreeView Navigation
**Source**: ctl_WorkflowMgr_Quote_WCP.ascx, lines 20-25
```html
<uc1:ctlTreeView runat="server" ID="ctlTreeView" />
```
- **Event**: Tree node selection
- **Action**: Show/hide appropriate section divs
- **Workflow**: Section-based navigation control

### IRPM Integration  
**Source**: ctl_WorkflowMgr_Quote_WCP.ascx, line 35
```html
<uc1:ctlCommercial_IRPM runat="server" ID="ctl_WCP_IRPM" />
```
- **Integration**: Insurance Rate and Premium Management system
- **Event**: Rating calculation triggers
- **Action**: Premium and rate factor calculations

### Attachment Upload
**Source**: ctl_WorkflowMgr_Quote_WCP.ascx, line 30
```html
<uc1:ctl_AttachmentUpload runat="server" ID="ctl_AttachmentUpload" />
```
- **Event**: File upload operations
- **Action**: Supporting document attachment to quote
- **Workflow**: Optional supporting documentation

## EVIDENCE STATUS: ✅ VERIFIED FROM SOURCE CODE
All event workflows traced through JavaScript functions, server controls, and workflow container structure. Methods and functions identified with specific file and line references.