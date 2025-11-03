# WCP Underwriting Questions Popup Modal Patterns

## MODAL IMPLEMENTATION: ctlUWQuestionsPopup.ascx

**Source Evidence**: `//project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/IFM.VR.Web/User Controls/ctlUWQuestionsPopup.ascx`

### Modal Window Implementation Pattern
- **Type**: jQuery UI Dialog
- **Configuration**:
  - Title: "Underwriting Questions"
  - Width: 550px (variable `popupDialogWidth`)
  - Draggable: false
  - AutoOpen: true
  - Modal: commented out (not modal)
  - DialogClass: "no-close"

**Implementation Code (Lines 123-132)**:
```javascript
$("#<%=Me.divUwQuestions.ClientId%>").dialog({
    title: "Underwriting Questions",
    width: popupDialogWidth,              
    draggable: false,
    autoOpen: true,
    //modal: true,
    dialogClass: "no-close"
});
```

### Question Structure Patterns

#### 1. **Dynamic Kill Questions Table**
- **Table ID**: `tblKillQuestions`
- **Structure**: Repeater-driven alternating rows
- **Pattern**: Question row followed by Additional Information row
- **Fields per Question**:
  - Yes/No radio buttons
  - Additional Information textarea (90% width, multiline)
  - Hidden field for PolicyUnderwritingCodeId

**Repeater Template Structure**:
```html
<tr style="background-color: lightgray;">
    <td style="width: 400px;"><%# DataBinder.Eval(Container.DataItem, "Description_NoQuestionNumber")%></td>
    <td style="width: 70px;">
        <span style="display: none; font-size: 15pt; color: red;">*</span>
        <asp:RadioButton ID="radYes" Text="Yes" runat="server" />
    </td>
    <td><asp:RadioButton ID="radNo" Text="No" runat="server" /></td>
</tr>
<tr>
    <td colspan="3">
        <div style="margin-left: 30px;">
            <span>Additional Information</span><br />
            <asp:TextBox ID="txtMoreInfo" Width="90%" TextMode="MultiLine" runat="server"></asp:TextBox>
        </div>
    </td>
</tr>
```

#### 2. **LOB-Specific Question Sections**

**WCP-Specific Questions**: Not explicitly shown in this control, but framework exists for Commercial LOBs through `kqLobId == IFMLOBEnum.WCP.LobId` JavaScript variable.

**BOP Additional Questions** (Lines 889-952):
- Condo Directors & Officers coverage question
- Building size questions (over 35,000 sq ft, over 3 stories)
- Gross sales threshold ($6M+)
- Incidental occupancies with conditional textarea

**Example BOP Question**:
```html
<tr>
    <td>Is any building over 35,000 feet in total area?</td>
    <td><asp:RadioButton GroupName="bop_Over35k" ID="radBOPOver35kYes" Text="Yes" /></td>
    <td><asp:RadioButton GroupName="bop_Over35k" ID="radBOPOver35kNo" Text="No" /></td>
</tr>
```

#### 3. **Effective Date Integration**
**Pattern**: All UW questions modals include effective date picker with extensive validation
**Implementation**:
- jQuery UI datepicker with month/year selection
- Date mask: "00/00/0000"
- Min/max date validation from hidden fields
- Real-time validation with error display

**Validation Fields**:
```html
<input id="hdnAppMinimumEffectiveDate" type="hidden" runat="server" />
<input id="hdnAppMaximumEffectiveDate" type="hidden" runat="server" />
<asp:label ID="lblEffectiveDateError" ForeColor="Red" />
```

### Extra Info Box Requirements

#### Conditional Display Logic
**Function**: `ShowHideAdditionalInfo()` (Lines 267-279)
**Pattern**: For every question row, if "Yes" is selected, show the additional info textarea

**Implementation**:
```javascript
$('#tblKillQuestions > tbody > tr').each(function () {
    if (index % 2 == 0) {
        if ($(this).find('input').first().is(':checked')) {
            $(this).next().show();  // Show additional info row
        } else {
            $(this).next().hide();  // Hide additional info row
        }
    }
    index += 1;
});
```

#### Required Additional Information
**Validation**: `AllAdditionalInfoFieldsAreAnswered()` (Lines 504-528)
**Rule**: When "Yes" is selected, additional information textarea becomes required
**Visual Indicator**: Red border and error message for empty required fields

**Validation Code**:
```javascript
if ($(this).next().find('textarea').first().val() == '') {
    All_IfYesHasAdditionalInfo = false;
    $(this).next().find('textarea').first().attr('style', 'border: 1px solid red; width: 100%;');
    $(this).next().find('span').first().css('color', 'red');
    $(this).next().find('span').first().text("Additional Information Response Required");
}
```

### Validation Logic Patterns

#### 1. **Complete Answer Validation**
**Function**: `AllAnswersAreAnswered()` (Lines 282-502)
**Requirements**:
- All questions must have Yes or No selected
- Visual indicators (red asterisk) for missing answers
- Question-specific validation for additional fields

#### 2. **Form Submission Validation**
**Function**: `ValidateUWForm()` (Lines 824-870)
**Validation Chain**:
1. All answers provided
2. All additional info fields completed
3. Effective date valid
4. LOB-specific additional questions answered
5. Governing state selected

**Submission Code**:
```javascript
function ValidateUWForm() {
    var a1 = AllAnswersAreAnswered()
    var a2 = AllAdditionalInfoFieldsAreAnswered();
    var a3 = ValidateEffectiveDate();       
    var a4 = AllPPAAdditionalInfoFieldsAreAnswered();
    var a5 = AllBOPAdditionalInfoFieldsAreAnswered();
    // ... additional validations
    return (a1 && a2 && a3 && a4 && a5 && ...);
}
```

### Modal Display Triggers

#### JavaScript Show/Hide Functions
**Show Modal**: `ShowUwQuestions()` (Lines 134-233)
- Initializes dialog if not already created
- Sets up LOB-specific conditional logic
- Configures date picker and validation

**Hide Modal**: `HideUwQuestions()` (Lines 235-238)
- Closes jQuery UI dialog
- Maintains form state

### Form Integration Pattern
**Integration**: Modal appends to main form to maintain postback context
**Code**: `$("#<%=Me.divUwQuestions.ClientId%>").parent().appendTo(jQuery("form:first"));`

## EVIDENCE STATUS
**Verification**: CONFIRMED - Source code examined with line references
**Modal Type**: jQuery UI Dialog with custom validation framework
**Question Structure**: Repeater-driven with conditional additional information sections
**Integration**: Embedded in WCP Quote workflow manager