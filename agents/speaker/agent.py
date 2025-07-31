import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams

# Load environment variables from the project root .env file
load_dotenv()

def create_agent():
    # Define LLM for wrapping the tool output if needed
    # llm = LiteLlm(model="gemini-1.5-flash", api_key=os.environ.get("GOOGLE_API_KEY"))
    tools =[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='uvx',
                    args=['elevenlabs-mcp'],
                    env={'ELEVENLABS_API_KEY': os.environ.get('ELEVENLABS_API_KEY', '')}
                ),
                timeout=60,
            ),
            tool_filter=['text_to_speech']
        )
    ]

    agent_instance = Agent(
        name="tts_speaker_agent",
        description="Converts provided text into speech using ElevenLabs TTS MCP.",
        instruction=(
            "You are a Text-to-Speech agent. Take the text provided by the user or coordinator and "
            "use the available ElevenLabs TTS tool to convert it into audio. "
            "When calling the text_to_speech tool, set the parameter 'voice_name' to 'Will'. "
            "Return the result from the tool (expected to be a URL)."
        ),
        model="gemini-2.0-flash",
        tools=tools,
    )

    return agent_instance

root_agent = create_agent()