import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, AsyncOpenAI,Runner
from agents.run import RunConfig
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Set up the Gemini-compatible OpenAI client
external_client = AsyncOpenAI(
api_key=gemini_api_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Setup the model
model = ResponseTextDeltaEvent(
model="gemini-2.0-flash",
openai_client=external_client
)

# Run config for the agent runner
config = RunConfig(
model=model,
model_provider=external_client,
tracing_disabled=True
)
    
async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    prompt=input("enter your query ")

    result = Runner.run_streamed(agent,prompt)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "_main_":
    asyncio.run(main())