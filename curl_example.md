# Using Grok API with curl

This example shows how to use the Grok API with a simple curl command.

## Basic Usage

Here's a one-line curl command to send a query to the Grok API:

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Cookie: sso=your_sso_cookie_value_here; sso-rw=your_sso_rw_cookie_value_here" \
  -d '{"model":"grok-3","messages":[{"role":"user","content":"What is the capital of France?"}]}'
```

## How to Use

1. Replace `your_sso_cookie_value_here` and `your_sso_rw_cookie_value_here` with your actual Grok cookie values
2. Run the command in your terminal

## Streaming Response

To get a streaming response (like ChatGPT), add the `stream` parameter:

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Cookie: sso=your_sso_cookie_value_here; sso-rw=your_sso_rw_cookie_value_here" \
  -d '{"model":"grok-3","messages":[{"role":"user","content":"What is the capital of France?"}],"stream":true}'
```

## Windows PowerShell Version

For Windows PowerShell users:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/v1/chat/completions" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Cookie"="sso=your_sso_cookie_value_here; sso-rw=your_sso_rw_cookie_value_here"} `
  -Body '{"model":"grok-3","messages":[{"role":"user","content":"What is the capital of France?"}]}'
```