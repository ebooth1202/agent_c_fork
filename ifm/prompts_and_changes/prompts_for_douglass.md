# Updated Prompts for Douglas - IFI Analysis Requests

This document provides updated standardized prompt templates for requesting various types of IFI analysis from Douglas. These templates incorporate the new endorsement analysis standards and business-friendly documentation requirements.

---

## 🎯 **TEMPLATE 1: Complete LOB Analysis**

**Use For**: Full Line of Business analysis with new endorsement workflow standards

```markdown
Douglas, I need you to orchestrate a complete IFI analysis for the [LOB NAME] Line of Business.

**Scope**: Complete [LOB NAME] system analysis with new endorsement workflow documentation
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Line of Business**: [LOB NAME]

**Deliverable Requirement**:
Produce ONE consolidated requirements document at:
//project/ifm/[LOB]_Complete_Requirements.md

The document must:
- Transform Rex's technical pattern extraction into business-friendly requirements
- Apply new endorsement workflow format (User Selections/Interactions → Downstream Impacts)
- Use business-friendly language throughout (no method calls or technical properties)

**Content Restrictions** (Client Requirements):
- NO Executive Summaries or Business Purpose sections
- NO Insurance Compliance frameworks or regulatory guidance
- NO Modernization Recommendations or architectural strategy  
- NO Agent involvement explanations or process descriptions

**MANDATORY STANDARDS**:
- Include "UI Alert Messages" sections for ANY alerts, popups, validation messages, or system notifications
- Use ONLY new Source Code Details format: Primary Location/Secondary Location/External Dependencies (separate lines)
- Apply endorsement workflow: Field Specifications → User Selections/Interactions → Downstream Impacts → UI Alert Messages → Source Code Details
- Business-friendly language (no method calls or technical properties)
- Exclude IgnoreForLists="Yes" data
- Document ALL UI text in **bold quotes**

**Complete Option Documentation Requirements**:
- Extract ALL possible dropdown options (not just defaults) excluding IgnoreForLists="Yes" items
- Document selection impact and business consequences  
- Apply Complete Option Set and Selection Impact Analysis sections from template
- Reject "various options available" - must specify complete option universe
- Integrate Aria's current architecture analysis (no modernization recommendations) as subsections within relevant features
- Integrate Rita's technical validation as notes where applicable
- Include Vera's quality certification as the final section
- Follow the updated documentation standards at //project/ifm/templates/requirements_documentation_standards.md

**Endorsement Analysis Requirements**:
For each endorsement, apply the standardized format:
- Field Specifications (preserve existing format)
- User Selections/User Interactions (business-friendly system behavior descriptions)
- Downstream Impacts (Applications Page requirements, Rating Engine impacts, Claims Processing changes, etc.)
- Source Code Details (Primary Location/Secondary Location/External Dependencies format)

Coordinate the team through the sequential IFI workflow to produce a single comprehensive stakeholder-ready deliverable that covers all [LOB NAME] functionality with business-friendly language and proper cross-system impact analysis.
```

**Example LOB Names**: Workers' Compensation (WCP), Business Owners Policy (BOP), Commercial General Liability (CGL), Personal Auto, Homeowners

---

## 🎯 **TEMPLATE 2: Specific Feature Analysis**

**Use For**: Focused analysis on specific system features or modules

