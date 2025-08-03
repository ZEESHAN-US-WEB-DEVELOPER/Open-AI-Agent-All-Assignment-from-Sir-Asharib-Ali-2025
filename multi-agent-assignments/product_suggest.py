import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ⚙️ Set up Gemini Flash model
client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# 🤖 Agent Definition
agent = Agent(
    name="Smart Store Agent",
    instructions=(
        "Suggest a relevant medicine or product based on the user's problem. "
        "Include a short, clear reason.\n\n"
        "Format:\n🤖 Suggestion: [product]\n📌 Reason: [explanation]"
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