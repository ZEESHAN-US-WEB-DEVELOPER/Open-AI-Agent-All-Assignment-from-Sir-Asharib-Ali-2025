from agents import Agent, Runner, AsyncOenAI, set
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os

# load enviroment variable
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# SET UP THE GIMINI COMPATIBLE OPENAI CLIENT
external_client = AsyncOenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
model = ResponseTextDeltaEvent (
    model="gemini-2.0-flash",
    openai_client = external_client

)