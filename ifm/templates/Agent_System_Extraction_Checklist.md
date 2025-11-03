# 🧭 Agent System Extraction Checklist

## 1️. UI & Field Discovery
- [ ] Capture **all UI fields** visible on the screen or configuration page.  
- [ ] Record each field’s:
  - Display Label  
  - Field Type (Text, Dropdown, Date Picker, Checkbox, etc.)  
  - Required / Optional status  
  - Default value and possible dropdown options  
- [ ] Note any **dynamic visibility** or enablement conditions.  
- [ ] Document **pop-ups, alerts, or confirmation messages** triggered by user actions.  

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

## 7. Quality & Cross-Verification
- [ ] Ensure each requirement is backed by **direct system evidence**.  
- [ ] Reconcile UI findings with **source code** to prevent assumption-based entries.  