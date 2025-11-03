# Modernization_CGL_CoverageValidation

**Line of Business**: Commercial General Liability (CGL)  
**Feature**: Coverage Validation Framework  
**Document Version**: 1.0  
**Date**: 2024-12-19  
**Status**: Draft

---

## 1. Executive Summary

The CGL Coverage Validation Framework implements a sophisticated multi-tier validation system that enforces complex business rules, coverage limit hierarchies, enhancement dependencies, and mandatory field synchronizations across the entire Commercial General Liability product. This critical framework ensures proper risk assessment, premium accuracy, regulatory compliance, and underwriting consistency through systematic validation of coverage relationships, limit hierarchies, and business rule constraints.

**Key Points:**
- **Business Purpose**: Enforce comprehensive business rules and coverage relationships to maintain underwriting integrity and regulatory compliance
- **Current Implementation**: Multi-file validation framework including GeneralInformationValidator.cs, CGL_PolicyCoveragesValidator.cs, PolicyLevelValidations.cs with hierarchical rule enforcement
- **Modernization Scope**: Transform complex legacy validation logic into modern validation architecture with enhanced error handling, improved user guidance, and maintainable rule management
- **Expected Business Value**: Maintained rigorous validation standards with improved user experience, better error messaging, and enhanced maintenance capabilities

The validation framework serves as the quality control backbone for CGL quotes, preventing invalid coverage configurations that could create exposure gaps, pricing errors, or regulatory violations while guiding users toward compliant coverage selections.

---

## 2. Business Overview

The CGL Coverage Validation Framework serves as the comprehensive business rule enforcement mechanism for Commercial General Liability insurance, ensuring all coverage configurations meet actuarial requirements, regulatory standards, and underwriting guidelines. This sophisticated system validates coverage limit relationships, enforces enhancement dependencies, manages mandatory field synchronizations, and prevents invalid coverage combinations that could create business risk.

### 2.1 Feature Purpose

The validation framework exists to protect the insurance company from operational risk by preventing invalid coverage configurations that could result in:
- **Exposure Gaps**: Coverage limits that don't align with risk exposure requirements
- **Premium Errors**: Coverage combinations that affect pricing accuracy
- **Regulatory Violations**: Coverage configurations that fail to meet state requirements
- **Underwriting Inconsistency**: Coverage selections that bypass established underwriting guidelines

The multi-layered validation approach ensures systematic rule enforcement from basic field validation through complex business rule validation, providing immediate feedback to users while maintaining data integrity throughout the quote process.

### 2.2 User Roles and Personas

**Primary Users:**
- **Insurance Agents**: Receive real-time validation feedback during coverage selection, must understand validation messages to guide clients toward compliant selections
- **Commercial Insurance Brokers**: Navigate complex validation rules for large accounts with sophisticated coverage requirements
- **Underwriters**: Rely on validation framework to ensure submitted quotes meet underwriting standards before review

**Secondary Users:**
- **Agency Staff**: Encounter validation messages during data entry, require clear guidance on resolving validation errors
- **System Administrators**: Monitor validation rule performance and manage validation rule updates
- **Compliance Officers**: Ensure validation rules align with regulatory requirements and company policies

### 2.3 Business Process Context

The validation framework operates throughout the CGL coverage configuration workflow, providing continuous validation from initial coverage selection through quote finalization. This real-time validation approach prevents invalid configurations from progressing through the quote process, reducing rework and improving quote accuracy.

**Validation Workflow Integration:**
1. Coverage Selection and Limit Configuration
2. **→ Real-time Validation Framework** (continuous operation)
3. Policy-Level Coverage Configuration  
4. **→ Enhanced Validation Framework** (comprehensive rule checking)
5. Premium Calculation and Quote Generation
6. **→ Final Validation Framework** (complete rule verification)

The progressive validation approach ensures early detection of validation issues while allowing complex rule validation at appropriate workflow points.

### 2.4 Regulatory Context

CGL validation rules must comply with state insurance regulations governing coverage limits, mandatory coverages, and policy structure requirements. The validation framework incorporates regulatory requirements for coverage limit relationships, ensuring policies meet state minimum requirements while preventing configurations that exceed regulatory guidelines.

State-specific validation rules address regulatory variations for coverage requirements, ensuring Ohio Stop Gap validation, Illinois-specific coverage rules, and multi-state compliance requirements are properly enforced throughout the quote process.

---

## 3. Detailed Feature Specifications

### 3.1 Coverage Limit Hierarchy Validation

**Source**: `GeneralInformationValidator.cs` - Coverage limit relationship enforcement

**Hierarchy Rule 1: General Aggregate ≥ Occurrence Liability Limit**
- **Business Rule**: General Aggregate must be greater than or equal to Occurrence Liability Limit
- **Validation Logic**: Compare selected General Aggregate value against selected Occurrence Liability Limit
- **Error Condition**: General Aggregate < Occurrence Liability Limit
- **Error Message**: "General Aggregate limit must be greater than or equal to Occurrence Liability limit"
- **User Guidance**: System suggests minimum General Aggregate based on Occurrence selection
- **Business Rationale**: General Aggregate covers all occurrences within policy period, must exceed per-occurrence limit
- **Source**: GeneralInformationValidator.cs, coverage limit comparison logic

**Hierarchy Rule 2: General Aggregate ≥ Product/Completed Operations Aggregate**
- **Business Rule**: General Aggregate must be greater than or equal to Product/Completed Operations Aggregate when Products coverage not excluded
- **Validation Logic**: When Products/Completed Operations coverage included, compare General Aggregate against Products Aggregate
- **Error Condition**: Products coverage included AND General Aggregate < Products Aggregate
- **Error Message**: "General Aggregate limit must be greater than or equal to Product/Completed Operations Aggregate limit"
- **Conditional Logic**: Validation only applies when Products/Completed Operations coverage not excluded
- **Business Rationale**: General Aggregate provides umbrella coverage over all aggregate limits including Products
- **Source**: GeneralInformationValidator.cs, conditional aggregate validation

