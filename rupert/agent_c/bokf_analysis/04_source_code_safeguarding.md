# BOKF Source Code Safeguarding

## Workspace Segregation Strategy

**Primary Safeguard**: Complete workspace isolation between original source and modernization work

### Workspace Architecture

**Original Source Code** (READ-ONLY):
- **Workspace**: `bokf_source`
- **Purpose**: Contains original BOKF VB.NET codebase from client
- **Access Pattern**: Reference only, no modification
- **Security**: Agents read for analysis but never write to this workspace

**Modernization Work** (WRITE):
- **Workspace**: `bokf_design`
- **Purpose**: All new C# modernization development
- **Access Pattern**: Full read/write for modernization team
- **Security**: Isolated from original source code

**Database Schemas** (READ-ONLY):
- **Workspace**: `bokf_schema`
- **Purpose**: Database structure documentation from client
- **Access Pattern**: Reference for data model understanding
- **Security**: Read-only access, no modifications

**Polished Analysis Output** (READ-ONLY):
- **Workspace**: `output`
- **Purpose**: Final requirements and analysis documentation
- **Access Pattern**: Reference for requirements understanding
- **Security**: Read-only access to finalized deliverables

**Gatekeeper Specialized Work** (WRITE):
- **Workspace**: `gatekeeper`
- **Purpose**: Specialized Gatekeeper system modernization
- **Access Pattern**: Full read/write for Gatekeeper team
- **Security**: Isolated workspace for specific subsystem

---

## Access Control Patterns

### Agent Workspace Access Matrix

| Agent | bokf_source | bokf_design | bokf_schema | output | gatekeeper |
|-------|-------------|-------------|-------------|--------|------------|
| Douglas (Main) | READ | READ/WRITE | READ | READ | - |
| Douglas (Design Engine) | READ | READ/WRITE | READ | READ | - |
| Tina | READ | READ | READ | READ | - |
| Dominic | READ | READ | READ | READ | - |
| Douglas (Gatekeeper) | READ | - | READ | READ | READ/WRITE |

### Read-Only Enforcement

**Original Source Protection**:
- No agent has write access to `bokf_source` workspace
- All agents configured with primary workspace OTHER than `bokf_source`
- Analysis stored in metadata structures within agent workspaces
- Original code referenced via read operations only

**Metadata-Based Analysis Storage**:
```
SAFE: workspace_read("//bokf_source/originalfile.vb")
SAFE: workspace_read_meta("//bokf_source/meta/analysis/domain_01/")
UNSAFE: workspace_write("//bokf_source/...", data) ← NOT USED
```

---

## Competitive Intelligence Arsenal Safeguarding

### Rita's Enhanced Source Analysis

**Location**: `//bokf_source/.scratch/analyze_source/enhanced/`
**Content**: File-by-file analysis of original BOKF codebase
**Safeguarding**:
- Analysis stored SEPARATE from original code
- Located in `.scratch` subdirectory (analysis artifacts)
- Original files remain untouched
- Analysis provides understanding without source modification

**Access Pattern**:
```
READ: //bokf_source/.scratch/analyze_source/enhanced/[system]/[file_analysis].md
WRITE: //bokf_design/modernization/[new_code].cs
```

### Client Standards Repository

**Location**: Workspace metadata under `client_standards` key
**Content**: BOKF-specific coding conventions, security requirements, architecture preferences
**Safeguarding**:
- Stored in metadata structures, not in source code directories
- Agents read standards to inform modernization work
- Standards guide new code creation, don't modify old code

---

## Scratchpad and Trash Management

### Scratchpad Isolation

**Per-Agent Scratchpads**:
```
//bokf_design/.scratch  ← Douglas (Main), Douglas (Design Engine)
//bokf_source/.scratch  ← Tina, Dominic (for analysis artifacts only)
//gatekeeper/.scratch   ← Douglas (Gatekeeper)
```

**Safeguarding Rules**:
- Scratchpads in modernization workspaces (`bokf_design`, `gatekeeper`) - full access
- Scratchpad in `bokf_source` - analysis artifacts only, no source modification
- Each agent's scratchpad isolated from others
- No test scripts in scratchpads (testing elevated to user/specialized agents)

### Trash Management

**Trash Locations**:
```
//bokf_design/.scratch/trash  ← Modernization work trash
//bokf_source/.scratch/trash  ← Analysis artifacts trash (NOT source code)
//gatekeeper/.scratch/trash   ← Gatekeeper work trash
```

**Safeguarding Rules**:
- `workspace_mv` used to move outdated files to trash
- Original source code never moved to trash
- Only agent-generated artifacts moved to trash
- Trash directories provide recovery capability if needed

