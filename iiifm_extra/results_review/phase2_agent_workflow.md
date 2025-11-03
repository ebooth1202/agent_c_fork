# Phase 2 Agent: Workflow Breakdown

**Agent:** Link - Cross-Module Linkage Analyst (NEW agent to be created)

---

## AGENT PROFILE

**Name:** Link
**Category:** `assist` (helper agent)
**Primary Role:** Cross-module dependency analysis and linkage documentation
**Work Style:** Primarily solo, optional team consultation

**Key Tools:**
- WorkspaceTools (read Phase 1 docs, read source code, write linkage docs)
- ThinkTools (reasoning about data flow and dependencies)
- WorkspaceGrep (search for field/variable usage across codebase)
- WorkspaceKnowledgeTools (if available for code search)

---

## TEAM INTEGRATION

### Invocation Model: **USER-INITIATED VIA DOUGLAS** ✅

**Workflow:**
```
Phase 1 complete → User reviews Phase 1 doc → User validates accuracy → 
User tells Douglas: "Please have Link do Phase 2 cross-functional analysis" → 
Douglas invokes Link → Link produces linkage addendum → 
Douglas delivers results to user
```

**User Experience:**
- User stays in conversation with Douglas (no new conversation needed)
- User: "Douglas, please initiate Phase 2 with Link"
- Douglas coordinates with Link behind the scenes
- User receives Phase 2 results from Douglas

**Rationale:**
- User validates Phase 1 accuracy before Phase 2 investment
- User determines if cross-functional analysis needed for this module
- Prevents wasted Phase 2 work on inaccurate Phase 1 data
- User maintains control over scope and timing
- Especially important if Phase 1 data may need corrections
- Clean UX: User doesn't switch conversations

**Douglas Role:**
- Completes Phase 1 and delivers to user
- Does NOT automatically invoke Link
- Waits for user decision on Phase 2
- IF user requests Phase 2: Invokes Link via AgentTeamTools or AgentAssistTools
- Coordinates Link's work and delivers results

### Collaboration Model: **Primarily Solo**

**Invoked By:** Douglas (on user request)
**Works With:** Minimal team collaboration

**Why Solo?**
- Phase 1 team already did deep source code analysis
- Link needs different perspective: data flow tracing vs feature extraction
- Less coordination overhead = faster execution
- Phase 2 is distinct enough to warrant independent work
- Douglas acts as coordinator, Link does the work

**Optional Consultation:**
- Can ask Rex: "Find all references to field X across modules"
- Can ask Mason: "Trace where variable Y is used in other files"
- Can ask Rita: "What's the business process impact of Z?"
- But most work done independently

**Returns Results To:** Douglas (who delivers to user)

---

## WORKFLOW: How Link Does Its Work

### Step 1: Input Analysis
**Action:** Read and parse Phase 1 documentation
**Focus Areas:**
- Coverage/endorsement selections with values
- Input fields that accept user data
- Validation rules that might have cross-module implications
**Output:** List of "trace candidates" (fields/selections to investigate)

**Example Trace Candidates from WCP doc:**
- "Waiver of Subrogation" checkbox + "Number of Waivers" field
- "Inclusion of Sole Proprietors" checkbox
- "Experience Modification" value

---

### Step 2: Cross-Module Code Tracing
**Action:** For each trace candidate, search source code for usage
**Method:**
- Grep for field names, variable names, database columns
- Search for related business logic in other modules
- Identify where data flows after initial capture
**Focus:** HIGH-LEVEL tracing, not deep dive

**Example for "Number of Waivers":**
```
Search: "NumberOfWaivers", "WaiverCount", "waiver" in application-side code
Find: Application module has "Schedule Waivers" section
Trace: Number entered on coverage page → Required count on application page
```

---

### Step 3: Downstream Requirement Identification
**Action:** Determine what user must do elsewhere based on selections
**Pattern Recognition:**
- Selection on Page A → Required data entry on Page B
- Value on Page A → Validation constraint on Page B
- Endorsement selection → Application form requirement
**Output:** Structured list of cross-module dependencies

**Example:**
```
Coverage Selection: Waiver of Subrogation = TRUE, Number of Waivers = 5
→ Downstream Requirement: User must schedule 5 named individuals on Application page
→ Location: Application Module > Named Individuals section
→ Business Rule: Count of scheduled individuals must match Number of Waivers
```