**Hierarchy Rule 3: Product/Completed Operations Aggregate ≥ Occurrence Liability Limit**
- **Business Rule**: Product/Completed Operations Aggregate must be greater than or equal to Occurrence Liability Limit when Products coverage included
- **Validation Logic**: When Products coverage not excluded, compare Products Aggregate against Occurrence Limit
- **Error Condition**: Products coverage included AND Products Aggregate < Occurrence Limit
- **Error Message**: "Product/Completed Operations Aggregate must be greater than or equal to Occurrence Liability limit"
- **Coverage Integration**: Links with Products/Completed Operations exclusion logic
- **Business Rationale**: Products aggregate must cover individual product liability occurrences
- **Source**: GeneralInformationValidator.cs, products aggregate validation

**Hierarchy Rule 4: Occurrence Liability Limit ≥ Personal and Advertising Injury Limit**
- **Business Rule**: Occurrence Liability Limit must be greater than or equal to Personal and Advertising Injury sublimit
- **Validation Logic**: Compare Occurrence Limit against Personal and Advertising Injury limit selection
- **Error Condition**: Occurrence Limit < Personal and Advertising Injury Limit
- **Error Message**: "Personal and Advertising Injury limit cannot exceed Occurrence Liability limit"
- **Coverage Relationship**: Personal and Advertising Injury is sublimit of General Liability occurrence
- **Business Rationale**: Sublimits cannot exceed primary coverage limits they fall under
- **Source**: GeneralInformationValidator.cs, sublimit validation logic

### 3.2 Enhancement Endorsement Dependencies

**Source**: `CGL_PolicyCoveragesValidator.cs` - Enhancement dependency enforcement

**Enhancement Rule 1: Subrogation Waiver Requires Business Master Enhancement**
- **Business Rule**: Blanket Waiver of Subrogation coverage only available when Business Master Enhancement Endorsement selected
- **Validation Logic**: If Blanket Waiver of Subrogation != "No", then Business Master Enhancement must be selected
- **Error Condition**: Subrogation waiver selected AND Business Master Enhancement not selected
- **Error Message**: "Blanket Waiver of Subrogation requires Business Master Enhancement Endorsement selection"
- **Coverage Dependency**: Subrogation waiver is enhancement feature requiring base enhancement endorsement
- **Business Rationale**: Enhanced subrogation features require broader enhancement endorsement foundation
- **Source**: CGL_PolicyCoveragesValidator.cs, enhancement dependency validation

**Enhancement Rule 2: Enhanced Coverage Features Availability**
- **Business Rule**: Certain coverage features only available with appropriate enhancement endorsements
- **Validation Logic**: Check enhancement endorsement selections against requested coverage features
- **Coverage Dependencies**: Advanced features require corresponding enhancement endorsement selections
- **Error Handling**: Prevent selection of enhancement features without required base endorsements
- **Business Rationale**: Enhanced features have actuarial pricing dependencies on base enhancements
- **Source**: CGL_PolicyCoveragesValidator.cs, feature dependency logic

### 3.3 Employee Benefits Fixed Ratio Requirements

**Source**: `PolicyLevelValidations.cs` - Employee Benefits coverage validation

**Employee Benefits Rule 1: Fixed 3:1 Aggregate to Occurrence Ratio**
- **Business Rule**: Employee Benefits Aggregate Limit must equal exactly 3 times Employee Benefits Occurrence Limit
- **Validation Logic**: Employee Benefits Aggregate = Employee Benefits Occurrence × 3 (exact calculation required)
- **Error Condition**: Employee Benefits Aggregate ≠ (Employee Benefits Occurrence × 3)
- **Error Message**: "Employee Benefits Aggregate must equal 3 times the Occurrence limit (currently [calculated value] required)"
- **Auto-Calculation**: System automatically calculates and sets Aggregate when Occurrence selected
- **Business Rationale**: Actuarial analysis determined optimal 3:1 ratio for Employee Benefits exposure
- **Source**: PolicyLevelValidations.cs, Employee Benefits ratio enforcement

**Employee Benefits Rule 2: Fixed $1,000 Deductible Requirement**
- **Business Rule**: Employee Benefits coverage must have exactly $1,000 deductible (not selectable by user)
- **Validation Logic**: When Employee Benefits selected, deductible automatically set to $1,000
- **Error Condition**: Employee Benefits selected with deductible != $1,000
- **Error Message**: "Employee Benefits deductible is fixed at $1,000"
- **System Behavior**: Deductible automatically populated, no user selection allowed
- **Business Rationale**: Underwriting standards require standardized Employee Benefits deductible
- **Source**: PolicyLevelValidations.cs, fixed deductible enforcement

**Employee Benefits Rule 3: Employee Count Range Validation**
- **Business Rule**: Employee Benefits requires valid employee count between 1-1000 employees
- **Validation Logic**: Employee count field must contain integer value 1 ≤ count ≤ 1000
- **Error Condition**: Employee count < 1 OR Employee count > 1000 OR non-integer value
- **Error Message**: "Employee count must be between 1 and 1000 employees"
- **Field Requirement**: Employee count required when Employee Benefits coverage selected
- **Business Rationale**: Employee count determines exposure base for Employee Benefits premium calculation
- **Source**: PolicyLevelValidations.cs, employee count range validation

**Employee Benefits Rule 4: Occurrence Limit Minimum Requirement**
- **Business Rule**: Employee Benefits Occurrence Limit must be greater than or equal to Policy Occurrence Limit
- **Validation Logic**: Employee Benefits Occurrence ≥ Policy Occurrence Liability Limit
- **Error Condition**: Employee Benefits Occurrence < Policy Occurrence Limit
- **Error Message**: "Employee Benefits Occurrence limit must be at least equal to Policy Occurrence limit"
- **Coverage Relationship**: Employee Benefits cannot have lower occurrence limit than primary policy
- **Business Rationale**: Employee Benefits provides specialized coverage that cannot be less than general coverage
- **Source**: PolicyLevelValidations.cs, Employee Benefits occurrence validation

