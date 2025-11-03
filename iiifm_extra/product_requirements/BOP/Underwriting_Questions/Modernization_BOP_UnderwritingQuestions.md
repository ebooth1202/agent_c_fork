# Modernization_BOP_UnderwritingQuestions

**Line of Business**: Business Owner's Policy (BOP)  
**Feature**: Underwriting Questions  
**Document Version**: 1.0  
**Date**: 2024-12-19  
**Status**: Draft

---

## 1. Executive Summary

The BOP Underwriting Questions feature manages comprehensive risk assessment through a sophisticated dual-question architecture that combines quick screening capabilities with detailed underwriting data collection. This modernization scope addresses the complete underwriting questionnaire system including kill question screening, application-level question management, and dynamic UI behaviors with real-time validation.

**Key Points:**
- **Business Purpose**: Enable comprehensive risk assessment for Business Owner's Policy applications through systematic underwriting questioning that identifies both immediate disqualifiers and detailed risk characteristics
- **Current Implementation**: Dual-system architecture with 6 kill questions for screening and 11 primary underwriting questions for comprehensive data collection, supported by dynamic UI panels and 125-character validation limits
- **Modernization Scope**: Complete underwriting questions workflow including question presentation, validation logic, character limit enforcement, conditional panel display, and regulatory compliance tracking
- **Expected Business Value**: Streamlined risk assessment process with improved data quality, consistent underwriting standards, and enhanced user experience through real-time validation and guidance

The current system successfully manages both immediate risk screening through popup kill questions and comprehensive underwriting data collection through application-level questioning, with robust validation and dynamic UI behaviors that guide users through the risk assessment process.

---

## 2. Business Overview

The BOP Underwriting Questions feature serves as the cornerstone of risk assessment in the commercial insurance application process, enabling underwriters to evaluate business risks systematically and consistently. This feature directly impacts binding authority, pricing decisions, and regulatory compliance while providing agents with clear guidance on risk acceptability and documentation requirements.

### 2.1 Feature Purpose

The underwriting questions system exists to systematically capture risk-relevant information that enables informed underwriting decisions while maintaining regulatory compliance and consistent risk evaluation standards. The dual-question architecture supports both immediate risk screening (kill questions) and comprehensive risk documentation (application questions), ensuring efficient processing while maintaining thorough risk evaluation.

### 2.2 User Roles and Personas

**Primary Users:**
- **Insurance Agents**: Complete underwriting questions during application process, receive immediate feedback on risk acceptability, and provide additional information as required
- **Underwriters**: Review question responses for risk evaluation, analyze additional information provided, and make binding decisions based on systematic risk assessment
- **Compliance Officers**: Monitor question completion rates, ensure regulatory compliance, and maintain audit trails for underwriting decisions

### 2.3 Business Process Context

The underwriting questions feature operates within the broader BOP application workflow, positioned after initial applicant information collection but before final risk evaluation and pricing. The system integrates with kill question screening for immediate risk elimination, Diamond underwriting system for regulatory compliance, and application workflow for comprehensive data collection. Question responses directly influence coverage availability, pricing adjustments, and binding authority requirements.

### 2.4 Regulatory Context

The underwriting questions system maintains compliance with state insurance regulations regarding risk assessment documentation, unfair discrimination prevention, and underwriting standards consistency. The Diamond integration ensures questions meet regulatory requirements across all operating states, while the audit trail functionality supports regulatory examination requirements and complaint resolution processes.

---

## 3. Detailed Feature Specifications

The BOP Underwriting Questions feature implements a comprehensive dual-architecture system that manages both immediate risk screening and detailed underwriting data collection through integrated question presentation, validation, and processing workflows.

### 3.1 Dual Question System Architecture

**Kill Questions Popup System (6 Questions)**:
- **Trigger**: "Yes" responses during quote process activate popup modal
- **Control**: `ctlUWQuestionsPopup.ascx` modal implementation  
- **Function**: `GetKillQuestions()` filters codes {9003, 9006, 9007, 9008, 9009, 9400}
- **Purpose**: Quick screening and qualification for immediate risk elimination
- **Display Pattern**: Sequential numbering (1, 2, 3, etc.) with simplified presentation
- **Source**: UWQuestions.vb, GetKillQuestions() method filtering from complete question set

