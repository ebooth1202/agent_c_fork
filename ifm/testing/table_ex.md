# WCP Endorsement Downstream Effects - Visualization Examples

## Table Approach 1: Complete Workflow Matrix

| Endorsement Selection | Coverage Page Action | Application Page Requirement | User Must Enter | Additional Requirements | Data Storage |
|----------------------|---------------------|----------------------------|-----------------|------------------------|--------------|
| **Inclusion of Sole Proprietors** | ✅ Check checkbox | Navigate to Named Individuals → Add each person | • Person Name<br>• Type (Sole Proprietor/Partner/LLC) | • Health insurance documentation upload<br>• Written proof of coverage | `GoverningStateQuote.InclusionOfSoleProprietorRecords` |
| **Waiver of Subrogation** | ✅ Check checkbox<br>📝 Enter count (e.g., "2") | Navigate to Named Individuals → Add exactly 2 waivers | • Name of each waiver<br>• Must match count entered | None | `GoverningStateQuote.WaiverOfSubrogationRecords` |
| **Blanket Waiver of Subrogation** | ✅ Check checkbox | ❌ No application action required | None | None | `GoverningStateQuote.BlanketWaiverOfSubrogation = "4"` |
| **Exclusion of Amish Workers (IN)** | ✅ Check checkbox | Navigate to Named Individuals → Add each worker | • Name of each excluded worker | None | `INQuote.ExclusionOfAmishWorkerRecords` |
| **Exclusion of Executive Officer (IN/KY)** | ✅ Check checkbox | Navigate to Named Individuals → Add each officer | • Name of each excluded officer | None | `INQuote.ExclusionOfSoleProprietorRecords`<br>`KYQuote.ExclusionOfSoleProprietorRecords` |
| **Exclusion of Sole Proprietors (IL)** | ✅ Check checkbox | Navigate to Named Individuals → Add each individual | • Name of each excluded person | None | `ILQuote.ExclusionOfSoleProprietorRecords_IL` |
| **Rejection of Coverage (KY)** | ✅ Check checkbox | Navigate to Named Individuals → Add each person | • Name of each person rejecting coverage | None | `KYQuote.KentuckyRejectionOfCoverageEndorsementRecords` |

---

## Table Approach 2: User Journey Flow Table

| Step | Coverage Selection Module | Application Module | Result |
|------|--------------------------|-------------------|---------|
| 1️⃣ | User checks "Waiver of Subrogation" | ❌ Not yet available | Checkbox checked, field appears |
| 2️⃣ | User enters "Number of Waivers: 2" | ❌ Not yet available | Count stored, validation activated |
| 3️⃣ | User saves coverage selections | ❌ Not yet available | Data persisted to quote |
| 4️⃣ | User navigates to Application page | ✅ "Waiver of Subrogation" section appears | System shows named individual interface |
| 5️⃣ | System requirement activated | ✅ User must add exactly 2 waiver names | Validation: Count must match |
| 6️⃣ | User adds first waiver name | ✅ "Waiver of Subrogation - #1" created | First record saved |
| 7️⃣ | User adds second waiver name | ✅ "Waiver of Subrogation - #2" created | Second record saved |
| 8️⃣ | System validation | ✅ Count matches (2 names = 2 waivers) | ✅ Complete |

---

## Table Approach 3: Impact Classification Matrix

| Endorsement | State Availability | Count Required? | Documentation Required? | Validation Level | Complexity |
|-------------|-------------------|-----------------|------------------------|------------------|------------|
| **Inclusion of Sole Proprietors** | All (IN/IL/KY) | ❌ Open-ended | ✅ Health insurance proof | High | 🔴 Complex |
| **Waiver of Subrogation** | IN/IL only | ✅ Must match count | ❌ None | High | 🔴 Complex |
| **Blanket Waiver of Subrogation** | IN/IL only | ❌ N/A - No application action | ❌ None | None | 🟢 Simple |
| **Exclusion of Amish Workers** | IN only | ❌ Open-ended | ❌ None | Medium | 🟡 Moderate |
| **Exclusion of Executive Officer** | IN/KY only | ❌ Open-ended | ❌ None | Medium | 🟡 Moderate |
| **Exclusion of Sole Proprietors (IL)** | IL only | ❌ Open-ended | ❌ None | Medium | 🟡 Moderate |
| **Rejection of Coverage (KY)** | KY only | ❌ Open-ended | ❌ None | Medium | 🟡 Moderate |

---

## Flow Diagram Approach

```
WCP POLICY LEVEL COVERAGES PAGE
├── Employer's Liability Limits ──────────► Rating Engine (No App Action)
├── Experience Modification ──────────────► Rating Engine (No App Action) 
├── Experience Mod Effective Date ────────► Rating Engine (No App Action)
├── Farm Indicator (Auto) ────────────────► Rating Engine (No App Action)
└── ENDORSEMENTS:
    ├── Inclusion of Sole Proprietors ────┐
    ├── Waiver of Subrogation ────────────┤
    ├── Exclusion of Amish Workers ───────┤──► WCP APPLICATION MODULE
    ├── Exclusion of Executive Officer ───┤    └── Named Individuals Section
    ├── Exclusion of Sole Proprietors ────┤        ├── Add Individual Names
    ├── Rejection of Coverage ────────────┤        ├── Enter Details
    └── Blanket Waiver ──────────────────┘        └── Save Records
                    │                              
                    └─ (No App Action) ────────────► Direct to Rating
```

---

## Visual Impact Summary

### 🔴 High Impact Endorsements (Complex Downstream Requirements)
- **Inclusion of Sole Proprietors** - Names + Types + Health Insurance Documentation
- **Waiver of Subrogation** - Names must match exact count entered

### 🟡 Medium Impact Endorsements (Standard Downstream Requirements)  
- **Exclusion of Amish Workers** - Individual names required
- **Exclusion of Executive Officer** - Individual names required
- **Exclusion of Sole Proprietors (IL)** - Individual names required
- **Rejection of Coverage (KY)** - Individual names required

### 🟢 Low Impact Endorsements (No Downstream Requirements)
- **Blanket Waiver of Subrogation** - Direct processing, no application actions

---

## Development Planning Matrix

| Endorsement | Frontend Changes | Backend Changes | Validation Logic | Testing Complexity |
|-------------|------------------|-----------------|------------------|-------------------|
| **All Named Individual Endorsements** | Application UI for name entry | Collections management | Name validation + count matching | High - Multi-step workflows |
| **Inclusion of Sole Proprietors** | + Document upload UI | + Document storage | + Health insurance validation | Very High - Documents + Compliance |
| **Waiver of Subrogation** | + Count matching validation | + Count synchronization | + Exact count validation | Very High - Count dependencies |
| **Blanket Waiver** | Rating integration only | Premium calculation | Premium value validation | Low - Direct processing |

---

## Stakeholder Communication Summary

**For Business Stakeholders:**
> "Most endorsements create a two-step user process: Select on Coverage page → Enter individual names on Application page"

**For Development Teams:**  
> "6 of 7 endorsements require Named Individual collection interface with state-specific data storage and validation"

**For Testing Teams:**
> "Each endorsement requires end-to-end workflow testing across Coverage → Application modules with validation verification"