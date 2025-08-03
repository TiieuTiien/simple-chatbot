import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams
from google.adk.models.lite_llm import LiteLlm

# Load environment variables from the project root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

async def create_agent():
    # Define LLM for wrapping the tool output if needed
    # llm = LiteLlm(model="gemini-1.5-flash", api_key=os.environ.get("GOOGLE_API_KEY"))
    toolset =[
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
            "You are a Text-to-Speech agent. Convert user text to speech audio files.\n\n"
            "IMPORTANT FORMATTING RULES:\n"
            "1. Always call the text_to_speech tool with voice_name='Will'\n"
            "2. When the tool returns a file path, format your response like this example:\n"
            "   'I've converted your text to speech. The audio file is saved at `/path/to/file.mp3`'\n"
            "3. Make sure to put ONLY the file path inside backticks (`), not any additional text\n"
            "4. Never modify or abbreviate the path\n\n"
            "This exact format is critical for proper processing."
        ),
        model="gemini-2.0-flash",
        tools=toolset,
    )

    return agent_instance, toolset

root_agent = Agent(
    name="tts_speaker_agent",
    description="Converts provided text into speech using ElevenLabs TTS MCP.",
    instruction=(
        "You are a Text-to-Speech agent. Convert user text to speech audio files.\n\n"
        "IMPORTANT FORMATTING RULES:\n"
        "1. Always call the text_to_speech tool with voice_name='Will'\n"
        "2. When the tool returns a file path, format your response like this example:\n"
        "   'I've converted your text to speech. The audio file is saved at `/path/to/file.mp3`'\n"
        "3. Make sure to put ONLY the file path inside backticks (`), not any additional text\n"
        "4. Never modify or abbreviate the path\n\n"
        "This exact format is critical for proper processing."
    ),
    model="gemini-2.0-flash",
    tools=[
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
    ],
)