**Application UW Questions System (11 Primary Questions)**:
- **Location**: Application workflow sections with accordion UI organization
- **Control**: `ctlCommercialUWQuestionList.ascx` and `ctlCommercialUWQuestionItem.ascx`
- **Function**: `GetCommercialBOPUnderwritingQuestions()` complete question set (lines 1012-1447)
- **Purpose**: Comprehensive underwriting data collection and risk documentation
- **Display Pattern**: Grouped by section name ("Applicant Information", "Business Owners - General Info", etc.)
- **Source**: UWQuestions.vb, GetCommercialBOPUnderwritingQuestions() method complete implementation

### 3.2 The 11 Primary BOP Questions Specification

**Question Mix Analysis**: 5 standard UW questions + 6 kill questions = 11 total primary questions

**Questions 1-3: Standard Information Collection**
1. **Code 9000**: "1A. Is the Applicant a subsidiary of another entity?" (Not Required)
2. **Code 9001**: "1B. Does the Applicant have any subsidiaries?" (Not Required)  
3. **Code 9002**: "2. Is a formal safety program in operation?" (Not Required)

**Questions 4-9: Kill Questions (Required)**
4. **Code 9003**: "3. Any exposure to flammables, explosives, chemicals?" (KILL - Required)
5. **Code 9006**: "5. Any policy or coverage declined, cancelled or non-renewed during the prior 3 years for any premises or operations?" (KILL - Required)
6. **Code 9007**: "6. Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?" (KILL - Required)
7. **Code 9008**: "7. During the last five years has any Applicant been indicted for or convicted of any degree of the crime of fraud, bribery, arson or any other arson-related crime in connection with this or any other property?" (TRUE KILL - Required)
8. **Code 9009**: "8. Any uncorrected fire and/or safety code violations?" (KILL - Required)
9. **Code 9400**: "9. Has Applicant had a foreclosure, repossession, bankruptcy or filed for bankruptcy in the last five (5) years?" (KILL - Required)

**Questions 10-11: Standard Information Collection**
10. **Code 9005**: "4. Any other insurance with this company? (List Policy Numbers)" (Not Required)
11. **Code 9010**: "10. Has Applicant had a judgement or lien during the last five (5) years?" (Not Required)

**Source Verification**: All questions verified from UWQuestions.vb, lines 1067-1199, GetCommercialBOPUnderwritingQuestions() method

### 3.3 Question Classification and Processing Logic

**Kill Question Processing**:
- **Immediate Impact Questions**: Codes 9003, 9006, 9007, 9008, 9009, 9400
- **True Kill Question**: Code 9008 (IsTrueKillQuestion = True) - immediately stops quote processing
- **Standard Kill Questions**: Remaining kill questions trigger underwriting review and additional information requirements
- **Popup Display Logic**: Kill questions appear in both application context and popup modal context

**Standard UW Question Processing**:
- **Information Collection**: Codes 9000, 9001, 9002, 9005, 9010
- **Optional Response**: Not required fields, support business risk profiling
- **Application Context Only**: Display only in application workflow, not in kill question popups

---

## 4. UI/UX Requirements ⭐ MANDATORY

### 4.1 Auto-Display/Hide Behaviors

**Additional Information Panel Display Logic**:

When user selects "Yes" for any question, the Additional Information panel automatically displays below the radio buttons. When user selects "No" or no selection is made, the panel remains hidden unless the question has "AlwaysShowDescription" property set.

**Implementation Specification**:
- **Trigger Condition**: Radio button "Yes" selection activates display logic
- **Default State**: Hidden (style="display:none;")  
- **Show Condition**: "Yes" selection OR AlwaysShowDescription="true"
- **Hide Condition**: "No" selection AND AlwaysShowDescription="false"
- **Control Classes**: CSS classes control display behavior
  - `alwaysShow`: Panel always visible regardless of selection
  - `neverShow`: Panel never displays regardless of selection
  - Default: Panel displays only on "Yes" selection

**JavaScript Function**: Dynamic panel management handled by question-specific logic
**Source**: ctlCommercialUWQuestionItem.ascx, DescriptionTable element with conditional CSS classes

### 4.2 Text Input Specifications

**Field Specifications**:

| Field Name | Label | Type | Character Limit | Required | Default |
|------------|-------|------|-----------------|----------|---------|
| txtUWQDescription | "Additional Information" | Multi-line | 125 chars | Conditional | Empty |

