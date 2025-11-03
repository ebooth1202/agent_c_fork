# Modernization_CGL_StateSpecificCoverage

**Line of Business**: Commercial General Liability (CGL)  
**Feature**: State-Specific Coverage Variations  
**Document Version**: 1.0  
**Date**: 2024-12-19  
**Status**: Draft

---

## 1. Executive Summary

The CGL State-Specific Coverage Variations feature implements sophisticated state-dependent coverage offerings, business rules, and regulatory compliance requirements across Illinois, Ohio, and Indiana. This critical component manages distinct coverage patterns including Illinois Home Repair & Remodeling coverage, Ohio Stop Gap liability protection, and coordinated Indiana/Ohio liquor liability frameworks, while maintaining system architecture flexibility for future state expansion.

**Key Points:**
- **Business Purpose**: Provide state-compliant coverage options that meet specific regulatory requirements and market demands in Illinois, Ohio, and Indiana
- **Current Implementation**: State-conditional coverage display logic, distinct liquor liability structures, Illinois-specific additional insured types, Ohio-exclusive Stop Gap coverage
- **Modernization Scope**: Transform state-specific logic into maintainable, scalable architecture supporting current state variations while enabling future state expansion
- **Expected Business Value**: Maintained regulatory compliance with improved system maintainability, enhanced state logic management, and reduced complexity for future state additions

The system demonstrates sophisticated state logic management requiring careful architectural planning to preserve regulatory compliance while improving system maintainability and extensibility.

---

## 2. Business Overview

The CGL State-Specific Coverage Variations feature addresses the complex reality that Commercial General Liability insurance must comply with varying state regulations, market demands, and underwriting requirements across different jurisdictions. This sophisticated system manages three distinct state coverage patterns while maintaining a unified user experience and system architecture.

### 2.1 Feature Purpose

State-specific coverage variations exist to ensure regulatory compliance and market competitiveness across different states while maintaining operational efficiency through a unified CGL platform. The system addresses:

- **Regulatory Compliance**: Each state has unique insurance regulations requiring specific coverage offerings, limits, and endorsements
- **Market Competitiveness**: States have different market demands requiring specialized coverage options to compete effectively
- **Underwriting Standards**: State-specific risk patterns require tailored coverage approaches and underwriting guidelines
- **Operational Efficiency**: Unified system architecture with state-conditional logic provides scalability while managing complexity

The current three-state implementation (Illinois, Ohio, Indiana) provides foundation patterns for future state expansion while demonstrating architectural approaches to state-specific complexity management.

### 2.2 User Roles and Personas

**Primary Users:**
- **State-Licensed Insurance Agents**: Must understand state-specific coverage options and regulatory requirements for their licensed states
- **Multi-State Commercial Insurance Brokers**: Navigate varying state requirements for clients with operations across multiple states
- **State-Specific Underwriters**: Apply state-specific underwriting guidelines and coverage standards

**Secondary Users:**
- **Compliance Officers**: Monitor state-specific coverage offerings for regulatory compliance and filing requirements
- **Product Managers**: Manage state coverage variations and coordinate new state implementation
- **System Administrators**: Configure and maintain state-specific logic and coverage availability

### 2.3 Business Process Context

State-specific coverage logic integrates throughout the CGL workflow, influencing available coverage options, validation rules, additional insured types, and premium calculations. This pervasive state dependency requires careful coordination across all system components.

**State Logic Integration Points:**
1. **Quote Initialization**: State determines available coverage universe
2. **Coverage Selection**: State-conditional coverage options display
3. **Additional Insureds**: State-specific additional insured types (Illinois City of Chicago)
4. **Validation Rules**: State-specific business rule enforcement
5. **Premium Calculation**: State-specific rating factors and coverage pricing
6. **Policy Issuance**: State-compliant policy forms and endorsements

### 2.4 Regulatory Context

State insurance regulations require specific coverage offerings, policy language, and underwriting practices that vary significantly across jurisdictions. The system must maintain compliance with:

- **Illinois Regulations**: Home Repair & Remodeling coverage requirements, Chicago municipal requirements for scaffolding operations
- **Ohio Regulations**: Workers' compensation coordination through Stop Gap coverage, specific liquor liability structures
- **Indiana Regulations**: Coordinated liquor liability regulations similar to Ohio patterns
- **Multi-State Compliance**: Consistent application of state-specific rules while maintaining operational efficiency

---

## 3. Detailed Feature Specifications

### 3.1 Illinois-Specific Coverage Patterns

**Source**: State conditional logic throughout CGL coverage controls

**Illinois Coverage 1: Home Repair & Remodeling (IL-Specific)**
- **Coverage Code**: IL Contractors - Home Repair & Remodeling
- **Availability**: Illinois quotes only (state-conditional display)
- **Coverage Limit**: Fixed $10,000 coverage limit (not user-selectable)
- **Business Purpose**: Address Illinois regulatory requirements for home improvement contractor liability
- **Premium Structure**: Fixed premium based on $10K limit and contractor operations exposure
- **Regulatory Basis**: Illinois state requirements for residential contractor coverage
- **Source**: State-specific coverage configuration in CGL policy level coverages

