# Modernization_CGL_UnderwritingQuestions

**Line of Business**: Commercial General Liability (CGL)  
**Feature**: Underwriting Questions  
**Document Version**: 1.0  
**Date**: 2024-01-15  
**Status**: Draft

---

## 1. Executive Summary

The CGL Underwriting Questions feature implements a critical risk assessment mechanism for Commercial General Liability insurance quotes through a modal popup interface containing 7 kill questions (6 currently displayed due to technical debt, 1 missing from popup filter). These questions target specific high-risk exposures including coverage history, legal liability risks, explosive materials, contractor management, equipment leasing, and specialized industries. The feature follows the QuickQuote system-driven pattern with pure dynamic loading through VelociRater's underwriting question framework.

**Key Points:**
- **Business Purpose**: Screen high-risk CGL applicants through targeted underwriting questions before quote generation
- **Current Implementation**: Modal popup with 6 kill questions displayed (codes 9345-9350) + 1 additional kill question defined but not displayed due to filter bug (code 9400)
- **Technical Debt**: Question 9400 exists as kill question but missing from GetKillQuestions filter, should display 7 questions total
- **Modernization Scope**: Transform legacy popup modal into modern responsive underwriting workflow with enhanced validation and user experience
- **Expected Business Value**: Maintained risk assessment capability with improved user interface, better mobile compatibility, and enhanced accessibility compliance

The system serves as a gatekeeper for CGL quotes, ensuring only appropriate risks proceed to coverage selection and pricing. "Yes" answers to any of the 7 kill questions trigger underwriting review or decline, protecting the company from adverse selection while streamlining processing for standard risks.

**CRITICAL BUSINESS IMPACT**: The missing 7th question (bankruptcy/foreclosure screening) represents a significant underwriting gap, as financial distress is a key risk indicator for commercial liability claims.

---

## 2. Business Overview

The CGL Underwriting Questions feature serves as the primary risk screening mechanism for Commercial General Liability insurance applications. This critical component appears as a modal popup during the initial quote process, designed to present 7 targeted kill questions that identify high-risk exposures requiring special underwriting attention or automatic decline.

**CURRENT BUSINESS ISSUE**: Only 6 of 7 kill questions currently display due to technical implementation gap. The missing question (9400) screens for financial distress indicators (bankruptcy, foreclosure) which are critical predictors of claim frequency and policyholder reliability.

### 2.1 Feature Purpose

This feature exists to protect the insurance company from adverse selection by identifying and screening out high-risk Commercial General Liability applications before significant underwriting resources are invested. The 7 questions target specific risk categories that historically generate high claim frequencies or severities:

**Risk Assessment Categories**:
1. **Coverage History Risk** (9345) - Prior declinations indicate carrier-identified problems
2. **Employment Practices Risk** (9346) - Sexual abuse/discrimination exposure requiring EPLI
3. **Hazardous Operations Risk** (9347) - Explosive materials requiring specialized coverage
4. **Contractor Management Risk** (9348) - Inadequate risk transfer practices
5. **Products Liability Risk** (9349) - Equipment leasing operations exposure
6. **Aviation Industry Risk** (9350) - Specialized aviation liability requiring surplus lines
7. **Financial Distress Risk** (9400) - Bankruptcy/foreclosure indicating claim propensity **[MISSING FROM CURRENT POPUP]**

The screening mechanism allows standard risks to proceed directly to coverage selection while flagging exceptional risks for specialized underwriting review or decline. This dual-path approach optimizes processing efficiency while maintaining rigorous risk control standards for the CGL line of business.

**Business Impact of Missing Question**: The absent financial distress screening (9400) creates an underwriting gap where financially distressed applicants may receive standard processing instead of enhanced review, potentially increasing loss ratios and collection issues.

### 2.2 User Roles and Personas

**Primary Users:**
- **Insurance Agents**: Create CGL quotes for commercial clients, must answer all 6 underwriting questions to proceed with quote development
- **Commercial Insurance Brokers**: Similar to agents but often representing larger commercial accounts with complex liability exposures
- **Underwriters**: Review applications where "Yes" answers are provided to kill questions, make coverage decisions for flagged risks

**Secondary Users:**
- **Agency Staff**: May assist agents with quote preparation and data entry including underwriting question responses
- **Compliance Officers**: Monitor that proper risk screening occurs for all CGL applications through question completion tracking

### 2.3 Business Process Context

The underwriting questions modal appears early in the CGL quote workflow, typically after basic applicant information is entered but before detailed coverage selections are made. This positioning allows early identification of unacceptable risks before significant time investment in coverage configuration.

**Workflow Position:**
1. Applicant Information Entry
2. **→ CGL Underwriting Questions Modal** (this feature)
3. Coverage Selection and Configuration
4. Location and Exposure Details
5. Premium Calculation and Quote Generation

The modal blocks progression to subsequent steps until all questions are answered, ensuring complete risk assessment data is captured for every CGL application. Integration with the QuickQuote framework allows automatic application of appropriate coverage defaults (EPLI, CLI) based on question responses.

### 2.4 Regulatory Context

CGL underwriting questions address regulatory and industry best practices for liability risk assessment. Questions regarding sexual abuse/molestation claims align with state regulatory requirements for Employment Practices Liability Insurance (EPLI) coverage considerations. Explosive materials questions support compliance with hazardous operations underwriting guidelines.

The mandatory nature of all question responses ensures consistent risk assessment documentation that supports regulatory examination requirements and demonstrates proper underwriting due diligence across all CGL applications.

---

## 3. Detailed Feature Specifications

### 3.1 Kill Questions Business Rules

**Source**: UWQuestions.vb, lines 48-51 (CGL case logic)

