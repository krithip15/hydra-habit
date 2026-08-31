# HydraHabit API

Base URL: `http://127.0.0.1:8000`

## Endpoints

### POST /users

Creates a user profile.

### POST /health-data

Adds daily hydration data.

### GET /health-summary/{user_id}

Returns hydration average, achievement, gap, trend, and data quality.

### POST /agent/analyze/{user_id}

Runs the agent and returns the insight, recommendation, action, and confidence.

### GET /recommendations/{user_id}

Returns saved recommendations.

### GET /agent/logs/{user_id}

Returns agent execution logs including tool input, output, decision summary, and final action.

## Example

### POST /health-data

```json
{
  "user_id": 1,
  "date": "2026-08-31",
  "water_intake_ml": 2050
}
```

### GET /health-summary/1

```json
{
  "target_ml": 2200,
  "average_intake_ml": 1642.86,
  "trend": "IMPROVING",
  "data_quality": "GOOD"
}
```

## Errors

- `400` — Invalid request / agent error
- `404` — User not found
- `409` — Duplicate record
- `422` — Validation error
