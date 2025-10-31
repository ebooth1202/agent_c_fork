## Agent C Event System Architecture
The Agent C realtime API uses a structured event system built on a clear inheritance hierarchy:
  
### BaseEvent Structure
All events inherit from `BaseEvent` which provides the `type` field

#### Event Type Naming Convention 
Event types follow snake_case naming WITHOUT "event" suffix:

- Class: `TextDeltaEvent` → Type: `"text_delta"`
- Class: `SystemPromptEvent` → Type: `"system_prompt"`
- Class: `ToolCallEvent` → Type: `"tool_call"`
  
### Event Categories 

**Control Events**: Inherit directly from `BaseEvent` 
- Handle session management, configuration, and system operations
- Only contain the base `type` field plus event-specific data
- Examples: `get_agents`, `set_agent`, `avatar_list`, `tool_catalog`
  
**Session Events**: Inherit from `SessionEvent` (which extends `BaseEvent`) 
- Handle chat interactions and content within active sessions
- Include session context fields:
  - `session_id` (required str): The CHAT SESSION ID of the chat session this event came from, MAY NOT MATCH THE CHAT SESSION IF FOR THE CURRENT CHAT SESSION
  - `role` (required str): Role that triggered the event
  - `parent_session_id` (optional str): Parent session if this is a child session
  - `user_session_id` (optional str): This ill ALWAYS match the CHAT SESSION ID of the actice chat session for the user.
- Examples: `text_delta`, `completion`, `tool_call`, `render_media`

### Events vs messages
When we resume a chat session, i.e. when we receive a ChatSessionChanged, is the only time we're dealing with intact "messages", with the exception of the `AntrhopicUserMessage`, `OpenAIUserMessage` and `SystemMessage` which do get emitted in their entirerty as SessionEvents, all other chat messages are assembled from deltas and rendered on the fly as the deltas come in.
  
There are MANY more events in the chat stream that the client should display while streaming than are present in the `messages` array in the `ChatSession`. `RenderMedia` is one such event.
  
### SessionEvents
Events that inherit from `SessionEvent` are distinct from the control events used between the client and the server. 
  
- SessionEvents all have a `session_id` that identifies the ChatSession the message belongs to. Note: this isn't because the client receives events for other chat sessions, but because the the server supports "sub-sessions".
  
### Roles
- Never modify the `role` field in a SessionEvent
- There cane be MANY more roles than just "user" and "assistant"
  - THEY ARE NOT PRESENT IN THE SAVED SESSION the come via SessionEvents
  - Two common examples are "tool" and "system"

### Sub-sessions
Sub-sessions are created when an agent uses one of the delegation tools to communicate with another agent / clone.
  
In addition to the main `session_id` there are two other chat session IDs in the SessionEvents:
  
1. `user_session_id` - This contains the chat session ID for the top level user session. If this field matches the `session_id` the event is for the user session.
2. `parent_session_id` - This contains `session_id` of chat session that originated the sub-session
    - When the primary agent uses a delegation tool, `parent_session_id` will match `user_session_id`
    - When the delegated agent uses a delegation tool `parent_session_id` will contain the ID for the the calling agent's chat session, and `user_session_id` will point to the user session.
      
#### Sub-session Events
There are a pair of events used to signal the start / end of a subsession:
  
1. SubsessionStartedEvent - contains information about the type of sub-session and the agents involved
2. SubsessionEndedEvent - Which contains no unique fields of it's own, just the `type` and the standard session event fields

### Important Rules for Events (and other models from the API)
- It is ESSENTIAL that clients use the same names and models as the API as a baseline (conversion from snake_case, to another case system is allowed)
  - If an event must be modified to work in the client, it should be wrapped, not modified directly
- These events, models and types are part of the API contract between the client and server
  - They MUST NOT be modified without a corresponding change in the API