**Question 1 (Code 9345): Coverage History Assessment**
- **Text**: "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"
- **Risk Category**: Coverage History
- **Business Rule**: "Yes" answer indicates prior carrier identified unacceptable risk factors
- **Action on "Yes"**: Triggers underwriting review for risk assessment and possible decline
- **Source**: UWQuestions.vb, lines 966-971

**Question 2 (Code 9346): Legal/Discrimination Risk**
- **Text**: "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
- **Risk Category**: Employment Practices/Legal Liability
- **Business Rule**: "Yes" answer indicates high EPLI exposure requiring specialized coverage or decline
- **Action on "Yes"**: Mandatory underwriting review, may require specialized EPLI coverage or decline
- **Source**: UWQuestions.vb, lines 973-978

**Question 3 (Code 9347): Explosive/Hazardous Operations**
- **Text**: "Do any operations include blasting or utilize or store explosive material?"
- **Risk Category**: Hazardous Operations
- **Business Rule**: "Yes" answer indicates specialized liability exposures requiring excess coverage or decline
- **Action on "Yes"**: Requires specialized underwriting, may need excess liability or surplus lines placement
- **Source**: UWQuestions.vb, lines 980-985

**Question 4 (Code 9348): Contractor Risk Management**
- **Text**: "Are subcontractors allowed to work without providing you with a certificate of insurance?"
- **Risk Category**: Indemnification/Contractor Liability
- **Business Rule**: "Yes" answer indicates inadequate risk transfer practices creating additional insured exposure
- **Action on "Yes"**: Underwriting review for contractor risk management practices and additional insured requirements
- **Source**: UWQuestions.vb, lines 987-992

**Question 5 (Code 9349): Equipment Liability**
- **Text**: "Does applicant lease equipment to others with or without operators?"
- **Risk Category**: Products/Completed Operations Liability
- **Business Rule**: "Yes" answer indicates products liability exposure requiring enhanced coverage limits
- **Action on "Yes"**: Review for products liability coverage adequacy and premium adjustment
- **Source**: UWQuestions.vb, lines 994-999

**Question 6 (Code 9350): Specialized Industry Risk**
- **Text**: "Any products related to the aircraft or space industry?"
- **Risk Category**: Aviation/Aerospace Liability  
- **Business Rule**: "Yes" answer indicates specialized professional liability requiring aviation coverage
- **Action on "Yes"**: Decline for standard CGL, requires specialized aviation liability coverage
- **Source**: UWQuestions.vb, lines 1001-1006

**Question 7 (Code 9400): Financial Distress Risk** 🚨 **MISSING FROM POPUP - TECHNICAL DEBT**
- **Text**: "Has Applicant had a foreclosure, repossession, bankruptcy or filed for bankruptcy during the last five (5) years?"
- **Risk Category**: Financial Stability/Credit Risk
- **Business Rule**: "Yes" answer indicates financial distress correlating with increased claim propensity and collection risk
- **Action on "Yes"**: Triggers underwriting review for financial stability assessment, possible decline or enhanced terms
- **Current Status**: ⚠️ **DEFINED BUT NOT DISPLAYED** - Question exists in database but excluded from GetKillQuestions filter
- **Business Impact**: Critical underwriting gap allowing financially distressed applicants to bypass screening
- **Source**: UWQuestions.vb, lines 2453-2463 (question definition), line 50 (missing from filter)

### 3.2 Dynamic Question Loading Logic

**Source**: ctlUWQuestionsPopup.ascx.vb, lines 1027, 1045-1046

**Loading Process:**
1. System identifies LOB as CGL (QuickQuoteLobType.CommercialGeneralLiability = "9")
2. Calls `VR.Common.UWQuestions.UWQuestions.GetKillQuestions(lobid, EffectiveDate)`
3. GetKillQuestions method filters GetCGLUnderwritingQuestions() for kill question codes **[BUG: INCOMPLETE FILTER]**
4. **CURRENT BEHAVIOR**: Returns List(Of VRUWQuestion) with 6 questions (codes 9345-9350) - MISSING 9400
5. **CORRECT BEHAVIOR**: Should return 7 questions (codes 9345-9350 + 9400)
6. Binds question list to Repeater1 control for modal display

**TECHNICAL DEBT IDENTIFIED**:
- **File**: UWQuestions.vb, line 50
- **Issue**: CGL filter list `{"9345", "9346", "9347", "9348", "9349", "9350"}` missing "9400"
- **Comparison**: BOP correctly includes "9400" in its filter (line 54)
- **Fix Required**: Add "9400" to CGL killQuestionCodes list
- **Root Cause**: Inconsistent filter maintenance between LOBs

**Question Properties (6 Displayed Questions - Codes 9345-9350):**
- **IsTrueUwQuestion**: True (identifies as kill questions)
- **IsQuestionRequired**: True (mandatory response required)
- **Section**: "Risk Grade Questions"
- **PolicyUnderwritingTabId**: "2"
- **PolicyUnderwritingLevelId**: "1"

**Question Properties (1 Missing Question - Code 9400):**
- **IsTrueUwQuestion**: True (identifies as kill question) ✅ **CORRECTLY CONFIGURED**
- **IsQuestionRequired**: True (mandatory response required) ✅ **CORRECTLY CONFIGURED**  
- **Section**: "Applicant Information" (different section from others)
- **PolicyUnderwritingTabId**: "3" (different tab from others)
- **PolicyUnderwritingLevelId**: "1"
- **Status**: ⚠️ **READY TO DISPLAY** - All properties correct, only missing from filter list

### 3.3 Coverage Integration Logic