### 3.4 Mandatory Auto Coverage Synchronization

**Source**: `CGL_PolicyCoveragesValidator.cs` - Auto coverage synchronization rules

**Auto Coverage Rule 1: Hired and Non-Owned Auto Must Match**
- **Business Rule**: Hired Auto coverage and Non-Owned Auto coverage selections must be identical (both selected or both not selected)
- **Validation Logic**: (Hired Auto selected AND Non-Owned Auto selected) OR (Hired Auto not selected AND Non-Owned Auto not selected)
- **Error Condition**: Hired Auto selected XOR Non-Owned Auto selected (exclusive or condition)
- **Error Message**: "Hired Auto and Non-Owned Auto coverages must both be selected or both be unselected"
- **Selection Enforcement**: System automatically synchronizes selections when one is changed
- **Business Rationale**: Underwriting standards require coordinated auto liability coverage for risk management
- **Source**: CGL_PolicyCoveragesValidator.cs, auto coverage synchronization

### 3.5 Deductible All-or-None Validation

**Source**: `GeneralInformationValidator.cs` - Deductible selection validation

**Deductible Rule 1: Complete Deductible Configuration Required**
- **Business Rule**: If any deductible field is completed, then ALL deductible fields (Type, Amount, Basis) must be completed
- **Validation Logic**: (All deductible fields empty) OR (All deductible fields completed)
- **Error Condition**: Some deductible fields completed AND some deductible fields empty
- **Error Message**: "If selecting a deductible, all deductible fields (Type, Amount, Basis) must be completed"
- **Field Dependencies**: Type, Amount, and Basis fields are interdependent requirements
- **Business Rationale**: Complete deductible specification required for proper premium calculation and claim handling
- **Source**: GeneralInformationValidator.cs, all-or-none deductible validation

### 3.6 Liquor Liability Coverage Validation

**Source**: `PolicyLevelValidations.cs` - Liquor Liability business rule enforcement

**Liquor Liability Rule 1: Sales Amount Required When Selected**
- **Business Rule**: When Liquor Liability coverage selected, sales amount must be provided as positive whole number
- **Validation Logic**: Liquor Liability selected → Sales amount required AND Sales amount > 0 AND Sales amount = whole number
- **Error Condition**: Liquor Liability selected AND (Sales amount empty OR Sales amount ≤ 0 OR Sales amount not whole number)
- **Error Message**: "Liquor Liability sales amount required and must be positive whole number"
- **Field Requirement**: Sales amount field conditional on Liquor Liability selection
- **Business Rationale**: Sales volume determines exposure base for Liquor Liability premium calculation
- **Source**: PolicyLevelValidations.cs, liquor sales validation

**Liquor Liability Rule 2: Classification Required When Selected**
- **Business Rule**: When Liquor Liability coverage selected, business classification must be specified from approved list
- **Validation Logic**: Liquor Liability selected → Business classification required from dropdown options
- **Error Condition**: Liquor Liability selected AND business classification not selected
- **Error Message**: "Liquor Liability business classification required"
- **Classification Options**: Manufacturer/Wholesalers, Restaurants/Hotels, Package Stores, Clubs
- **Business Rationale**: Business type determines appropriate Liquor Liability coverage scope and premium
- **Source**: PolicyLevelValidations.cs, liquor classification validation

**Liquor Liability Rule 3: Occurrence Limit Minimum Requirement**
- **Business Rule**: Liquor Liability Occurrence Limit must be greater than or equal to Policy Occurrence Limit
- **Validation Logic**: Liquor Liability Occurrence ≥ Policy Occurrence Liability Limit
- **Error Condition**: Liquor Liability Occurrence < Policy Occurrence Limit
- **Error Message**: "Liquor Liability Occurrence limit must be at least equal to Policy Occurrence limit"
- **Coverage Relationship**: Specialized coverage cannot have lower limits than general policy coverage
- **Business Rationale**: Liquor Liability provides additional coverage that supplements (not replaces) general coverage
- **Source**: PolicyLevelValidations.cs, liquor occurrence validation

---

## 4. UI/UX Requirements ⭐ MANDATORY

### 4.1 Auto-Display/Hide Behaviors

**Pattern Description:**
The validation framework provides real-time feedback through dynamic error message display, field highlighting, and user guidance appearing as coverage selections are made. Validation messages appear immediately when rule violations occur and disappear when issues are resolved.

**Real-time Validation Display:**
```
Validation Trigger: Coverage limit selection changes, field input changes, checkbox selections
Error Display: Red error messages appear below violating fields immediately
Success Behavior: Error messages disappear when validation rules are satisfied
Progressive Validation: Simple field validation → business rule validation → complex relationship validation
Source: GeneralInformationValidator.cs, CGL_PolicyCoveragesValidator.cs, real-time validation events
```

**Conditional Field Dependencies:**
```
Employee Benefits Selection: When selected, employee count field appears with range 1-1000
Deductible Selection: When any deductible field completed, all deductible fields become required
Liquor Liability Selection: When selected, sales amount and classification fields appear
Enhancement Dependencies: Subrogation options appear only when Business Master Enhancement selected
Source: PolicyLevelValidations.cs, conditional field display logic
```

### 4.2 Text Input Specifications

**Field Specifications:**

