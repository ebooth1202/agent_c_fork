# WCP Endorsement Downstream Effects - Trial Format

## 1.0 Waiver of Subrogation Endorsement

### 1.1 User Selections/User Interactions

1.11 When the endorsement checkbox for "Waiver of Subrogation" is selected, the "Number of Waivers" text input field becomes visible and available for user entry.

1.12 The "Number of Waivers" field becomes required for form validation when the checkbox is checked, requiring a numeric value greater than zero.

1.13 When the checkbox is unchecked, the system displays confirmation dialog "Are you sure you want to delete this coverage?" before clearing the waiver data and hiding the Number of Waivers field.

1.14 During save operations, the system stores both the checkbox selection state and the waiver count value for use in downstream processing.

### 1.2 Downstream Impacts

#### 1.21 Applications Page

1.211 When the Waiver of Subrogation endorsement has been selected, the Application page displays the "Waiver of Subrogation" section for data entry.

1.212 The system creates space for waiver records collection, with each record requiring individual name entry through the named individual interface.

1.213 Users must add individual waiver records equal to the number specified on the coverage page, each containing a mandatory name field.

1.214 The system validates each waiver name is not empty with error message "Missing Name" if validation fails.

#### 1.22 Rating Engine

1.221 The waiver selection affects premium calculations through endorsement rating factor application.

1.222 Waiver count and selection data are passed to rating calculations for premium modification based on subrogation waiver endorsement factors.

#### 1.23 Claims Processing

1.231 Waiver records are referenced during claims processing to determine subrogation rights limitations based on the named waivers.

1.232 Claims processing validates claim subrogation against the specific waiver names stored in the application module to determine recovery rights.

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 370-380 (CheckWaiverOfSubro method), Lines 598-612 (Save method) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 25-50 (WaiverOfSubrogation enum), Lines 200-250 (Save method) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 100-150 (Populate method) + ctl_AppSection_WCP

---

## 2.0 Exclusion of Amish Workers Endorsement

### 2.1 User Selections/User Interactions

2.11 The "Exclusion of Amish Workers" checkbox is only visible when Indiana state is included in the quote.

2.12 When the checkbox is selected, the system stores the selection on the Indiana state quote during save operations.

2.13 The checkbox selection triggers the standard coverage confirmation dialog when unchecked: "Are you sure you want to delete this coverage?" to prevent accidental data loss.

2.14 No additional fields are enabled or required on the coverage page when this endorsement is selected.

### 2.2 Downstream Impacts

#### 2.21 Applications Page

2.211 When the Exclusion of Amish Workers endorsement has been selected, the Application page displays the "Exclusion of Amish Workers" section for data entry.

2.212 The system creates space for exclusion records collection, with each record requiring individual name entry through the named individual interface.

2.213 Users must add individual exclusion records for each Amish worker to be excluded, each containing a mandatory name field.

2.214 The system validates each exclusion name is not empty with error message "Missing Name" if validation fails.

2.215 Users can add multiple exclusion records through the "Add New" functionality which creates new exclusion record instances.

#### 2.22 Claims Processing

2.221 Exclusion records are referenced during claims processing to deny coverage for workers listed in the exclusion records collection.

2.222 Claims processing validates worker identity against the exclusion names stored in the application module to determine coverage eligibility.

#### 2.23 Regulatory Compliance

2.231 Exclusion selections are tracked for Indiana Workers Compensation Board reporting requirements through the state-specific exclusion data collection.

2.232 The endorsement selection affects regulatory filing and compliance documentation maintained in the Indiana quote structure.

## Source Code Details:
**Primary Location:** ctl_WCP_Coverages.ascx.vb Lines 675-680 (Save method IN section), Lines 370-375 (Populate visibility) + ctl_WCP_Coverages

**Secondary Location:** ctl_WCP_NamedIndividual.ascx.vb Lines 50-75 (ExclusionOfAmishWorkers enum), Lines 300-350 (Save method) + ctl_WCP_NamedIndividual

**External Dependencies:** ctl_AppSection_WCP.ascx.vb Lines 180-220 (IN state section populate) + ctl_AppSection_WCP