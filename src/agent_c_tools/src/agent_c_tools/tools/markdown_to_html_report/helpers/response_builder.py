"""
Response Builder

Provides utilities for creating standardized JSON responses for tool operations.
Ensures consistent response format across all tool methods.
"""

import json
from typing import Any, Dict


class ResponseBuilder:
    """Builds standardized JSON responses for tool operations."""

    @staticmethod
    def create_error_response(error_message: str) -> str:
        """
        Create a standardized error response.

        Args:
            error_message: Description of the error

        Returns:
            JSON string with error response format
        """
        return json.dumps({
            "success": False,
            "error": error_message
        })

    @staticmethod
    def create_success_response(message: str, **additional_data: Any) -> str:
        """
        Create a standardized success response.

        Args:
            message: Success message
            **additional_data: Additional data to include in response

        Returns:
            JSON string with success response format
        """
        response: Dict[str, Any] = {
            "success": True,
            "message": message,
            **additional_data
        }
        return json.dumps(response)