**Illinois Coverage 2: Illinois Liquor Liability Structure**
- **Business Types**: 4 categories - Manufacturer/Wholesalers, Restaurants/Hotels, Package Stores, Clubs
- **Structural Difference**: Different limit structure and validation rules compared to Indiana/Ohio
- **Sales Input Requirements**: Separate sales input required for each selected business type
- **Validation Logic**: Illinois-specific validation rules for sales amounts and classification requirements
- **Premium Calculation**: Illinois-specific rating factors and premium structure
- **Regulatory Compliance**: Illinois liquor liability regulations and underwriting requirements
- **Source**: Illinois-specific liquor liability configuration and validation logic

**Illinois Coverage 3: City of Chicago - Scaffolding Additional Insured**
- **Additional Insured Code**: 80537
- **Availability**: Illinois quotes only, specifically for Chicago operations
- **Premium**: $25 (standard additional insured premium)
- **Required Fields**: Name and premises/location description mandatory
- **Regulatory Purpose**: Meet Chicago municipal requirements for scaffolding contractor coverage
- **Business Rule**: Mandatory for scaffolding operations within Chicago city limits
- **Source**: ctl_App_AdditionalInsureds_CGL.ascx, Illinois state conditional logic

### 3.2 Ohio-Specific Coverage Patterns

**Source**: Ohio state conditional logic in CGL coverage system

**Ohio Coverage 1: Stop Gap Liability Coverage**
- **Coverage Purpose**: Coordinate with Ohio workers' compensation system for liability gaps
- **Availability**: Ohio quotes only (state-exclusive coverage)
- **Coverage Structure**: Specific limit selections coordinated with workers' compensation coverage
- **Field Requirements**: Payroll input required for exposure calculation and premium rating
- **Business Integration**: Coordinates with workers' compensation coverage to provide gap protection
- **Underwriting Logic**: Ohio-specific underwriting requirements for Stop Gap coverage selection
- **Premium Calculation**: Based on payroll exposure and Ohio-specific rating factors
- **Source**: Ohio state-specific coverage configuration in policy level coverages

**Ohio Coverage 2: Ohio Liquor Liability Structure (Shared with Indiana)**
- **Business Types**: 4 categories - Manufacturer/Wholesalers, Restaurants/Hotels, Package Stores, Clubs (identical to Indiana)
- **Shared Pattern**: Common liquor liability structure and validation logic with Indiana
- **Sales Input Requirements**: Separate sales input for each selected business type category
- **Validation Rules**: Shared validation logic between Ohio and Indiana implementations
- **Limit Structure**: Common limit options and premium structure with Indiana
- **Regulatory Alignment**: Ohio and Indiana liquor liability regulations sufficiently aligned for shared implementation
- **Source**: Ohio/Indiana shared liquor liability configuration logic

### 3.3 Indiana-Specific Coverage Patterns

**Source**: Indiana state conditional logic coordination with Ohio patterns

**Indiana Coverage 1: Indiana Liquor Liability Structure (Shared with Ohio)**
- **Business Types**: 4 categories - Manufacturer/Wholesalers, Restaurants/Hotels, Package Stores, Clubs (identical to Ohio)
- **Shared Implementation**: Common codebase and business logic with Ohio for operational efficiency
- **Sales Input Structure**: Identical sales input requirements and validation as Ohio
- **Premium Coordination**: Shared premium calculation logic with Ohio-specific rating factors
- **Regulatory Coordination**: Indiana liquor liability regulations align sufficiently with Ohio for shared system logic
- **Validation Rules**: Common validation framework with Ohio for business type selection and sales requirements
- **Source**: Indiana/Ohio shared liquor liability implementation

### 3.4 Multi-State Coordination Patterns

**Source**: State detection and conditional logic throughout CGL system

**State Detection Logic:**
- **Policy State Determination**: System identifies policy state early in quote process
- **Coverage Universe Control**: State determines which coverages display in coverage selection interface
- **Validation Rule Selection**: State determines which validation rules apply to coverage selections
- **Additional Insured Filtering**: State controls which additional insured types are available
- **Premium Rating Coordination**: State determines applicable rating factors and calculation methods

**Shared Pattern Management:**
- **Ohio/Indiana Liquor Coordination**: Common implementation reduces maintenance complexity
- **Illinois Differentiation**: Separate implementation acknowledges Illinois regulatory differences
- **Architecture Flexibility**: State conditional logic designed to support additional state implementations

**State Logic Architecture:**
- **Centralized State Detection**: Single point of state determination for consistency
- **Distributed State Logic**: State-conditional logic distributed throughout system components
- **Configuration Management**: State-specific configurations managed through systematic approach
- **Validation Coordination**: State-specific validation rules coordinated with general CGL validation framework

---

## 4. UI/UX Requirements ⭐ MANDATORY

### 4.1 Auto-Display/Hide Behaviors

**Pattern Description:**
State-specific coverage options appear and disappear based on the policy state detected during quote initialization. The interface dynamically adjusts available coverage options, additional insured types, and field requirements while maintaining a consistent user experience across all states.

