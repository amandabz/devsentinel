import os
import time
import threading
from dotenv import load_dotenv

from devsentinel.monitor.docker_monitor import DockerMonitor
from devsentinel.alerts.telegram_bot import TelegramAlerter
from devsentinel.ai.analyzer import IncidentAnalyzer
from devsentinel.monitor.metrics_collector import MetricsCollector


load_dotenv()

POLL_INTERVAL = 30
CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 80.0

previous_states: dict = {}
manually_stopped: set = set()


def handle_event(
    event: dict,
    monitor: DockerMonitor,
    alerter: TelegramAlerter,
    analyzer: IncidentAnalyzer,
    collector: MetricsCollector,
) -> None:
    action = event.get("Action", "")
    container_name = event.get("Actor", {}).get("Attributes", {}).get("name", "unknown")

    if action not in {"stop", "die"}:
        return

    print(f"🚨 Event detected: [{action}] on container '{container_name}'")

    if action == "stop":
        # container was stopped manually → simple alert, no AI
        manually_stopped.add(container_name)
        message = (
            "🛡️ *DevSentinel Alert*\n\n"
            f"Container: `{container_name}`\n"
            "🟡 Container was stopped manually."
        )
        alerter.alert(message)
        print(f"✅ Stop alert sent for '{container_name}'")
        return

    if action == "die":
        if container_name in manually_stopped:
            # already alerted via stop event, ignore this die
            manually_stopped.discard(container_name)
            return

        # container crashed unexpectedly → alert with AI analysis
        try:
            stats = monitor.get_container_stats_by_name(container_name)
        except Exception:
            stats = {
                "name": container_name,
                "status": "unknown",
                "cpu_percent": 0.0,
                "mem_usage_mb": 0.0,
                "mem_percent": 0.0,
            }

        message = (
            "🛡️ *DevSentinel Alert*\n\n"
            f"Container: `{container_name}`\n"
            "🔴 Container crashed unexpectedly.\n"
        )

        try:
            logs = collector.get_logs(container_name)
            analysis = analyzer.analyze(stats, logs)
            message += f"\n{analysis}"
        except Exception as e:
            message += f"\n⚠️ AI analysis unavailable: {e}"

        alerter.alert(message)
        print(f"✅ Crash alert sent for '{container_name}'")


def events_loop(
    monitor: DockerMonitor,
    alerter: TelegramAlerter,
    analyzer: IncidentAnalyzer,
    collector: MetricsCollector,
) -> None:
    print("👂 Event listener started.")
    for event in monitor.stream_events():
        try:
            handle_event(event, monitor, alerter, analyzer, collector)
        except Exception as e:
            print(f"❌ Error handling event: {e}")


def metrics_loop(
    monitor: DockerMonitor,
    alerter: TelegramAlerter,
    analyzer: IncidentAnalyzer,
    collector: MetricsCollector,
) -> None:
    print("📊 Metrics polling started.")
    while True:
        try:
            stats = monitor.get_all_stats()
            for container in stats:
                name = container["name"]
                alerts = []

                if container["cpu_percent"] > CPU_THRESHOLD:
                    alerts.append(f"⚠️ High CPU: {container['cpu_percent']}%")

                if container["mem_percent"] > MEM_THRESHOLD:
                    alerts.append(f"⚠️ High Memory: {container['mem_percent']}%")

                if not alerts:
                    previous_states[name] = ""
                    continue

                current_alert_key = "|".join(alerts)
                if current_alert_key == previous_states.get(name):
                    continue

                previous_states[name] = current_alert_key

                message = "🛡️ *DevSentinel Alert*\n\n"
                message += f"Container: `{name}`\n"
                message += "\n".join(alerts)

                try:
                    logs = collector.get_logs(name)
                    analysis = analyzer.analyze(container, logs)
                    message += f"\n\n{analysis}"
                except Exception as e:
                    message += f"\n\n⚠️ AI analysis unavailable: {e}"

                alerter.alert(message)
                print(f"✅ Metrics alert sent for '{name}'")

        except Exception as e:
            print(f"❌ Error in metrics loop: {e}")

        time.sleep(POLL_INTERVAL)


def main() -> None:
    monitor = DockerMonitor()
    alerter = TelegramAlerter(
        token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        chat_id=os.getenv("TELEGRAM_CHAT_ID", "")
    )
    analyzer = IncidentAnalyzer(api_key=os.getenv("GROQ_API_KEY", ""))
    collector = MetricsCollector()

    print("🛡️ DevSentinel started.")

    t_events = threading.Thread(
        target=events_loop,
        args=(monitor, alerter, analyzer, collector),
        daemon=True
    )
    t_metrics = threading.Thread(
        target=metrics_loop,
        args=(monitor, alerter, analyzer, collector),
        daemon=True
    )

    t_events.start()
    t_metrics.start()

    t_events.join()
    t_metrics.join()


if __name__ == "__main__":
    main()
