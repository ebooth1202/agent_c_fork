# BOP Initial Quote Questions - QuickQuote Popup Analysis

## Overview
This document catalogs all questions that appear in the QuickQuote BOP popup UI window based on comprehensive source code analysis.

## Question Count Summary
**Total Questions: 11**

**Question Loading Pattern**: Hybrid approach using both dynamic kill questions and static conditional questions.

- **6 Dynamic Kill Questions** - Loaded from underwriting question system
- **5 Static Questions** - Hardcoded in UI with conditional visibility

## Complete Question List

### **DYNAMIC KILL QUESTIONS** (Questions 1-6)
**Loading Pattern**: Dynamically loaded via `UWQuestions.GetKillQuestions()` method
**Source**: `ctlUWQuestionsPopup.ascx.vb` lines 1027-1047 + `UWQuestions.vb` lines 52-62
**Question Codes**: {"9003", "9006", "9007", "9008", "9009", "9400"}

#### Question 1 (Code 9003): Flammables/Explosives
- **Text**: "Any exposure to flammables, explosives, chemicals?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

#### Question 2 (Code 9006): Prior Cancellations
- **Text**: "Any policy or coverage declined, cancelled or non-renewed during the prior 3 years?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

#### Question 3 (Code 9007): Sexual Abuse/Discrimination
- **Text**: "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

#### Question 4 (Code 9008): Criminal Convictions
- **Text**: "During the last 5 years, has any applicant been indicted for or convicted of any degree of the crime of fraud, bribery, arson, or any other arson-related crime in the connection with this or any other property?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

#### Question 5 (Code 9009): Fire Code Violations
- **Text**: "Any uncorrected fire code violations?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

#### Question 6 (Code 9400): Bankruptcy/Liens
- **Text**: "Any bankruptcies, tax or credit liens against the applicant in the past 5 years?"
- **UI Control Type**: Radio button (Yes/No)
- **Loading**: Dynamic via Repeater1.DataBind()
- **Business Rule**: Kill question - "Yes" answer stops quote process

### **STATIC HARDCODED QUESTIONS** (Questions 7-11)
**Loading Pattern**: Hardcoded in ASCX markup with conditional visibility
**Source**: `ctlUWQuestionsPopup.ascx` lines 909-985
**Visibility Control**: `BopStpUwQuestionsHelper.IsBopStpUwQuestionsAvailable()`

#### Question 7: Condo Directors & Officers
- **Text**: "Is this risk a condominium or homeowner association that requires Condo Directors & Officers coverage, and you want to place with us?"
- **Control ID**: `radBOPCondoDandO`
- **Group Name**: `bop_multi`
- **UI Control Type**: Radio button (Yes/No)
- **Visibility**: Always visible
- **Source**: ctlUWQuestionsPopup.ascx, Lines 909-916

#### Question 8: Building Size
- **Text**: "Is any building over 35,000 feet in total area?"
- **Control ID**: `radBOPOver35k`
- **Group Name**: `bop_Over35k`
- **UI Control Type**: Radio button (Yes/No)
- **Visibility**: Conditional (via `BopStpUwQuestionsHelper`)
- **Business Rule**: "Yes" answer redirects to CPP product line
- **Source**: ctlUWQuestionsPopup.ascx, Lines 919-926

#### Question 9: Building Height
- **Text**: "Does any building exceed 3 stories?"
- **Control ID**: `radBOPOver3Stories`
- **Group Name**: `bop_Over3Stories`
- **UI Control Type**: Radio button (Yes/No)
- **Visibility**: Conditional (via `BopStpUwQuestionsHelper`)
- **Business Rule**: "Yes" answer redirects to CPP product line
- **Source**: ctlUWQuestionsPopup.ascx, Lines 929-936

#### Question 10: Gross Sales
- **Text**: "Are gross sales $6,000,000 or more?"
- **Control ID**: `radBOPSales6M`
- **Group Name**: `bop_Sales6M`
- **UI Control Type**: Radio button (Yes/No)
- **Visibility**: Conditional (via `BopStpUwQuestionsHelper`)
- **Business Rule**: "Yes" answer redirects to CPP product line
- **Source**: ctlUWQuestionsPopup.ascx, Lines 939-946

