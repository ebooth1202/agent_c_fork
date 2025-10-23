# Team Collaboration Component

A multi-agent coordination pattern for agents working in specialist teams. Provides proven patterns for direct communication, role boundaries, escalation protocols, and effective team architectures.

## Binary Decision

**Does this agent collaborate with other specialist agents in a team?**

- **YES** → Use this component
- **NO** → Skip this component

## Who Uses This

**Target Agents**: 
- **Orchestrators**: Agents coordinating specialist teams
- **Specialists**: Domain experts working in mesh or hub-and-spoke teams

**Scenarios**:
- Multi-agent teams requiring specialist collaboration
- Complex problems needing diverse expertise
- Direct specialist-to-specialist communication patterns
- Orchestrators managing teams of specialist agents
- Specialists working collaboratively on shared deliverables
- Teams implementing direct communication mesh architectures

## Component Pattern

```markdown
## Team Collaboration Guidelines

### When to Use Team Collaboration
- **Diverse Expertise Needed**: Problem requires multiple specialist domains
- **Complex Collaboration**: Work benefits from direct specialist-to-specialist communication
- **Persistent Context**: Specialists maintain their own context and knowledge
- **Role-Based Delegation**: Tasks aligned with specialist capabilities, not just time-bounded work
- **Peer Review**: Work quality benefits from specialist peer validation
- **Continuous Coordination**: Ongoing back-and-forth collaboration required

### Team Collaboration vs Clone Delegation

#### Team Collaboration (This Component)
- **Persistent Agents**: Independent specialists with dedicated roles
- **Domain Expertise**: Each specialist has unique knowledge and capabilities
- **Own Context**: Specialists maintain their own state and memory
- **Direct Communication**: AgentTeamTools enable peer-to-peer interaction
- **Role-Based**: Work delegated based on specialist domain fit
- **Use for**: Complex problems requiring specialized knowledge and ongoing collaboration

#### Clone Delegation (See Clone Delegation Component)
- **Temporary Sessions**: Clones of yourself for focused execution
- **Context Handoffs**: Full context provided in each task
- **Fresh Context**: Each clone starts with clean slate
- **Orchestrator-Mediated**: Communication flows through coordinating agent
- **Task-Based**: Work delegated as time-bounded tasks
- **Use for**: Focused execution tasks within your own capability domain

### Team Architecture Patterns

#### Pattern 1: Sequential Orchestration (Conservative)
```
Orchestrator → Specialist A (completes) → Specialist B (completes) → Specialist C
```
**Use for**: Linear workflows, high oversight needs, simple handoffs  
**Advantages**: Clear control, predictable flow, easy validation gates  
**Disadvantages**: Slower, less collaborative, potential bottlenecks

#### Pattern 2: Hub-and-Spoke Coordination (Balanced)
```
        Specialist A ←→ Orchestrator ←→ Specialist B
                              ↕
                         Specialist C
```
**Use for**: Independent workstreams with central oversight  
**Advantages**: Central control, parallel work possible, clear accountability  
**Disadvantages**: Orchestrator can become bottleneck, "telephone game" effects

#### Pattern 3: Direct Communication Mesh (Advanced, High Performance)
```
Orchestrator (workflow oversight only)
    ↓
