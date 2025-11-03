# Prompts for Douglas - IFI Analysis Requests

This document provides standardized prompt templates for requesting various types of IFI analysis from Douglas. Use these templates to ensure consistent, high-quality deliverables with appropriate enhanced UI specifications.

---

## 🎯 **TEMPLATE 1: Complete LOB Analysis**

**Use For**: Full Line of Business analysis with enhanced UI capabilities

```markdown
Douglas, I need you to orchestrate a complete IFI analysis for the [LOB NAME] Line of Business.

**Scope**: Complete [LOB NAME] system analysis with enhanced UI specifications for complex components
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Line of Business**: [LOB NAME]

**Deliverable Requirement**:
Produce ONE consolidated requirements document at:
//project/ifm/[LOB]_Complete_Requirements.md

The document must:
- Transform Rex's technical pattern extraction into business-friendly requirements
- Apply Enhanced UI Analysis for complex components (modals, dynamic forms, validation-heavy interfaces)
- Integrate Aria's architecture analysis as subsections within relevant features
- Integrate Rita's insurance compliance validation as notes where applicable
- Include Vera's quality certification as the final section
- Follow the updated documentation standards at //project/ifm/templates/requirements_documentation_standards.md
- Have NO "Business Purpose" sections
- have NO "Executive Summary" sections

**Enhanced UI Requirements**:
- Apply Enhanced UI Analysis to complex components (kill questions, endorsement workflows, rating interfaces, etc.)
- Use standard documentation for simple fields (basic dropdowns, text inputs)
- Follow Enhanced UI template from documentation standards for complex interactions

Coordinate the team through the sequential IFI workflow to produce a single comprehensive stakeholder-ready deliverable that covers all [LOB NAME] functionality with appropriate enhanced UI specifications for complex components.
```

**Example LOB Names**: Workers' Compensation (WCP), Business Owners Policy (BOP), Commercial General Liability (CGL), Personal Auto, Homeowners

---

## 🎯 **TEMPLATE 2: Specific Feature Analysis**

**Use For**: Focused analysis on specific system features or modules

```markdown
Douglas, I need you to orchestrate a focused IFI analysis for [SPECIFIC FEATURE/MODULE] in the [LOB NAME if applicable] system.

**Scope**: [SPECIFIC FEATURE] analysis with enhanced UI specifications for complex components
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Focus Area**: [SPECIFIC FEATURE/MODULE NAME]

**Deliverable Requirement**:
Produce ONE focused requirements document at:
//project/ifm/[FEATURE]_Requirements.md

The document must:
- Focus exclusively on [SPECIFIC FEATURE] functionality
- Apply Enhanced UI Analysis for any complex UI components within this feature
- Transform technical patterns into business-friendly requirements
- Include architecture considerations and insurance compliance notes as subsections
- Follow updated documentation standards with enhanced UI specifications where applicable
- Have NO "Business Purpose" sections
- Have NO "Executive Summary" sections

**Enhanced UI Focus**:
- Identify complex UI components within [SPECIFIC FEATURE] (modals, dynamic workflows, etc.)
- Apply Enhanced UI Analysis template for complex interactions
- Use standard documentation for simple field components
- Ensure complete UI interaction specification for stakeholder implementation

Coordinate the team to produce comprehensive [SPECIFIC FEATURE] documentation with appropriate enhanced UI specifications.
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
- Business rule connecting the modules
- Validation impact (if any)
- Source code evidence with file/line references for BOTH modules

**Enhanced UI Considerations**:
- Apply Enhanced UI Analysis to complex cross-module UI interactions
- Document UI behavior that spans multiple modules
- Focus on user actions in [LOB NAME] that trigger UI changes in other modules

Follow the Cross-Module Dependencies template in //project/ifm/templates/requirements_documentation_standards.md

Coordinate Rex to extract cross-module patterns, Mason to document dependencies, Aria to map architectural integration points, Rita to validate insurance compliance across modules, and Vera to certify Phase 2 completeness.
```

---

## 🎯 **TEMPLATE 4: Enhanced UI Focused Analysis**

**Use For**: Detailed analysis of specific complex UI components requiring enhanced documentation

```markdown
Douglas, I need you to orchestrate a focused Enhanced UI Analysis for [SPECIFIC UI COMPONENT] in the [LOB NAME/SYSTEM AREA].

**Scope**: Enhanced UI interaction analysis for [SPECIFIC UI COMPONENT]
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**UI Component Focus**: [SPECIFIC UI COMPONENT NAME]

**Deliverable Requirement**:
Produce enhanced UI specification document at:
//project/ifm/[COMPONENT]_Enhanced_UI_Specifications.md

**Enhanced UI Analysis Requirements**:
- Complete user interaction flow documentation
- Visual state transition mapping (normal → error → recovery)
- Error recovery workflow analysis
- Progressive disclosure pattern documentation
- Source code evidence for all UI behavior (JavaScript + backend)

**Component Analysis Focus**:
- Document every user action and immediate system response
- Capture all visual feedback patterns (color changes, border states, label dynamics)
- Map complete error identification and resolution workflows
- Identify all dynamic field interactions (show/hide/enable logic)
- Document validation timing (real-time vs submit-time)

Coordinate Rex for enhanced UI pattern extraction, Mason for enhanced UI requirements documentation using the Enhanced UI template, and Vera for enhanced UI quality certification.

Focus exclusively on [SPECIFIC UI COMPONENT] with complete enhanced UI specification for stakeholder implementation confidence.
```

