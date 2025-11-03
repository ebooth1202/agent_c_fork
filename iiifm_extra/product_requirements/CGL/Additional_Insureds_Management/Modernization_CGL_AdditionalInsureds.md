# Modernization_CGL_AdditionalInsureds

**Line of Business**: Commercial General Liability (CGL)  
**Feature**: Additional Insureds Management System  
**Document Version**: 1.0  
**Date**: 2024-12-19  
**Status**: Draft

---

## 1. Executive Summary

The CGL Additional Insureds Management System implements a sophisticated 15-type additional insured selection framework with complex business rules, conditional field requirements, state-specific variations, and precise premium calculations. This critical component manages liability coverage extensions for third parties with contractual relationships to the insured, requiring detailed risk assessment and pricing for each additional insured type.

**Key Points:**
- **Business Purpose**: Enable systematic selection and management of additional insured endorsements with proper risk assessment and premium calculation
- **Current Implementation**: 15 distinct additional insured types with $0-$25 premium structure, conditional field requirements, 4-insured maximum limit, Illinois state-specific type
- **Modernization Scope**: Transform complex legacy control structure into modern component with enhanced validation, improved user experience, and maintainable business rule architecture
- **Expected Business Value**: Preserved sophisticated additional insured functionality with improved compliance, better user guidance, and reduced processing errors

The system represents one of the most complex CGL components, combining endorsement management, premium calculation, state-specific variations, and conditional field validation in a single comprehensive interface requiring specialized insurance domain expertise.

---

## 2. Business Overview

The CGL Additional Insureds Management System serves as a critical component for extending liability coverage to third parties who have contractual relationships with the named insured. This sophisticated feature manages 15 distinct additional insured types, each with specific business rules, premium implications, and field requirements designed to ensure proper coverage extension while maintaining underwriting control.

### 2.1 Feature Purpose

Additional insured endorsements exist to satisfy contractual requirements where third parties (contractors, landlords, lenders, vendors) require liability coverage under the named insured's policy for their legal exposure arising from the named insured's operations. The system ensures proper coverage extension through:

- **Risk-Based Premium Structure**: $0 for low-risk "checkbox" types, $25 for standard coverage extensions
- **Mandatory Field Validation**: Conditional requirements ensure adequate coverage specification for each additional insured type
- **Business Logic Enforcement**: 4-insured maximum limit prevents excessive exposure concentration
- **State-Specific Compliance**: Illinois-specific additional insured types address state regulatory requirements

The dual-tier pricing structure ($0 vs $25) reflects actuarial risk assessment where certain additional insured types represent minimal additional exposure (co-owners, controlling interests) while others require substantial coverage extension evaluation.

### 2.2 User Roles and Personas

**Primary Users:**
- **Insurance Agents**: Select appropriate additional insured types based on client contractual obligations, must understand coverage implications and premium impacts
- **Commercial Insurance Brokers**: Manage complex additional insured requirements for large commercial accounts with multiple contractual relationships
- **Underwriters**: Review additional insured selections for coverage adequacy and exposure concentration risk

**Secondary Users:**
- **Agency Staff**: Assist with additional insured data entry and validation, require understanding of conditional field requirements
- **Compliance Officers**: Monitor additional insured selections for regulatory compliance, particularly state-specific requirements
- **Policy Services Representatives**: Handle endorsement changes and additional insured modifications during policy term

### 2.3 Business Process Context

The Additional Insureds Management System appears during the CGL coverage selection workflow, typically after basic coverage limits are established but before premium calculation and quote finalization. This positioning ensures additional insured exposure is factored into overall policy pricing and coverage design.

**Workflow Position:**
1. Coverage Selection and Limits Configuration
2. **→ Additional Insureds Management System** (this feature)
3. Other Policy-Level Coverages (EPLI, Cyber, etc.)
4. Premium Calculation and Quote Generation
5. Policy Binding and Endorsement Processing

The maximum 4 additional insured limit ensures exposure concentration remains within acceptable underwriting parameters while allowing sufficient coverage for typical commercial relationships.

### 2.4 Regulatory Context

Additional insured endorsements must comply with state insurance regulations governing coverage extensions and liability assignments. Illinois-specific additional insured types (City of Chicago - Scaffolding) address state regulatory requirements for specialized construction operations. The conditional field requirements ensure adequate coverage specification meets regulatory documentation standards for liability coverage extensions.

Premium calculations must reflect actuarial risk assessment approved by state regulatory authorities, supporting the $0 vs $25 tiered structure based on exposure analysis and claim experience data.

---

## 3. Detailed Feature Specifications

### 3.1 Additional Insured Types and Business Rules

**Source**: `ctl_App_AdditionalInsureds_CGL.ascx` (500+ lines of complex business logic)

**Type 1: City of Chicago - Scaffolding (Code 80537)**
- **Classification**: Illinois-specific regulatory requirement
- **Premium**: $25 (standard premium type)
- **Availability**: Illinois quotes only (state-specific display logic)
- **Required Fields**: Name, Location/Premises description
- **Business Rule**: Mandatory for scaffolding operations in Chicago jurisdiction
- **Risk Assessment**: High-risk construction operation requiring specialized coverage
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, Illinois state conditional logic