```markdown
Douglas, I need you to orchestrate a focused IFI analysis for [SPECIFIC FEATURE/MODULE] in the [LOB NAME if applicable] system.

**Scope**: [SPECIFIC FEATURE] analysis with new endorsement workflow standards
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Focus Area**: [SPECIFIC FEATURE/MODULE NAME]

**Deliverable Requirement**:
Produce ONE focused requirements document at:
//project/ifm/[FEATURE]_Requirements.md

The document must:
- Focus exclusively on [SPECIFIC FEATURE] functionality
- Apply new endorsement workflow format for any endorsements or complex components within this feature
- Transform technical patterns into business-friendly requirements
- Use business-friendly language throughout (no method calls or technical properties)

**Content Restrictions** (Client Requirements):
- NO Executive Summaries or Business Purpose sections
- NO Insurance Compliance frameworks or regulatory guidance
- NO Modernization Recommendations or architectural strategy
- NO Agent involvement explanations or process descriptions

**MANDATORY STANDARDS**:
- Include "UI Alert Messages" sections for ANY alerts, popups, validation messages, or system notifications
- Use ONLY new Source Code Details format: Primary Location/Secondary Location/External Dependencies (separate lines)
- Apply endorsement workflow: Field Specifications → User Selections/Interactions → Downstream Impacts → UI Alert Messages → Source Code Details
- Business-friendly language (no method calls or technical properties)
- Exclude IgnoreForLists="Yes" data
- Document ALL UI text in **bold quotes**

**Complete Option Documentation Requirements**:
- Extract ALL possible dropdown options (not just defaults) excluding IgnoreForLists="Yes" items
- Document selection impact and business consequences
- Apply Complete Option Set and Selection Impact Analysis sections from template
- Reject "various options available" - must specify complete option universe
- Include current architecture considerations and technical validation notes as subsections
- Follow updated documentation standards with new endorsement workflow format where applicable

**Cross-System Impact Requirements**:
- Document what happens in OTHER modules when selections are made in [SPECIFIC FEATURE]
- Identify specific user actions required elsewhere (e.g., "User must add 2 waiver names in Application module")
- Map workflow completion requirements across system modules

Coordinate the team to produce comprehensive [SPECIFIC FEATURE] documentation with business-friendly language and proper downstream impact analysis.
```

**Example Features**: Policy Level Coverages, Rating Engine, Endorsement Processing, Application Data Entry, Claims Integration, Billing Integration

---

## 🎯 **TEMPLATE 3: Cross-Module Dependencies Analysis (Phase 2)**

**Use For**: Cross-module integration analysis after Phase 1 completion

```markdown
Douglas, I need you to orchestrate a Phase 2 analysis for the [LOB NAME] Line of Business.

**Phase 2 Scope**: Cross-Module Dependencies Analysis
**Focus**: Document how [LOB NAME] integrates with other system modules (Policy, Billing, Claims, Endorsements, Rating, etc.)
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Existing Phase 1 Work**: Available in //project/ifm/

**Deliverable Requirement**:
Create a Cross-Module Dependencies Analysis document at:
//project/ifm/[LOB]_Cross_Module_Deps.md

The Phase 2 analysis must document:
- Downstream Requirements: Selections in [LOB NAME] that trigger requirements in other modules
- Data Flow: How data moves from [LOB NAME] to other modules
- Cross-Module Validation: Validation rules that span multiple modules
- Integration Points: API calls, shared objects, database dependencies
- Linkage Rules: Business rules connecting [LOB NAME] to other modules

For each cross-module dependency, document:
- Field/Coverage in [LOB NAME] that triggers downstream requirement
- Target module and specific location affected
- Business rule connecting the modules (in business-friendly language)
- Validation impact (if any)
- Source code evidence with file/line references for BOTH modules

**Business Language Requirements**:
- Use stakeholder-friendly language for all cross-module descriptions
- Convert technical integration details to business workflow implications
- Focus on user actions and system responses rather than technical implementation

**MANDATORY STANDARDS**:
- Include "UI Alert Messages" sections for ANY alerts, popups, validation messages
- Use ONLY new Source Code Details format: Primary Location/Secondary Location/External Dependencies (separate lines)
- Business-friendly language (no method calls or technical properties)
- Document ALL UI text in **bold quotes**

Follow the Cross-Module Dependencies template in //project/ifm/templates/requirements_documentation_standards.md

Coordinate Rex to extract cross-module patterns, Mason to document dependencies with business-friendly language, Aria to map architectural integration points, Rita to validate insurance compliance across modules, and Vera to certify Phase 2 completeness.
```

---

## 🎯 **TEMPLATE 4: Policy Level Analysis**

**Use For**: Cross-LOB policy-level functionality analysis

