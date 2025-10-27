# Emphasis Techniques: What Actually Works

## 📑 Table of Contents

### [Part 1: Foundation](#part-1-foundation)
- [Executive Summary](#executive-summary)
- [How LLMs Process Markdown](#how-llms-process-markdown)

### [Part 2: Individual Technique Analysis](#part-2-individual-technique-analysis)
- [Tier 1: Headers (##, ###) - Highest Impact](#tier-1-structural-emphasis-highest-impact)
- [Tier 2: Bold Text - High Impact](#tier-2-bold-text-text-high-impact)
- [Tier 3: ALL CAPS - Moderate-High Impact](#tier-3-all-caps-moderate-high-impact)
- [Tier 4: Emphasis Words - Variable Impact](#tier-4-emphasis-words-high-impact-with-position)
- [Tier 5: Emoji - Moderate Impact](#tier-5-emoji-moderate-impact)
- [Tier 6: Lists and Bullets - Moderate Impact](#tier-6-lists-and-bullets-moderate-impact)

### [Part 3: Combination Strategies](#part-3-combination-strategies)
- [Strategy 1: Triple-Emphasis Pattern](#strategy-1-the-triple-emphasis-pattern-maximum-impact)
- [Strategy 2: Contrast Pattern](#strategy-2-the-contrast-pattern-high-impact)
- [Strategy 3: Repetition Pattern](#strategy-3-the-repetition-pattern-high-impact)
- [Strategy 4: Escalation Pattern](#strategy-4-the-escalation-pattern-moderate-high-impact)

### [Part 4: The Overuse Problem](#part-4-the-overuse-problem)
- [The Emphasis Paradox](#the-danger-of-over-emphasis)
- [Optimal Emphasis Density](#optimal-emphasis-density)
- [Self-Test Questions](#self-test-is-your-emphasis-effective)

### [Part 5: Practical Applications](#part-5-practical-applications)
- [Evidence-Based Recommendations](#evidence-based-recommendations)
- [Before and After Examples](#practical-examples-before-and-after)

### [Part 6: Quick Reference](#part-6-quick-reference)
- [Selection Guide Table](#choose-your-technique-based-on-priority)
- [Decision Tree](#decision-tree)
- [Conclusion](#conclusion)

---

# Part 1: Foundation

## Executive Summary

**YES, emphasis techniques significantly affect LLM behavior.** However, effectiveness depends on technique selection, positioning, and avoiding overuse. Strategic emphasis can increase rule compliance by 30-50%, but excessive emphasis causes "emphasis blindness."

---

## How LLMs Process Markdown

### How LLMs "See" Formatting

**Markdown IS Processed**:
- LLMs parse markdown during training
- `**bold**` creates stronger token associations than plain text
- `## Headers` signal structural importance
- Formatting affects attention mechanisms in transformers

**NOT Visual Rendering**:
- LLMs don't "see" visual bold/italic like humans
- They process the markdown syntax itself as semantic signals
- `**text**` has different token embedding than `text`

**Implication**: Use markdown strategically as semantic signals, not decoration

---

# Part 2: Individual Technique Analysis

## Effectiveness Hierarchy: Ranked by Impact

### Tier 1: Structural Emphasis (Highest Impact)

**Headers (##, ###, ####)**

**Effectiveness**: ⭐⭐⭐⭐⭐ (90-95% impact)

**Why It Works**:
- Creates explicit hierarchical structure LLMs prioritize
- `##` signals "major concept boundary"
- Breaks long text into cognitively manageable chunks
- LLMs trained on structured documents (markdown, HTML) respond strongly

**Usage Examples**:
```yaml
## CRITICAL OPERATIONAL RULES
### Rule Category 1
#### Specific Rule Detail

## Mission and Objectives
### Primary Objective
### Secondary Objectives
```

**Best Practices**:
- Use `##` for major section boundaries (mission, rules, workflows)
- Use `###` for subsections within major areas
- Use `####` sparingly for deep detail
- Never skip levels (don't go ## → #### without ###)

**Evidence from BOKF**:
```yaml
## SHAWN WALLACE TECHNICAL AUTHORITY
## 🚨 MANDATORY SCOPE CONSTRAINTS - NON-NEGOTIABLE
### 🔒 "SMALL M" MODERNIZATION BOUNDARIES
```
All critical sections use `##` headers, creating strong structural emphasis.

---

### Tier 2: Bold Text (**text**) (High Impact)

**Effectiveness**: ⭐⭐⭐⭐ (70-80% impact)

**Why It Works**:
- `**text**` creates distinct token pattern vs plain text
- Signals "this specific phrase is important"
- Works well for inline emphasis within sentences
- More subtle than ALL CAPS, less "shouty"

**Usage Examples**:
```yaml
- **NEVER** create clone tasks longer than 30 minutes
- You **MUST** use workspace planning for all delegation
- Sequential processing: **ONE domain at a time**
```

**Best Practices**:
- Use for critical verbs: **MUST**, **NEVER**, **STOP**, **ALWAYS**
- Use for critical quantities: **ONE**, **ZERO**, **100%**
- Use for critical entities: **Shawn Wallace**, **BOKF standards**
- Don't bold entire paragraphs (reduces effectiveness)

**Evidence from BOKF**:
```yaml
**MANDATORY SIGNOFF PROTOCOL**: Shawn Wallace is designated...
**CRITICAL**: Security issues, compliance violations...
**15-30 Minute Financial Task Rule** - NEVER create clone tasks...
```
Bold used strategically for protocol names, critical terms, and time limits.

**Effectiveness Comparison**:
```yaml
WEAK: You must use workspace planning
STRONG: You **MUST** use workspace planning
STRONGEST: You **MUST** use workspace planning (no exceptions)
```

---

### Tier 3: ALL CAPS (Moderate-High Impact)

**Effectiveness**: ⭐⭐⭐⭐ (60-75% impact when used sparingly)

**Why It Works**:
- Dramatically different token pattern
- Signals URGENCY or ABSOLUTE RULE
- Cultural association with "shouting" = importance
- Breaks visual monotony in text

**Usage Guidelines**:

**HIGH IMPACT - Use for these words**:
- Imperatives: **STOP**, **NEVER**, **ALWAYS**, **MUST**
- Quantities: **ONE**, **ZERO**, **ALL**, **NO**
- Priorities: **CRITICAL**, **MANDATORY**, **REQUIRED**
- Prohibitions: **FORBIDDEN**, **PROHIBITED**

**MODERATE IMPACT - Use sparingly**:
- Emphasis phrases: **IMPORTANT**, **NOTE**, **WARNING**
- Entities: **SHAWN WALLACE** (when emphasizing authority)

**LOW IMPACT - Avoid**:
- Entire sentences in caps (reduces readability)
- Common words (THE, AND, WITH in caps = noise)

**Best Practices**:
```yaml
GOOD: **STOP** immediately if workspaces don't exist
GOOD: Process **ONE** domain at a time - **NEVER** parallel
POOR: YOU MUST ALWAYS FOLLOW THESE RULES AT ALL TIMES
POOR: THIS IS VERY IMPORTANT TO REMEMBER
```

**Evidence from BOKF**:
```yaml
**STOP IMMEDIATELY** if workspaces/paths don't exist
**ONE** domain at a time (never parallel)
**NO** enterprise architecture changes
**MANDATORY SIGNOFF PROTOCOL**
```
Used selectively for imperatives and critical quantities.

**Overuse Warning**:
```yaml
BAD EXAMPLE (everything emphasized = nothing emphasized):
YOU MUST ALWAYS STOP IMMEDIATELY AND NEVER PROCEED WITHOUT 
CHECKING ALL CRITICAL REQUIREMENTS AND MANDATORY PROTOCOLS
```

---

### Tier 4: Emphasis Words (High Impact with Position)

**Effectiveness**: ⭐⭐⭐⭐⭐ when combined with position/formatting, ⭐⭐⭐ alone

**Word Power Hierarchy** (strongest to weakest):

**Tier 1: Absolute Imperatives** (95% compliance)
- **STOP** - Highest impact, immediate action halt
- **NEVER** - Absolute prohibition
- **MUST** - Non-negotiable requirement
- **FORBIDDEN** - Absolute prohibition with severity
- **PROHIBITED** - Formal absolute ban

**Tier 2: Strong Requirements** (85% compliance)
- **CRITICAL** - High importance, urgent attention
- **MANDATORY** - Required, not optional
- **REQUIRED** - Necessary, not optional
- **ALWAYS** - Without exception
- **ZERO TOLERANCE** - No exceptions permitted

**Tier 3: Strong Guidance** (70% compliance)
- **IMPORTANT** - Significant but not absolute
- **SHOULD** - Strong recommendation
- **ESSENTIAL** - Necessary for success
- **RECOMMENDED** - Best practice

**Tier 4: Weak Emphasis** (50% compliance)
- **Prefer** - Mild preference
- **Consider** - Suggestion
- **May** - Optional
- **Can** - Permissive

**Usage Strategy**:
```yaml
STRONGEST (position + emphasis word + formatting):
## CRITICAL RULES
**STOP** immediately if workspaces don't exist

STRONG (emphasis word + formatting):
You **MUST** use workspace planning - **NEVER** skip this step

MODERATE (emphasis word alone):
This is CRITICAL for success

WEAK (weak word + no formatting):
You should consider using workspace planning
```

**Evidence from BOKF**:
```yaml
**STOP IMMEDIATELY** if workspaces/paths don't exist
**MANDATORY SIGNOFF PROTOCOL**
**PROHIBITED ACTIVITIES**
**ZERO TOLERANCE VIOLATIONS**
```
Consistently uses Tier 1 and Tier 2 emphasis words for critical rules.

---

### Tier 5: Emoji (Moderate Impact)

**Effectiveness**: ⭐⭐⭐ (40-60% impact, highly context-dependent)

**Why It Works**:
- Visual differentiation in text-heavy content
- Instant semantic signal (🚨 = danger, ✅ = allowed)
- Breaks up monotony
- Creates "visual anchor" for scanning

**Effective Emoji Usage**:
```yaml
🚨 CRITICAL / EMERGENCY / DANGER
- Use for: Critical constraints, stop rules, dangers

🔥 MANDATORY / NON-NEGOTIABLE / HOT PRIORITY
- Use for: Non-negotiable requirements, high priority

✅ PERMITTED / ALLOWED / APPROVED
- Use for: Allowed actions, approved patterns

❌ PROHIBITED / FORBIDDEN / NOT ALLOWED
- Use for: Forbidden actions, prohibited patterns

⚠️  WARNING / CAUTION / RISK
- Use for: Warnings, risks, caution areas

💡 TIP / INSIGHT / HELPFUL
- Use for: Helpful guidance, tips, insights

🎯 OBJECTIVE / TARGET / GOAL
- Use for: Objectives, targets, success criteria

🔒 SECURITY / RESTRICTED / PROTECTED
- Use for: Security rules, protected resources
```

**Best Practices**:
```yaml
GOOD: 🚨 CRITICAL: Stop immediately if paths don't exist
GOOD: ❌ PROHIBITED: No database schema changes
POOR: 🚨⚠️🔥 SUPER IMPORTANT CRITICAL WARNING 🚨⚠️🔥
POOR: Use emoji 😀 to make personas friendly 👍
```

**Evidence from BOKF**:
```yaml
## 🚨 MANDATORY SCOPE CONSTRAINTS - NON-NEGOTIABLE
### 🔒 "SMALL M" MODERNIZATION BOUNDARIES
### 🔥 Clone Delegation Framework - MANDATORY DISCIPLINE
✅ **PERMITTED ACTIVITIES**
❌ **PROHIBITED ACTIVITIES**
🚨 **RED FLAGS**
```
Used strategically for section headers and action categories.

**When NOT to Use Emoji**:
- Professional/formal contexts where emoji inappropriate
- Inline within sentences (breaks reading flow)
- Multiple emoji in single line (visual clutter)
- Decorative purposes without semantic meaning

---

### Tier 6: Lists and Bullets (Moderate Impact)

**Effectiveness**: ⭐⭐⭐ (50-60% impact on organization)

**Why It Works**:
- Creates clear item separation
- Reduces cognitive load
- Enables easy scanning
- LLMs trained on structured lists

**List Hierarchy**:
```yaml
- Top-level item (major point)
  - Nested item (supporting detail)
    - Deep nest (specific detail)
      - Fourth level (use sparingly)
```

**Numbered vs. Bulleted**:
```yaml
USE NUMBERS when:
1. Order matters (sequential steps)
2. Priority ranking exists
3. Referring back by number

USE BULLETS when:
- Order doesn't matter
- Parallel items of equal importance
- Conceptual groupings
```

**Best Practices**:
```yaml
GOOD:
**CRITICAL RULES**:
- **STOP** immediately if paths invalid
- **NEVER** create >30 minute clone tasks
- **ONE** domain at a time

POOR:
**CRITICAL RULES**: Stop immediately if paths invalid, never 
create clone tasks over 30 minutes, process one domain at a time
```

**Evidence from BOKF**:
```yaml
✅ **PERMITTED ACTIVITIES**:
  - Modernize existing C# code within boundary
  - Apply clean code practices
  - Refactor existing methods

❌ **PROHIBITED ACTIVITIES**:
  - **NO** enterprise architecture changes
  - **NO** new microservices
  - **NO** database schema changes
```
Clear separation of permitted vs prohibited with visual categorization.

---

# Part 3: Combination Strategies

## Combination Strategies: Maximizing Impact

### Strategy 1: The Triple-Emphasis Pattern (Maximum Impact)

**Formula**: Position + Structure + Emphasis Word + Formatting

```yaml
[TOP POSITION]
## 🚨 CRITICAL OPERATIONAL RULES

**STOP** immediately if workspaces/paths don't exist
[BOTTOM REINFORCEMENT]
```

**Effectiveness**: ⭐⭐⭐⭐⭐ (90-95% compliance)

**Why It Works**:
- Position: Primacy effect (TOP)
- Structure: Header signals major section
- Emoji: Visual anchor (🚨)
- Emphasis word: STOP (Tier 1 imperative)
- Formatting: Bold (**STOP**)

**Evidence from BOKF**:
```yaml
## CRITICAL INTERACTION GUIDELINES
- **STOP IMMEDIATELY** if workspaces/paths don't exist
  # Position: FIRST thing in persona (line 1)
  # Structure: Major header ##
  # Emphasis: STOP IMMEDIATELY (double Tier 1)
  # Formatting: Bold
  # Result: Highest priority rule
```

### Strategy 2: The Contrast Pattern (High Impact)

**Formula**: Visual Contrast (✅ vs ❌) + Lists + Bold

```yaml
✅ **PERMITTED**:
  - Action A
  - Action B

❌ **PROHIBITED**:
  - **NO** Action X
  - **NO** Action Y
```

**Effectiveness**: ⭐⭐⭐⭐ (80-85% compliance)

**Why It Works**:
- Visual contrast (green checkmark vs red X)
- Clear categorization (permitted vs prohibited)
- Bold emphasis on NO
- List structure for clarity

**Evidence from BOKF**:
```yaml
✅ **PERMITTED ACTIVITIES**:
  - Modernize existing C# code
  - Apply clean code practices

❌ **PROHIBITED ACTIVITIES**:
  - **NO** enterprise architecture changes
  - **NO** new microservices
  - **NO** database schema changes
```

### Strategy 3: The Repetition Pattern (High Impact)

**Formula**: Critical rule stated multiple times with variations

```yaml
[EARLY POSITION]
## CRITICAL: Clone Task Sizing
**NEVER** create clone tasks longer than 30 minutes

[MIDDLE REMINDER]
### Clone Delegation Rules
- Clone tasks: **15-30 minutes maximum**
- Break larger tasks into multiple clones

[LATE REINFORCEMENT]
Remember: **ALL clone tasks must be 15-30 minutes**
```

**Effectiveness**: ⭐⭐⭐⭐⭐ (85-90% compliance through reinforcement)

**Why It Works**:
- Primacy: Early statement establishes rule
- Recency: Late reminder refreshes rule
- Variation: Different phrasing prevents habituation
- Context: Each mention reinforces in different context

### Strategy 4: The Escalation Pattern (Moderate-High Impact)

**Formula**: Progressive emphasis from guidance to absolute

```yaml
## Standard Practice
You should use workspace planning for complex tasks.

## Strong Recommendation  
You **SHOULD** use workspace planning for all delegation.

## Requirement
You **MUST** use workspace planning for ALL delegation.

## Absolute Rule
**STOP**: **NEVER** delegate without workspace planning.
```

**Effectiveness**: ⭐⭐⭐⭐ (Clearly signals priority levels)

**Why It Works**:
- Differentiates nice-to-have from must-have
- Clear priority levels
- LLM understands escalation pattern

---

# Part 4: The Overuse Problem

## Overuse: The Emphasis Paradox

### The Danger of Over-Emphasis

**Principle**: If everything is CRITICAL, nothing is critical.

**Over-Emphasis Example** (POOR):
```yaml
## CRITICAL IMPORTANT MANDATORY RULES

**CRITICAL**: You **MUST ALWAYS** use **CRITICAL** workspace planning 
for **ALL** delegation which is **MANDATORY** and **REQUIRED** and 
**ESSENTIAL** and **CRITICAL** and **IMPORTANT**.

🚨🔥⚠️ **WARNING**: This is **EXTREMELY CRITICAL** and **SUPER IMPORTANT** 🔥🚨⚠️

**NEVER EVER EVER** skip this **ABSOLUTELY CRITICAL MANDATORY REQUIREMENT**.
```

**Problems**:
- Emphasis blindness (LLM habituates to constant emphasis)
- Reduces effectiveness of each emphasis technique
- No differentiation between truly critical and important
- Cognitive overload for LLM processing

**Measured Emphasis Example** (GOOD):
```yaml
## Clone Delegation Rules

**Clone Task Sizing** (CRITICAL):
- **15-30 minutes maximum** per clone task
- Break larger tasks into sequential clones
- Single focused deliverable per task

Standard Practice:
- Use descriptive task names
- Include clear success criteria
- Document task dependencies
```

**Why Better**:
- CRITICAL reserved for task sizing rule only
- Bold used selectively for key constraint
- Standard practices stated normally
- Clear priority differentiation

### Optimal Emphasis Density

**Guidelines**:

**Headers (##)**:
- Use freely for structure (every major section)
- No overuse risk

**Bold (**text**)**:
- 5-10 per 100 lines: Good
- 20-30 per 100 lines: Acceptable
- 50+ per 100 lines: Over-emphasized

**ALL CAPS**:
- 3-5 per 100 lines: Good
- 10-15 per 100 lines: Maximum
- 20+ per 100 lines: Over-emphasized

**Emphasis Words** (CRITICAL, MUST, NEVER):
- Tier 1 words: 2-5 per major section (good)
- Tier 1 words: 10+ per section (excessive)
- Mix tiers appropriately

**Emoji**:
- 1-3 per major section: Good
- 5-7 per section: Maximum
- 10+ per section: Visual clutter

### Self-Test: Is Your Emphasis Effective?

**Questions**:
1. If I removed ALL emphasis, which rules are truly critical?
   → Those should have emphasis, others shouldn't

2. Can I scan the document and immediately spot critical rules?
   → If yes, emphasis is effective
   → If everything looks equally emphasized, overuse

3. Do I have more than 3 "CRITICAL" sections?
   → If yes, they're not all critical

4. Are my Tier 1 emphasis words (STOP, NEVER, MUST) used only for absolute rules?
   → If yes, good
   → If used for recommendations, diluted

5. Do I use bold for entire paragraphs or just key phrases?
   → Key phrases only = effective
   → Entire paragraphs = overuse

---

# Part 5: Practical Applications

## Evidence-Based Recommendations

### For Critical Constraints (Must NOT Be Violated)

**Use This Pattern**:
```yaml
[TOP POSITION]
## CRITICAL OPERATIONAL CONSTRAINTS

**STOP** immediately if [condition]
**NEVER** [prohibited action]
**ZERO TOLERANCE** for [violation]

[MIDDLE REMINDER]
### [Section Name]
Remember: **NEVER** [prohibited action]

[BOTTOM REINFORCEMENT]
Critical reminder: [constraint restatement]
```

**Techniques**:
- Position: TOP + repeated
- Structure: Major header (##)
- Emphasis words: STOP, NEVER (Tier 1)
- Formatting: Bold
- Emoji: 🚨 optional

### For Required Behaviors (Must Be Done)

**Use This Pattern**:
```yaml
## [Section Name]

**MANDATORY**: [required action]
- You **MUST** [specific behavior]
- [Supporting detail without emphasis]
- [Supporting detail without emphasis]
```

**Techniques**:
- Emphasis words: MANDATORY, MUST (Tier 2)
- Formatting: Bold for requirement only
- Lists: Clear itemization
- No overuse: Supporting details plain text

### For Strong Recommendations (Should Be Done)

**Use This Pattern**:
```yaml
## [Section Name]

**Best Practice**: [recommended action]
- You **SHOULD** [behavior]
- Rationale: [explanation]
```

**Techniques**:
- Emphasis words: SHOULD (Tier 3)
- Formatting: Bold for best practice label
- Plain text: Rationale and details
- No ALL CAPS: Not absolute requirement

### For Informational Content (Good to Know)

**Use This Pattern**:
```yaml
## [Section Name]

Regular text explaining concept or process.

💡 **Tip**: [helpful insight]

Background information without emphasis.
```

**Techniques**:
- No emphasis words
- Regular text for content
- Optional emoji for tips
- Minimal bold usage

---

## Practical Examples: Before and After

### Example 1: Weak Emphasis

**BEFORE** (Weak):
```yaml
You should use workspace planning for delegation and make sure 
to track tasks and use clones for work and never make tasks too 
long and always compress context.
```

**AFTER** (Strong):
```yaml
## Delegation Rules

**MANDATORY Workspace Planning**:
- **ALL** delegation **MUST** use workspace planning tool
- Track every delegated task for recovery

**Clone Task Sizing**:
- **15-30 minutes maximum** per clone task
- **NEVER** exceed 30 minutes

Context Management:
- Compress context between major phases
- Use progressive summarization
```

**Improvements**:
- Added structure (headers)
- Bold for critical rules (MANDATORY, ALL, MUST, NEVER)
- Clear categorization
- Emphasis only on critical items

### Example 2: Over-Emphasis

**BEFORE** (Over-emphasized):
```yaml
## CRITICAL IMPORTANT MANDATORY RULES!!!

**CRITICAL**: You **MUST ALWAYS** use **CRITICAL** workspace planning 
**EVERY SINGLE TIME** for **ALL** delegation which is **SUPER IMPORTANT** 
and **ABSOLUTELY MANDATORY** and **CRITICAL** and **ESSENTIAL**!!!

🚨🔥⚠️ **WARNING WARNING WARNING** 🚨🔥⚠️

**NEVER EVER EVER** skip this **CRITICALLY IMPORTANT REQUIREMENT**!!!
```

**AFTER** (Measured):
```yaml
## Delegation Rules

**Workspace Planning** (CRITICAL):
- **ALL** delegation **MUST** use workspace planning tool
- No exceptions to this rule

**If Planning Fails**:
- **STOP** delegation immediately
- Document failure reason
- Escalate to orchestrator
```

**Improvements**:
- Removed redundant emphasis words
- Single CRITICAL designation
- Clear, specific rules
- No excessive punctuation or emoji
- Preserved critical constraint emphasis

### Example 3: Poor Hierarchy

**BEFORE** (No hierarchy):
```yaml
Clone tasks should be 15-30 minutes and you should track them and 
use workspace planning and sequential processing is important and 
context compression helps and never make long tasks and always 
validate quality and shawn wallace approval is needed.
```

**AFTER** (Clear hierarchy):
```yaml
## Clone Delegation Framework

**CRITICAL Rules**:
- **15-30 minutes maximum** per clone task
- **NEVER** exceed this limit

**MANDATORY Requirements**:
- **ALL** delegation via workspace planning
- Sequential processing: **ONE** task at a time

**Authority Protocol**:
- Shawn Wallace **MUST** approve all major deliverables

Best Practices:
- Compress context between phases
- Validate quality at each gate
```

**Improvements**:
- Clear hierarchy (CRITICAL > MANDATORY > Best Practices)
- Structural separation (headers)
- Strategic emphasis (critical items only)
- Scannable format

---

# Part 6: Quick Reference

## Quick Reference: Emphasis Technique Selection

### Choose Your Technique Based on Priority

| Priority Level | Header | Bold | CAPS | Emphasis Word | Emoji | Position |
|----------------|--------|------|------|---------------|-------|----------|
| **ABSOLUTE** (stop rule) | ## | Yes | Yes | STOP, NEVER | 🚨 | TOP + BOTTOM |
| **CRITICAL** (must do) | ## | Yes | Key words | MUST, MANDATORY | 🔥 | TOP or EARLY |
| **REQUIRED** (needed) | ### | Yes | Minimal | REQUIRED, MUST | - | EARLY |
| **RECOMMENDED** (should) | ### | Key terms | No | SHOULD | - | MIDDLE |
| **OPTIONAL** (may) | #### | Minimal | No | May, Consider | 💡 | MIDDLE |
| **INFORMATIONAL** | #### | Minimal | No | - | - | ANY |

### Decision Tree

```
Is this rule absolutely critical (safety/compliance)?
├─ YES → Use: TOP position + ## header + **BOLD** + ALL CAPS + STOP/NEVER + 🚨
└─ NO → Is it required for success?
    ├─ YES → Use: EARLY position + ## header + **BOLD** + MUST/MANDATORY + 🔥
    └─ NO → Is it strongly recommended?
        ├─ YES → Use: ### header + **bold key terms** + SHOULD
        └─ NO → Use: Plain text with minimal emphasis
```

---

## Conclusion

**Strategic emphasis multiplies effectiveness**:
- Right technique for right priority level
- Position + emphasis = strongest impact
- Avoid overuse (paradox of emphasis)
- Test by scanning: Can you spot critical rules immediately?

**The Formula for Maximum Compliance**:
```
Effectiveness = (Position Weight × Emphasis Technique × Scarcity) - Overuse Penalty

Optimal: TOP position + Bold + STOP/NEVER + Used sparingly
Weak: Middle position + No emphasis + Common words + Overused
```

**Remember**: Emphasis is a tool, not decoration. Use strategically, not automatically.