**State-Conditional Display Logic:**
```
Illinois Quotes: Show Home Repair & Remodeling, Illinois Liquor Liability structure, City of Chicago Scaffolding AI
Ohio Quotes: Show Stop Gap coverage, Ohio/Indiana Liquor Liability structure  
Indiana Quotes: Show Ohio/Indiana Liquor Liability structure only
All Other States: Standard CGL coverage options without state-specific additions
Source: State detection logic throughout CGL coverage controls
```

**Coverage Section Visibility:**
```
Home Repair & Remodeling: Visible only for Illinois quotes with $10K fixed limit display
Stop Gap Coverage: Visible only for Ohio quotes with limit selection and payroll input
Liquor Liability: Different business type structures based on Illinois vs Ohio/Indiana
City of Chicago AI: Visible only in Illinois additional insured type selection
Source: State-conditional coverage display throughout policy level coverage controls
```

### 4.2 Text Input Specifications

**Field Specifications:**

| Field Name | Label | Type | Character Limit | Required | Default | State Availability |
|------------|-------|------|-----------------|----------|---------|-------------------|
| IL Home Repair Limit | "Home Repair & Remodeling" | Display Only | N/A | N/A | $10,000 | Illinois Only |
| OH Stop Gap Limit | "Stop Gap Limit" | Dropdown | N/A | When Selected | None | Ohio Only |
| OH Stop Gap Payroll | "Annual Payroll ($)" | Integer | 10 digits | When Stop Gap | Empty | Ohio Only |
| IL Liquor Sales (by type) | "Annual Sales ($)" | Integer | 10 digits | When Type Selected | Empty | Illinois Only |
| OH/IN Liquor Sales (by type) | "Annual Sales ($)" | Integer | 10 digits | When Type Selected | Empty | Ohio/Indiana |
| Chicago Scaffolding Name | "Name" | Text | 255 chars | When Selected | Empty | Illinois Only |
| Chicago Scaffolding Premises | "Premises/Location" | Multi-line | 500 chars | When Selected | Empty | Illinois Only |

**State-Specific Field Requirements:**

| State | Coverage | Required Fields | Conditional Logic |
|-------|----------|----------------|-------------------|
| Illinois | Home Repair & Remodeling | None (fixed limit) | Always $10K when displayed |
| Ohio | Stop Gap | Limit + Payroll | Payroll required when Stop Gap selected |
| Illinois | Liquor Liability | Sales by business type | Each selected type requires sales input |
| Ohio/Indiana | Liquor Liability | Sales by business type | Each selected type requires sales input |
| Illinois | City of Chicago - Scaffolding | Name + Premises | Both required when AI type selected |

### 4.3 Validation Visual Indicators

**Error States:**

**State-Specific Coverage Validation Errors:**
- **Visual**: Red error message below state-specific coverage fields with state context
- **Error Messages**: 
  - "Stop Gap payroll is required when Stop Gap coverage is selected"
  - "Illinois Liquor Liability sales amount required for selected business types"
  - "City of Chicago - Scaffolding requires name and premises information"
- **State Context**: Error messages include state reference for clarity
- **Trigger**: State-specific field requirements not met when coverage selected

**Liquor Liability Structure Validation:**
- **Visual**: Red borders around empty sales input fields for selected business types
- **Error Messages**: 
  - "Sales amount required for selected liquor liability business types"
  - "Sales amount must be positive whole number"
- **Structure Differences**: Illinois shows different validation messages than Ohio/Indiana
- **Business Type Validation**: Each selected business type must have corresponding sales input

**Additional Insured State Validation:**
- **Visual**: Red border around empty required fields for City of Chicago - Scaffolding
- **Error Message**: "Name and premises description required for City of Chicago - Scaffolding additional insured"
- **Illinois-Specific**: Only appears for Illinois quotes when scaffolding AI type selected
- **Field-Specific**: Separate validation for name and premises fields

### 4.4 Interactive Elements

**State-Conditional Coverage Selection:**
- **Illinois Coverage Checkboxes**: Home Repair & Remodeling (fixed $10K), Illinois Liquor Liability structure
- **Ohio Coverage Options**: Stop Gap with limit dropdown and payroll input field
- **Indiana Coverage Options**: Ohio/Indiana Liquor Liability structure (identical to Ohio)
- **Dynamic Display**: Coverage options appear based on detected policy state

**Liquor Liability Business Type Selection:**
- **Illinois Structure**: 4 business types with Illinois-specific validation and premium rules
- **Ohio/Indiana Structure**: Same 4 business types with shared validation and premium structure
- **Sales Input Fields**: Conditional sales input fields appear when business types selected
- **Validation Coordination**: Real-time validation for required sales inputs by business type

**Stop Gap Coverage Configuration (Ohio Only):**
- **Limit Selection**: Dropdown with Ohio-specific Stop Gap limit options
- **Payroll Input**: Required annual payroll field for exposure calculation
- **Integration Display**: Shows coordination with workers' compensation coverage
- **Premium Calculation**: Real-time premium calculation based on limit and payroll

### 4.5 Accessibility Requirements

