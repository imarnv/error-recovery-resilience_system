import os

def get_bool_env(key, default):
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")

SIMULATE_ELEVENLABS_503 = get_bool_env("SIMULATE_ELEVENLABS_503", True)

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 5.0 
RETRY_BACKOFF_FACTOR = 2.0

CIRCUIT_BREAKER_FAILURE_THRESHOLD = 3
CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 10.0

ALERT_WEBHOOK_URL = "https://mock-webhook.com/alert"