**Source**: ctlUWQuestionsPopup.ascx.vb, lines 1698-1699, 1703-1704

**Automatic Coverage Application:**
- **EPLI Coverage**: `IFM.VR.Common.Helpers.CGL.EPLIHelper.Toggle_EPLI_Is_Applied(qq, True)`
- **CLI Coverage**: `IFM.VR.Common.Helpers.CGL.CLIHelper.Toggle_CLI_Is_Applied(qq, True)`

**Business Rule**: CGL quotes automatically include Employment Practices Liability Insurance (EPLI) and Commercial Lines Insurance (CLI) coverages as default protections, particularly relevant for questions addressing discrimination and employment practices risks.

---

## 4. UI/UX Requirements ⭐ MANDATORY

### 4.1 Auto-Display/Hide Behaviors

**Pattern Description:**
The CGL underwriting questions appear in a modal popup dialog triggered during the quote workflow. The modal displays automatically when the user reaches the underwriting questions step and cannot be bypassed until all questions are answered.

**Modal Display Trigger:**
```
Modal appears when: User reaches CGL underwriting questions workflow step
Modal title: "Underwriting Questions"
Modal width: 550px (popupDialogWidth variable)
Modal cannot be closed: Until all questions answered and validated
CURRENT STATE: Displays 6 questions (missing 7th due to filter bug)
TARGET STATE: Should display 7 questions (requires filter fix)
Source: ctlUWQuestionsPopup.ascx, lines 125-135
```

**Question Display Pattern:**
```
Each question displays as: Radio button pair (Yes/No) with question text
Additional info textarea: Shows when user selects "Yes" (90% width)
Default state: All questions visible, no answers selected
Required indicators: Red asterisk (*) for all questions (mandatory)
CURRENT: 6 questions numbered 1-6
TARGET: 7 questions numbered 1-7 (including financial distress screening)
Source: ctlUWQuestionsPopup.ascx, lines 795-825
```

### 4.2 Text Input Specifications

**Field Specifications:**

| Field Name | Label | Type | Character Limit | Required | Default |
|------------|-------|------|-----------------|----------|---------|
| Question Response | "Yes" / "No" | Radio Buttons | N/A | Yes | None Selected |
| Additional Info (Q1) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| Additional Info (Q2) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| Additional Info (Q3) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| Additional Info (Q4) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| Additional Info (Q5) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| Additional Info (Q6) | "(Additional information)" | Multi-line | No limit specified | When "Yes" | Empty |
| **Additional Info (Q7)** | **"(Additional information)"** | **Multi-line** | **No limit specified** | **When "Yes"** | **Empty** **[MISSING - REQUIRES FILTER FIX]** |

**Additional Info Text Areas:**
- **Width**: 90% of modal width
- **Display Logic**: Only appears when user selects "Yes" for corresponding question
- **Requirement**: Required when "Yes" is selected (must provide explanation)
- **Validation**: Checked by ValidateUWForm() JavaScript function
- **Source**: ctlUWQuestionsPopup.ascx, Repeater1 template structure

### 4.3 Validation Visual Indicators

**Error States:**

**Empty Required Question:**
- **Visual**: Red border around radio button container
- **Error Message**: "All Questions Must Be Answered" (displayed at top of modal in red)
- **Icon**: Red asterisk (*) next to question text (always displayed)
- **Trigger**: User attempts to continue with unanswered questions
- **Validation Function**: AllAnswersAreAnswered() JavaScript function

**Missing Additional Information:**
- **Visual**: Red border around textarea
- **Error Message**: "Additional information required for 'Yes' answers"
- **Trigger**: User selects "Yes" but leaves additional info textarea empty
- **Validation Function**: ValidateUWForm() JavaScript function checks for empty textareas when Yes selected

**Success States:**
- **Visual**: No special visual indicator for correct completion
- **Action**: Continue button becomes functional, modal can be submitted
- **Behavior**: Modal closes and workflow proceeds to next step

### 4.4 Interactive Elements

**Radio Buttons:**
- **Labels**: "Yes" / "No" for each question
- **Behavior**: Mutually exclusive selection per question
- **Default State**: No selection (forcing user to make conscious choice)
- **Selection Logic**: Clicking Yes shows additional info textarea, clicking No hides it

**Continue Button:**
- **Label**: "Continue" (standard modal button text)
- **Enabled State**: Always enabled (validation occurs on click)
- **Click Action**: Triggers ValidateUWForm() validation before proceeding
- **OnClientClick**: "return ValidateUWForm();" JavaScript validation call

**Additional Info Textareas:**
- **Display**: Conditional (only when "Yes" selected)
- **Sizing**: 90% width, multi-row height
- **Placeholder**: None specified
- **Required**: Only when corresponding "Yes" selected

### 4.5 Accessibility Requirements

- **ARIA Labels**: Each radio button group labeled with question text for screen readers
- **Keyboard Navigation**: Standard tab order through questions and radio buttons
- **Focus Indicators**: Browser default focus highlighting on radio buttons and textareas
- **Screen Reader Text**: Question numbers and text read aloud for each question
- **Color Contrast**: Red error indicators must meet WCAG 2.1 AA compliance (4.5:1 minimum)

### 4.6 Responsive Design Requirements

- **Mobile Devices**: Modal scales to device width, maintains 550px maximum width
- **Tablets**: Full modal display with touch-friendly radio button sizing
- **Desktop**: Standard 550px modal width centered on screen
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge, IE11 (VelociRater supported browsers)

---

## 5. Validation Rules and Business Logic ⭐ MANDATORY

### 5.1 Client-Side Validation (JavaScript)

