# Error Recovery & Resilience System

This project demostrates an error handling system for an AI Call Agent featuring **Retry Logic**, **Circuit Breakers**, **Structured Logging** and **Alerting**.

## Architecture

The system is designed with a modular architecture:

- **`src/errors`**: Defines a custom exception hierarchy (`TransientServiceError`, `PermanentServiceError`).
- **`src/retry`**: Implements a reusable `@retry_with_backoff` decorator for transient errors.
- **`src/circuit_breaker`**: Implements the Circuit Breaker pattern (CLOSED -> OPEN -> HALF_OPEN).
- **`src/health_check`**: Monitors service health and automatically resets circuit breakers.
- **`src/alerts`**: Mock implementation of multi-channel alerting (Email, Telegram, Webhook).
- **`src/logging`**: Structured logging to local files and mock Google Sheets.
- **`src/services`**: Mock external services (ElevenLabs) with simulation capabilities.

## Key Features

1.  **Transient Error Handling**: Automatically retries failed calls with some time backoff.
2.  **Circuit Breaker**: Fails fast after a configured number of failures (`config.py`) to protect the system and dependency.
3.  **Graceful Degradation**: Skips calls when the circuit is OPEN while ensuring the system doesn't hang.
4.  **Auto-Recovery**: Periodic health checks detects when service is back online and resets the circuit breaker.

## Simulation Scenario

The `src/main.py` script runs a simulation scenario:
1.  **Happy Path**: Successful calls to ElevenLabs.
2.  **Failure Injection**: Simulates a 503 Service Unavailable.
3.  **Resilience**:
    - Detects error.
    - Retries 3 times (time backoff).
    - Opens Circuit Breaker after threshold.
    - Triggers Alerts.
4.  **Degradation**: Skips subsequent calls immediately.
5.  **Recovery**: Simulates service restoration then Health Check detects it and Circuit Breaker is reset.
6.  **Resume**: Normal processing resumes.

## How to Run

1.  Navigate to the project root.
2.  Run the simulation:
    ```bash
    export PYTHONPATH=$PYTHONPATH:.
    python3 src/main.py
    ```
3.  Check the logs:
    - `logs/app.log`: Detailed application logs.
    - `logs/google_sheets_mock.csv`: Mock Google Sheets entries.

## Configuration

All configurable parameters are in `src/config.py`.
