## @agentc/realtime-core 
Where most of our code lives. 
Location: `packages/core`
 
**The Central Hub - RealtimeClient** (`/src/client/RealtimeClient.ts`)
**WebSocket Protocol** (`/src/client/WebSocketManager.ts`)
**Audio System Architecture** (`/src/audio/`)
**Manager Pattern Implementation** (`/src/session/`, `/src/auth/`, etc.)
  - **AuthManager**: JWT lifecycle, token refresh before expiry
  - **SessionManager**: Chat history, message accumulation from text deltas
  - **TurnManager**: Server-driven turn control, prevents talk-over
  - **VoiceManager**: Tracks available voices, handles special modes (none/avatar)
  - **AvatarManager**: HeyGen integration state
  - **ReconnectionManager**: Exponential backoff with configurable limits
**Event System** (`/src/events/`)
  - The event system uses comprehensive TypeScript types with discriminated unions:
      - Binary frames automatically emit as `audio:output` events.

${blocks_core_types]