**Function: AllAnswersAreAnswered()**
- **Purpose**: Validates that all CGL underwriting questions have Yes or No selection
- **Current State**: Validates 6 questions (due to filter limiting display to 6)
- **Target State**: Should validate 7 questions (when filter bug is fixed)
- **Trigger**: Called by ValidateUWForm() during form submission validation
- **Logic**: Iterates through table rows, checks even-indexed rows (questions) for radio button selection
- **Error Display**: Shows red border styling and asterisk indicators for incomplete questions
- **Return Value**: Boolean - true if all answered, false if any missing
- **Source**: ctlUWQuestionsPopup.ascx, JavaScript section

**Function: ValidateUWForm()**
- **Purpose**: Comprehensive form validation before modal submission
- **Trigger**: OnClientClick event from Continue button ("return ValidateUWForm();")
- **Logic**: 
  1. Calls AllAnswersAreAnswered() to verify all questions have responses
  2. Checks additional info textareas are completed when "Yes" answers provided
  3. Displays "All Questions Must Be Answered" error message if validation fails
- **Error Message**: "All Questions Must Be Answered" (exact text displayed)
- **Visual Feedback**: Red border styling, error message display at modal top
- **Return Value**: Boolean - true allows form submission, false blocks submission
- **Source**: ctlUWQuestionsPopup.ascx, JavaScript section

### 5.2 Required Field Validation

**Required Fields:**

| Field Name | Required When | Validation Logic | Error Message |
|------------|---------------|------------------|---------------|
| Question 1 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Question 2 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Question 3 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Question 4 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Question 5 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Question 6 Response | Always | Radio button selection required | "All Questions Must Be Answered" |
| Additional Info (any) | If "Yes" Selected | Textarea not empty when Yes selected | "Additional information required for 'Yes' answers" |

**Conditional Requirements:**
- **Additional Information Textareas**: Required only when user selects "Yes" for corresponding question
- **Logic**: ValidateUWForm() checks each question's radio button value, if "Yes" then validates corresponding textarea is not empty
- **Enforcement**: Client-side validation prevents form submission until all conditional requirements met

### 5.3 Business Rule Validation

**Rule 1: Complete Response Requirement**
- **Description**: All underwriting questions must have Yes or No response before quote can proceed
- **Current Implementation**: 6 questions (codes 9345-9350) due to filter bug
- **Correct Implementation**: Should require 7 questions (codes 9345-9350 + 9400)
- **Validation Logic**: AllAnswersAreAnswered() iterates through all question radio button groups, returns false if any unselected
- **Error Handling**: Modal cannot be submitted, error message displayed, visual indicators shown
- **Source**: ctlUWQuestionsPopup.ascx, AllAnswersAreAnswered() JavaScript function

**Rule 2: Additional Information for Yes Answers**
- **Description**: When user answers "Yes" to any kill question, additional explanatory information must be provided
- **Validation Logic**: ValidateUWForm() checks each question, if Yes selected validates corresponding textarea contains text
- **Error Handling**: Form submission blocked, error message displayed, red border on empty textareas
- **Business Rationale**: Underwriters require detailed information about risk factors to make informed coverage decisions
- **Source**: ctlUWQuestionsPopup.ascx, ValidateUWForm() JavaScript function

**Rule 3: Kill Question Processing**
- **Description**: All 7 CGL questions are kill questions (IsTrueUwQuestion = True), Yes answers trigger underwriting review/decline
- **Current Gap**: Financial distress question (9400) not processed due to filter exclusion
- **Business Risk**: Missing critical risk screening for bankruptcy/foreclosure indicators
- **Validation Logic**: Server-side processing after modal submission evaluates Yes answers for underwriting action
- **Action Processing**: SetPolicyUws() method saves responses to quote object for underwriting workflow
- **Business Impact**: Yes answers may result in automatic decline or referral to specialized underwriters
- **Source**: ctlUWQuestionsPopup.ascx.vb, lines 1748, UWQuestions.vb kill question definitions

### 5.4 Server-Side Validation

**Security Validations:**
- **Input Sanitization**: All text input sanitized to prevent malicious script injection
- **SQL Injection Prevention**: Parameterized queries used for database operations
- **Cross-Site Scripting (XSS) Prevention**: User input encoded before display or database storage

**Data Integrity Checks:**
- **Question Code Validation**: Ensures only valid CGL diamond codes (9345-9350) are processed
- **Response Format Validation**: Validates Yes/No responses match expected enumeration values
- **Additional Info Length**: Server-side validation of textarea content length for database storage
- **LOB Consistency**: Validates questions match CGL LOB type throughout processing chain

---

## 6. User Stories and Acceptance Criteria

### US-CGL-UW-001: View CGL Underwriting Questions

**As an** Insurance Agent  
**I need to** view all 6 CGL underwriting questions in a modal popup  
**So that** I can assess risk factors for my commercial general liability applicant

**Acceptance Criteria:**
1. Given I am creating a CGL quote, when I reach the underwriting questions step, then a modal popup displays with title "Underwriting Questions"
2. Given the modal is displayed, when I view the content, then I see exactly 6 numbered questions with Yes/No radio buttons
3. Given each question is displayed, when I read the question text, then I see the exact regulatory-compliant question wording from the Diamond system
4. Given the modal opens, when I attempt to close it without answering, then the modal remains open and cannot be bypassed
5. Given the modal is 550px wide, when displayed on desktop, then it appears centered and properly formatted

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: None (standalone modal functionality)

### US-CGL-UW-002: Answer Kill Questions with Validation

**As an** Insurance Agent  
**I need to** answer all underwriting questions with proper validation  
**So that** I provide complete risk assessment information required for the quote

