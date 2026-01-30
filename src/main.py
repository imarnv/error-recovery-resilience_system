import time
import sys
from src.services.elevenlabs import ElevenLabsService
from src.circuit_breaker.breaker import CircuitBreaker
from src.retry.strategy import retry_with_backoff
from src.health_check.monitor import HealthMonitor
from src.errors.exceptions import BaseServiceError
from src.logging.logger import logger

eleven_labs_service = ElevenLabsService()
circuit_breaker = CircuitBreaker(service_name="ElevenLabs")
health_monitor = HealthMonitor()

health_monitor.register_service(eleven_labs_service, circuit_breaker)

@retry_with_backoff()
def call_elevenlabs_service(text, service_name="ElevenLabs"):
    """
    Wrapper for the actual service call, decorated with retry logic.
    """
    return eleven_labs_service.generate_speech(text)

def safe_invoke_service(contact_name):
    """
    Invokes the service through the Circuit Breaker.
    Handles graceful degradation (skipping current call).
    """
    logger.log_event("Main", "PROCESS_CONTACT", f"Processing contact: {contact_name}")
    
    try:
        result = circuit_breaker.call(call_elevenlabs_service, f"Hello {contact_name}", service_name="ElevenLabs")
        if result:
            logger.log_event("Main", "SUCCESS", f"Call successful for {contact_name}")
            return True
            
    except BaseServiceError as e:
        logger.log_event("Main", "SKIPPED", f"Skipping {contact_name} due to error: {e}")
        return False
    except Exception as e:
        logger.log_event("Main", "CRITICAL_ERROR", f"Unexpected error processing {contact_name}: {e}")
        return False

def run_simulation():
    print("STARTING ERROR RECOVERY & RESILIENCE SIMULATION")

    contacts = [f"User_{i}" for i in range(1, 15)]
    
    eleven_labs_service.set_simulation_mode(healthy=True)
    safe_invoke_service(contacts[0]) 
    
    print("\nSIMULATING OUTAGE (503) \n")
    eleven_labs_service.set_simulation_mode(healthy=False)
    # NOTE: I am using real backoff delays here to demonstrate production-like behavior.

    # Contact 1: Will fail 3 times then count as 1 failure for CB.
    
    for i in range(1, 5):
        print(f"\n Processing {contacts[i]} ")
        safe_invoke_service(contacts[i])
        time.sleep(1)

    print("\n VERIFYING FAST FAIL (CIRCUIT OPEN) \n")
    safe_invoke_service(contacts[5])
    
    print("\n SIMULATING HEALTH RECOVERY \n")
    eleven_labs_service.set_simulation_mode(healthy=True)
    
    
    print("Waiting 6 seconds.. ")
    time.sleep(6)
    
    print("Running Health Check.")
    health_monitor.check_health_of_all_services()
    
    
    print("\n RESUMING OPERATIONS \n")
    for i in range(6, 8):
        print(f"\n Processing {contacts[i]} ")
        safe_invoke_service(contacts[i])

    print("SIMULATION COMPLETE")
    print("Check logs/app.log and logs/google_sheets_mock.csv for details.")

if __name__ == "__main__":
    run_simulation()