**Type 2: Co-Owner of Insured Premises (Code 21018)**
- **Classification**: $0 premium "checkbox" type
- **Premium**: $0 (minimal risk exposure)
- **Required Fields**: Name, Location/Premises description
- **Business Rule**: Low additional exposure due to shared ownership interest
- **Risk Assessment**: Existing ownership interest provides natural risk alignment
- **Coverage Scope**: Premises liability for co-ownership situations
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, checkbox AI type logic

**Type 3: Controlling Interests (Code 926)**
- **Classification**: $0 premium "checkbox" type
- **Premium**: $0 (minimal risk exposure)
- **Required Fields**: Name only (no premises/location required)
- **Business Rule**: Parent/subsidiary relationship provides risk control alignment
- **Risk Assessment**: Control relationship reduces moral hazard concerns
- **Coverage Scope**: General liability coverage for controlling entity operations
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, name-only requirement logic

**Type 4: Designated Person Or Organization (Code 21022)**
- **Classification**: Standard premium type
- **Premium**: $25 (full risk assessment required)
- **Required Fields**: Name only
- **Business Rule**: Broad additional insured coverage requiring premium charge
- **Risk Assessment**: Unspecified relationship requires full premium evaluation
- **Coverage Scope**: Comprehensive additional insured protection
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, standard premium logic

**Type 5: Engineers, Architects or Surveyors (Code 21019)**
- **Classification**: $0 premium "checkbox" type
- **Premium**: $0 (professional service relationship)
- **Required Fields**: No additional inputs required (type selection sufficient)
- **Business Rule**: Professional service provider relationship has limited additional exposure
- **Risk Assessment**: Professional services typically covered under separate E&O policies
- **Coverage Scope**: Limited to work performed for named insured
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, no-input checkbox type

**Type 6: Engineers, Architects or Surveyors Not Engaged by Named Insured (Code 21023)**
- **Classification**: Standard premium type
- **Premium**: $25 (uncontrolled relationship premium required)
- **Required Fields**: Name (identification of specific entity)
- **Business Rule**: Third-party professional relationship requires premium assessment
- **Risk Assessment**: No direct contractual control increases exposure risk
- **Coverage Scope**: Professional services performed for third parties
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, third-party professional logic

**Type 7: Lessor of Leased Equipment (Code 21020)**
- **Classification**: Standard premium type
- **Premium**: $25 (equipment liability exposure)
- **Required Fields**: Name (lessor identification)
- **Business Rule**: Equipment leasing creates products liability exposure requiring premium
- **Risk Assessment**: Equipment failure/malfunction liability transferred to policy
- **Coverage Scope**: Equipment-related liability for leased items
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, equipment lessor logic

**Type 8: Managers or Lessors of Premises (Code 21053)**
- **Classification**: Standard premium type
- **Premium**: $25 (premises liability exposure)
- **Required Fields**: Name, Premises description
- **Business Rule**: Premises management relationship creates liability exposure requiring premium
- **Risk Assessment**: Premises control creates additional liability exposure
- **Coverage Scope**: Premises-related liability for managed/leased property
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, premises management logic

**Type 9: Mortgagee, Assignee or Receiver (Code 21054)**
- **Classification**: $0 premium "checkbox" type
- **Premium**: $0 (financial interest protection)
- **Required Fields**: Name, Premises description
- **Business Rule**: Financial interest holder has limited operational exposure
- **Risk Assessment**: Collateral protection interest reduces additional exposure
- **Coverage Scope**: Property interest protection for financial stakeholders
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, financial interest logic

**Type 10: Owner or Other Interests From Whom Land has been Leased (Code 21055)**
- **Classification**: $0 premium "checkbox" type
- **Premium**: $0 (land owner interest)
- **Required Fields**: Name, Premises description
- **Business Rule**: Land ownership interest provides natural coverage alignment
- **Risk Assessment**: Land owner has inherent interest in property protection
- **Coverage Scope**: Land-related liability for property owners
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, land owner logic

**Type 11: Owners, Lessees or Contractors (Code 21024)**
- **Classification**: Standard premium type
- **Premium**: $25 (construction/contracting exposure)
- **Required Fields**: Name, Premises (auto-populated text)
- **Business Rule**: Construction relationships require full premium assessment
- **Risk Assessment**: Construction operations create significant additional exposure
- **Coverage Scope**: Construction-related liability coverage
- **Auto-Population Logic**: Premises text automatically filled for construction type
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, construction auto-fill logic

**Type 12: State or Political Subdivision - Permits Relating to Premises (Code 21016)**
- **Classification**: Standard premium type
- **Premium**: $25 (governmental entity coverage)
- **Required Fields**: Standard governmental entity requirements
- **Business Rule**: Government permit requirements necessitate coverage extension
- **Risk Assessment**: Governmental liability exposure requires premium charge
- **Coverage Scope**: Premises-related permits and governmental oversight
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, governmental permit logic

**Type 13: State or Political Subdivisions - Permits (Code 21026)**
- **Classification**: Standard premium type
- **Premium**: $25 (general governmental permits)
- **Required Fields**: Standard permit requirements
- **Business Rule**: General permit relationships require coverage extension
- **Risk Assessment**: Permit authority liability requires premium assessment
- **Coverage Scope**: General permit and licensing liability
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, general permit logic

**Type 14: Townhouse Associations (Code 21017)**
- **Classification**: Standard premium type
- **Premium**: $25 (HOA/association coverage)
- **Required Fields**: No additional inputs required
- **Business Rule**: Association liability relationships require premium charge
- **Risk Assessment**: Association management creates governance liability exposure
- **Coverage Scope**: Townhouse/HOA management liability
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, association logic

