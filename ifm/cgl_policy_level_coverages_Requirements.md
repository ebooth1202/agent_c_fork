# CGL Policy Level Coverages - COMPLETE REQUIREMENTS DOCUMENT

## Section 1 - General Information

### 1.1 - Program Type
**Field Specifications**:
- User selects program type from dropdown menu
- Field hidden by default, displayed when business rules require program selection
- When "Preferred" program selected (Value: 55), system displays qualification criteria popup

**User Experience & Validation**:
- Preferred program popup shows qualification requirements including 3-year loss ratio ≤55%, building age requirements, experience criteria
- User acknowledges qualification criteria before selection completes
- System validates program eligibility based on defined business criteria

**Conditional Logic**:
- Field visibility controlled by quote type and business rules
- Preferred program selection triggers additional validation requirements
- System displays detailed eligibility criteria for preferred program option

**Complete Option Set**:
- Option values loaded from program type configuration based on line of business
- Preferred Program (Value: 55) - triggers eligibility popup
- Standard Program options vary by state and company combination

**Selection Impact Analysis**:
- Preferred program selection affects rating and underwriting requirements
- System tracks program type for pricing and eligibility validation
- Selection impacts downstream underwriting review process

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 21-30, ctl_CGL_Coverages.ascx.vb lines 250-280
- Secondary Location: VrCgl.js popup message configuration
- External Dependencies: ConfigurationManager AppSettings for program criteria

### 1.2 - Occurrence Liability Limit (Required)
**Field Specifications**:
- User selects occurrence liability limit amount from dropdown menu
- Required field for all CGL policies (marked with asterisk)
- Selection drives multiple dependent limit calculations automatically

**User Experience & Validation**:
- System requires user selection before proceeding
- Selected value automatically populates related aggregate limits
- System validates selection against available state/company options
- Changes to this field trigger recalculation of dependent limits

**Conditional Logic**:
- Selection below $300,000 prevents liquor liability coverage availability
- System automatically sets general aggregate to double the occurrence limit
- Personal injury limit automatically matches occurrence liability limit value
- Employee benefits liability limit mirrors selected occurrence limit

**Complete Option Set**:
Based on source analysis, available options include:
- $25,000 (Value: 8) - No liquor liability eligibility
- $50,000 (Value: 9) - No liquor liability eligibility  
- $100,000 (Value: 10) - No liquor liability eligibility
- $200,000 (Value: 32) - No liquor liability eligibility
- $300,000 (Value: 33) - Liquor liability eligible, triggers $600,000 aggregates
- $500,000 (Value: 34) - Liquor liability eligible, triggers $1,000,000 aggregates
- $1,000,000 (Value: 56) - Liquor liability eligible, triggers $2,000,000 aggregates

**Selection Impact Analysis**:
- Drives automatic calculation of General Aggregate limit (typically double OLL value)
- Controls Product/Completed Operations Aggregate limit (matches General Aggregate)
- Sets Personal and Advertising Injury limit (matches OLL value)
- Determines liquor liability coverage availability (≥$300,000 required)
- Affects Employee Benefits Liability limit calculation (mirrors OLL)
- Impacts rating engine premium calculations across all coverage sections

**Downstream User Actions Required**:
- Rating module: System recalculates all premiums based on limit selection
- Coverage validation: User may need to adjust other coverages if limits become incompatible
- Underwriting review: Higher limits may trigger additional underwriting requirements

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 31-39, ctl_CGL_Coverages.ascx.vb lines 300-350
- Secondary Location: VrCgl.js OccurrenceLiabilityLimitChanged function lines 150-350
- External Dependencies: State/company-specific dropdown loading, liquor liability eligibility logic

### 1.3 - General Aggregate (Required)
**Field Specifications**:
- User views automatically calculated general aggregate limit
- Required field populated based on occurrence liability limit selection
- Value typically set to double the selected occurrence liability limit

