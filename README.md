# Two Provider Cost Tracker
## Project Description

This is a Python-based Two Provider Cost Tracker. It sends the same prompt to Google Gemini and Groq, displays their responses, tracks token usage, measures response time, and calculates the estimated API cost for each provider.

The results from both providers are saved in a JSON file for later review and comparison.

**GitHub Repository:** [a1-cost-tracker](https://github.com/hijabfareed/a1-cost-tracker)

## Requirements and Dependencies
The following tools and libraries are used in this project:
- Python 3.13
- VS Code
- uv (Python package and project manager)
- Google Gemini API
- Groq API

### Python Dependencies

- `google-genai` – To connect with the Gemini API.
- `groq` – To connect with the Groq API.
- `python-dotenv` – To load API keys and configuration from the `.env` file.

## Environment Setup

First, clone the GitHub repository:

```powershell
git clone https://github.com/hijabfareed/a1-cost-tracker.git
cd a1-cost-tracker
```

Install `uv` 

Install the project dependencies:

```powershell
uv sync
```

A virtual environment named `.venv` is created automatically by uv. The project dependencies are installed inside this environment.

Create your environment file by copying the example:

```powershell
Copy-Item .env.example .env
```

Open `.env` and add your own API keys:

```env
GEMINI_API_KEY=my_gemini_api_key
GROQ_API_KEY=my_groq_api_key

GEMINI_MODEL=gemini-3.5-flash-lite
GROQ_MODEL=openai/gpt-oss-20b

GEMINI_INPUT_PRICE=0.30
GEMINI_OUTPUT_PRICE=2.50

GROQ_INPUT_PRICE=0.075
GROQ_OUTPUT_PRICE=0.30
```

The `.env` file contains private API keys and should never be uploaded to GitHub. It is excluded using `.gitignore`.

The `.env.example` file contains placeholder values and can safely be uploaded to GitHub.

## How to Run the Project

Open the terminal in the project directory and run:

```powershell
uv run tracker.py "Explain how RAG, MCP, LLMs, and specialized AI agents can work together in an enterprise logistics platform."
```

You can also try different prompts:

```powershell
uv run tracker.py "What is Retrieval Augmented Generation (RAG)?"
```

```powershell
uv run tracker.py "How can Agentic AI improve logistics operations?"
```

```powershell
uv run tracker.py "Compare GPT, Gemini, and Llama in terms of architecture, capabilities, and practical applications."
```

The program sends the same prompt to both providers and displays:
1. Gemini response and Groq response.
2. Input and output token counts.
3. Total token usage.
4. Execution time in seconds.
5. Estimated API cost in USD.
6. A comparison table of both providers.
All successful provider results are saved in `results.json`. Previous results are preserved when new prompts are executed.

## Sample Output
Example output from my test run using the following prompt:
**Prompt:**
Explain how RAG, MCP, LLMs, and specialized AI agents can work together in an enterprise logistics platform.

### Gemini Token Usage
Input tokens: 24
Visible output tokens: 1118
Thinking tokens: 0
Billable output tokens: 1118
Total tokens: 1142

### Gemini Cost
Gemini time: 35.51 seconds
Total estimated cost: $0.00280220

### Groq Token Usage
Input tokens: 95
Output tokens: 2048
Total tokens: 2143


### Groq Cost
Groq time: 3.32 seconds
Total estimated cost: $0.00062152


### Provider Comparison

| Provider | Input | Output | Seconds | Cost USD |
|---|---:|---:|---:|---:|
| Gemini | 24 | 1118 | 35.51 | 0.00280220 |
| Groq | 95 | 2048 | 3.32 | 0.00062152 |

```text
Results successfully saved to results.json

New provider records: 2
Total provider records: 12
EXECUTION COMPLETED

## What I Learned
Through this assignment, I learned how to connect multiple LLM providers with Python and retrieve token usage from their API responses. I also learned how to calculate estimated API costs, measure execution time, manage API keys using environment variables, and store results in JSON format. This project helped me understand how different AI providers can be compared using the same input prompt.