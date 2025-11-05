# 🧭 Agent System Extraction Checklist

## 1️. UI & Field Discovery
- [ ] Capture **all UI fields** visible on the screen or configuration page.  
- [ ] Record each field’s:
  - Display Label  
  - Field Type (Text, Dropdown, Date Picker, Checkbox, etc.)  
  - Required / Optional status  
  - Default value and possible dropdown options  
- [ ] Note any **dynamic visibility** or enablement conditions.  
- [ ] Document **UI alert messages** including:
  - JavaScript popups and system alerts
  - Validation error messages
  - Informational text displays
  - Auto-upgrade or system notifications  
  - Warning messages or confirmations
  - Confirmation dialogs
- [ ] For each alert, capture:
  - **Location:** Where alert appears (specific page/section)
  - **Trigger:** What condition causes it (user action, system state, etc.)
  - **Alert Text:** Exact message text in **bold quotes**
  - **Alert Type:** JavaScript popup, validation error, system notification, etc.

### 1.1 Complete Option Enumeration (MANDATORY)
- [ ] For **EVERY dropdown/selection field**, extract **ALL possible options** with source evidence
- [ ] Document **selection consequences**: What happens when each option is chosen?
- [ ] Capture **business rules** that fire based on selections
- [ ] Extract **value ranges** and typical business usage patterns
- [ ] Record **premium impacts**, **additional requirements**, or **conditional logic** triggered by each selection
- [ ] Identify **option dependencies** (Option A available only if Condition X met)
- [ ] Document **business meaning** of each option (not just technical values)

**Quality Standard**: "Has dropdown with various options" is INSUFFICIENT. Must document complete option universe with business impact.

## 1.5️. Enhanced UI Interaction Analysis (For Complex Components)

**Trigger Conditions:** Modal popups, multi-step workflows, dynamic form interactions, validation-heavy interfaces

- [ ] Document **complete user interaction flows**:
  - Initial display state for all elements
  - Each user action and immediate system response
  - Visual state transitions (normal → error → recovery)
  - Progressive disclosure sequences (what triggers additional fields)
  
- [ ] Capture **visual feedback patterns**:
  - Color changes (black → red labels, border changes)
  - Dynamic label text variations
  - Icon/indicator appearances (asterisks, checkmarks, tooltips)
  - Hover states and focus behavior
  
- [ ] Map **error recovery workflows**:
  - How users identify and fix validation issues
  - Visual indicators during error resolution
  - Success confirmation feedback patterns
  - Form submission prevention/enablement logic

- [ ] Record **client-side interaction evidence**:
  - JavaScript function calls for UI behavior
  - CSS classes for different visual states
  - Event handlers for user actions
  - Real-time validation timing and feedback

## 2️. Validation & Rule Extraction
- [ ] Identify **validation logic** applied on all fields:
  - Required field validations  
  - Range or pattern checks  
  - Conditional dependencies (Field B required if Field A = X)  
- [ ] Record all **error messages / warning text** exactly as they appear.  
- [ ] Map each validation rule to its **triggering condition**.  
- [ ] Confirm if validation is **client-side (JavaScript)** or **server-side (backend)**.  

## 3. Business Logic Analysis
- [ ] Locate logic controlling:
  - Field population and defaulting  
  - Calculations (premium, factors, multipliers)  
  - Auto-upgrade or downgrade rules  
  - Visibility or availability of endorsements / forms  
- [ ] Identify cross-dependencies with other modules (Policy, Billing, Claims).  
- [ ] Note any **state-specific or regulatory logic** (e.g., KY, IN, IL variations).  

## 4. Event & Workflow Tracing
- [ ] Capture **client-side events** (onChange, onClick, onBlur) and linked functions.  
- [ ] Identify **workflow triggers**:
  - Save / Rate / Bind operations  
  - Endorsement or Renewal triggers  
- [ ] Document the **methods, classes, or functions** invoked at each event.  
- [ ] Verify that system events align with expected user interactions.
- [ ] For enhanced UI components, capture **micro-interactions**:
  - Hover states and tooltips
  - Focus/blur behavior  
  - Real-time validation feedback timing
  - Animation or transition effects  

## 5. Evidence Collection
- [ ] For every observation, capture:
  - Screenshot or snippet of UI / message  
  - Source-code excerpt (line numbers where logic is implemented)  
  - File path or object name  
- [ ] Tag evidence as:
  - ✅ Verified from Source Code  
  - 🧩 Inferred from UI  
  - ⚠️ Unverified / Needs Recheck  

## 6. Requirement Documentation
- [ ] Convert extracted logic into **business-friendly field names and behavior statements**.
- [ ] Use the standardized requirement format:
  ```
  Field Name:
  Field Type:
  Visibility Condition:
  Required Condition:
  Validation Message:
  Source Evidence:
  ```
- [ ] Cross-reference related validations, rules, or events in the same section.
- [ ] For complex UI components, use **Enhanced UI Interaction template** instead of basic field format
- [ ] Apply enhanced documentation when:
  - ✅ Modal popups with complex validation
  - ✅ Multi-step user workflows  
  - ✅ Dynamic visual feedback
  - ❌ Simple text fields
  - ❌ Basic dropdowns
- [ ] Mark any assumptions clearly as “UNVERIFIED.”  

## 6.5. Endorsement-Specific Extraction (NEW)

**For Endorsement Analysis (Checkboxes, Optional Coverages):**

- [ ] **Identify Endorsement Pattern**: Checkbox selection → Downstream application requirement
- [ ] **Document Progressive Disclosure**: Additional fields that appear when endorsement selected
- [ ] **Trace Application Dependencies**:
  - Does endorsement selection require named individual entry in Application module?
  - What specific data must user enter in downstream modules?
  - Are there count validation requirements (e.g., "Number of Waivers = 2" requires exactly 2 names)?
- [ ] **Extract Downstream Module Impacts**:
  - Applications Page requirements
  - Rating Engine premium calculation impacts  
  - Claims Processing coverage determination changes
  - Billing System premium/invoice impacts
  - Regulatory Compliance reporting requirements
- [ ] **Validate Cross-Module Workflows**:
  - User cannot complete quote without visiting application module
  - System validates endorsement selections have corresponding downstream data
  - Error conditions when endorsement selected but downstream requirements not met

**Data Exclusion Validation:**
- [ ] **Exclude `IgnoreForLists="Yes"`**: Remove any dropdown options marked with this attribute from documentation
- [ ] **User-Accessible Options Only**: Document only options actually available to end users
- [ ] **Verify Source**: Confirm all options come from actual source code, not static configuration files

**Business Language Requirements:**
- [ ] **Remove Technical Methods**: No `CheckWaiverOfSubro()`, `govStateQuote.HasWaiverOfSubrogation` in business descriptions
- [ ] **Convert to User Actions**: "When the endorsement checkbox is selected" instead of method calls
- [ ] **Focus on Workflows**: "Users must add individual records" instead of technical property assignments

## 7. Quality & Cross-Verification
- [ ] Ensure each requirement is backed by **direct system evidence**.  
- [ ] Reconcile UI findings with **source code** to prevent assumption-based entries.  
- [ ] **Endorsement Validation**: Verify endorsement analysis follows new standardized format
- [ ] **Cross-Module Verification**: Confirm downstream impacts are source-code verified, not assumed