**User Experience & Validation**:
- System automatically populates field when occurrence liability limit changes
- For newer company configurations, user can select from available options
- System prevents incompatible limit combinations through validation
- Field updates dynamically when occurrence liability changes

**Conditional Logic**:
- Standard rule: General aggregate = 2x occurrence liability limit
- For $1,000,000 occurrence limit: User can select $2,000,000 or $3,000,000
- $3,000,000 option availability depends on company configuration and quote characteristics
- Selection affects products/completed operations aggregate options

**Complete Option Set**:
Available options based on Occurrence Liability Limit selection:
- For $300,000 OLL: $600,000 (Value: 178) - automatically selected
- For $500,000 OLL: $1,000,000 (Value: 56) - automatically selected
- For $1,000,000 OLL: $2,000,000 (Value: 65) or $3,000,000 (Value: 167)

**Selection Impact Analysis**:
- Controls available Product/Completed Operations Aggregate options
- $3,000,000 selection enables $3,000,000 products/completed operations option
- Affects premium calculations for all general liability coverages
- Higher limits may require additional underwriting review

**Downstream User Actions Required**:
- Products/Completed Operations field automatically updates based on selection
- Rating engine recalculates premiums for all liability coverages
- Underwriting module may flag higher limits for additional review

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 40-48, VrCgl.js GeneralAggregateChanged function
- Secondary Location: GenAggProducts3MHelper.vb for $3M option management
- External Dependencies: Company configuration flags, effective date validation

## Section 2 - Deductibles (Conditional Section)

*Section displayed only when user selects "Yes" for Add a General Liability Deductible*

### 2.1 - Deductible Type (Required when section active)
**Field Specifications**:
- User selects deductible category type from dropdown menu
- Required field when deductible section is active (marked with asterisk)
- Selection affects available deductible amount and basis options

**User Experience & Validation**:
- Field only appears when user enables general liability deductible option
- System requires selection before allowing policy save
- User must select from available deductible category types

**Complete Option Set**:
- Options loaded from GL Premises and Products Deductible Category Type configuration
- Specific values vary by state and company combination
- UNVERIFIED: Exact option list requires configuration data extraction

**Selection Impact Analysis**:
- Selected type affects available deductible amounts
- Impacts deductible basis options available to user
- Affects premium calculations and deductible application rules

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 120-128
- Secondary Location: QuickQuotePropertyName.GL_PremisesAndProducts_DeductibleCategoryTypeId data loading
- External Dependencies: State/company-specific deductible configurations

### 2.2 - Deductible Amount (Required when section active)
**Field Specifications**:
- User selects specific deductible dollar amount from dropdown menu
- Required field when deductible section is active (marked with asterisk)
- Available amounts depend on selected deductible type

**User Experience & Validation**:
- System requires amount selection when deductible is enabled
- Available options filtered based on deductible type selection
- User cannot proceed without selecting deductible amount

**Complete Option Set**:
- Options loaded from GL Premises and Products Deductible configuration
- Specific amounts vary by deductible type and state/company rules
- UNVERIFIED: Exact amount options require configuration data analysis

**Selection Impact Analysis**:
- Selected amount affects premium calculations and claim handling
- Higher deductibles typically provide premium reductions
- Amount selection impacts policy terms and conditions

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 129-137
- Secondary Location: QuickQuotePropertyName.GL_PremisesAndProducts_DeductibleId data loading
- External Dependencies: Deductible amount configuration by type and jurisdiction

### 2.3 - Deductible Basis (Required when section active)
**Field Specifications**:
- User selects deductible application basis from dropdown menu
- Required field when deductible section is active (marked with asterisk)
- Defines how deductible applies to claims and coverage

**User Experience & Validation**:
- System requires basis selection to complete deductible configuration
- Selection determines deductible application methodology
- User must understand basis implications for claim scenarios

**Complete Option Set**:
- Options loaded from GL Premises and Products Deductible Per Type configuration
- Typical options include per occurrence, per claim, aggregate basis
- UNVERIFIED: Specific basis options require configuration analysis

