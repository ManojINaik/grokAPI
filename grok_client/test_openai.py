from openai import OpenAI
import os
import json

# Example cookie values from .env file
COOKIES = {
    "sso": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY",
    "sso-rw": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY"
}

def test_streaming():
    # Initialize OpenAI client with local endpoint
    client = OpenAI(
        base_url="http://localhost:8000/v1",  # Local Grok API server
        api_key="dummy-key"  # Not used but required
    )

    # Create a streaming chat completion
    stream = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        stream=True
    )

    print("Streaming response:")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")

def test_non_streaming():
    # Initialize OpenAI client with local endpoint
    client = OpenAI(
        base_url="http://localhost:8000/v1",  # Local Grok API server
        api_key="dummy-key"  # Not used but required
    )

    # Create a non-streaming chat completion
    response = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        stream=False
    )

    print("Non-streaming response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    # Test streaming completion
    print("Testing streaming completion...")
    test_streaming()

    # Test non-streaming completion
    print("\nTesting non-streaming completion...")
    test_non_streaming()