```markdown
Douglas, I need you to orchestrate an IFI analysis for Policy Level functionality across the system.

**Scope**: Policy Level coverage and functionality analysis with cross-LOB implications and new endorsement workflow standards
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Focus**: Policy Level coverages, limits, and cross-LOB functionality

**Deliverable Requirement**:
Produce ONE consolidated policy level requirements document at:
//project/ifm/Policy_Level_Complete_Requirements.md

The document must:
- Document policy-level coverages that apply across multiple LOBs
- Apply new endorsement workflow format for policy-level endorsements and complex components
- Use business-friendly language throughout (no method calls or technical properties)
- Identify cross-LOB policy management functionality
- Include architecture considerations for policy-level integration
- Include insurance compliance validation for policy-level requirements
- Follow updated documentation standards with new endorsement workflow format

**MANDATORY STANDARDS**:
- Include "UI Alert Messages" sections for ANY alerts, popups, validation messages, or system notifications
- Use ONLY new Source Code Details format: Primary Location/Secondary Location/External Dependencies (separate lines)
- Apply endorsement workflow: Field Specifications → User Selections/Interactions → Downstream Impacts → UI Alert Messages → Source Code Details
- Business-friendly language (no method calls or technical properties)
- Exclude IgnoreForLists="Yes" data
- Document ALL UI text in **bold quotes**

**Cross-LOB Considerations**:
- Document how policy-level functionality applies across WCP, BOP, CGL, Personal Lines
- Identify shared policy components vs LOB-specific policy elements
- Analyze policy-level integration points with LOB-specific functionality
- Use business language to describe cross-LOB workflow impacts

**Cross-System Impact Requirements**:
- Document downstream user actions required in other modules for policy-level selections
- Map workflow completion requirements across LOBs
- Identify integration touchpoints and data flows between policy-level and LOB-specific modules

Coordinate the team to produce comprehensive policy-level documentation with business-friendly language that serves as foundation for policy management across all lines of business.
```

---

## 🎯 **TEMPLATE 5: Cross-System Integration Analysis Enhancement**

**Use For**: After initial analysis is complete and you're satisfied with the document quality
**Purpose**: Add cross-system impact analysis to existing excellent documentation
**Result**: Creates new enhanced file (preserves original unchanged)

```markdown
Douglas, I need you to enhance an existing requirements document with cross-system integration analysis.

**Source Document to Enhance**: [SPECIFY PATH - e.g., //project/ifm/policy_level_coverages_Requirements.md]

**Output File**: Create new file with same name + "_cross_system.md" suffix
**Example Output**: //project/ifm/policy_level_coverages_Requirements_cross_system.md

**CRITICAL INSTRUCTIONS**:
- BUILD ON the existing document structure (don't start fresh)
- PRESERVE ALL existing content, tables, matrices, formatting, and section numbering  
- MAINTAIN all professional presentation and quality standards
- ADD "Cross-System Impact Analysis" as NEW subsections after "Selection Impact Analysis" where relevant
- This is SUPPLEMENTAL enhancement, not replacement

**Cross-System Integration Focus**:
- Document downstream consequences in other system modules (Application, Billing, Claims, Endorsements, Rating)
- For each major user selection, identify what additional work is created elsewhere in the system  
- Example pattern: "Selection made in [CURRENT MODULE] → Required follow-up action in [OTHER MODULE]"
- Focus on cross-module workflow implications and user journey completion requirements
- Include integration touchpoints where data flows between system components

**Business Language Requirements**:
- Use stakeholder-friendly language for all cross-system impact descriptions
- Convert technical integration details to business workflow implications
- Focus on user actions required in other modules rather than technical implementation details

**MANDATORY STANDARDS**:
- Include "UI Alert Messages" sections for ANY alerts, popups, validation messages
- Use ONLY new Source Code Details format: Primary Location/Secondary Location/External Dependencies (separate lines)
- Business-friendly language (no method calls or technical properties)
- Document ALL UI text in **bold quotes**

Coordinate the team to enhance the existing excellent documentation by adding comprehensive cross-system integration analysis while preserving all existing quality and formatting.
```