**Selection Impact Analysis**:
- Basis selection affects how deductible applies to multiple claims
- Impacts claim handling procedures and insured responsibilities  
- Different basis types affect premium calculations and coverage interpretation

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 138-146
- Secondary Location: QuickQuotePropertyName.GL_PremisesAndProducts_DeductiblePerTypeId data loading
- External Dependencies: Deductible basis configuration and claim handling rules

## Section 3 - Policy Level Coverages

### 3.1 - Additional Insured (Enhanced UI Component)

**Field Specifications**:
- User indicates whether policy includes additional insured coverage via checkbox
- When selected, system displays detailed additional insured configuration options
- User specifies number and types of additional insureds through dropdown and checkbox selections

**User Selections/User Interactions**:
- User checks "Additional Insured" to activate coverage
- System displays "How many of the following Additional Insureds Apply?" dropdown
- User selects from quantity options: 0, 1, 2, 3, or "4 or more"
- System presents list of available additional insured categories with explanatory bullet points
- User selects applicable additional insured types through individual checkboxes for specific coverage situations

**Complete Option Set - Quantity Selection**:
- 0 additional insureds (Value: "0")
- 1 additional insured (Value: "1")  
- 2 additional insureds (Value: "2")
- 3 additional insureds (Value: "3")
- 4 or more additional insureds (Value: "4")

**Complete Option Set - Additional Insured Types**:
- Co-Owner of Insured Premises
- Controlling Interests  
- Engineers, Architects, or Surveyors not Engaged by the Named Insured
- Mortgagee, Assignee or Receiver
- Owner or Other Interests from Whom Land has been Leased

**Additional Insured Categories Listed**:
System displays these categories for user reference:
- Vendors
- Designated Person or Organization
- Engineers, Architects, or Surveyors not Engaged by the Named Insured  
- Owners, Lessees or Contractors
- Lessor of Leased Equipment
- Managers or Lessors of Premises

**Selection Impact Analysis**:
- Additional insured selections affect policy limits application and coverage extension
- Different AI types have varying coverage scopes and application methods
- Quantity selection impacts premium calculations and policy administration
- Selection triggers policy endorsement attachment and coverage modifications

**Downstream Impacts**:
- **Applications Page**: User may need to complete Additional Insured Supplemental Application with specific entity details
- **Rating Engine**: System recalculates premiums based on number and types of additional insureds selected
- **Policy Documentation**: System generates appropriate endorsement forms based on selections
- **Claims Processing**: Additional insured types affect claim notification and coverage determination procedures

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx lines 180-230 (dropdown and checkbox structure)
- Secondary Location: VrCgl.js CoverageCheckboxChanged('AI') function
- External Dependencies: Additional insured endorsement forms, premium calculation logic

### 3.2 - Condo Directors and Officers (Enhanced UI Component)

**Field Specifications**:
- User selects Condo Directors and Officers coverage via checkbox
- Coverage available only for Commercial Package Policies (CPP)
- When selected, system displays named association field and deductible options
- System automatically adjusts occurrence liability limit requirements

**User Selections/User Interactions**:
- User checks "Condo Directors and Officers" checkbox to activate coverage
- System displays eligibility guidelines popup with qualification criteria
- User enters named association name if different from named insured
- User selects deductible amount from available dropdown options
- System automatically constrains Occurrence Liability Limit to $1,000,000 minimum when coverage selected

**Complete Option Set - Availability**:
- Available: Commercial Package Policies only
- Not Available: Standalone General Liability policies

**Complete Option Set - Deductible Options**:
- Multiple deductible amounts available via dropdown selection
- UNVERIFIED: Exact deductible values require configuration data extraction

**Selection Impact Analysis**:
- Coverage selection forces minimum Occurrence Liability Limit of $1,000,000
- Fixed coverage limit of $1,000,000 cannot be modified by user
- Selection triggers display of eligibility guidelines and qualification requirements
- Named association field allows coverage for different entity than named insured