**Type 15: Vendors (Code 21021)**
- **Classification**: Standard premium type
- **Premium**: $25 (vendor relationship coverage)
- **Required Fields**: Name, Products description
- **Business Rule**: Vendor relationships create products liability exposure
- **Risk Assessment**: Product distribution creates liability transfer requirement
- **Coverage Scope**: Vendor/distributor products liability
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, vendor products logic

### 3.2 Business Logic and Validation Rules

**Maximum Additional Insured Limit: 4**
- **Enforcement**: JavaScript validation prevents selection of more than 4 additional insureds
- **Business Rationale**: Exposure concentration control to maintain underwriting parameters
- **Error Handling**: User notification when attempting to exceed 4-insured limit
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, JavaScript limit validation

**Premium Classification Logic:**
- **$0 Premium Types (5 types)**: 21018, 926, 21019, 21054, 21055 - "Checkbox AI" types
- **$25 Premium Types (10 types)**: All remaining types require standard premium
- **Premium Calculation**: Total Additional Insured premium = (Count of $25 types) × $25
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, premium calculation logic

**Conditional Field Requirements:**
- **Name Field**: Required for types requiring entity identification
- **Premises Field**: Required for location-specific coverage types
- **Products Field**: Required for vendor types involving product distribution
- **Auto-Population**: Type 21024 (Owners, Lessees, Contractors) auto-fills premises text
- **Validation**: JavaScript validation ensures required fields completed before submission
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, conditional field validation

**State-Specific Business Rules:**
- **Illinois Only**: Type 80537 (City of Chicago - Scaffolding) displays only for Illinois quotes
- **State Detection**: System checks policy state to determine available additional insured types
- **Regulatory Compliance**: Illinois-specific types address state regulatory requirements
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, state conditional display logic

---

## 4. UI/UX Requirements ⭐ MANDATORY

### 4.1 Auto-Display/Hide Behaviors

**Pattern Description:**
The Additional Insureds interface displays as an integrated section within the CGL coverage selection workflow. The interface dynamically shows/hides conditional input fields based on selected additional insured types while maintaining a clean, organized presentation of the 15 available types.

**Selection Interface Behavior:**
```
Display Pattern: Checkboxes for all 15 additional insured types in organized list
State-Specific Display: Illinois quotes show all 15 types, other states show 14 types
Conditional Fields: Input fields appear below selected types when required
Maximum Limit: JavaScript prevents selection beyond 4 additional insureds
Source: ctl_App_AdditionalInsureds_CGL.ascx, type selection interface
```

**Conditional Field Display Logic:**
```
Name Field Display: When types requiring name identification are selected
Premises Field Display: When location-specific types are selected
Products Field Display: When vendor types (21021) are selected
Auto-Fill Behavior: Type 21024 automatically populates premises text
Default State: No additional insureds selected, no conditional fields visible
Source: ctl_App_AdditionalInsureds_CGL.ascx, conditional field logic
```

### 4.2 Text Input Specifications

**Field Specifications:**

| Field Name | Label | Type | Character Limit | Required | Default |
|------------|-------|------|-----------------|----------|---------|
| AI Type Selection | [Type Description] | Checkbox | N/A | Conditional | None Selected |
| Name Field | "Name" | Single-line text | 255 chars (estimated) | When Required | Empty |
| Premises Field | "Premises/Location" | Multi-line text | 500 chars (estimated) | When Required | Empty/Auto-fill |
| Products Field | "Products" | Multi-line text | 300 chars (estimated) | When Required | Empty |

**Conditional Field Requirements:**

| Additional Insured Type | Name Required | Premises Required | Products Required | Auto-Fill |
|-------------------------|---------------|-------------------|-------------------|-----------|
| City of Chicago - Scaffolding (80537) | Yes | Yes | No | No |
| Co-Owner of Insured Premises (21018) | Yes | Yes | No | No |
| Controlling Interests (926) | Yes | No | No | No |
| Designated Person Or Organization (21022) | Yes | No | No | No |
| Engineers, Architects or Surveyors (21019) | No | No | No | No |
| Engineers, Architects... Not Engaged (21023) | Yes | No | No | No |
| Lessor of Leased Equipment (21020) | Yes | No | No | No |
| Managers or Lessors of Premises (21053) | Yes | Yes | No | No |
| Mortgagee, Assignee or Receiver (21054) | Yes | Yes | No | No |
| Owner... From Whom Land Leased (21055) | Yes | Yes | No | No |
| Owners, Lessees or Contractors (21024) | Yes | Yes | No | **Auto-fills premises** |
| State/Political - Permits/Premises (21016) | Standard | Standard | No | No |
| State/Political - Permits (21026) | Standard | Standard | No | No |
| Townhouse Associations (21017) | No | No | No | No |
| Vendors (21021) | Yes | No | **Yes** | No |

### 4.3 Validation Visual Indicators

**Error States:**

**Maximum Limit Exceeded:**
- **Visual**: Warning message display above additional insured selection area
- **Error Message**: "Maximum 4 additional insureds allowed. Please deselect items to continue."
- **Behavior**: Prevents additional checkbox selection, existing selections remain valid
- **Trigger**: User attempts to select 5th additional insured
- **Validation Function**: JavaScript limit checking on checkbox selection events

