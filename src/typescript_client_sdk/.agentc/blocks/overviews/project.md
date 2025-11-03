# Agent C Typescript Client SDK Project Overview

The Agent C Typescript Client SDK, aka "Agent C Realtime SDK", allows Typescript developers to easily integrate with the Agent C realtime API and build applications that allow users to collaborate with AI agents via a chat interface.  Unlike most web based chat apps that use HTTP, the Agent C realtime API is fully event driven and uses WebSockets to provide a low latency, high throughput experience that is ideal for real-time collaboration with AI agents.

## Project Structure

The `${default_workspace}` contains a monorepo with the client SDK packages:

${blocks.overviews.core}

${blocks.overviews.react}

${blocks.overviews.ui}

In addition, there are two client apps to showcase these components.  The apps are essentially skeletons with little tro no functionality of their own.  

${blocks.overviews.demo}

${blocks.overviews.static_spa}

### Additional workspaces
- `project` contains the main monorepo for the entire Agent C project.  The Workspaces below are shortcuts to various `//project/src` folders.
- `api` (`src/agent_c_api`) contains the Python source for the Agent C API. 
- `core` (`src/agent_c_core`) contains the Python source for the core Agent C framework, containing the agent runtimes, models, and base classes. 
- `tools` (`src/agent_c_tools`) contains the Python source for the Agent C tools package.  This package provides agent tools. 
