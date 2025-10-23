# BOKF Clone Delegation Patterns

## Core Clone Delegation Principles

**Universal Rules Across All Agents**:
- **15-30 minute task sizing**: Optimal clone task duration
- **Single-focus deliverable**: One specific output per clone
- **Strict fallback protocol**: Execute only single step if clone fails
- **Mandatory subtask tracking**: Track all delegations for recovery
- **Context compression**: Summarize outputs for next clone

---

## Phase 2: Domain Analysis (Dominic)

### Clone Delegation Strategy

**Pattern**: Sequential domain processing with clone delegation per domain

**Per-Domain Clone Usage**:

**Step 1: Requirements Extraction** (15-20 minutes)
- **Clone Task**: Extract all requirements for assigned domain from master document
- **Input**: `//output/BOKF_Enterprise_Requirements_Master.md`
- **Output**: Domain-specific requirements list
- **Deliverable**: Structured requirement list with IDs and categories

**Step 2: Capability Grouping** (20-30 minutes)
- **Clone Task**: Group related requirements into logical business capabilities
- **Input**: Domain requirements list from Step 1
- **Output**: Initial capability definitions with requirement mappings
- **Deliverable**: Capability map with requirement traceability

**Step 3: Cross-Domain Analysis** (15-25 minutes)
- **Clone Task**: Review integration points with previously completed domains
- **Input**: Current domain capabilities + previous domain metadata
- **Output**: Cross-domain opportunity matrix for current domain
- **Deliverable**: Integration points and shared capability opportunities

**Step 4: Business Value Assessment** (20-30 minutes)
- **Clone Task**: Assess business criticality and modernization value per capability
- **Input**: Domain capability map
- **Output**: Business value scores and modernization priorities
- **Deliverable**: Prioritized capability list with business justification

**Step 5: Stakeholder Materials** (20-30 minutes)
- **Clone Task**: Create business-friendly validation scenarios and visual models
- **Input**: Domain capabilities with business value
- **Output**: Stakeholder validation package
- **Deliverable**: Non-technical capability descriptions, test scenarios, process flows

### Clone Coordination Per Domain

**Total Clones Per Domain**: 5 sequential clones
**Domain Processing Time**: 90-150 minutes of clone work + coordination overhead
**Context Handoff**: Each clone receives compressed output from previous clone

**Fallback Protocol**:
- If clone fails at Step 3: Execute only "Extract integration points from first 2 completed domains"
- Document failure, update subtask tracking, return control to orchestrator

---

## Phase 4: Technical Analysis (Tina)

### Clone Delegation Strategy

**Pattern**: Multi-clone coordination with decomposition for complex analysis

### 4.1 Legacy Constraint Analysis (7 steps)