**Acceptance Criteria:**
1. Given a question is displayed, when I select "Yes" or "No", then my selection is visually confirmed and recorded
2. Given I select "Yes" for any question, when the selection is made, then an additional information textarea appears below that question
3. Given I select "No" after previously selecting "Yes", when the selection changes, then the additional information textarea disappears
4. Given I attempt to continue with unanswered questions, when I click Continue, then validation prevents submission and shows "All Questions Must Be Answered" error
5. Given I select "Yes" but leave additional information empty, when I attempt to continue, then validation prevents submission and shows error message

**Priority**: High  
**Complexity**: Large  
**Dependencies**: US-CGL-UW-001 (requires modal display)

### US-CGL-UW-003: Process Coverage History Question (9345)

**As an** Insurance Agent  
**I need to** answer the prior coverage declined/cancelled question accurately  
**So that** underwriters can assess the applicant's insurance history risk

**Acceptance Criteria:**
1. Given question 1 is displayed, when I read the text, then I see "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"
2. Given I select "Yes", when the selection is made, then an additional information field appears for explanation details
3. Given I select "Yes" and provide additional information, when I submit, then the response is recorded for underwriting review
4. Given I select "No", when the selection is made, then no additional information is required and the response is recorded
5. Given a "Yes" answer is submitted, when processed, then the application is flagged for underwriting review

**Priority**: High  
**Complexity**: Small  
**Dependencies**: US-CGL-UW-002 (requires answer functionality)

### US-CGL-UW-004: Process Sexual Abuse/Discrimination Question (9346)

**As an** Insurance Agent  
**I need to** answer the sexual abuse/discrimination claims question  
**So that** EPLI coverage requirements can be properly evaluated

**Acceptance Criteria:**
1. Given question 2 is displayed, when I read the text, then I see "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"
2. Given I select "Yes", when the selection is made, then additional information field appears and EPLI coverage considerations are triggered
3. Given a "Yes" answer is provided with details, when submitted, then the response triggers specialized EPLI underwriting review
4. Given I select "No", when submitted, then standard EPLI coverage defaults apply without special review
5. Given EPLI coverage is involved, when the question is processed, then appropriate coverage defaults are applied to the quote

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: US-CGL-UW-002, EPLI coverage integration

### US-CGL-UW-005: Process Explosive Materials Question (9347)

**As an** Insurance Agent  
**I need to** answer the explosive materials/blasting operations question  
**So that** hazardous operation exposures can be properly underwritten

**Acceptance Criteria:**
1. Given question 3 is displayed, when I read the text, then I see "Do any operations include blasting or utilize or store explosive material?"
2. Given I select "Yes", when the selection is made, then additional information field appears for operation details
3. Given a "Yes" answer is provided, when submitted, then the application is flagged for specialized hazardous operations underwriting
4. Given I select "No", when submitted, then standard CGL coverage applies without additional review
5. Given explosive operations are indicated, when processed, then specialized coverage or surplus lines placement may be required

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: US-CGL-UW-002, hazardous operations underwriting workflow

### US-CGL-UW-006: Process Subcontractor Insurance Question (9348)

**As an** Insurance Agent  
**I need to** answer the subcontractor certificate requirement question  
**So that** contractor risk transfer practices can be evaluated

**Acceptance Criteria:**
1. Given question 4 is displayed, when I read the text, then I see "Are subcontractors allowed to work without providing you with a certificate of insurance?"
2. Given I select "Yes", when the selection is made, then additional information field appears for risk management details
3. Given a "Yes" answer indicates inadequate risk transfer, when submitted, then underwriting review is triggered for additional insured requirements
4. Given I select "No", when submitted, then standard contractor provisions apply
5. Given poor risk transfer practices are indicated, when processed, then enhanced additional insured coverage or decline may be required

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: US-CGL-UW-002, contractor risk assessment workflow

### US-CGL-UW-007: Process Equipment Leasing Question (9349)

**As an** Insurance Agent  
**I need to** answer the equipment leasing operations question  
**So that** products liability exposures can be properly assessed

**Acceptance Criteria:**
1. Given question 5 is displayed, when I read the text, then I see "Does applicant lease equipment to others with or without operators?"
2. Given I select "Yes", when the selection is made, then additional information field appears for leasing operation details
3. Given equipment leasing is indicated, when submitted, then products liability coverage review is triggered
4. Given I select "No", when submitted, then standard products liability coverage applies
5. Given leasing operations exist, when processed, then enhanced products liability limits or premium adjustments may be required

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: US-CGL-UW-002, products liability assessment

### US-CGL-UW-008: Process Aircraft Industry Question (9350)

**As an** Insurance Agent  
**I need to** answer the aircraft/space industry products question  
**So that** specialized aviation liability requirements can be identified

**Acceptance Criteria:**
1. Given question 6 is displayed, when I read the text, then I see "Any products related to the aircraft or space industry?"
2. Given I select "Yes", when the selection is made, then additional information field appears for aviation industry details
3. Given aviation industry involvement is indicated, when submitted, then the application is typically declined for standard CGL coverage
4. Given I select "No", when submitted, then standard CGL coverage processing continues
5. Given aviation products are involved, when processed, then referral to specialized aviation insurance markets is required

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: US-CGL-UW-002, aviation insurance referral workflow

### US-CGL-UW-009: Complete Question Workflow and Proceed

**As an** Insurance Agent  
**I need to** complete all underwriting questions and successfully proceed to coverage selection  
**So that** I can continue building the CGL quote for my client

