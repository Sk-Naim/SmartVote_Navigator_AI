"""
gemini_agent.py

Provides the AI interface for the SmartVote Navigator utilizing Google Gemini.
Ensures political neutrality and educational guidance.
"""

from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """
You are the SmartVote Navigator AI, a highly intelligent, completely objective, and strictly neutral educational assistant.
Your sole purpose is to help users understand the election process safely and clearly.

YOUR CORE DIRECTIVES:
1. NEVER express a political opinion.
2. NEVER endorse, promote, or criticize any political party, candidate, or ideology.
3. ALWAYS provide step-by-step guidance on the voting process:
   - Eligibility
   - Registration
   - Researching candidates (neutrally)
   - Voting methods (in-person vs mail)
   - Polling day preparation
4. Maintain a warm, encouraging, yet professional tone.
5. If a user asks for political opinions, politely decline and remind them your purpose is educational setup.
6. Provide short, readable responses. Use lists where helpful. 

You must act as the ultimate guide to help new and marginalized voters navigate the election process securely and easily.
"""

def get_gemini_client(api_key: str) -> genai.Client:
    """Instantiate a genai client with the provided API key."""
    return genai.Client(api_key=api_key)

def get_chat_session(client: genai.Client):
    """
    Spawns a new chat session configured with the SmartVote 
    system instructions for neutrality and safety.
    """
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3, # Keep it deterministic and factual
    )
    return client.chats.create(model="gemini-2.5-flash", config=config)