**Missing Required Fields:**
- **Visual**: Red border around empty required input fields
- **Error Message**: "Name required for selected additional insured type" / "Premises required for selected additional insured type"
- **Icon**: Red asterisk (*) next to required field labels
- **Trigger**: Form submission attempted with incomplete required fields
- **Validation Function**: Server-side and client-side field requirement validation

**Premium Calculation Display:**
- **Visual**: Real-time premium calculation display showing "$0" and "$25" type totals
- **Format**: "Additional Insureds Premium: $[total] ([count] × $25 + [count] × $0)"
- **Update**: Automatically recalculates as types are selected/deselected
- **Trigger**: Any checkbox selection change
- **Calculation Function**: JavaScript premium calculation on selection events

### 4.4 Interactive Elements

**Type Selection Checkboxes:**
- **Labels**: Full additional insured type descriptions with premium indicators
- **Premium Display**: "($0)" or "($25)" shown next to each type description
- **Grouping**: Organized by premium type ($0 types grouped, $25 types grouped)
- **Selection Logic**: Independent checkbox selection (not mutually exclusive)
- **Maximum Enforcement**: JavaScript prevents >4 selections

**Conditional Input Fields:**
- **Name Fields**: Single-line text input, required validation when applicable
- **Premises Fields**: Multi-line textarea, auto-expanding height for longer descriptions
- **Products Fields**: Multi-line textarea for product/service descriptions
- **Auto-Fill Behavior**: Type 21024 automatically populates standard construction premises text

**Premium Calculator Display:**
- **Real-time Updates**: Recalculates total as selections change
- **Breakdown Display**: Shows count of each premium type and calculation logic
- **Integration**: Feeds into overall policy premium calculation
- **Visual Format**: Bold text for total premium amount

### 4.5 Accessibility Requirements

- **ARIA Labels**: Each additional insured type checkbox properly labeled for screen readers
- **Keyboard Navigation**: Standard tab order through checkboxes and conditional input fields
- **Focus Indicators**: Clear visual focus highlighting on interactive elements
- **Screen Reader Text**: Premium amounts and conditional field requirements announced
- **Color Contrast**: Red error indicators meet WCAG 2.1 AA compliance (4.5:1 minimum)
- **Conditional Field Announcements**: Screen readers notify when conditional fields appear/disappear

### 4.6 Responsive Design Requirements

- **Mobile Devices**: Stacked layout for additional insured types with touch-friendly checkboxes
- **Tablets**: Two-column layout for efficient space utilization while maintaining readability
- **Desktop**: Full multi-column layout showing all 15 types with optimal organization
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge, IE11 (VelociRater supported browsers)
- **Conditional Fields**: Responsive sizing for input fields across all device types

---

## 5. Validation Rules and Business Logic ⭐ MANDATORY

### 5.1 Client-Side Validation (JavaScript)

**Function: ValidateMaximumAdditionalInsuredLimit()**
- **Purpose**: Enforces 4 additional insured maximum limit across all type selections
- **Trigger**: Checkbox selection events for all 15 additional insured types
- **Logic**: Counts selected checkboxes, prevents selection if count would exceed 4
- **Error Message**: "Maximum 4 additional insureds allowed. Please deselect items to continue."
- **Visual Feedback**: Warning message display, checkbox selection prevention
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, JavaScript maximum limit validation

**Function: ValidateConditionalFieldRequirements()**
- **Purpose**: Ensures required name/premises/products fields completed for selected types
- **Trigger**: Form submission events and real-time field validation
- **Logic**: Iterates through selected additional insured types, validates corresponding required fields
- **Error Messages**: Type-specific error messages for missing required fields
- **Visual Feedback**: Red borders on empty required fields, asterisk indicators
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, conditional field validation logic

**Function: CalculateAdditionalInsuredPremium()**
- **Purpose**: Real-time calculation and display of additional insured premium totals
- **Trigger**: Checkbox selection/deselection events
- **Logic**: Counts $25 premium types, multiplies by $25, adds $0 types (no charge)
- **Display Format**: "Additional Insureds Premium: $[total] ([count] × $25 + [count] × $0)"
- **Update Frequency**: Immediate recalculation on any selection change
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, premium calculation JavaScript

### 5.2 Conditional Field Validation

**Name Field Requirements:**

| Additional Insured Type | Name Required | Validation Logic | Error Message |
|-------------------------|---------------|------------------|---------------|
| City of Chicago - Scaffolding (80537) | Yes | Not empty, min 2 characters | "Name required for City of Chicago - Scaffolding additional insured" |
| Co-Owner of Insured Premises (21018) | Yes | Not empty, min 2 characters | "Name required for Co-Owner additional insured" |
| Controlling Interests (926) | Yes | Not empty, min 2 characters | "Name required for Controlling Interests additional insured" |
| Designated Person Or Organization (21022) | Yes | Not empty, min 2 characters | "Name required for Designated Person/Organization additional insured" |
| Engineers... Not Engaged (21023) | Yes | Not empty, min 2 characters | "Name required for Engineers/Architects additional insured" |
| Lessor of Leased Equipment (21020) | Yes | Not empty, min 2 characters | "Name required for Equipment Lessor additional insured" |
| Managers or Lessors of Premises (21053) | Yes | Not empty, min 2 characters | "Name required for Premises Manager/Lessor additional insured" |
| Mortgagee, Assignee or Receiver (21054) | Yes | Not empty, min 2 characters | "Name required for Mortgagee/Assignee additional insured" |
| Owner... From Whom Land Leased (21055) | Yes | Not empty, min 2 characters | "Name required for Land Owner additional insured" |
| Owners, Lessees or Contractors (21024) | Yes | Not empty, min 2 characters | "Name required for Owners/Contractors additional insured" |
| Vendors (21021) | Yes | Not empty, min 2 characters | "Name required for Vendors additional insured" |