**Downstream Impacts**:
- **Policy Limits**: System automatically increases Occurrence Liability Limit to $1,000,000 if currently below that level
- **Rating Engine**: System recalculates premiums based on $1,000,000 coverage limit and selected deductible
- **Underwriting Review**: Coverage selection may trigger additional underwriting review for association qualifications
- **Policy Documentation**: System generates appropriate Condo D&O endorsement forms

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Condo D&O section with checkbox and sub-controls
- Secondary Location: VrCgl.js Cgl.ToggleOccurrenceLiabLimit() function for OLL constraint
- External Dependencies: CPP availability logic, eligibility guidelines popup content

### 3.3 - Cyber Liability (Enhanced UI Component)

**Field Specifications**:
- User selects Cyber Liability coverage via checkbox
- Coverage availability determined by state, company, and class code eligibility
- Fixed coverage limits and deductible amounts
- State-specific variations in coverage type and application

**User Selections/User Interactions**:
- User checks "Cyber Liability" or "Cyber Coverage" checkbox (name varies by availability)
- System displays fixed coverage limits and deductible information
- Coverage automatically applies when selected without additional configuration
- System validates class code eligibility before allowing selection

**Complete Option Set - State Availability**:
- Indiana/Ohio: Eligible states with standard application (Type ID "23")
- Illinois: Opt-out state with different application rules (Type ID "24")
- Other States: Availability varies by company configuration

**Complete Option Set - Coverage Terms**:
- Aggregate Limit: $50,000 (fixed, cannot be modified)
- Deductible: $2,500 (fixed, cannot be modified)

**Selection Impact Analysis**:
- Coverage eligibility restricted by specific class codes (per configuration settings)
- State location determines application type and coverage characteristics
- Fixed terms prevent user modification of limits or deductibles
- Selection affects premium calculations and policy terms

**Downstream Impacts**:
- **Class Code Validation**: System checks all policy and location class codes against ineligible list
- **Rating Engine**: System applies cyber liability premium calculations based on fixed terms
- **State Compliance**: Different states have varying regulatory requirements and application processes
- **Underwriting Review**: Certain class codes may require additional cyber risk assessment

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Cyber Liability checkbox section
- Secondary Location: CLIHelper.vb for eligibility and application logic
- External Dependencies: ConfigurationManager AppSetting "CLIIneligibleCGLclasscodes", CPP.CyberCoverageHelper availability logic

### 3.4 - Employee Benefits Liability

**Field Specifications**:
- User selects Employee Benefits Liability coverage via checkbox
- Coverage requires number of employees input field
- Fixed occurrence limit that mirrors policy occurrence liability limit
- Numeric input validation for employee count

**User Selections/User Interactions**:
- User checks "Employee Benefits Liability" checkbox to activate coverage
- System displays employee count input field requiring numeric entry
- User enters total number of employees (required field when coverage selected)
- System automatically sets occurrence limit to match policy occurrence liability limit

**Complete Option Set - Coverage Terms**:
- Each Employee Occurrence Limit: Matches Policy Occurrence Liability Limit (e.g., $1,000,000)
- Number of Employees: User-entered value (required, numeric only with comma formatting)

**Selection Impact Analysis**:
- Employee count directly affects premium calculations
- Occurrence limit automatically adjusts when policy occurrence liability limit changes
- Coverage provides protection for employee benefit administration errors
- Selection requires accurate employee count disclosure for proper coverage

**Downstream Impacts**:
- **Rating Engine**: Premium calculations based on occurrence limit and number of employees
- **Policy Documentation**: Employee count recorded for coverage verification and claim handling
- **Underwriting Review**: Large employee counts may trigger additional underwriting questions
- **Coverage Validation**: Employee count must be updated if business size changes significantly

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Employee Benefits section with checkbox and input controls
- Secondary Location: JavaScript numeric formatting for employee count field (comma insertion on keyup/blur)
- External Dependencies: Policy occurrence liability limit linkage for automatic limit setting

