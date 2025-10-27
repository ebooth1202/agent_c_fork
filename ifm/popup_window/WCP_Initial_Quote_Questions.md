# WCP Initial Quote Questions - UI Popup Modal

**Analysis Date**: October 27, 2025  
**Source System**: VelociRater Insurance Rating Engine  
**LOB**: Workers' Compensation Policy (WCP)  
**Question Type**: Kill Questions (Initial Quote Popup Modal)  

## Overview

This document contains the 6 WCP-specific initial quote questions that appear in popup modal windows during the initial quote process in the VelociRater system. These questions are technically termed "kill questions" in the codebase and serve as pre-qualification filters.

:::important
**QuickQuote System Integration**: These WCP questions are part of the QuickQuote object implementation. VelociRater is built on the QuickQuote framework, and the UWQuestions system IS the "quick quote object" method that handles initial quote workflows.
:::

## Source Code Reference

**Primary Source File**: `//project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/IFM.VR.Common/UWQuestions/UWQuestions.vb`  
**Method**: `GetCommercialWCPUnderwritingQuestions()` (Lines 1856-2248)  
**Kill Question Definition**: Lines 82-84  
**QuickQuote Integration**: Lines 81-90 show `QuickQuoteObject.QuickQuoteLobType.WorkersCompensation` case handling

### QuickQuote Architecture Context

**Framework**: VelociRater is built on QuickQuote.CommonObjects  
**Import**: `Imports QuickQuote.CommonObjects`  
**Helper Class**: Uses `QuickQuote.CommonMethods.QuickQuoteHelperClass`  
**WCP Handler**: `QuickQuoteObject.QuickQuoteLobType.WorkersCompensation` case processes these 6 kill questions  

---

## WCP Initial Quote Questions

### Question 1: Aircraft/Watercraft Ownership
- **Question Text**: "Does Applicant own, operate or lease aircraft or watercraft?"
- **Diamond Code**: 9341
- **Section**: Risk Grade Questions
- **Required**: Yes
- **Source Reference**: Lines 1869-1879, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

### Question 2: Hazardous Materials
- **Question Text**: "Do/have past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material? (e.g. landfills, wastes, fuel tanks, etc.)"
- **Diamond Code**: 9086
- **Section**: Risk Grade Questions
- **Required**: Yes
- **Source Reference**: Lines 1882-1892, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

### Question 3: Employee Residence (Conditional Logic)

:::important
**Note**: This question has two versions based on effective date logic
:::

#### Version A: Multi-State Version
- **Question Text**: "Do any employees live outside the state(s) of Indiana, Illinois, or Kentucky?"
- **Diamond Code**: 9573
- **Condition**: For effective dates >= Kentucky WCP effective date
- **Source Reference**: Lines 1894-1911, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 84)

#### Version B: Single-State Version  
- **Question Text**: "Do any employees live outside the state of {governingStateString}?"
- **Diamond Code**: 9342
- **Condition**: For non-multi-state effective dates
- **Source Reference**: Lines 1914-1925, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

**Conditional Logic**: 
- Uses `IFM.VR.Common.Helpers.MultiState.General.IsMultistateCapableEffectiveDate()`
- Governing state string is dynamically populated based on acceptable states

### Question 4: Prior Coverage Issues
- **Question Text**: "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"
- **Diamond Code**: 9343
- **Section**: Risk Grade Questions
- **Required**: Yes
- **Source Reference**: Lines 1929-1939, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

### Question 5: Professional Employment Organization
- **Question Text**: "Is the Applicant involved in the operation of a professional employment organization, employee leasing operation, or temporary employment agency?"
- **Diamond Code**: 9344
- **Section**: Risk Grade Questions
- **Required**: Yes
- **Source Reference**: Lines 1942-1952, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

### Question 6: Financial Issues
- **Question Text**: "Any tax liens or bankruptcy within the last 5 years? (If 'Yes', please specify)"
- **Diamond Code**: 9107
- **Section**: Workers Compensation
- **Required**: Yes
- **Kill Question Indicator**: `IsTrueKillQuestion = True`
- **Source Reference**: Lines 2222-2233, UWQuestions.vb
- **Kill Question Status**: Confirmed (Line 82)

---

## Technical Implementation Details

### UI Control Implementation
- **Main Control**: `IFM.VR.Web/User Controls/VR Commercial/Application/BOP/ctlCommercialUWQuestionList.ascx`
- **JavaScript Handler**: `HandleRadioButtonClicksWCP()` function (Lines 369-392)

### Kill Question Processing Logic
```javascript
// Diamond code 9107 triggers ineligibility workflow
case 9107:
    ans = confirm("The risk is ineligible, if answered 'Yes' in error select 'Cancel'. If answered correctly, select 'OK'")
    if (ans == true) {
        ArchiveQuote(); // Archives quote and returns to MyVelocirater
    }
```

### Question Logic Summary
- **Total Questions**: 6 (with Question 3 having conditional versions)
- **All Required**: Yes
- **Kill Question Behavior**: "Yes" answers typically trigger ineligibility workflow
- **UI Pattern**: Popup modal with radio button selections
- **Processing**: JavaScript validation with confirmation dialogs

---

## Quality Verification

:::tip
**Extraction Quality Standards Met**:
- ✅ All 6 questions have verified source code references
- ✅ All diamond codes confirmed in kill question list  
- ✅ UI implementation verified with JavaScript handling
- ✅ No assumptions made - all content source-verified
- ✅ WCP-specific focus maintained - no cross-LOB contamination
- ✅ Completeness: HIGH - Complete extraction with full source traceability
:::

---

**Extracted by**: Douglas (IFI Analysis Team Orchestrator)  
**Pattern Mining by**: Rex (IFI Pattern Miner Enhanced)  
**Date**: October 27, 2025  
**File Location**: `//project/ifm/popup_window/WCP_Initial_Quote_Questions.md`