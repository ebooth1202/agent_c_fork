"""
Optimized prompt for Dynamics CRM toolset.

This prompt has been reduced from ~6000 to ~2000 tokens while maintaining
essential information and patterns.
"""

from typing import Any
from agent_c.prompting.prompt_section import PromptSection


class DynamicsCRMPrompt(PromptSection):
    def __init__(self, **data: Any):
        template = (
            "# Microsoft Dynamics CRM Tool\n\n"
            
            "## Overview\n"
            "Query and manipulate Microsoft Dynamics CRM data using OData parameters. "
            "Returns YAML format optimized for token efficiency. "
            "Automatically presents data in appropriate detail level based on result size.\n\n"
            
            "**IMPORTANT**: When user asks for 'my' or 'mine' (e.g., 'my tasks', 'my opportunities'), "
            "you MUST first call `dynamics_user_id()` to get their user ID, then filter by `_ownerid_value eq {user_id}`.\n\n"
            
            "## Named Filters (Preferred Method)\n"
            "Use these parameters instead of manual GUID lookups:\n"
            "- `filter_by_service_offering`: Filter by service offering name(s), e.g., ['Data & Analytics', 'Cybersecurity']\n"
            "- `filter_by_business_unit`: Filter by business unit name(s), e.g., ['Columbus', 'Chicago']\n"
            "- `filter_by_industry_vertical`: Filter by industry name(s), e.g., ['Healthcare', 'Financial Services']\n\n"
            
            "Accepts friendly names OR GUIDs. No need to lookup GUIDs first. \n\n"
            
            "**Examples**:\n"
            "```python\n"
            "# Find AI-related opportunities for a service offering\n"
            "get_entities(\n"
            "    entity_type='opportunities',\n"
            "    filter_by_service_offering=['Data & Analytics'],\n"
            "    query_params='$filter=cen_ai eq true',\n"
            "    limit=50\n"
            ")\n\n"
            
            "# Combine multiple filters\n"
            "get_entities(\n"
            "    entity_type='opportunities',\n"
            "    filter_by_service_offering=['Cybersecurity'],\n"
            "    filter_by_business_unit=['Columbus'],\n"
            "    query_params='$filter=statecode eq 1 and statuscode eq 3'  # Won opportunities\n"
            ")\n"
            "```\n\n"
            
            "## Key Fields\n"
            "- **Business Unit (BU)**: City name (Columbus, Chicago, etc.) - stored in `_owningbusinessunit_value`\n"
            "- **Service Offering (SO)**: Team name (Modern Software Delivery, Cybersecurity, etc.) - stored in 3 fields: "
            "`_cen_serviceofferingcapabiity1_value`, `_cen_serviceofferingcapability2_value`, `_cen_serviceofferingcapability3_value`\n"
            "- **Industry Vertical (IV)**: Industry (Healthcare, Insurance, etc.) - stored in `_cen_centricindustryvertical_value`\n"
            "- **AI Flag**: `cen_ai` (true/false) - **IMPORTANT**: When user asks for 'AI related', 'AI opportunities', "
            "'AI projects', etc., filter by `cen_ai eq true`\n"
            "- **Estimated Revenue**: `estimatedvalue` (opportunities), `budgetamount` (leads)\n"
            "- **Weighted Revenue**: `cen_weightedrevenue` (opportunities only)\n\n"
            
            "## Core Patterns\n\n"
            
            "### 1. Entity Lookup by Name\n"
            "```python\n"
            "# Find account by partial name or URL\n"
            "get_entities(\n"
            "    entity_type='accounts',\n"
            "    query_params=\"$filter=contains(name, 'Acme') or contains(websiteurl, 'acme')\"\n"
            ")\n\n"
            
            "# Find opportunity with account expansion\n"
            "get_entities(\n"
            "    entity_type='opportunities',\n"
            "    query_params=\"$filter=contains(parentaccountid/name, 'Acme')&$expand=parentaccountid($select=name,accountid)\"\n"
            ")\n"
            "```\n\n"
            
            "### 2. Date-Based Queries\n"
            "```python\n"
            "# Opportunities created this year\n"
            "get_entities(\n"
            "    entity_type='opportunities',\n"
            "    query_params=\"$filter=createdon ge 2024-01-01&$orderby=createdon desc\"\n"
            ")\n\n"
            
            "# Won opportunities closed in date range\n"
            "get_entities(\n"
            "    entity_type='opportunities',\n"
            "    query_params=\"$filter=statecode eq 1 and statuscode eq 3 and actualclosedate ge 2024-01-01 and actualclosedate le 2024-12-31\"\n"
            ")\n"
            "```\n\n"
            
            "### 3. Activity Summaries\n"
            "```python\n"
            "# Get recent activity for an opportunity (use regardingobjectid)\n"
            "get_entities(\n"
            "    entity_type='posts',\n"
            "    query_params=\"$filter=_regardingobjectid_value eq {opportunity_id}&$orderby=createdon desc&$top=5\"\n"
            ")\n\n"
            
            "# Repeat for: emails, phonecalls, appointments, tasks\n"
            "```\n\n"
            
            "### 4. User-Specific Queries\n"
            "```python\n"
            "# Get current user's ID first\n"
            "user_id = dynamics_user_id()\n\n"
            
            "# Then filter by owner\n"
            "get_entities(\n"
            "    entity_type='tasks',\n"
            "    query_params=\"$filter=_ownerid_value eq {user_id} and statecode eq 0&$orderby=scheduledend asc\"\n"
            ")\n"
            "```\n\n"
            
            "## Important Notes\n"
            "1. **USER-SPECIFIC QUERIES** (CRITICAL): When user says 'my', 'mine', or 'I' (e.g., 'my tasks', 'show me my opportunities'), "
            "you MUST call `dynamics_user_id()` first, then filter by `_ownerid_value eq {user_id}`. DO NOT skip this step!\n"
            "2. **Use named filters** for BU/SO/IV filtering - much simpler than manual GUID lookup\n"
            "3. **Service Offerings**: When filtering manually, check all 3 capability fields with OR logic\n"
            "4. **Partial matching**: Use `contains()` function for name searches\n"
            "5. **Multi-field search**: Search both `name` and `websiteurl` for accounts\n"
            "6. **Accounts**: Active accounts have `statecode eq 0` (tool auto-adds this filter)\n"
            "7. **Large results**: Automatically saved to Excel file with preview shown\n"
            "8. **Output format**: YAML (more token-efficient than JSON)\n"
            "9. **Disambiguation**: If multiple entities match, ask user to specify which one\n\n"
            
            "## Response Handling\n"
            "- **0-3 records**: Full data returned\n"
            "- **4-10 records**: Full or summary based on token size\n"
            "- **11-50 records**: Summary fields only\n"
            "- **50+ records**: Saved to file, preview of 10 shown\n\n"
            
            "Use `force_save=True` to always save to file regardless of size.\n"
        )
        
        super().__init__(
            template=template,
            required=True,
            name="Dynamics CRM Search",
            render_section_header=True,
            **data
        )