**Character Limit Details**:
- **Maximum Characters**: 125 (exact limit for BOP questions)
- **Real-time Character Counter**: Displays remaining characters as user types
- **Validation Function**: `CheckMaxTextNoDisable(this, 125)`
- **Input Restrictions**: Both OnKeyUp and OnPaste events trigger validation
- **Source**: ctlCommercialUWQuestionItem.ascx, line 36: `maxLength="125" OnKeyUp="CheckMaxTextNoDisable(this, 125);"`

**Text Area Properties**:
- **Dimensions**: 4 rows × 50 columns display area
- **CSS Class**: "DescriptionTextBox" for consistent styling
- **Multi-line Support**: TextMode="MultiLine" enables paragraph entry
- **Focus Behavior**: Focus returns to text area after validation error

### 4.3 Validation Visual Indicators

**Character Limit Exceeded State**:
- **Visual**: Red border around text area
- **Error Message**: "Maximum of 125 characters exceeded" (displayed in red)
- **Character Counter**: Shows exceeded character count in red
- **Button State**: Submit button disabled when limit exceeded  
- **Trigger**: Real-time as user types or pastes content
- **Validation Function**: `CheckMaxTextNoDisable(textarea, 125)`
- **Source**: VrApp.js, CheckMaxText function implementation

**Empty Required Field (Kill Questions)**:
- **Visual**: Red asterisk (*) next to radio buttons
- **Label Change**: "Additional Information Response Required" in red text
- **Border**: Red border around empty required text area
- **Trigger**: Form submission attempted with unanswered required question
- **Recovery**: Visual indicators clear when question answered
- **Source**: ctlUWQuestions.ascx, AllOpenTextboxesHaveValues() function

**Success/Normal States**:
- **Visual**: Normal border (no border styling)
- **Message**: "[X] characters remaining" in black text
- **Submit Button**: Enabled when all validation passes
- **Required Indicator**: Asterisk hidden when question answered

### 4.4 Interactive Elements

**Radio Buttons**:
- **Options**: "No" (left) and "Yes" (right) for each question
- **Selection Behavior**: Mutually exclusive within question group
- **Default State**: No selection (both unchecked)
- **Required Indicator**: Red asterisk appears for unanswered required questions
- **Group Management**: Each question has unique group identifier

**Submit Buttons**:
- **Primary**: "Save" button (StandardSaveButton CSS class)
- **Secondary**: "Application" button for workflow navigation
- **Width**: 150px standardized button width
- **Validation**: OnClientClick='return ValidateForm();' prevents invalid submission
- **State Management**: Disabled when character limits exceeded

**Additional Information Panels**:
- **Toggle Behavior**: Show/hide based on "Yes"/"No" selection
- **Label**: "Additional Information" standard across all questions
- **Text Area**: 125-character limit with real-time validation
- **Display Logic**: Conditional based on question configuration

### 4.5 Accessibility Requirements

**ARIA Labels**: 
- Radio button groups labeled with question text
- Text areas labeled "Additional Information for Question [X]"
- Character counters announced to screen readers

**Keyboard Navigation**:
- Tab order: Radio buttons → Text area → Submit buttons
- Arrow key navigation within radio button groups
- Focus indicators visible on all interactive elements

**Screen Reader Text**:
- Question requirements announced ("Required" or "Optional")
- Character limit information provided ("125 character maximum")
- Validation error messages read aloud when triggered

**Color Contrast**: WCAG 2.1 AA compliance maintained
- Red error indicators: 4.5:1 contrast ratio minimum
- Black text on white background: High contrast maintained

### 4.6 Responsive Design Requirements

**Desktop Implementation**: 
- Question table layout with fixed column widths (500px left, 132px right)
- Text areas: 450px width × 50px height standard sizing
- Button alignment: Center-aligned with consistent spacing

**Browser Compatibility**:
- Internet Explorer 11+ supported
- Chrome, Firefox, Safari, Edge current versions
- JavaScript validation functions cross-browser compatible

---

## 5. Validation Rules and Business Logic ⭐ MANDATORY

### 5.1 Client-Side Validation (JavaScript)

