from openai import OpenAI
import os
import json
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default cookie values (replace with your own or use command line arguments)
DEFAULT_COOKIES = {
    "sso": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY",
    "sso-rw": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY"
}

def test_models_endpoint(client):
    """Test the models endpoint"""
    try:
        models = client.models.list()
        logger.info(f"Available models: {models}")
        return True
    except Exception as e:
        logger.error(f"Error testing models endpoint: {e}")
        return False

def test_streaming_completion(client):
    """Test streaming chat completion"""
    try:
        logger.info("Testing streaming completion...")
        stream = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ],
            stream=True
        )

        print("Streaming response:")
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)
        print("\n")
        
        logger.info(f"Completed streaming response: {len(full_response)} characters")
        return True
    except Exception as e:
        logger.error(f"Error testing streaming completion: {e}")
        return False

def test_non_streaming_completion(client):
    """Test non-streaming chat completion"""
    try:
        logger.info("Testing non-streaming completion...")
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
        
        logger.info(f"Completed non-streaming response")
        return True
    except Exception as e:
        logger.error(f"Error testing non-streaming completion: {e}")
        return False

def test_json_format(client):
    """Test JSON format response"""
    try:
        logger.info("Testing JSON format response...")
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in JSON format."},
                {"role": "user", "content": "Give me information about Paris in JSON format with population and famous landmarks."}
            ],
            response_format={"type": "json_object"},
            stream=False
        )

        print("JSON format response:")
        content = response.choices[0].message.content
        print(content)
        
        # Verify it's valid JSON
        try:
            json_data = json.loads(content)
            logger.info(f"Valid JSON response received with keys: {list(json_data.keys())}")
            return True
        except json.JSONDecodeError:
            logger.error("Response is not valid JSON")
            return False
    except Exception as e:
        logger.error(f"Error testing JSON format: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test OpenAI-compatible Grok API')
    parser.add_argument('--base-url', default="http://localhost:8000/v1", help='Base URL for the API')
    parser.add_argument('--sso', help='SSO cookie value')
    parser.add_argument('--sso-rw', help='SSO-RW cookie value')
    
    args = parser.parse_args()
    
    # Set up cookies in header
    cookies = DEFAULT_COOKIES.copy()
    if args.sso:
        cookies["sso"] = args.sso
    if args.sso_rw:
        cookies["sso-rw"] = args.sso_rw
    
    # Convert cookies to header format
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    
    # Initialize OpenAI client
    client = OpenAI(
        base_url=args.base_url,
        api_key="dummy-key",  # Not used but required by the OpenAI client
        default_headers={"cookie": cookie_header}
    )
    
    logger.info(f"Testing OpenAI-compatible Grok API at {args.base_url}")
    
    # Run tests
    tests = [
        ("Models endpoint", test_models_endpoint),
        ("Streaming completion", test_streaming_completion),
        ("Non-streaming completion", test_non_streaming_completion),
        ("JSON format", test_json_format)
    ]
    
    results = {}
    for name, test_func in tests:
        logger.info(f"Running test: {name}")
        results[name] = test_func(client)
    
    # Print summary
    print("\n===== Test Results =====")
    all_passed = True
    for name, result in results.items():
        status = "PASSED" if result else "FAILED"
        if not result:
            all_passed = False
        print(f"{name}: {status}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())