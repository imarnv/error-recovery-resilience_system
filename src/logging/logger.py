import logging
import os
import csv
import datetime

class AppLogger:
    def __init__(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log_event(self, service_name, event_type, details=None, retry_count=0, circuit_state="CLOSED"):
        """
        Logs an event to local file and mock Google Sheets.
        """
        timestamp = datetime.datetime.now().isoformat()
        
        # Local File Logging
        log_message = f"Service: {service_name} | Event: {event_type} | Retry: {retry_count} | Circuit: {circuit_state} | Details: {details}"
        if event_type == "ERROR":
            self.logger.error(log_message)
        else:
            self.logger.info(log_message)

        # Mocking Google Sheets Logging
        self._log_to_google_sheets_mock(timestamp, service_name, event_type, retry_count, circuit_state, details)

    def _log_to_google_sheets_mock(self, timestamp, service_name, event_type, retry_count, circuit_state, details):
        """
        Simulates logging to Google Sheets by printing to console with a specific prefix
        and appending to a CSV file for verification.
        """
        row = [timestamp, service_name, event_type, retry_count, circuit_state, details]
        
        print(f"[Google Sheets (mock)] Append Row: {row}")
        
        with open("logs/google_sheets_mock.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

logger = AppLogger()
