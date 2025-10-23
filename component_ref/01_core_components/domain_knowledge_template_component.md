# Domain Knowledge Template Component

A structural template that provides consistent organization for specialist domain expertise across different agent types. This is NOT a content component but a framework for organizing domain-specific knowledge.

## Binary Decision

**Is this agent a specialist that needs structured domain expertise?**

- **YES** → Use this template structure
- **NO** → Skip this component

## Who Uses This

**Target Agents**: All specialist agents requiring deep domain expertise

**Scenarios**:
- Requirements analysts organizing their discovery and analysis methodologies
- Architects structuring their design philosophies and patterns
- Implementation specialists organizing their coding practices
- Testing specialists organizing their test strategies and methodologies
- Documentation specialists organizing their content preparation approaches
- Any specialist agent with significant domain knowledge to organize

**When NOT to Use**: 
- General-purpose domo agents without specialized domain focus
- Utility agents performing simple, single-function operations
- Orchestrators (they coordinate specialists rather than provide deep domain expertise)

## Component Pattern

**IMPORTANT**: This is a STRUCTURAL template only - the content is entirely domain-specific and must be customized for each specialist.

```markdown
## [Domain Name] Expertise

### [Domain Name] Philosophy
[Core approach and beliefs about the domain - what principles guide your work in this area]

### [Domain Name] Methodologies
[Key methodologies and frameworks used in this domain - the systematic approaches you follow]

### [Domain Name] Best Practices
[Domain-specific best practices and principles - the proven patterns that lead to success]

### [Domain Name] Tools and Techniques
[Specific tools and techniques for the domain - the practical methods and instruments used]

### [Domain Name] Quality Standards
[Quality criteria and validation approaches - how you know when domain work is done well]
```

## Usage Notes

**Positioning**: Place after core guidelines (pairing, workspace, working rules) as main body of specialist persona.

**Key Points**:
- **Structure Only**: Template provides organization, NOT content
- **Highly Domain-Specific**: Content varies dramatically between domains
- **Flexible Sections**: Add, remove, rename sections based on domain needs
- **Examples Essential**: Domain sections benefit from concrete examples

**Customization by Specialist Type**:
- **Requirements**: Philosophy, Discovery/Elicitation, Analysis, Classification, Validation
- **Architecture**: Philosophy, Design Process, Patterns/Styles, Technology Selection, Validation
- **Implementation**: Craftsmanship, Methodologies, Standards/Patterns, Refactoring, Quality
- **Testing**: Philosophy, Strategy Development, Methodologies/Frameworks, Design, Coverage
- **Documentation**: Philosophy, Organization, Writing Standards, Workflows, Quality

**Anti-Patterns**:
- ❌ Generic template content without customization
- ❌ Excessive theory without practical guidance
- ❌ Overwhelming depth that obscures key principles

## Example Implementation

See Component Pattern for template structure. Examples: Requirements specialist includes Philosophy, Discovery/Elicitation, Analysis, Quality Standards sections. Architecture specialist includes Philosophy, Design Process, Patterns, Quality Standards. Testing specialist includes Philosophy, Strategy Development, Methodologies, Quality Standards. Customize all content for your specific domain.


