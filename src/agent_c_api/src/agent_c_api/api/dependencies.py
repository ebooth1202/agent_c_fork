from fastapi import Request
from typing import List

def get_chat_session_manager(request: Request) -> 'ChatSessionManager':
    return request.app.state.chat_session_manager

def get_auth_service(request: Request) -> 'AuthService':
    """FastAPI dependency that provides the AuthService from app state."""
    return request.app.state.auth_service

def get_heygen_client(request: Request) -> 'HeyGenStreamingClient':
    """FastAPI dependency that provides the HeyGenStreamingClient from app state."""
    return request.app.state.heygen_client

def get_heygen_avatar_list(request: Request) -> List:
    """FastAPI dependency that provides the HeyGenStreamingClient from app state."""
    return request.app.state.heygen_avatar_list
