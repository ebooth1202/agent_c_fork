# TypeScript Development Standards

## Core Principles

### 1. Type Safety First
- NO `any` types - Every value must have a proper type
- Use `unknown` when type is genuinely unknown, then narrow with type guards
- Enable strict mode in all TypeScript configurations
- Prefer compile-time type checking over runtime validation where possible

### 2. Explicit Over Implicit
- Always specify return types for functions
- Use explicit type annotations for complex objects
- Avoid relying on type inference for public APIs
- Document type constraints clearly

### 3. Immutability by Default
- Use `readonly` modifiers for properties that shouldn't change
- Prefer `const` assertions for literal types
- Use immutable data structures where appropriate
- Avoid mutating function parameters

## TypeScript Configuration

### Required Compiler Options
```json
{
"compilerOptions": {
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "strictFunctionTypes": true,
  "strictBindCallApply": true,
  "strictPropertyInitialization": true,
  "noImplicitThis": true,
  "alwaysStrict": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noImplicitReturns": true,
  "noFallthroughCasesInSwitch": true,
  "esModuleInterop": true,
  "skipLibCheck": false,
  "forceConsistentCasingInFileNames": true
}
}
```

### File Naming Conventions
- **Components/Classes**: PascalCase (e.g., `RealtimeClient.ts`)
- **Utilities/Functions**: camelCase (e.g., `messageUtils.ts`)
- **Types/Interfaces**: PascalCase with `.types.ts` suffix
- **Constants**: UPPER_SNAKE_CASE in `constants.ts` files


### Module Organization
- One primary export per file
- Group related functionality in subdirectories
- Keep files under 300 lines (prefer smaller, focused modules)


## Type System Guidelines
- Use Interfaces vs Type Alias
- Discriminated Unions for Events
- Use generic constraints for type safety
- Use branded types to prevent primitive obsession

## Naming Conventions

### Variables and Functions
- Use descriptive names
- Avoid abbreviations

### Classes and Interfaces
- Interfaces: No 'I' prefix, use descriptive names
- Abstract classes: 'Abstract' prefix
- Implementation classes: Descriptive suffix


### Enums and Constants
- Enums: PascalCase for name, UPPER_SNAKE_CASE for values
- Constants: UPPER_SNAKE_CASE

## Import/Export Patterns

### Import Organization
-  Order: External -> Internal -> Types -> Styles

### Export Patterns
```typescript
// Named exports for utilities and types
export const processMessage = () => {};
export type { MessageConfig };

// Default export for main class/component
export default RealtimeClient;

// Re-exports from index files
export { RealtimeClient } from './client/RealtimeClient';
export type { ClientConfig } from './types';

// Avoid export * - be explicit
export { specificFunction } from './utils'; // ✅ Good
export * from './utils';                    // ❌ Bad
```

## Error Handling

### Custom Error Classes
-  Create specific error classes

### Result Types for Expected Failures
```typescript
// Use Result type for operations that can fail
type Result<T, E = Error> = 
| { success: true; data: T }
| { success: false; error: E };

async function connectToServer(): Promise<Result<Connection>> {
try {
  const connection = await establishConnection();
  return { success: true, data: connection };
} catch (error) {
  return { success: false, error: error as Error };
}
}
```

### Error Boundaries and Recovery
-  Always implement error recovery strategies

## Async/Await Patterns

### Promise Handling
-  Always use async/await over .then() chains

### Concurrent Operations
-  Use Promise.all for concurrent operations
-  Use Promise.allSettled when failures are acceptable

## Event System Standards

### Event Emitter Pattern
```typescript
// Type-safe event emitter
class TypedEventEmitter<T extends Record<string, any>> {
private listeners = new Map<keyof T, Set<(data: any) => void>>();

on<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
  if (!this.listeners.has(event)) {
    this.listeners.set(event, new Set());
  }
  this.listeners.get(event)!.add(listener);
}

emit<K extends keyof T>(event: K, data: T[K]): void {
  this.listeners.get(event)?.forEach(listener => listener(data));
}

off<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
  this.listeners.get(event)?.delete(listener);
}
}
```

### Event Type Definitions
- Define all events in a central location
- Use throughout the application

## Documentation Requirements
- Code MUST include JSDoc Comments

## Performance Considerations
- Memoize expensive computations
- Debounce rapid events
- Use lazy initialization

## Code Review Checklist

Before submitting code for review, ensure:

### Type Safety
- [ ] No `any` types used
- [ ] All functions have explicit return types
- [ ] Proper null/undefined handling
- [ ] Type imports use `import type`

### Code Quality
- [ ] Follows naming conventions
- [ ] Proper error handling
- [ ] No console.log statements

- [ ] Documentation updated

### Performance
- [ ] No memory leaks
- [ ] Proper cleanup in dispose/unmount
- [ ] Efficient algorithms used
- [ ] Debouncing/throttling where appropriate