| Field Name | Label | Type | Character Limit | Required | Default |
|------------|-------|------|-----------------|----------|---------|
| Occurrence Liability Limit | "Occurrence Liability Limit" | Dropdown | N/A | Yes | Lowest Available |
| General Aggregate | "General Aggregate" | Dropdown | N/A | Yes | Auto-calculated minimum |
| Personal and Advertising Injury | "Personal and Advertising Injury" | Dropdown | N/A | Yes | Match Occurrence |
| Product/Completed Operations Aggregate | "Product/Completed Operations Aggregate" | Dropdown | N/A | Conditional | Auto-calculated |
| Employee Count | "Number of Employees" | Integer Input | 4 digits | When EB Selected | Empty |
| Liquor Sales Amount | "Annual Liquor Sales ($)" | Integer Input | 10 digits | When LL Selected | Empty |
| Deductible Type | "Deductible Type" | Dropdown | N/A | When Any Deductible | None Selected |
| Deductible Amount | "Deductible Amount" | Dropdown | N/A | When Any Deductible | None Selected |
| Deductible Basis | "Deductible Basis" | Dropdown | N/A | When Any Deductible | None Selected |

**Auto-Calculation Display Logic:**
- **General Aggregate Minimum**: Automatically displays minimum value based on Occurrence Limit selection
- **Employee Benefits Aggregate**: Automatically calculates and displays (Occurrence × 3) when Occurrence selected
- **Products Aggregate Minimum**: Displays minimum based on Occurrence Limit when Products coverage included

### 4.3 Validation Visual Indicators

**Error States:**

**Coverage Limit Hierarchy Violations:**
- **Visual**: Red error message below violating limit field with specific relationship explanation
- **Error Message**: "General Aggregate limit must be greater than or equal to Occurrence Liability limit"
- **Icon**: Red exclamation icon next to invalid field
- **Trigger**: Real-time when limit selections violate hierarchy rules
- **Auto-Correction**: System suggests valid options in dropdown when possible

**Enhancement Dependency Violations:**
- **Visual**: Red error message below dependent field with requirement explanation
- **Error Message**: "Blanket Waiver of Subrogation requires Business Master Enhancement Endorsement selection"
- **Behavior**: Dependent field disabled until requirement satisfied
- **Trigger**: Selection of dependent feature without required base enhancement
- **Resolution Guidance**: Clear instruction on required prerequisite selection

**Employee Benefits Validation Errors:**
- **Visual**: Red border around employee count field, red error message below
- **Error Messages**: 
  - "Employee count must be between 1 and 1000 employees"
  - "Employee Benefits Aggregate must equal 3 times the Occurrence limit"
- **Auto-Calculation Display**: Shows calculated aggregate value "(Employee Benefits Occurrence × 3 = $X)"
- **Trigger**: Invalid employee count or ratio mismatch detection

**Auto Coverage Synchronization Errors:**
- **Visual**: Red error message spanning both Hired and Non-Owned Auto fields
- **Error Message**: "Hired Auto and Non-Owned Auto coverages must both be selected or both be unselected"
- **Auto-Correction**: System offers "Select Both" or "Deselect Both" buttons for quick resolution
- **Highlight Behavior**: Both auto coverage fields highlighted until synchronized

**Success States:**
- **Visual**: Green checkmark icons next to validated fields
- **Message**: Brief confirmation message for complex validations ("Coverage limits validated")
- **Behavior**: Error indicators disappear, green success indicators appear briefly

### 4.4 Interactive Elements

**Auto-Correction Features:**
- **Minimum Value Suggestions**: Dropdowns automatically filter to show only valid options based on other selections
- **Auto-Calculate Buttons**: "Calculate Minimum" buttons for complex relationship calculations
- **Synchronization Buttons**: "Match Coverage" buttons for fields requiring synchronization
- **Enhancement Helpers**: "Select Required Enhancement" links for dependency resolution

**Validation Helper Tools:**
- **Coverage Limit Calculator**: Tool showing current hierarchy relationships and requirements
- **Enhancement Dependency Checker**: Visual display of enhancement relationships and requirements
- **Employee Benefits Calculator**: Real-time calculation display for aggregate requirements

**Progressive Validation Display:**
- **Field-Level Validation**: Immediate feedback on individual field requirements
- **Section-Level Validation**: Validation summary for coverage sections
- **Quote-Level Validation**: Comprehensive validation summary before quote generation

### 4.5 Accessibility Requirements

- **ARIA Labels**: All validation error messages properly associated with related form fields
- **Keyboard Navigation**: All validation resolution features accessible via keyboard navigation
- **Screen Reader Support**: Validation error messages announced immediately when they appear
- **Focus Management**: Focus automatically moves to fields requiring correction
- **Color Independence**: Validation errors indicated by text and icons, not color alone
- **High Contrast**: Error indicators meet WCAG 2.1 AA contrast requirements

### 4.6 Responsive Design Requirements

- **Mobile Devices**: Validation messages stack vertically below fields, auto-correction tools accessible via touch
- **Tablets**: Validation messages display adjacent to fields when space allows, touch-friendly correction tools
- **Desktop**: Full validation message display with inline auto-correction features
- **Browser Compatibility**: Validation features function across Chrome, Firefox, Safari, Edge, IE11
- **Performance**: Validation feedback appears within 0.5 seconds of triggering action

---

## 5. Validation Rules and Business Logic ⭐ MANDATORY

### 5.1 Client-Side Validation (JavaScript)

**Function: ValidateCoverageLimitHierarchy()**
- **Purpose**: Real-time validation of coverage limit relationships and hierarchy rules
- **Trigger**: OnChange events for all coverage limit dropdown selections
- **Logic**: 
  1. Compare General Aggregate against Occurrence Liability Limit
  2. Compare General Aggregate against Product/Completed Operations Aggregate (when applicable)
  3. Compare Product/Completed Operations Aggregate against Occurrence Limit (when applicable)
  4. Compare Occurrence Limit against Personal and Advertising Injury Limit
- **Error Messages**: Specific hierarchy violation messages for each relationship
- **Visual Feedback**: Red error messages, field highlighting, auto-correction suggestions
- **Source**: GeneralInformationValidator.cs validation logic converted to JavaScript

