from src.logging.logger import logger
from src.alerts.alerter import Alerter
from src.circuit_breaker.breaker import CircuitState
from src.errors.exceptions import BaseServiceError

class HealthMonitor:
    def __init__(self):
        self.services = {} 
    def register_service(self, service_instance, circuit_breaker):
        self.services[service_instance.service_name] = (service_instance, circuit_breaker)

    def check_health_of_all_services(self):
        """
        Iterates through registered services and checks their health.
        If a service is healthy and its circuit is OPEN, it attempts to reset it.
        """
        logger.log_event("HealthMonitor", "HEALTH_CHECK_INIT", "Starting periodic health check..")
        
        for name, (service, breaker) in self.services.items():
            if breaker.state == CircuitState.OPEN:
                try:
                    is_healthy = service.check_health()
                    if is_healthy:
                        logger.log_event(name, "HEALTH_CHECK_SUCCESS", "Service is healthy again. Resetting Circuit Breaker.")
                        breaker._transition_to_closed()
                        Alerter.alert_service_down(name, duration="Unknown (Recovered)") # Notify recovery
                    else:
                        logger.log_event(name, "HEALTH_CHECK_FAIL", "Service still unhealthy via health check.")
                except Exception as e:
                     logger.log_event(name, "HEALTH_CHECK_ERROR", f"Error checking health: {e}")
            else:
                 pass
