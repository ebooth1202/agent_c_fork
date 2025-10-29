# Nuitka Project File options
#
# ============================================
# OS SPECIFIC SETTINGS
# ============================================
# nuitka-project-if: {OS} =="Windows":
#   nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/icon.png
#   nuitka-project: --mode=standalone
#   nuitka-project: --output-filename=agentc-api.exe
# nuitka-project-if: {OS} =="Darwin":
#   nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/icon.png
#   nuitka-project: --mode=app
#   nuitka-project: --output-filename=agentc-api.app
# nuitka-project-if: {OS} =="Linux":
#   nuitka-project: --linux-app-icon={MAIN_DIRECTORY}/icon.png
#   nuitka-project: --mode=onefile
#   nuitka-project: --output-filename=agentc-api
#
# ============================================
# MISC SETTINGS
# ============================================
# nuitka-project: --assume-yes-for-downloads
#
# ============================================
# METADATA
# ============================================
# nuitka-project: --product-name=Agent C API
# nuitka-project: --product-version=0.3.0
# nuitka-project: --file-version=0.3.0
# nuitka-project: --copyright=Copyright 2023-2025 Centric Computing
# nuitka-project: --file-description=Runtime API for Agent C.
#
# ============================================
# Include packages
# ============================================
# nuitka-project: --include-package=agent_c_api
# nuitka-project: --follow-import-to=agent_c
# nuitka-project: --follow-import-to=agent_c_tools
# nuitka-project: --include-package=passlib.handlers
# nuitka-project: --include-package-data=puremagic
# nuitka-project: --include-package-data=tiktoken
#
# ============================================
# ALWAYS EXCLUDE (tests, dev tools)
# ============================================
# nuitka-project: --nofollow-import-to=agent_c_api.tests
# nuitka-project: --nofollow-import-to=agent_c.tests
# nuitka-project: --nofollow-import-to=agent_c_tools.tests
# nuitka-project: --nofollow-import-to=pytest
# nuitka-project: --nofollow-import-to=_pytest
# nuitka-project: --nofollow-import-to=unittest
# nuitka-project: --nofollow-import-to=test
#
# ============================================
# PLUGINS
# ============================================
# nuitka-project: --enable-plugin=no-qt
#
# ============================================
# MODULE PARAMETERS
# ============================================
# --module-parameter=torch-disable-jit=no

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
    logger.info(f"Agent C Config path: {config_path}")
    key_file_path = Path(config_path).joinpath("certs/dev_key.pem")
    cert_file_path = Path(config_path).joinpath("certs/dev_cert.pem")
    logger.info(f"SSL Key File Path: {key_file_path}")
    logger.info(f"SSL Cert File Path: {cert_file_path}")
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