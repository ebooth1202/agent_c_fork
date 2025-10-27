# BOP Popup Questions - Pattern Mining Results

## FROM: Rex (Pattern Mining Specialist)
## TO: Douglas IFI Orchestrator
## FEATURE: BOP Kill Questions Popup Modal

## EXECUTIVE SUMMARY (Complete Pattern Match Achieved)
Successfully identified **6 BOP kill questions** using the established WCP/CGL pattern. Found exact code implementation in `UWQuestions.vb` with verified question content from `GetCommercialBOPUnderwritingQuestions()` function. BOP follows identical technical pattern: 6 questions, same modal control (`ctlUWQuestionsPopup.ascx`), sequential auto-numbering, all required fields.

## KEY FINDINGS

### 1. BOP Kill Question Implementation (VERIFIED)
- **Source**: `UWQuestions.vb`, lines 52-62
- **Case**: `QuickQuoteObject.QuickQuoteLobType.CommercialBOP '"25"`
- **Codes**: `{"9003", "9006", "9007", "9008", "9009", "9400"}` 
- **Count**: 6 questions (matches WCP and CGL pattern)

### 2. Question Content Function (VERIFIED)
- **Function**: `GetCommercialBOPUnderwritingQuestions()` (line 1012)
- **Processing**: Auto-numbered display (1. 2. 3. etc.)
- **Field Used**: `kqDescription` for actual popup text

### 3. Complete BOP Question List (VERIFIED)
1. **9003**: "Any exposure to flammables, explosives, chemicals?"
2. **9006**: "Any policy or coverage declined, cancelled or non-renewed during the prior 3 years?"  
3. **9007**: "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
4. **9008**: "During the last 5 years, has any applicant been indicted for or convicted of any degree of the crime of fraud, bribery, arson, or any other arson-related crime?" **(TRUE KILL QUESTION)**
5. **9009**: "Any uncorrected fire code violations?"
6. **9400**: "Any bankruptcies, tax or credit liens against the applicant in the past 5 years?"

### 4. Technical Pattern Consistency (VERIFIED)
✅ Same `ctlUWQuestionsPopup.ascx` modal control  
✅ Identical LINQ filtering by kill question codes  
✅ Sequential numbering processing loop  
✅ All questions marked as required (`IsQuestionRequired = True`)  
✅ Same question structure with Description and kqDescription fields  

### 5. Special BOP Characteristics (VERIFIED)
- **One True Kill**: Question 9008 has `IsTrueKillQuestion = True` (immediately stops quote)
- **Five UW Questions**: Remaining questions collect info for underwriting review
- **All Required**: Every kill question marked as required field
- **Commercial Focus**: Business-oriented questions (applicant, property, operations)

## METADATA LOCATIONS
- **Pattern Analysis**: `//ifm/meta/rex/bop_popup_questions/bop_kill_questions_analysis.md`
- **Summary Findings**: `//ifm/meta/rex/bop_popup_questions/bop_findings_summary.md`

## COMPLETENESS: HIGH
**STATUS: COMPLETE**

All 6 BOP popup questions successfully identified with:
- ✅ Source code evidence and line references
- ✅ Exact question text from kqDescription fields  
- ✅ Technical implementation details verified
- ✅ Pattern consistency with WCP/CGL confirmed
- ✅ Special kill question behavior documented

## LOB PATTERN SUMMARY
- **WCP**: 6 questions (9341, 9086, 9342/9573, 9343, 9344, 9107)
- **CGL**: 6 questions (9345, 9346, 9347, 9348, 9349, 9350)  
- **BOP**: 6 questions (9003, 9006, 9007, 9008, 9009, 9400) ✅ **COMPLETE**

**PATTERN ESTABLISHED**: All three Commercial LOBs follow identical 6-question kill question popup structure with same technical implementation approach.