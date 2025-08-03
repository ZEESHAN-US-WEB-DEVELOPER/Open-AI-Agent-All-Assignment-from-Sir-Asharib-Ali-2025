import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel

# 🔐 Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ⚙️ Gemini Flash Setup
client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# 🧭 Agent 1: Capital Finder
capital_agent = Agent(
    name="Capital Finder",
    model=model,
    instructions="Return ONLY the capital city of the provided country. No explanation."
)

# 🗣️ Agent 2: Language Finder
language_agent = Agent(
    name="Language Finder",
    model=model,
    instructions="Return ONLY the main language spoken in the provided country. No explanation."
)

# 👥 Agent 3: Population Finder
population_agent = Agent(
    name="Population Finder",
    model=model,
    instructions="Return ONLY the population of the provided country in short format (e.g., '241 million')."
)

# 🧠 Final Orchestrator Agent
orchestrator = Agent(
    name="Country Info Orchestrator",
    model=model,
    instructions="""
You are a smart assistant that summarizes the results from 3 agents: Capital, Language, and Population.

Respond like this:
'The capital of [country] is [capital], the language is [language], and the population is [population].'

If any value is missing, reply:
'I cannot fulfill that request. Please provide a valid country name.'
"""
)

def main():
    print("🌍 Welcome to the Country Info Toolkit!\n")
    country = input("🔎 Enter a country name: ").strip().title()

    try:
        capital = Runner.run_sync(capital_agent, input=country, run_config=config).final_output.strip()
        language = Runner.run_sync(language_agent, input=country, run_config=config).final_output.strip()
        population = Runner.run_sync(population_agent, input=country, run_config=config).final_output.strip()

        combined_input = f"Country: {country}, Capital: {capital}, Language: {language}, Population: {population}"
        summary = Runner.run_sync(orchestrator, input=combined_input, run_config=config)

        print("\n📘 Country Summary:\n" + summary.final_output + "\n")

    except Exception as e:
        print("❌ An error occurred:", e)

if __name__ == "__main__":
    main()