- **State Context Clarity**: Screen readers announce state-specific coverage availability and requirements
- **Keyboard Navigation**: All state-specific coverage options accessible via keyboard navigation
- **Focus Management**: Focus moves logically through state-conditional fields and coverage options
- **ARIA Labels**: State-specific coverage options properly labeled for assistive technology
- **Error Announcements**: State-specific validation errors announced immediately with state context

### 4.6 Responsive Design Requirements

- **Mobile Devices**: State-specific coverage options stack vertically with clear state identification
- **Tablets**: Two-column layout for state coverage options while maintaining state context clarity
- **Desktop**: Full layout showing all available state-specific options with clear state identification
- **State Identification**: Clear visual indication of which state's coverage options are displayed
- **Browser Compatibility**: State-conditional logic functions across all VelociRater-supported browsers

---

## 5. Validation Rules and Business Logic ⭐ MANDATORY

### 5.1 Client-Side Validation (JavaScript)

**Function: ValidateIllinoisSpecificCoverages()**
- **Purpose**: Validate Illinois-specific coverage selections and field requirements
- **Trigger**: Illinois coverage selection events, Illinois-specific field input changes
- **Logic**:
  1. Validate Home Repair & Remodeling coverage (fixed $10K limit, no additional validation)
  2. Validate Illinois Liquor Liability sales inputs for selected business types
  3. Validate City of Chicago - Scaffolding name and premises fields when selected
- **Error Messages**: Illinois-specific error messages with state context
- **State Context**: Only executes when policy state = Illinois
- **Source**: Illinois state-specific validation logic

**Function: ValidateOhioSpecificCoverages()**
- **Purpose**: Validate Ohio-specific coverage selections including Stop Gap requirements
- **Trigger**: Ohio coverage selection events, Stop Gap field changes, payroll input changes
- **Logic**:
  1. Validate Stop Gap limit selection when coverage selected
  2. Validate payroll input required when Stop Gap selected (positive integer, reasonable range)
  3. Validate Ohio/Indiana Liquor Liability structure (shared validation with Indiana)
- **Error Messages**: "Stop Gap payroll is required when Stop Gap coverage is selected"
- **Payroll Validation**: Range validation for annual payroll input (minimum/maximum thresholds)
- **Source**: Ohio state-specific validation logic

**Function: ValidateIndianaSpecificCoverages()**
- **Purpose**: Validate Indiana-specific coverage selections (primarily shared Ohio/Indiana Liquor)
- **Trigger**: Indiana coverage selection events, liquor liability field changes
- **Logic**:
  1. Validate Ohio/Indiana Liquor Liability structure (shared validation with Ohio)
  2. Validate sales inputs for selected liquor business types
  3. Apply Indiana-specific validation rules where different from Ohio
- **Error Messages**: Indiana-specific context in shared validation messages
- **Shared Logic**: Leverages common validation functions with Ohio for liquor liability
- **Source**: Indiana state-specific validation logic (primarily shared with Ohio)

**Function: ValidateLiquorLiabilityByState()**
- **Purpose**: Apply appropriate liquor liability validation based on policy state
- **Trigger**: Liquor liability selection events across all states
- **Logic**:
  1. Determine policy state (Illinois vs Ohio/Indiana pattern)
  2. Apply Illinois-specific liquor validation OR Ohio/Indiana shared validation
  3. Validate business type selections and corresponding sales inputs
  4. Apply state-specific limit and premium validation
- **State Branching**: Different validation paths for Illinois vs Ohio/Indiana patterns
- **Sales Validation**: Positive integer validation with state-specific business type requirements
- **Source**: State-conditional liquor liability validation logic

### 5.2 State-Specific Field Validation

**Illinois Field Requirements:**

| Coverage/Feature | Required Fields | Validation Logic | Error Message |
|------------------|----------------|------------------|---------------|
| Home Repair & Remodeling | None | Fixed $10K limit (no user input) | N/A (no validation needed) |
| Illinois Liquor Liability | Sales by business type | Sales > 0, integer, when type selected | "Sales amount required for selected Illinois liquor business types" |
| City of Chicago - Scaffolding | Name + Premises | Not empty, minimum 2 chars name, 5 chars premises | "Name and premises required for City of Chicago - Scaffolding" |

**Ohio Field Requirements:**

| Coverage/Feature | Required Fields | Validation Logic | Error Message |
|------------------|----------------|------------------|---------------|
| Stop Gap Coverage | Limit + Payroll | Limit selected, payroll > 0 integer | "Stop Gap limit and payroll both required when coverage selected" |
| Ohio/Indiana Liquor | Sales by business type | Sales > 0, integer, when type selected | "Sales amount required for selected liquor business types" |

**Indiana Field Requirements:**

| Coverage/Feature | Required Fields | Validation Logic | Error Message |
|------------------|----------------|------------------|---------------|
| Ohio/Indiana Liquor | Sales by business type | Sales > 0, integer, when type selected | "Sales amount required for selected liquor business types" |

### 5.3 Business Rule Validation

