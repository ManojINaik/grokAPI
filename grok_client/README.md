# Grok OpenAI-Compatible Client

This library provides an easy way to interact with the Grok API using the OpenAI-compatible interface. It simplifies the process of authenticating and making requests to the Grok API.

## Features

- Simple authentication with SSO tokens
- Support for streaming and non-streaming responses
- JSON format responses
- Interactive chat application
- Compatible with the OpenAI Python client library

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
API_HOST=127.0.0.1  # Optional, defaults to 127.0.0.1
API_PORT=8000       # Optional, defaults to 8000
MODEL_NAME=grok-3   # Optional, defaults to grok-3
GROK_SSO=your_sso_token_here
GROK_SSO_RW=your_sso_rw_token_here
```

You can obtain the SSO tokens from your Grok account cookies.

## Usage

### Basic Usage

```python
from grok_client.grok_openai_client import GrokOpenAIClient

# Initialize client
client = GrokOpenAIClient()

# Simple completion
response = client.simple_completion("What is the capital of France?")
print(response)
```

### Streaming Responses

```python
from grok_client.grok_openai_client import GrokOpenAIClient

# Initialize client
client = GrokOpenAIClient()

# Get streaming response
stream = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short story about a robot."}
    ],
    stream=True
)

# Process the streaming response
client.process_streaming_response(stream)
```

### JSON Format Responses

```python
from grok_client.grok_openai_client import GrokOpenAIClient
import json

# Initialize client
client = GrokOpenAIClient()

# Get JSON response
json_response = client.json_completion(
    "Give me information about Paris with population and landmarks."
)

print(json.dumps(json_response, indent=2))
```

### Interactive Chat

You can use the interactive chat application to have a conversation with Grok:

```bash
python -m grok_client.interactive_chat
```

Command line options:

```
--host      API host (default: from .env or 127.0.0.1)
--port      API port (default: from .env or 8000)
--model     Model name (default: from .env or grok-3)
--sso       SSO token (default: from .env)
--sso-rw    SSO-RW token (default: from .env)
--json      Request responses in JSON format
--system    Custom system message
--temperature  Temperature for response generation (default: 1.0)
```

### Chat Commands

While in the interactive chat, you can use these commands:

- `exit`, `quit` - Exit the chat
- `clear` - Clear conversation history
- `/help` - Show help message
- `/json` - Toggle JSON response format
- `/temp <value>` - Set temperature (0.0-2.0)
- `/system <message>` - Set system message

## API Server

To run the OpenAI-compatible API server:

```bash
uvicorn grok_client.server:app --reload --host 0.0.0.0 --port 8000
```

This will start a server that implements the OpenAI API interface, allowing you to use the Grok API with any OpenAI-compatible client.

## Examples

See the `example.py` file for more examples of how to use the client.

## License

This project is licensed under the terms of the license included in the repository.