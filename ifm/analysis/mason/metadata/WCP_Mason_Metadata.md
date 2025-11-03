# WCP METADATA FOR MASON (REQUIREMENTS EXTRACTION)

**From:** Rex (Pattern Mining Specialist)  
**To:** Mason (Requirements Extraction Specialist)  
**Feature:** Workers' Compensation (WCP)  
**Analysis Date:** Current

## EXECUTIVE SUMMARY (400 tokens)

Complete WCP technical pattern analysis reveals 25+ distinct patterns across 6 major functional areas providing comprehensive foundation for requirements documentation. Analysis covers WCP initial quote kill questions (6 questions with multi-state conditional logic), state-specific endorsement matrix (8 endorsement types across IN/IL/KY), dynamic class code management with Diamond integration, experience modification workflow with automatic field management, and complete validation framework.

Key business-ready patterns: (1) 6 initial quote kill questions with sophisticated geographic conditional logic for multi-state vs single-state scenarios, (2) State-specific endorsement matrix supporting different endorsement combinations based on state presence (IN/IL/KY), (3) Experience modification business rules with automatic date field enable/disable when value equals 1, (4) Farm indicator detection based on specific class codes, (5) Multi-state classification validation requiring one classification per state, (6) Employer's liability auto-upgrade from 100/500/100 to 500/500/500 for umbrella compatibility.

All patterns include complete source code evidence, business rule documentation, validation requirements, and user experience specifications ready for requirements transformation.

## KEY FINDINGS FOR REQUIREMENTS (500 tokens)

### 1. WCP Initial Quote Kill Questions Business Logic
**Pattern**: 6 mandatory kill questions in popup modal before quote development
- **Aircraft/Watercraft**: "Does Applicant own, operate or lease aircraft or watercraft?" (Diamond 9341)
- **Hazardous Materials**: Complex question about past/present/discontinued hazardous material operations (Diamond 9086)  
- **Employee Residence**: Dynamic question with multi-state vs single-state logic - changes from "state of {governingStateString}" to "Indiana, Illinois, or Kentucky" based on Kentucky WCP effective date (Diamond 9573/9342)
- **Coverage History**: 3-year lookback for declined/cancelled/non-renewed coverage (Diamond 9343)
- **Business Operations**: Professional employment organization/leasing operations assessment (Diamond 9344)
- **Financial Stability**: True kill question - 5-year lookback for tax liens/bankruptcy with immediate quote termination (Diamond 9107)

**Requirements Impact**: All questions required, "Yes" answers typically flag ineligibility, Question #6 has immediate termination workflow

### 2. State-Specific Endorsement Requirements Matrix  
**Pattern**: Dynamic endorsement visibility and business rules based on state combinations
- **IN/IL Common**: Inclusion of Sole Proprietors (health insurance proof required), Blanket Waiver of Subrogation, Waiver of Subrogation (requires number of waivers)
- **IN Exclusive**: Exclusion of Amish Workers, Exclusion of Executive Officer (requires Indiana state form 36097)
- **IL Exclusive**: Exclusion of Sole Proprietors Partners Officers LLC Members (IL version)  
- **KY Exclusive**: Rejection of Coverage Endorsement (only when effective date >= Kentucky WCP effective date)
- **Label Updates**: When Kentucky enabled, labels change from "(IN/IL)" to "(IN/IL/KY)"

**Requirements Impact**: Conditional visibility rules, state-specific form requirements, health insurance documentation requirements

### 3. Experience Modification Business Rules
**Pattern**: Complex validation with automatic field management
- **Default Value**: "1" when empty or "0" 
- **Date Field Logic**: Experience Mod Eff Date required only when Experience Modification > 1, disabled when = 1
- **Validation**: Must be numeric and > 0
- **Auto-Clear**: Dates automatically cleared when Experience Modification = 0 or 1

**Requirements Impact**: Conditional required field behavior, automatic form state management, user guidance needed

### 4. Class Code Management Requirements
**Pattern**: Lookup-driven classification with business rules
- **Class Code**: Read-only, populated via lookup button triggering search modal
- **Payroll**: Required user input field
- **Description**: Read-only, auto-populated from class code selection
- **Farm Detection**: Specific class codes (0005, 0008, 0016, 0034, 0036, 0037, 0050, 0079, 0083, 0113, 0170, 8279) automatically set farm indicator flag
- **Save Requirement**: Red warning - "You MUST click save after entering each classification!"

**Requirements Impact**: Multi-step workflow, lookup integration, automatic business rule application

### 5. Multi-State Validation Requirements  
**Pattern**: Different validation rules for single vs multi-state quotes
- **Multi-State**: Each state must have minimum one location and one classification
- **Single-State**: Must have minimum one location and one classification  
- **Error Messages**: State-specific error messages listing missing states
- **Geographic Logic**: Quote processing approach determined by effective date and multi-state capability

**Requirements Impact**: State-specific validation rules, conditional error messaging, geographic business logic

## METADATA LOCATIONS

- **Complete Pattern Analysis**: `//project/workspaces/ifi/.scratch/WCP_Complete_Pattern_Analysis_Rex.md`
- **Detailed Evidence**: All patterns include source file and line references
- **Business Logic Catalog**: 25+ patterns with complete business behavior documentation
- **Validation Rules**: Comprehensive validation framework documentation
- **UI Specifications**: Complete field specifications with conditional behavior

## COMPLETENESS: HIGH
**STATUS**: COMPLETE
**EVIDENCE QUALITY**: 100% source code verified, zero speculation
**BUSINESS VALUE**: Ready for immediate requirements transformation

**Quality Assurance**: Every business rule includes source code evidence, all conditional logic documented with complete matrices, all assumptions marked as UNVERIFIED (none found).