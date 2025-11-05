# WCP Policy Level Coverages - COMPLETE REQUIREMENTS DOCUMENT

## Section 1 - General Information Fields

### Field Specifications

#### 1.1 Employer's Liability Coverage Limits
**Field Type**: Single-select dropdown
**Required**: Yes
**Default Value**: "500/500/500"

**Complete Option Set**: Options loaded dynamically from database via `EmployersLiabilityId` property lookup for WCP LOB. Confirmed options include:
- 100/500/100 (Internal ID: 311)
- 500/500/500 (Internal ID: 313) - Default selection
- Additional limit combinations available through system configuration

**Selection Impact**: 
- Affects premium calculation in rating engine
- Determines umbrella policy eligibility (500/500/500 minimum required)
- Auto-upgrade logic: 100/500/100 automatically upgraded to 500/500/500 when policy restart required

#### 1.2 Experience Modification Factor
**Field Type**: Numeric input with decimal support
**Required**: Yes
**Default Value**: 1
**Format**: Decimal number (e.g., 0.85, 1.0, 1.25)

**Input Validation**:
- JavaScript keypress validation allows numbers 0-9 and decimal point only
- Real-time validation on value entry
- AutoPostBack enabled for immediate processing

#### 1.3 Experience Modification Effective Date
**Field Type**: Date picker with calendar popup
**Required**: Conditionally (when Experience Modification ≠ 1)
**Format**: MM/dd/yyyy
**Default Value**: Current date

### Validation Rules

**Employer's Liability Validation**:
- Selection required - displays "Missing Employers Liability" error if not selected
- Automatic upgrade validation: 100/500/100 limits trigger upgrade to 500/500/500 with user notification

**Experience Modification Validation**:
- Must be numeric value
- When value = 0 or 1: Effective Date field disabled and cleared
- When value ≠ 1: Effective Date field enabled and required

**Cross-Field Validation**:
- Experience Modification of 1 automatically disables and clears Effective Date
- Values other than 1 enable Effective Date field and require date selection

### User Experience & Validation

**Real-Time Field Interaction**:
- Experience Modification field triggers immediate validation on keyup
- JavaScript handler: `Wcp.ExperienceModificationValueChanged(modFieldId, dateFieldId)`
- Date field enabling/disabling occurs instantly based on modification value

**User Notification Patterns**:
- Auto-upgrade alert: "The Employers Liability limit defaulted to 500/500/500, which is the minimum limit required to quote an umbrella."
- Alert triggered when 100/500/100 upgraded during policy restart scenarios

### Conditional Logic

**Experience Modification Date Logic**:
```
IF Experience Modification = 1 THEN
    Disable Effective Date field
    Clear Effective Date value
ELSE
    Enable Effective Date field  
    Require Effective Date selection
END IF
```

**Employer's Liability Reset Logic**:
```
IF existing EmployersLiabilityId = "311" (100/500/100) AND policy restart required THEN
    Set EmployersLiabilityId = "313" (500/500/500)
    Display upgrade notification alert
END IF
```

### Architecture Considerations

**Data Storage Pattern**:
- Experience Modification stored at top-level Quote object (`ExperienceModificationFactor`)
- Effective dates stored at multiple levels:
  - Top-level: `RatingEffectiveDate`, `ModificationProductionDate` 
  - State-level: `AnniversaryRatingEffectiveDate` for each subquote
- Employer's Liability stored per state subquote (`EmployersLiabilityId`)

**JavaScript Integration**:
- Client-side validation handlers attached via server-side code
- Real-time field interaction without postback for user experience
- Integration with `Wcp.js` client-side library for business logic

### Source Code Details

**Primary Implementation**: `ctl_WCP_Coverages.ascx/.vb`
- Line 173: Dropdown population via `QQHelper.LoadStaticDataOptionsDropDown`
- Lines 178-184: Default selection logic for "500/500/500"
- Lines 132-139: Auto-upgrade logic with user notification
- Lines 288-307: Experience Modification and date field logic
- Lines 576-588: Save logic with multi-level data storage

## Section 2 - Locations Management

### Field Specifications

#### 2.1 Location List Container
**Implementation**: Embedded user control (`ctl_WCP_LocationList`)
**Container Element**: `<div id="divLocations" runat="server">`
**Integration Pattern**: Delegated location management to specialized control

### User Experience & Validation

**Control Integration**:
- Parent control provides location container structure
- Location-specific business logic handled by embedded `ctl_WCP_LocationList` control
- Standard ASP.NET user control communication patterns for data exchange