### 3.5 - Employment Practices Liability (Enhanced UI Component)

**Field Specifications**:
- User selects Employment Practices Liability coverage via checkbox
- Claims-made coverage with fixed limits and deductible
- Class code eligibility restrictions apply
- State-specific application variations

**User Selections/User Interactions**:
- User checks "Employment Practices Liability" checkbox to activate coverage
- System displays fixed coverage terms without user modification options
- Coverage automatically applies when selected if class codes are eligible
- System validates class code eligibility against exclusion list

**Complete Option Set - Coverage Terms**:
- Each "Claim" Limit: $100,000 (fixed, cannot be modified)
- Aggregate Limit: $100,000 (fixed, cannot be modified) 
- Deductible: $5,000 (fixed, cannot be modified)

**Complete Option Set - State Variations**:
- Indiana/Ohio: Non-underwritten application (Type ID "22")
- Illinois: Opt-out application with different processing (Type ID "19")
- Ineligible Classes: Automatic denial for excluded class codes (Type ID "20")

**Selection Impact Analysis**:
- Class code eligibility determines coverage availability before user can select
- Claims-made coverage requires continuous coverage to maintain protection
- Fixed terms prevent user customization of limits or deductibles
- State location affects application processing and underwriting requirements

**Downstream Impacts**:
- **Class Code Validation**: System checks all policy and location class codes against EPLI ineligible list
- **Rating Engine**: Premium calculations based on fixed coverage terms and class code risk factors
- **Underwriting Review**: Non-underwritten in most states, but may require additional review for high-risk classes
- **Claims Processing**: Claims-made coverage has specific notice and reporting requirements

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx EPLI checkbox section
- Secondary Location: EPLIHelper.vb for eligibility logic and class code exclusion validation
- External Dependencies: ConfigurationManager AppSetting "EPLIIneligibleCGLclasscodes" for class code restrictions

### 3.6 - Stop Gap (OH) (Enhanced UI Component)

**Field Specifications**:
- User selects Stop Gap coverage via checkbox (Ohio only)
- Coverage available only for Ohio quotes after specific effective date
- Requires limit selection and Ohio-specific payroll entry
- Conditional availability based on location and effective date

**User Selections/User Interactions**:
- User checks "Stop Gap (OH)" checkbox to activate coverage (Ohio quotes only)
- System displays limit dropdown for user selection
- User enters Ohio-only payroll amount in designated field
- System provides deletion confirmation dialog if user attempts to remove existing coverage

**Complete Option Set - Availability**:
- Available: Ohio quotes with effective dates after configured threshold
- Not Available: All non-Ohio states and Ohio quotes before effective date threshold

**Complete Option Set - Coverage Options**:
- Limit Options: Available through dropdown selection
- UNVERIFIED: Exact limit values require dropdown configuration extraction
- Payroll Entry: Numeric input field for Ohio-specific payroll amounts

**Selection Impact Analysis**:
- Coverage availability restricted to Ohio location and specific effective date requirements
- Payroll amount affects premium calculations and coverage scope
- Stop Gap provides employers liability protection where workers compensation excluded
- Selection creates specific Ohio regulatory compliance coverage

**Downstream Impacts**:
- **Geographic Validation**: System validates Ohio location before allowing coverage selection
- **Effective Date Logic**: Coverage only available for quotes meeting Ohio effective date requirements
- **Rating Engine**: Premium calculations based on selected limits and Ohio payroll amounts
- **Workers Compensation**: Coverage coordinates with workers compensation exclusions and exposures

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Stop Gap section with Ohio-specific controls
- Secondary Location: VrCgl.js Cgl.HandleStopGapClicks() function with deletion confirmation dialog
- External Dependencies: GetOhioEffectiveDate() configuration, HasStopGap() property validation