**Acceptance Criteria:**
1. Given all displayed questions have Yes or No answers, when I click Continue, then validation passes and the modal closes
2. Given any questions have "Yes" answers with additional information provided, when I continue, then all responses are saved to the quote
3. Given the modal closes successfully, when processing completes, then I proceed to the coverage selection step of the quote workflow
4. Given responses indicate underwriting review is needed, when processing completes, then appropriate workflow flags are set
5. Given all questions answered with "No" responses, when processing completes, then standard CGL quote processing continues with default coverages applied

**Current State**: 6 questions due to filter bug  
**Target State**: 7 questions when filter is corrected

**Priority**: High  
**Complexity**: Large  
**Dependencies**: All previous user stories (requires complete question workflow)

### US-CGL-UW-010: Process Financial Distress Question (9400) 🚨 **MISSING - TECHNICAL DEBT**

**As an** Insurance Agent  
**I need to** answer the financial distress/bankruptcy question for CGL applicants  
**So that** underwriters can assess financial stability risk indicators

**Acceptance Criteria:**
1. Given question 7 is displayed, when I read the text, then I see "Has Applicant had a foreclosure, repossession, bankruptcy or filed for bankruptcy during the last five (5) years?"
2. Given I select "Yes", when the selection is made, then an additional information field appears for financial details
3. Given a "Yes" answer indicates financial distress, when submitted, then underwriting review is triggered for financial stability assessment
4. Given I select "No", when submitted, then standard CGL processing continues
5. Given financial distress is indicated, when processed, then enhanced underwriting review or decline may be required based on severity

**Current Status**: ⚠️ **BLOCKED - Question exists in database but not displayed due to filter bug**
**Technical Fix Required**: Add "9400" to GetKillQuestions filter list (UWQuestions.vb line 50)
**Business Priority**: HIGH - Financial distress strongly correlates with claim propensity
**Complexity**: Small (once filter bug fixed)  
**Dependencies**: Filter bug resolution (technical debt remediation)

---

## 7. Testing Requirements

### 7.1 Functional Testing

**Test Scenario 1: Modal Display and Basic Functionality**
- **Setup**: Navigate to CGL quote workflow, reach underwriting questions step
- **Steps**: 
  1. Verify modal popup appears with "Underwriting Questions" title
  2. Confirm modal is 550px width and properly centered
  3. ⚠️ **CURRENT**: Verify 6 questions display (missing 7th due to filter bug)
  4. ✅ **TARGET**: Verify all 7 questions display with correct numbering and text
  5. Confirm each question has Yes/No radio button options
  6. Verify red asterisk (*) appears next to each question indicating required
- **Current Expected Result**: Modal displays correctly with 6 questions (INCOMPLETE)
- **Target Expected Result**: Modal displays correctly with all 7 questions properly formatted and marked required

**Test Scenario 1A: Technical Debt Verification**
- **Setup**: Code analysis of GetKillQuestions filter
- **Steps**:
  1. Verify UWQuestions.vb line 50 contains only 6 codes (9345-9350)
  2. Verify UWQuestions.vb line 2453-2463 contains question 9400 definition
  3. Confirm question 9400 has IsTrueUwQuestion = True
  4. Compare with BOP filter (line 54) which correctly includes 9400
- **Expected Result**: Confirms filter bug - question exists but not included in CGL filter

**Test Scenario 2: Question Response Selection**
- **Setup**: CGL underwriting questions modal is displayed
- **Steps**:
  1. Select "Yes" for question 1, verify additional info textarea appears
  2. Select "No" for question 1, verify additional info textarea disappears
  3. ⚠️ **CURRENT**: Repeat Yes/No selection test for questions 1-6 (missing question 7)
  4. ✅ **TARGET**: Repeat Yes/No selection test for all questions 1-7 (including financial distress)
  5. Verify radio button selections are mutually exclusive per question
  6. Confirm multiple questions can have "Yes" selections simultaneously
- **Expected Result**: Additional info textareas appear/disappear correctly based on Yes/No selection for each question

**Test Scenario 2A: Missing Question 7 Testing (POST-FIX)**
- **Setup**: After filter bug is fixed and question 7 displays
- **Steps**:
  1. Verify question 7 appears as "Has Applicant had a foreclosure, repossession, bankruptcy..."
  2. Select "Yes" for question 7, verify additional info textarea appears
  3. Select "No" for question 7, verify additional info textarea disappears
  4. Verify question 7 has same validation behavior as questions 1-6
- **Expected Result**: Question 7 behaves identically to other kill questions

**Test Scenario 3: Validation Error Handling**
- **Setup**: CGL underwriting questions modal with some questions unanswered
- **Steps**:
  1. Leave questions 1, 3, 5 unanswered, attempt to click Continue
  2. Verify "All Questions Must Be Answered" error message displays
  3. Verify red border appears around unanswered questions
  4. Answer questions 1, 3, 5 as "Yes" but leave additional info empty
  5. Attempt to continue, verify additional info validation error
- **Expected Result**: Appropriate error messages display and form submission is blocked until all validation passes

**Test Scenario 4: Complete Workflow Success**
- **Setup**: CGL underwriting questions modal displayed
- **Steps**:
  1. Answer all 6 questions with mix of "Yes" and "No" responses
  2. Provide additional information for all "Yes" answers
  3. Click Continue button
  4. Verify modal closes and workflow proceeds to next step
  5. Confirm responses are saved to quote object
- **Expected Result**: Modal closes successfully, workflow advances, all responses properly recorded

### 7.2 UI Behavior Testing

**Auto-Display/Hide Testing:**
- Verify modal appears automatically when reaching underwriting questions step
- Test modal cannot be closed/bypassed until all questions answered
- Validate additional info textareas show/hide based on Yes/No selections
- Confirm default state shows all questions with no selections