**Step CONS-TA-ANAL-001**: Analyze Architecture Patterns (30 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (15 min): Extract patterns from DOM-01, DOM-02, DOM-03
  - **Clone B** (15 min): Extract patterns from DOM-04, DOM-05, DOM-06
  - **Clone C** (15 min): Extract patterns from DOM-07, DOM-08, DOM-09
  - **Clone D** (15 min): Extract patterns from DOM-10, DOM-11
  - **Clone E** (20 min): Consolidate patterns from A, B, C, D outputs
- **Aggregation**: Unified architecture pattern inventory

**Step CONS-TA-ANAL-002**: Identify Anti-Patterns (25 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (20 min): Analyze anti-patterns in authentication/authorization
  - **Clone B** (20 min): Analyze anti-patterns in data access layers
  - **Clone C** (20 min): Analyze anti-patterns in workflow management
  - **Clone D** (15 min): Consolidate anti-pattern findings
- **Aggregation**: Comprehensive anti-pattern catalog

**Step CONS-TA-ANAL-003**: Map Technical Debt to Business Impact (30 minutes)
- **Single Clone**: 30-minute focused analysis
- **Input**: Architecture patterns + anti-patterns from previous steps
- **Output**: Technical debt inventory with business impact scores

**Steps CONS-TA-ANAL-004 through CONS-TA-ANAL-007**: Similar patterns
- Each step: 1-3 clones depending on complexity
- Sequential coordination when outputs depend on previous analysis
- Parallel coordination when analyzing independent aspects

### 4.2 Modernization Opportunity Identification (8 steps)

**Step CONS-TA-SYNTH-001**: Cloud-Native Opportunities (30 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (20 min): Identify containerization opportunities
  - **Clone B** (20 min): Identify serverless function opportunities
  - **Clone C** (20 min): Identify managed service opportunities
  - **Clone D** (15 min): Synthesize cloud-native strategy
- **Aggregation**: Prioritized cloud-native modernization roadmap

**Step CONS-TA-SYNTH-002**: Microservices Decomposition (35 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (20 min): Analyze bounded contexts in domains 1-4
  - **Clone B** (20 min): Analyze bounded contexts in domains 5-8
  - **Clone C** (20 min): Analyze bounded contexts in domains 9-11
  - **Clone D** (20 min): Design microservice boundaries
  - **Clone E** (15 min): Create decomposition roadmap
- **Aggregation**: Microservice architecture proposal with migration path

**Steps CONS-TA-SYNTH-003 through CONS-TA-SYNTH-008**: Similar patterns
- Complex synthesis steps use 3-5 clones
- Each clone: 15-20 minute focused task
- Final aggregation clone: 15-20 minutes to synthesize

### 4.3 Technical Modernization Principles (6 steps)

**Step CONS-TA-VALID-001**: Enterprise Architecture Principles (25 minutes)
- **Single Clone**: 25-minute focused research and synthesis
- **Input**: Modernization opportunities from phase 4.2
- **Output**: Enterprise architecture principles document

**Steps CONS-TA-VALID-002 through CONS-TA-VALID-006**: Similar patterns
- Most validation steps: 1-2 clones
- 20-30 minute duration per clone
- Focus on synthesis and validation rather than analysis

### Clone Load Management Strategy

**Prevents Overload**:
- ❌ Never assign "Analyze all 11 domains" (too big)
- ✅ Assign "Extract patterns from DOM-01, DOM-02, DOM-03" (right size)

**Task Decomposition Example**:
```
Large Task: "Create complete technical debt analysis"
Decomposed Into:
- Clone 1: Extract debt from domains 1-3
- Clone 2: Extract debt from domains 4-6
- Clone 3: Extract debt from domains 7-9
- Clone 4: Extract debt from domains 10-11
- Clone 5: Consolidate findings into unified analysis
```

---

## Phase 6: Consolidation Management (Tina)

### Clone Delegation Strategy

**Pattern**: Step-by-step consolidation with multi-clone coordination

### 6.1 Cross-Domain Coordination (10 steps)

**Step CONS-CD-ANAL-001**: Monitor Domain Progress (20 minutes)
- **Single Clone**: Collect and synthesize progress data
- **Input**: Metadata from all domain analyses
- **Output**: Progress summary with completion status

**Step CONS-CD-ANAL-003**: Resolve Capability Conflicts (40 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (25 min): Identify conflicting capabilities between domains
  - **Clone B** (25 min): Analyze conflict root causes and business impact
  - **Clone C** (20 min): Propose resolution strategies
  - **Clone D** (20 min): Create conflict resolution decision matrix
  - **Clone E** (15 min): Document final resolutions
- **Aggregation**: Conflict-free capability registry

**Step CONS-CD-ANAL-004**: Facilitate Shared Capabilities (35 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (20 min): Group authentication-related capabilities
  - **Clone B** (20 min): Group data access capabilities
  - **Clone C** (20 min): Group workflow management capabilities
  - **Clone D** (20 min): Group reporting capabilities
  - **Clone E** (15 min): Create shared capability registry
- **Aggregation**: Prioritized shared capability opportunities

**Steps CONS-CD-ANAL-005 through CONS-CD-ANAL-010**: Similar patterns
- Complex coordination: 3-5 clones (40-50 minutes total)
- Simple coordination: 1-2 clones (20-30 minutes total)

### 6.2 Consolidation Opportunity Analysis (9 steps)

**Step CONS-CD-SYNTH-004**: Design Shared Service Architecture (50 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (25 min): Design authentication shared service from identified capabilities
  - **Clone B** (25 min): Design data access shared service
  - **Clone C** (25 min): Design workflow shared service
  - **Clone D** (25 min): Design reporting shared service
  - **Clone E** (20 min): Design integration layer between shared services
  - **Clone F** (15 min): Create unified shared service architecture
- **Aggregation**: Complete shared service architecture with integration patterns

**Steps CONS-CD-SYNTH-005 through CONS-CD-SYNTH-009**: Similar patterns
- Architecture design steps: 4-6 clones (50-70 minutes total)
- Roadmap creation steps: 2-3 clones (30-40 minutes total)

### 6.3 Quality Assurance and Validation (8 steps)

**Step CONS-CD-VALID-001**: Review Domain Outputs (40 minutes)
- **Multi-Clone Decomposition**:
  - **Clone A** (20 min): Quality assessment domains 1-3
  - **Clone B** (20 min): Quality assessment domains 4-6
  - **Clone C** (20 min): Quality assessment domains 7-9
  - **Clone D** (20 min): Quality assessment domains 10-11
  - **Clone E** (15 min): Consolidated quality report
- **Aggregation**: Comprehensive quality assessment with remediation recommendations

**Steps CONS-CD-VALID-002 through CONS-CD-VALID-008**: Similar patterns
- Validation steps: 3-5 clones (40-60 minutes total)
- Focus on quality verification and stakeholder readiness

---

## Clone Delegation Metadata Tracking

**Structure**: `//[workspace]/meta/[agent_area]/subtask_tracking/`

**Active Delegations**:
```
delegation_id: "CLONE-DOM-01-REQ-EXTRACT"
assigned_clone_task: "Extract all requirements for DOM-01"
delegation_timestamp: ISO timestamp
expected_completion: "15 minutes"
delegation_status: "completed"
deliverable_location: "//bokf_source/meta/domain_analysis/DOM-01/requirements/"
```

**Failed Delegations**:
```
delegation_id: "CLONE-TA-ARCH-ALL"
failure_reason: "Task too large - analyzing all 11 domains simultaneously"
fallback_action_taken: "Extracted architecture patterns from DOM-01 only"
recovery_requirements: "Decompose into 4 smaller tasks (DOM 1-3, 4-6, 7-9, 10-11)"
```

---

## Clone Delegation Success Metrics

**Optimal Task Characteristics**:
- ✅ 15-30 minute duration
- ✅ Single specific deliverable
- ✅ 1-3 input sources
- ✅ Clear output format
- ✅ Measurable completion criteria

**Red Flags (Overload Indicators)**:
- ❌ Multiple deliverables in one task
- ❌ >30 minute estimated duration
- ❌ >5 input sources
- ❌ Vague or compound objectives

**Recovery Protocol**:
1. Acknowledge failure immediately
2. Evaluate if task was too large
3. Decompose into smaller tasks if needed
4. Execute single fallback step only
5. Update subtask tracking
6. Return control with resumption guidance
