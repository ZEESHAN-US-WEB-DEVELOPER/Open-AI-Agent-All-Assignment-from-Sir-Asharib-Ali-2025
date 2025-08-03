import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
# Load environment variables
load_dotenv()
# Initialize OpenAI client with Gemini API endpoint
# Get API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")


# ⚙️ Gemini Flash 2.0 Setup
client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# Disable tracing to reduce overhead
set_tracing_disabled(disabled=True)
# Define specialized agents
faq_agent = Agent(
    name="FAQAgent",
    instructions=("Answer common customer questions about store hours, menu, or location. Be concise and friendly."),
    model=model
)
order_agent = Agent(
    name="OrderAgent", 
    model="gemini-2.0-flash",  # Updated to correct model name
    instructions="Provide order status updates based on the order ID provided. Use the check_order_status tool.",
    tools=[{
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Check the status of an order by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, e.g., 12345"
                    }
                },
                "required": ["order_id"]
            }
        }
    }]
)
complaint_agent = Agent(
    name="ComplaintAgent",
    model="gemini-2.0-flash",  # Updated to correct model name
    instructions="Handle customer complaints empathetically and offer solutions or escalate if needed.",
)
# Define triage agent to route queries
triage_agent = Agent(
    name="TriageAgent",
    model="gemini-2.0-flash",  # Updated to correct model name
    instructions="Analyze the user's query and route it to the appropriate agent: FAQAgent for general questions, OrderAgent for order status, or ComplaintAgent for complaints.",
    handoffs=[faq_agent, order_agent, complaint_agent]
)

async def check_order_status(order_id: str) -> str:
    # Simulated order status database
    order_statuses = {
        "12345": "In transit",
        "67890": "Delivered",
        "11111": "Processing"
    }
    
    # Simulate a small delay to mimic real database query
    await asyncio.sleep(0.1)
    
    # Return order status or not found message
    return order_statuses.get(order_id, "Order ID not found.")

# Main function to run the support agent system
async def run_support_agent():
    print("Welcome to the Customer Support Agent System!")
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input("Enter your query: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            # Run the triage agent with user input
            result = await Runner.run_sync(
                input=user_input,
                agent=triage_agent, complaint_agent=complaint_agent,
                tools={"check_order_status": check_order_status}
            )
            # Print the final response
            print(f"Response: {result.final_output}\n")
        except Exception as e:
            print(f"Error processing query: {str(e)}\n")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(run_support_agent())