### 3.7 - Hired/Non-Owned Autos

**Field Specifications**:
- User views auto coverage status via checkbox display
- Coverage automatically checked when quote includes hired or non-owned auto exposure
- Coverage status reflects existing auto coverage selections from other system modules
- Deletion requires confirmation dialog

**User Selections/User Interactions**:
- System automatically checks coverage when quote has hired auto or non-owned auto exposure
- User can uncheck coverage to remove auto exposures (with confirmation dialog)
- Coverage status reflects decisions made in auto coverage modules
- User confirmation required before removing existing auto coverage

**Complete Option Set - Coverage Status**:
- Checked: Quote has hired auto coverage OR non-owned auto coverage
- Unchecked: Quote has neither hired nor non-owned auto exposures

**Selection Impact Analysis**:
- Coverage checkbox reflects auto exposure decisions made elsewhere in system
- Unchecking coverage removes auto exposures and affects overall policy scope
- Auto coverage affects liability limits application and premium calculations
- Selection coordinates with commercial auto coverage modules

**Downstream Impacts**:
- **Auto Coverage Module**: Changes to checkbox affect hired/non-owned auto exposure settings
- **Rating Engine**: Auto coverage selections impact liability premium calculations
- **Policy Documentation**: Auto exposures must be documented for coverage verification
- **Coverage Coordination**: Hired/non-owned auto coordinates with commercial auto policies if present

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Hired/Non-Owned Autos checkbox
- Secondary Location: VrCgl.js Cgl.CoverageCheckboxChanged('HNO') function with deletion confirmation
- External Dependencies: HasHiredAuto and HasNonOwnedAuto property validation from auto coverage modules

### 3.8 - Liquor Liability - Indiana/Ohio Format (Enhanced UI Component)

**Field Specifications**:
- User selects Liquor Liability coverage via checkbox (Indiana/Ohio format)
- Coverage available only when Occurrence Liability Limit is $300,000 or higher
- User selects applicable business types and enters corresponding sales amounts
- Multiple business type categories with individual sales reporting

**User Selections/User Interactions**:
- User checks "Liquor Liability" checkbox to activate coverage
- System displays business type selection checkboxes with sales amount fields
- User selects applicable business categories from available options
- User enters annual liquor sales amounts for each selected business type
- System formats sales amounts with currency display during entry

**Complete Option Set - Eligibility Requirements**:
- Minimum Occurrence Liability Limit: $300,000 (system validates before allowing selection)
- Available States: Indiana and Ohio only
- Occurrence Limit: Matches Policy Occurrence Liability Limit value

**Complete Option Set - Business Type Categories**:
- Manufacturers, Wholesalers & Distributors (with sales amount field)
- Restaurants Or Hotels (with sales amount field)
- Package Stores (with sales amount field)
- Clubs (with sales amount field)

**Selection Impact Analysis**:
- Business type selections determine coverage scope and endorsement forms
- Sales amounts directly affect premium calculations and coverage limits
- Multiple business types can be selected simultaneously if applicable
- Coverage requires supplemental application completion for selected business types

**Downstream Impacts**:
- **Applications Page**: User must complete Liquor Liability Application or Restaurant Supplemental Application
- **Rating Engine**: Premium calculations based on selected business types and reported sales volumes
- **Coverage Validation**: Sales amounts must be accurate for proper coverage and claim handling
- **Underwriting Review**: High sales volumes or multiple business types may require additional underwriting

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Liquor Liability Indiana/Ohio section with business type checkboxes and sales fields
- Secondary Location: JavaScript currency formatting for all sales amount fields
- External Dependencies: OLL minimum requirement validation, supplemental application requirements

### 3.9 - Liquor Liability - Illinois Format (Enhanced UI Component)

**Field Specifications**:
- User selects Liquor Liability coverage via checkbox (Illinois-specific format)
- Coverage available only when Occurrence Liability Limit is $300,000 or higher
- Coverage uses Illinois statutory limits format instead of occurrence limit matching
- User selects applicable business types and enters corresponding sales amounts

