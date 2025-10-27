import os
import time
import uvicorn
from dotenv import load_dotenv
from agent_c.util.logging_utils import LoggingManager

load_dotenv(override=True)

# dictionary to track performance metrics
_timing = {
    "start_time": time.time(),
    "app_creation_start": 0,
    "app_creation_end": 0
}

# Configure logging
logging_manager = LoggingManager("agent_c_api")
logger = logging_manager.get_logger()
logger.info("Agent C API starting up...")
LoggingManager.configure_root_logger()
LoggingManager.configure_external_loggers()
LoggingManager.configure_external_loggers({
    "agent_c_api.core.util.middleware_logging": "WARNING",  # Show INFO logs for middleware_logging, debug is too noisy
    "sqlalchemy.engine": "WARNING",  # Suppress SQLAlchemy engine logs
    "sqlalchemy.pool": "WARNING",  # Suppress connection pool logs
    "aiosqlite": "WARNING",  # Suppress aiosqlite operation logs
})

logger.info("Loading API router")
from agent_c_api.api import router

logger.info("Creating API application")
_timing["app_creation_start"] = time.time()
from agent_c_api.config.env_config import settings
from agent_c_api.core.setup import create_application
app = create_application(router=router, settings=settings)
_timing["app_creation_end"] = time.time()

logger.info(f"Registered {len(app.routes)} routes")



def run():
    """Entrypoint for the API"""
    logger.info(f"FastAPI Reload Setting is: {settings.RELOAD}.")
    logger.info(f"Agent_C API server running on {settings.HOST}:{settings.PORT}")
    logger.info(f"Working Directory: {os.getcwd()}")
    
    # If reload is enabled, we must use the import string
    if settings.RELOAD:
        uvicorn.run(
            "agent_c_api.main:app",
            host=settings.HOST,
            port=settings.PORT,
            ssl_keyfile="./agent_c_config/localhost_self_signed-key.pem",
            ssl_certfile="./agent_c_config/localhost_self_signed.pem",
            reload=settings.RELOAD,
            log_level=LoggingManager.LOG_LEVEL.lower() if hasattr(LoggingManager, 'LOG_LEVEL') else "info"
        )
    else:
        # Otherwise, we can use the app object directly for better debugging
        if os.environ.get("RUNNING_IN_DOCKER", "false").lower() == "true":
            logger.info("Detected running in Docker, disabling SSL for Uvicorn")
            uvicorn.run(
                app,
                host=settings.HOST,
                port=settings.PORT,
                log_level=LoggingManager.LOG_LEVEL.lower() if hasattr(LoggingManager, 'LOG_LEVEL') else "info"
            )
        else:
            uvicorn.run(
                app,
                host=settings.HOST,
                port=settings.PORT,
                ssl_keyfile="agent_c_config/localhost_self_signed-key.pem",
                ssl_certfile="agent_c_config/localhost_self_signed.pem",
                log_level=LoggingManager.LOG_LEVEL.lower() if hasattr(LoggingManager, 'LOG_LEVEL') else "info"
            )
    logger.info(f"Exiting Run Loop")

if __name__ == "__main__":
    run()