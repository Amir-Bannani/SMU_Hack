

https://github.com/user-attachments/assets/9d1926c7-88af-454f-b671-08f01e3bbb76

# Responsible Leadership System

A hackathon project designed to help companies practice responsible leadership by detecting burnout, workload inequity, and bias using AI-driven analytics.

## 🚀 New Features Added

We have transformed the initial concept into a working MVP with the following core components:

### 1. Data Simulator (`backend/simulator.py`)
Instead of relying on static mock data, we now generate realistic synthetic data for:
- **HR Data**: Work hours, tenure, promotion history.
- **Feedback**: Employee satisfaction scores, manager ratings.
- **Task Management**: Jira/Notion-style tasks with statuses, deadlines, and time spent.

### 2. Analytics Engine (`backend/analytics.py`)
A dedicated engine that processes the simulated data to generate actionable insights:
- **🔥 Burnout Risk Model**: Calculates a risk score (0-100) based on excessive work hours (>50h), low feedback scores, and missed deadlines.
- **⚖️ Workload Equity Algorithm**: Analyzes the distribution of work hours across the team to detect imbalances.
- **⚠️ Bias Detection**: Identifies potential bias by comparing objective performance (task completion rates) with subjective manager ratings.

### 3. Enhanced Manager Dashboard
The frontend has been updated to visualize these insights:
- **Risk Indicators**: Color-coded bars showing burnout risk for each employee.
- **Equity Charts**: Visual breakdown of who is doing the most work.
- **Bias Alerts**: Automatic flags for high-performers with low manager ratings.

## 🛠️ How to Run

### Backend
```bash
cd backend
# Activate virtual environment
.\venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Run the server
python app.py
```

### Frontend
```bash
cd frontend
# Install dependencies
npm install
# Run the dev server
npm run dev
```

## 🏗️ Architecture
`Simulator` -> `Analytics Engine` -> `Flask API` -> `React Dashboard`
