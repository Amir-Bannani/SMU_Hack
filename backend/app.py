from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Flask!"})

tasks = [
    {"id": 1, "title": "Update Server Security", "status": "Pending", "assignee": "John Doe"},
    {"id": 2, "title": "Fix Login Bug", "status": "In Progress", "assignee": "Jane Smith"},
    {"id": 3, "title": "Deploy New Feature", "status": "Completed", "assignee": "Mike Johnson"}
]

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = {
        "performance": [
            {"name": "Jan", "value": 65},
            {"name": "Feb", "value": 72},
            {"name": "Mar", "value": 85},
            {"name": "Apr", "value": 78},
            {"name": "May", "value": 90},
            {"name": "Jun", "value": 88}
        ],
        "taskDistribution": [
            {"name": "Pending", "value": 5},
            {"name": "In Progress", "value": 8},
            {"name": "Completed", "value": 12}
        ]
    }
    return jsonify(stats)

@app.route('/api/insights', methods=['GET'])
def get_insights():
    # Mock AI response
    insights = {
        "productivity": "Team productivity has increased by 15% this month. High performance observed in the backend team.",
        "risk": "Potential burnout detected in the frontend team due to high task volume.",
        "recommendation": "Consider redistributing tasks from the frontend team to balance the workload. Schedule a team building activity."
    }
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
