import time
from enum import Enum
from src.config import CIRCUIT_BREAKER_FAILURE_THRESHOLD, CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from src.errors.exceptions import BaseServiceError
from src.logging.logger import logger
from src.alerts.alerter import Alerter

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, service_name):
        self.service_name = service_name
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.threshold = CIRCUIT_BREAKER_FAILURE_THRESHOLD
        self.recovery_timeout = CIRCUIT_BREAKER_RECOVERY_TIMEOUT

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self._transition_to_half_open()
            else:
                logger.log_event(self.service_name, "CIRCUIT_OPEN_REJECT", "Call rejected due to open circuit", circuit_state=self.state.value)
                raise BaseServiceError(f"Circuit Breaker is OPEN for {self.service_name}", self.service_name)

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except BaseServiceError as e:
            self._on_failure(e)
            raise e

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_closed()
            logger.log_event(self.service_name, "CIRCUIT_RECOVERY", "Service recovered, circuit closed", circuit_state=self.state.value)
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def _on_failure(self, error):
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.log_event(self.service_name, "FAILURE_COUNT", f"{self.failure_count}/{self.threshold}", circuit_state=self.state.value)

        if self.state == CircuitState.HALF_OPEN or self.failure_count >= self.threshold:
            self._transition_to_open(error)

    def _transition_to_open(self, error):
        self.state = CircuitState.OPEN
        logger.log_event(self.service_name, "CIRCUIT_STATE_CHANGE", f"Transitioned to OPEN", circuit_state=self.state.value)
        Alerter.alert_circuit_open(self.service_name, error)

    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        logger.log_event(self.service_name, "CIRCUIT_STATE_CHANGE", "Transitioned to CLOSED", circuit_state=self.state.value)

    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        logger.log_event(self.service_name, "CIRCUIT_STATE_CHANGE", "Transitioned to HALF_OPEN (Probing)", circuit_state=self.state.value)
