# 🗄️ Database Modeling (Single Project Architecture)

Since we are focusing on a **Single Project** (e.g., "Project Phoenix"), the schema is simplified to focus on depth of data for that one project.

## 1. `employees` Table
*The team members working on this project.*

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT (PK) | Unique Employee ID |
| `full_name` | VARCHAR | Name (e.g., "Sarah Connor") |
| `role` | VARCHAR | Job Title (e.g., "Backend Dev") |
| `primary_skills` | JSON | List of core skills (e.g., `["Python", "SQL"]`) |
| `active` | BOOLEAN | Is currently on the team? |

## 2. `project` Table
*The single project being tracked.*

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT (PK) | Unique Project ID (e.g., 1) |
| `name` | VARCHAR | Project Name (e.g., "Project Phoenix") |
| `description` | TEXT | Goal of the project |
| `start_date` | DATE | When it started |

## 3. `weekly_logs` Table
*The core time-series data. One row per employee per week.*

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT (PK) | Unique Log ID |
| `employee_id` | INT (FK) | Links to `employees` |
| `project_id` | INT (FK) | Links to `project` |
| `week_start` | DATE | The Monday of the week (e.g., "2023-10-23") |
| `hours_worked` | FLOAT | Total hours logged |
| `tasks_completed` | INT | Number of tasks finished |
| `tech_used` | JSON | Tech stack used this week (e.g., `["Python", "Legacy Code"]`) |
| `reported_difficulties` | TEXT | Blocker/Stress feedback |
| **`skill_match_score`** | FLOAT | **AI Metric**: 0.0 - 1.0 (Alignment of `tech_used` vs `primary_skills`) |
| **`workload_score`** | FLOAT | **AI Metric**: Normalized workload index |
| **`burnout_risk_score`** | FLOAT | **AI Metric**: 0-100 Risk Score |

## 4. `weekly_insights` Table
*AI-generated summary for the project for a specific week.*

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT (PK) | Unique Insight ID |
| `project_id` | INT (FK) | Links to `project` |
| `week_start` | DATE | The week being analyzed |
| `insights_text` | TEXT | LLM-generated summary |
| `recommendations` | TEXT | Actionable advice for the manager |
| `anomalies_detected` | JSON | Count of high-risk employees, etc. |

---

## 🔗 Relationships
- **One** Project has **Many** Employees.
- **One** Employee has **Many** Weekly Logs (History).
- **One** Project has **Many** Weekly Insights (History).