---

### Step 4: Linkage Documentation
**Action:** Create structured cross-functional linkage document
**Format:**
```markdown
## Cross-Module Dependencies

### Coverage: [Name]
**Selection/Value:** [What user selects/enters]
**Triggers Requirement In:** [Module/Page name]
**Requirement Description:** [What user must do]
**Business Rule:** [The linkage rule]
**Validation:** [Any cross-module validation that occurs]
**Source Code Evidence:** [File references]
```

---

### Step 5: Output Delivery
**Action:** Return linkage document
**Options:**
- Standalone addendum document
- Integrated sections added to Phase 1 doc
- Summary for Douglas to review

---

## EXAMPLE WORKFLOW EXECUTION

### Scenario: Analyze WCP Policy Level Coverages Doc

**Step 1: Link reads Phase 1 doc**
- Identifies: Waiver of Subrogation, Number of Waivers, Inclusion of Sole Proprietors, etc.
- Creates trace list: 8 fields/selections to investigate

**Step 2: Link traces "Number of Waivers"**
- Searches codebase for "NumberOfWaivers" usage
- Finds references in application-side code
- Discovers "Schedule Waivers" requirement

**Step 3: Link identifies downstream requirement**
- Coverage page: User enters "5" in Number of Waivers
- Application page: User must schedule 5 named individuals
- Business rule: Count must match

**Step 4: Link documents linkage**
```markdown
### Waiver of Subrogation - Number of Waivers
**Coverage Selection:** Number of Waivers = [X]
**Triggers Requirement:** Application Module
**Location:** Named Individuals Scheduling Section
**User Must:** Schedule X named individuals matching the count entered
**Business Rule:** Scheduled count must equal Number of Waivers
**Validation:** System validates count match before quote completion
**Source Code:** ApplicationModule.vb lines 234-267
```

**Step 5: Link returns linkage doc**
- Returns to Douglas or user
- Douglas can integrate into Phase 1 doc or keep separate

---

## EFFICIENCY CONSIDERATIONS

### Why This is Fast
- ✅ No deep feature extraction (Phase 1 already did that)
- ✅ High-level tracing only (grep-based searches)
- ✅ Focused scope (just cross-module linkages)
- ✅ Solo work (no coordination overhead)
- ✅ Clear input/output format

### When to Consult Team
- 🤔 Can't find source code references → Ask Mason to trace
- 🤔 Unclear business logic → Ask Rita to clarify
- 🤔 Pattern not obvious → Ask Rex to find similar patterns
- But aim for 80%+ solo completion

---

## INTEGRATION WITH DOUGLAS

### Douglas Role in Phase 2

**Minor Updates Needed to Douglas:**
- After Phase 1 completion, inform user Phase 2 is available
- Wait for user to request Phase 2 (never automatic)
- IF user requests Phase 2:
  - Invoke Link via AgentTeamTools or AgentAssistTools
  - Pass Phase 1 doc path and source code context to Link
  - Wait for Link's linkage document
  - Deliver results to user

**Conversation Flow:**
```
Douglas: "Phase 1 documentation complete. Review and let me know if you need any revisions. 
          If you'd like cross-functional linkage analysis (Phase 2), I can coordinate with Link."
          
User: Reviews Phase 1 doc, validates accuracy

User: "Looks good. Please have Link do the Phase 2 cross-functional analysis."

Douglas: "I'll coordinate with Link for the cross-module dependency analysis."
         [Invokes Link behind the scenes]
         
Link: [Does analysis work, returns linkage document to Douglas]

Douglas: "Phase 2 complete. Here's the cross-functional linkage analysis from Link..."
```

---

## WORK ESTIMATE

**Per Module Analysis:**
- Simple module (few cross-module linkages): 15-30 minutes
- Complex module (many linkages like WCP): 45-90 minutes

**vs enhancing existing team:**
- All 6 agents carry Phase 2 weight always
- Coordination overhead for multi-agent Phase 2
- Likely slower execution

---

## SUMMARY

**Agent:** Link (new agent)
**Work Style:** Primarily solo with optional team consultation
**Process:** Read Phase 1 doc → Trace data usage → Identify downstream requirements → Document linkages
**Integration:** Invoked by Douglas after Phase 1 OR directly by user
**Output:** Cross-functional linkage addendum document
**Efficiency:** Fast, focused, no bloat to existing agents