### Architecture Considerations

**Separation of Concerns**:
- Policy Level Coverages control focuses on coverage and endorsement logic  
- Location management delegated to specialized location control
- Clean interface boundary between coverage and location functionality

**Cross-Control Communication**:
- Location data changes may trigger coverage validation updates
- Location address changes can affect state-based endorsement availability

### Source Code Details

**Primary Implementation**: `ctl_WCP_Coverages.ascx`
- Location container: `<div id="divLocations" runat="server">`
- Embedded control: `<uc1:ctl_WCP_Locations id="ctl_WCP_LocationList" runat="server">`

## Section 3 - Classification Information

### Field Specifications  

#### 3.1 Classification List
**Field Type**: Dynamic repeater-based list
**Item Template**: `ctl_WCP_Classification` user controls
**Capacity**: Multiple classifications per quote
**State Support**: Single-state and multi-state quote configurations

### User Experience & Validation

**Dynamic List Management**:
- Add New Classification: `lbAddNewClassification` link button
- Save Classifications: `btnSaveClassifications` saves all classification changes
- Individual classification controls handle classification-specific logic

**Event-Driven Architecture**:
- Classification controls raise events for Add, Delete, and Populate requests
- Parent control responds to events and coordinates list management
- Event handlers: `AddNewClassification`, `DeleteClassification`, `HandleClassificationPopulateRequest`

### Conditional Logic

**Single-State vs Multi-State Logic**:
```
IF Quote.EffectiveDate supports multistate THEN
    Load classifications from GetMultistateClassifications()
    Set state-specific indices for each classification
    Configure Diamond state IDs for rating integration
ELSE  
    Load classifications from Quote.Locations(0).Classifications
    Set single-state classification indices
END IF
```

**Multi-State Classification Aggregation**:
- Aggregates classifications from all active quote states
- Maintains state association for each classification  
- Preserves classification order and indexing per state

### Architecture Considerations

**Index Management Strategy**:
- `ClassificationIndex`: Overall position in unified list
- `StateQuoteClassificationIndex`: Position within specific state's classifications  
- `ClassificationStateId`: Diamond state ID for rating engine integration

**Data Storage Pattern**:
- Single-state: Classifications stored at `Quote.Locations(0).Classifications`
- Multi-state: Classifications stored per state at respective location level
- State association maintained through `ClassIficationItem_enum` structure

### Source Code Details

**Primary Implementation**: `ctl_WCP_Coverages.ascx.vb`
- Lines 421-485: `PopulateClassifications()` method with single/multi-state logic
- Lines 486-529: `GetMultistateClassifications()` method for multi-state aggregation
- Lines 147-153: Event handler attachment for classification controls
- Classification container: `<div runat="server" id="divClassificationList">`

## Section 4 - Endorsements (Enhanced UI Specifications)

### Field Specifications

The Endorsements section contains 7 distinct endorsement checkboxes with complex state-conditional behavior, dynamic labeling, and progressive disclosure patterns requiring enhanced user interaction documentation.

#### 4.1 Inclusion of Sole Proprietors, Partners, and LLC Members
**Field Type**: Checkbox
**Form Code**: WC 00 03 10
**Applicable States**: IN/IL (base), extends to include KY when Kentucky coverage enabled
**Visibility**: Always visible when WCP quote active
**JavaScript Handler**: `Wcp.CoverageCheckboxChanged('INCLSOLE', checkboxId, '', '', '', '', '')`

#### 4.2 Blanket Waiver of Subrogation  
**Field Type**: Checkbox
**Form Code**: WCP 1001
**Applicable States**: IN/IL only
**Visibility**: Visible only when Indiana OR Illinois present on quote
**JavaScript Handler**: `Wcp.CoverageCheckboxChanged('BLNKTW', checkboxId, '', '', '', '', '')`

#### 4.3 Waiver of Subrogation
**Field Type**: Checkbox with progressive disclosure
**Form Code**: WC 00 03 13  
**Applicable States**: IN/IL only
**Progressive Disclosure**: Reveals "Number of Waivers" numeric input field when checked
**JavaScript Handler**: `Wcp.CoverageCheckboxChanged('WAIVERSUBRO', checkboxId, numberRowId, '', '', '', '')`

**Associated Field - Number of Waivers**:
- **Field Type**: Numeric input (integers only)
- **Visibility**: Hidden by default, shown when parent checkbox checked
- **Validation**: Client-side keypress validation allows numbers 0-9 only
- **Business Impact**: Each waiver generates $50 premium (`WaiverOfSubrogationPremiumId = "3"`)