**Function: ValidateEmployeeBenefitsRules()**
- **Purpose**: Enforce Employee Benefits coverage business rules and calculations
- **Trigger**: Employee Benefits selection, employee count changes, occurrence limit changes
- **Logic**:
  1. Validate employee count range (1-1000)
  2. Calculate and validate Aggregate = Occurrence × 3
  3. Enforce $1,000 fixed deductible
  4. Validate occurrence limit ≥ policy occurrence limit
- **Error Messages**: 
  - "Employee count must be between 1 and 1000 employees"
  - "Employee Benefits Aggregate must equal 3 times the Occurrence limit"
- **Auto-Calculation**: Automatically calculates and displays aggregate value
- **Source**: PolicyLevelValidations.cs Employee Benefits validation

**Function: ValidateAutoCoverageSynchronization()**
- **Purpose**: Enforce Hired Auto and Non-Owned Auto coverage synchronization requirement
- **Trigger**: OnChange events for Hired Auto or Non-Owned Auto checkboxes
- **Logic**: Ensure (Hired Auto AND Non-Owned Auto) OR (NOT Hired Auto AND NOT Non-Owned Auto)
- **Error Message**: "Hired Auto and Non-Owned Auto coverages must both be selected or both be unselected"
- **Auto-Correction**: Provides "Select Both" or "Deselect Both" resolution options
- **Source**: CGL_PolicyCoveragesValidator.cs auto coverage validation

**Function: ValidateEnhancementDependencies()**
- **Purpose**: Enforce enhancement endorsement dependency requirements
- **Trigger**: Enhancement endorsement selections, dependent feature selections
- **Logic**: Check that dependent features have required base endorsements selected
- **Error Message**: "Blanket Waiver of Subrogation requires Business Master Enhancement Endorsement selection"
- **Dependency Resolution**: Auto-highlight required endorsement selections
- **Source**: CGL_PolicyCoveragesValidator.cs enhancement dependency validation

**Function: ValidateDeductibleAllOrNone()**
- **Purpose**: Enforce all-or-none deductible field completion requirement
- **Trigger**: OnChange events for deductible type, amount, or basis fields
- **Logic**: (All deductible fields empty) OR (All deductible fields completed)
- **Error Message**: "If selecting a deductible, all deductible fields (Type, Amount, Basis) must be completed"
- **Visual Feedback**: Highlight incomplete deductible fields, show completion requirements
- **Source**: GeneralInformationValidator.cs deductible validation

### 5.2 Coverage Limit Hierarchy Validation

**Hierarchy Validation Rules:**

| Validation Rule | Comparison | Error Condition | Error Message |
|-----------------|------------|-----------------|---------------|
| General Aggregate ≥ Occurrence | GA ≥ OL | GA < OL | "General Aggregate limit must be greater than or equal to Occurrence Liability limit" |
| General Aggregate ≥ Products Aggregate | GA ≥ PA | GA < PA AND Products included | "General Aggregate limit must be greater than or equal to Product/Completed Operations Aggregate limit" |
| Products Aggregate ≥ Occurrence | PA ≥ OL | PA < OL AND Products included | "Product/Completed Operations Aggregate must be greater than or equal to Occurrence Liability limit" |
| Occurrence ≥ Personal Injury | OL ≥ PI | OL < PI | "Personal and Advertising Injury limit cannot exceed Occurrence Liability limit" |

**Conditional Hierarchy Logic:**
- **Products Coverage Validation**: Only applies when Products/Completed Operations coverage not excluded
- **Personal Injury Validation**: Always applies as Personal Injury is standard sublimit
- **Auto-Correction Logic**: System suggests minimum valid values in dropdowns based on other selections
- **Progressive Validation**: Validates immediate relationships first, then complex multi-field relationships

### 5.3 Business Rule Validation

**Rule 1: Employee Benefits 3:1 Ratio Enforcement**
- **Description**: Employee Benefits Aggregate must equal exactly 3 times Employee Benefits Occurrence
- **Validation Logic**: EB_Aggregate = EB_Occurrence × 3 (exact equality required)
- **Error Handling**: Display calculated requirement value, auto-populate correct aggregate
- **Business Rationale**: Actuarial pricing model requires fixed 3:1 ratio for Employee Benefits
- **Source**: PolicyLevelValidations.cs, Employee Benefits ratio validation

**Rule 2: Enhancement Endorsement Dependencies**
- **Description**: Certain coverage features require base enhancement endorsements to be selected
- **Validation Logic**: Dependent feature selected → Required base endorsement must be selected
- **Error Handling**: Disable dependent features until requirements met, clear dependency messaging
- **Business Rationale**: Enhanced features have underwriting dependencies on base endorsement coverage
- **Source**: CGL_PolicyCoveragesValidator.cs, enhancement dependency logic

**Rule 3: Auto Coverage Synchronization Requirement**
- **Description**: Hired Auto and Non-Owned Auto coverages must be selected or deselected together
- **Validation Logic**: (Hired Auto XOR Non-Owned Auto) = FALSE (exclusive or must be false)
- **Error Handling**: Synchronization buttons, clear messaging about required coordination
- **Business Rationale**: Underwriting standards require coordinated auto liability coverage
- **Source**: CGL_PolicyCoveragesValidator.cs, auto synchronization validation

**Rule 4: Liquor Liability Coverage Requirements**
- **Description**: Liquor Liability coverage requires sales amount, classification, and appropriate limits
- **Validation Logic**: Liquor selected → (Sales > 0 AND Classification selected AND Occurrence ≥ Policy Occurrence)
- **Error Handling**: Conditional field requirements, range validation, limit hierarchy enforcement
- **Business Rationale**: Liquor Liability pricing and coverage require complete exposure information
- **Source**: PolicyLevelValidations.cs, liquor liability validation