**Function: CheckMaxTextNoDisable(textarea, maxLength)**
- **Purpose**: Validates 125-character limit for BOP additional information fields
- **Trigger**: Real-time on KeyUp and OnPaste events
- **Logic**: 
  - Counts current character length against 125-character maximum
  - When limit exceeded: applies red border, disables text area, displays error message
  - When under limit: shows remaining character count, enables normal styling
- **Visual Feedback**: Red border on text area, error message in red text
- **Error Message**: "Maximum of 125 characters exceeded"
- **Source**: VrApp.js, CheckMaxText function (adapted for BOP with no-disable behavior)

**Function: AllQuestionsAreAnswered()**
- **Purpose**: Validates all required questions have been answered
- **Trigger**: Form submission attempt
- **Logic**: Iterates through question tables, checks radio button selections
- **Visual Feedback**: Red asterisk (*) appears next to unanswered required questions
- **Error State**: "All Questions Must Be Answered" label turns red
- **Source**: ctlUWQuestions.ascx, lines for validation logic

**Function: AllOpenTextboxesHaveValues()**
- **Purpose**: Validates required additional information fields are completed
- **Trigger**: Form submission when required text areas are visible
- **Logic**: Checks visible text areas associated with answered questions
- **Visual Feedback**: Red border on empty text area, error message update
- **Error Message**: "Additional Information Response Required"
- **Source**: ctlUWQuestions.ascx, validation function implementation

### 5.2 Character Limit Validation

**Function: CheckMaxTextNoDisable(field, 125)**
- **Character Limit**: 125 characters maximum (BOP-specific limit)
- **Validation Type**: Real-time (as user types) AND on paste operations
- **Behavior**: 
  - **Under Limit**: Displays "[X] characters remaining" in black text
  - **At Limit**: Prevents further input, shows "Maximum of 125 characters exceeded" in red
  - **Recovery**: Allows backspace/delete to reduce character count
- **Visual Feedback**: Dynamic border color (normal/red), character counter, error text
- **Submit Impact**: Does not disable submit button (NoDisable version for BOP)
- **Source**: ctlCommercialUWQuestionItem.ascx, maxLength="125" OnKeyUp="CheckMaxTextNoDisable(this, 125);"

### 5.3 Required Field Validation

**Required Fields by Question Type**:

| Question Code | Question Text | Required When | Error Indicator |
|---------------|---------------|---------------|-----------------|
| 9003 | Flammables/explosives | Always | Red asterisk |
| 9006 | Prior coverage declined | Always | Red asterisk |
| 9007 | Sexual abuse/discrimination | Always | Red asterisk |
| 9008 | Fraud/arson conviction | Always | Red asterisk |
| 9009 | Fire code violations | Always | Red asterisk |
| 9400 | Bankruptcy/foreclosure | Always | Red asterisk |
| 9000, 9001, 9002, 9005, 9010 | Standard questions | Never | No indicator |

**Conditional Additional Information Requirements**:
- **Trigger**: Any "Yes" selection on kill questions requires additional information
- **Validation**: Text area must contain content when visible and required
- **Error Message**: "Additional Information Response Required"
- **Visual**: Red border on text area, red error text

### 5.4 Business Rule Validation

**Rule 1: Kill Question Processing**
- **Description**: Questions designated as kill questions (9003, 9006, 9007, 9008, 9009, 9400) trigger enhanced processing
- **Validation Logic**: "Yes" responses require additional information, may trigger underwriting review
- **Error Handling**: Additional information required validation, popup modal display capability
- **Source**: UWQuestions.vb, GetCommercialBOPUnderwritingQuestions() with kill question flagging

**Rule 2: True Kill Question Handling**
- **Description**: Question 9008 (fraud/arson conviction) is designated as "True Kill Question"
- **Validation Logic**: "Yes" response immediately stops quote processing
- **Error Handling**: Quote archival process, navigation back to MyVelocirater
- **Source**: UWQuestions.vb, line 1151-1162, .IsTrueKillQuestion = True property

**Rule 3: Additional Information Conditional Display**
- **Description**: Additional information panels display based on question configuration
- **Validation Logic**: Panel visibility controlled by AlwaysShowDescription, NeverShowDescription properties
- **Business Impact**: Ensures appropriate information collection based on risk assessment needs
- **Source**: ctlCommercialUWQuestionItem.ascx, CSS class management for DescriptionTable

### 5.5 Server-Side Validation

