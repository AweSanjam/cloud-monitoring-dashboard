import psutil
import json
import requests
import openai
import random
import os

# ========== CONFIG ==========

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")  # or replace with your key as string for quick test

# Path to where your dashboard reads data from
DATA_FILE = "data.json"

# ========== SYSTEM MONITORING ==========

def get_system_metrics():
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": random.randint(100, 10000)  # mock uptime
    }
    return data

# ========== ALERT LOGIC ==========

def check_alerts(metrics):
    alerts = []
    if metrics["cpu"] > 80:
        alerts.append("High CPU usage")
    if metrics["memory"] > 85:
        alerts.append("High memory usage")
    if metrics["disk"] > 90:
        alerts.append("Low disk space")
    return alerts

# ========== GPT RESPONSE ==========

def get_auto_response(alerts):
    if not alerts:
        return "✅ All systems are running within normal parameters."

    prompt = f"""
    You are an IT support engineer. Provide polite, professional auto-responses for the following system issues:
    {', '.join(alerts)}.
    Format it like a support email.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"⚠️ Error getting response from GPT: {e}"

# ========== SAVE METRICS TO FILE ==========

def save_data(metrics, alerts, response):
    output = {
        "metrics": metrics,
        "alerts": alerts,
        "auto_response": response
    }
    with open(DATA_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print("✅ Data written to dashboard!")

# ========== MAIN ==========

def main():
    metrics = get_system_metrics()
    alerts = check_alerts(metrics)
    auto_response = get_auto_response(alerts)
    save_data(metrics, alerts, auto_response)
    print("\n🚨 Auto-Response:\n", auto_response)

if __name__ == "__main__":
    main()
