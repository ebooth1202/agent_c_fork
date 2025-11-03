# CGL QuickQuote Popup Modal Questions

## Overview

The Commercial General Liability (CGL) QuickQuote popup modal contains **6 kill questions** that determine whether a quote can proceed. These questions serve as initial screening criteria for CGL coverage eligibility.

## Source Code Reference

**Method**: `UWQuestions.GetCGLUnderwritingQuestions()`  
**File**: `//project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/IFM.VR.Common/UWQuestions/UWQuestions.vb`  
**Verification Status**: ✅ **VERIFIED** - Content extracted from source code  
**Last Updated**: Based on Rex's independent verification analysis

## CGL Kill Questions (6 Questions)

### Question 1 - Prior Coverage Issues
**Diamond Code**: 9345  
**Question**: "Any prior coverage declined, cancelled or non-renewed during the prior 3 years?"

### Question 2 - Sexual Abuse/Discrimination Claims  
**Diamond Code**: 9346  
**Question**: "Any past losses or claims relating to sexual abuse or molestation allegations, discrimination or negligent hiring?"

### Question 3 - Explosive Materials
**Diamond Code**: 9347  
**Question**: "Do any operations include blasting or utilize or store explosive material?"

### Question 4 - Subcontractor Insurance
**Diamond Code**: 9348  
**Question**: "Are subcontractors allowed to work without providing you with a certificate of insurance?"

### Question 5 - Equipment Leasing
**Diamond Code**: 9349  
**Question**: "Does applicant lease equipment to others with or without operators?"

### Question 6 - Aircraft/Space Industry Products
**Diamond Code**: 9350  
**Question**: "Any products related to the aircraft or space industry?"

## Technical Implementation Notes

### Dynamic Loading Pattern
- Questions are loaded dynamically from the Diamond underwriting system via the `GetCGLUnderwritingQuestions()` method
- Each question is identified by a unique Diamond Code (9345-9350)
- Questions are LOB-specific (CGL) and pulled from the centralized underwriting questions repository

### Modal Display Mechanism
**Status**: ⚠️ **UNVERIFIED - REQUIRES STAKEHOLDER CONFIRMATION**

The specific modal popup display mechanism and trigger events have not been verified in source code analysis. Key implementation details requiring confirmation:
- Modal popup trigger conditions (button click, workflow stage, validation event)
- Popup window sizing and layout specifications  
- Question display order and formatting rules
- User interaction behavior (required vs optional responses)
- Modal closing conditions and validation requirements

## Business Impact Classification

**Question Type**: Kill Questions  
**Purpose**: Initial CGL coverage eligibility screening  
**Impact**: Negative responses may prevent quote continuation  
**Stakeholder**: Underwriting team, sales agents, customers

## Notes for Architecture Planning

- Questions sourced from external Diamond system integration
- Dynamic content loading requires API connectivity
- Modal popup implementation needs UI framework verification
- Consider caching strategy for question content to improve performance
- Ensure responsive design for various screen sizes

---

**Documentation prepared by**: Mason (Requirements Extraction Specialist)  
**Based on analysis by**: Rex (Pattern Miner)  
**Evidence Standard**: Source code verified with file/method references  
**Stakeholder Readiness**: High - Ready for architecture planning and business review