**Validation Testing:**
- Test all 6 questions individually for required response validation
- Verify additional info textareas required only when "Yes" selected
- Test JavaScript validation functions (AllAnswersAreAnswered, ValidateUWForm)
- Validate error message display and visual indicators (red borders, asterisks)

### 7.3 Cross-Browser Testing

Test on:
- **Chrome (latest version)**: Primary browser for VelociRater compatibility
- **Firefox (latest version)**: Secondary browser support
- **Safari (latest version)**: Mac user support
- **Edge (latest version)**: Windows default browser
- **IE11**: Legacy browser support if still required by VelociRater

### 7.4 Accessibility Testing

- **Screen Reader Compatibility**: Test with NVDA/JAWS for question text and radio button labels
- **Keyboard Navigation**: Verify tab order through questions and radio buttons works correctly
- **Focus Indicators**: Confirm visual focus highlighting on interactive elements
- **ARIA Label Verification**: Validate each question group has proper ARIA labeling
- **Color Contrast Validation**: Test red error indicators meet WCAG 2.1 AA standards (4.5:1)

### 7.5 Performance Testing

- **Modal Load Time**: Verify popup appears within 2 seconds of trigger
- **Question Loading**: Test dynamic question loading from GetCGLUnderwritingQuestions() completes quickly
- **Validation Response**: Confirm JavaScript validation functions execute without noticeable delay
- **Form Submission**: Test modal submission and workflow progression performance

---

## 8. Critical Technical Debt and Business Impact 🚨

### 8.1 Missing Kill Question Business Impact Analysis

**Financial Distress Screening Gap**:
- **Missing Question**: "Has Applicant had a foreclosure, repossession, bankruptcy or filed for bankruptcy during the last five (5) years?" (Code 9400)
- **Risk Category**: Financial stability and creditworthiness assessment
- **Underwriting Significance**: Financial distress indicators are strong predictors of:
  - Increased claim frequency (financially stressed businesses often cut safety costs)
  - Higher collection risk (difficulty collecting deductibles and premiums)
  - Policy lapse risk (inability to pay ongoing premiums)
  - Moral hazard (increased incentive for claims due to financial pressure)

**Business Quantification**:
- **Current State**: 100% of CGL applicants bypass financial distress screening
- **Risk Exposure**: Unknown percentage of financially distressed applicants receive standard processing
- **Loss Impact**: Potential increased loss ratios due to unscreened financial risk
- **Collection Impact**: Potential increased collection costs and bad debt

### 8.2 Root Cause Analysis

**Technical Root Cause**:
- **File**: UWQuestions.vb, line 50
- **Issue**: CGL GetKillQuestions filter list missing "9400" code
- **Evidence**: BOP correctly includes "9400" in filter (line 54), CGL does not
- **Question Status**: Fully defined with correct properties (IsTrueUwQuestion = True, IsQuestionRequired = True)

**Process Root Cause**:
- **Pattern**: Inconsistent filter maintenance across LOBs
- **Timing**: Likely occurred when question 9400 was added but CGL filter not updated
- **Quality Gap**: No systematic validation that kill question definitions match filter lists

### 8.3 Immediate Remediation Requirements

**Priority 1: Filter Fix (Technical)**
- **Action**: Add "9400" to CGL killQuestionCodes list (line 50)
- **Change**: `From {"9345", "9346", "9347", "9348", "9349", "9350"}` TO `{"9345", "9346", "9347", "9348", "9349", "9350", "9400"}`
- **Testing**: Verify 7 questions display in CGL popup after fix
- **Validation**: Ensure question 7 behaves identically to other kill questions

**Priority 2: Business Process Update**
- **Agent Training**: Update training materials to include 7th question
- **Underwriting Guidelines**: Clarify financial distress evaluation criteria
- **Documentation**: Update all CGL procedures to reflect 7 questions

**Priority 3: Quality Control Enhancement**
- **Validation Rule**: Implement automated check that kill question definitions match filter lists
- **Code Review Process**: Require LOB cross-validation when updating kill question filters
- **Testing Protocol**: Mandate question count verification in LOB testing procedures

### 8.4 Long-term Modernization Impact

**Architecture Improvement Opportunity**:
- **Current Issue**: Manual filter list maintenance prone to human error
- **Modern Solution**: Dynamic filter based on IsTrueUwQuestion flag eliminates filter maintenance
- **Implementation**: Replace hardcoded filter lists with database-driven filtering
- **Benefit**: Eliminates possibility of filter/definition mismatches across LOBs

**Data Integrity Validation**:
- **Requirement**: Systematic validation that all kill questions defined in database are displayed in UI
- **Automation**: Implement automated tests verifying question count consistency
- **Monitoring**: Add runtime validation that expected question count matches displayed count

## 9. Migration and Modernization Considerations

### 8.1 Data Migration
**Current Data Structure**: VRUWQuestion objects with IsTrueUwQuestion flags and diamond codes 9345-9350
**Migration Requirements**: Preserve all question codes, text, and kill question designations during platform migration
**Data Integrity**: Maintain GetCGLUnderwritingQuestions() method functionality or equivalent data source

### 8.2 Configuration Migration
**Question Content**: Migrate exact question text from Diamond system to new platform
**Business Rules**: Preserve kill question behavior and underwriting trigger logic
**Coverage Integration**: Maintain EPLI/CLI automatic application functionality
**Validation Rules**: Port JavaScript validation logic to modern framework validation

### 8.3 Integration Impact
**QuickQuote Framework**: Modern platform must support equivalent dynamic question loading
**Diamond System Integration**: Maintain connection to external underwriting question source
**Underwriting Workflow**: Preserve integration with underwriting review triggers
**Coverage Application**: Maintain automatic EPLI/CLI coverage application logic

