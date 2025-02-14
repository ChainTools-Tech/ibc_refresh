import requests
import logging
from datetime import datetime


notification_logger = logging.getLogger("NotificationLogger")

class NotificationHandler:
    def __init__(self, config):
        self.notifications = config.get("notifications", [])

    def send_notification(self, title, description, severity="info", command=None, chain=None, dst_chain=None):
        color_map = {
            "critical": 16711680,  # Red
            "warning": 16776960,   # Yellow
            "info": 3066993        # Blue
        }
        embed_color = color_map.get(severity, 3066993)
        timestamp = datetime.now(datetime.UTC)

        for destination in self.notifications:
            notify_type = destination.get("type")
            webhook = destination.get("webhook")

            if notify_type == "discord":
                self._send_discord_notification(webhook, title, description, embed_color, command, chain, dst_chain, timestamp)
            elif notify_type == "slack":
                self._send_slack_notification(webhook, title, description, command, chain, dst_chain, timestamp)
            else:
                notification_logger.warning(f"Unsupported notification type: {notify_type}")

    def _send_discord_notification(self, webhook, title, description, color, command, chain, dst_chain, timestamp):
        if not webhook:
            notification_logger.error("Discord webhook URL is missing.")
            return

        embed = {
            "username": "IBC Refresh",
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                    "fields": [
                        {"name": "🔹 Command", "value": f"`{command}`"} if command else None,
                        {"name": "🔹 Chain", "value": chain} if chain else None,
                        {"name": "🔹 Destination Chain", "value": dst_chain} if dst_chain else None
                    ],
                    "timestamp": timestamp,
                    "footer": {"text": "IBC Refresh Notification"}
                }
            ]
        }
        embed["embeds"][0]["fields"] = [field for field in embed["embeds"][0]["fields"] if field]

        try:
            response = requests.post(webhook, json=embed)
            if response.status_code == 204:
                notification_logger.info("Discord notification sent successfully.")
            else:
                notification_logger.error(f"Failed to send Discord notification. Status code: {response.status_code}")
        except requests.RequestException as e:
            notification_logger.error(f"Error sending Discord notification: {e}")

    def _send_slack_notification(self, webhook, title, description, command, chain, dst_chain, timestamp):
        if not webhook:
            notification_logger.error("Slack webhook URL is missing.")
            return
        payload = {
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*"}},
                {"type": "section", "fields": [
                    {"type": "mrkdwn", "text": f"*🔹 Description:*\n`{description}`"} if command else None,
                    {"type": "mrkdwn", "text": f"*🔹 Command:*\n`{command}`"} if command else None,
                    {"type": "mrkdwn", "text": f"*🔹 Chain:*\n{chain}"} if chain else None,
                    {"type": "mrkdwn", "text": f"*🔹 Destination Chain:*\n{dst_chain}"} if dst_chain else None
                ]},
                {"type": "context", "elements": [
                    {"type": "mrkdwn", "text": f"📅 Timestamp: {timestamp}"}
                ]}
            ]
        }
        payload["blocks"][1]["fields"] = [field for field in payload["blocks"][1]["fields"] if field]
        try:
            response = requests.post(webhook, json=payload)
            if response.status_code == 200:
                notification_logger.info("Slack notification sent successfully.")
            else:
                notification_logger.error(f"Failed to send Slack notification. Status code: {response.status_code}")
        except requests.RequestException as e:
            notification_logger.error(f"Error sending Slack notification: {e}")