**Premises Field Requirements:**

| Additional Insured Type | Premises Required | Validation Logic | Error Message |
|-------------------------|-------------------|------------------|---------------|
| City of Chicago - Scaffolding (80537) | Yes | Not empty, min 5 characters | "Premises description required for scaffolding operations" |
| Co-Owner of Insured Premises (21018) | Yes | Not empty, min 5 characters | "Premises description required for co-owner coverage" |
| Managers or Lessors of Premises (21053) | Yes | Not empty, min 5 characters | "Premises description required for manager/lessor coverage" |
| Mortgagee, Assignee or Receiver (21054) | Yes | Not empty, min 5 characters | "Premises description required for mortgagee coverage" |
| Owner... From Whom Land Leased (21055) | Yes | Not empty, min 5 characters | "Premises description required for land owner coverage" |
| Owners, Lessees or Contractors (21024) | Yes | Auto-populated + validation | "Premises information auto-filled for construction coverage" |

### 5.3 Business Rule Validation

**Rule 1: Maximum 4 Additional Insureds Limit**
- **Description**: Policy cannot have more than 4 additional insureds to control exposure concentration
- **Validation Logic**: JavaScript counts selected checkboxes across all 15 types, blocks selection at 4
- **Error Handling**: Warning message display, prevents additional checkbox selection
- **Business Rationale**: Underwriting exposure concentration limits require maximum 4 additional insured extensions
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, JavaScript limit validation

**Rule 2: State-Specific Additional Insured Availability**
- **Description**: Illinois quotes include City of Chicago - Scaffolding type, other states exclude this type
- **Validation Logic**: Server-side state detection controls display of Illinois-specific additional insured type
- **Error Handling**: Type simply not displayed for non-Illinois quotes (no error state)
- **Business Rationale**: State regulatory requirements determine available additional insured endorsements
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, state conditional display logic

**Rule 3: Premium Calculation Accuracy**
- **Description**: Additional insured premium must accurately reflect $0 vs $25 type selections
- **Validation Logic**: JavaScript counts premium types separately, calculates ($25 types × $25) + ($0 types × $0)
- **Error Handling**: Real-time premium display with calculation breakdown for transparency
- **Business Rationale**: Actuarial pricing requires accurate premium calculation based on risk assessment
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, premium calculation logic

**Rule 4: Conditional Field Completion**
- **Description**: Selected additional insured types requiring name/premises/products fields must have completed information
- **Validation Logic**: Client-side and server-side validation checks required fields for each selected type
- **Error Handling**: Red borders, specific error messages, form submission prevention
- **Business Rationale**: Coverage specification requires adequate identification and scope definition for each additional insured
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, conditional field validation

### 5.4 Server-Side Validation

**Security Validations:**
- **Input Sanitization**: All name, premises, products text fields sanitized to prevent injection attacks
- **SQL Injection Prevention**: Parameterized queries for additional insured data storage
- **Cross-Site Scripting (XSS) Prevention**: User input encoded before display or database storage
- **Maximum Length Enforcement**: Server-side validation of field length limits for database compatibility

**Data Integrity Checks:**
- **Type Code Validation**: Ensures only valid additional insured codes (80537, 21016-21026) are processed
- **Premium Calculation Verification**: Server-side recalculation confirms client-side premium calculation accuracy
- **State Consistency**: Validates Illinois-specific types only selected for Illinois quotes
- **Limit Enforcement**: Server-side confirmation that maximum 4 additional insureds rule is maintained

---

## 6. User Stories and Acceptance Criteria

### US-CGL-AI-001: View Available Additional Insured Types

**As an** Insurance Agent  
**I need to** view all available additional insured types for CGL coverage  
**So that** I can select appropriate coverage extensions for my client's contractual requirements

**Acceptance Criteria:**
1. Given I am in the CGL coverage selection section, when I view additional insured options, then I see all available types organized by premium structure
2. Given I am creating an Illinois quote, when I view additional insured types, then I see all 15 types including "City of Chicago - Scaffolding"
3. Given I am creating a non-Illinois quote, when I view additional insured types, then I see 14 types excluding the Illinois-specific type
4. Given each additional insured type is displayed, when I read the descriptions, then I see premium indicators ($0 or $25) next to each type
5. Given the interface loads, when displayed, then premium types are organized with $0 types grouped separately from $25 types

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: None (base functionality)

### US-CGL-AI-002: Select Additional Insured Types with Limit Enforcement

**As an** Insurance Agent  
**I need to** select multiple additional insured types while respecting the 4-insured maximum  
**So that** I can configure appropriate coverage while maintaining underwriting parameters

**Acceptance Criteria:**
1. Given additional insured types are displayed, when I select any combination of types, then my selections are recorded and visually confirmed
2. Given I have selected 0-3 additional insureds, when I attempt to select another, then the selection is allowed and recorded
3. Given I have selected 4 additional insureds, when I attempt to select a 5th type, then the selection is blocked and I receive a warning message
4. Given I have reached the 4-insured limit, when I deselect one type, then I can select a different type to replace it
5. Given my selections exceed the limit, when the warning appears, then I see "Maximum 4 additional insureds allowed. Please deselect items to continue."

