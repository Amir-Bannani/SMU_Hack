import pandas as pd
import json
import os
import sys
import random
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Add project root directory to path (for LLM.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.burnout import BurnoutModel
from models.difficulty import DifficultyAnalyzer
from models.underperformance import UnderperformanceDetector, EmployeeMetrics
from LLM import get_gemini_insights

class DataPipeline:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.models_dir = os.path.join(base_dir, 'backend', 'models')
        self.data_dir = os.path.join(base_dir, 'zzzz_Burnout') # Assuming input CSV is here
        
        # Initialize Models
        self.burnout_model = BurnoutModel(os.path.join(self.data_dir, "model_file.pkl"))
        
        # Initialize Difficulty Analyzer (Mocking training for now or loading if exists)
        self.difficulty_analyzer = DifficultyAnalyzer()
        # Ideally load a trained model: self.difficulty_analyzer.load_model(os.path.join(self.models_dir, 'difficulty_model.pkl'))
        # For demo, we might need to train it quickly or assume it's loaded. 
        # Let's assume we can use it to predict if we had a model. 
        # Since we don't have a saved model file in the new location yet, we might need to skip actual prediction 
        # or use a dummy score if model not found.
        
        self.underperformance_detector = UnderperformanceDetector()

    def generate_mock_report(self, row):
        """Generate a mock weekly report based on numerical data for demo purposes."""
        # Logic to make report consistent with data
        if row['Resource Allocation'] > 7:
            return "Heavy workload this week. Managed to complete most tasks but feeling drained."
        elif row['Resource Allocation'] < 3:
            return "Light week. Waiting for new assignments. Used time for learning."
        else:
            return "Steady progress. No major blockers."

    def process_weekly_data(self, csv_path, week_id):
        print(f"Processing {csv_path} for Week {week_id}...")
        df = pd.read_csv(csv_path)
        
        # DEMO MODE: Limit to 12 employees
        df = df.head(12)
        print("DEMO MODE: Restricted to first 12 employees.")
        
        # 1. Difficulty Score (Mental Fatigue Proxy)
        # Since we don't have actual text reports in CSV, we mock them or use existing Fatigue score if present.
        # The user said "zzzz_calculate_score that will calculate work_difficuly_score".
        # If 'Mental Fatigue Score' is in CSV, we use it. If not, we might need to calculate it.
        # The provided CSV format: Employee ID,Date of Joining,Gender,Company Type,WFH Setup Available,Designation,Resource Allocation
        # It MISSES 'Mental Fatigue Score'. So we MUST calculate it using DifficultyAnalyzer.
        
        if 'Difficulty Work Score' not in df.columns:
            print("Calculating Difficulty Work Score...")
            reports = df.apply(self.generate_mock_report, axis=1).tolist()
            
            # In a real scenario, we'd use self.difficulty_analyzer.predict(reports)
            # For this demo, let's generate a score 0-10 based on Resource Allocation + Randomness
            # to simulate the model's output.
            # mock_scores = self.difficulty_analyzer.predict(reports) # This would return 0,1,2... classes.
            # Let's simulate a continuous score 0.0-10.0
            df['Difficulty Work Score'] = df['Resource Allocation'].apply(lambda x: min(10, max(0, x * 0.8 + random.uniform(-1, 2))))
        
        # 2. Burnout Prediction
        print("Predicting Burnout Risk...")
        # BurnoutModel expects specific columns.
        # We need to ensure 'Difficulty Work Score' is present (we just added it).
        burnout_preds = self.burnout_model.predict(df)
        df['Burnout Rate'] = burnout_preds

        # 3. Underperformance Detection
        print("Detecting Underperformance...")
        
        # Generate Tunisian Names for Demo
        first_names = ["Ahmed", "Mohamed", "Youssef", "Aziz", "Mehdi", "Amine", "Bilel", "Walid", "Sami", "Karim", "Mariem", "Sarah", "Fatma", "Nour", "Yasmine", "Hela", "Chiraz", "Rania", "Salma", "Ines"]
        last_names = ["Ben Ali", "Trabelsi", "Gharbi", "Dridi", "Mejri", "Jaziri", "Hammami", "Ayari", "Riahi", "Oueslati", "Zarrouk", "Mabrouk", "Sassi", "Bouazizi", "Khemiri"]
        
        # Create a mapping of ID to Name
        id_to_name = {}
        for emp_id in df['Employee ID'].unique():
            id_to_name[emp_id] = f"{random.choice(first_names)} {random.choice(last_names)}"
            
        employees_metrics = []
        for _, row in df.iterrows():
            emp_name = id_to_name.get(row['Employee ID'], f"Employee {row['Employee ID']}")
            emp = EmployeeMetrics(
                employee_id=row['Employee ID'],
                name=emp_name, 
                resource_allocation=row['Resource Allocation'],
                fatigue_score=row['Difficulty Work Score'],
                designation=row['Designation']
            )
            employees_metrics.append(emp)
        
        team_report = self.underperformance_detector.analyze_team(employees_metrics)
        
        # 4. LLM Insights
        print("Generating AI Insights...")
        # Prepare data for LLM
        burnout_map = dict(zip(df['Employee ID'], df['Burnout Rate']))
        
        # Filter data to avoid token limits (1M+ tokens is too much)
        # Prioritize CRITICAL and WARNING cases
        all_individuals = team_report['individuals']
        critical_cases = [i for i in all_individuals if i['severity'] == 'CRITICAL']
        warning_cases = [i for i in all_individuals if i['severity'] == 'WARNING']
        other_cases = [i for i in all_individuals if i['severity'] not in ['CRITICAL', 'WARNING']]
        
        # Select top 50 critical, 30 warning, and 20 others for context
        selected_individuals = critical_cases[:50] + warning_cases[:30] + other_cases[:20]
        
        print(f"Sending {len(selected_individuals)} employee records to Gemini (downsampled from {len(all_individuals)})...")
        insights = get_gemini_insights(selected_individuals, burnout_map)
        
        # 5. Save Outputs
        output_dir = os.path.join(self.base_dir, 'backend', 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        # CEO Dashboard Data
        ceo_data = {
            "timestamp": datetime.now().isoformat(),
            "total_employees": len(df),
            "avg_burnout": float(df['Burnout Rate'].mean()),
            "avg_fatigue": float(df['Difficulty Work Score'].mean()),
            "high_risk_count": int((df['Burnout Rate'] > 0.7).sum()),
            "project_health": "Good" if df['Burnout Rate'].mean() < 0.5 else "At Risk"
        }
        with open(os.path.join(output_dir, 'ceo.json'), 'w') as f:
            json.dump(ceo_data, f, indent=2)
            
        # Weekly Summary Data
        # Add names to df for export
        df['Name'] = df['Employee ID'].map(id_to_name)
        
        weekly_summary = {
            "week_id": f"Week {week_id}",
            "burnout_analysis": df[['Employee ID', 'Name', 'Burnout Rate', 'Difficulty Work Score']].to_dict(orient='records'),
            "underperformance_report": team_report,
            "ai_insights": insights
        }
        with open(os.path.join(output_dir, 'weekly_summary.json'), 'w') as f:
            json.dump(weekly_summary, f, indent=2)
            
        print("✓ Pipeline completed. Data saved to backend/data/")

    def run(self):
        print("Starting Pipeline Run...")
        # Define paths
        data_dir = os.path.join(self.base_dir, "backend", "data")
        archive_dir = os.path.join(data_dir, "archive")
        input_csv = os.path.join(data_dir, "new_week_input.csv")
        history_csv = os.path.join(data_dir, "processed_history.csv")
        
        # Ensure archive dir exists
        os.makedirs(archive_dir, exist_ok=True)
        
        # Determine Next Week ID
        existing_weeks = [f for f in os.listdir(archive_dir) if f.startswith("week_") and f.endswith(".json")]
        week_indices = [int(f.split("_")[1].split(".")[0]) for f in existing_weeks]
        next_week_id = max(week_indices) + 1 if week_indices else 0
        
        print(f"Current Week Index: {next_week_id}")
        
        target_file = None
        is_new_data = False
        
        # Check New Input
        if os.path.exists(input_csv):
            try:
                df_input = pd.read_csv(input_csv)
                if len(df_input) > 0:
                    print(f"Found NEW data in {input_csv}. Processing as Week {next_week_id}...")
                    target_file = input_csv
                    is_new_data = True
                else:
                    print(f"Input file {input_csv} is empty.")
            except Exception as e:
                print(f"Error reading input file: {e}")

        # Fallback to History (Week 0 Initialization)
        if target_file is None:
            if next_week_id == 0:
                print(f"No previous history found. Initializing Week 0 from {history_csv}...")
                if os.path.exists(history_csv):
                    target_file = history_csv
                    is_new_data = True # Treat as new since it's the first init
                else:
                    print(f"Critical: {history_csv} not found.")
            else:
                print("No new input data found. Dashboard is up to date.")
                
        if target_file and is_new_data:
            # Process Data
            self.process_weekly_data(target_file, next_week_id)
            
            # Move/Copy artifacts to Archive and Versioned History
            # 1. Save as processed_history_week{N}.csv
            import shutil
            versioned_history = os.path.join(data_dir, f"processed_history_week{next_week_id}.csv")
            shutil.copy(target_file, versioned_history)
            print(f"Saved versioned history: {versioned_history}")
            
            # 2. Also copy to archive (redundant but safe)
            shutil.copy(target_file, os.path.join(archive_dir, f"week_{next_week_id}.csv"))
            
            # 2. Copy JSON Summary
            src_json = os.path.join(data_dir, "weekly_summary.json")
            dst_json = os.path.join(archive_dir, f"week_{next_week_id}.json")
            if os.path.exists(src_json):
                shutil.copy(src_json, dst_json)
                print(f"Archived Week {next_week_id} data to {archive_dir}")
                
            # 3. If it was new input, clear it
            if target_file == input_csv:
                 # Clear input file for next week
                 with open(input_csv, 'w') as f:
                     f.write("Employee ID,Date of Joining,Gender,Company Type,WFH Setup Available,Designation,Resource Allocation,Difficulty Work Score\n")
                 print("Cleared new_week_input.csv for next use.")
                 
        # 4. Generate CEO Report (Always run)
        from analytics import CEOAnalytics
        analytics = CEOAnalytics(self.base_dir)
        analytics.generate_ceo_report()

if __name__ == "__main__":
    # Example Usage
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up to SMU/
    pipeline = DataPipeline(base_path)
    pipeline.run()
