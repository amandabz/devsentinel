from groq import Groq


class IncidentAnalyzer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def analyze(self, container_stats: dict, logs: str) -> str:
        prompt = f"""
You are a DevOps expert analyzing a container incident.

Container stats:
- Name: {container_stats['name']}
- Status: {container_stats['status']}
- CPU usage: {container_stats['cpu_percent']}%
- Memory usage: {container_stats['mem_percent']}% ({container_stats['mem_usage_mb']} MB)

Recent logs:
{logs}

Analyze what is happening and respond in this exact format:
🔍 DIAGNOSIS: <one sentence explaining what is wrong>
🧠 PROBABLE CAUSE: <one sentence explaining why>
🔧 SUGGESTED FIX: <one concrete action to take>
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        return response.choices[0].message.content or "⚠️ AI analysis unavailable"
