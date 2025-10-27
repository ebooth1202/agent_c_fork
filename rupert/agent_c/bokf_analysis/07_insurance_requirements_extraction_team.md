# Insurance Requirements Extraction Team Design

## Client Challenge Overview

**System**: Legacy .NET insurance underwriting system
**Domains**: Multiple insurance product lines (WCP, BOP, CGL, etc.)
**Complexity**: Similar methods/functions across domains with domain-specific implementations
**Objective**: Accurate requirement extraction (NOT modernization)
**Critical Challenge**: Patterns don't carry between domains - must handle domain-specific variations

---

## Key Design Constraints

### Pattern Variation Challenge

**Similar Functions, Different Logic**:
```
Example across domains:
- CalculatePremium() exists in WCP, BOP, CGL
- Each has different rating factors, tables, rules
- Cannot assume WCP patterns apply to BOP
- Must extract requirements independently per domain
```

**Accuracy Requirements**:
- Domain-specific business rules must not be conflated
- Rating algorithms vary by product line
- Regulatory requirements differ by insurance type
- Underwriting criteria unique per domain

---

## Recommended Team Architecture

### Team Structure: Sequential Domain Extraction with Verification

**Pattern**: Modified Dominic pattern with enhanced accuracy focus

```
Primary Orchestrator: Insurance Requirements Coordinator
├── Domain Extraction Specialist (ONE domain at a time)
├── Accuracy Validator (cross-check extracted requirements)
└── Pattern Variation Tracker (document domain differences)
```

---

## Agent 1: Insurance Requirements Coordinator (Primary Orchestrator)

### Role
Sequential orchestration of domain-by-domain requirement extraction with accuracy validation gates

### Key Responsibilities
- Assign domains sequentially to extraction specialist
- Enforce strict domain isolation (prevent cross-contamination)
- Coordinate accuracy validation after each domain
- Track pattern variations across domains
- Manage context compression between domains
- Quality gate enforcement before domain completion

### Coordination Pattern
```
Coordinator → Domain Extraction Specialist (WCP)
  ↓
Accuracy Validator reviews WCP extraction
  ↓
Pattern Tracker documents WCP-specific patterns
  ↓
Coordinator quality gate validation
  ↓
Coordinator → Domain Extraction Specialist (BOP)
  ↓
[Repeat for each domain]
```

### Configuration Highlights
```yaml
name: "Insurance Requirements Coordinator"
category: ["insurance", "requirements_extraction", "orchestrator"]
coordination_pattern: "Sequential domain processing with accuracy gates"
primary_workspace: "insurance_source"

critical_rules:
  - ONE domain at a time (strict isolation)
  - No cross-domain assumption propagation
  - Accuracy validation mandatory per domain
  - Pattern variation documentation required
  - Context compression between domains
```

---

## Agent 2: Domain Extraction Specialist

### Role
Extract requirements from single insurance domain with domain-specific pattern recognition

### Key Responsibilities
- Process ONE insurance domain per assignment
- Extract business rules, rating logic, underwriting criteria
- Identify domain-specific patterns and variations
- Document regulatory requirements per domain
- Create domain-specific requirement catalog
- Use clone delegation for detailed code analysis (15-30 min tasks)

### Per-Domain Extraction Workflow

**Phase 1: Domain Code Inventory** (2-3 hours)
- **Clone Task 1** (20 min): Catalog all classes/files for domain
- **Clone Task 2** (25 min): Map domain entry points and workflows
- **Clone Task 3** (20 min): Identify domain-specific configuration/data
- **Output**: Complete code inventory for domain

**Phase 2: Business Rule Extraction** (4-6 hours)
- **Clone Task 1** (25 min): Extract premium calculation rules
- **Clone Task 2** (30 min): Extract underwriting decision logic
- **Clone Task 3** (25 min): Extract rating factor tables/algorithms
- **Clone Task 4** (20 min): Extract policy validation rules
- **Clone Task 5** (25 min): Extract commission calculation rules
- **Clone Task 6** (20 min): Consolidate business rules
- **Output**: Domain business rule catalog

**Phase 3: Regulatory & Compliance Requirements** (2-3 hours)
- **Clone Task 1** (25 min): Extract state-specific requirements
- **Clone Task 2** (20 min): Extract compliance validation rules
- **Clone Task 3** (25 min): Extract audit/reporting requirements
- **Clone Task 4** (20 min): Document regulatory traceability
- **Output**: Domain compliance requirement catalog