**Data Persistence Validation**:
- **Answer Values**: "1" (Yes), "-1" (No), "0" (No Answer) stored in PolicyUnderwritingAnswer
- **Additional Information**: Text content stored in PolicyUnderwritingExtraAnswer with 125-character database limit
- **Question Association**: Diamond code stored in PolicyUnderwritingCodeId for regulatory tracking
- **Source**: ctlCommercialUWQuestionItem.ascx.vb, Save() function implementation

**Security Validations**:
- **Input Sanitization**: Server-side validation of additional information text content
- **Cross-Site Scripting Prevention**: HTML encoding of user-entered text
- **SQL Injection Prevention**: Parameterized queries for database operations
- **Data Type Validation**: Answer values restricted to valid enumeration (-1, 0, 1)

**Data Integrity Checks**:
- **Question Code Validation**: Ensures submitted question codes match valid BOP question set
- **Answer Consistency**: Validates additional information provided only when question answered "Yes"
- **Character Limit Enforcement**: Server-side 125-character limit validation as backup to client-side
- **Required Field Enforcement**: Server-side validation that kill questions are answered when submitted

---

## 6. User Stories and Acceptance Criteria

### US-BOP-UW-001: Complete Required Kill Questions

**As an** Insurance Agent  
**I need to** answer all required kill questions for a BOP application  
**So that** I can determine if the risk is eligible for coverage and proceed with the application

**Acceptance Criteria:**
1. Given I am on the BOP underwriting questions page, when I attempt to submit without answering required questions, then red asterisks appear next to unanswered questions and submission is prevented
2. Given I answer "Yes" to any kill question, when the additional information panel appears, then I must provide text content before submitting
3. Given I answer "No" to all kill questions, when I submit the form, then the application proceeds to the next step without additional information requirements
4. Given I answer question 9008 (fraud/arson conviction) with "Yes", when I confirm the selection, then the quote is immediately archived and I am returned to MyVelocirater

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: Diamond question code integration, kill question filtering logic

### US-BOP-UW-002: Provide Additional Information with Character Limit Compliance

**As an** Insurance Agent  
**I need to** provide additional information for "Yes" responses within the 125-character limit  
**So that** underwriters have sufficient detail for risk assessment while maintaining data consistency

**Acceptance Criteria:**
1. Given I select "Yes" for any question, when the additional information panel appears, then I can enter up to 125 characters
2. Given I am typing in an additional information field, when I reach the 125-character limit, then I see "Maximum of 125 characters exceeded" and the text area shows a red border
3. Given I have exceeded the character limit, when I delete characters to get below 125, then the error message clears and normal styling returns
4. Given I am entering text, when I have remaining characters, then I see "[X] characters remaining" displayed in black text

**Priority**: High  
**Complexity**: Small  
**Dependencies**: Character validation JavaScript function, UI styling components

### US-BOP-UW-003: Navigate Question Flow with Visual Feedback

**As an** Insurance Agent  
**I need to** receive clear visual feedback on question completion status  
**So that** I can efficiently complete the underwriting questions without missing required information

**Acceptance Criteria:**
1. Given I have unanswered required questions, when I attempt to submit, then "All Questions Must Be Answered" appears in red
2. Given I answer a question that requires additional information, when I leave the text area empty, then it shows a red border with "Additional Information Response Required"
3. Given I have completed all required fields, when all validation passes, then the submit button remains enabled and visual indicators show normal state
4. Given I select "Yes" or "No" for a question, when the selection is made, then any error indicators for that question disappear

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: JavaScript validation functions, CSS styling for error states

### US-BOP-UW-004: Review Standard Information Collection Questions

**As an** Insurance Agent  
**I need to** complete optional standard underwriting questions  
**So that** I can provide comprehensive risk information without being blocked by non-critical requirements

**Acceptance Criteria:**
1. Given I am answering standard questions (9000, 9001, 9002, 9005, 9010), when I select "Yes" or "No", then additional information panels may appear but are not required
2. Given I leave standard questions unanswered, when I submit the form, then submission is not prevented by these questions
3. Given I provide additional information for standard questions, when I submit, then the information is saved with the application
4. Given I am reviewing question requirements, when I see questions without asterisks, then I understand these are optional

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: Question classification logic, optional field handling

### US-BOP-UW-005: Validate Question Data Persistence

