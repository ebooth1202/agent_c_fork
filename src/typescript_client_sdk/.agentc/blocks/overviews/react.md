## @agentc/realtime-react 
React Integration / Hooks Layer
Location: `packages/react`

**Provider Pattern** (`/src/providers/AgentCProvider.tsx`) - The provider handles StrictMode double-mounting
**Hook Implementation Patterns** (`/src/hooks/`) 

Available hooks:   
  - `useRealtimeClient` - Direct client access
  - `useConnection` - Connection state with statistics tracking
  - `useAudio` - Audio control with turn awareness and 100ms status polling
  - `useChat` - Message history and text sending
  - `useTurnState` - Turn management UI synchronization
  - `useVoiceModel` - Voice selection with special modes
  - `useAvatar` - HeyGen avatar session management