import random
from datetime import datetime, timedelta

class Simulator:
    def __init__(self):
        self.employees = self.generate_employees()
        self.projects = self.generate_projects()
        self.assignments = self.assign_employees()
        self.weekly_logs = self.generate_weekly_logs()

    def generate_employees(self):
        roles = ['Backend Dev', 'Frontend Dev', 'Data Scientist', 'Designer', 'DevOps']
        skills_pool = {
            'Backend Dev': ['Python', 'SQL', 'Flask', 'Django'],
            'Frontend Dev': ['React', 'JavaScript', 'CSS', 'TypeScript'],
            'Data Scientist': ['Python', 'Pandas', 'Machine Learning', 'SQL'],
            'Designer': ['Figma', 'UI/UX', 'CSS'],
            'DevOps': ['Docker', 'Kubernetes', 'AWS', 'CI/CD']
        }
        
        employees = []
        names = ["Sarah", "Mike", "Ali", "Youssef", "Jessica", "David", "Emily", "Kevin"]
        
        for i, name in enumerate(names):
            role = random.choice(roles)
            employees.append({
                "id": i + 1,
                "full_name": name,
                "role": role,
                "primary_skills": skills_pool[role],
                "email": f"{name.lower()}@company.com",
                "active": True
            })
        return employees

    def generate_projects(self):
        # Single Project Mode
        projects = [
            {"id": 101, "name": "Project Phoenix", "description": "Next-gen AI Platform", "manager_id": 1}
        ]
        return projects

    def assign_employees(self):
        assignments = []
        assign_id = 1
        # Assign ALL employees to the single project
        project = self.projects[0]
        
        for emp in self.employees:
            assignments.append({
                "id": assign_id,
                "employee_id": emp['id'],
                "project_id": project['id'],
                "role_in_project": emp['role'],
                "assigned_since": (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')
            })
            assign_id += 1
        return assignments

    def generate_weekly_logs(self):
        logs = []
        log_id = 1
        weeks = 4 # Generate data for last 4 weeks
        
        today = datetime.now()
        # Find the most recent Monday
        start_of_week = today - timedelta(days=today.weekday())
        
        for i in range(weeks):
            week_date = (start_of_week - timedelta(weeks=i)).strftime('%Y-%m-%d')
            
            for assignment in self.assignments:
                emp = next(e for e in self.employees if e['id'] == assignment['employee_id'])
                
                # Simulate data
                hours = random.uniform(20, 55) # Normal is ~40
                tasks = random.randint(2, 10)
                complexity = random.randint(1, 5)
                
                # Tech used: mix of primary skills and random others (to simulate mismatch)
                if random.random() > 0.2:
                    tech_used = random.sample(emp['primary_skills'], k=min(2, len(emp['primary_skills'])))
                else:
                    tech_used = ["Legacy Code", "Manual Entry"] # Mismatch examples
                
                logs.append({
                    "id": log_id,
                    "employee_id": emp['id'],
                    "project_id": assignment['project_id'],
                    "week_start": week_date,
                    "tasks_completed": tasks,
                    "hours_worked": round(hours, 1),
                    "reported_difficulties": random.choice(["None", "Unclear requirements", "Technical debt", "Too many meetings"]) if random.random() > 0.7 else "None",
                    "tech_used": tech_used,
                    "avg_task_complexity": complexity,
                    "notes": "Weekly update"
                })
                log_id += 1
                
        return logs

    def get_all_data(self):
        return {
            "employees": self.employees,
            "projects": self.projects,
            "assignments": self.assignments,
            "weekly_logs": self.weekly_logs
        }
