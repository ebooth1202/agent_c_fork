# Workers' Compensation (WCP) - Section 1.1 Initial Quote Kill Questions

## User Experience Overview
**User Action:** User initiates WCP quote process  
**System Response:** System presents modal popup with 6 mandatory risk assessment questions  
**User Must Do:** Answer all questions before quote development can proceed

---

## Question 1: Aircraft/Watercraft Risk Assessment

**Question Text:** "Does Applicant own, operate or lease aircraft or watercraft?"  
**Response Options:** Yes/No radio buttons (required)  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** Selection recorded for underwriting review with risk flag
- **Business Rule:** "Yes" answer flags as potential ineligibility risk
- **Diamond Integration:** Records response with Diamond code 9341 for audit trail

---

## Question 2: Hazardous Materials Operations

**Question Text:** "Do/have past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material? (e.g. landfills, wastes, fuel tanks, etc.)"  
**Response Options:** Yes/No radio buttons (required)  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** Selection recorded for underwriting review with risk flag
- **Business Rule:** "Yes" answer flags as potential ineligibility risk
- **Diamond Integration:** Records response with Diamond code 9086 for audit trail

---

## Question 3: Employee Geographic Coverage

**Multi-State Scenario:**  
**Question Text:** "Do any employees live outside the state(s) of Indiana, Illinois, or Kentucky?"  

**Single-State Scenario:**  
**Question Text:** "Do any employees live outside the state of [governing state]?"  

**Response Options:** Yes/No radio buttons (required)  
**Business Rule:** Question text adapts based on multi-state capability and effective date

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row
- **Dynamic Question Text:** Question text automatically adapts based on multi-state capability

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** Selection recorded for underwriting review with geographic coverage analysis
- **Business Rule:** "Yes" answer triggers geographic coverage validation
- **Diamond Integration:** Records response with Diamond codes 9573/9342 for audit trail

---

## Question 4: Coverage History Verification

**Question Text:** "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"  
**Response Options:** Yes/No radio buttons (required)  
**Time Scope:** 3-year lookback period
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** Selection recorded for underwriting review with coverage history analysis
- **Business Rule:** "Yes" answer flags as potential ineligibility risk
- **Diamond Integration:** Records response with Diamond code 9343 for audit trail

---

## Question 5: Business Operation Classification

**Question Text:** "Is the Applicant involved in the operation of a professional employment organization, employee leasing operation, or temporary employment agency?"  
**Response Options:** Yes/No radio buttons (required)  
**Business Rule:** "Yes" answer flags as potential ineligibility risk

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** Selection recorded for underwriting review with business operation analysis
- **Business Rule:** "Yes" answer flags as potential ineligibility risk
- **Diamond Integration:** Records response with Diamond code 9344 for audit trail

---

## Question 6: Financial Stability Assessment (True Kill Question)

**Question Text:** "Any tax liens or bankruptcy within the last 5 years? (If 'Yes', please specify)"  
**Response Options:** Yes/No radio buttons (required)  
**Time Scope:** 5-year lookback period  
**Special Processing:** This is a true kill question with immediate termination

### User Interaction Flow & UI Behavior

**Initial Display:**
- **Required Indicator:** Red asterisk (*) initially hidden, appears if unanswered
- **Additional Information Section:** Initially hidden below question row

**User Action: Selects "Yes"**
- **System Response:** Additional information text area immediately appears below question
- **Text Area Specifications:**
  - **Label:** "Additional Information"
  - **Text Box Type:** Multi-line text area (`TextMode="MultiLine"`)
  - **Styling:** Standard border, no character limit specified
  - **Required:** Text input required when "Yes" selected

**User Action: Selects "No"**
- **System Response:** Additional information text area immediately hides
- **Validation:** No additional text required

**User Action: Attempts to save without answering**
- **Visual Indicator:** Red asterisk (*) appears next to "Yes" radio button
- **Border Change:** Question row receives red border highlight
- **Tooltip:** "Response Required" appears on hover
- **Error State:** Prevents form submission

**User Action: Selects "Yes" but leaves text area empty**
- **Text Area Border:** Changes to red
- **Label Color:** Changes from black to red
- **Label Text:** Changes from "Additional Information" to **"Additional Information Response Required"**
- **Validation Block:** Prevents form submission until text entered

**User Action: Enters text after "Yes" selection**
- **Text Area Border:** Returns to normal styling
- **Label Color:** Returns to black
- **Label Text:** Returns to "Additional Information"
- **Form Status:** Ready for submission

**User Action: Selects "Yes" with valid text and clicks Continue**
- **System Response:** **IMMEDIATE QUOTE TERMINATION** - workflow stops completely
- **Business Rule:** True kill question - no further processing allowed
- **Diamond Integration:** Records response with Diamond code 9107 for audit trail

### Technical Implementation Details
**Source Code Location:** ctlUWQuestionsPopup.ascx, Repeater1 ItemTemplate
**JavaScript Validation:** `AllAnswersAreAnswered()` and `AllAdditionalInfoFieldsAreAnswered()` functions
**Server Integration:** Diamond system codes for regulatory compliance
**CSS Classes:** Standard form styling with dynamic red error states