**Priority**: High  
**Complexity**: Large  
**Dependencies**: US-CGL-AI-001 (requires type display)

### US-CGL-AI-003: Complete Required Fields for Selected Types

**As an** Insurance Agent  
**I need to** provide required information for selected additional insured types  
**So that** coverage specifications are adequate and complete for policy issuance

**Acceptance Criteria:**
1. Given I select a type requiring a name field, when the selection is made, then a name input field appears below the type
2. Given I select a type requiring premises information, when the selection is made, then a premises textarea appears below the type
3. Given I select "Vendors" type, when the selection is made, then both name and products fields appear
4. Given I select "Owners, Lessees or Contractors", when the selection is made, then the premises field auto-populates with construction text
5. Given I deselect a type with conditional fields, when the deselection occurs, then the corresponding fields disappear

**Priority**: High  
**Complexity**: Large  
**Dependencies**: US-CGL-AI-002 (requires type selection functionality)

### US-CGL-AI-004: Calculate Real-time Premium for Selections

**As an** Insurance Agent  
**I need to** see real-time premium calculations for selected additional insureds  
**So that** I can communicate accurate pricing to my client during quote preparation

**Acceptance Criteria:**
1. Given I have no additional insureds selected, when viewing the premium display, then I see "Additional Insureds Premium: $0"
2. Given I select only $0 premium types, when selections are made, then premium remains $0 with breakdown showing count of $0 types
3. Given I select one $25 premium type, when the selection is made, then premium displays "$25 (1 × $25 + 0 × $0)"
4. Given I select a mix of $0 and $25 types, when selections are made, then premium accurately reflects "(count × $25) + (count × $0)"
5. Given I change my selections, when any checkbox is selected/deselected, then premium recalculates immediately

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: US-CGL-AI-002 (requires selection functionality)

### US-CGL-AI-005: Validate Required Field Completion

**As an** Insurance Agent  
**I need to** receive validation feedback for incomplete required fields  
**So that** I can ensure all necessary information is provided before quote submission

**Acceptance Criteria:**
1. Given I select a type requiring a name field, when I leave the name field empty and attempt to continue, then I receive a field-specific error message
2. Given I select a type requiring premises information, when I leave premises empty and attempt to continue, then I receive a premises-specific error message
3. Given incomplete required fields exist, when validation occurs, then empty fields display red borders and asterisk indicators
4. Given I complete all required fields, when validation occurs, then error indicators disappear and submission is allowed
5. Given validation errors exist, when I attempt form submission, then submission is blocked until all required fields are completed

**Priority**: High  
**Complexity**: Large  
**Dependencies**: US-CGL-AI-003 (requires conditional field functionality)

### US-CGL-AI-006: Process City of Chicago Scaffolding Requirements

**As an** Insurance Agent in Illinois  
**I need to** select City of Chicago - Scaffolding additional insured coverage  
**So that** I can meet regulatory requirements for Chicago construction operations

**Acceptance Criteria:**
1. Given I am creating an Illinois CGL quote, when I view additional insured options, then I see "City of Chicago - Scaffolding ($25)" as an available option
2. Given I am creating a quote in any other state, when I view additional insured options, then the City of Chicago type is not displayed
3. Given I select City of Chicago - Scaffolding type, when the selection is made, then name and premises fields appear as required inputs
4. Given I complete the required fields for scaffolding coverage, when I submit, then the coverage is added with $25 premium charge
5. Given scaffolding coverage is selected, when premium is calculated, then it contributes to the $25 premium type total

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: US-CGL-AI-003, state-specific logic implementation

### US-CGL-AI-007: Manage Co-Owner and Controlling Interest Types

**As an** Insurance Agent  
**I need to** select $0 premium additional insured types for ownership relationships  
**So that** I can provide coverage for entities with ownership/control interests without premium impact

**Acceptance Criteria:**
1. Given I view additional insured options, when I see ownership types, then "Co-Owner of Insured Premises ($0)" and "Controlling Interests ($0)" are clearly marked as no-charge options
2. Given I select "Co-Owner of Insured Premises", when the selection is made, then name and premises fields appear as required inputs
3. Given I select "Controlling Interests", when the selection is made, then only the name field appears (no premises required)
4. Given I complete ownership type selections, when premium is calculated, then these types contribute $0 to the total premium
5. Given ownership types are selected with other types, when premium displays, then breakdown shows correct count of $0 types

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: US-CGL-AI-003, premium calculation functionality

### US-CGL-AI-008: Handle Professional Services Types

**As an** Insurance Agent  
**I need to** select appropriate additional insured coverage for professional service providers  
**So that** I can address liability coverage for architects, engineers, and surveyors

**Acceptance Criteria:**
1. Given I view professional service options, when displayed, then I see "Engineers, Architects or Surveyors ($0)" and "Engineers... Not Engaged by Named Insured ($25)"
2. Given I select the $0 professional type, when the selection is made, then no additional fields are required (checkbox only)
3. Given I select the $25 professional type, when the selection is made, then a name field appears for entity identification
4. Given I select both professional types, when premium is calculated, then only the $25 type contributes to premium total
5. Given professional types are selected, when validation occurs, then appropriate field requirements are enforced

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: US-CGL-AI-003, differential field requirements

