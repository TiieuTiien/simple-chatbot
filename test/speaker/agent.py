import asyncio
import os
from dotenv import load_dotenv

from google.genai import types
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StdioConnectionParams

# Load environment variables from the project root .env file
load_dotenv()

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

async def async_main():
    session_service = InMemorySessionService()
    # Artifact service might not be needed for this example
    artifact_service = InMemoryArtifactService()

    session = await session_service.create_session(
        state={},
        app_name="speaker_a2a_app",
        user_id="default_a2a_user",
    )

    query = "Say \"Hello, this is a TTS test\" in a friendly tone."
    print(f"User query: {query}")
    content = types.Content(
        role='user',
        parts=[
            types.Part(text=query)
        ]
    )
    root_agent, toolset = await create_agent()

    # Use async context manager to properly handle MCP lifecycle
    try:
        runner = Runner(
            app_name="speaker_a2a_app",
            agent=root_agent,
            session_service=session_service,
            artifact_service=artifact_service,
        )

        print("Running agent...")
        events_async = runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=content,
        )

        async for event in events_async:
            print(f"Event received: {event}")

    finally:
        # Properly cleanup the MCP toolset
        print("Cleaning up MCP connections...")
        for tool in toolset:
            if hasattr(tool, 'close'):
                try:
                    await tool.close()
                except Exception as e:
                    print(f"Error closing toolset: {e}")
        print("Cleanup complete.")
    
if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")