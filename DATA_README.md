# 📊 Dataset Overview

This project uses a dataset focused on **Employee Burnout & Performance Analysis**.

## Source File
*   **Path:** `zzzz_Burnout/test.csv`
*   **Rows:** ~12,000 employees (Processed in batches for the dashboard)

## Data Columns

| Column Name | Description |
| :--- | :--- |
| **Employee ID** | Unique identifier for each employee (e.g., `fffe3200...`). |
| **Date of Joining** | The date the employee started working. |
| **Gender** | Male / Female. |
| **Company Type** | `Service` or `Product` based company. |
| **WFH Setup Available** | `Yes` / `No` - Does the employee have a work-from-home setup? |
| **Designation** | Seniority level (0.0 - 5.0). Higher means more senior. |
| **Resource Allocation** | Workload score (1.0 - 10.0). Higher means more hours/projects. |
| **Mental Fatigue Score** | Self-reported fatigue level (0.0 - 10.0). |

## Derived Metrics (Calculated by Pipeline)
*   **Burnout Rate:** Predicted score (0.0 - 1.0) using a Regression Model based on the features above.
*   **Names:** Mock names are generated for the dashboard (localized to Tunisian context).
