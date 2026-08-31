# HydraHabit Architecture

## High-Level Flow

```text
                PostgreSQL
                    ▲
                    │
                SQLAlchemy
                    ▲
                    │
                 FastAPI
                    │
        ┌───────────┴───────────┐
        │                       │
   Health Summary          LangGraph Agent
        │                       │
        │              ┌────────┴────────┐
        │              │                 │
        │        Data Quality         Qwen3 1.7B
        │              │                 │
        └──────────────┴─────────────────┘
                       │
                       ▼
                Recommendation
                       │
                       ▼
                  PostgreSQL
```

## Agent Flow

```text
Get User Profile
       ↓
Get Hydration Summary
       ↓
Check Data Quality
       ↓
   ┌───┴───────────┐
   │               │
INSUFFICIENT     SUFFICIENT
   │               │
NO_ACTION          ↓
   │           Qwen3 Analysis
   │               ↓
   └──────→ Save Recommendation
```

## Responsibilities

### FastAPI

Handles HTTP requests and exposes the application APIs.

### PostgreSQL / SQLAlchemy

Stores users, hydration records, recommendations, and agent execution logs.

### Health Summary

Calculates hydration metrics such as average intake, target achievement, gap, trend, and data quality.

### LangGraph

Orchestrates the agent workflow and controls the flow between the different stages.

### Qwen3

Interprets the structured hydration summary and generates the final recommendation.

### Frontend

Provides a simple interface for loading profiles, recording hydration, viewing summaries, and requesting recommendations.
