# AI Usage

## AI Tools Used

- ChatGPT
- Ollama / Qwen3

## How AI Was Used

- Used for architecture brainstorming, implementation assistance, debugging, testing ideas, and documentation.
- Important prompts will be listed briefly.

## My Contribution

I worked on the project implementation, integration, testing, and final modifications, with AI used as a development assistant.

## Approximate AI Assistance

Approximately 30–40%, mainly for development assistance, debugging, review, and documentation.

## AI Suggestion Corrected

I modified the approach so that hydration calculations and data-quality checks are handled by the application before the LLM generates its recommendation.

## Technical Issue

Fixed a JSON serialization error during LangGraph/LLM integration.

## Important Prompts

### Architecture

"Design a simple hydration habit agent using FastAPI, PostgreSQL, SQLAlchemy, LangGraph and a local LLM."

### Agent

"Design a LangGraph workflow that retrieves user data, evaluates hydration data quality, analyzes the summary with an LLM, and saves the recommendation."

### Safety

"Review the recommendation workflow to avoid diagnosis, medication advice, or unsafe health recommendations."

### Testing

"Suggest important pytest scenarios for the hydration API, including invalid input, unknown users, duplicate records, and insufficient data."

### Debugging

"Analyze this error and identify the smallest change needed to fix it."
