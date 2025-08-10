# Banking Assistant Project

This project implements a simple banking assistant using Python, leveraging the `uv` package manager and virtual environment tool. The assistant supports user authentication and basic banking queries like checking account balance. It uses a modular agent-based architecture with guardrails for input validation and output formatting, powered by the Gemini Flash 2.0 model via an OpenAI-compatible API.

## Features
- **User Authentication**: Validates user credentials (name and PIN) before allowing access to banking services.
- **Banking Queries**: Supports queries like checking account balance for authenticated users.
- **Guardrails**: Input validation for banking-related queries and formatted output responses.
- **Agent-Based Design**: Uses two agents: one for authentication and another for handling banking services.
- **Environment Management**: Uses `uv` for dependency management and virtual environments.

## Prerequisites
- Python 3.8 or higher
- `uv` (Universal Virtual environment manager)
- A Gemini API key (set as an environment variable `GEMINI_API_KEY`)

## Installation

1. **Install `uv`**:
   If you don't have `uv` installed, you can install it via pip or follow the official instructions at [uv documentation](https://github.com/astral-sh/uv):
   ```bash
   pip install uv

Clone the Repository:bash

git clone <repository-url>
cd <repository-directory>

Set Up the Virtual Environment:
Use uv to create and activate a virtual environment:bash

uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install Dependencies:
Create a requirements.txt file with the following dependencies:

python-dotenv
pydantic

Then install them using uv:bash

uv pip install -r requirements.txt

Note: The agents package (containing Agent, Runner, etc.) is assumed to be a custom or third-party library. Ensure it is available in your project or install it as needed.
Set Up Environment Variables:
Create a .env file in the project root and add your Gemini API key:env

GEMINI_API_KEY=your_gemini_api_key_here

UsageActivate the Virtual Environment:
If not already activated, run:bash

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Run the Application:
Execute the main script:bash

python main.py

Interact with the Assistant:Enter your name and a 4-digit PIN when prompted.
For testing, use:Name: Sadiq khan
PIN: 1234

If authentication succeeds, you can ask banking-related questions (e.g., "Check my balance").
Type exit to quit the program.

Example interaction:

Enter your name: Sadiq khan
Enter your 4-digit PIN: 1234
DEBUG: Auth result: Authentication successful., Authenticated: True
Bank Response: Authentication successful.. How can we assist you further?
You are now authenticated. Ask your banking questions.
Your banking question (or 'exit' to quit): Check my balance
Bank Response: Your balance for account 123456789 is $50,000.. How can we assist you further?
Your banking question (or 'exit' to quit): exit

Project Structure

├── main.py              # Main script with authentication and banking logic
├── .env                 # Environment variables (e.g., GEMINI_API_KEY)
├── requirements.txt     # Project dependencies
└── README.md            # This file

Dependenciespython-dotenv: Loads environment variables from a .env file.
pydantic: Used for data validation and modeling (e.g., Account class).
agents: Custom or third-party library for agent-based architecture (ensure availability).
Gemini Flash 2.0 API: Requires a valid API key for model access.

NotesEnsure the GEMINI_API_KEY is valid and correctly set in the .env file.
The agents library is not a standard package. Replace it with the actual library or custom code as needed.
The project assumes a hardcoded account number (123456789) and balance ($50,000) for demonstration purposes.
Guardrails ensure only banking-related queries are processed, and responses are formatted appropriately.

TroubleshootingAuthentication Failure: Verify the name (Sadiq khan) and PIN (1234) are entered correctly.
API Key Issues: Ensure the GEMINI_API_KEY is correctly set in the .env file and that the Gemini API is accessible.
Dependency Errors: Confirm all dependencies are installed using uv pip install -r requirements.txt.
Module Not Found: If the agents module is missing, ensure the library is installed or included in your project.

LicenseThis project is licensed under the MIT License. See the LICENSE file for details.ContributingContributions are welcome! Please submit a pull request or open an issue for any bugs, features, or improvements.

### Notes:
- The README assumes the `agents` package is either a custom module or a third-party library. If it's custom, you may need to include it in the repository or provide instructions for its setup.
- The installation steps use `uv` for virtual environment and dependency management, as specified.
- The usage section includes a sample interaction to guide users.
- The `.env` file setup is emphasized to ensure the Gemini API key is properly configured.
- If the `agents` library requires specific setup or is not publicly available, you may need to provide additional instructions o