#### 4.4 Exclusion of Amish Workers
**Field Type**: Checkbox  
**Form Code**: WC 00 03 08
**Applicable States**: Indiana only
**Visibility**: Visible only when Indiana present on quote
**JavaScript Handler**: `Wcp.CoverageCheckboxChanged('AMISH', checkboxId, '', '', '', '', '')`

#### 4.5 Exclusion of Executive Officer
**Field Type**: Checkbox
**Form Code**: WC 00 03 08  
**Applicable States**: IN/KY
**Visibility**: Visible when Indiana OR Kentucky present on quote
**Complex JavaScript Behavior**: Handler parameters vary based on Indiana presence
- **With Indiana**: Includes informational message trigger
- **Without Indiana**: Standard handler only

#### 4.6 Exclusion of Sole Proprietors, Partners, Officers, LLC Members & Others (Illinois)
**Field Type**: Checkbox
**Form Code**: WC 12 03 07
**Applicable States**: Illinois only
**Visibility**: Visible only when Illinois present on quote AND multistate-capable effective date
**JavaScript Handler**: `Wcp.CoverageCheckboxChanged('EXCLSOLE_IL', checkboxId, '', '', '', '', '')`

#### 4.7 Rejection of Coverage Endorsement
**Field Type**: Checkbox
**Form Code**: WC 16 03 01
**Applicable States**: Kentucky only  
**Visibility**: Visible when Kentucky coverage enabled and effective date >= Kentucky WCP effective date
**JavaScript Handler**: Standard checkbox behavior (no specialized handler)

### State-Based Conditional Logic

#### Complete State Combination Matrix

**State Presence Detection Logic**:
The system evaluates active states on the quote using `SubQuotesContainsState()` function and applies endorsement visibility based on the following matrix:

| Endorsement | IN Only | IL Only | KY Only | IN+IL | IN+KY | IL+KY | IN+IL+KY |
|-------------|---------|---------|---------|-------|-------|-------|----------|
| Inclusion of Sole Prop | Show (IN/IL) | Show (IN/IL) | Show (IN/IL/KY) | Show (IN/IL) | Show (IN/IL/KY) | Show (IN/IL/KY) | Show (IN/IL/KY) |
| Blanket Waiver | Show | Show | Hide | Show | Show | Show | Show |
| Waiver of Subro | Show | Show | Hide | Show | Show | Show | Show |
| Excl Amish Workers | Show | Hide | Hide | Show | Show | Hide | Show |
| Excl Executive Officer | Show | Hide | Show | Show | Show | Show | Show |
| Excl Sole Prop (IL) | Hide | Show | Hide | Show | Hide | Show | Show |
| Rejection Coverage (KY) | Hide | Hide | Show | Hide | Show | Show | Show |

#### Dynamic Label Modification Logic

**Inclusion of Sole Proprietors Label Variations**:
- **Kentucky Governing State**: "(IN/IL/KY)"
- **Kentucky Enabled (Non-Gov)**: "(IN/IL/KY)"  
- **Kentucky Disabled**: "(IN/IL)"

**Exclusion of Executive Officer Label Variations**:
- **Kentucky Enabled**: "(IN/KY)"
- **Kentucky Disabled**: "(IN)"

**Label Assignment Code Pattern**:
```
IF Quote.QuickQuoteState = Kentucky THEN
    Set labels to include KY
    Show KY-specific endorsements
ELSE IF Kentucky coverage enabled by effective date THEN
    Set labels to include KY  
    Show KY-specific endorsements
ELSE
    Set labels without KY
    Hide KY-specific endorsements
END IF
```

### Enhanced User Interaction Flows

#### Flow 1: Waiver of Subrogation Progressive Disclosure
```
1. User views Endorsements section
2. Waiver of Subrogation checkbox visible (if IN/IL present)
3. User checks Waiver of Subrogation
4. JavaScript handler triggers with numberRowId parameter
5. "Number of Waivers" row becomes visible with slide-down effect
6. User enters numeric value in Number of Waivers field
7. Field validation restricts to numeric input only
8. Save operation stores checkbox state and waiver count
9. Premium calculation includes $50 per waiver
```

#### Flow 2: State-Based Field Visibility Update
```
1. Quote initially loaded with specific state combination
2. System evaluates active states using SubQuotesContainsState()
3. Endorsement visibility matrix applied
4. Labels updated based on state combination  
5. JavaScript handlers attached with appropriate parameters
6. User sees only applicable endorsements for their state combination
7. Field interactions limited to visible/applicable endorsements
```

