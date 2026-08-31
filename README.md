# HydraHabit

A simple AI-assisted hydration habit tracker that analyzes recent water-intake data and provides a personalized recommendation.

## Features

- User profile management
- Daily hydration logging
- 7-day hydration summary
- Average intake and target achievement
- Trend detection
- Missing and suspicious data detection
- AI-generated hydration recommendations
- LangGraph agent workflow
- Agent execution logging
- PostgreSQL database
- REST API with FastAPI
- Simple web UI
- Automated API tests

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- LangGraph
- Ollama
- Qwen3 1.7B
- HTML / CSS / JavaScript
- Pytest

## Architecture

```text
                PostgreSQL
                    ▲
                    │
              SQLAlchemy
                    │
                    ▼
                FastAPI
                    │
        ┌───────────┴───────────┐
        │                       │
   Health Summary          LangGraph Agent
        │                       │
        │              ┌────────┴────────┐
        │              │                 │
        │          Data Quality       Qwen3
        │              │                 │
        └──────────────┴─────────────────┘
                       │
                       ▼
                Recommendation
```

The application calculates important hydration metrics and data-quality information deterministically. The LLM receives the structured summary and is used mainly to interpret the information and generate a recommendation.

## Agent Workflow

```text
Get User Profile
       ↓
Get Hydration Summary
       ↓
Check Data Quality
       ↓
   ┌───┴───────────────┐
   │                   │
Insufficient          Sufficient
   │                   │
NO_ACTION              ↓
   │               Qwen3 Analysis
   │                   ↓
   └────────────→ Save Recommendation
```

Agent execution steps are logged in the database.

## API Endpoints

### Users

```
POST /users
GET  /users/{user_id}
```

### Hydration Data

```
POST /health-data
GET  /health-data/{user_id}
```

### Health Summary

```
GET /health-summary/{user_id}
```

### Agent

```
POST /agent/analyze/{user_id}
GET  /agent/logs/{user_id}
```

### Recommendations

```
GET /recommendations/{user_id}
```

Interactive API documentation is available through FastAPI Swagger UI at:

```
/docs
```

## Sample Data

The project includes three sample users representing different situations:

- Improving hydration
- Imperfect data with missing and suspicious values
- Insufficient data

Seed the database with:

```
python seed/seed_data.py
```

To reset and recreate the sample data:

```
python -m seed.seed_data --reset
```

## Running the Project

### 1. Create and activate virtual environment

```
python -m venv .venv
```

Windows:

```
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Create a `.env` file with the database connection:

```
DATABASE_URL=your_postgresql_connection_string
```

Do not commit `.env`.

### 4. Run database migrations

```
alembic upgrade head
```

### 5. Seed sample data

```
python seed/seed_data.py
```

### 6. Run the API

```
fastapi dev app/main.py
```

Open:

```
http://127.0.0.1:8000/docs
```

The frontend can be opened from the frontend directory.

## Testing

Run:

```
python -m pytest -v
```

The project includes automated tests for:

- Unknown users
- Invalid hydration input
- Future hydration dates
- Duplicate hydration records
- Profile retrieval
- Health summary retrieval
- Unknown-user API behavior

## Safety

The agent is designed as a wellness-tracking prototype rather than a medical diagnostic system.

Recommendations are based on the supplied profile and calculated hydration summary. The agent is instructed not to diagnose medical conditions or prescribe medication or treatment.

When the available hydration data is insufficient, the agent avoids making a normal recommendation and instead asks the user to continue recording data.

## Documentation

Additional project documentation is available in the `docs/` directory:

- [Architecture](docs/architecture.md)
- [Database Schema](docs/database-schema.md)
- [Product Note](docs/product-note.md)
- [AI Usage](AI_USAGE.md)

## Project Status

HydraHabit is a functional prototype demonstrating:

- deterministic health-data processing
- data-quality checks
- agent orchestration with LangGraph
- local LLM integration
- recommendation generation
- persistent agent execution logs
- API and UI integration
