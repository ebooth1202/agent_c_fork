# WCP Modal Window and Extra Info Box User Stories
## Comprehensive User Story Collection

**FROM**: Mason (Requirements Extraction Specialist)  
**SOURCE**: Rex's WCP modal pattern analysis transformed into stakeholder requirements  
**PURPOSE**: Development-ready user stories with acceptance criteria  
**TARGET**: Development teams, product owners, business analysts  

---

## EPIC 1: UNDERWRITING QUESTIONS COLLECTION

### Story 1.1: Display Underwriting Questions Modal
**As a** WCP quote user  
**I want** the system to automatically display underwriting questions in a popup window  
**So that** I can provide required underwriting information without leaving the main quote form  

**Acceptance Criteria**:
- [ ] Modal window appears automatically during WCP quote workflow  
- [ ] Window displays "Underwriting Questions" title  
- [ ] Window is 550 pixels wide and cannot be dragged  
- [ ] Window cannot be closed without completing all requirements  
- [ ] Effective date picker is included and functional  
- [ ] All questions display with Yes/No radio button options  

**Source Evidence**: `ctlUWQuestionsPopup.ascx` integrated in WCP Quote workflow  

### Story 1.2: Answer Underwriting Questions
**As a** WCP quote user  
**I want** to answer Yes or No to each underwriting question  
**So that** the system can assess my risk profile for workers' compensation coverage  

**Acceptance Criteria**:
- [ ] Each question displays with clear Yes/No radio button options  
- [ ] Questions have alternating background colors for readability  
- [ ] All questions must be answered before form submission  
- [ ] Visual indicators (red asterisk) appear for unanswered questions  
- [ ] Questions are sourced dynamically from underwriting system  

**Source Evidence**: Repeater-driven question structure in `ctlUWQuestionsPopup.ascx`

### Story 1.3: Provide Additional Information When Required
**As a** WCP quote user  
**I want** additional information text boxes to appear only when I answer "Yes" to questions  
**So that** I can provide necessary details without cluttering the interface  

**Acceptance Criteria**:
- [ ] Additional info text box appears immediately when "Yes" is selected  
- [ ] Text box hides and clears content when "No" is selected  
- [ ] Text box displays "Additional Information" label  
- [ ] Text box width is 90% of available space  
- [ ] Text box supports multiple lines of text  

**Source Evidence**: `ShowHideAdditionalInfo()` function lines 267-279

### Story 1.4: Validate Additional Information Completeness
**As a** WCP quote user  
**I want** the system to require additional information when I answer "Yes"  
**So that** I provide complete information for underwriting review  

**Acceptance Criteria**:
- [ ] Additional info becomes required field when "Yes" is selected  
- [ ] Empty required additional info fields show red border  
- [ ] Error message "Additional Information Response Required" displays  
- [ ] Form cannot be submitted with incomplete required additional info  
- [ ] 125 character limit enforced with real-time validation  

**Source Evidence**: `AllAdditionalInfoFieldsAreAnswered()` validation function lines 504-528

### Story 1.5: Complete Multi-Layer Form Validation
**As a** WCP quote user  
**I want** comprehensive validation before form submission  
**So that** I don't encounter errors after spending time completing the form  

**Acceptance Criteria**:
- [ ] All questions must have Yes or No selection  
- [ ] All conditional additional information must be completed  
- [ ] Effective date must be valid and within allowed range  
- [ ] LOB-specific additional questions must be answered  
- [ ] Form submission blocked until all validation passes  
- [ ] Real-time validation feedback provided  

**Source Evidence**: `ValidateUWForm()` validation chain lines 824-870

---

## EPIC 2: QUOTE ELIGIBILITY MANAGEMENT

### Story 2.1: Handle Ineligible Risk Confirmation
**As a** WCP quote user encountering Diamond Code 9107  
**I want** clear confirmation before my quote becomes ineligible  
**So that** I understand the consequences and can correct errors  

**Acceptance Criteria**:
- [ ] Confirmation dialog displays when Diamond Code 9107 answered "Yes"  
- [ ] Dialog message: "The risk is ineligible, if answered 'Yes' in error select 'Cancel'. If answered correctly, select 'OK'"  
- [ ] "OK" button triggers quote ineligibility process  
- [ ] "Cancel" button resets answer to "No" and continues quote  
- [ ] Dialog prevents accidental ineligibility declaration  

**Source Evidence**: `HandleRadioButtonClicksWCP()` function lines 316-351

