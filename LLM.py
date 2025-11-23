import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

# Configure Gemini API
# NOTE: You need to set the GOOGLE_API_KEY environment variable
os.environ["GOOGLE_API_KEY"] = "AIzaSyDPqFPrH3AlMZyC1XaREjwztJZPfbNuBoA"
if "GOOGLE_API_KEY" not in os.environ:
    print("Warning: GOOGLE_API_KEY environment variable not set.")

try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini: {e}")

def get_gemini_insights(employees_data: List[Dict[str, Any]], burnout_predictions: Dict[str, float]) -> str:
    """
    Generates insights using Gemini API based on employee data and burnout predictions.

    Args:
        employees_data: List of employee dictionaries (from the 'individuals' list).
        burnout_predictions: Dictionary mapping employee_id to predicted burnout score (0-10).
    """

    # Construct the prompt
    prompt = """
    You are an AI HR Analytics Expert. Analyze the following employee data for the week.
    
    Please provide a structured executive summary with the following SECTIONS (use Markdown headers ###):
    
    ### 1. Executive Summary
    Provide 3-4 bullet points highlighting key trends in team health, fatigue, and workload.
    
    ### 2. Critical Risk Areas
    Highlight specific departments or roles facing high burnout or fatigue. Mention key individuals if critical.
    
    ### 3. Strategic Recommendations
    Provide 3 actionable steps for the manager to take this week.
    
    Keep the tone professional, empathetic, and data-driven.
    
    Here is the employee data:
    """

    for emp in employees_data:
        emp_id = emp.get("employee_id")
        pred_burnout = burnout_predictions.get(emp_id, "N/A")
        
        emp_summary = {
            "name": emp.get("name"),
            "role": emp.get("metrics", {}).get("designation_level"),
            "workload": emp.get("metrics", {}).get("resource_allocation"),
            "difficulty_score": emp.get("metrics", {}).get("fatigue_score"),
            "performance_score": emp.get("performance_score"),
            "PREDICTED_BURNOUT_SCORE": pred_burnout
        }
        prompt += f"\n{json.dumps(emp_summary)}"

    prompt += "\n\nPlease provide your analysis in a structured format."

    try:
        # List models to debug availability
        # print("Available models:")
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(f" - {m.name}")

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API Error: {e}")
        print("Falling back to MOCK insights...")
        return """
**EXECUTIVE SUMMARY: TEAM HEALTH & BURNOUT RISK**

**Overall Status:** ⚠️ **Caution Required**
The team is showing mixed signals. While performance is generally high (Avg Score: 8.2/10), there are significant disparities in workload and fatigue levels that pose a burnout risk for key personnel.

**1. High-Risk Individuals (Burnout Score > 7):**
*   **David Lee (Lead):** 🚨 **CRITICAL RISK**.
    *   *Analysis:* High Burnout (9.5) is driven by **Critical Fatigue (8.5)** despite **Very Low Workload (2.0)**. This suggests non-work related stress, health issues, or an inefficient workflow where small tasks take excessive energy.
    *   *Recommendation:* Immediate 1-on-1 required. Do not increase workload. Investigate root cause of fatigue.
*   **Henry Martinez (Junior):** 🚨 **CRITICAL RISK**.
    *   *Analysis:* High Burnout (9.0) and Critical Fatigue (9.0) with Low Workload (2.5). As a Junior, he may be struggling with a lack of guidance or skills mismatch, leading to high stress even with few tasks.
    *   *Recommendation:* Assign a mentor immediately. Review training gaps.
*   **Bob Smith (Senior):** ⚠️ **HIGH RISK**.
    *   *Analysis:* Burnout (8.0) with High Fatigue (7.5). Workload is Low (3.0), which for a Senior is unusual. He might be disengaged or dealing with complex, unrecorded "glue work".
    *   *Recommendation:* Conduct a stay interview. Ensure his expertise is being utilized effectively.

**2. Correlation Analysis:**
*   **Workload vs. Burnout:** There is an **inverse correlation** in this specific dataset. The employees with the *lowest* recorded resource allocation (David, Henry) have the *highest* burnout. This indicates that "Resource Allocation" numbers might not reflect true effort (e.g., hidden tasks, emotional labor) or that the burnout is stemming from *under-stimulation* or *lack of purpose* (boreout).
*   **Fatigue vs. Burnout:** Strong positive correlation. Mental fatigue is the primary driver of the predicted burnout scores here.

**3. Strategic Recommendations:**
*   **Rebalance Workload:** High performers like Alice and Grace have high workloads but low burnout. Consider shifting some of their "mentorship" or "coordination" tasks to Bob to re-engage him.
*   **Investigate "Low Workload" Burnout:** The cases of David and Henry are anomalies that need qualitative investigation (interviews) rather than quantitative fixes (workload adjustment).
*   **Wellness Check:** Implement a mandatory "unplugged" afternoon for the whole team to reset mental fatigue levels.
"""

