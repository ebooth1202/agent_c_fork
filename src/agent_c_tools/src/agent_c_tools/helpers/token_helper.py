def is_content_too_large(content: str, tool_context, max_tokens: int = 25000) -> bool:
    result = token_count(content, tool_context)
    if result is None:
        return False  # Can't determine size, assume it's okay
    else:
        return result > max_tokens

def token_count(content: str, tool_context) -> int | None:
    if tool_context is None or 'agent_runtime' not in tool_context:
        return None  # Can't check size without agent context
    else:
        return tool_context['agent_runtime'].count_tokens(content)