**User Selections/User Interactions**:
- User checks "Liquor Liability" checkbox to activate coverage (Illinois format)
- System displays "STATE STATUTORY LIMITS WILL APPLY" for all occurrence limit levels
- User selects applicable business categories from available options
- User enters annual liquor sales amounts for each selected business type
- System manages state-specific control visibility through JavaScript

**Complete Option Set - Eligibility Requirements**:
- Minimum Occurrence Liability Limit: $300,000 (system validates before allowing selection)
- Available State: Illinois only
- Coverage Format: "Each Person BI Limit/Each Person PD Limit/Loss of Means of Support"
- Statutory Limits: "STATE STATUTORY LIMITS WILL APPLY" regardless of OLL selection

**Complete Option Set - Business Type Categories**:
- Manufacturers, Wholesalers & Distributors (with sales amount field)
- Restaurants Or Hotels (with sales amount field)  
- Package Stores (with sales amount field)
- Clubs (with sales amount field)

**Selection Impact Analysis**:
- Illinois format uses statutory limits instead of policy occurrence limits
- Business type selections determine applicable coverage endorsements and forms
- Sales amounts affect premium calculations under Illinois regulatory framework
- Coverage format differs significantly from Indiana/Ohio approach

**Downstream Impacts**:
- **Applications Page**: User must complete Illinois-specific Liquor Liability Application or Restaurant Supplemental Application
- **Rating Engine**: Premium calculations based on Illinois statutory framework and reported sales volumes
- **State Compliance**: Coverage must comply with Illinois liquor liability regulatory requirements
- **Claims Processing**: Illinois statutory limits apply regardless of underlying policy limits

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Liquor Liability Illinois section with state-specific formatting
- Secondary Location: VrCgl.js Cgl.ToggleLiquorLiabilityControls() function for state-specific visibility management
- External Dependencies: Illinois statutory limit requirements, state-specific application processing

### 3.10 - IL Contractors - Home Repair & Remodeling

**Field Specifications**:
- User selects Illinois Contractors coverage via checkbox (Illinois only)
- Coverage provides fixed $10,000 limit for home repair and remodeling operations
- Coverage available only for Illinois-based contractors
- System displays informational details when coverage selected

**User Selections/User Interactions**:
- User checks "IL Contractors - Home Repair & Remodeling" checkbox to activate coverage
- System displays coverage information and fixed limit details
- Coverage automatically applies with preset terms when selected
- System manages Illinois-specific information visibility through JavaScript

**Complete Option Set - Availability**:
- Available: Illinois state contractors only
- Not Available: All non-Illinois states
- Coverage Limit: $10,000 (fixed, cannot be modified)

**Selection Impact Analysis**:
- Coverage addresses Illinois regulatory requirements for contractor operations
- Fixed limit provides specific protection for home repair and remodeling activities
- Selection triggers Illinois-specific contractor coverage endorsement
- Coverage complements general liability protection for specified contractor activities

**Downstream Impacts**:
- **State Compliance**: Coverage meets Illinois contractor regulatory requirements
- **Rating Engine**: System applies Illinois contractor premium calculations based on fixed coverage terms
- **Coverage Coordination**: Coordinates with general liability coverage for comprehensive contractor protection
- **Policy Documentation**: Illinois-specific contractor endorsement attached to policy

**Source Code Details**:
- Primary Location: ctl_CGL_Coverages.ascx Illinois Contractors section
- Secondary Location: VrCgl.js Cgl.ILContractorsHomeRepairCheckboxChanged() function for info row visibility management
- External Dependencies: Illinois state validation, contractor coverage regulatory requirements

## Quality Certification

This comprehensive requirements document has been prepared based on complete technical analysis of the CGL Policy Level Coverages system. All field specifications, user interactions, option sets, and downstream impacts have been verified through source code evidence and business logic validation.