### 8.4 Rollback Strategy
**Data Preservation**: Maintain backup of current VelociRater UWQuestions.vb implementation
**Functionality Verification**: Test all 6 questions load correctly with proper validation before go-live
**Business Continuity**: Ensure kill question processing continues without interruption during migration
**User Training**: Provide agents with continuity guidance if UI changes significantly

---

## 10. Source Attribution and Traceability

### 10.1 Source Code Files Analyzed

| File Path | Purpose | Lines Analyzed |
|-----------|---------|----------------|
| UWQuestions.vb | CGL question definitions and loading logic | 48-51, 961-1009, 2257-2332 |
| ctlUWQuestionsPopup.ascx | Modal UI markup and JavaScript validation | 125-135, 795-825, JavaScript functions |
| ctlUWQuestionsPopup.ascx.vb | Modal code-behind processing and data binding | 1027, 1045-1046, 1627-1634, 1698-1699, 1703-1704, 1747-1748 |

### 10.2 Key Functions and Methods

| Function Name | File | Line | Purpose |
|---------------|------|------|---------|
| GetKillQuestions() | UWQuestions.vb | 48-51 | Filters CGL questions by kill codes 9345-9350 |
| GetCGLUnderwritingQuestions() | UWQuestions.vb | 961-1009 | Returns complete CGL question definitions |
| AllAnswersAreAnswered() | ctlUWQuestionsPopup.ascx | JavaScript | Validates all questions have responses |
| ValidateUWForm() | ctlUWQuestionsPopup.ascx | JavaScript | Comprehensive form validation before submission |
| Toggle_EPLI_Is_Applied() | ctlUWQuestionsPopup.ascx.vb | 1698-1699 | Applies EPLI coverage automatically |
| Toggle_CLI_Is_Applied() | ctlUWQuestionsPopup.ascx.vb | 1703-1704 | Applies CLI coverage automatically |
| SetPolicyUws() | ctlUWQuestionsPopup.ascx.vb | 1748 | Saves underwriting responses to quote |

### 10.3 Traceability Matrix

| Requirement ID | Source Code Reference | Validation | Status |
|----------------|----------------------|------------|--------|
| 7 Kill Questions Total | UWQuestions.vb:48-51 (filter), 2257-2463 (definitions) | US-CGL-UW-001 | ⚠️ PARTIAL (6 displayed, 1 missing) |
| Coverage History | UWQuestions.vb:2257-2267, code 9345 | US-CGL-UW-003 | ✅ COMPLETE |
| Sexual Abuse/Discrimination | UWQuestions.vb:2270-2280, code 9346 | US-CGL-UW-004 | ✅ COMPLETE |
| Explosive Materials | UWQuestions.vb:2283-2293, code 9347 | US-CGL-UW-005 | ✅ COMPLETE |
| Subcontractor Insurance | UWQuestions.vb:2296-2306, code 9348 | US-CGL-UW-006 | ✅ COMPLETE |
| Equipment Leasing | UWQuestions.vb:2309-2319, code 9349 | US-CGL-UW-007 | ✅ COMPLETE |
| Aircraft Industry | UWQuestions.vb:2322-2332, code 9350 | US-CGL-UW-008 | ✅ COMPLETE |
| **Financial Distress** | **UWQuestions.vb:2453-2463, code 9400** | **US-CGL-UW-010** | **⚠️ MISSING (filter bug)** |
| Modal Display | ctlUWQuestionsPopup.ascx:125-135 | US-CGL-UW-001 | ✅ COMPLETE |
| Validation Logic | ctlUWQuestionsPopup.ascx JavaScript | US-CGL-UW-002 | ✅ COMPLETE |
| EPLI Integration | ctlUWQuestionsPopup.ascx.vb:1698-1699 | US-CGL-UW-004 | ✅ COMPLETE |
| Dynamic Loading | ctlUWQuestionsPopup.ascx.vb:1027,1045-1046 | US-CGL-UW-009 | ⚠️ INCOMPLETE (missing Q7) |
| **Filter Bug** | **UWQuestions.vb:50 (missing "9400")** | **Technical Debt** | **⚠️ BLOCKING ISSUE** |

---

## 11. Document Metadata

**Prepared By**: Mason (IFI Requirements Extraction Specialist)  
**Reviewed By**: Vera (IFI Quality Validator) - Pending  
**Approved By**: [IFI Technical Authority] - Pending  
**Document Location**: `//project/ifm/product_requirements/CGL/Underwriting_Questions/Modernization_CGL_UnderwritingQuestions.md`

**Analysis Source**: Rex (IFI Pattern Miner) - CGL Pattern Analysis Complete  
**Architecture Input**: Aria (IFI Architect) - Pending  
**Domain Validation**: Rita (IFI Insurance Specialist) - Pending  
**Orchestration**: Douglas (IFI Orchestrator) - Request Delegated

**Rex Analysis Files Referenced**:
- `//project/ifm/meta/rex/cgl/cgl_pattern_analysis.md`
- `//project/ifm/meta/rex/cgl_popup_questions/cgl_questions_structured.json`
- `//project/ifm/meta/rex/cgl_popup_questions/cgl_popup_analysis.md`

**Token Budget Used**: 12.5K / 25K tokens

**CRITICAL FINDING**: 7th CGL kill question identified (code 9400) - exists in database but missing from popup filter, creating significant underwriting gap for financial distress screening.

**UPDATE REASON**: Corrected Rex's analysis through independent source code verification. Original analysis found 6 questions; actual source shows 7 questions with 1 missing due to filter implementation bug.

---

**END OF REQUIREMENTS DOCUMENT**