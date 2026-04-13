import os
import time
from dotenv import load_dotenv

from devsentinel.monitor.docker_monitor import DockerMonitor
from devsentinel.alerts.telegram_bot import TelegramAlerter

load_dotenv()

POLL_INTERVAL = 30
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 80.0

previous_states = {}

def check_and_alert(monitor: DockerMonitor, alerter: TelegramAlerter) -> None:
    stats = monitor.get_all_stats()

    for container in stats:
        name = container["name"]
        current_status = container["status"]
        alerts = []

        if container["cpu_percent"] > CPU_THRESHOLD:
            alerts.append(f"⚠️ High CPU: {container['cpu_percent']}%")

        if container["mem_percent"] > MEM_THRESHOLD:
            alerts.append(f"⚠️ High Memory: {container['mem_percent']}%")

        if current_status != "running":
            alerts.append(f"🔴 Container is {current_status}")

        previous = previous_states.get(name)
        current_alert_key = "|".join(alerts)

        if alerts and current_alert_key != previous:
            message = "🛡️ *DevSentinel Alert*\n\n"
            message += f"Container: `{name}`\n"
            message += "\n".join(alerts)
            alerter.alert(message)

        previous_states[name] = current_alert_key if alerts else ""

def main() -> None:
    monitor = DockerMonitor()
    alerter = TelegramAlerter(
        token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        chat_id=os.getenv("TELEGRAM_CHAT_ID", "")
    )

    print("🛡️ DevSentinel started. Monitoring containers...")

    while True:
        check_and_alert(monitor, alerter)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