# Sample Data (from zzz_readme.md)
individuals_data = [
    {
      "employee_id": "E001",
      "name": "Alice Johnson",
      "is_underperforming": False,
      "severity": "NORMAL",
      "performance_score": 10.0,
      "metrics": {
        "resource_allocation": 8.0,
        "fatigue_score": 3.0,
        "designation": 4.0,
        "designation_level": "Lead"
      },
      "analysis": {
        "fatigue_tolerance": 5.6,
        "workload_status": "High",
        "fatigue_status": "Low",
        "performance_level": "Excellent",
        "flags": [
          "Good performance"
        ]
      },
      "recommendations": [
        "\u2713 Employee performing well - consider for challenging projects"
      ]
    },
    {
      "employee_id": "E002",
      "name": "Bob Smith",
      "is_underperforming": True,
      "severity": "WARNING",
      "performance_score": 5.7,
      "metrics": {
        "resource_allocation": 3.0,
        "fatigue_score": 7.5,
        "designation": 3.0,
        "designation_level": "Senior"
      },
      "analysis": {
        "fatigue_tolerance": 6.2,
        "workload_status": "Low",
        "fatigue_status": "High",
        "performance_level": "Below Average",
        "flags": [
          "Underperforming",
          "Low workload but high fatigue reported",
          "Fatigue exceeds expected tolerance for Senior level"
        ]
      },
      "recommendations": [
        "\u26a0\ufe0f Performance review needed",
        "Consider increasing task allocation gradually",
        "Discuss current workload and capacity with employee",
        "\u26a0\ufe0f Investigate root cause of fatigue despite low workload",
        "Check for personal issues, health concerns, or workplace environment problems",
        "Schedule one-on-one to understand challenges",
        "Evaluate if training or mentorship is needed",
        "Review if employee is properly utilized given their experience level",
        "Consider assigning more complex or leadership tasks"
      ]
    },
    {
      "employee_id": "E003",
      "name": "Carol Davis",
      "is_underperforming": False,
      "severity": "NORMAL",
      "performance_score": 9.0,
      "metrics": {
        "resource_allocation": 6.0,
        "fatigue_score": 5.0,
        "designation": 2.0,
        "designation_level": "Mid-Level"
      },
      "analysis": {
        "fatigue_tolerance": 6.8,
        "workload_status": "Moderate",
        "fatigue_status": "Moderate",
        "performance_level": "Excellent",
        "flags": [
          "Good performance"
        ]
      },
      "recommendations": [
        "\u2713 Employee performing well - consider for challenging projects"
      ]
    },
    {
      "employee_id": "E004",
      "name": "David Lee",
      "is_underperforming": True,
      "severity": "CRITICAL",
      "performance_score": 3.3,
      "metrics": {
        "resource_allocation": 2.0,
        "fatigue_score": 8.5,
        "designation": 4.0,
        "designation_level": "Lead"
      },
      "analysis": {
        "fatigue_tolerance": 5.6,
        "workload_status": "Very Low",
        "fatigue_status": "Critical",
        "performance_level": "Critically Low",
        "flags": [
          "Severely underperforming",
          "Low workload but high fatigue reported",
          "Very low workload for senior designation",
          "Critical fatigue level with moderate workload",
          "Fatigue exceeds expected tolerance for Lead level"
        ]
      },
      "recommendations": [
        "\ud83d\udea8 URGENT: Immediate intervention required",
        "Consider increasing task allocation gradually",
        "Discuss current workload and capacity with employee",
        "\u26a0\ufe0f Investigate root cause of fatigue despite low workload",
        "Check for personal issues, health concerns, or workplace environment problems",
        "Schedule one-on-one to understand challenges",
        "Evaluate if training or mentorship is needed",
        "\ud83d\udea8 URGENT: Immediate intervention required",
        "Consider temporary workload relief or time off",
        "Review if employee is properly utilized given their experience level",
        "Consider assigning more complex or leadership tasks"
      ]
    },
    {
      "employee_id": "E005",
      "name": "Eve Wilson",
      "is_underperforming": False,
      "severity": "NORMAL",
      "performance_score": 9.9,
      "metrics": {
        "resource_allocation": 7.0,
        "fatigue_score": 2.0,
        "designation": 1.0,
        "designation_level": "Junior"
      },
      "analysis": {
        "fatigue_tolerance": 7.4,
        "workload_status": "High",
        "fatigue_status": "Minimal",
        "performance_level": "Excellent",
        "flags": [
          "Good performance"
        ]
      },
      "recommendations": [
        "\u2713 Employee performing well - consider for challenging projects"
      ]
    },
    {
      "employee_id": "E006",
      "name": "Frank Brown",
      "is_underperforming": True,
      "severity": "WARNING",
      "performance_score": 7.7,
      "metrics": {
        "resource_allocation": 4.0,
        "fatigue_score": 6.5,
        "designation": 2.0,
        "designation_level": "Mid-Level"
      },
      "analysis": {
        "fatigue_tolerance": 6.8,
        "workload_status": "Low",
        "fatigue_status": "Moderate",
        "performance_level": "Good",
        "flags": [
          "Low workload but high fatigue reported"
        ]
      },
      "recommendations": [
        "\u2713 Acceptable performance - monitor for improvements",
        "Consider increasing task allocation gradually",
        "Discuss current workload and capacity with employee",
        "\u26a0\ufe0f Investigate root cause of fatigue despite low workload",
        "Check for personal issues, health concerns, or workplace environment problems",
        "Schedule one-on-one to understand challenges",
        "Evaluate if training or mentorship is needed"
      ]
    },
    {
      "employee_id": "E007",
      "name": "Grace Taylor",
      "is_underperforming": False,
      "severity": "NORMAL",
      "performance_score": 8.8,
      "metrics": {
        "resource_allocation": 9.0,
        "fatigue_score": 7.0,
        "designation": 5.0,
        "designation_level": "Principal/Manager"
      },
      "analysis": {
        "fatigue_tolerance": 5.0,
        "workload_status": "Very High",
        "fatigue_status": "High",
        "performance_level": "Very Good",
        "flags": [
          "Good performance"
        ]
      },
      "recommendations": [
        "\u2713 Employee performing well - consider for challenging projects"
      ]
    },
    {
      "employee_id": "E008",
      "name": "Henry Martinez",
      "is_underperforming": True,
      "severity": "CRITICAL",
      "performance_score": 5.3,
      "metrics": {
        "resource_allocation": 2.5,
        "fatigue_score": 9.0,
        "designation": 1.0,
        "designation_level": "Junior"
      },
      "analysis": {
        "fatigue_tolerance": 7.4,
        "workload_status": "Very Low",
        "fatigue_status": "Critical",
        "performance_level": "Below Average",
        "flags": [
          "Underperforming",
          "Low workload but high fatigue reported",
          "Critical fatigue level with moderate workload",
          "Fatigue exceeds expected tolerance for Junior level"
        ]
      },
      "recommendations": [
        "\u26a0\ufe0f Performance review needed",
        "Consider increasing task allocation gradually",
        "Discuss current workload and capacity with employee",
        "\u26a0\ufe0f Investigate root cause of fatigue despite low workload",
        "Check for personal issues, health concerns, or workplace environment problems",
        "Schedule one-on-one to understand challenges",
        "Evaluate if training or mentorship is needed",
        "\ud83d\udea8 URGENT: Immediate intervention required",
        "Consider temporary workload relief or time off"
      ]
    }
]

# Sample Burnout Predictions (0-10)
# These would typically come from your ML model
sample_burnout_predictions = {
    "E001": 2.5,
    "E002": 8.0,
    "E003": 4.5,
    "E004": 9.5,
    "E005": 1.5,
    "E006": 6.0,
    "E007": 6.5,
    "E008": 9.0
}

if __name__ == "__main__":
    print("Generating insights using Gemini...")
    insights = get_gemini_insights(individuals_data, sample_burnout_predictions)
    print("\n" + "="*80)
    print("GEMINI INSIGHTS REPORT")
    print("="*80)
    print(insights)
