from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@app.route('/api/weekly-summary', methods=['GET'])
def get_weekly_summary():
    try:
        # Path to the generated JSON
        data_path = os.path.join(DATA_DIR, 'weekly_summary.json')
        
        if not os.path.exists(data_path):
            return jsonify({"error": "Weekly summary not found. Please run the pipeline first."}), 404
            
        with open(data_path, 'r') as f:
            data = json.load(f)
            
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ceo-summary', methods=['GET'])
def get_ceo_summary():
    try:
        file_path = os.path.join(DATA_DIR, 'ceo_summary.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({"error": "CEO summary not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-week', methods=['POST'])
def process_week():
    try:
        from pipeline import DataPipeline
        # Assuming app.py is in backend/ and pipeline.py is in backend/
        # BASE_DIR is backend/
        # pipeline expects base_dir to be the project root (SMU/)
        project_root = os.path.dirname(BASE_DIR)
        pipeline = DataPipeline(project_root)
        pipeline.run()
        return jsonify({"message": "Week processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

