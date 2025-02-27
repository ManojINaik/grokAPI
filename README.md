# Grok3 API

Grok3 is cool, smart, and useful, but there is no official API available. This is an **unofficial Python client** for interacting with the Grok 3 API. It leverages cookies from browser requests to authenticate and access the API endpoints.

---

## Setup

Follow these steps to get started with the Grok3 API client.

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone git@github.com:ManojINaik/grokAPI.git
```

### 2. Install the Package
Navigate to the project directory, create a virtual environment, and install the package:

```bash
cd grok3-api
python -m venv pyenv  # or virtualenv pyenv

# On Windows
pyenv\Scripts\activate

# On macOS/Linux
source pyenv/bin/activate

# Install the package
pip install .

# For development
pip install -r grok_client/requirements.txt
```

### 3. Obtain Cookie Values

To use this client, you need to extract authentication cookies from a browser session:

* Open grok.com in your browser.
* Log in if you aren't already logged in.
* Open the browser's developer tools (e.g., F12 or right-click > Inspect).
* Go to the "Network" tab and filter for requests containing the new-chat endpoint (e.g., https://grok.com/rest/app-chat/conversations/new).
* Right-click the request, select "Copy as cURL," and paste it somewhere.
* From the curl command, extract the following cookie values from the -H 'cookie: ...' header:
    * x-anonuserid
    * x-challenge
    * x-signature
    * sso
    * sso-rw

Example cookie string from a curl command:
```
-H 'cookie: x-anonuserid=ffdd32e1; x-challenge=TkC4D...; x-signature=fJ0U00...; sso=eyJhbGci...; sso-rw=eyJhbGci...'
```

### 4. Configure Environment

Create a `.env` file in the root directory with your authentication tokens:

```
# API Server Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Grok Model Configuration
MODEL_NAME=grok-3

# Authentication Cookies
GROK_SSO=your_sso_cookie_value_here
GROK_SSO_RW=your_sso_rw_cookie_value_here
```

## Using the API

### Direct Client Usage

Pass the extracted cookie values to the GrokClient and send a message:

```python
from grok_client import GrokClient

# Your cookie values
cookies = {
    "x-anonuserid": "ffdd32e1",
    "x-challenge": "TkC4D..",
    "x-signature": "fJ0...",
    "sso": "ey...",
    "sso-rw": "ey..."
}

# Initialize the client
client = GrokClient(cookies)

# Send a message and get response
response = client.send_message("write a poem")
print(response)
```

### OpenAI-Compatible Client

Use the OpenAI-compatible client for a more familiar interface:

```python
from grok_client.grok_openai_client import GrokOpenAIClient

# Initialize client (will use values from .env file)
client = GrokOpenAIClient()

# Simple completion
response = client.simple_completion("What is the capital of France?")
print(response)

# Chat completion with system message
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    stream=False
)
print(response.choices[0].message.content)

# Get JSON response
json_response = client.json_completion(
    "Give me information about Paris with population and landmarks."
)
print(json_response)
```

### Interactive Chat

Use the interactive chat application for a command-line conversation:

```bash
python -m grok_client.interactive_chat
```

Available commands in interactive chat:
- `exit`, `quit` - Exit the chat
- `clear` - Clear conversation history
- `/help` - Show help message
- `/json` - Toggle JSON response format
- `/temp <value>` - Set temperature (0.0-2.0)
- `/system <message>` - Set system message

## Running the API Server

To run the OpenAI-compatible API server:

```bash
uvicorn grok_client.server:app --reload --host 0.0.0.0 --port 8000
```

This will start a server that implements the OpenAI API interface, allowing you to use the Grok API with any OpenAI-compatible client or library.

### Using the API Server with Other Applications

#### Python (with OpenAI library)

```python
from openai import OpenAI

# Connect to your local API server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy-key"  # Not used but required by the OpenAI client
)

# Create a chat completion
response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like today?"}
    ]
)

print(response.choices[0].message.content)
```

#### JavaScript/Node.js

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'http://localhost:8000/v1',
  apiKey: 'dummy-key', // Not used but required
});

async function main() {
  const response = await openai.chat.completions.create({
    model: 'grok-3',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Explain how solar panels work.' }
    ],
  });

  console.log(response.choices[0].message.content);
}

main();
```

#### cURL

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Tell me a joke."}
    ]
  }'
```

### 5. Optional: Add Memory with Mem0

If you want Grok to remember conversations, you can integrate it with Mem0. Mem0 provides a memory layer for AI applications.

#### 5.1 Install Mem0

```bash
pip install mem0ai
```

#### 5.2 Add & Retrieve Memory

```python
from mem0 import Memory

memory = Memory()

# for user alice
result = memory.add("I like to take long walks on weekends.", user_id="alice")

# Retrieve memories
related_memories = memory.search("What do I like to do on weekends?", user_id="alice")
print(related_memories)
```

## Troubleshooting

- **Authentication Issues**: Make sure your SSO tokens are correct and up-to-date. They may expire after some time.
- **Connection Errors**: Verify that your API server is running and accessible at the configured host and port.
- **Rate Limiting**: If you encounter rate limiting, consider adding delays between requests.

## Disclaimer

This is an **unofficial API client** for Grok3 and is **not affiliated with or endorsed by xAI**, the creators of Grok. It relies on reverse-engineering browser requests and may break if the underlying API changes. 

**Use at your own risk.** The authors are not responsible for any consequences arising from its use, including but not limited to:

- Account suspension or termination
- Data loss or corruption
- Legal issues related to terms of service violations
- Any other direct or indirect damages

Ensure you comply with Grok's terms of service and applicable laws when using this client. This software is provided "as is", without warranty of any kind, express or implied.

By using this client, you acknowledge that:
1. You are responsible for your use of the API
2. You understand the potential risks involved
3. You will not use this client for any malicious purposes or in ways that violate Grok's terms of service



Inspired and improvized from https://github.com/mem0ai/grok3-api