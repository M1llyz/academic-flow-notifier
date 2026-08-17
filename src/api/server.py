from flask import Flask, jsonify

from src.workflows.flow_notifier import run_flow

app = Flask(__name__)

@app.post("/run")
def run_pipeline():
    result = run_flow()

    return jsonify(
        {
            "cards_count": len(result["cards"]),
            "events_count": len(result["events"]),
            "notifications_count": len(result["notifications"]),
            "status": "completed",
        }
    )

@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})