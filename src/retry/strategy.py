import time
import functools
from src.errors.exceptions import TransientServiceError
from src.config import MAX_RETRIES, INITIAL_RETRY_DELAY, RETRY_BACKOFF_FACTOR
from src.logging.logger import logger

def retry_with_backoff(
    max_retries=MAX_RETRIES,
    initial_delay=INITIAL_RETRY_DELAY,
    backoff_factor=RETRY_BACKOFF_FACTOR
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            # Basically Logic is if it's a method calling 'self'then we might want to get the service name from self.service_name if it exists
            service_name = kwargs.get('service_name', "Service")
            if hasattr(args[0], 'service_name'):
                 service_name = args[0].service_name

            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except TransientServiceError as e:
                    retries += 1
                    if retries > max_retries:
                        logger.log_event(service_name, "RETRY_EXHAUSTED", f"Max retries ({max_retries}) exceeded.", retry_count=retries)
                        raise e 
                    
                    logger.log_event(service_name, "RETRY_ATTEMPT", f"Transient error caught: {e}. Retrying in {delay}s...", retry_count=retries)
                    time.sleep(delay)
                    delay *= backoff_factor
            return None 
        return wrapper
    return decorator