### Story 2.2: Process Quote Archival for Ineligible Risk
**As a** WCP underwriting system  
**I want** to automatically archive quotes declared ineligible  
**So that** ineligible risks cannot proceed through the quote process  

**Acceptance Criteria**:
- [ ] Quote automatically archived when ineligibility confirmed  
- [ ] User redirected to MyVelocirater main page  
- [ ] Quote cannot be reopened or continued  
- [ ] Archival action creates permanent audit trail  
- [ ] System call to GenHandlers/UWHandler.ashx completes successfully  

**Source Evidence**: `ArchiveQuote()` function with JSON call

### Story 2.3: Prevent Accidental Ineligibility Declaration
**As a** WCP quote user who made an error  
**I want** the ability to cancel ineligibility confirmation  
**So that** I can correct my mistake and continue the quote  

**Acceptance Criteria**:
- [ ] "Cancel" option available in ineligibility confirmation dialog  
- [ ] "Cancel" resets Diamond Code 9107 answer to "No"  
- [ ] Quote process continues normally after cancellation  
- [ ] No archival or redirection occurs when cancelled  
- [ ] User can continue completing the quote form  

**Source Evidence**: Reset logic in `HandleRadioButtonClicksWCP()` function

---

## EPIC 3: COVERAGE MANAGEMENT ALERTS

### Story 3.1: Display Sole Proprietor Documentation Alert
**As a** WCP quote user selecting sole proprietor coverage  
**I want** to be notified of health insurance documentation requirements  
**So that** I understand what additional documentation is needed  

**Acceptance Criteria**:
- [ ] Alert displays when sole proprietor coverage checkbox selected  
- [ ] Alert message: "Sole Proprietors, Partners & LLC Members who elect to be included must provide written proof of health insurance coverage via the Upload tool in VelociRater or sent to your Underwriter."  
- [ ] Alert requires user acknowledgment  
- [ ] Documentation requirement clearly communicated  
- [ ] Upload tool and underwriter submission options explained  

**Source Evidence**: `CoverageCheckboxChanged` function in `vrWCP.js` line 33

### Story 3.2: Handle Coverage Deletion Safely
**As a** WCP quote user  
**I want** confirmation before deleting coverage selections  
**So that** I don't accidentally remove needed coverage  

**Acceptance Criteria**:
- [ ] Confirmation dialog displays before any coverage deletion  
- [ ] Dialog message: "Are you sure you want to delete this coverage?"  
- [ ] "OK" confirms deletion and removes coverage from form  
- [ ] "Cancel" retains coverage selection  
- [ ] Coverage fields cleared and hidden when deletion confirmed  
- [ ] No accidental deletions possible  

**Source Evidence**: Coverage deletion confirmation in `vrWCP.js` line 39

---

## EPIC 4: CLASS CODE LOOKUP AND RISK ASSESSMENT

### Story 4.1: Access Class Code Lookup Modal
**As a** WCP quote user  
**I want** to search for appropriate class codes through a modal window  
**So that** I can select the correct classification for my business  

**Acceptance Criteria**:
- [ ] "Class Code Lookup" button triggers modal popup  
- [ ] Modal opens as standard popup window  
- [ ] Modal displays search interface  
- [ ] Modal includes risk grade information  
- [ ] Modal can be cancelled without changes  

**Source Evidence**: `ctlRiskGradeSearch.ascx` modal control

### Story 4.2: Search Class Codes with Multiple Options
**As a** WCP quote user  
**I want** flexible search options for class codes  
**So that** I can find the most appropriate classification quickly  

**Acceptance Criteria**:
- [ ] GL Class Code direct lookup available  
- [ ] Description search with "Contains" option  
- [ ] Description search with "Starts With" option  
- [ ] State-specific filtering (IN/IL) functional  
- [ ] Search results display relevant class codes  

**Source Evidence**: Search capabilities in `ctlRiskGradeSearch.ascx`

### Story 4.3: View Risk Grade Definitions
**As a** WCP quote user  
**I want** to see risk grade definitions in the class code modal  
**So that** I understand the underwriting implications of different class codes  

**Acceptance Criteria**:
- [ ] Risk grade table always visible in modal  
- [ ] Code 1: Generally Acceptable - Authority to quote and bind  
- [ ] Code 2: Conditionally Acceptable - Referral required  
- [ ] Code 3: Generally Unacceptable - Contact underwriter  
- [ ] Code P: Prohibited - No authority to quote/bind  
- [ ] Definitions clearly formatted and readable  

**Source Evidence**: Risk grade definition table in modal

### Story 4.4: Select and Transfer Class Code
**As a** WCP quote user  
**I want** to select a class code and return it to the main form  
**So that** I can complete my quote with the correct classification  