### US-CGL-AI-009: Process Vendor Product Liability Coverage

**As an** Insurance Agent  
**I need to** configure vendor additional insured coverage with product specifications  
**So that** I can provide products liability coverage for vendor/distributor relationships

**Acceptance Criteria:**
1. Given I view additional insured options, when I see "Vendors ($25)", then the premium charge is clearly indicated
2. Given I select "Vendors" type, when the selection is made, then both name and products fields appear as required inputs
3. Given I complete vendor name and products information, when I submit, then the coverage is configured with products liability scope
4. Given vendor coverage is selected, when premium is calculated, then the $25 charge is included in the total
5. Given vendor products field is empty, when I attempt to continue, then validation prevents submission and shows products-specific error

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: US-CGL-AI-003, products liability integration

### US-CGL-AI-010: Complete Additional Insured Configuration Workflow

**As an** Insurance Agent  
**I need to** complete all additional insured selections and validations successfully  
**So that** I can proceed to other coverage sections with properly configured additional insured endorsements

**Acceptance Criteria:**
1. Given I have selected 1-4 additional insured types, when all required fields are completed, then validation passes and I can proceed
2. Given my selections include both $0 and $25 premium types, when configuration is complete, then accurate premium calculation is recorded
3. Given all validations pass, when I proceed from additional insureds section, then my configuration is saved to the quote object
4. Given additional insured configuration is complete, when I continue the quote workflow, then selected types and premiums integrate with overall policy calculation
5. Given the workflow completes successfully, when I review the quote, then additional insured selections and premiums are accurately reflected

**Priority**: High  
**Complexity**: Large  
**Dependencies**: All previous user stories (requires complete additional insured functionality)

---

## 7. Testing Requirements

### 7.1 Functional Testing

**Test Scenario 1: Additional Insured Type Display and Selection**
- **Setup**: Navigate to CGL coverage section, access additional insureds interface
- **Steps**:
  1. Verify all 15 additional insured types display for Illinois quotes
  2. Verify 14 types display for non-Illinois quotes (excluding City of Chicago)
  3. Confirm premium indicators ($0 or $25) appear next to each type
  4. Test checkbox selection functionality for all types
  5. Verify visual confirmation of selections
- **Expected Result**: Correct type display based on state, proper selection functionality, accurate premium indicators

**Test Scenario 2: Maximum 4 Additional Insured Limit Enforcement**
- **Setup**: Additional insureds interface loaded with all types available
- **Steps**:
  1. Select 4 different additional insured types
  2. Attempt to select a 5th type
  3. Verify warning message appears and 5th selection is blocked
  4. Deselect one of the 4 types
  5. Confirm 5th type can now be selected
- **Expected Result**: Maximum limit properly enforced, appropriate warning message, selection becomes available after deselection

**Test Scenario 3: Conditional Field Display and Validation**
- **Setup**: Additional insureds interface with various type selections
- **Steps**:
  1. Select types requiring only name fields, verify name field appears
  2. Select types requiring premises fields, verify premises field appears
  3. Select vendors type, verify both name and products fields appear
  4. Select "Owners, Lessees or Contractors", verify premises auto-populates
  5. Deselect types, verify corresponding fields disappear
- **Expected Result**: Correct conditional fields appear/disappear based on type requirements

**Test Scenario 4: Premium Calculation Accuracy**
- **Setup**: Additional insureds interface ready for selection testing
- **Steps**:
  1. Select only $0 premium types, verify total shows $0
  2. Select one $25 premium type, verify total shows $25 with breakdown
  3. Select mix of $0 and $25 types, verify accurate calculation
  4. Change selections, verify real-time premium updates
  5. Confirm premium integrates properly with overall policy calculation
- **Expected Result**: Accurate premium calculation in real-time with proper breakdown display

### 7.2 UI Behavior Testing

**Conditional Field Testing:**
- Verify all 15 types show/hide appropriate conditional fields correctly
- Test auto-population for "Owners, Lessees or Contractors" premises field
- Validate field disappearance when types are deselected
- Confirm proper field labeling and requirement indicators

**Validation Testing:**
- Test required field validation for each type requiring conditional inputs
- Verify error message specificity for different field requirements
- Test visual indicators (red borders, asterisks) for validation errors
- Confirm validation error clearing when fields are completed

### 7.3 Cross-Browser Testing

Test comprehensive functionality on:
- **Chrome (latest version)**: Primary VelociRater browser
- **Firefox (latest version)**: Secondary browser support
- **Safari (latest version)**: Mac platform compatibility
- **Edge (latest version)**: Windows platform default
- **IE11**: Legacy support if required by VelociRater compatibility

### 7.4 State-Specific Testing

**Illinois Quote Testing:**
- Verify City of Chicago - Scaffolding type appears in Illinois quotes
- Test scaffolding type selection and required field functionality
- Confirm premium calculation includes scaffolding premium

**Non-Illinois Quote Testing:**
- Verify City of Chicago - Scaffolding type does not appear in other state quotes
- Test all other 14 types function properly in non-Illinois quotes
- Confirm premium calculations work correctly without Illinois-specific type

### 7.5 Performance Testing

