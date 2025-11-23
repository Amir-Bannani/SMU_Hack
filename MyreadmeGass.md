Great — now that the project is clearer, I can give you **the exact database structure you need** for a weekly-updated IT employee monitoring + workload balance + AI insights dashboard.

Your system has **4 core goals**:

1. Track employees’ weekly work data **per project**
2. Detect:

   * uneven workload
   * skills mismatch
   * potential burnout/stress risk (AI indicator, not medical)
3. Provide manager dashboard + statistics
4. Provide weekly LLM insights + advice
5. Compare current week vs previous week → **see improvement**

To achieve this, your database must allow:

✔ time-series data (weekly logs)
✔ per-project granularity
✔ per-employee data
✔ AI-generated metrics
✔ insights history

---

# ✅ **Perfect Database Structure for Your Project**

Below is the **exact schema** tailored for your idea.

---

# 🗂 **1. `employees` Table**

Basic info about each employee.

| Column         | Type           | Why                      |
| -------------- | -------------- | ------------------------ |
| id             | INT (PK)       | unique                   |
| full_name      | VARCHAR        | display name             |
| role           | VARCHAR        | e.g. backend dev         |
| primary_skills | VARCHAR / JSON | for skill-match analysis |
| email          | VARCHAR        | internal communication   |
| active         | BOOLEAN        | current employee         |

---

# 🗂 **2. `projects` Table**

| Column      | Type                  |
| ----------- | --------------------- |
| id          | INT                   |
| name        | VARCHAR               |
| description | TEXT                  |
| manager_id  | INT (FK to employees) |
| start_date  | DATE                  |
| end_date    | DATE                  |

---

# 🗂 **3. `employee_project_assignment` Table**

Because one employee can work on several projects.

| Column          | Type           |
| --------------- | -------------- |
| id              | INT            |
| employee_id     | INT FK         |
| project_id      | INT FK         |
| role_in_project | VARCHAR        |
| assigned_since  | DATE           |
| expected_skills | VARCHAR / JSON |

This table is **super important** for skill mismatch analysis.

---

# 🗂 **4. `weekly_logs` Table (The Heart of the System)**

Every week, the manager uploads or the system receives fresh logs per employee per project.

| Column                | Type    | Purpose                       |
| --------------------- | ------- | ----------------------------- |
| id                    | INT     |                               |
| employee_id           | INT FK  |                               |
| project_id            | INT FK  |                               |
| week_start            | DATE    | identifies the week           |
| tasks_completed       | INT     | productivity                  |
| hours_worked          | FLOAT   | workload tracking             |
| reported_difficulties | TEXT    | qualitative data              |
| tech_used             | VARCHAR | compare with expertise        |
| avg_task_complexity   | INT     | skill usage                   |
| workload_score        | FLOAT   | normalized workload index     |
| skill_match_score     | FLOAT   | 0–1 (AI-calculated)           |
| burnout_risk_score    | FLOAT   | AI-calculated but NOT medical |
| notes                 | TEXT    | human comments                |

This table enables:

* uneven workload detection
* skills mismatch detection
* burnout/stress risk detection
* weekly comparisons
* charts

---

# 🗂 **5. `weekly_insights` Table (LLM Output)**

The LLM generates weekly insights per project.

| Column             | Type |                                |
| ------------------ | ---- | ------------------------------ |
| id                 | INT  |                                |
| project_id         | INT  |                                |
| week_start         | DATE |                                |
| insights_text      | TEXT | suggestions, risk analysis     |
| recommendations    | TEXT | improvement plan               |
| detected_anomalies | JSON | uneven workload, mismatch, etc |

---

# 🗂 **6. `improvement_tracking` Table**

Compare insights week over week.

| Column       | Type    |                       |
| ------------ | ------- | --------------------- |
| id           | INT     |                       |
| project_id   | INT     |                       |
| week_start   | DATE    |                       |
| metric_name  | VARCHAR | e.g. workload_balance |
| before_value | FLOAT   |                       |
| after_value  | FLOAT   |                       |
| improved     | BOOLEAN |                       |

This allows the dashboard to show:

* ✔ did the manager’s changes work?
* ✔ did the workload become more balanced?
* ✔ did burnout risk reduce?

---

# 🗂 **7. `tasks_distribution` Table** (Optional but useful)

| Column      | Type                                  |
| ----------- | ------------------------------------- |
| id          | INT                                   |
| employee_id | INT                                   |
| project_id  | INT                                   |
| week_start  | DATE                                  |
| task_type   | VARCHAR (‘backend’, ‘design’, ‘data’) |
| task_hours  | FLOAT                                 |

This helps detect:

* employees doing work outside their specialty
* unfair task distribution
* overloading junior staff

---

# 🎯 **How the Workflow Happens (Full Pipeline)**

### **1️⃣ Weekly logs arrive (CSV/Excel/API/manual)**

→ Insert into `weekly_logs`.

### **2️⃣ AI runs analysis**

* uneven workload
* skill mismatch
* burnout risk
* anomalies

Updates `weekly_logs` with calculated scores.

### **3️⃣ LLM generates insights**

Stored in `weekly_insights`.

### **4️⃣ Dashboard updates**

React fetches data from Flask API:

* charts
* pie charts
* workload distribution
* risk indicators
* recommendations

### **5️⃣ Next week arrives**

You compare results using:

* `weekly_logs` (week n vs week n-1)
* `improvement_tracking`

Manager sees:

📉 “Burnout risk for Ali improved by 23%.”
📈 “Skill match improved for Youssef.”
⚠ “Uneven workload increased again.”

---

# ⭐ If You Want, I Can Generate:

✔ SQL code for all tables
✔ Full ER diagram
✔ API endpoints (Flask)
✔ React dashboard structure
✔ AI pipeline architecture
✔ Weekly automation script

Just tell me what you want next.
