from dotenv import load_dotenv
load_dotenv()  

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool, RunContextWrapper
import os
from pydantic import BaseModel

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Flash 2.0 Setup
client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# Context model
class Account(BaseModel):
    name: str
    pin: int
    account_number: str = "123456789" 
    authenticated: bool = False  

# Input guardrail: Validate banking-related query
def is_banking_query(query: str) -> bool:
    banking_keywords = ["balance", "account", "help"]
    return any(keyword in query.lower() for keyword in banking_keywords)

# Output guardrail: Format responses
def format_response(response: str, authenticated: bool) -> str:
    if not authenticated:
        return "Sorry, authentication failed. Please check your name and PIN."
    return f"Bank Response: {response}. How can we assist you further?"

# Tool 1: Authentication
@function_tool(is_enabled=lambda ctx, agent: True)
def authenticate(ctx: RunContextWrapper[Account]) -> str:
    if ctx.context.name == "Sadiq khan" and ctx.context.pin == 1234:
        ctx.context.authenticated = True
        return "Authentication successful."
    return "Authentication failed. Incorrect name or PIN."

# Tool 2: Check balance
@function_tool(is_enabled=lambda ctx, agent: ctx.context.authenticated)
def check_balance(ctx: RunContextWrapper[Account]) -> str:
    return f"Your balance for account {ctx.context.account_number} is $50,000."

# Agent 1: Authentication Agent
auth_agent = Agent(
    name="Auth Agent",
    instructions="Verify user credentials and authenticate them using the provided tool.",
    tools=[authenticate],
    model=model,
)

# Agent 2: Bank Service Agent
bank_agent = Agent(
    name="Bank Service Agent",
    instructions="Assist authenticated customers with banking queries like checking balance.",
    tools=[check_balance],
    model=model,
)

# Main logic
def main():
    # Input guardrails
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    try:
        pin = int(input("Enter your 4-digit PIN: "))
        if not (1000 <= pin <= 9999):
            print("PIN must be a 4-digit number.")
            return
    except ValueError:
        print("Invalid PIN format.")
        return

    user_context = Account(name=name, pin=pin)

    # Handoff 1: Run Auth Agent
    auth_result = Runner.run_sync(auth_agent, "Authenticate the user.", context=user_context, run_config=config)
    print(f"DEBUG: Auth result: {auth_result.final_output}, Authenticated: {user_context.authenticated}")
    print(format_response(auth_result.final_output, user_context.authenticated))

    # Check if authentication was successful
    if user_context.authenticated:
        print("You are now authenticated. Ask your banking questions.")
        while True:
            query = input("Your banking question (or 'exit' to quit): ").strip()
            if query.lower() == 'exit':
                break
            if not query or not is_banking_query(query):
                print("Please ask a valid banking question (e.g., balance, account).")
                continue

            # Handoff 2: Run Bank Agent
            result = Runner.run_sync(bank_agent, query, context=user_context, run_config=config)
            print(format_response(result.final_output, user_context.authenticated))
    else:
        print("Authentication failed. Exiting.")

if __name__ == "__main__":
    main()