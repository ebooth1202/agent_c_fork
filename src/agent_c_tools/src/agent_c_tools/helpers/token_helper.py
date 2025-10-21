def is_content_too_large(content: str, tool_context, max_tokens: int = 25000) -> bool:
    if tool_context is None or 'agent_runtime' not in tool_context:
        return True  # Can't check size without agent context
    else:
        token_count: int = tool_context['agent_runtime'].count_tokens(content)
        return token_count > max_tokens