**Rule 1: State Coverage Availability Enforcement**
- **Description**: Only state-appropriate coverage options can be selected based on detected policy state
- **Validation Logic**: Policy state determines coverage universe, prevents invalid state/coverage combinations
- **Error Handling**: Invalid coverage selections prevented through UI control (not displayed rather than validation error)
- **Business Rationale**: Regulatory compliance requires state-appropriate coverage offerings only
- **Source**: State detection logic throughout coverage selection interface

**Rule 2: Illinois Home Repair & Remodeling Fixed Limit**
- **Description**: Illinois Home Repair & Remodeling coverage has fixed $10,000 limit (not user-selectable)
- **Validation Logic**: When coverage selected, limit automatically set to $10K with no user modification allowed
- **Error Handling**: No validation error possible (system-controlled value)
- **Business Rationale**: Illinois regulatory requirements specify exact coverage limit for residential contractor coverage
- **Source**: Illinois-specific coverage configuration logic

**Rule 3: Ohio Stop Gap Payroll Requirement**
- **Description**: Ohio Stop Gap coverage requires annual payroll input for exposure calculation and premium rating
- **Validation Logic**: Stop Gap coverage selected → Annual payroll required (positive integer, reasonable range)
- **Error Handling**: Validation prevents quote progression without payroll input
- **Business Rationale**: Stop Gap premium calculation requires payroll exposure base for actuarial accuracy
- **Source**: Ohio Stop Gap coverage validation and premium calculation logic

**Rule 4: Liquor Liability Structure by State**
- **Description**: Illinois uses different liquor liability structure and validation than Ohio/Indiana shared pattern
- **Validation Logic**: State determines which liquor liability validation and premium calculation applies
- **Error Handling**: State-appropriate validation messages and business rules applied
- **Business Rationale**: State regulatory differences require different liquor liability treatment
- **Source**: State-conditional liquor liability implementation

**Rule 5: City of Chicago Additional Insured Availability**
- **Description**: City of Chicago - Scaffolding additional insured type only available for Illinois quotes
- **Validation Logic**: Additional insured type 80537 only displays when policy state = Illinois
- **Error Handling**: Type not available for selection in non-Illinois quotes (UI control rather than validation)
- **Business Rationale**: Chicago municipal requirements only apply to Illinois operations
- **Source**: Illinois state-conditional additional insured type availability

### 5.4 Server-Side Validation

**Security Validations:**
- **State Tampering Prevention**: Server-side verification that selected coverages match detected policy state
- **Input Sanitization**: All state-specific numeric inputs (payroll, sales amounts) sanitized and range-validated
- **Coverage Consistency**: Server-side verification of state/coverage combinations for regulatory compliance
- **Premium Calculation Verification**: Server-side recalculation of state-specific premiums for accuracy

**Data Integrity Checks:**
- **State Detection Consistency**: Verify policy state determination consistency across quote components
- **Coverage Configuration Validation**: Ensure state-specific coverage configurations match regulatory requirements
- **Field Requirement Enforcement**: Server-side validation of state-specific required field completion
- **Regulatory Compliance Verification**: Server-side confirmation of state regulatory requirement satisfaction

---

## 6. User Stories and Acceptance Criteria

### US-CGL-STATE-001: Display Illinois-Specific Coverage Options

**As an** Insurance Agent licensed in Illinois  
**I need to** see Illinois-specific coverage options when creating Illinois CGL quotes  
**So that** I can provide state-compliant coverage that meets Illinois regulatory requirements

**Acceptance Criteria:**
1. Given I am creating a CGL quote with Illinois policy state, when I view coverage options, then I see "Home Repair & Remodeling" coverage with fixed $10,000 limit
2. Given I am creating an Illinois quote, when I view liquor liability options, then I see Illinois-specific liquor liability structure with 4 business types
3. Given I am creating an Illinois quote, when I view additional insured options, then I see "City of Chicago - Scaffolding" as an available additional insured type
4. Given I am creating quotes in states other than Illinois, when I view coverage options, then Illinois-specific coverages are not displayed
5. Given Illinois-specific coverages are displayed, when I select them, then appropriate field requirements and validation apply

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: State detection logic, coverage configuration system

### US-CGL-STATE-002: Configure Ohio Stop Gap Coverage

**As an** Insurance Agent licensed in Ohio  
**I need to** configure Stop Gap coverage with appropriate limit and payroll information  
**So that** I can provide proper workers' compensation coordination coverage for Ohio clients

**Acceptance Criteria:**
1. Given I am creating an Ohio CGL quote, when I view coverage options, then I see "Stop Gap" coverage as an available option
2. Given I select Stop Gap coverage, when the selection is made, then limit selection dropdown and payroll input field appear
3. Given I select a Stop Gap limit without entering payroll, when I attempt to continue, then I receive validation error requiring payroll input
4. Given I enter payroll information for Stop Gap, when I complete the fields, then premium calculation includes Stop Gap coverage
5. Given I am creating quotes in states other than Ohio, when I view coverage options, then Stop Gap coverage is not displayed

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: Ohio state detection, Stop Gap coverage configuration, payroll validation

### US-CGL-STATE-003: Manage Shared Ohio/Indiana Liquor Liability

**As an** Insurance Agent licensed in Ohio or Indiana  
**I need to** configure liquor liability coverage using the shared Ohio/Indiana structure  
**So that** I can provide appropriate liquor liability coverage with consistent business rules across both states