**As an** Underwriter  
**I need to** review saved underwriting question responses with associated additional information  
**So that** I can make informed risk assessment decisions based on complete application data

**Acceptance Criteria:**
1. Given an agent has completed underwriting questions, when I review the application, then all "Yes"/"No" answers are clearly displayed
2. Given additional information was provided, when I review question responses, then the text is visible with question association maintained
3. Given a kill question was answered "Yes", when I review the application, then it is flagged for underwriting attention
4. Given question 9008 was answered "Yes", when I check the application status, then it shows as archived with appropriate disposition

**Priority**: High  
**Complexity**: Large  
**Dependencies**: Data persistence layer, underwriting review interface, question classification system

### US-BOP-UW-006: Access Question Information Across Dual System Architecture

**As a** System Administrator  
**I need to** verify that questions appear correctly in both popup and application contexts  
**So that** the dual architecture maintains data consistency and proper user experience

**Acceptance Criteria:**
1. Given kill questions are configured, when they appear in popup context, then the same questions appear in application context
2. Given a question is answered in one context, when viewed in another context, then the answer persists correctly
3. Given question configuration changes, when questions are loaded, then both popup and application systems reflect updates
4. Given diagnostic testing is performed, when comparing question sets, then kill question filtering produces expected results

**Priority**: Medium  
**Complexity**: Large  
**Dependencies**: Question loading architecture, kill question filtering logic, data consistency validation

### US-BOP-UW-007: Maintain Regulatory Compliance Through Question Tracking

**As a** Compliance Officer  
**I need to** verify that all required questions are presented and answered according to regulatory requirements  
**So that** BOP applications meet state insurance regulatory standards

**Acceptance Criteria:**
1. Given regulatory requirements for question presentation, when questions are loaded, then all required Diamond codes are present
2. Given questions are answered, when audit trail is created, then question codes and responses are properly recorded
3. Given regulatory examination occurs, when question compliance is reviewed, then documentation demonstrates proper question administration
4. Given state-specific requirements exist, when questions are presented, then appropriate questions appear for the application state

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: Diamond integration, regulatory compliance tracking, audit trail functionality

---

## 7. Testing Requirements

### 7.1 Functional Testing

**Test Scenario 1: Kill Question Identification and Processing**
- **Setup**: Configure test BOP application with all 11 primary questions loaded
- **Steps**: 
  1. Verify questions 9003, 9006, 9007, 9008, 9009, 9400 display with required indicators
  2. Answer each kill question "Yes" and verify additional information panel appears
  3. Submit form and verify additional information is required for "Yes" responses
  4. Answer question 9008 "Yes" and verify true kill processing (quote archival)
- **Expected Result**: Kill questions properly identified, additional information required, true kill question archives quote

**Test Scenario 2: Standard Question Optional Processing**
- **Setup**: Load questions 9000, 9001, 9002, 9005, 9010 in test environment
- **Steps**:
  1. Leave all standard questions unanswered
  2. Submit form and verify submission proceeds
  3. Answer some standard questions "Yes" and verify additional information panels appear
  4. Submit with optional additional information and verify data persistence
- **Expected Result**: Standard questions do not block submission, optional information saves correctly

**Test Scenario 3: 125-Character Limit Enforcement**
- **Setup**: Configure BOP questions with character limit validation active
- **Steps**:
  1. Enter exactly 125 characters in additional information field
  2. Attempt to enter 126th character and verify prevention
  3. Paste text longer than 125 characters and verify truncation/error
  4. Reduce character count and verify error state clears
- **Expected Result**: 125-character limit strictly enforced, visual feedback accurate, error recovery functional

### 7.2 UI Behavior Testing

**Auto-Display/Hide Panel Testing**:
- **Test 1**: Select "No" for question with conditional panel → Panel remains hidden
- **Test 2**: Select "Yes" for question with conditional panel → Panel appears immediately
- **Test 3**: Questions with "AlwaysShowDescription" → Panel always visible regardless of selection
- **Test 4**: Questions with "NeverShowDescription" → Panel never appears
- **Expected Results**: Panel visibility matches question configuration exactly

**Validation Visual Indicator Testing**:
- **Test 1**: Submit form with unanswered required questions → Red asterisks appear
- **Test 2**: Exceed character limit in text area → Red border and error message appear
- **Test 3**: Complete required field → Visual error indicators disappear
- **Test 4**: Character counter accuracy → Displays correct remaining character count
- **Expected Results**: All validation indicators appear/disappear correctly

