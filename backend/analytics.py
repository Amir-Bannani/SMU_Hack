import os
import json
import pandas as pd
import numpy as np

class CEOAnalytics:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, 'backend', 'data')
        self.archive_dir = os.path.join(self.data_dir, 'archive')
        
    def generate_ceo_report(self):
        print("Generating CEO Report...")
        
        # 1. Load all weekly summaries
        weeks = []
        if os.path.exists(self.archive_dir):
            files = [f for f in os.listdir(self.archive_dir) if f.startswith("week_") and f.endswith(".json")]
            # Sort by week index
            files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
            
            for f in files:
                with open(os.path.join(self.archive_dir, f), 'r') as file:
                    data = json.load(file)
                    # Extract week index from filename or data
                    week_idx = int(f.split("_")[1].split(".")[0])
                    data['week_index'] = week_idx
                    weeks.append(data)
        
        if not weeks:
            print("No weekly data found for CEO report.")
            return
            
        # 2. Calculate Trends
        trend_weeks = []
        trend_burnout = []
        trend_fatigue = []
        trend_equity = []
        
        latest_week = weeks[-1]
        
        for week in weeks:
            week_label = f"Week {week['week_index']}"
            employees = week.get('burnout_analysis', [])
            df = pd.DataFrame(employees)
            
            if not df.empty:
                avg_burnout = df['Burnout Rate'].mean()
                avg_fatigue = df['Difficulty Work Score'].mean()
                
                # Workload Equity: Std Dev of Resource Allocation (if available)
                # We need to look up Resource Allocation. It might not be in burnout_analysis dict directly 
                # if we didn't save it there.
                # Let's check pipeline.py: 
                # "burnout_analysis": df[['Employee ID', 'Name', 'Burnout Rate', 'Difficulty Work Score']].to_dict(orient='records')
                # It seems we didn't save Resource Allocation in the summary JSON.
                # We should probably load the CSV for full details or update pipeline to save it.
                # For now, let's try to load the corresponding CSV if needed, OR update pipeline.
                # Actually, let's assume we update pipeline to include it, or we load CSV.
                # Loading CSV is safer for now.
                
                csv_path = os.path.join(self.archive_dir, f"week_{week['week_index']}.csv")
                if os.path.exists(csv_path):
                    df_full = pd.read_csv(csv_path)
                    equity_score = df_full['Resource Allocation'].std()
                else:
                    equity_score = 0
                
                trend_weeks.append(week_label)
                trend_burnout.append(round(avg_burnout, 2))
                trend_fatigue.append(round(avg_fatigue, 2))
                trend_equity.append(round(equity_score, 2))
        
        # 3. Calculate Manager Metrics (Evolution)
        # Compare Latest vs Previous
        if len(weeks) > 1:
            prev_week = weeks[-2]
            prev_burnout = trend_burnout[-2]
            curr_burnout = trend_burnout[-1]
            burnout_mitigation = round(prev_burnout - curr_burnout, 3) # Positive means improvement
        else:
            burnout_mitigation = 0.0
            
        # Retention Risk (Current)
        current_employees = pd.DataFrame(latest_week.get('burnout_analysis', []))
        critical_count = (current_employees['Burnout Rate'] > 0.7).sum()
        retention_risk = round((critical_count / len(current_employees)) * 100, 1) if not current_employees.empty else 0
        
        # 4. Construct CEO JSON
        ceo_data = {
            "timestamp": latest_week.get('timestamp', ''), # We might need to add timestamp to weekly_summary
            "manager_performance": {
                "workload_equity": trend_equity[-1] if trend_equity else 0,
                "burnout_mitigation": burnout_mitigation,
                "retention_risk": f"{retention_risk}%",
                "team_size": len(current_employees)
            },
            "trends": {
                "weeks": trend_weeks,
                "burnout": trend_burnout,
                "fatigue": trend_fatigue,
                "equity": trend_equity
            },
            "latest_week_id": latest_week.get('week_id', 'Unknown')
        }
        
        output_file = os.path.join(self.data_dir, 'ceo_summary.json')
        with open(output_file, 'w') as f:
            json.dump(ceo_data, f, indent=2)
            
        print(f"CEO Report generated: {output_file}")

if __name__ == "__main__":
    # Test
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Go up to SMU/
    analytics = CEOAnalytics(base_path)
    analytics.generate_ceo_report()
