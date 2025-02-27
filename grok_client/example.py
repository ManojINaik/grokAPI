from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_grok_api():
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    api_host = os.getenv('API_HOST', '127.0.0.1')
    api_port = os.getenv('API_PORT', '8000')
    model_name = os.getenv('MODEL_NAME', 'grok-3')
    grok_sso = os.getenv('GROK_SSO')
    grok_sso_rw = os.getenv('GROK_SSO_RW')
    
    if not all([grok_sso, grok_sso_rw]):
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    # Initialize OpenAI client with local endpoint
    client = OpenAI(
        base_url=f"http://{api_host}:{api_port}/v1",
        api_key="dummy-key",  # Not used but required
        default_headers={
            "Cookie": f"sso={grok_sso}; sso-rw={grok_sso_rw}"
        }
    )
    
    def test_simple_questions():
        questions = [
            "What is the capital of France?"
        ]
        
        logger.info("Testing simple questions...")
        for question in questions:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": question}
                    ]
                )
                logger.info(f"\nQ: {question}")
                print(f"A: {response.choices[0].message.content}")
            except Exception as e:
                logger.error(f"Question failed: {e}")

    # Run tests
    test_simple_questions()

if __name__ == "__main__":
    test_grok_api() 