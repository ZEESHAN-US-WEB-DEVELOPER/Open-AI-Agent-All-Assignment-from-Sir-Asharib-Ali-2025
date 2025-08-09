import os
from dotenv import load_dotenv
from agents import Agent, Runner, GuardrailFunctionOutput, RunContextWrapper,TResponseInputItem, input_guardrail
from pydantic import BaseModel


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ⚙️ Set up Gemini Flash model
client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# 🤖 Agent Definition
agent = Agent(
    name="Bank Agent",
    instructions=(
        ""
    ),
    model=model
)

def main():
    print("🛒 Welcome to the Smart Store! Describe your issue (or type 'exit' to quit):")
    while True:
        user_input = input("🗣️ You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye! Take care.")
            break

        result = Runner.run_sync(agent, input=user_input, run_config=config)
        print(result.final_output + "\n")

if __name__ == "__main__":
    main()