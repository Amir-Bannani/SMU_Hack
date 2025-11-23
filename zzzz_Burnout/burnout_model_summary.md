# Burnout Prediction Model Analysis
**Source:** `SAP_burnout_modelling1.ipynb`

## Model Selection
- **Model Used:** Linear Regression (`sklearn.linear_model.LinearRegression`)
- **Library:** Scikit-learn

## Target Variable
- **Label:** `Burn Rate` (Float, 0.0 - 1.0)

## Input Features
The model uses the following features to predict burnout:
1.  **Designation** (Numeric: 0.0 - 5.0)
2.  **Resource Allocation** (Numeric: 1.0 - 10.0)
3.  **Mental Fatigue Score** (Numeric: 0.0 - 10.0)
4.  **Gender** (Categorical, Label Encoded: 0/1)
5.  **Company Type** (Categorical, Label Encoded: 0/1)
6.  **WFH Setup Available** (Categorical, Label Encoded: 0/1)

*Note: `Employee ID`, `Date of Joining`, and `Experience` were dropped during preprocessing.*

## Data Preprocessing
- **Missing Values:**
    - `Resource Allocation` and `Mental Fatigue Score`: Filled with Median.
    - `Burn Rate`: Rows with missing target values were dropped.
- **Encoding:** Label Encoding used for categorical features (`Gender`, `Company Type`, `WFH Setup Available`).
- **Splitting:**
    - Train/Test Split: 80% Train, 20% Test.
    - Validation Split: Further 75%/25% split on Training data.

## Model Performance
Performance metrics on the Validation Set:
- **Accuracy (R-squared):** ~91.30%
- **Mean Absolute Error (MAE):** ~0.0478
- **Mean Squared Error (MSE):** ~0.0034

## Key Insights
- **High Correlation:** `Mental Fatigue Score` and `Resource Allocation` are highly correlated with `Burn Rate`.
- **Sector Impact:** Service sector employees appear slightly more prone to burnout than Product sector employees.
- **Experience:** Higher designation and resource allocation correlate with higher burnout risk.












Now, the EDA part is over. Let's summarize by writing some points about the dataset:


1.   Irrespective of gender, employees in service sector are prone to higher burn rates.
2.   Employees with higher mental fatigue scores are having proportinally higher burn rates.
3.   Employees at higher designation allocate more resources and hence have higher burn rate.
4.   At every level of designation and resource allocation, employees who don't have WFH setup available are suffering from higher burn rates.

Let's see the correlation matrix to see correlations between fields.





