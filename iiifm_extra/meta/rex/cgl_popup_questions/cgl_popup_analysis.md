# CGL (Commercial General Liability) Popup Window Questions Analysis

## OVERVIEW
**STATUS**: ✅ COMPLETE - 6 CGL popup questions found and verified
**PATTERN MATCH**: Identical architecture to WCP popup questions
**TOTAL QUESTIONS**: 6 kill questions
**POPUP CONTROL**: ctlUWQuestionsPopup.ascx (same as WCP)

## SOURCE CODE EVIDENCE

### Primary Function: GetKillQuestions
**File**: `UWQuestions.vb`
**Lines**: 48-51
**Code Reference**:
```vb
Case QuickQuoteObject.QuickQuoteLobType.CommercialGeneralLiability '"9"
    'CGL
    Dim killQuestionCodes As New List(Of String) From {"9345", "9346", "9347", "9348", "9349", "9350"}
    Return (From uw In GetCGLUnderwritingQuestions() Where killQuestionCodes.Contains(uw.PolicyUnderwritingCodeId) Select uw).ToList()
```

### Question Content Function: GetCGLUnderwritingQuestions
**File**: `UWQuestions.vb`
**Lines**: 961-1009
**Function**: Returns List(Of VRUWQuestion) with complete question definitions

## CGL POPUP QUESTIONS (6 TOTAL)

### Question 1 - Coverage History
- **Code**: "9345"
- **Text**: "1. Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"
- **Line**: 966-971
- **IsTrueUwQuestion**: True

### Question 2 - Sexual Abuse/Discrimination Claims
- **Code**: "9346" 
- **Text**: "2. Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
- **Line**: 973-978
- **IsTrueUwQuestion**: True

### Question 3 - Explosive Materials
- **Code**: "9347"
- **Text**: "3. Do any operations include blasting or utilize or store explosive material?"
- **Line**: 980-985
- **IsTrueUwQuestion**: True

### Question 4 - Subcontractor Insurance
- **Code**: "9348"
- **Text**: "4. Are subcontractors allowed to work without providing you with a certificate of insurance?"
- **Line**: 987-992
- **IsTrueUwQuestion**: True

### Question 5 - Equipment Leasing
- **Code**: "9349"
- **Text**: "5. Does applicant lease equipment to others with or without operators?"
- **Line**: 994-999
- **IsTrueUwQuestion**: True

### Question 6 - Aircraft/Space Industry
- **Code**: "9350"
- **Text**: "6. Any products related to the aircraft or space industry?"
- **Line**: 1001-1006
- **IsTrueUwQuestion**: True

## TECHNICAL ARCHITECTURE

### Popup Implementation Pattern
- **LOB Type**: QuickQuoteObject.QuickQuoteLobType.CommercialGeneralLiability ("9")
- **Filter Logic**: LINQ query filtering GetCGLUnderwritingQuestions() by kill question codes
- **UI Control**: Same ctlUWQuestionsPopup.ascx modal as WCP
- **Question Structure**: VRUWQuestion objects with standardized properties

### Code Pattern Consistency
✅ **Same Function Architecture**: GetKillQuestions switch/case pattern
✅ **Same LOB Detection**: QuickQuoteLobType enumeration
✅ **Same Question Codes**: String list pattern ("9345", "9346", etc.)
✅ **Same UI Modal**: ctlUWQuestionsPopup.ascx control
✅ **Same Data Structure**: VRUWQuestion with IsTrueUwQuestion flag

## BUSINESS LOGIC PATTERNS

### Risk Assessment Focus
- **Coverage History**: Prior declinations/cancellations (high risk indicator)
- **Legal/Discrimination Risk**: Sexual abuse, molestation, discrimination claims
- **Explosive/Hazardous Operations**: Blasting, explosive materials storage
- **Contractor Risk Management**: Subcontractor insurance requirements
- **Equipment Liability**: Leasing operations with/without operators
- **Specialized Industry Risk**: Aircraft/space industry products

### Kill Question Behavior
- All 6 questions marked as `IsTrueUwQuestion = True`
- "Yes" answers to any question trigger underwriting review/decline
- Questions numbered 1-6 sequentially in popup display
- Each question targets specific commercial liability exposures

## COMPARISON TO WCP PATTERN

| Aspect | WCP | CGL | Match |
|--------|-----|-----|-------|
| Total Questions | 6 | 6 | ✅ |
| Function Pattern | GetKillQuestions case | GetKillQuestions case | ✅ |
| Code Structure | List(Of String) codes | List(Of String) codes | ✅ |
| UI Control | ctlUWQuestionsPopup.ascx | ctlUWQuestionsPopup.ascx | ✅ |
| LINQ Filter | killQuestionCodes.Contains | killQuestionCodes.Contains | ✅ |
| Question Object | VRUWQuestion | VRUWQuestion | ✅ |

## VERIFICATION STATUS
- ✅ **Source Code Located**: UWQuestions.vb confirmed
- ✅ **Function Found**: GetKillQuestions CGL case verified
- ✅ **Question Codes Extracted**: 6 codes confirmed (9345-9350)
- ✅ **Question Text Retrieved**: All 6 questions with exact wording
- ✅ **Architecture Verified**: Same popup control pattern as WCP
- ✅ **Business Logic Documented**: Risk assessment patterns identified

**EVIDENCE QUALITY**: HIGH - All claims backed by specific source code lines and exact code quotes.