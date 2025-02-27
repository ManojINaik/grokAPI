from openai import OpenAI
import os
import json
import logging
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GrokOpenAIClient:
    """
    A client for interacting with the Grok API using the OpenAI-compatible interface.
    This client simplifies the process of authenticating and making requests to the Grok API.
    """
    
    def __init__(self, 
                 api_host: str = None, 
                 api_port: str = None, 
                 model_name: str = None, 
                 sso_token: str = None, 
                 sso_rw_token: str = None,
                 load_from_env: bool = True):
        """
        Initialize the Grok OpenAI client.
        
        Args:
            api_host (str, optional): The API host. Defaults to value from environment or '127.0.0.1'.
            api_port (str, optional): The API port. Defaults to value from environment or '8000'.
            model_name (str, optional): The model name to use. Defaults to value from environment or 'grok-3'.
            sso_token (str, optional): The SSO token for authentication. Required if not loading from env.
            sso_rw_token (str, optional): The SSO-RW token for authentication. Required if not loading from env.
            load_from_env (bool, optional): Whether to load configuration from environment. Defaults to True.
        """
        # Load environment variables if requested
        if load_from_env:
            load_dotenv()
            
        # Get configuration from parameters or environment
        self.api_host = api_host or os.getenv('API_HOST', '127.0.0.1')
        self.api_port = api_port or os.getenv('API_PORT', '8000')
        self.model_name = model_name or os.getenv('MODEL_NAME', 'grok-3')
        self.sso_token = sso_token or os.getenv('GROK_SSO')
        self.sso_rw_token = sso_rw_token or os.getenv('GROK_SSO_RW')
        
        # Validate required tokens
        if not all([self.sso_token, self.sso_rw_token]):
            raise ValueError("Missing required authentication tokens. Provide them as parameters or in .env file.")
        
        # Initialize OpenAI client with local endpoint
        self.client = OpenAI(
            base_url=f"http://{self.api_host}:{self.api_port}/v1",
            api_key="dummy-key",  # Not used but required by the OpenAI client
            default_headers={
                "Cookie": f"sso={self.sso_token}; sso-rw={self.sso_rw_token}"
            }
        )
        
        logger.info(f"Initialized GrokOpenAIClient with endpoint: http://{self.api_host}:{self.api_port}/v1")
    
    def list_models(self):
        """
        List available models.
        
        Returns:
            dict: The models response from the API.
        """
        try:
            return self.client.models.list()
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            raise
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       stream: bool = False, 
                       temperature: float = 1.0,
                       max_tokens: int = None,
                       model: str = None,
                       response_format: Dict[str, str] = None) -> Any:
        """
        Create a chat completion with the Grok API.
        
        Args:
            messages (List[Dict[str, str]]): The messages to send to the API.
                Each message should have 'role' and 'content' keys.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            temperature (float, optional): The temperature for response generation. Defaults to 1.0.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to None.
            model (str, optional): The model to use. Defaults to the client's model_name.
            response_format (Dict[str, str], optional): The format for the response. 
                Use {"type": "json_object"} for JSON responses. Defaults to None.
        
        Returns:
            Union[str, Iterator]: The completion response or a stream of responses.
        """
        try:
            # Use the provided model or default to the client's model_name
            model_name = model or self.model_name
            
            # Create the completion request parameters
            params = {
                "model": model_name,
                "messages": messages,
                "stream": stream,
                "temperature": temperature
            }
            
            # Add optional parameters if provided
            if max_tokens is not None:
                params["max_tokens"] = max_tokens
                
            if response_format is not None:
                params["response_format"] = response_format
            
            # Make the API request
            response = self.client.chat.completions.create(**params)
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating chat completion: {e}")
            raise
    
    def process_streaming_response(self, stream):
        """
        Process a streaming response and print it to the console.
        
        Args:
            stream: The streaming response from the API.
            
        Returns:
            str: The complete response text.
        """
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print()  # Add a newline after the response
        return full_response
    
    def simple_completion(self, prompt: str, system_message: str = None) -> str:
        """
        A simplified method to get a completion for a single prompt.
        
        Args:
            prompt (str): The user's prompt.
            system_message (str, optional): An optional system message to set context.
                Defaults to None.
        
        Returns:
            str: The completion response.
        """
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
            
        # Add user message
        messages.append({"role": "user", "content": prompt})
        
        # Get completion
        response = self.chat_completion(messages=messages, stream=False)
        
        # Return the content of the response
        return response.choices[0].message.content
    
    def json_completion(self, prompt: str, system_message: str = None) -> dict:
        """
        Get a completion in JSON format.
        
        Args:
            prompt (str): The user's prompt.
            system_message (str, optional): An optional system message to set context.
                Defaults to a message requesting JSON output.
        
        Returns:
            dict: The parsed JSON response.
        """
        # Default system message for JSON responses if not provided
        if system_message is None:
            system_message = "You are a helpful assistant that always responds in valid JSON format."
            
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # Get completion with JSON format
        response = self.chat_completion(
            messages=messages, 
            stream=False,
            response_format={"type": "json_object"}
        )
        
        # Parse and return the JSON response
        content = response.choices[0].message.content
        return json.loads(content)

# Example usage
def example_usage():
    # Initialize client
    client = GrokOpenAIClient(load_from_env=True)
    
    # Simple completion
    response = client.simple_completion("What is the capital of France?")
    print(f"Simple completion response:\n{response}\n")
    
    # JSON completion
    json_response = client.json_completion(
        "Give me information about Paris with population and famous landmarks."
    )
    print(f"JSON completion response:\n{json.dumps(json_response, indent=2)}\n")
    
    # Streaming completion
    print("Streaming completion response:")
    stream = client.chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short story about a robot learning to feel emotions."}
        ],
        stream=True
    )
    client.process_streaming_response(stream)

if __name__ == "__main__":
    example_usage()