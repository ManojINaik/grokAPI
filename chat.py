#!/usr/bin/env python

"""
Grok Interactive Chat

This script provides a command-line interface for interacting with the Grok API.
It allows users to have a conversation with the Grok model through a simple text interface.

Usage:
    python chat.py

Requirements:
    - A running Grok API server (default: http://localhost:8000)
    - Environment variables set in .env file (GROK_SSO, GROK_SSO_RW)
"""

from grok_client.interactive import interactive_chat

if __name__ == "__main__":
    interactive_chat()