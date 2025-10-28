import os
import time
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from agent_c.util.logging_utils import LoggingManager
from agent_c.config import locate_config_path
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
    config_path = locate_config_path()
    key_file_path = Path(config_path).joinpath("certs/key.pem")
    cert_file_path = Path(config_path).joinpath("certs/cert.pem")
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
            ssl_keyfile=str(key_file_path),
            ssl_certfile=str(cert_file_path),
            log_level=LoggingManager.LOG_LEVEL.lower() if hasattr(LoggingManager, 'LOG_LEVEL') else "info"
        )
    logger.info(f"Exiting Run Loop")

if __name__ == "__main__":
    run()