**Phase 4: Data & Integration Requirements** (2-3 hours)
- **Clone Task 1** (20 min): Extract data model for domain
- **Clone Task 2** (25 min): Extract external integration points
- **Clone Task 3** (20 min): Extract internal system dependencies
- **Clone Task 4** (20 min): Document data flows
- **Output**: Domain data/integration requirement catalog

**Phase 5: Domain Pattern Documentation** (1-2 hours)
- **Clone Task 1** (25 min): Document domain-specific patterns
- **Clone Task 2** (20 min): Identify variations from other domains
- **Clone Task 3** (20 min): Create domain pattern summary
- **Output**: Domain pattern variation document

### Configuration Highlights
```yaml
name: "Insurance Domain Extraction Specialist"
category: ["insurance", "domain_analysis", "requirements_extraction"]
coordination_pattern: "Clone delegation with accuracy focus"
primary_workspace: "insurance_source"

critical_rules:
  - Focus on single assigned domain only
  - No cross-domain assumptions
  - Clone tasks 15-30 minutes maximum
  - Verify every extracted requirement against code
  - Document domain-specific variations
  - Flag uncertainties for validation
```

### Domain-Specific Extraction Strategy

**Workers Compensation (WCP)**:
```
Focus Areas:
- State-specific rating laws
- Industry/class code rating
- Experience modification calculations
- Loss history impact on premium
- Medical-only claims vs. indemnity
```

**Business Owner's Policy (BOP)**:
```
Focus Areas:
- Package policy bundling rules
- Building/contents coverage calculations
- Business interruption formulas
- Liability limits and pricing
- Industry-specific endorsements
```

**Commercial General Liability (CGL)**:
```
Focus Areas:
- Occurrence vs. claims-made calculations
- Per-occurrence and aggregate limits
- Additional insured endorsements
- Aggregate tracking and reinstatement
- Classification-based rating
```

---

## Agent 3: Accuracy Validator

### Role
Validate extracted requirements against source code for accuracy and completeness

### Key Responsibilities
- Review extracted requirements per domain
- Cross-reference requirements against .NET source code
- Identify missing or incomplete requirements
- Validate business rule accuracy
- Flag ambiguities or uncertainties
- Approve domain extraction or request remediation

### Validation Workflow (per domain)

**Phase 1: Completeness Validation** (2-3 hours)
- **Clone Task 1** (25 min): Verify all domain classes covered
- **Clone Task 2** (25 min): Verify all public methods documented
- **Clone Task 3** (20 min): Verify configuration/data sources captured
- **Clone Task 4** (20 min): Identify gaps in extraction
- **Output**: Completeness assessment report

**Phase 2: Accuracy Validation** (3-4 hours)
- **Clone Task 1** (30 min): Validate premium calculation requirements vs. code
- **Clone Task 2** (30 min): Validate underwriting logic requirements vs. code
- **Clone Task 3** (25 min): Validate rating factor requirements vs. code
- **Clone Task 4** (25 min): Validate validation rule requirements vs. code
- **Clone Task 5** (20 min): Consolidate accuracy findings
- **Output**: Accuracy assessment with discrepancies

**Phase 3: Pattern Verification** (1-2 hours)
- **Clone Task 1** (25 min): Verify domain-specific patterns are accurate
- **Clone Task 2** (20 min): Verify no cross-domain contamination
- **Clone Task 3** (20 min): Document validation results
- **Output**: Pattern verification report

### Configuration Highlights
```yaml
name: "Insurance Requirements Accuracy Validator"
category: ["insurance", "validation", "quality_assurance"]
coordination_pattern: "Independent validation with source verification"
primary_workspace: "insurance_source"

critical_rules:
  - Independent review (don't rely on extraction output alone)
  - Cross-reference every requirement against code
  - Use clone delegation for detailed verification
  - Flag ANY uncertainty or ambiguity
  - Enforce accuracy thresholds before approval
```

### Validation Quality Gates

**Completeness Gate**:
- 100% of domain classes/files reviewed
- 95%+ of public methods documented
- 100% of configuration sources identified
- 90%+ of data flows traced

**Accuracy Gate**:
- 95%+ business rule accuracy vs. code
- 100% of critical calculations verified
- 95%+ regulatory requirements validated
- Zero contradictions with source code

---

## Agent 4: Pattern Variation Tracker

### Role
Document pattern variations across domains to prevent cross-contamination

