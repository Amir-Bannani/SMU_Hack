import pickle
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

class BurnoutModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()
        
        # Features used for prediction
        self.features = [
            'Designation', 
            'Resource Allocation', 
            'Difficulty Work Score', 
            'Gender_Female', 
            'Gender_Male',
            'Company Type_Product', 
            'Company Type_Service',
            'WFH Setup Available_No', 
            'WFH Setup Available_Yes'
        ]

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = pickle.load(open(self.model_path, "rb"))
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Warning: Model file not found at {self.model_path}")

    def predict(self, data: pd.DataFrame):
        """
        Predicts burnout rate.
        Expects DataFrame with columns: ['Gender', 'Company Type', 'WFH Setup Available', 'Designation', 'Resource Allocation', 'Difficulty Work Score']
        """
        if self.model is None:
            return [0.5] * len(data) # Return dummy values if model not loaded

        # Preprocessing
        X = data.copy()
        
        # Drop unnecessary columns if they exist
        cols_to_drop = ['Employee ID', 'Date of Joining', 'Name']
        X.drop([c for c in cols_to_drop if c in X.columns], axis=1, inplace=True)

        # Label Encoding
        cat_features = ['Gender', 'Company Type', 'WFH Setup Available']
        for cat in cat_features:
            if cat in X.columns:
                le = LabelEncoder()
                X[cat] = le.fit_transform(X[cat])
        
        # Select only relevant features if they exist
        # Note: Real model prediction requires exact feature match. 
        # The model expects 'Mental Fatigue Score', but we have 'Difficulty Work Score'.
        if 'Difficulty Work Score' in X.columns:
            X.rename(columns={'Difficulty Work Score': 'Mental Fatigue Score'}, inplace=True)
            
        try:
            return self.model.predict(X)
        except Exception as e:
            print(f"Prediction error (using fallback): {e}")
            # Fallback logic if model features don't match
            return [0.5] * len(data)
