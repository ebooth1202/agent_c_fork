FROM ghcr.io/centricconsulting/agent_c_python_base

# Set working directory and create required directories
WORKDIR /app
RUN mkdir -p /app/images
RUN mkdir -p /app/workspaces/desktop
RUN mkdir -p /app/workspaces/downloads
RUN mkdir -p /app/workspaces/documents

# Copy source code first
COPY src/agent_c_core ./src/agent_c_core
COPY src/agent_c_tools ./src/agent_c_tools
COPY src/agent_c_api ./src/agent_c_api
COPY compose_workspaces.json /app/.local_workspaces.json
COPY .agentcignore /app/.agentcignore
COPY docs /app/docs

# Copy in the personas - right now we mount in docker-compose
COPY agent_c_config /app/agent_c_config

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
USER root
RUN chown -R agent_c:agent_c /app

COPY build_support/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

USER agent_c
# Install Python dependencies
WORKDIR /app/src
RUN pip install -e ace_proto \
    && pip install  -e agent_c_core \
    && pip install -e agent_c_tools \
    && pip install -e agent_c_api

# Return to the app's root
WORKDIR /app

# Set environment variables
ENV ENVIRONMENT="LOCAL_DEV"
ENV DALLE_IMAGE_SAVE_FOLDER="/app/images"
ENV RUNNING_IN_DOCKER="True"

# Expose the FastAPI server port
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "agent_c_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
#CMD ["/app/api_entrypoint.sh"]