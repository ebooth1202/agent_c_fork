### Event Flow Pipeline
  
1. INGRESS (WebSocketManager)
   ├─ Text frame → JSON.parse → event object
   └─ Binary frame → ArrayBuffer → audio data
  
2. ROUTING (RealtimeClient.handleMessage)
   ├─ Special events (ping/pong) → Direct handling
   ├─ Stream events → EventStreamProcessor
   └─ Control events → Direct emission
  
3. PROCESSING (EventStreamProcessor)
   ├─ Message events → MessageBuilder
   ├─ Tool events → ToolCallManager
   └─ Session events → SessionManager
  
4. EMISSION (EventEmitter)
   ├─ Internal components
   └─ External React/UI layer