import requests
import logging
import yaml

logger = logging.getLogger("NotificationLogger")

class NotificationHandler:
    def __init__(self, config):
        self.notifications = config.get("notifications", [])

    def send_notification(self, message):
        for destination in self.notifications:
            notify_type = destination.get("type")
            webhook = destination.get("webhook")

            if notify_type == "discord":
                self._send_discord_notification(webhook, message)
            else:
                logger.warning(f"Unsupported notification type: {notify_type}")

    def _send_discord_notification(self, webhook, message):
        if not webhook:
            logger.error("Discord webhook URL is missing.")
            return

        payload = {"content": message}
        try:
            response = requests.post(webhook, json=payload)
            if response.status_code == 204:
                logger.info("Discord notification sent successfully.")
            else:
                logger.error(f"Failed to send Discord notification. Status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error sending Discord notification: {e}")