**Acceptance Criteria:**
1. Given I am creating an Ohio or Indiana quote, when I view liquor liability options, then I see the shared 4 business type structure
2. Given I select liquor liability business types in Ohio, when I make selections, then the same validation and field requirements apply as Indiana
3. Given I select business types for liquor coverage, when selections are made, then corresponding sales input fields appear for each type
4. Given I complete sales information for selected types, when information is provided, then premium calculation applies shared Ohio/Indiana logic
5. Given the shared structure is used, when I switch between Ohio and Indiana quotes, then liquor liability interface and requirements remain consistent

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: Ohio/Indiana state detection, shared liquor liability implementation

### US-CGL-STATE-004: Validate Illinois Home Repair & Remodeling Coverage

**As an** Insurance Agent in Illinois  
**I need to** have Home Repair & Remodeling coverage automatically configured with fixed limit  
**So that** coverage meets Illinois regulatory requirements without manual limit selection

**Acceptance Criteria:**
1. Given I select Illinois Home Repair & Remodeling coverage, when the selection is made, then the limit is automatically set to $10,000
2. Given Home Repair & Remodeling is selected, when I view the coverage, then the $10K limit is displayed as fixed (not user-modifiable)
3. Given the coverage is selected with fixed limit, when premium calculation occurs, then appropriate premium is applied for $10K Home Repair coverage
4. Given I attempt to modify the Home Repair limit, when I interact with the coverage, then no limit modification options are available
5. Given the coverage is configured, when I review the quote, then Home Repair & Remodeling appears with correct $10K limit and appropriate premium

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: Illinois state detection, fixed limit coverage configuration

### US-CGL-STATE-005: Configure City of Chicago Scaffolding Additional Insured

**As an** Insurance Agent in Illinois writing coverage for Chicago operations  
**I need to** select City of Chicago - Scaffolding additional insured coverage with required information  
**So that** I can meet Chicago municipal requirements for scaffolding contractor operations

**Acceptance Criteria:**
1. Given I am creating an Illinois quote, when I view additional insured options, then I see "City of Chicago - Scaffolding ($25)" as available
2. Given I am creating quotes in other states, when I view additional insured options, then City of Chicago - Scaffolding is not displayed
3. Given I select City of Chicago - Scaffolding, when the selection is made, then name and premises input fields appear as required
4. Given I leave name or premises fields empty, when I attempt to continue, then validation prevents submission with specific error messages
5. Given I complete all required fields for scaffolding coverage, when information is provided, then $25 premium is applied and coverage is configured

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: Illinois state detection, additional insured system, conditional field validation

### US-CGL-STATE-006: Handle State Detection and Coverage Universe Control

**As a** CGL system  
**I need to** automatically detect policy state and display appropriate coverage options  
**So that** agents see only valid, state-compliant coverage choices for their quotes

**Acceptance Criteria:**
1. Given a quote is initiated with Illinois address information, when coverage options load, then Illinois-specific coverages are included in available options
2. Given a quote is initiated with Ohio address information, when coverage options load, then Ohio-specific coverages (Stop Gap) are available
3. Given a quote is initiated with Indiana address information, when coverage options load, then shared Ohio/Indiana liquor structure is available
4. Given a quote is initiated with address from other states, when coverage options load, then only standard CGL coverages are available without state-specific additions
5. Given state detection occurs, when coverage universe is determined, then validation rules and field requirements match the detected state

**Priority**: High  
**Complexity**: Large  
**Dependencies**: Address processing, state detection logic, coverage configuration system

### US-CGL-STATE-007: Validate State-Specific Field Requirements

**As an** Insurance Agent  
**I need to** receive appropriate validation feedback for state-specific coverage field requirements  
**So that** I can complete state-compliant coverage configurations correctly

**Acceptance Criteria:**
1. Given I select Ohio Stop Gap coverage without payroll, when validation occurs, then I receive "Stop Gap payroll is required" error message
2. Given I select Illinois liquor liability types without sales information, when validation occurs, then I receive Illinois-specific liquor validation errors
3. Given I select City of Chicago - Scaffolding without required fields, when validation occurs, then I receive scaffolding-specific field requirement errors
4. Given I complete all state-specific field requirements, when validation occurs, then validation passes and I can proceed with quote
5. Given validation errors exist for state-specific fields, when errors are displayed, then error messages include appropriate state context for clarity

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: State-specific validation logic, error message system

### US-CGL-STATE-008: Calculate State-Specific Premiums Correctly

**As an** Insurance Agent  
**I need to** have state-specific coverage premiums calculated accurately  
**So that** quotes reflect proper pricing for state-specific coverage extensions

**Acceptance Criteria:**
1. Given I configure Illinois Home Repair & Remodeling coverage, when premium calculation occurs, then appropriate premium is applied for fixed $10K coverage
2. Given I configure Ohio Stop Gap with limit and payroll, when premium calculation occurs, then Stop Gap premium reflects limit selection and payroll exposure
3. Given I configure Illinois liquor liability with sales information, when premium calculation occurs, then Illinois-specific liquor premium calculation applies
4. Given I configure Ohio/Indiana liquor liability, when premium calculation occurs, then shared premium calculation logic applies appropriately
5. Given state-specific coverages are selected, when total premium is calculated, then all state-specific coverage premiums integrate correctly with base CGL premium