**Usage Notes**:
- Use only after reviewing and approving initial analysis
- Original document remains unchanged for safety
- Compare both versions to determine which serves stakeholder needs best

---

## 📝 **PROMPT CUSTOMIZATION GUIDELINES**

### **Required Elements in Every Prompt:**
1. **Clear Scope Definition**: Exactly what you want analyzed
2. **Source Code Location**: Always specify the VelociRater path
3. **Workspace**: Always //project/ifm/
4. **Deliverable Path**: Specific output file location
5. **Business Language Requirements**: Transformation of technical findings to stakeholder language
6. **New Standards Reference**: Reference to updated documentation standards and endorsement workflow format

### **New Standard Elements (Add to All Prompts):**
- **Endorsement Workflow Format**: User Selections/Interactions → Downstream Impacts structure
- **Business Language Transformation**: No method calls or technical properties in business descriptions
- **Data Exclusion**: Exclude IgnoreForLists="Yes" items from documentation
- **Cross-System Impact**: Document downstream user actions required in other modules
- **Standardized Source Code Format**: Primary/Secondary/External Dependencies structure

### **Optional Elements (Add as Needed):**
- **Existing Work Reference**: Point to prior analysis if building on previous work
- **Specific Focus Areas**: Narrow scope to particular functionality
- **Quality Requirements**: Special quality considerations
- **Integration Points**: Specific cross-module or cross-LOB requirements

---

## 🎯 **QUICK REFERENCE: Updated Analysis Types**

### **Full LOB Analysis** → Use Template 1
- Complete system coverage for entire LOB
- New endorsement workflow format applied to endorsements and complex components
- Business-friendly language throughout
- Cross-functional team coordination

### **Feature-Specific Analysis** → Use Template 2  
- Focused on specific functionality area
- Component analysis with new workflow standards
- Cross-system impact documentation
- Targeted team coordination

### **Cross-Module Analysis** → Use Template 3
- Phase 2 analysis after Phase 1 completion
- Focus on integration points and dependencies
- Business language for cross-module workflows
- Integration workflow documentation

### **Policy Level Analysis** → Use Template 4
- Cross-LOB policy functionality
- Policy-level endorsement analysis with new workflow format
- Enterprise-level policy coordination
- Cross-LOB workflow implications

### **Integration Enhancement** → Use Template 5
- Supplemental analysis for existing documents
- Cross-system impact analysis addition
- Preserves original document quality
- Downstream workflow documentation

---

## ✅ **SUCCESS INDICATORS**

**Proper Prompt Results In:**
- Clear deliverable with specified file name and location
- Appropriate application of new endorsement workflow format
- Business-friendly language throughout (no technical method calls)
- Professional stakeholder-ready documentation
- Complete source code traceability with standardized format
- Cross-system impact analysis with downstream user action requirements
- Integrated team outputs in single consolidated document

**Quality Output Includes:**
- Endorsement workflow specifications using User Selections/Interactions → Downstream Impacts format
- Business language transformation of technical findings
- Standardized Source Code Details format (Primary/Secondary/External)
- Complete evidence backing with zero speculation
- Cross-system workflow implications documented
- Insurance compliance validation and architecture integration
- Exclusion of IgnoreForLists="Yes" data from user-facing documentation

Use these updated templates to ensure consistent, high-quality IFI analysis deliverables with business-friendly language, proper endorsement workflow documentation, and comprehensive cross-system impact analysis while maintaining streamlined documentation standards.

---

## 🔗 **TEMPLATE REFERENCE**

All templates reference the updated standards at:
- **//project/ifm/templates/requirements_documentation_standards.md** (Updated with endorsement analysis standard)
- **//project/ifm/templates/endorsement_analysis_template.md** (Complete reference template with examples)
- **//project/ifm/templates/Agent_System_Extraction_Checklist.md** (Updated extraction guidance)

These templates ensure consistent application of the new endorsement workflow format and business language standards across all analysis types.