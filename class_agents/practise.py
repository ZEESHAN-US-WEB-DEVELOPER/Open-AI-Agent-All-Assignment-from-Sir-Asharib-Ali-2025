from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, AsyncOpenAI,Runner, function_tool, enable_verbose_stdout_logging, RunContextWrapper
from pydantic import BaseModel
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
    agent = 'help me',
    model="gemini-2.0-flash",
    openai_client=external_client

)

# Run config for the agent runner
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class UserContext(BaseModel):
    name:str
    marks:int

@function_tool
def check_result(wrapper: RunContextWrapper[UserContext]) ->str:
    if wrapper.context.marks > 50:
        return "passed"
    else:
        return "failed"
    