### Key Responsibilities
- Track similar functions with different implementations
- Document domain-specific pattern variations
- Create cross-domain comparison matrices
- Flag high-risk areas for cross-contamination
- Maintain pattern variation knowledge base

### Pattern Tracking Workflow

**Per Domain Completion** (1-2 hours):
- **Task 1** (25 min): Identify common function patterns in domain
- **Task 2** (25 min): Compare patterns to previously analyzed domains
- **Task 3** (20 min): Document variations and differences
- **Task 4** (20 min): Update pattern variation matrix
- **Output**: Domain pattern variation document

### Configuration Highlights
```yaml
name: "Insurance Pattern Variation Tracker"
category: ["insurance", "pattern_analysis", "cross_domain"]
coordination_pattern: "Cross-domain analysis with variation focus"
primary_workspace: "insurance_source"

critical_rules:
  - Document ALL pattern variations
  - Never assume patterns carry across domains
  - Highlight high-risk similarity areas
  - Create clear differentiation guidance
  - Update knowledge base continuously
```

---

## Workflow: Sequential Domain Extraction

### Overall Process (per domain cycle)

```
Step 1: Domain Assignment (Coordinator)
  - Assign domain to Domain Extraction Specialist
  - Provide domain-specific focus areas
  - Initialize domain metadata structures

Step 2: Domain Extraction (Specialist)
  - Execute 5-phase extraction workflow
  - Use clone delegation (15-30 min tasks)
  - Document domain-specific patterns
  - Flag uncertainties for validation
  - Total: 11-17 hours per domain

Step 3: Accuracy Validation (Validator)
  - Execute 3-phase validation workflow
  - Cross-reference against source code
  - Identify gaps and inaccuracies
  - Total: 6-9 hours per domain

Step 4: Pattern Variation Documentation (Tracker)
  - Identify domain-specific patterns
  - Compare to previous domains
  - Document variations
  - Total: 1-2 hours per domain

Step 5: Quality Gate (Coordinator)
  - Review extraction completeness
  - Review accuracy validation results
  - Review pattern documentation
  - APPROVE or REQUEST REMEDIATION

Step 6: Context Compression (Coordinator)
  - Compress domain requirements for efficiency
  - Preserve pattern variation knowledge
  - Prepare for next domain

Step 7: Next Domain Assignment
  - Repeat for next insurance domain
```

### Domain Processing Sequence

**Recommended Order**:
1. **Workers Compensation (WCP)** - Most complex rating, establish baseline
2. **Commercial General Liability (CGL)** - Common patterns, identify variations
3. **Business Owner's Policy (BOP)** - Package complexity, cross-domain dependencies
4. **[Additional domains in order of business priority/complexity]**

### Timeline Estimates

**Per Domain**:
- Extraction: 11-17 hours (1.5-2 days)
- Validation: 6-9 hours (1 day)
- Pattern Documentation: 1-2 hours (0.25 day)
- Quality Gate: 2-3 hours (0.25 day)
- **Total per domain**: 20-31 hours (2.5-4 days)

**For 6 Insurance Domains**:
- **Total**: 120-186 hours (15-23 days, or 3-4.5 weeks)

---

## Workspace Architecture

### Workspace Structure

```
insurance_source (READ-ONLY):
  - Legacy .NET codebase
  - WCP domain code
  - BOP domain code
  - CGL domain code
  - [Additional domain code]
  - Configuration files
  - Database scripts

insurance_requirements (READ/WRITE):
  - Domain-specific requirement catalogs
  - Validation reports
  - Pattern variation documentation
  - Cross-domain comparison matrices
  - Final consolidated requirements
```

### Metadata Structure

```
//insurance_source/meta/
├── domain_extraction/
│   ├── WCP/
│   │   ├── business_rules/
│   │   ├── regulatory_requirements/
│   │   ├── data_requirements/
│   │   ├── integration_requirements/
│   │   └── domain_patterns/
│   ├── BOP/ [same structure]
│   ├── CGL/ [same structure]
│   └── [Additional domains]
├── accuracy_validation/
│   ├── WCP/
│   │   ├── completeness_report/
│   │   ├── accuracy_report/
│   │   └── validation_findings/
│   └── [Other domains]
├── pattern_variations/
│   ├── cross_domain_matrix/
│   ├── variation_knowledge_base/
│   └── high_risk_areas/
└── orchestration/
    ├── current_domain_assignment/
    ├── domain_progress_tracking/
    └── quality_gate_history/
```

---

## Critical Success Factors