#### Flow 3: Indiana Informational Message Trigger
```  
1. User interacts with Exclusion of Executive Officer checkbox
2. System checks: (checkbox checked OR pre-multistate date) AND Indiana present
3. IF conditions met: Show Indiana form requirement message
4. Message includes link to required state form 36097
5. Message provides submission instructions to WC board and underwriter
6. User must acknowledge compliance requirement before proceeding
```

### Progressive Disclosure Patterns

#### Pattern 1: Conditional Field Revealing
**Trigger Field**: Waiver of Subrogation checkbox
**Revealed Field**: Number of Waivers input field
**Behavior**: 
- Hidden by default (`style="display:none"`)
- Revealed when checkbox checked (`style="display:''`)
- Hidden again when checkbox unchecked

**Implementation**: `CheckWaiverOfSubro()` method controls visibility
```javascript
IF chkWaiverofSubro.Checked THEN
    trNumberOfWaiversRow.style.display = ''
ELSE  
    trNumberOfWaiversRow.style.display = 'none'
END IF
```

#### Pattern 2: Contextual Information Display
**Trigger Conditions**: Multiple condition evaluation for Indiana message
**Revealed Element**: Indiana compliance information row
**Complex Logic**:
```
Show Information IF:
    (Exclusion of Executive Officer checked OR pre-multistate effective date) 
    AND Indiana present on quote
Hide Information IF:
    All other conditions
```

### Cross-Field Dependencies

#### Dependency 1: Experience Modification ↔ Effective Date
**Primary Field**: Experience Modification factor
**Dependent Field**: Experience Modification Effective Date  
**Relationship**: Date field enabled/disabled based on modification value
**Logic**: Value = 1 disables date; Value ≠ 1 enables date

#### Dependency 2: State Presence ↔ Endorsement Availability
**Primary Data**: Active states on quote (IN, IL, KY)
**Dependent Fields**: All 7 endorsement checkboxes
**Relationship**: Field visibility determined by state combination matrix
**Dynamic Updates**: Field visibility changes when quote states modified

#### Dependency 3: Checkbox State ↔ Progressive Disclosure
**Primary Field**: Waiver of Subrogation checkbox
**Dependent Field**: Number of Waivers input
**Relationship**: Input field visibility controlled by checkbox state
**Business Logic**: Unchecked clears waiver count and premium impact

### Complete State Combination Matrix

#### Endorsement Behavior by State Configuration

**Indiana-Only Quote (IN)**:
- Inclusion of Sole Proprietors: Visible, labeled "(IN/IL)"
- Blanket Waiver of Subrogation: Visible
- Waiver of Subrogation: Visible with Number of Waivers disclosure
- Exclusion of Amish Workers: Visible (Indiana-specific)
- Exclusion of Executive Officer: Visible, labeled "(IN)", includes info message
- Exclusion of Sole Proprietors (IL): Hidden
- Rejection of Coverage (KY): Hidden

**Illinois-Only Quote (IL)**:
- Inclusion of Sole Proprietors: Visible, labeled "(IN/IL)"
- Blanket Waiver of Subrogation: Visible  
- Waiver of Subrogation: Visible with Number of Waivers disclosure
- Exclusion of Amish Workers: Hidden
- Exclusion of Executive Officer: Hidden
- Exclusion of Sole Proprietors (IL): Visible (Illinois-specific)
- Rejection of Coverage (KY): Hidden

**Kentucky-Only Quote (KY) - When KY Enabled**:
- Inclusion of Sole Proprietors: Visible, labeled "(IN/IL/KY)"
- Blanket Waiver of Subrogation: Hidden (no IN/IL)
- Waiver of Subrogation: Hidden (no IN/IL)  
- Exclusion of Amish Workers: Hidden
- Exclusion of Executive Officer: Visible, labeled "(IN/KY)", no info message
- Exclusion of Sole Proprietors (IL): Hidden
- Rejection of Coverage (KY): Visible (Kentucky-specific)

**Multi-State Quote (IN+IL+KY)**:
- Inclusion of Sole Proprietors: Visible, labeled "(IN/IL/KY)"
- Blanket Waiver of Subrogation: Visible
- Waiver of Subrogation: Visible with Number of Waivers disclosure
- Exclusion of Amish Workers: Visible (Indiana component)
- Exclusion of Executive Officer: Visible, labeled "(IN/KY)", includes info message
- Exclusion of Sole Proprietors (IL): Visible (Illinois component)
- Rejection of Coverage (KY): Visible (Kentucky component)