**Acceptance Criteria**:
- [ ] Submit button transfers selected class code to main form  
- [ ] Selected values passed through hidden form fields  
- [ ] Modal closes after successful selection  
- [ ] Main form updates with selected class code information  
- [ ] Data integrity maintained during transfer  

**Source Evidence**: Data transfer mechanism in `ctlRiskGradeSearch.ascx`

---

## EPIC 5: DYNAMIC FIELD CONTROL

### Story 5.1: Manage Location-Based Field States
**As a** WCP quote user with no owned locations  
**I want** irrelevant location fields to be disabled  
**So that** I don't waste time entering unnecessary information  

**Acceptance Criteria**:
- [ ] "No owned locations" checkbox available  
- [ ] Checking checkbox disables street number fields  
- [ ] Checking checkbox hides save button  
- [ ] Unchecking checkbox enables all location fields  
- [ ] Unchecking checkbox shows save button  
- [ ] Field states update immediately upon checkbox change  

**Source Evidence**: `NoOwnedLocationsCheckboxChanged` function in `vrWCP.js`

### Story 5.2: Exclude Disabled Fields from Validation
**As a** WCP quote user  
**I want** disabled fields to be excluded from required field validation  
**So that** I can submit forms without entering data in irrelevant fields  

**Acceptance Criteria**:
- [ ] Disabled street number fields not required for submission  
- [ ] Form validation skips disabled fields  
- [ ] Save button visibility matches field requirement status  
- [ ] User cannot interact with disabled fields  
- [ ] Clear visual indication of disabled state  

**Source Evidence**: Field management logic in location control functions

---

## CROSS-CUTTING USER STORIES

### Story C.1: Maintain Consistent Modal Behavior
**As a** WCP system user  
**I want** all modals to behave consistently  
**So that** I have a predictable user experience across the application  

**Acceptance Criteria**:
- [ ] All modals use jQuery UI Dialog framework  
- [ ] Modal styling consistent across all popup windows  
- [ ] Form integration works properly for all modals  
- [ ] State persistence maintained during modal interactions  
- [ ] Error handling consistent across all modal types  

**Source Evidence**: jQuery UI Dialog implementations across all modal patterns

### Story C.2: Preserve Data Integrity Across Modal Interactions
**As a** WCP quote user  
**I want** my form data to be preserved during modal interactions  
**So that** I don't lose progress when using popup windows  

**Acceptance Criteria**:
- [ ] Main form data preserved when modals open  
- [ ] Modal data integrated properly with main form submission  
- [ ] User selections maintained across modal interactions  
- [ ] No data loss during validation error recovery  
- [ ] Form state consistent after modal closure  

**Source Evidence**: Form integration patterns across modal implementations

### Story C.3: Provide Clear Visual Feedback for Validation
**As a** WCP system user  
**I want** clear visual indicators for validation errors  
**So that** I can quickly identify and correct form completion issues  

**Acceptance Criteria**:
- [ ] Red border styling for fields with validation errors  
- [ ] Red error text messages for specific validation failures  
- [ ] Red asterisk indicators for incomplete required fields  
- [ ] Real-time validation feedback updates immediately  
- [ ] Consistent error styling across all modals and forms  

**Source Evidence**: Validation error display patterns across all modal implementations

---

## DEVELOPMENT NOTES

### Technical Implementation Requirements
- **Framework**: jQuery UI Dialog for consistent modal behavior  
- **Integration**: All modals must integrate with ASP.NET Web Forms postback model  
- **State Management**: Modal content must persist during form interactions  
- **Validation**: Comprehensive client-side validation with server-side backup  

### Business Rule Implementation
- **Diamond Code 9107**: Critical business rule requiring careful implementation and testing  
- **Character Limits**: Enforce 125-character limit on additional information fields  
- **Required Field Logic**: Complex conditional requirements based on Yes/No selections  

### Quality Assurance Focus
- **Validation Testing**: Comprehensive testing of multi-layer validation chains  
- **Modal Integration**: Verify proper data flow between modals and main forms  
- **Error Recovery**: Test user ability to correct validation errors  
- **Business Rule Testing**: Verify Diamond Code 9107 ineligibility process works correctly  

---

**TRACEABILITY**: All user stories derived from stakeholder requirements extracted from Rex's comprehensive WCP modal pattern analysis  
**SOURCE EVIDENCE**: Complete file references and line numbers provided in requirements documentation  
**DEVELOPMENT READINESS**: HIGH - Stories ready for sprint planning and development estimation