### 7.3 Cross-Browser Testing

**Browser Support Matrix**:
- **Internet Explorer 11**: JavaScript validation functions, CSS styling, form submission
- **Chrome (Latest)**: Real-time character validation, panel show/hide, responsive layout
- **Firefox (Latest)**: Form validation, error message display, keyboard navigation
- **Safari (Latest)**: Text area behavior, button functionality, visual indicators
- **Edge (Latest)**: Complete workflow testing, validation accuracy

**Test Coverage Per Browser**:
- Character limit validation accuracy
- Panel show/hide behavior
- Form submission validation
- Error message display
- CSS styling consistency

### 7.4 Accessibility Testing

**Screen Reader Compatibility**:
- **JAWS**: Question text reading, validation error announcements, character limit notifications
- **NVDA**: Form navigation, radio button group identification, required field identification
- **VoiceOver**: Text area labeling, error state communication, submission feedback

**Keyboard Navigation Testing**:
- **Tab Order**: Questions → Radio buttons → Text areas → Submit buttons
- **Arrow Keys**: Within radio button groups
- **Enter/Space**: Radio button activation, button submission
- **Focus Indicators**: Visible focus outline on all interactive elements

### 7.5 Performance Testing

**Question Loading Performance**:
- **Test**: Load all 11 BOP questions simultaneously
- **Metric**: Page load time < 2 seconds
- **Validation**: All questions render without delay

**Real-time Validation Performance**:
- **Test**: Type rapidly in text area with character limit validation
- **Metric**: Validation feedback appears within 100ms
- **Validation**: No input lag or character loss during validation

**Form Submission Performance**:
- **Test**: Submit form with all questions answered and additional information provided
- **Metric**: Submission processing < 3 seconds
- **Validation**: All data saves correctly without timeout

---

## 8. Migration and Modernization Considerations

### 8.1 Data Migration

**Question Response Data Migration**:
- **Current Format**: PolicyUnderwritingAnswer values (-1, 0, 1) in Diamond format
- **Migration Requirement**: Preserve existing question responses during system upgrade
- **Data Mapping**: Maintain Diamond code associations for regulatory continuity
- **Validation**: Verify all historical BOP question responses migrate correctly

**Additional Information Migration**:
- **Current Storage**: PolicyUnderwritingExtraAnswer field with varying character limits
- **Standardization**: Migrate to consistent 125-character limit for BOP
- **Data Truncation**: Handle existing responses exceeding 125 characters with user notification
- **Backup Strategy**: Preserve original additional information in archived format

### 8.2 Configuration Migration

**Question Configuration Updates**:
- **Kill Question Flags**: Migrate IsRequired, IsTrueKillQuestion properties
- **Display Logic**: Migrate AlwaysShowDescription, NeverShowDescription settings
- **Diamond Code Mapping**: Preserve regulatory question code associations
- **LOB Associations**: Maintain BOP-specific question filtering logic

**UI Configuration Migration**:
- **Character Limits**: Standardize on 125-character limit across all BOP questions
- **Validation Rules**: Migrate existing validation logic to new framework
- **Error Messages**: Standardize error message text across implementations
- **Panel Display Logic**: Migrate conditional panel show/hide rules

### 8.3 Integration Impact

**Diamond System Integration**:
- **Question Synchronization**: Maintain Diamond code alignment during migration
- **Regulatory Compliance**: Preserve regulatory question requirements mapping
- **Audit Trail**: Ensure migration maintains compliance audit capabilities
- **State-Specific Rules**: Preserve any state-specific question variations

**Kill Question Popup Integration**:
- **Dual System Maintenance**: Ensure kill question filtering continues during migration
- **Popup Functionality**: Preserve popup modal behavior for kill question screening
- **Question Overlap**: Maintain proper question display in both contexts
- **Data Consistency**: Ensure answers persist correctly across both systems

### 8.4 Rollback Strategy

**Configuration Rollback**:
- **Question Configuration**: Ability to revert to previous question set if issues arise
- **Character Limits**: Option to restore previous character limit settings
- **Validation Rules**: Rollback capability for validation logic changes
- **UI Behavior**: Restore previous panel display and error handling logic