#### Question 11: Incidental Occupancies
- **Text**: "Are there any incidental occupancies?"
- **Control ID**: `radBOPIncOcc`
- **Group Name**: `bop_IncOcc`
- **UI Control Type**: Radio button (Yes/No) with conditional text area
- **Visibility**: Conditional (via `BopStpUwQuestionsHelper`)
- **Conditional Logic**: If "Yes" is selected, shows additional text area for more information
- **Source**: ctlUWQuestionsPopup.ascx, Lines 949-985

## Technical Implementation Details

### Question Loading Architecture
**Hybrid Loading Pattern**: Combines dynamic database-driven questions with static conditional questions

#### Dynamic Question Loading
- **Source File**: `ctlUWQuestionsPopup.ascx.vb` lines 1027-1047
- **Method**: `VR.Common.UWQuestions.UWQuestions.GetKillQuestions(lobid, EffectiveDate)`
- **Configuration**: `UWQuestions.vb` lines 52-62 defines kill question codes
- **UI Container**: `tblKillQuestions` table (populated by Repeater1)
- **Data Binding**: `Me.Repeater1.DataSource = questions; Me.Repeater1.DataBind()`

#### Static Question Loading
- **Source File**: `ctlUWQuestionsPopup.ascx` lines 909-985
- **Container**: `divAdditionalBOPQuestions` div with class `tblBOPKillQuestions`
- **Visibility Control**: `BopStpUwQuestionsHelper.IsBopStpUwQuestionsAvailable(myQuote)`
- **Implementation Date**: 09/02/2021 (Bug 51550 MLW)

### Conditional Logic Implementation

#### Question Visibility Control
**File**: `ctlUWQuestionsPopup.ascx.vb` lines 1295-1307
```vb
If BopStpUwQuestionsHelper.IsBopStpUwQuestionsAvailable(myQuote) Then
    trBOPOver35k.Visible = True
    trBOPOver3Stories.Visible = True  
    trBOPSales6M.Visible = True
    radBOPIncOcc.Visible = True
Else
    [Questions 8-11 hidden]
End If
```

#### Additional Information Logic
**JavaScript Function**: `ShowHideBopAdditionalSections()` (Lines 68-76)
- Triggered when Question 11 (Incidental Occupancies) is answered "Yes"
- Shows additional information text area (`txtIncidentalOccupancyRelated`)
- Uses jQuery to show/hide UI elements

#### Business Rule Processing
- **Kill Questions (1-6)**: "Yes" answers terminate quote process
- **CPP Redirect Questions (8-10)**: "Yes" answers redirect quote to Commercial Package Policy product line
- **Save Logic**: Lines 2072-2096 in code-behind processes all BOP-specific question responses

## Content Type Classification
- **6 questions DYNAMICALLY LOADED** from underwriting question system
- **5 questions HARDCODED** in ASCX markup with conditional visibility
- **Mixed content approach** combining database-driven and static questions

## Validation Status
- ✅ **VERIFIED**: All 11 questions located with exact source references
- ✅ **VERIFIED**: Dynamic loading pattern identified and documented
- ✅ **VERIFIED**: Static hardcoded questions confirmed with conditional visibility
- ✅ **VERIFIED**: Business rule impacts documented (kill questions vs CPP redirect)
- ✅ **VERIFIED**: Complete popup architecture documented
- ✅ **VERIFIED**: Integration points and validation logic confirmed

## Key Discovery
**Previous Analysis Gap**: Initial analysis only found static hardcoded questions and missed the 6 dynamically loaded kill questions that form the core screening mechanism of the popup.

**Accurate Pattern**: BOP popup uses a hybrid approach combining:
1. **6 Dynamic Kill Questions** loaded from underwriting question database
2. **5 Static Questions** with conditional visibility based on business rules

---
*Analysis completed by Rex IFI Pattern Miner (Comprehensive Reassessment)*  
*Source Code Base: VelociRater WebSystems*  
*Analysis Date: October 27, 2025*