**Priority**: High  
**Complexity**: Large  
**Dependencies**: Premium calculation system, state-specific rating factors, coverage integration

---

## 7. Testing Requirements

### 7.1 Functional Testing

**Test Scenario 1: Illinois State Coverage Display and Configuration**
- **Setup**: Create new CGL quote with Illinois address/state information
- **Steps**:
  1. Verify Illinois state detection occurs correctly
  2. Confirm Home Repair & Remodeling coverage appears with fixed $10K limit
  3. Verify Illinois liquor liability structure displays (different from Ohio/Indiana)
  4. Confirm City of Chicago - Scaffolding appears in additional insured options
  5. Test Illinois-specific field requirements and validation
- **Expected Result**: All Illinois-specific coverages display correctly with appropriate field requirements

**Test Scenario 2: Ohio State Coverage Display and Stop Gap Configuration**
- **Setup**: Create new CGL quote with Ohio address/state information
- **Steps**:
  1. Verify Ohio state detection occurs correctly
  2. Confirm Stop Gap coverage appears as available option
  3. Select Stop Gap coverage and verify limit dropdown and payroll field appear
  4. Test payroll requirement validation when Stop Gap selected
  5. Verify Ohio/Indiana liquor liability structure displays (shared with Indiana)
- **Expected Result**: Ohio-specific coverages display correctly with proper Stop Gap configuration requirements

**Test Scenario 3: Indiana State Coverage Display and Shared Liquor Structure**
- **Setup**: Create new CGL quote with Indiana address/state information
- **Steps**:
  1. Verify Indiana state detection occurs correctly
  2. Confirm Ohio/Indiana liquor liability structure displays
  3. Test liquor liability business type selection and sales input requirements
  4. Verify validation and premium calculation match Ohio pattern
  5. Confirm no Indiana-unique coverages display (only shared patterns)
- **Expected Result**: Indiana quote displays shared Ohio/Indiana liquor structure with consistent behavior

**Test Scenario 4: Other State Standard Coverage Display**
- **Setup**: Create new CGL quote with address from state other than IL/OH/IN (e.g., California)
- **Steps**:
  1. Verify standard state detection occurs correctly
  2. Confirm NO Illinois-specific coverages display (Home Repair, City of Chicago AI)
  3. Confirm NO Ohio-specific coverages display (Stop Gap)
  4. Confirm standard liquor liability structure displays (not Illinois or Ohio/Indiana patterns)
  5. Verify standard CGL coverage options and validation apply
- **Expected Result**: Only standard CGL coverages display without any state-specific additions

### 7.2 State Logic Testing

**State Detection Testing:**
- Verify accurate state detection based on policy address information
- Test edge cases (military addresses, PO boxes, etc.)
- Confirm state detection consistency across quote workflow
- Validate state detection integration with coverage display logic

**Coverage Availability Testing:**
- Test each state's coverage universe matches requirements exactly
- Verify state-specific coverages only appear for appropriate states
- Test shared coverage patterns display consistently across applicable states
- Confirm coverage availability coordination with additional insured types

**State-Specific Validation Testing:**
- Test Illinois validation rules (Home Repair, liquor, City of Chicago AI)
- Test Ohio validation rules (Stop Gap payroll, shared liquor)
- Test Indiana validation rules (shared liquor structure)
- Test other state standard validation (no state-specific rules)

### 7.3 Cross-State Integration Testing

**Multi-State Workflow Testing:**
- Test agents working across multiple states can access appropriate coverages
- Verify consistent user experience across state-specific variations
- Test state switching scenarios (changing policy address mid-quote)
- Confirm state-specific premium calculations integrate correctly

**Shared Pattern Testing:**
- Test Ohio/Indiana liquor liability shared implementation thoroughly
- Verify consistency of shared patterns across both states
- Test maintenance efficiency of shared vs separate implementations
- Confirm shared pattern changes apply correctly to both states

### 7.4 Regulatory Compliance Testing

**Illinois Compliance Testing:**
- Verify Home Repair & Remodeling fixed $10K limit meets Illinois requirements
- Test City of Chicago - Scaffolding additional insured meets municipal requirements
- Confirm Illinois liquor liability structure complies with state regulations
- Validate Illinois-specific field requirements and validation messages

**Ohio Compliance Testing:**
- Verify Stop Gap coverage structure meets Ohio workers' compensation coordination requirements
- Test payroll input requirements and validation for Stop Gap exposure calculation
- Confirm Ohio liquor liability structure meets state regulatory requirements

**Indiana Compliance Testing:**
- Verify shared Ohio/Indiana liquor structure meets Indiana regulatory requirements
- Test sales input requirements and validation for Indiana liquor liability
- Confirm Indiana regulatory requirements satisfied through shared implementation

### 7.5 Performance Testing

