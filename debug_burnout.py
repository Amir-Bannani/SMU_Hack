import pandas as pd
import os
import sys
import pickle
from sklearn.preprocessing import LabelEncoder

# Add backend to path
sys.path.append(os.path.abspath('backend'))
from models.burnout import BurnoutModel

def debug_prediction():
    print("Debugging Burnout Prediction...")
    
    # Load Data
    csv_path = "backend/data/processed_history.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded data with {len(df)} rows.")
    print("Columns:", df.columns.tolist())
    
    # Load Model
    model_path = "zzzz_Burnout/model_file.pkl"
    print(f"Loading model from {model_path}...")
    
    try:
        model = BurnoutModel(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Try Prediction (this should trigger the error if any)
    print("\nAttempting prediction...")
    try:
        # We need to simulate what pipeline does (ensure columns exist)
        # pipeline ensures 'Difficulty Work Score' is present.
        if 'Difficulty Work Score' not in df.columns:
             # Simulate calculation if missing (though processed_history should have it)
             df['Difficulty Work Score'] = 5.0 
        
        # Call predict directly to see the error
        # We bypass the try-except in the class method if possible, or just rely on print
        # Actually, let's instantiate the class and call predict, but since the class has a try-except block that returns 0.5,
        # we might not see the error unless we modify the class or copy the logic here.
        
        # Let's copy the logic to see the raw error
        data = df.copy()
        
        # Preprocessing logic from burnout.py
        cols_to_drop = ['Employee ID', 'Date of Joining', 'Name']
        data.drop([c for c in cols_to_drop if c in data.columns], axis=1, inplace=True)

        cat_features = ['Gender', 'Company Type', 'WFH Setup Available']
        for cat in cat_features:
            if cat in data.columns:
                le = LabelEncoder()
                data[cat] = le.fit_transform(data[cat])
        
        print("Data prepared for prediction. Columns:", data.columns.tolist())
        
        # Raw prediction using the loaded pickle model
        if model.model:
            preds = model.model.predict(data)
            print("Prediction successful:", preds[:5])
        else:
            print("Model object is None.")
            
    except Exception as e:
        print(f"\nCAUGHT EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_prediction()
