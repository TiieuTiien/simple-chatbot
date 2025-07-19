# Simple Chatbot

An ADK-powered agent that fetches and summarizes game development news from Reddit subreddits like r/gamedev, r/unity3d, and r/unrealengine.

## Acknowledgements

This project was inspired by and follows concepts from the excellent tutorial by **AI Oriented Dev**: 
[Forget MCP... don't sleep on the Google Agent Development Kit (ADK) - Full tutorial](https://youtu.be/BiP4tKZKTvU)

Special thanks for the comprehensive walkthrough of Google's ADK capabilities and practical implementation examples.

## Project Components

An ADK-powered agent that fetches and summarizes game development news from Reddit subreddits like r/gamedev, r/unity3d, and r/unrealengine.

## General Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:TiieuTiien/simple-chatbot.git
   cd simple-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On macOS/Linux
   source .venv/bin/activate
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Reddit Scout Agent Setup

1. **Navigate to the agent directory:**
   ```bash
   cd agents/reddit_scout
   ```

2. **Configure environment variables:**
   - Copy the example file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and configure your credentials:

   **Option A: Google AI Studio API Key (Recommended for testing)**
   ```dotenv
   GOOGLE_GENAI_USE_VERTEXAI="False"
   GOOGLE_API_KEY="your-google-ai-studio-api-key"
   ```

   **Option B: Vertex AI (For production)**
   ```dotenv
   GOOGLE_GENAI_USE_VERTEXAI="True"
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   GOOGLE_CLOUD_LOCATION="us-central1"
   ```

   **Reddit API Configuration:**
   ```dotenv
   REDDIT_CLIENT_ID="your-reddit-client-id"
   REDDIT_CLIENT_SECRET="your-reddit-client-secret"
   REDDIT_USER_AGENT="GameDevNewsScout/0.1 by YourUsername"
   ```

3. **Get Reddit API credentials:**
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Create a new application (script type)
   - Note down your client ID and secret

4. **Run the Reddit Scout agent:**
   ```bash
   # From the project root
   adk run agents/reddit_scout
   ```

## Project Structure

```
simple-chatbot/
├── chatbot.py               # Basic chatbot example
├── agents/                  # ADK agents directory
│   ├── __init__.py
│   └── reddit_scout/        # Reddit Scout Agent
│       ├── __init__.py
│       ├── agents.py        # Main agent implementation
│       ├── .env             # Environment variables (not in git)
│       └── .env.example     # Environment template
├── .book.venv/              # Virtual environment
└── README.md                # This file
```

## Usage Examples

### Running the Agent

To interact with the Reddit Scout agent, you can use the following commands from your project root:

**Run in CLI mode:**

```bash
adk run agents/reddit_scout
```

**Run with the ADK web interface:**

```bash
adk web agents/reddit_scout
```

This will launch a local web UI where you can chat with the agent in your browser.

Try these example prompts:
- `What's the latest game development news?`
- `Give me news from r/unity3d`
- `Show me posts from unrealengine subreddit`
- `Any updates from the gamedev community?`

The agent will:
1. Identify the appropriate subreddit(s)
2. Fetch recent hot posts using the Reddit API
3. Present them in a formatted list
4. Fall back to mock data if Reddit API is unavailable

## Features

### Reddit Scout Agent Capabilities:
- **Real Reddit Integration**: Fetches live data from Reddit's API
- **Multiple Subreddit Support**: Supports r/gamedev, r/unity3d, r/unrealengine, and more
- **Intelligent Subreddit Detection**: Automatically determines which subreddit to query
- **Error Handling**: Graceful fallback and error reporting
- **Mock Data Fallback**: Provides sample data when API is unavailable

## Troubleshooting

### Common Issues:

1. **ImportError: cannot import name 'agent'**
   - Ensure your file is named `agents.py` (as shown in the project structure)
   - Check that `__init__.py` imports match your file names

2. **Reddit API Errors**
   - Verify your Reddit API credentials in `.env`
   - Ensure your user agent string is descriptive and unique
   - Check that requested subreddits exist and are accessible

3. **Google AI API Issues**
   - Verify your API key is correct and active
   - Check your API quotas and usage limits
   - Ensure you have the correct model permissions

4. **Agent Not Found or Not Running from Correct Directory**
    - Make sure you navigate to the `agents/reddit_scout` directory before running the agent.
    - Example:
      ```bash
      cd agents/reddit_scout
      adk run .
      ```
    - Running from the wrong directory can cause import or path errors.

## Development Notes

This project uses:
- **Google Generative AI SDK** for the basic chatbot
- **Google ADK (Agent Development Kit)** for the Reddit Scout agent
- **PRAW (Python Reddit API Wrapper)** for Reddit integration
- **python-dotenv** for environment variable management

## Resources

- [Google AI Studio](https://aistudio.google.com/) - Get your API keys
- [Google ADK Documentation](https://developers.google.com/adk) - Official ADK docs
- [Reddit API Documentation](https://www.reddit.com/dev/api/) - Reddit API reference
- [AI Oriented Dev YouTube Channel](https://www.youtube.com/@AIOriented) - More AI development tutorials

## License

This project is for educational and demonstration purposes only.