import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
# error on the line No.3



load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,  # Fixed typo: changed mode_provider to model_provider
    tracing_disabled=True
)

poem_agent = Agent(
    name="poet agent",
    instructions="You are a helpful agent. You always write good and funny poems."
)

result = Runner.run_sync(
    poem_agent,
    input="Pls write a very good and funny poem on doll",
    run_config=config
)

print(result.final_output)