---

## Metadata-Based State Management

### Safeguarding Through Metadata

**Analysis Stored Separately**:
```
//bokf_source/meta/domain_analysis/[DOMAIN_ID]/  ← Domain analysis
//bokf_source/meta/technical_analysis_steps/     ← Technical debt analysis
//bokf_source/meta/consolidation_management_steps/ ← Consolidation work
//bokf_source/meta/orchestrator/                 ← Orchestration state
```

**Benefits**:
- Original source code remains untouched in main workspace
- All analysis, state, and coordination in metadata structures
- Clear separation between reference material and analysis outputs
- Metadata can be cleared without affecting original source

### Context Compression Safeguarding

**Context Storage Locations**:
```
//bokf_design/meta/orchestration_workflow/context_compression/
//bokf_source/meta/domain_analysis/[DOMAIN_ID]/context_compression/
```

**Safeguarding**:
- Compressed context stored in metadata, not mixed with source
- Context packages contain analysis insights, not source code copies
- Progressive summarization reduces need for repeated source access
- Context restoration uses metadata, not source file re-reading

---

## Gatekeeper Specialized Safeguarding

### Additional Safeguards for Financial Systems

**Shawn Wallace Authority Protocol**:
- Mandatory signoff for all work phases
- No code changes without technical authority approval
- Approval batching prevents unauthorized changes
- Complete audit trail of all modifications

**Scope Boundary Enforcement**:
- "SMALL M" modernization constraints strictly enforced
- No database schema changes (database structure protected)
- No API contract changes (external interfaces protected)
- No infrastructure modifications (deployment environment protected)

**Licensing Safeguards**:
- Zero tolerance for new licensed dependencies
- BOKF shared library usage required (prevents unauthorized libraries)
- All new dependencies must be approved license types
- Prevents introduction of IP risk or compliance violations

---

## Traceability and Audit Trail

### Complete Traceability Chain

**Requirements to Delivery**:
```
Original Requirements (output workspace, READ-ONLY)
  ↓
Domain Analysis (bokf_source metadata)
  ↓
Technical Analysis (bokf_source metadata)
  ↓
Architecture Design (bokf_design workspace)
  ↓
Implementation (bokf_design/phase_4_implementation OR gatekeeper workspace)
  ↓
Testing (bokf_design workspace OR gatekeeper workspace)
```

**Safeguarding Benefits**:
- Every change traces back to requirements
- Original requirements never modified
- Modernization work clearly separated
- Complete audit trail for compliance

### Workspace Planning Tool Integration

**Plan Storage**:
```
//bokf_design/plan/[plan_id]
//gatekeeper/plan/[plan_id]
```

**Safeguarding**:
- Plans stored in modernization workspaces only
- No plans modify original source workspace
- All work tracked through planning tool
- Clear record of what was changed, by whom, and why

---

## Recovery and Rollback Safeguards

### Checkpoint-Based Recovery

**Checkpoint Storage**:
```
//bokf_design/meta/orchestration_workflow/recovery_system/
```

**Safeguarding**:
- Recovery points capture modernization work state
- Original source never part of recovery/rollback
- Failed modernization can be rolled back without affecting original
- Original source remains pristine reference

### Context Corruption Protection

**Context Integrity Checks**:
- Automated detection of context corruption
- Context restoration from backup metadata
- Original source used as ground truth for validation
- Corrupted context never written back to source workspace

---

## Best Practice Summary

### DO (Safeguarding Patterns)
✅ Read from `bokf_source` for analysis
✅ Write analysis to metadata structures
✅ Write new code to `bokf_design` or `gatekeeper`
✅ Use scratchpad for temporary work
✅ Move outdated work to trash
✅ Store context in metadata
✅ Reference client standards from metadata

### DON'T (Unsafe Patterns)
❌ Write to `bokf_source` workspace (except metadata)
❌ Modify original source files
❌ Mix new code with old code
❌ Store analysis in source directories
❌ Create dependencies between new and old code
❌ Allow test scripts in source workspace
❌ Bypass workspace segregation

---

## Compliance and Security Benefits

**IP Protection**:
- Original client source code never modified or mixed with new code
- Clear ownership: client owns original, modernized work is separate deliverable

**Regulatory Compliance**:
- Complete audit trail of all changes
- Traceability from requirements to implementation
- Change control through planning tool and authority signoff

**Risk Mitigation**:
- Modernization failures don't corrupt original source
- Rollback capability without affecting original
- Multiple recovery points for business continuity

**Operational Security**:
- Workspace segregation limits blast radius of errors
- Read-only access prevents accidental modifications
- Trash provides safety net for accidental deletions
