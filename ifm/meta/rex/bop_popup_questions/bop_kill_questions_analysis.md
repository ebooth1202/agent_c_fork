# BOP (Business Owners Policy) Popup Questions Analysis

## Executive Summary
Successfully identified **6 BOP kill questions** following the established pattern from WCP and CGL LOBs. All questions found in the `GetCommercialBOPUnderwritingQuestions()` function with corresponding `kqDescription` fields for popup display.

## Source Code Evidence

### Kill Questions Function Location
- **File**: `UWQuestions.vb`
- **Function**: `GetKillQuestions()` (line 23)
- **BOP Case**: Lines 52-62
- **Case Statement**: `QuickQuoteObject.QuickQuoteLobType.CommercialBOP '"25"`

### BOP Kill Question Codes (Line 54)
```vb
Dim killQuestionCodes As New List(Of String) From {"9003", "9006", "9007", "9008", "9009", "9400"}
```

### Question Content Function
- **Function**: `GetCommercialBOPUnderwritingQuestions()` (line 1012)
- **LINQ Query**: Line 55 filters questions by kill question codes
- **Special Processing**: Questions are automatically numbered (1. 2. 3. etc.) in popup display

## Complete BOP Kill Questions List

### Question 1: Code 9003
- **Source**: Lines 1101-1111
- **Popup Text**: "Any exposure to flammables, explosives, chemicals?"
- **Full Description**: "3. Any exposure to flammables, explosives, chemicals?"
- **Required**: Yes
- **Kill Status**: Standard UW Question

### Question 2: Code 9006
- **Source**: Lines 1125-1135  
- **Popup Text**: "Any policy or coverage declined, cancelled or non-renewed during the prior 3 years?"
- **Full Description**: "5. Any policy or coverage declined, cancelled or non-renewed during the prior 3 years for any premises or operations?"
- **Required**: Yes
- **Kill Status**: Standard UW Question

### Question 3: Code 9007
- **Source**: Lines 1138-1148
- **Popup Text**: "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
- **Full Description**: "6. Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
- **Required**: Yes
- **Kill Status**: Standard UW Question

### Question 4: Code 9008
- **Source**: Lines 1151-1162
- **Popup Text**: "During the last 5 years, has any applicant been indicted for or convicted of any degree of the crime of fraud, bribery, arson, or any other arson-related crime in the connection with this or any other property?"
- **Full Description**: "7. During the last five years has any Applicant been indicted for or convicted of any degree of the crime of fraud, bribery, arson or any other arson-related crime in connection with this or any other property?"
- **Required**: Yes
- **Kill Status**: **TRUE KILL QUESTION** (.IsTrueKillQuestion = True)

### Question 5: Code 9009
- **Source**: Lines 1165-1175
- **Popup Text**: "Any uncorrected fire code violations?"
- **Full Description**: "8. Any uncorrected fire and/or safety code violations?"
- **Required**: Yes
- **Kill Status**: Standard UW Question

### Question 6: Code 9400
- **Source**: Lines 1178-1188
- **Popup Text**: "Any bankruptcies, tax or credit liens against the applicant in the past 5 years?"
- **Full Description**: "9. Has Applicant had a foreclosure, repossession, bankruptcy or filed for bankruptcy in the last five (5) years?"
- **Required**: Yes
- **Kill Status**: Standard UW Question

## Technical Implementation Details

### Popup Display Processing
- Questions are numbered sequentially (1, 2, 3, etc.) via loop processing (lines 57-61)
- `kqDescription` field contains the actual popup text shown to users
- Questions display in order of kill question codes list

### UI Control Integration  
- Uses same `ctlUWQuestionsPopup.ascx` modal control as WCP and CGL
- Modal triggered by "Yes" responses to kill questions during quote process
- All BOP kill questions marked as `IsQuestionRequired = True`

### Special Notes
- **Question 9008** is the only "True Kill Question" that immediately stops the quote process
- All other questions are "UW Questions" that collect information for underwriting review
- BOP follows identical pattern to WCP (6 questions) and CGL (6 questions)

## Pattern Consistency Verification

### Confirmed Pattern Match:
✅ **Kill Question Count**: 6 questions (matches WCP and CGL)  
✅ **Function Structure**: GetKillQuestions() → GetCommercialBOPUnderwritingQuestions()  
✅ **Code List Format**: List(Of String) From {...}  
✅ **Popup Control**: Same ctlUWQuestionsPopup.ascx modal  
✅ **Question Numbering**: Sequential auto-numbering in popup display  
✅ **Required Status**: All marked as required questions  

### LOB Comparison:
- **WCP**: 6 questions (codes 9341, 9086, 9342/9573, 9343, 9344, 9107)
- **CGL**: 6 questions (codes 9345, 9346, 9347, 9348, 9349, 9350) 
- **BOP**: 6 questions (codes 9003, 9006, 9007, 9008, 9009, 9400)

## Completeness Status
**COMPLETE** - All 6 BOP popup questions successfully identified with full source code evidence and exact question text verified.