- **State Detection Performance**: State detection and coverage universe determination complete within 1 second
- **Coverage Display Performance**: State-conditional coverage options display within 2 seconds
- **Validation Performance**: State-specific validation feedback appears within 0.5 seconds
- **Premium Calculation Performance**: State-specific premium calculations complete within 2 seconds

---

## 8. Migration and Modernization Considerations

### 8.1 Data Migration

**Current State Logic Architecture**: State-conditional logic distributed throughout CGL coverage controls and validation classes
**Migration Requirements**: Preserve exact state coverage availability and business rule logic for regulatory compliance
**State Detection Migration**: Maintain consistent state detection logic and coverage universe determination
**Configuration Preservation**: Migrate all state-specific coverage configurations and field requirements exactly

### 8.2 Configuration Migration

**State-Specific Coverage Configuration**: Migrate Illinois Home Repair ($10K fixed), Ohio Stop Gap, shared Ohio/Indiana liquor
**Additional Insured State Logic**: Preserve Illinois City of Chicago - Scaffolding availability logic
**Validation Rule Migration**: Maintain state-specific validation logic and error messages
**Premium Calculation Migration**: Preserve state-specific rating factors and calculation methods

### 8.3 Integration Impact

**Quote Object Integration**: Ensure state-specific coverage selections integrate properly with quote data structure
**Premium Calculation Integration**: Maintain state-specific premium calculation coordination with overall policy rating
**Validation Framework Integration**: Preserve state-specific validation coordination with general CGL validation framework
**Address Processing Integration**: Maintain state detection coordination with address processing and validation

### 8.4 Rollback Strategy

**State Logic Preservation**: Maintain backup of current state-conditional logic throughout system
**Regulatory Compliance Backup**: Preserve current state-specific coverage configurations for regulatory rollback
**Coverage Availability Backup**: Maintain current coverage universe determination logic as rollback option
**Performance Baseline**: Document current state logic performance for comparison and rollback assessment

---

## 9. Source Attribution and Traceability

### 9.1 Source Code Files Analyzed

| File Path | Purpose | Lines Analyzed |
|-----------|---------|----------------|
| [State detection logic files] | Policy state determination and coverage universe control | [To be determined] |
| [Illinois-specific coverage files] | Home Repair & Remodeling, Illinois liquor, City of Chicago AI | [To be determined] |
| [Ohio-specific coverage files] | Stop Gap coverage, Ohio/Indiana liquor structure | [To be determined] |
| [Indiana-specific coverage files] | Shared Ohio/Indiana liquor implementation | [To be determined] |
| ctl_App_AdditionalInsureds_CGL.ascx | City of Chicago - Scaffolding state logic | Illinois state conditional logic |

### 9.2 State-Specific Coverage Specifications

| State | Coverage | Availability | Key Requirements |
|-------|----------|-------------|------------------|
| Illinois | Home Repair & Remodeling | Illinois only | Fixed $10K limit |
| Illinois | Illinois Liquor Liability | Illinois only | 4 business types, separate structure |
| Illinois | City of Chicago - Scaffolding AI | Illinois only | Name + premises required, $25 premium |
| Ohio | Stop Gap Coverage | Ohio only | Limit selection + payroll input required |
| Ohio | Ohio/Indiana Liquor | Ohio + Indiana | 4 business types, shared structure |
| Indiana | Ohio/Indiana Liquor | Ohio + Indiana | 4 business types, shared with Ohio |

### 9.3 Traceability Matrix

| Requirement ID | Source Code Reference | Validation |
|----------------|----------------------|------------|
| Illinois Coverage Display | Illinois state detection logic | US-CGL-STATE-001 |
| Ohio Stop Gap | Ohio-specific coverage logic | US-CGL-STATE-002 |
| Ohio/Indiana Liquor | Shared liquor implementation | US-CGL-STATE-003 |
| Illinois Home Repair | Illinois coverage configuration | US-CGL-STATE-004 |
| City of Chicago AI | ctl_App_AdditionalInsureds_CGL.ascx | US-CGL-STATE-005 |
| State Detection | State logic throughout system | US-CGL-STATE-006 |
| State Validation | State-specific validation files | US-CGL-STATE-007 |
| State Premium Calc | State-specific rating logic | US-CGL-STATE-008 |

---

## 10. Document Metadata

**Prepared By**: Mason (IFI Requirements Extraction Specialist)  
**Reviewed By**: Vera (IFI Quality Validator) - Pending  
**Approved By**: [IFI Technical Authority] - Pending  
**Document Location**: `//project/ifm/product_requirements/CGL/State_Specific_Coverage/Modernization_CGL_StateSpecificCoverage.md`

**Analysis Source**: Rex (IFI Pattern Miner) - CGL Comprehensive System Analysis  
**Architecture Input**: Aria (IFI Architect) - Pending  
**Domain Validation**: Rita (IFI Insurance Specialist) - Pending  
**Orchestration**: Douglas (IFI Orchestrator) - Delegation In Progress

**Rex Analysis Source**: `//project/ifm/meta/rex/cgl_comprehensive_system_analysis/cgl_complete_lob_patterns.md`

**Token Budget Used**: 18.5K / 25K tokens

---

**END OF REQUIREMENTS DOCUMENT**