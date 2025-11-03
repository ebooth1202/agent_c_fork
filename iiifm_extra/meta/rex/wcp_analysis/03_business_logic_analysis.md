# WCP LOB - Step 3: Business Logic Analysis

## SOURCE EVIDENCE
- **UW Questions Logic**: UWQuestions.vb, lines 80-88, 1856-2233
- **Multi-State Logic**: UWQuestions.vb, lines 83-85, 1894-1925
- **Rating Logic**: ctl_WCP_Coverages.ascx AutoPostBack behaviors
- **State Logic**: ctl_WCP_Coverages.ascx conditional endorsement rendering

## KILL QUESTIONS BUSINESS LOGIC

### QuickQuote System Integration
**Source**: UWQuestions.vb, GetCommercialWCPUnderwritingQuestions method, lines 1856-2233
- **System Architecture**: WCP fully integrated with QuickQuote framework
- **Question Loading**: Dynamic loading via `GetCommercialWCPUnderwritingQuestions(effectiveDate)`
- **Kill Question Filtering**: Only 6 specific questions shown in popup (lines 82-87)

### Multi-State Logic Variations
**Source**: UWQuestions.vb, lines 82-85, 1894-1925
```vb
If (IFM.VR.Common.Helpers.MultiState.General.IsMultistateCapableEffectiveDate(effDate)) Then
    killQuestionCodes = New List(Of String) From {"9341", "9086", "9573", "9343", "9344", "9107"}
Else
    killQuestionCodes = New List(Of String) From {"9341", "9086", "9342", "9343", "9344", "9107"}
```
- **Single State**: Uses question code 9342 for employee residency
- **Multi-State**: Uses question code 9573 for employee residency
- **Effective Date Dependency**: Logic varies based on policy effective date

### Question 3 State-Specific Logic
**Source**: UWQuestions.vb, lines 1894-1925
```vb
Dim dscr As String = $"3. Do any employees live outside the state(s) of {governingStateString}?"
If effDate >= CDate(IFM.VR.Common.Helpers.MultiState.General.KentuckyWCPEffectiveDate).Date Then
    dscr = "3. Do any employees live outside the state(s) of Indiana, Illinois, or Kentucky?"
```
- **Dynamic Question Text**: Incorporates governing state(s) from LOBHelper
- **Kentucky Enhancement**: Specific hardcoded text when KY WCP effective date reached
- **Multi-State Capability**: Question adapts to available states for effective date

## EXPERIENCE MODIFICATION BUSINESS LOGIC

### Rating Integration
**Source**: ctl_WCP_Coverages.ascx, line 37
```html
<asp:TextBox ID="txtExpMod" runat="server" AutoPostBack="true"></asp:TextBox>
```
- **Immediate Rating Impact**: AutoPostBack triggers server-side rate recalculation
- **Rating Dependency**: Experience mod directly affects premium calculation
- **Required for UW**: Must be entered for quote completion

### Effective Date Requirement  
**Source**: ctl_WCP_Coverages.ascx, lines 40-45
- **Business Rule**: Experience modification requires associated effective date
- **UW Validation**: Both fields required for proper underwriting assessment

## CLASS CODE BUSINESS LOGIC

### Lookup System Integration
**Source**: ctl_WCP_Classification.ascx, lines 20-35
```html
<uc1:ctl_WCP_ClassCodeLookup id="ctl_ClassCodeLookup" runat="server"></uc1:ctl_WCP_ClassCodeLookup>
<asp:Button ID="btnClassCodeLookup" CssClass="standardSaveButton" runat="server" Text="Class Code Lookup" />
```
- **Lookup Dependency**: Class codes must be selected via lookup (not manually entered)
- **Description Population**: Class code description auto-populated from lookup
- **Read-Only Fields**: Prevents manual manipulation of class code data

### Payroll Business Rules
**Source**: ctl_WCP_Classification.ascx, lines 30-35
- **Required Field**: Payroll mandatory for each classification
- **Rating Impact**: Payroll directly affects premium calculation per class code
- **Save Requirement**: Each classification must be individually saved

### Multiple Classification Support
**Source**: ctl_WCP_Coverages.ascx, lines 55-65
```html
<asp:Repeater ID="rptClassifications" runat="server">
    <ItemTemplate>
        <uc1:ctl_WCP_Classification id="ctl_Classification" runat="server" />
    </ItemTemplate>
</asp:Repeater>
```
- **Dynamic Classifications**: Support for multiple class codes per policy
- **Individual Management**: Each classification managed independently
- **Business Logic**: Reflects real-world business operations with multiple work types

## ENDORSEMENT BUSINESS LOGIC

### State-Specific Availability  
**Source**: ctl_WCP_Coverages.ascx, lines 85-127
- **Indiana Only**: Exclusion of Amish Workers (WC 00 03 08)(IN)
- **Indiana Only**: Exclusion of Executive Officer (WC 00 03 08)(IN) 
- **Illinois Only**: Exclusion of Sole Proprietors, Partners, Officers, LLC Members (WC 12 03 07)(IL)
- **Kentucky Only**: Rejection of Coverage Endorsement (WC 16 03 01)(KY)
- **IN/IL Combined**: Inclusion of Sole Proprietors (WC 00 03 10)(IN/IL)

### Waiver Logic
**Source**: ctl_WCP_Coverages.ascx, lines 90-115
- **Blanket vs Individual**: Two waiver options with different forms
- **Numeric Dependency**: Individual waiver requires count of waivers
- **Business Rule**: Blanket waiver doesn't require count, individual waiver does

### Indiana State Form Requirement
**Source**: ctl_WCP_Coverages.ascx, lines 120-125
```html
The State of Indiana requires that you complete and submit form 36097 (Notice For Workers Compensation And Occupational Diseases Coverage) when excluding officers from workers compensation coverage.
```
- **Regulatory Compliance**: Indiana-specific form requirement
- **Documentation**: Links to state form and submission instructions
- **UW Process**: Copy must be submitted to underwriter

## EMPLOYER'S LIABILITY BUSINESS LOGIC

### Umbrella Coordination
**Source**: ctl_WCP_Coverages.ascx, lines 25-30
```html
<span>We require minimum limits of 500/500/500 when quoting an umbrella.</span>
```
- **Cross-LOB Dependency**: Employer's Liability limits affect umbrella eligibility
- **Minimum Limits Rule**: 500/500/500 required for umbrella coordination
- **Business Logic**: Prevents inadequate underlying coverage

## LOCATION BUSINESS LOGIC

### Multi-Location Support
**Source**: ctl_WCP_LocationList.ascx + ctl_WCP_Location.ascx
- **Business Reality**: WCP supports multiple work locations
- **Address Reuse**: Leverages existing property address control
- **Individual Management**: Each location managed independently

## CROSS-DEPENDENCIES IDENTIFIED

### Policy Integration
- **Experience Mod ↔ Rating**: Direct rating impact
- **Class Codes ↔ Payroll**: Combined for premium calculation  
- **Employer's Liability ↔ Umbrella**: Cross-LOB coordination
- **UW Questions ↔ Quote Approval**: Kill questions affect quotability

### Regulatory Logic
- **State ↔ Endorsements**: State-specific form availability
- **State ↔ UW Questions**: Question text varies by governing state
- **Effective Date ↔ Multi-State**: Date determines multi-state capability

## EVIDENCE STATUS: ✅ VERIFIED FROM SOURCE CODE
All business logic patterns verified through code analysis. Complex interdependencies documented with specific file and line references.