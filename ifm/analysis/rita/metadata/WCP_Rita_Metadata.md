# WCP METADATA FOR RITA (DOMAIN VALIDATION)

**From:** Rex (Pattern Mining Specialist)  
**To:** Rita (Insurance Domain Specialist)  
**Feature:** Workers' Compensation (WCP)  
**Analysis Date:** Current

## EXECUTIVE SUMMARY (400 tokens)

WCP domain analysis reveals sophisticated workers' compensation insurance patterns requiring domain expertise validation across risk assessment, regulatory compliance, multi-state coverage rules, and insurance-specific business logic. Analysis identifies critical domain-dependent patterns including kill question risk assessment criteria, state-specific regulatory endorsements, experience modification rating logic, class code business classification rules, and farm operation indicators.

Key domain validation needs: (1) Kill question risk assessment criteria - aircraft/watercraft ownership, hazardous materials operations definitions, and professional employment organization classification accuracy, (2) State-specific regulatory compliance - Indiana state form requirements, Kentucky rejection of coverage endorsement rules, and multi-state endorsement applicability, (3) Experience modification rating logic - industry standard practices and effective date requirements, (4) Workers' compensation class code accuracy - 12 specific farm-related class codes and business operation classification validation, (5) Geographic coverage rules - employee residence restrictions and multi-state capability business logic.

Domain patterns require insurance expertise validation for regulatory compliance accuracy, risk assessment appropriateness, and industry standard alignment. Technical implementation appears sound but business rule accuracy needs domain validation.

## KEY FINDINGS REQUIRING DOMAIN VALIDATION (500 tokens)

### 1. Kill Question Risk Assessment Criteria
**Domain Pattern**: Risk assessment questions for workers' compensation eligibility
- **Aircraft/Watercraft Risk**: "Does Applicant own, operate or lease aircraft or watercraft?" - Need validation of risk criteria and underwriting guidelines
- **Hazardous Materials Definition**: Complex question covering "past, present or discontinued operations involve(d) storing, treating, discharging, applying, disposing, or transporting of hazardous material" - Requires validation of hazardous material definition scope and examples (landfills, wastes, fuel tanks)
- **Professional Employment Organization**: "professional employment organization, employee leasing operation, or temporary employment agency" - Need validation of PEO definition accuracy and coverage implications

**Domain Validation Needed**: 
- Are risk assessment criteria aligned with industry underwriting standards?
- Do hazardous material definitions match regulatory classifications?
- Are PEO definitions consistent with workers' compensation industry practice?

### 2. State-Specific Regulatory Endorsements
**Domain Pattern**: State-specific endorsement rules and compliance requirements
- **Indiana Requirements**: Form 36097 (Notice For Workers Compensation And Occupational Diseases Coverage) required for officer exclusions - Need validation of current form requirements and submission process
- **Kentucky Integration**: Rejection of Coverage Endorsement (WC 16 03 01) only available when effective date >= Kentucky WCP effective date - Requires validation of Kentucky regulatory timeline and form applicability
- **Multi-State Labels**: System changes endorsement labels from "(IN/IL)" to "(IN/IL/KY)" based on Kentucky effective date - Need confirmation of regulatory accuracy

**Domain Validation Needed**:
- Are Indiana state form requirements current and accurate?
- Is Kentucky WCP effective date implementation correct for regulatory compliance?
- Do endorsement form numbers (WC 00 03 10, WC 00 03 08, etc.) match current industry forms?

### 3. Experience Modification Rating Logic
**Domain Pattern**: Experience modification factor business rules and rating implications
- **Default Value**: System defaults to "1" for new accounts - Need validation of industry standard practice
- **Date Requirements**: Experience Mod Eff Date required only when factor > 1, disabled when = 1 - Requires validation of rating bureau requirements
- **Date Clearing**: Automatic clearing of dates when factor = 0 or 1 - Need confirmation of proper rating implementation
- **Range Validation**: System requires factor > 0 - Need validation of acceptable range limits

**Domain Validation Needed**:
- Are experience modification default and validation rules consistent with NCCI or state bureau requirements?
- Do date field requirements align with rating effective date business practices?
- Are automatic clearing rules appropriate for experience modification rating?

