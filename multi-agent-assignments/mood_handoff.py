import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# 🔐 Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ⚙️ Gemini Flash 2.0 Setup
client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# 🧠 Agent 1: Mood Detector
mood_agent = Agent(
    name="Mood Detector",
    instructions=(
        "You're a mood analysis bot. Read the user's message and respond with ONLY ONE word: "
        "happy, sad, angry, excited, stressed, or neutral. No extra text or explanation."
    ),
    model=model
)

# 💡 Agent 2: Uplift Activity Suggester
activity_agent = Agent(
    name="Uplift Buddy",
    instructions=(
        "If the user's mood is sad, stressed, or angry, suggest a simple and comforting activity.\n\n"
        "Use this format:\n"
        "🧘 Suggested Activity: [activity]\n💬 Note: [encouraging message]"
    ),
    model=model
)

def main():
    print("🌈 Welcome to the Mood Analyzer! (Type 'exit' to quit)\n")
    while True:
        user_input = input("🗣️ How are you feeling? ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Take care! Stay strong and positive.\n")
            break
        if not user_input:
            print("⚠️ Please enter a message to analyze.\n")
            continue

        mood = Runner.run_sync(mood_agent, input=user_input, run_config=config).final_output.strip().lower()
        print(f"🔍 Detected Mood: {mood}")

        if mood in ["sad", "stressed", "angry"]:
            suggestion = Runner.run_sync(activity_agent, input=user_input, run_config=config)
            print(suggestion.final_output + "\n")
        elif mood in ["happy", "excited", "neutral"]:
            print("✅ You're doing well! Keep up the positive vibes! 🌟\n")
        else:
            print("⚠️ Mood not recognized. Try expressing it differently.\n")

if __name__ == "__main__":
    main()