**Example UI Components**: Kill Questions Modal, Endorsement Selection Workflow, Coverage Selection Matrix, Rating Calculation Interface, Application Data Wizard

---

## 🎯 **TEMPLATE 5: Policy Level Analysis**

**Use For**: Cross-LOB policy-level functionality analysis

```markdown
Douglas, I need you to orchestrate an IFI analysis for Policy Level functionality across the system.

**Scope**: Policy Level coverage and functionality analysis with cross-LOB implications
**Source Code Location**: //project/ifm/source-code/Primary Source Code/WebSystems_VelociRater/
**Workspace**: //project/ifm/
**Focus**: Policy Level coverages, limits, and cross-LOB functionality

**Deliverable Requirement**:
Produce ONE consolidated policy level requirements document at:
//project/ifm/Policy_Level_Complete_Requirements.md

The document must:
- Document policy-level coverages that apply across multiple LOBs
- Apply Enhanced UI Analysis for complex policy-level UI components
- Identify cross-LOB policy management functionality
- Include architecture considerations for policy-level integration
- Include insurance compliance validation for policy-level requirements
- Follow updated documentation standards with enhanced UI specifications where applicable

**Enhanced UI Focus for Policy Level**:
- Coverage selection matrices with dynamic interactions
- Policy limit selection workflows with interdependencies  
- Premium calculation interfaces with real-time feedback
- Policy management workflows (renewal, endorsement, cancellation)

**Cross-LOB Considerations**:
- Document how policy-level functionality applies across WCP, BOP, CGL, Personal Lines
- Identify shared policy components vs LOB-specific policy elements
- Analyze policy-level integration points with LOB-specific functionality

Coordinate the team to produce comprehensive policy-level documentation that serves as foundation for policy management across all lines of business.
```

---

## 📝 **PROMPT CUSTOMIZATION GUIDELINES**

### **Required Elements in Every Prompt:**
1. **Clear Scope Definition**: Exactly what you want analyzed
2. **Source Code Location**: Always specify the VelociRater path
3. **Workspace**: Always //project/ifm/
4. **Deliverable Path**: Specific output file location
5. **Enhanced UI Requirements**: When to apply enhanced vs standard documentation
6. **Documentation Standards**: Reference to updated templates

### **Optional Elements (Add as Needed):**
- **Existing Work Reference**: Point to prior analysis if building on previous work
- **Specific Focus Areas**: Narrow scope to particular functionality
- **Quality Requirements**: Special quality considerations
- **Integration Points**: Specific cross-module or cross-LOB requirements

### **Enhanced UI Trigger Language:**
Always include this language for enhanced UI capability:

```markdown
**Enhanced UI Requirements**:
- Apply Enhanced UI Analysis to complex components (modals, dynamic forms, validation-heavy interfaces)
- Use standard documentation for simple fields (basic dropdowns, text inputs)
- Follow Enhanced UI template from documentation standards for complex interactions
```

---

## 🎯 **QUICK REFERENCE: Analysis Types**

### **Full LOB Analysis** → Use Template 1
- Complete system coverage for entire LOB
- Enhanced UI applied to complex components throughout
- Cross-functional team coordination

### **Feature-Specific Analysis** → Use Template 2  
- Focused on specific functionality area
- Enhanced UI applied to complex components within feature
- Targeted team coordination

### **Cross-Module Analysis** → Use Template 3
- Phase 2 analysis after Phase 1 completion
- Focus on integration points and dependencies
- Enhanced UI for cross-module interactions

### **UI-Focused Analysis** → Use Template 4
- Deep dive on specific complex UI components
- Complete enhanced UI specification
- UI-specialized team coordination

### **Policy Level Analysis** → Use Template 5
- Cross-LOB policy functionality
- Enhanced UI for complex policy management interfaces
- Enterprise-level policy coordination

---

## ✅ **SUCCESS INDICATORS**

**Proper Prompt Results In:**
- Clear deliverable with specified file name and location
- Appropriate application of enhanced UI analysis (not over-applied)
- Professional stakeholder-ready documentation
- Complete source code traceability
- Integrated team outputs in single consolidated document

**Quality Output Includes:**
- Enhanced UI specifications for complex components (10-20% of UI documentation)
- Standard documentation for simple components (80-90% of UI documentation)
- Professional formatting following updated documentation standards
- Complete evidence backing with zero speculation
- Insurance compliance validation and architecture integration

Use these templates to ensure consistent, high-quality IFI analysis deliverables with appropriate enhanced UI specifications for complex components while maintaining streamlined documentation for standard system elements.