**Data Rollback Protection**:
- **Response Preservation**: Maintain ability to access question responses in previous format
- **Additional Information**: Preserve original additional information content
- **Audit Trail**: Maintain historical question administration records
- **Integration Points**: Restore previous Diamond system integration if needed

---

## 9. Source Attribution and Traceability

### 9.1 Source Code Files Analyzed

| File Path | Purpose | Lines Analyzed |
|-----------|---------|----------------|
| IFM.VR.Common/UWQuestions/UWQuestions.vb | BOP question definitions and logic | 1012-1447 |
| User Controls/VR Commercial/Application/BOP/ctlCommercialUWQuestionItem.ascx | BOP-specific UI control | Complete file |
| User Controls/VR Commercial/Application/BOP/ctlCommercialUWQuestionItem.ascx.vb | BOP question processing logic | Complete file |
| User Controls/VR Commercial/Application/BOP/ctlCommercialUWQuestionList.ascx | BOP question list management | Complete file |
| User Controls/Application/ctlUWQuestions.ascx | General UW questions control | 687 |
| js/VrApp.js | Character validation functions | 265-291 |

### 9.2 Key Functions and Methods

| Function Name | File | Line | Purpose |
|---------------|------|------|---------|
| GetCommercialBOPUnderwritingQuestions() | UWQuestions.vb | 1012 | Primary BOP question loading |
| GetKillQuestions() | UWQuestions.vb | 52-62 | Kill question filtering |
| CheckMaxTextNoDisable() | VrApp.js | 265 | Character limit validation |
| AllQuestionsAreAnswered() | ctlUWQuestions.ascx | JS | Required question validation |
| AllOpenTextboxesHaveValues() | ctlUWQuestions.ascx | JS | Additional info validation |
| Save() | ctlCommercialUWQuestionItem.ascx.vb | 45 | Question response persistence |

### 9.3 Traceability Matrix

| Requirement ID | Source Code Reference | Validation |
|----------------|----------------------|------------|
| BOP-UW-001 (11 Questions) | UWQuestions.vb:1067-1199 | Rex Pattern Analysis |
| BOP-UW-002 (125 Char Limit) | ctlCommercialUWQuestionItem.ascx:36 | Source Code Verification |
| BOP-UW-003 (Kill Questions) | UWQuestions.vb:GetKillQuestions() | Diamond Code Analysis |
| BOP-UW-004 (Dual Architecture) | ctlUWQuestionsPopup.ascx + ctlCommercialUWQuestionList.ascx | Control Implementation |
| BOP-UW-005 (Validation Logic) | VrApp.js:CheckMaxTextNoDisable | JavaScript Function |
| BOP-UW-006 (UI Behaviors) | ctlCommercialUWQuestionItem.ascx:CSS Classes | Dynamic Panel Logic |
| BOP-UW-007 (Data Persistence) | ctlCommercialUWQuestionItem.ascx.vb:Save() | Server-side Processing |

---

## 10. Document Metadata

**Prepared By**: Mason (IFI Requirements Extraction Specialist)  
**Reviewed By**: [Pending Vera Quality Validation]  
**Approved By**: [Pending IFI Technical Authority]  
**Document Location**: `//project/ifm/product_requirements/BOP/Underwriting_Questions/Modernization_BOP_UnderwritingQuestions.md`

**Analysis Source**: Rex (IFI Pattern Miner) - BOP 11 Questions Complete Analysis  
**Architecture Input**: [Pending Aria IFI Architect Review]  
**Domain Validation**: [Pending Rita IFI Insurance Specialist Review]  
**Orchestration**: Douglas (IFI Orchestrator Enhanced)

**Source Analysis Files**:
- `//project/ifm/meta/rex/bop_11_questions_corrected/bop_11_questions_complete.md`
- `//project/ifm/meta/rex/bop_11_questions_corrected/corrected_handoff_summary.md`
- `//project/ifm/meta/rex/bop_11_questions_corrected/bop_error_analysis.md`

**Lessons Learned Applied**:
- BOP Popup Questions Discovery Pattern (hybrid loading verification)
- Character limit validation patterns from similar LOB implementations
- Dual-system architecture recognition from WCP analysis patterns

**Token Budget Used**: ~18K / 25K tokens

---

**END OF REQUIREMENTS DOCUMENT**