**Rule 5: Complete Deductible Specification**
- **Description**: Deductible selection requires all deductible fields (Type, Amount, Basis) to be completed
- **Validation Logic**: Any deductible field completed → All deductible fields required
- **Error Handling**: Highlight incomplete fields, show completion requirements, clear all-or-none messaging
- **Business Rationale**: Complete deductible specification required for premium calculation and claim handling
- **Source**: GeneralInformationValidator.cs, deductible all-or-none validation

### 5.4 Server-Side Validation

**Security Validations:**
- **Input Sanitization**: All numeric inputs sanitized and validated for appropriate ranges
- **SQL Injection Prevention**: Parameterized queries for validation rule data access
- **Business Rule Integrity**: Server-side re-validation of all client-side validation rules
- **Data Consistency**: Cross-field validation to ensure data integrity throughout quote object

**Data Integrity Checks:**
- **Coverage Limit Consistency**: Server-side verification of all coverage limit hierarchy relationships
- **Enhancement Dependency Verification**: Server-side confirmation of enhancement endorsement dependencies
- **Premium Calculation Validation**: Verification that coverage selections align with premium calculations
- **Regulatory Compliance**: Server-side validation of state-specific coverage requirements and limits

---

## 6. User Stories and Acceptance Criteria

### US-CGL-VAL-001: Validate Coverage Limit Hierarchies

**As an** Insurance Agent  
**I need to** receive immediate feedback when coverage limits violate hierarchy requirements  
**So that** I can configure valid coverage limits that meet underwriting standards

**Acceptance Criteria:**
1. Given I select an Occurrence Liability Limit, when I select a General Aggregate lower than the Occurrence, then I receive an error message "General Aggregate limit must be greater than or equal to Occurrence Liability limit"
2. Given I have Products coverage included, when I select a General Aggregate lower than Products Aggregate, then I receive a products-specific hierarchy error message
3. Given I select Personal and Advertising Injury limit higher than Occurrence, when the selection is made, then I receive a sublimit error message
4. Given I correct a coverage limit hierarchy violation, when the correction is made, then the error message disappears immediately
5. Given coverage limits are properly configured, when validation occurs, then green success indicators appear briefly

**Priority**: High  
**Complexity**: Large  
**Dependencies**: None (core validation functionality)

### US-CGL-VAL-002: Enforce Employee Benefits Fixed Ratios

**As an** Insurance Agent  
**I need to** have Employee Benefits Aggregate automatically calculated at 3 times Occurrence  
**So that** Employee Benefits coverage meets actuarial requirements and pricing accuracy

**Acceptance Criteria:**
1. Given I select Employee Benefits coverage, when I select an Employee Benefits Occurrence limit, then the Aggregate automatically calculates to exactly 3 times the Occurrence
2. Given Employee Benefits is selected, when I enter an employee count outside 1-1000 range, then I receive a range validation error message
3. Given Employee Benefits Occurrence is selected, when the system calculates Aggregate, then it displays "(Employee Benefits Occurrence × 3 = $X)" for transparency
4. Given Employee Benefits coverage is configured, when I review the coverage, then the deductible is automatically set to $1,000 with no user selection required
5. Given Employee Benefits Occurrence is less than Policy Occurrence, when validation occurs, then I receive an error requiring Employee Benefits Occurrence ≥ Policy Occurrence

**Priority**: High  
**Complexity**: Medium  
**Dependencies**: Coverage limit hierarchy validation (US-CGL-VAL-001)

### US-CGL-VAL-003: Synchronize Auto Coverage Selections

**As an** Insurance Agent  
**I need to** have Hired Auto and Non-Owned Auto coverages synchronized automatically  
**So that** coverage meets underwriting requirements for coordinated auto liability

**Acceptance Criteria:**
1. Given I select Hired Auto coverage, when the selection is made, then Non-Owned Auto coverage is automatically selected
2. Given I deselect Hired Auto coverage, when the deselection is made, then Non-Owned Auto coverage is automatically deselected
3. Given I have only one auto coverage selected, when validation occurs, then I receive error message "Hired Auto and Non-Owned Auto coverages must both be selected or both be unselected"
4. Given I have mismatched auto coverage selections, when the error appears, then I see "Select Both" and "Deselect Both" resolution buttons
5. Given I click a resolution button, when the action completes, then both auto coverages are properly synchronized and error disappears

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: None (independent validation rule)

### US-CGL-VAL-004: Validate Enhancement Dependencies

**As an** Insurance Agent  
**I need to** receive guidance when selecting enhancement features that require base endorsements  
**So that** I understand coverage dependencies and configure valid enhancement combinations

**Acceptance Criteria:**
1. Given I attempt to select Blanket Waiver of Subrogation without Business Master Enhancement, when the selection is attempted, then I receive dependency error message
2. Given enhancement dependency errors exist, when I view the error, then I see clear instruction "Blanket Waiver of Subrogation requires Business Master Enhancement Endorsement selection"
3. Given I select the required base enhancement, when the selection is made, then dependent enhancement features become available
4. Given all enhancement dependencies are satisfied, when I review selections, then all chosen enhancements are properly enabled
5. Given I deselect a required base enhancement, when the deselection occurs, then dependent features are automatically disabled with user notification

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: Enhancement selection functionality

### US-CGL-VAL-005: Enforce Complete Deductible Specification

**As an** Insurance Agent  
**I need to** complete all deductible fields when selecting any deductible option  
**So that** deductible specifications are complete for premium calculation and claim handling

**Acceptance Criteria:**
1. Given I select a deductible type without completing amount and basis, when validation occurs, then I receive "all deductible fields must be completed" error message
2. Given I complete deductible amount without type and basis, when validation occurs, then I receive the all-or-none error message
3. Given I have partial deductible information, when the error appears, then incomplete fields are highlighted with red borders
4. Given I complete all three deductible fields, when validation occurs, then error messages disappear and deductible configuration is accepted
5. Given I clear all deductible fields, when validation occurs, then no deductible errors appear (all-empty state is valid)