### 1. Domain Isolation Discipline
- **NEVER assume patterns from one domain apply to another**
- Process each domain as if it's the first
- Use Pattern Variation Tracker to document differences
- Explicit validation that domain-specific logic is captured

### 2. Accuracy Over Speed
- Clone delegation for detailed analysis (prevents rushing)
- Independent validation mandatory
- Cross-reference every requirement against code
- Quality gates enforce accuracy thresholds

### 3. Uncertainty Management
- Flag ANY uncertainty during extraction
- Don't guess or assume
- Escalate ambiguities to subject matter experts
- Document assumptions explicitly

### 4. Context Compression Discipline
- Compress domain requirements after completion
- Preserve pattern variation knowledge
- Prevent context window burnout
- Enable efficient multi-domain processing

### 5. Clone Task Sizing
- 15-30 minute tasks (no larger)
- Single focused deliverable per clone
- Prevents overload and errors
- Enables accurate verification

---

## Quality Gates

### Per-Domain Quality Gate

**Gate Criteria**:
```
Completeness:
- [ ] 100% of domain classes/files reviewed
- [ ] 95%+ of public methods documented
- [ ] 100% of domain entry points traced
- [ ] 90%+ of data flows captured

Accuracy:
- [ ] 95%+ business rule accuracy validated
- [ ] 100% of critical calculations verified
- [ ] 95%+ regulatory requirements confirmed
- [ ] Zero code-requirement contradictions

Pattern Documentation:
- [ ] Domain-specific patterns documented
- [ ] Variations from other domains identified
- [ ] High-risk similarity areas flagged
- [ ] Cross-domain matrix updated

Validation:
- [ ] Independent validator approval
- [ ] All uncertainties resolved or escalated
- [ ] Pattern variation tracker approval
- [ ] Coordinator quality gate passed
```

**Gate Decision**:
- **PASS**: All criteria met, proceed to next domain
- **REMEDIATION**: Gaps identified, specialist re-extracts specific areas
- **FAIL**: Critical issues, restart domain extraction

---

## Risk Mitigation Strategies

### Risk 1: Cross-Domain Pattern Contamination
**Mitigation**:
- Strict sequential processing (one domain at a time)
- Pattern Variation Tracker documents differences
- Independent validation per domain
- Context compression isolates domain knowledge

### Risk 2: Requirement Inaccuracy
**Mitigation**:
- Clone delegation prevents rushing
- Independent accuracy validator
- Cross-reference against source code mandatory
- Quality gates enforce accuracy thresholds

### Risk 3: Missing Requirements
**Mitigation**:
- Completeness validation mandatory
- 100% code coverage requirement
- Multiple extraction phases (business, regulatory, data, integration)
- Validator identifies gaps

### Risk 4: Domain-Specific Complexity Underestimation
**Mitigation**:
- Process most complex domain first (WCP)
- Adjust timeline estimates based on first domain
- Build pattern variation knowledge progressively
- Escalation protocol for unexpected complexity

---

## Deliverables

### Per Domain
1. **Domain Requirement Catalog** (comprehensive)
   - Business rules
   - Regulatory requirements
   - Data requirements
   - Integration requirements
   
2. **Domain Pattern Document** (variations)
   - Domain-specific patterns
   - Variations from other domains
   - High-risk similarity areas
   
3. **Validation Report** (accuracy assurance)
   - Completeness assessment
   - Accuracy verification
   - Gap identification
   - Remediation tracking

### Final Consolidated
1. **Cross-Domain Requirements Master** (all domains)
   - All domain requirements consolidated
   - Cross-domain dependencies mapped
   - Pattern variation matrix complete
   
2. **Requirement Traceability Matrix**
   - Every requirement → source code location
   - Domain classification
   - Business criticality
   - Regulatory impact

---

## Adaptation from BOKF Patterns

**What's Different**:
- Focus on extraction accuracy (not modernization)
- Pattern variation is a FEATURE not a bug
- Domain isolation more critical than cross-domain integration
- Independent validation required per domain
- Completeness more critical than synthesis

**What's Similar**:
- Sequential domain processing (Dominic pattern)
- Clone delegation for detailed work
- Context compression between domains
- Quality gates at transitions
- Workspace safeguarding (read-only source)
- Metadata-based state management

**Key Insight**: This team prioritizes ACCURACY and DOMAIN ISOLATION over speed and cross-domain optimization, making it ideal for requirement extraction from complex domain-specific systems.
