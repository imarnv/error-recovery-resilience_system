import logging

class Alerter:
    @staticmethod
    def send_email(subject, message):
        print(f"[ALERT][EMAIL] Subject: {subject} | Message: {message}")

    @staticmethod
    def send_telegram(message):
        print(f"[ALERT][TELEGRAM] {message}")

    @staticmethod
    def send_webhook(payload):
        print(f"[ALERT][WEBHOOK] Payload: {payload}")

    @classmethod
    def alert_circuit_open(cls, service_name, last_error):
        subject = f"Circuit Breaker OPEN for {service_name}"
        message = f"Service {service_name} has failed repeatedly. Last error: {last_error}"
        cls.send_email(subject, message)
        cls.send_telegram(f"CRITICAL: {subject}. {message}")
        cls.send_webhook({"event": "circuit_open", "service": service_name, "error": str(last_error)})

    @classmethod
    def alert_service_down(cls, service_name, duration):
        message = f"Service {service_name} has been down for {duration} seconds."
        cls.send_email(f"Service Down: {service_name}", message)
        cls.send_telegram(message)