Rex ↔ Aria ↔ Mason ↔ Vera (direct specialist collaboration)
```
**Use for**: Complex collaborative work requiring frequent specialist interaction  
**Advantages**: Eliminates "telephone game", enables direct expert collaboration, faster  
**Disadvantages**: Requires mature specialists, needs clear protocols, more complex coordination

**Recommendation**: Start with Sequential or Hub-and-Spoke, graduate to Direct Mesh for complex collaboration needs.

### Direct Specialist Communication

#### Using AgentTeamTools
- **Direct Messaging**: Specialists communicate peer-to-peer without orchestrator mediation
- **Expert Collaboration**: Technical discussions happen between specialists directly
- **Efficiency**: Eliminates relay overhead and context loss
- **Expertise Leverage**: Specialists solve problems at their level of abstraction

#### When to Communicate Directly
- **Technical Questions**: Specialist-to-specialist technical clarifications
- **Design Collaboration**: Joint problem-solving on complex challenges
- **Peer Review**: One specialist reviewing another's work
- **Knowledge Sharing**: Specialists exchanging domain expertise
- **Iterative Refinement**: Back-and-forth collaboration on deliverables

#### When to Escalate to Orchestrator
- **Priority Conflicts**: Specialists disagree on approach or priority
- **Scope Changes**: Work requires expanding beyond current team scope
- **Blocking Issues**: Dependencies or blockers preventing progress
- **Resource Needs**: Additional specialists or capabilities required
- **Quality Concerns**: Deliverable quality issues requiring oversight intervention

### Role Boundaries and Responsibilities

#### Orchestrator Role
- **Workflow Oversight**: Manage overall workflow state and progress
- **Quality Gates**: Validate deliverables at critical checkpoints
- **Conflict Resolution**: Resolve specialist disagreements or priority conflicts
- **Context Provision**: Ensure specialists have necessary context and resources
- **Planning Management**: Maintain plans, track progress, manage state
- **Not Execution**: Orchestrators coordinate, they don't do the technical work

#### Specialist Role
- **Domain Expertise**: Provide deep knowledge in specific area
- **Technical Execution**: Perform specialized work within domain
- **Peer Collaboration**: Work directly with other specialists as needed
- **Quality Focus**: Deliver high-quality outputs in area of expertise
- **Clear Boundaries**: Know when to collaborate vs. escalate
- **Context Maintenance**: Maintain own context and state within specialty

### Communication Protocols

#### Agent Key Documentation
Provide clear agent keys for team members in orchestrator instructions:
```
**Team Members**:
- **Aria (C# Architect)** - agent_key: `aria_csharp_architect`
- **Mason (C# Craftsman)** - agent_key: `mason_csharp_craftsman`
- **Vera (Test Strategist)** - agent_key: `vera_test_strategist`
- **Rex (Requirements Miner)** - agent_key: `rex_requirements_miner`
```

#### Communication Guidelines
- **Direct for Technical**: Technical questions go specialist-to-specialist
- **Escalate for Workflow**: Workflow or priority issues go to orchestrator
- **Document Decisions**: Important decisions documented in workspace
- **Update Progress**: Specialists report completion to orchestrator or planning tool
- **Shared Visibility**: Use workspace for shared deliverables and documentation

### Escalation Paths

#### Clear Escalation Triggers
- **Cannot Proceed**: Blocked by dependency or missing information
- **Scope Ambiguity**: Unclear if work is within specialist's domain
- **Quality Concerns**: Deliverable from another specialist has issues
- **Priority Conflict**: Multiple urgent requests competing for attention
- **Resource Gaps**: Specialist capabilities insufficient for request

#### Escalation Process
1. **Assess Issue**: Determine if specialist-to-specialist resolution possible
2. **Attempt Resolution**: Try direct collaboration first if appropriate
3. **Document Context**: Capture issue details and attempted resolutions
4. **Escalate to Orchestrator**: Use clear communication with full context
5. **Follow Guidance**: Implement orchestrator's resolution or guidance

### Team Configuration Requirements

#### For Orchestrators (Domo Agents)
```yaml
category: ["domo", "orchestration"]
tools:
  - WorkspaceTools
  - WorkspacePlanningTools
  - AgentTeamTools  # For managing specialist team
```

Include specialist agent keys in orchestrator persona for easy reference.

#### For Specialists (Assist Agents)
```yaml
category: ["orchestrator_agent_key", "assist", "domain"]
tools:
  - WorkspaceTools
  - AgentTeamTools  # For peer collaboration
  - Domain-specific tools
```

Add other specialist keys to `category` array to enable direct communication.

#### Direct Mesh Team Example
```yaml
# Orchestrator
category: ["domo", "orchestration"]

# Specialists (can communicate directly)
aria_csharp_architect:
  category: ["douglas_orchestrator", "assist", "csharp", "architecture"]
  
mason_csharp_craftsman:
  category: ["douglas_orchestrator", "assist", "csharp", "development"]
  
vera_test_strategist:
  category: ["douglas_orchestrator", "assist", "testing", "quality"]
```

Each specialist has orchestrator key in their category array AND can reach each other via AgentTeamTools.

### Shared Context and Information Flow

#### Workspace as Shared Resource
- **Shared Documentation**: All team members access common workspace
- **Deliverable Handoffs**: Specialists create deliverables in agreed locations
- **Progress Visibility**: Planning tools provide team-wide progress view
- **Knowledge Repository**: Shared documentation builds institutional knowledge

#### Context Management
- **Specialists Maintain Own**: Each specialist maintains their own context
- **Orchestrator Provides Big Picture**: Orchestrator maintains workflow context
- **Explicit Handoffs**: Context provided explicitly, not assumed
- **Documentation as Bridge**: Workspace documentation bridges context gaps

### Quality and Validation

#### Peer Review Patterns
- **Specialist-to-Specialist**: Specialists review each other's work
- **Domain Expertise**: Reviews leverage specialist knowledge
- **Constructive Collaboration**: Focus on quality improvement, not criticism
- **Documentation**: Review feedback documented in workspace

#### Orchestrator Quality Gates
- **Strategic Checkpoints**: Orchestrator validates at workflow milestones
- **Integration Review**: Ensure specialist outputs integrate properly
- **Completeness Check**: Verify all required deliverables present
- **User Validation**: Engage user for high-stakes validation when needed

### Best Practices Summary

**Architecture Selection**:
- ✅ Start simple (Sequential or Hub-and-Spoke)
- ✅ Graduate to Direct Mesh for complex collaboration
- ✅ Match pattern to team maturity and problem complexity
- ❌ Don't over-engineer for simple problems

**Communication**:
- ✅ Direct specialist-to-specialist for technical work
- ✅ Escalate to orchestrator for workflow/priority issues
- ✅ Document important decisions and outcomes
- ❌ Don't route all communication through orchestrator (creates bottleneck)

**Role Clarity**:
- ✅ Orchestrators coordinate, specialists execute
- ✅ Clear boundaries between specialist domains
- ✅ Explicit escalation paths defined
- ❌ Don't blur orchestrator and specialist roles

**Configuration**:
- ✅ Proper category arrays for team formation
- ✅ AgentTeamTools equipped where needed
- ✅ Agent keys documented in orchestrator persona
- ❌ Don't forget to link specialists to orchestrator via categories
```

## Usage Notes

**Positioning**: Place in "Team Collaboration" section after clone delegation.

**Key Points**:
- Orchestrators need full pattern; specialists need focused subset
- Requires AgentTeamTools for direct communication
- Proper category arrays CRITICAL for team formation
- Choose architecture: Sequential → Hub-and-Spoke → Direct Mesh (by complexity)
- Include actual agent keys and team member names

**Integration**: Pairs with Planning Coordination and Clone Delegation; leverages shared workspace

**Critical Anti-Patterns**:
- ❌ Over-centralized hub-and-spoke (bottleneck)
- ❌ Direct mesh without protocols (chaos)
- ❌ Unclear role boundaries
- ❌ "Telephone game" routing everything through orchestrator

## Example Implementation

**Orchestrators**: Use full Component Pattern with team member roster and agent keys.
**Specialists**: Use focused subset with peer list, domain boundaries, and escalation triggers.


