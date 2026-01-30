from src.errors.exceptions import TransientServiceError, PermanentServiceError
from src.config import SIMULATE_ELEVENLABS_503
import time

class ElevenLabsService:
    def __init__(self):
        self.service_name = "ElevenLabs"
        self.simulated_failure_mode = SIMULATE_ELEVENLABS_503
        self.is_currently_healthy = True 
        self.fail_until = 0 

    def generate_speech(self, text):
        """
        Mocks the API call to generate speech.
        """
        if not self.is_currently_healthy:
            raise TransientServiceError("503 Service Unavailable", self.service_name)
            
        print(f"[{self.service_name}] Generating speech for: '{text}'")
        return b"mock_audio_data"

    def check_health(self):
        """
        Returns True if healthy, False otherwise.
        In a real app, this would ping a health endpoint.
        """
        return self.is_currently_healthy

    def set_simulation_mode(self, healthy: bool):
        """
        Helper for simulation runner to toggle health.
        """
        self.is_currently_healthy = healthy
        if healthy:
            print(f"[{self.service_name}] Simulation: Service Restored.")
        else:
            print(f"[{self.service_name}] Simulation: Service Outage Started.")