### Architecture Considerations

**State Management Strategy**:
- State presence evaluated using `SubQuotesContainsState(SubQuotes, stateCode)` function
- Kentucky enablement determined by effective date comparison against `KentuckyWCPEffectiveDate`  
- Multistate capability checked via `IsMultistateCapableEffectiveDate(Quote.EffectiveDate)`

**JavaScript Integration Architecture**:
- Centralized `Wcp.CoverageCheckboxChanged()` handler with parameter variations
- State-specific parameter passing for contextual behavior
- Real-time DOM manipulation for progressive disclosure effects

**Data Persistence Strategy**:
- Governing state pattern: Some endorsements saved to governing state subquote only
- State-specific pattern: Other endorsements saved to applicable state subquotes
- Cross-state validation: Ensures consistency when endorsement affects multiple states

### Source Code Details

**Primary Implementation**: `ctl_WCP_Coverages.ascx.vb`
- Lines 225-280: State-based display logic in `Populate()` method
- Lines 95-115: JavaScript handler attachment with conditional parameters  
- Lines 318-380: Individual endorsement visibility logic
- Lines 590-650: Save logic with state-specific persistence patterns
- Lines 538-544: `CheckWaiverOfSubro()` progressive disclosure method

**UI Markup**: `ctl_WCP_Coverages.ascx`  
- Endorsement checkboxes with conditional display attributes
- Progressive disclosure containers with default hidden state
- Informational message row with Indiana compliance requirements

## Cross-Module Dependencies

### Rating Engine Integration
**Trigger Events**: Save Coverages, Rate This Quote button click
**Data Flow Direction**: Policy Level Coverages → Rating Engine

**Dependency Pattern**:
```
User selects Employer's Liability limits
↓
Selection stored to SubQuoteObject.EmployersLiabilityId  
↓
Rating engine uses liability limits for premium calculation
↓
Premium results displayed in quote summary
```

**Endorsement Impact on Rating**:
- Waiver of Subrogation: Adds $50 premium per waiver (`WaiverOfSubrogationPremiumId = "3"`)
- Other endorsements: May affect eligibility or require underwriter review
- Employer's Liability: Direct impact on liability premium calculation

### Quote Saving Workflow Integration  
**Trigger Events**: Save Coverages button, Save and Rate button, navigation away from page
**Data Flow Direction**: Policy Level Coverages → Quote Persistence Layer

**Save Operation Sequence**:
```
1. User clicks Save Coverages
2. Client-side validation passes
3. Coverage data collected from all sections
4. Experience Modification saved to top-level Quote object
5. Employer's Liability saved to each state subquote  
6. Endorsements saved to appropriate state subquotes or governing state
7. Quote status updated in database
8. Success confirmation displayed to user
```

### Underwriting Assistance Integration
**Trigger Event**: "Email for UW Assistance" button click  
**Data Flow Direction**: Current quote data → Email system → Underwriting team

**Integration Pattern**:
```
User clicks "Email for UW Assistance"
↓
JavaScript function InitEmailToUW() triggered
↓
Current quote data packaged for underwriter review
↓
Email generated with quote details and coverage selections
↓
Sent to appropriate underwriter based on agency and LOB
```

### Application Module Integration
**Dependency Type**: Downstream workflow continuation
**Data Flow Direction**: Policy Level Coverages → Application processing

**Cross-Module Impact**:
- Exclusion endorsements affect officer/owner coverage in application
- Experience modification factors carry forward to application rating
- Liability limits impact application underwriting requirements

### Billing System Integration  
**Dependency Type**: Premium and endorsement fee processing
**Data Flow Direction**: Policy Level Coverages → Billing calculations

**Integration Points**:
- Employer's Liability selections affect billing premium amounts
- Waiver endorsements create additional billing line items ($50 per waiver)
- State-specific endorsements may have different billing codes by jurisdiction

### Claims Processing Integration
**Dependency Type**: Coverage interpretation for claims handling  
**Data Flow Direction**: Policy Level Coverages → Claims system reference

**Coverage Impact on Claims**:
- Exclusion endorsements limit coverage scope for claims evaluation
- Waiver of subrogation affects claims recovery rights
- State-specific endorsements determine claims handling procedures by jurisdiction

This requirements document provides implementation teams with complete specifications for WCP Policy Level Coverages functionality, including enhanced UI requirements for complex state-conditional endorsement logic and cross-system integration patterns.