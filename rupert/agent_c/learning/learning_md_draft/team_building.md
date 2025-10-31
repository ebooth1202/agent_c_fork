# Building Agent Teams in Agent C

A practical guide to creating effective multi-agent systems.

---

## When Do You Need a Team?

**Single Agent Works When:**
- Task is straightforward with clear steps
- No specialized domain expertise required
- Token budget fits comfortably in one agent (under 10K)
- No need for independent validation
- One perspective is sufficient

**Team Becomes Necessary When:**
- **Multiple specialized domains** involved (architecture + compliance + quality)
- **Deep expertise required** in specific areas (regulatory knowledge, technical patterns)
- **Independent validation needed** (someone must check the work objectively)
- **Token efficiency matters** (specialization prevents bloated agents)
- **Clear role separation** improves quality (analyst shouldn't validate their own analysis)

### The Signal: "This Needs a Team"

Ask yourself:
- Would a single agent need 12K+ tokens to do this well?
- Do we need someone to validate this work independently?
- Does this require deep expertise in multiple distinct domains?
- Will role confusion create quality issues? (e.g., "extract requirements" vs "validate compliance")

**If yes to 2+ questions**: Consider a team.

---

## When Teams Excel: Scenarios and Complexity Thresholds

### Teams Outperform Single Agents When:

**1. Specialization Prevents Errors**

*Example: Insurance Analysis*
- **With Specialist**: Deep regulatory knowledge catches "This violates aggregate limit rules"
- **Without Specialist**: General agent misses compliance nuances, issues reach stakeholders

**2. Independent Validation Matters**

*Example: Quality Oversight*
- **With Independent Validator**: Fresh eyes catch "requirements lack source evidence"
- **Without Independence**: Coordinator validates own work, misses issues (judge and jury problem)

**3. Token Efficiency Through Focus**

*Real Pattern*:
- **Before**: 72-84K token mega-agent (bloated, unfocused)
- **After**: 37-45K specialized team (46-54% reduction)
- **How**: Each agent 5-8K focused tokens vs. one 80K+ generalist

### Complexity Thresholds

**Under 3 Specialized Domains**: Single agent usually sufficient

**3-5 Specialized Domains**: Team starts making sense
- Example: Pattern Discovery + Requirements + Architecture + Domain Validation + Quality

**6+ Specialized Domains**: Team almost certainly better
- Coordination overhead worth the specialization benefits

---

## Why Utilize a Team: Core Benefits

### 1. Token Efficiency Through Specialization

**Counter-Intuitive Truth**: Teams can be MORE token-efficient than single agents.

**The Math**:
- **Bloated Single Agent**: 70-80K tokens trying to cover everything
- **Focused Team (6 agents)**: 37-45K total
  - Pattern Analyzer: 5K
  - Requirements Extractor: 7K
  - Architect: 6K
  - Domain Specialist: 6K (with 2.6K deep expertise)
  - Quality Validator: 6K
  - Orchestrator: 7.5K

**Why This Works**:
- Each agent carries ONLY what it needs
- No redundant context across domains
- Deep expertise concentrated where needed
- Clear handoffs minimize context overlap

### 2. Specialization Prevents Errors

**Role Confusion Creates Quality Issues**:

| Scenario | Problem | Result |
|----------|---------|--------|
| Analyst also validates | Can't be neutral extractor AND critical validator | Misses own extraction errors |
| Architect also validates compliance | Lacks deep domain expertise | Misses regulatory nuances |
| Coordinator also validates quality | Judge and jury problem | Overlooks coordination issues |

**Specialization Solution**: Each agent does ONE thing deeply, with independent gates between roles.

### 3. Clear Role Separation

**What Each Agent Should Own**:
- **Discovery Agent**: WHAT exists (patterns, structure)
- **Extraction Agent**: WHAT it means (business requirements)
- **Design Agent**: HOW to build it (architecture, modernization)
- **Domain Specialist**: IF it meets specialized requirements (compliance, regulations)
- **Quality Agent**: IF quality is sufficient (evidence, completeness)
- **Orchestrator**: WHO does WHAT and WHEN (workflow, recovery)

**No Overlap = No Confusion**

### 4. Independent Validation Gates

**Why Independence Matters**:
- Analyst can't catch own extraction errors
- Coordinator can't objectively validate work they assigned
- Designer needs someone to challenge assumptions

**How to Structure**:
- Quality validator not involved in analysis/coordination
- Domain specialist focused on specialized validation only
- Clear separation between "do the work" and "validate the work"

---

## How Bobb Helps You Build Teams

Bobb is Agent C's meta-agent for designing agent systems. Here's how to leverage Bobb effectively:

### What Questions to Ask Bobb

**Start High-Level**:
- "I need to analyze [domain] and produce [deliverable]. Should this be one agent or a team?"
- "What specialized roles are needed for [specific workflow]?"
- "Where should independent validation happen in this workflow?"

**Get Specific About Roles**:
- "What expertise should the [domain] specialist have?"
- "How should the orchestrator coordinate between [Agent A] and [Agent B]?"
- "What handoff points need validation gates?"

**Refine Coordination**:
- "How should error recovery work in this team?"
- "What should the orchestrator delegate vs. handle directly?"
- "Where do we risk token bloat in these roles?"

### How to Ask (Specifics Matter!)

**❌ Too Vague**: "I need agents for my project"

**✅ Specific Context**:
"I need to analyze legacy insurance systems and create modernization requirements. The analysis must validate regulatory compliance. Stakeholders need clear, documented recommendations."

**❌ Missing Constraints**: "Design me a team"

**✅ Include Constraints**:
"Token budget: 50K total. Must include independent quality validation. Regulatory compliance is critical - we can't miss requirements."

**❌ Unclear Workflow**: "What agents do I need?"

**✅ Clear Workflow**:
"Workflow: Discover patterns in code → Extract requirements → Design architecture → Validate compliance → Certify quality → Deliver to stakeholders"

### What Information Bobb Needs

**1. Domain Context**:
- What field/industry? (insurance, finance, healthcare, etc.)
- What specialized knowledge required? (regulatory, technical, business)

**2. Workflow Clarity**:
- Input → Processing → Output sequence
- Where validation gates needed
- Who consumes the final output

**3. Constraints**:
- Token budget (be realistic)
- Quality requirements
- Coordination complexity tolerance

**4. Risk Areas**:
- What errors would be costly? (compliance violations, quality issues)
- Where do you need independent oversight?
- What expertise gaps exist?

### How Bobb Designs Coordination Patterns

Bobb will structure teams around:

**1. Sequential Workflows** (most common):
```
Orchestrator → Discover → Extract → Design → Validate → Certify → Deliver
```

**2. Validation Gates**:
- After critical work products
- Before stakeholder delivery
- Where specialized expertise needed

**3. Error Recovery**:
- Orchestrator monitors progress
- Validation gates catch issues early
- Clear escalation paths for problems

**4. Token Optimization**:
- Each agent carries only necessary context
- Handoffs minimize redundancy
- Deep expertise concentrated in specialists

### The Component Reference Library: Your Safety Net

Here's an important truth: **mistakes in team building are expected**. Hierarchy issues, positioning errors, role confusion—these are part of the learning process as you develop your "agent driving" skills.

But you're not learning in a vacuum. **The component reference library is a crucial safety net.**

When you work with Bobb to design agents, Bobb references this library of proven patterns, structures, and positioning strategies. Think of it as:
- ✅ **Tested templates** for common agent types (analyzers, validators, orchestrators)
- ✅ **Positioning patterns** that prevent common mistakes
- ✅ **Hierarchy structures** that keep critical rules visible
- ✅ **Coordination blueprints** for team workflows

Bobb uses these components to ensure:
- Your personas are structured properly (critical rules at top, not buried)
- Agents are positioned appropriately (clear roles, no confusion)
- Common failure patterns are avoided (learned from previous builds)
- Token efficiency best practices are applied

**What This Means for You**: You don't need to memorize every positioning rule or hierarchy principle. Bobb handles that by pulling from the component library. Your job is to describe your needs clearly—Bobb applies the proven patterns.

**As you gain experience**, you'll start recognizing these patterns yourself and can request specific components or adjustments. But early on, trust the library. It's built from real-world experience with what works and what fails.

---

## How Teams Falter: Hierarchy and Positioning Principles

Even with Bobb's help and the component reference library, understanding WHY certain patterns work helps you make better decisions. Here's what happens when teams falter:

Even well-designed teams can fail due to poor persona structure. Here's how hierarchy and positioning affect agent behavior:

### Why Order and Emphasis Matter

**Agent C Processes Personas Top-to-Bottom**:
- **Top = Primary Focus**: Agent prioritizes these instructions
- **Middle = Secondary**: Agent considers but may deprioritize under pressure
- **Bottom = Easily Forgotten**: Agent may ignore if context window stressed

**Example of Positioning Impact**:

**❌ Poor Positioning**:
```
Agent Persona:
- You are a helpful assistant
- You analyze data carefully
- You follow regulatory compliance rules [BURIED AT BOTTOM]
```
Result: Agent focuses on being "helpful" and "analyzing" but FORGETS compliance rules when context window fills.

**✅ Proper Positioning**:
```
Agent Persona:
- CRITICAL: You validate regulatory compliance above all else
- You analyze data through a compliance lens
- You are helpful while maintaining compliance focus
```
Result: Agent NEVER forgets compliance - it's the first thing processed, every time.

### Hierarchy Principles for Team Design

**1. Critical Instructions at Top**
- Non-negotiable rules first
- Quality gates before nice-to-haves
- Compliance requirements before efficiency preferences

**2. Role Definition Early**
- "You are a [ROLE]" near the top
- Core responsibilities clearly stated
- What you DON'T do (boundaries)

**3. Workflow Context Middle**
- How you interact with other agents
- Handoff expectations
- Coordination patterns

**4. Edge Cases and Details Lower**
- Formatting preferences
- Nice-to-have behaviors
- Optional enhancements

### Common Positioning Mistakes

**Mistake 1: Burying Critical Rules**
```
Agent Persona:
[200 lines of workflow instructions]
[100 lines of examples]
Oh, and by the way, never modify production data [LINE 350]
```
**Impact**: Agent violates critical rule because it's buried under token load.

**Fix**: Critical rules at TOP, repeated as section headers.

---

**Mistake 2: Role Confusion**
```
Agent Persona:
- You extract requirements AND validate quality AND check compliance
```
**Impact**: Agent doesn't know which role to prioritize, does all poorly.

**Fix**: ONE primary role per agent. If validation needed, create separate validator.

---

**Mistake 3: Equal Emphasis**
```
Agent Persona:
- Be accurate (important!)
- Be fast (important!)
- Be comprehensive (important!)
- Follow regulations (important!)
```
**Impact**: Agent paralyzed by conflicting priorities, or picks randomly.

**Fix**: Explicit hierarchy:
1. CRITICAL: Regulatory compliance (never compromise)
2. REQUIRED: Accuracy (can take time needed)
3. PREFERRED: Comprehensive (if time allows)
4. NICE-TO-HAVE: Speed (optimize but not at accuracy cost)

---

**Mistake 4: Implicit Expectations**
```
Agent Persona:
- You work with other agents
- Quality is important
- Follow the workflow
```
**Impact**: Agent doesn't know WHAT quality standards, WHICH workflow, or HOW to coordinate.

**Fix**: Explicit instructions:
- "Validation Gate: Before handoff to Architect, verify you have documented source evidence for every requirement"
- "Workflow: Receive patterns from Discovery Agent → Extract requirements → Hand to Architect with evidence"

---

### How Poor Positioning Causes Failures

**Real Failure Pattern 1: Validator Forgets to Validate**
- Quality validation instructions buried in middle of persona
- Context window pressure causes agent to skip validation
- Issues reach stakeholders unchecked

**Solution**: Quality gates at TOP of validator persona, repeated before handoff instructions.

---

**Real Failure Pattern 2: Specialist Acts as Generalist**
- Domain specialist persona starts with "you're helpful and collaborative"
- Specialist tries to do everyone's job instead of specializing
- Deep expertise never applied

**Solution**: Lead with "You are a [DOMAIN] SPECIALIST. Your ONLY role is [SPECIFIC EXPERTISE]. You do NOT [other roles]."

---

**Real Failure Pattern 3: Orchestrator Micromanages**
- Orchestrator persona emphasizes "detailed oversight"
- Orchestrator does specialists' work instead of coordinating
- Team becomes bottleneck

**Solution**: Lead with "You COORDINATE, you do NOT execute. Trust specialists, validate at gates, intervene only on failures."

---

## Team Building Checklist

Before you build your team, validate:

**✅ Role Clarity**
- Each agent has ONE primary role
- No overlap between agent responsibilities
- Clear boundaries (what each agent does NOT do)

**✅ Token Efficiency**
- Each agent under 10K tokens (ideally 5-8K)
- No redundant context across agents
- Deep expertise concentrated in specialists

**✅ Validation Gates**
- Independent validation after critical work
- Quality checks before stakeholder delivery
- Domain validation where expertise required

**✅ Hierarchy in Personas**
- Critical rules at TOP of each persona
- Role definition early and clear
- Explicit priorities (not equal emphasis)
- Workflow context and coordination patterns

**✅ Coordination Design**
- Orchestrator coordinates, doesn't execute
- Clear handoff expectations
- Error recovery patterns defined

**✅ Scope Match**
- Team size matches complexity (3-6 specialized domains = 3-6 agents)
- Specialization worth coordination overhead
- Not building a team just because you can

---

## Final Principle: Specialization vs. Coordination Overhead

**The Trade-Off**:
- **More Agents = More Specialization** (deeper expertise, clearer roles, better quality)
- **More Agents = More Coordination** (more handoffs, more orchestration, more complexity)

**When Specialization Wins**:
- Deep expertise prevents costly errors
- Role confusion would create quality issues
- Independent validation is critical
- Token efficiency matters (team is lighter than bloated single agent)

**When Coordination Overhead Wins**:
- Domains overlap significantly
- Expertise depth not critical
- Single agent can handle it under 10K tokens
- Team complexity overwhelms benefits

**Bobb Helps You Find the Balance**: Be explicit about your constraints, risks, and requirements. Let Bobb design for your specific needs.

---

**Ready to Build?** Start with Bobb. Describe your workflow, constraints, and risks. Iterate on the design. Get team structure right BEFORE building agents.
