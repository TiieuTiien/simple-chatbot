"""
Entry point for the Speaker Agent.
Initializes and starts the agent's server.
"""

import os
import sys
import logging
import argparse
import uvicorn
import asyncio # Import asyncio

from pathlib import Path
from contextlib import AsyncExitStack # For MCP exit stack
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

# Fall back to absolute imports (for direct execution and module mode)
# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now use absolute imports
from agents.speaker.task_manager import TaskManager
from agents.speaker.agent import create_agent
from common.a2a_server import AgentRequest, AgentResponse, create_agent_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_status = load_dotenv(dotenv_path=dotenv_path, override=True) # Use override just in case

# Global variable for the TaskManager instance
task_manager_instance: TaskManager | None = None

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Start the Speaker Agent server")
    parser.add_argument(
        "--host", 
        type=str, 
        default=os.getenv("SPEAKER_HOST", "0.0.0.0"),
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("SPEAKER_PORT", "8003")),
        help="Port to bind the server to"
    )
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        default=os.getenv("LOG_LEVEL", "info"),
        help="Set the logging level"
    )
    # Arguments related to TaskManager are handled via env vars now
    return parser.parse_args()

async def main(): # Make main async
    """Initialize and start the Speaker Agent server."""
    global task_manager_instance
    
    logger.info("Starting Speaker Agent A2A Server initialization...")
    
    # Await the root_agent coroutine to get the actual agent and exit_stack
    logger.info("Awaiting root_agent creation...")
    agent_instance, toolset = await create_agent()
    logger.info(f"Agent instance created: {agent_instance.name}")

    # Use the toolset to manage the MCP connection lifecycle
    try:
        logger.info("MCP toolset entered.")
        # Initialize the TaskManager with the resolved agent instance
        task_manager_instance = TaskManager(agent=agent_instance)
        logger.info("TaskManager initialized with agent instance.")

        # Configuration for the A2A server
        # Use environment variables or defaults
        host = os.getenv("SPEAKER_A2A_HOST", "127.0.0.1")
        port = int(os.getenv("SPEAKER_A2A_PORT", 8003))
        
        # Create the FastAPI app using the helper
        # Pass the agent name, description, and the task manager instance
        app = create_agent_server(
            name=agent_instance.name,
            description=agent_instance.description,
            task_manager=task_manager_instance 
        )
        
        logger.info(f"Speaker Agent A2A server starting on {host}:{port}")
        
        # Configure uvicorn
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        
        # Run the server
        await server.serve()
    
    finally:
        # This part will be reached after the server is stopped (e.g., Ctrl+C)
        # Ensure the MCP toolset is properly exited
        logger.info("Exiting MCP toolset...")
        for tool in toolset:
            if hasattr(tool, 'close'):
                try:
                    await tool.close()
                    logger.info(f"Closed tool: {type(tool).__name__}")
                except Exception as e:
                    logger.error(f"Error closing toolset: {e}")

        logger.info("MCP toolset exited successfully.")
        logger.info("Speaker Agent A2A server stopped.")

if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Speaker Agent server stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during server startup: {str(e)}", exc_info=True)
        sys.exit(1) 