- **Type Display Performance**: Verify all 15 types load and display within 2 seconds
- **Conditional Field Performance**: Test field show/hide responsiveness (<0.5 seconds)
- **Premium Calculation Performance**: Verify real-time calculation updates immediately
- **Maximum Limit Validation**: Test limit enforcement responds instantly to selection attempts
- **Form Submission Performance**: Ensure validation and submission complete within 3 seconds

---

## 8. Migration and Modernization Considerations

### 8.1 Data Migration

**Current Data Structure**: Complex additional insured configuration stored in VelociRater quote object with type codes, names, premises, products fields
**Migration Requirements**: Preserve all 15 additional insured type definitions with exact type codes, premium structures, field requirements
**Data Integrity**: Maintain relationship between additional insured selections and overall policy premium calculation
**Field Mapping**: Migrate conditional field requirements and auto-population logic for construction type

### 8.2 Configuration Migration

**Type Definitions**: Migrate exact additional insured type descriptions and codes from current system
**Premium Structure**: Preserve $0 vs $25 tiered premium classification system
**Business Rules**: Port maximum 4 additional insured limit and state-specific availability rules
**Conditional Logic**: Migrate complex conditional field requirements for each of the 15 types
**Validation Rules**: Preserve client-side and server-side validation logic for field requirements

### 8.3 Integration Impact

**Policy Premium Calculation**: Ensure additional insured premium integration with overall policy rating remains intact
**Quote Object Integration**: Maintain additional insured data storage and retrieval within quote management system  
**State Logic Integration**: Preserve state-specific type availability within state determination logic
**Underwriting Integration**: Maintain additional insured information flow to underwriting review processes

### 8.4 Rollback Strategy

**Data Preservation**: Maintain backup of current ctl_App_AdditionalInsureds_CGL.ascx functionality
**Business Continuity**: Ensure all 15 additional insured types remain available throughout migration
**Premium Calculation Backup**: Preserve existing premium calculation logic as fallback
**Validation Preservation**: Maintain current validation rules and error handling as rollback option

---

## 9. Source Attribution and Traceability

### 9.1 Source Code Files Analyzed

| File Path | Purpose | Lines Analyzed |
|-----------|---------|----------------|
| ctl_App_AdditionalInsureds_CGL.ascx | Additional insured UI and business logic | 500+ lines (entire control) |
| [Related premium calculation files] | Premium calculation integration | [To be determined] |
| [State logic determination files] | Illinois-specific type availability | [To be determined] |
| [Validation helper files] | Field requirement validation | [To be determined] |

### 9.2 Key Additional Insured Type Codes

| Type Code | Description | Premium | Required Fields |
|-----------|-------------|---------|-----------------|
| 80537 | City of Chicago - Scaffolding | $25 | Name, Premises |
| 21018 | Co-Owner of Insured Premises | $0 | Name, Premises |
| 926 | Controlling Interests | $0 | Name |
| 21022 | Designated Person Or Organization | $25 | Name |
| 21019 | Engineers, Architects or Surveyors | $0 | None |
| 21023 | Engineers... Not Engaged by Named Insured | $25 | Name |
| 21020 | Lessor of Leased Equipment | $25 | Name |
| 21053 | Managers or Lessors of Premises | $25 | Name, Premises |
| 21054 | Mortgagee, Assignee or Receiver | $0 | Name, Premises |
| 21055 | Owner... From Whom Land has been Leased | $0 | Name, Premises |
| 21024 | Owners, Lessees or Contractors | $25 | Name, Premises (auto-fill) |
| 21016 | State/Political - Permits Relating to Premises | $25 | Standard |
| 21026 | State/Political Subdivisions - Permits | $25 | Standard |
| 21017 | Townhouse Associations | $25 | None |
| 21021 | Vendors | $25 | Name, Products |

### 9.3 Traceability Matrix

| Requirement ID | Source Code Reference | Validation |
|----------------|----------------------|------------|
| 15 AI Types | ctl_App_AdditionalInsureds_CGL.ascx:full control | US-CGL-AI-001 |
| Maximum 4 Limit | JavaScript limit validation | US-CGL-AI-002 |
| Conditional Fields | Type-specific field display logic | US-CGL-AI-003 |
| Premium Calculation | JavaScript premium calculation functions | US-CGL-AI-004 |
| Illinois State Logic | State conditional display logic | US-CGL-AI-006 |
| $0 Premium Types | Premium classification logic | US-CGL-AI-007 |
| Vendor Products | Vendor type conditional field logic | US-CGL-AI-009 |
| Auto-Fill Logic | Construction type auto-population | US-CGL-AI-003 |

---

## 10. Document Metadata

**Prepared By**: Mason (IFI Requirements Extraction Specialist)  
**Reviewed By**: Vera (IFI Quality Validator) - Pending  
**Approved By**: [IFI Technical Authority] - Pending  
**Document Location**: `//project/ifm/product_requirements/CGL/Additional_Insureds_Management/Modernization_CGL_AdditionalInsureds.md`

**Analysis Source**: Rex (IFI Pattern Miner) - CGL Comprehensive System Analysis  
**Architecture Input**: Aria (IFI Architect) - Pending  
**Domain Validation**: Rita (IFI Insurance Specialist) - Pending  
**Orchestration**: Douglas (IFI Orchestrator) - Delegation Accepted

**Rex Analysis Source**: `//project/ifm/meta/rex/cgl_comprehensive_system_analysis/cgl_complete_lob_patterns.md`

**Token Budget Used**: 12.5K / 25K tokens

---

**END OF REQUIREMENTS DOCUMENT**