### 4. Workers' Compensation Class Code Business Rules
**Domain Pattern**: Class code classification and farm indicator logic
- **Farm Class Codes**: System identifies 12 specific class codes (0005, 0008, 0016, 0034, 0036, 0037, 0050, 0079, 0083, 0113, 0170, 8279) as farm-related - Requires validation of current class code definitions
- **Farm Indicator Logic**: Farm class codes automatically set farm indicator flag across all sub-quotes - Need validation of business logic appropriateness
- **Class Code Exclusions**: System excludes farm class codes from general WCP lookup via QuickQuote.dbo.WCPClassificationExclude table - Requires validation of exclusion business rationale

**Domain Validation Needed**:
- Do the 12 farm class codes accurately represent current farm-related workers' compensation classifications?
- Is the farm indicator logic appropriate for underwriting and pricing considerations?
- Are class code exclusion rules aligned with business underwriting guidelines?

### 5. Geographic Coverage and Employee Residence Rules
**Domain Pattern**: Multi-state coverage rules and employee residence restrictions
- **Geographic Kill Question**: Dynamic question changes based on multi-state capability - "state of {governingState}" vs "Indiana, Illinois, or Kentucky" - Need validation of coverage territory accuracy
- **Multi-State Logic**: System determines multi-state capability based on Kentucky WCP effective date - Requires validation of geographic expansion business rules
- **Employee Residence Restrictions**: Questions assess whether employees live outside approved states - Need validation of coverage territory limitations and regulatory requirements

**Domain Validation Needed**:
- Are geographic coverage territories accurately represented in the system logic?
- Do employee residence restrictions align with regulatory and underwriting requirements?
- Is multi-state capability logic consistent with business expansion and regulatory approval timelines?

### 6. Endorsement Business Logic Validation
**Domain Pattern**: State-specific endorsement applicability and business rules
- **Waiver of Subrogation**: Requires number of waivers with $50 premium per waiver - Need validation of pricing accuracy
- **Exclusion Logic**: Complex exclusion endorsements with state-specific applicability - Requires validation of regulatory compliance
- **Health Insurance Requirement**: Sole proprietor inclusion requires "written proof of health insurance coverage" - Need validation of regulatory requirement accuracy

**Domain Validation Needed**:
- Are endorsement pricing rules ($50 per waiver) current and accurate?
- Do exclusion endorsement rules comply with state regulatory requirements?
- Are health insurance documentation requirements consistent with regulatory compliance?

## INSURANCE DOMAIN QUESTIONS FOR VALIDATION

### Regulatory Compliance
1. Are all endorsement form numbers (WC 00 03 10, WC 00 03 08, WC 12 03 07, WC 16 03 01) current and accurate?
2. Does Indiana Form 36097 requirement accurately reflect current state regulations?
3. Is Kentucky WCP effective date implementation timeline correct for regulatory compliance?

### Underwriting Standards  
1. Do kill question risk assessment criteria align with industry underwriting guidelines?
2. Are experience modification business rules consistent with rating bureau standards?
3. Is the farm indicator logic appropriate for underwriting risk assessment?

### Business Classification
1. Are the 12 farm-related class codes accurate for current workers' compensation classifications?
2. Do hazardous material operation definitions align with industry risk assessment standards?
3. Are professional employment organization definitions current and complete?

### Coverage Territory
1. Do geographic coverage rules accurately reflect approved coverage territories?
2. Are employee residence restrictions consistent with regulatory and underwriting requirements?
3. Is multi-state expansion logic aligned with business and regulatory approvals?

## METADATA LOCATIONS

- **Complete Domain Analysis**: `//project/workspaces/ifi/.scratch/WCP_Complete_Pattern_Analysis_Rex.md`
- **Technical Implementation**: All domain patterns include source code references for validation
- **Business Rule Catalog**: Domain-specific business rules requiring expert validation
- **Regulatory Patterns**: State-specific compliance requirements needing domain confirmation

## COMPLETENESS: HIGH
**STATUS**: READY FOR DOMAIN VALIDATION
**DOMAIN COVERAGE**: All insurance-specific patterns identified with validation questions
**VALIDATION PRIORITY**: Kill questions, regulatory endorsements, experience modification rating

**Domain Expertise Required**: Workers' compensation underwriting, state regulatory compliance, NCCI/state bureau rating rules, class code classification standards, and multi-state coverage territory regulations.