**Priority**: Medium  
**Complexity**: Small  
**Dependencies**: None (independent validation rule)

### US-CGL-VAL-006: Validate Liquor Liability Requirements

**As an** Insurance Agent  
**I need to** provide complete information when selecting Liquor Liability coverage  
**So that** Liquor Liability coverage is properly configured with accurate exposure information

**Acceptance Criteria:**
1. Given I select Liquor Liability coverage, when the selection is made, then sales amount and business classification fields appear as required
2. Given I enter a negative or zero sales amount, when validation occurs, then I receive "sales amount must be positive whole number" error message
3. Given I select Liquor Liability without choosing business classification, when validation occurs, then I receive "business classification required" error message
4. Given I select Liquor Liability Occurrence less than Policy Occurrence, when validation occurs, then I receive occurrence minimum requirement error
5. Given I complete all Liquor Liability requirements correctly, when validation occurs, then coverage is accepted and integrated into quote

**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: Coverage limit hierarchy validation (US-CGL-VAL-001)

### US-CGL-VAL-007: Provide Real-time Validation Feedback

**As an** Insurance Agent  
**I need to** receive immediate validation feedback as I make coverage selections  
**So that** I can resolve issues quickly without waiting for form submission

**Acceptance Criteria:**
1. Given I make any coverage limit selection, when the selection changes, then validation occurs within 0.5 seconds
2. Given validation errors exist, when they appear, then error messages are specific to the violation and provide clear resolution guidance
3. Given I resolve a validation error, when the correction is made, then error indicators disappear immediately
4. Given multiple validation errors exist, when displayed, then errors are prioritized with most critical issues shown first
5. Given validation passes completely, when all rules are satisfied, then brief success indicators confirm proper configuration

**Priority**: High  
**Complexity**: Large  
**Dependencies**: All other validation user stories (comprehensive validation system)

### US-CGL-VAL-008: Handle Complex Multi-Field Validations

**As an** Insurance Agent  
**I need to** receive coordinated validation feedback for complex business rules involving multiple fields  
**So that** I can understand and resolve sophisticated validation requirements efficiently

**Acceptance Criteria:**
1. Given I have coverage configurations affecting multiple fields, when validation occurs, then related field requirements are clearly explained
2. Given I have Employee Benefits with invalid employee count and ratio issues, when validation occurs, then both issues are clearly identified with resolution guidance
3. Given I have enhancement dependency violations, when displayed, then I see both the dependent feature and required base enhancement clearly identified
4. Given complex validations are resolved, when corrections are made, then all related validation indicators update appropriately
5. Given I use auto-correction features, when applied, then all related fields are updated consistently and additional validation issues are prevented

**Priority**: Medium  
**Complexity**: Large  
**Dependencies**: All specific validation rules (requires comprehensive validation framework)

---

## 7. Testing Requirements

### 7.1 Functional Testing

**Test Scenario 1: Coverage Limit Hierarchy Validation**
- **Setup**: CGL coverage selection interface with all coverage limit dropdowns available
- **Steps**:
  1. Select Occurrence Liability Limit of $1M
  2. Attempt to select General Aggregate of $500K (less than Occurrence)
  3. Verify hierarchy error message appears immediately
  4. Change General Aggregate to $2M (greater than Occurrence)
  5. Confirm error message disappears and selection is accepted
- **Expected Result**: Immediate validation feedback with specific hierarchy error messages, proper error resolution

**Test Scenario 2: Employee Benefits Fixed Ratio Enforcement**
- **Setup**: Employee Benefits coverage selection with occurrence and aggregate fields
- **Steps**:
  1. Select Employee Benefits coverage
  2. Select Employee Benefits Occurrence of $1M
  3. Verify Aggregate automatically calculates to $3M (3 × $1M)
  4. Enter employee count of 1500 (exceeds maximum)
  5. Verify employee count range error appears
  6. Change employee count to 500 (valid range)
  7. Confirm all Employee Benefits validations pass
- **Expected Result**: Automatic 3:1 ratio calculation, employee count validation, $1K deductible auto-assignment

**Test Scenario 3: Auto Coverage Synchronization**
- **Setup**: Hired Auto and Non-Owned Auto coverage checkboxes
- **Steps**:
  1. Select only Hired Auto coverage (leave Non-Owned Auto unselected)
  2. Verify synchronization error message appears
  3. Click "Select Both" resolution button
  4. Confirm both auto coverages are now selected and error disappears
  5. Deselect Hired Auto coverage
  6. Verify Non-Owned Auto automatically deselects
- **Expected Result**: Synchronization enforcement with resolution tools, automatic coordination

**Test Scenario 4: Enhancement Dependency Validation**
- **Setup**: Enhancement endorsement selections and dependent feature options
- **Steps**:
  1. Attempt to select Blanket Waiver of Subrogation without Business Master Enhancement
  2. Verify dependency error message appears
  3. Select Business Master Enhancement Endorsement
  4. Confirm Blanket Waiver of Subrogation becomes available
  5. Deselect Business Master Enhancement
  6. Verify dependent features are disabled with user notification
- **Expected Result**: Clear dependency relationships with proper error messaging and feature availability control

### 7.2 UI Behavior Testing

**Real-time Validation Testing:**
- Verify all validation occurs within 0.5 seconds of triggering action
- Test error message appearance and disappearance timing
- Validate visual indicators (red borders, icons, success indicators)
- Confirm auto-correction suggestions and resolution tools function properly

**Multi-Field Validation Testing:**
- Test complex validations involving multiple interdependent fields
- Verify validation message prioritization and clarity
- Test progressive validation from simple field validation to complex business rules
- Confirm proper validation state management across form sections

### 7.3 Cross-Browser Testing

Test comprehensive validation functionality on:
- **Chrome (latest version)**: Primary VelociRater browser platform
- **Firefox (latest version)**: Secondary browser validation
- **Safari (latest version)**: Mac platform compatibility
- **Edge (latest version)**: Windows platform default browser
- **IE11**: Legacy browser support if required

