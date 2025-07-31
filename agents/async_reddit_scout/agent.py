import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams
from dotenv import load_dotenv

# Load environment variables from the project root .env file
load_dotenv()

def create_agent():
    """Creates the agent instance after fetching tools from the MCP server."""
    agent_instance = Agent(
        name="async_reddit_scout_agent",
        description="A Reddit scout agent that searches for hot posts in a given subreddit using an external MCP Reddit tool.",
        model="gemini-2.0-flash", # Ensure API key is in .env
        instruction=(
            "You are the Async Reddit News Scout. Your task is to fetch hot post titles from any subreddit using the connected Reddit MCP tool."
            "1. **Identify Subreddit:** Determine which subreddit the user wants news from. Default to 'gamedev' if none is specified. Use the specific subreddit mentioned (e.g., 'unity3d', 'unrealengine')."
            f"2. **Call Discovered Tool:** You **MUST** look for and call the tool named fetch_reddit_hot_threads and fetch_reddit_post_content with the identified subreddit name and optionally a limit." # Adjust name if needed!
            "3. **Present Results:** The tool will return a formatted string containing the hot post information or an error message."
            "   - Present this string directly to the user."
            "   - Clearly state which subreddit the information is from."
            "   - Format the links as clickable links."
            "   - If the tool returns an error message, relay that message accurately."
            "4. **Handle Missing Tool:** If you cannot find the required Reddit tool, inform the user that you cannot fetch Reddit news due to a configuration issue."
            "5. **Do Not Hallucinate:** Only provide information returned by the tool."
        ),
        tools=[
            MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command='uvx',
                        args=[
                            "--from",
                            "git+https://github.com/adhikasp/mcp-reddit.git",
                            "mcp-reddit"
                        ],
                        # Pass the API key as an environment variable to the npx process
                        # This is how the MCP server for Reddit expects the key.
                        env={
                            "REDDIT_CLIENT_ID": os.environ.get("REDDIT_CLIENT_ID"),
                            "REDDIT_CLIENT_SECRET": os.environ.get("REDDIT_CLIENT_SECRET")
                        }
                    ),
                    timeout=60,
                ),
                # You can filter for specific Reddit tools if needed:
                tool_filter=['fetch_reddit_hot_threads', 'fetch_reddit_post_content']
            )
        ],
    )
    
    return agent_instance

# Create the agent synchronously
root_agent = create_agent()