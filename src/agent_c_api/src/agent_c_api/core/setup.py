import os
import random
import re

from typing import Dict, Any
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from agent_c.chat import ChatSessionManager
from agent_c.config.saved_chat import SavedChatLoader
from agent_c.util.heygen_streaming_avatar_client import HeyGenStreamingClient
from agent_c_api.config.env_config import settings
from agent_c_api.core.realtime_session_manager import RealtimeSessionManager
from agent_c_api.core.util.logging_utils import LoggingManager
from agent_c_api.core.util.middleware_logging import APILoggingMiddleware
from agent_c.config.agent_config_loader import AgentConfigLoader

logging_manager = LoggingManager(__name__)
logger = logging_manager.get_logger()

random.seed()

def get_origins_regex():
    allowed_hosts_str = os.getenv("API_ALLOWED_HOSTS", "localhost,.local")
    patterns = [pattern.strip() for pattern in allowed_hosts_str.split(",")]
    # 1: ^https?:\/\/(localhost|.*\.local)(:\d+)?
    # 2: ^https?:\/\/(localhost|.*\.local)(:\d+)?
    regex_parts = []
    for pattern in patterns:
        if pattern.startswith("."):
            # Domain suffix like .local or .company.com
            suffix = re.escape(pattern)
            regex_parts.append(f".*{suffix}")
        else:
            # Specific host like localhost (with optional port)
            host = re.escape(pattern)
            regex_parts.append(f"{host}")

    return f"^https?://({"|".join(regex_parts)})(:\\d+)?"

def create_application(router: APIRouter, **kwargs) -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function sets up the application metadata, initializes the shared
    AgentManager resource via a lifespan handler, adds any required middleware,
    and includes the given router.
    """

    # Define a lifespan handler for startup and shutdown tasks.
    @asynccontextmanager
    async def lifespan(lifespan_app: FastAPI):
        # Import Redis configuration at runtime to avoid circular imports
        from agent_c_api.config.redis_config import RedisConfig
        from agent_c_api.config.env_config import settings

        logger.info(f"🔧 Initializing loaders:")
        lifespan_app.state.agent_config_loader = AgentConfigLoader()
        chat_loader = SavedChatLoader()

        logger.info("🔧 Initializing HeyGen client")
        try:
            lifespan_app.state.heygen_client = HeyGenStreamingClient()
            lifespan_app.state.heygen_avatar_list = (await lifespan_app.state.heygen_client.list_avatars()).data
            logger.info("✅ HeyGen avatars fetched")
        except Exception as e:
            logger.error(f"❌ Error initializing HeyGen client: {e}")
            lifespan_app.state.heygen_client = None
            lifespan_app.state.heygen_avatar_list = []

        # Initialize the chat session manager
        logger.info(f"🔧 Initializing chat session index and migrating old chat sessions (this may take a while):")
        await chat_loader.initialize_with_migration()
        lifespan_app.state.chat_session_manager = ChatSessionManager(loader=chat_loader)
        logger.info("✅ Chat session manager initialized successfully")

        logger.info("🤖 Initializing Client Session Manager...")
        lifespan_app.state.realtime_manager = RealtimeSessionManager(lifespan_app.state.chat_session_manager)
        await lifespan_app.state.realtime_manager.create_user_runtime_cache_entry("admin")  # Pre-create cache for admin user
        logger.info("✅ Client Session Manager initialized successfully")
        
        # Initialize FastAPICache with InMemoryBackend
        logger.info("💾 Initializing FastAPI Cache...")
        FastAPICache.init(InMemoryBackend(), prefix="agent_c_api_cache")
        logger.info("✅ FastAPICache initialized with InMemoryBackend")
        
        # Initialize authentication database
        logger.info("🗄️ Initializing authentication database...")
        from agent_c_api.config.database import initialize_database
        await initialize_database()
        logger.info("✅ Authentication database initialized")
        
        # Initialize authentication service
        logger.info("🔐 Initializing Authentication Service...")
        from agent_c_api.core.services.auth_service import AuthService
        lifespan_app.state.auth_service = AuthService()
        await lifespan_app.state.auth_service.initialize()
        logger.info("✅ Authentication Service initialized successfully")

        # Log startup completion
        logger.info("🎉 Application startup completed successfully")

        yield

        # Shutdown: Close authentication service, database and Redis connections
        logger.info("🔄 Application shutdown initiated...")
        
        # Close authentication service
        logger.info("🔐 Closing Authentication Service...")
        try:
            if hasattr(lifespan_app.state, 'auth_service'):
                await lifespan_app.state.auth_service.close()
            logger.info("✅ Authentication Service closed successfully")
        except Exception as e:
            logger.error(f"❌ Error during Authentication Service cleanup: {e}")
        
        # Close database connections
        logger.info("🗄️ Closing database connections...")
        try:
            from agent_c_api.config.database import close_database
            await close_database()
            logger.info("✅ Database connections closed successfully")
        except Exception as e:
            logger.error(f"❌ Error during database cleanup: {e}")

        logger.info("👋 Application shutdown completed")


    # Set up comprehensive OpenAPI metadata from settings (or fallback defaults)
    app_version = getattr(settings, "APP_VERSION", "0.3.0")

    openapi_metadata = {
        "title": getattr(settings, "APP_NAME", "Agent C API"),
        "description": getattr(settings, "APP_DESCRIPTION", "RESTful API for interacting with Agent C. The API provides resources for session management, chat interactions, file handling, and history access."),
        "version": app_version,
        "contact": {
            "name": getattr(settings, "CONTACT_NAME", "Agent C Team"),
            "email": getattr(settings, "CONTACT_EMAIL", "joseph.ours@centricconsulting.com"),
            "url": getattr(settings, "CONTACT_URL", "https://www.centricconsulting.com")
        },
        "license_info": {
            "name": getattr(settings, "LICENSE_NAME", "Business Source License 1.1"),
            "url": getattr(settings, "LICENSE_URL", "https://raw.githubusercontent.com/centricconsulting/agent_c_framework/refs/heads/main/LICENSE")
        },
        "terms_of_service": getattr(settings, "TERMS_URL", "https://www.centricconsulting.com/terms"),
        "docs_url": getattr(settings, "DOCS_URL", "/docs"),
        "redoc_url": getattr(settings, "REDOC_URL", "/redoc"),
        "openapi_url": getattr(settings, "OPENAPI_URL", "/openapi.json")
    }
    

    kwargs.update(openapi_metadata)
    app = FastAPI(lifespan=lifespan, **kwargs)

    #origin_regex = get_origins_regex()
    allowlist = [
        "http://localhost:5173",
        "https://localhost:5173",
        "http://localhost:3000",
        "https://localhost:3000",
        "http://agentc.local:5173",
        "https://agentc.local:5173",
    ]
    #logger.info(f"CORS allowed host regex: {origin_regex}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowlist,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    environment = getattr(settings, "ENV", os.getenv("ENV", "development")).lower()
    is_production = environment == "production"
    logger.info(f"Application running in {environment} environment")

    # Add our custom logging middleware
    # Enable request body logging in development but not in production
    app.add_middleware(
        APILoggingMiddleware,
        log_request_body=not is_production,
        log_response_body=False
    )

    app.include_router(router)

    return app