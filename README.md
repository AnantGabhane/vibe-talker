# Vibe Talker 🎙️

A conversational AI voice chat application that combines speech recognition, natural language processing, and text-to-speech synthesis. Vibe Talker listens to your voice, processes your input through an intelligent AI assistant powered by Google Gemini, and responds with natural-sounding audio.

## Features

- **🎤 Voice Input**: Real-time speech recognition using Google Speech Recognition API
- **🤖 AI Assistant**: Powered by Google Gemini 2.0 Flash for intelligent conversations
- **🔊 Text-to-Speech**: Natural voice synthesis using Gemini 2.5 Pro TTS with multiple voice options
- **💾 Conversation Memory**: MongoDB-backed conversation history with LangGraph checkpointing
- **🛠️ Command Execution**: AI can execute system commands and manage files autonomously
- **🔄 Stateful Conversations**: Maintains context across multiple interactions

## Architecture

The application is built on a modern AI stack:

- **LangGraph**: Orchestrates the conversation flow with state management
- **Google Gemini**: Powers the AI assistant and text-to-speech generation
- **MongoDB**: Stores conversation history and state checkpoints
- **Speech Recognition**: Google's speech-to-text API for voice input
- **Docker**: Containerized MongoDB for easy deployment

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for MongoDB)
- Google API credentials (Gemini API key)
- Microphone for voice input

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd vibe-talker
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root and add your Google API key:

```bash
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

To obtain these keys:
- Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
- Create a new API key for the Gemini API
- Add it to your `.env` file

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:
- `langgraph`: Agentic workflow orchestration
- `langchain`: LLM framework and tools
- `google-generativeai`: Google Gemini API client
- `speech_recognition`: Voice-to-text conversion
- `python-dotenv`: Environment variable management
- `pymongo`: MongoDB driver for conversation persistence

### 4. Start MongoDB

Start the MongoDB container using Docker Compose:

```bash
docker-compose up -d
```

This will start MongoDB on `localhost:27017` with default credentials (admin/admin).

## Usage

### Running the Application

```bash
python app/main.py
```

Once started, the application will:
1. Initialize the voice chat interface
2. Listen for your voice input
3. Process your speech through Google Speech Recognition
4. Send the recognized text to the AI assistant
5. Generate a response using Gemini
6. Convert the response to speech using TTS
7. Save the audio output to `./ai_generated/tts_output.wav`

### Voice Chat Interaction

```
🎙️ LangGraph Voice Chat Initialized. Speak or press Ctrl+C to exit.

Mic ready...

Say something...
Listening...
Recognizing...
You said: What's the weather like?
```

The AI will process your input and respond with both text and audio.

### Exiting

Press `Ctrl+C` to exit the application gracefully.

## Project Structure

```
vibe-talker/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point with voice I/O and TTS
│   └── graph.py             # LangGraph workflow definition
├── ai_generated/            # Generated files (audio, code, etc.)
├── docker-compose.yml       # MongoDB container configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in version control)
└── README.md               # This file
```

## Key Components

### main.py

The main entry point that handles:
- **Speech Recognition**: Captures and converts voice to text
- **TTS Generation**: Converts AI responses to natural speech
- **Graph Execution**: Runs the conversation through the LangGraph workflow
- **Session Management**: Maintains conversation state with MongoDB

### graph.py

Defines the LangGraph workflow:
- **State Management**: Tracks conversation messages
- **Chatbot Node**: Processes messages through Gemini
- **Tool Node**: Executes system commands when needed
- **Conditional Routing**: Routes between chatbot and tools based on response

### docker-compose.yml

MongoDB configuration:
- Exposes MongoDB on port 27017
- Uses default credentials (admin/admin)
- Persists data in a named volume

## Configuration

### MongoDB Connection

The application connects to MongoDB at:
```
mongodb://admin:admin@localhost:27017
```

To modify the connection string, edit the `DB_URI` variable in `app/main.py`.

### Voice Selection

The TTS uses the "Callirhoe" voice by default. To change the voice, modify the `voice` parameter in the `speak_with_tts()` function in `main.py`.

### AI Model

The application uses `gemini-2.0-flash` for chat and `gemini-2.5-pro-tts` for text-to-speech. These can be customized in `graph.py` and `main.py` respectively.

## Troubleshooting

### "GOOGLE_API_KEY environment variable is not set"

**Solution**: Ensure your `.env` file contains a valid `GOOGLE_API_KEY` and `GEMINI_API_KEY`.

### "Could not reach Google Speech Recognition service"

**Solution**: Check your internet connection. The Google Speech Recognition API requires an active internet connection.

### "Sorry, I couldn't understand that"

**Solution**: Speak clearly and ensure your microphone is working properly. Adjust the microphone sensitivity in the code if needed.

### MongoDB Connection Error

**Solution**: Ensure Docker is running and MongoDB is started:
```bash
docker-compose up -d
docker-compose ps  # Verify MongoDB is running
```

### Audio Output Not Generated

**Solution**: Check that the `./ai_generated/` directory exists and is writable. The application creates it automatically, but verify permissions if needed.

## Development

### Adding New Tools

To add new tools that the AI can use, define them in `graph.py`:

```python
@tool
def my_tool(param: str):
    """Tool description"""
    # Implementation
    return result

llm_with_tools = llm.bind(tools=[run_command, my_tool])
```

### Customizing the System Prompt

Edit the `system_prompt` in the `chatbot()` function in `graph.py` to change the AI's behavior and instructions.

### Extending Conversation History

The MongoDB checkpointer automatically stores all conversations. Access them by querying the MongoDB database directly or extending the application with a history retrieval feature.

## Performance Considerations

- **Speech Recognition**: Latency depends on audio length and internet connection
- **AI Response**: Typically 1-3 seconds for Gemini to generate a response
- **TTS Generation**: Usually 2-5 seconds depending on text length
- **Total Interaction Time**: Expect 5-15 seconds per full conversation cycle

## Security Notes

- Never commit `.env` files with real API keys to version control
- Use environment variables for all sensitive credentials
- The `run_command` tool can execute arbitrary system commands—use with caution
- MongoDB credentials should be changed in production environments

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Custom voice profiles
- [ ] Conversation analytics and insights
- [ ] Web UI for conversation management
- [ ] Integration with external APIs (weather, news, etc.)
- [ ] Streaming audio responses
- [ ] Voice activity detection for hands-free operation

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

---

**Built with ❤️ using LangGraph, Google Gemini, and MongoDB**
