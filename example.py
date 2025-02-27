from grok_client import GrokClient

# Cookie values extracted from .env file
cookies = {
    "sso": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY",
    "sso-rw": "eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiMTNjZTM0OTktMWExMS00NDY5LWI1ODQtYjM3MjEzYTJlNGNjIn0.CH843sGqBaYGyj2AnFh1NTshA4bH3gVT9ikQ9HekViY"
}

# Initialize the client
client = GrokClient(cookies)

# Send a message and get response
response = client.send_message("write a poem")
print("Response from Grok:")
print(response)