### 7.4 Performance Testing

- **Validation Response Time**: All validation feedback appears within 0.5 seconds
- **Complex Rule Processing**: Multi-field business rule validation completes within 1 second
- **Auto-Correction Performance**: Resolution suggestions and tools respond immediately
- **Form Submission Validation**: Complete validation pass completes within 2 seconds
- **Real-time Calculation**: Employee Benefits ratio calculations update immediately

### 7.5 Business Rule Accuracy Testing

**Coverage Limit Hierarchy Testing:**
- Test all coverage limit combinations for proper hierarchy enforcement
- Verify Products coverage conditional logic works correctly
- Test sublimit validation accuracy across all limit options

**Business Rule Logic Testing:**
- Verify Employee Benefits 3:1 ratio calculation accuracy across all occurrence limit options
- Test enhancement dependency relationships comprehensively
- Validate auto coverage synchronization in all selection scenarios
- Test deductible all-or-none logic with various completion patterns

---

## 8. Migration and Modernization Considerations

### 8.1 Data Migration

**Current Validation Architecture**: Multi-file validation system with GeneralInformationValidator.cs, CGL_PolicyCoveragesValidator.cs, PolicyLevelValidations.cs
**Migration Requirements**: Preserve all business rule logic, validation relationships, and error messaging accuracy
**Rule Preservation**: Maintain exact validation rule specifications and business logic calculations
**Error Message Migration**: Preserve specific error message text and user guidance content

### 8.2 Configuration Migration

**Business Rule Configuration**: Migrate all validation rule parameters (ranges, ratios, dependencies)
**Validation Trigger Points**: Preserve real-time validation behavior and form submission validation
**Auto-Correction Logic**: Migrate suggestion algorithms and resolution tool functionality
**State-Specific Rules**: Maintain state-specific validation variations and regulatory requirements

### 8.3 Integration Impact

**Quote Object Integration**: Ensure validation results properly integrate with quote data structure
**Premium Calculation Integration**: Maintain validation rule coordination with premium calculation logic
**Coverage Selection Integration**: Preserve validation framework coordination with coverage selection workflow
**Enhancement Integration**: Maintain validation coordination with enhancement endorsement selection

### 8.4 Rollback Strategy

**Validation Logic Preservation**: Maintain backup of current validation class implementations
**Business Rule Documentation**: Preserve complete business rule specifications for rollback reference
**Error Message Archive**: Maintain current error message text and logic for restoration if needed
**Performance Baseline**: Document current validation performance metrics for comparison

---

## 9. Source Attribution and Traceability

### 9.1 Source Code Files Analyzed

| File Path | Purpose | Lines Analyzed |
|-----------|---------|----------------|
| GeneralInformationValidator.cs | Coverage limit hierarchy validation | Complete file |
| CGL_PolicyCoveragesValidator.cs | Enhancement dependencies, auto synchronization | Complete file |
| PolicyLevelValidations.cs | Employee Benefits, Liquor Liability validation | Complete file |

### 9.2 Key Business Rules and Validation Methods

| Validation Rule | Source File | Key Logic |
|-----------------|-------------|-----------|
| Coverage Limit Hierarchy | GeneralInformationValidator.cs | General Aggregate ≥ Occurrence, Products Aggregate relationships |
| Employee Benefits 3:1 Ratio | PolicyLevelValidations.cs | Aggregate = Occurrence × 3, $1K deductible |
| Auto Coverage Synchronization | CGL_PolicyCoveragesValidator.cs | Hired Auto ⟷ Non-Owned Auto coordination |
| Enhancement Dependencies | CGL_PolicyCoveragesValidator.cs | Subrogation waiver requires Business Master Enhancement |
| Deductible All-or-None | GeneralInformationValidator.cs | Type, Amount, Basis all required when any selected |
| Liquor Liability Requirements | PolicyLevelValidations.cs | Sales amount, classification, occurrence minimum |

### 9.3 Traceability Matrix

| Requirement ID | Source Code Reference | Validation |
|----------------|----------------------|------------|
| Coverage Limit Hierarchy | GeneralInformationValidator.cs | US-CGL-VAL-001 |
| Employee Benefits Rules | PolicyLevelValidations.cs | US-CGL-VAL-002 |
| Auto Coverage Sync | CGL_PolicyCoveragesValidator.cs | US-CGL-VAL-003 |
| Enhancement Dependencies | CGL_PolicyCoveragesValidator.cs | US-CGL-VAL-004 |
| Deductible Validation | GeneralInformationValidator.cs | US-CGL-VAL-005 |
| Liquor Liability Rules | PolicyLevelValidations.cs | US-CGL-VAL-006 |
| Real-time Feedback | All validation files | US-CGL-VAL-007 |
| Complex Multi-Field | All validation files | US-CGL-VAL-008 |

---

## 10. Document Metadata

**Prepared By**: Mason (IFI Requirements Extraction Specialist)  
**Reviewed By**: Vera (IFI Quality Validator) - Pending  
**Approved By**: [IFI Technical Authority] - Pending  
**Document Location**: `//project/ifm/product_requirements/CGL/Coverage_Validation_Framework/Modernization_CGL_CoverageValidation.md`

**Analysis Source**: Rex (IFI Pattern Miner) - CGL Comprehensive System Analysis  
**Architecture Input**: Aria (IFI Architect) - Pending  
**Domain Validation**: Rita (IFI Insurance Specialist) - Pending  
**Orchestration**: Douglas (IFI Orchestrator) - Delegation In Progress

**Rex Analysis Source**: `//project/ifm/meta/rex/cgl_comprehensive_system_analysis/cgl_complete_lob_patterns.md`

**Token Budget Used**: 15.5K / 25K tokens

---

**END OF REQUIREMENTS DOCUMENT**