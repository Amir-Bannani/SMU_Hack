"""
Employee Underperformance Detection System
Rule-Based Approach using Resource Allocation, Fatigue Score, and Designation
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, List
import json


@dataclass
class EmployeeMetrics:
    """Employee performance metrics"""
    employee_id: str
    name: str
    resource_allocation: float  # 1.0-10.0 (workload)
    fatigue_score: float        # 0.0-10.0 (mental fatigue)
    designation: float          # 0.0-5.0 (seniority)


class UnderperformanceDetector:
    """
    Rule-based system to detect employee underperformance
    
    Core Logic:
    - Low workload + High fatigue = Red flag
    - High designation employees should handle more with less fatigue
    - Junior employees get more tolerance for fatigue
    """
    
    def __init__(self):
        # Thresholds (tunable based on your organization)
        self.LOW_WORKLOAD_THRESHOLD = 5.0      # Below this is considered low
        self.HIGH_FATIGUE_THRESHOLD = 6.0      # Above this is concerning
        self.CRITICAL_FATIGUE_THRESHOLD = 8.0   # Very concerning
        
        # Designation-based expectations
        self.DESIGNATION_LEVELS = {
            0: "Intern",
            1: "Junior",
            2: "Mid-Level",
            3: "Senior",
            4: "Lead",
            5: "Principal/Manager"
        }
    
    def calculate_expected_capacity(self, designation: float) -> float:
        """
        Calculate expected work capacity based on designation
        Higher designation = should handle more workload with same fatigue
        """
        # Linear scaling: Designation 0 expects 30%, Designation 5 expects 80%
        return 30 + (designation * 10)
    
    def calculate_fatigue_tolerance(self, designation: float) -> float:
        """
        Calculate fatigue tolerance based on designation
        Junior employees get more tolerance
        """
        # Inverse relationship: Junior (0) = 8.0 tolerance, Senior (5) = 5.0 tolerance
        return 8.0 - (designation * 0.6)
    
    def calculate_performance_score(self, resource_allocation: float, 
                                   fatigue_score: float, 
                                   designation: float) -> float:
        """
        Calculate performance score (0-10)
        Higher score = better performance
        Lower score = more underperforming
        
        Score interpretation:
        0-3: Severely underperforming
        4-5: Underperforming
        6-7: Below average
        8-9: Good performance
        10: Excellent performance
        """
        # Base score starts at 10 (perfect)
        score = 10.0
        
        # Penalty 1: Low workload relative to designation
        expected_min_workload = 3.0 + (designation * 0.8)  # Higher designation = higher expectation
        if resource_allocation < expected_min_workload:
            workload_penalty = (expected_min_workload - resource_allocation) * 0.5
            score -= workload_penalty
        
        # Penalty 2: High fatigue (weighted by workload)
        # If workload is low but fatigue is high = major penalty
        workload_factor = 10.0 - resource_allocation  # Higher when workload is lower
        fatigue_penalty = (fatigue_score / 10.0) * (workload_factor / 10.0) * 5.0
        score -= fatigue_penalty
        
        # Penalty 3: Fatigue exceeding designation tolerance
        fatigue_tolerance = self.calculate_fatigue_tolerance(designation)
        if fatigue_score > fatigue_tolerance:
            tolerance_penalty = (fatigue_score - fatigue_tolerance) * 0.4
            score -= tolerance_penalty
        
        # Bonus: High workload with low fatigue (especially for seniors)
        if resource_allocation >= 7.0 and fatigue_score <= 4.0:
            bonus = (designation / 5.0) * 1.0  # Senior gets more bonus
            score += bonus
        
        # Normalize to 0-10 range
        score = max(0.0, min(10.0, score))
        
        return round(score, 1)
    
    def detect_underperformance(self, metrics: EmployeeMetrics) -> Dict:
        """
        Main detection logic - returns detailed analysis
        """
        resource = metrics.resource_allocation
        fatigue = metrics.fatigue_score
        designation = metrics.designation
        
        # Calculate performance score (0-10)
        performance_score = self.calculate_performance_score(resource, fatigue, designation)
        fatigue_tolerance = self.calculate_fatigue_tolerance(designation)
        
        # Detection flags
        flags = []
        severity = "NORMAL"
        is_underperforming = False
        
        # Determine status based on performance score
        if performance_score < 4.0:
            severity = "CRITICAL"
            is_underperforming = True
            flags.append("Severely underperforming")
        elif performance_score < 6.0:
            severity = "WARNING"
            is_underperforming = True
            flags.append("Underperforming")
        elif performance_score < 7.0:
            severity = "CAUTION"
            flags.append("Below average performance")
        
        # Rule 1: Low workload + High fatigue
        if resource < self.LOW_WORKLOAD_THRESHOLD and fatigue > self.HIGH_FATIGUE_THRESHOLD:
            flags.append("Low workload but high fatigue")
            is_underperforming = True
            if severity == "NORMAL" or severity == "CAUTION":
                severity = "WARNING"
        
        # Rule 2: Very low workload for senior
        if resource < 3.0 and designation >= 3.0 and fatigue > 3.0:
            flags.append("Very low workload for senior level")
            is_underperforming = True
            if severity == "NORMAL" or severity == "CAUTION":
                severity = "WARNING"
        
        # Rule 3: Critical fatigue
        if fatigue > self.CRITICAL_FATIGUE_THRESHOLD and resource < 7.0:
            flags.append("Critical fatigue with moderate workload")
            is_underperforming = True
            severity = "CRITICAL"
        
        # Rule 4: Fatigue exceeds tolerance
        if fatigue > fatigue_tolerance and resource < 6.0:
            flags.append(f"Fatigue exceeds tolerance for level")
            is_underperforming = True
            if severity == "NORMAL" or severity == "CAUTION":
                severity = "WARNING"
        
        # Add appropriate flag if none exist
        if not flags:
            if performance_score >= 8.0:
                flags.append("Good performance")
            else:
                flags.append("Average performance")
        
        # Build compact result for LLM
        result = {
            "employee_id": metrics.employee_id,
            "name": metrics.name,
            "performance_score": performance_score,
            "status": severity,
            "underperforming": is_underperforming,
            "resource_allocation": resource,
            "fatigue_score": fatigue,
            "designation": designation,
            "issues": flags,
            "action_needed": self._get_compact_action(performance_score, severity)
        }
        
        return result
    
    def _get_priority_actions(self, results: List[Dict]) -> List[Dict]:
        """DEPRECATED - keeping for backwards compatibility"""
        return []
    
    def _get_recommendations(self, resource: float, fatigue: float, 
                            designation: float, flags: List[str], performance_score: float) -> List[str]:
        """DEPRECATED - keeping for backwards compatibility"""
        return []
    
    def _get_workload_status(self, resource: float) -> str:
        """Interpret workload level"""
        if resource < 3:
            return "Very Low"
        elif resource < 5:
            return "Low"
        elif resource < 7:
            return "Moderate"
        elif resource < 9:
            return "High"
        else:
            return "Very High"
    
    def _get_compact_action(self, score: float, severity: str) -> str:
        """Get compact action recommendation"""
        if severity == "CRITICAL":
            return "Urgent: Immediate intervention"
        elif severity == "WARNING":
            return "Schedule performance review"
        elif severity == "CAUTION":
            return "Monitor closely"
        else:
            return "Continue current track" if score >= 8 else "Maintain performance"
    
    def _get_performance_level(self, score: float) -> str:
        """Interpret performance score"""
        if score < 3:
            return "Severely Underperforming"
        elif score < 4:
            return "Critically Low"
        elif score < 5:
            return "Underperforming"
        elif score < 6:
            return "Below Average"
        elif score < 7:
            return "Average"
        elif score < 8:
            return "Good"
        elif score < 9:
            return "Very Good"
        else:
            return "Excellent"
    
    def _get_fatigue_status(self, fatigue: float) -> str:
        """Interpret fatigue level"""
        if fatigue < 3:
            return "Minimal"
        elif fatigue < 5:
            return "Low"
        elif fatigue < 7:
            return "Moderate"
        elif fatigue < 8:
            return "High"
        else:
            return "Critical"
    
    def _get_recommendations(self, resource: float, fatigue: float, 
                            designation: float, flags: List[str], performance_score: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Performance-based recommendations
        if performance_score >= 8.0:
            recommendations.append("✓ Employee performing well - consider for challenging projects")
            return recommendations
        elif performance_score >= 7.0:
            recommendations.append("✓ Acceptable performance - monitor for improvements")
        
        # Low performance score
        if performance_score < 4.0:
            recommendations.append("🚨 URGENT: Immediate intervention required")
        elif performance_score < 6.0:
            recommendations.append("⚠️ Performance review needed")
        
        # Low workload recommendations
        if resource < self.LOW_WORKLOAD_THRESHOLD:
            recommendations.append("Consider increasing task allocation gradually")
            recommendations.append("Discuss current workload and capacity with employee")
        
        # High fatigue recommendations
        if fatigue > self.HIGH_FATIGUE_THRESHOLD:
            if resource < 5:
                recommendations.append("⚠️ Investigate root cause of fatigue despite low workload")
                recommendations.append("Check for personal issues, health concerns, or workplace environment problems")
            else:
                recommendations.append("Consider workload reduction or deadline extensions")
            
            recommendations.append("Schedule one-on-one to understand challenges")
            recommendations.append("Evaluate if training or mentorship is needed")
        
        # Critical cases
        if fatigue > self.CRITICAL_FATIGUE_THRESHOLD:
            recommendations.append("🚨 URGENT: Immediate intervention required")
            recommendations.append("Consider temporary workload relief or time off")
        
        # Senior employee specific
        if designation >= 3 and resource < 5:
            recommendations.append("Review if employee is properly utilized given their experience level")
            recommendations.append("Consider assigning more complex or leadership tasks")
        
        return recommendations
    
    def analyze_team(self, employees: List[EmployeeMetrics]) -> Dict:
        """Analyze entire team and generate compact report"""
        results = []
        
        for emp in employees:
            result = self.detect_underperformance(emp)
            results.append(result)
        
        # Team statistics
        total = len(results)
        underperforming = sum(1 for r in results if r["underperforming"])
        critical = sum(1 for r in results if r["status"] == "CRITICAL")
        warning = sum(1 for r in results if r["status"] == "WARNING")
        caution = sum(1 for r in results if r["status"] == "CAUTION")
        
        # Priority cases
        priority_cases = [
            {
                "employee_id": r["employee_id"],
                "name": r["name"],
                "score": r["performance_score"],
                "status": r["status"],
                "action": r["action_needed"]
            }
            for r in results if r["status"] in ["CRITICAL", "WARNING"]
        ]
        
        # Sort by score (lowest first)
        priority_cases.sort(key=lambda x: x["score"])
        
        # Complete team report in single JSON
        team_report = {
            "report_metadata": {
                "total_employees": total,
                "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "summary": {
                "healthy": total - underperforming,
                "underperforming": underperforming,
                "critical": critical,
                "warning": warning,
                "caution": caution,
                "underperformance_rate_pct": round((underperforming / total * 100), 1) if total > 0 else 0,
                "avg_performance_score": round(sum(r["performance_score"] for r in results) / total, 1) if total > 0 else 0
            },
            "priority_actions": priority_cases,
            "all_employees": results
        }
        
        return team_report
    
    def _get_priority_actions(self, results: List[Dict]) -> List[Dict]:
        """Get prioritized list of actions needed"""
        actions = []
        
        # Critical cases first
        critical_cases = [r for r in results if r["severity"] == "CRITICAL"]
        for case in critical_cases:
            actions.append({
                "priority": "URGENT",
                "employee": case["name"],
                "action": "Immediate intervention required",
                "reason": ", ".join(case["analysis"]["flags"])
            })
        
        # Warning cases
        warning_cases = [r for r in results if r["severity"] == "WARNING"]
        for case in warning_cases:
            actions.append({
                "priority": "HIGH",
                "employee": case["name"],
                "action": "Schedule review meeting",
                "reason": ", ".join(case["analysis"]["flags"])
            })
        
        return actions


def print_employee_report(result: Dict):
    """Pretty print individual employee report"""
    print("\n" + "="*70)
    print(f"Employee: {result['name']} (ID: {result['employee_id']})")
    print("="*70)
    
    status_emoji = "🚨" if result['status'] == "CRITICAL" else "⚠️" if result['status'] == "WARNING" else "⚠️" if result['status'] == "CAUTION" else "✓"
    print(f"\nStatus: {status_emoji} {result['status']}")
    print(f"Performance Score: {result['performance_score']}/10")
    print(f"Underperforming: {'YES' if result['underperforming'] else 'NO'}")
    
    print(f"\n📊 Metrics:")
    print(f"  • Resource: {result['resource_allocation']}/10")
    print(f"  • Fatigue: {result['fatigue_score']}/10")
    print(f"  • Designation: {result['designation']}/5")
    
    print(f"\n🚩 Issues: {', '.join(result['issues'])}")
    print(f"💡 Action: {result['action_needed']}")


def print_team_report(report: Dict):
    """Pretty print team report"""
    print("\n" + "="*70)
    print("TEAM PERFORMANCE REPORT")
    print("="*70)
    
    summary = report['summary']
    print(f"\n📈 Summary:")
    print(f"  • Total: {report['report_metadata']['total_employees']}")
    print(f"  • Healthy: {summary['healthy']} ✓")
    print(f"  • Underperforming: {summary['underperforming']} ({summary['underperformance_rate_pct']}%)")
    print(f"  • Critical: {summary['critical']} 🚨 | Warning: {summary['warning']} ⚠️ | Caution: {summary['caution']} ⚠️")
    print(f"  • Avg Score: {summary['avg_performance_score']}/10")
    
    if report['priority_actions']:
        print(f"\n🎯 Priority Actions ({len(report['priority_actions'])} employees):")
        for action in report['priority_actions'][:5]:  # Show top 5
            emoji = "🚨" if action['status'] == "CRITICAL" else "⚠️"
            print(f"  {emoji} {action['name']}: Score {action['score']}/10 - {action['action']}")


# Example usage
def main():
    """Demo with sample data"""
    
    # Sample employee data
    employees = [
        EmployeeMetrics("E001", "Alice Johnson", 8.0, 3.0, 4.0),  # Senior, high workload, low fatigue - GOOD
        EmployeeMetrics("E002", "Bob Smith", 3.0, 7.5, 3.0),      # Senior, low workload, high fatigue - UNDERPERFORMING
        EmployeeMetrics("E003", "Carol Davis", 6.0, 5.0, 2.0),    # Mid-level, moderate workload, moderate fatigue - OK
        EmployeeMetrics("E004", "David Lee", 2.0, 8.5, 4.0),      # Lead, very low workload, critical fatigue - CRITICAL
        EmployeeMetrics("E005", "Eve Wilson", 7.0, 2.0, 1.0),     # Junior, good workload, low fatigue - GOOD
        EmployeeMetrics("E006", "Frank Brown", 4.0, 6.5, 2.0),    # Mid-level, low workload, moderate-high fatigue - WARNING
        EmployeeMetrics("E007", "Grace Taylor", 9.0, 7.0, 5.0),   # Manager, high workload, high fatigue - OK (expected)
        EmployeeMetrics("E008", "Henry Martinez", 2.5, 9.0, 1.0), # Junior, low workload, critical fatigue - CRITICAL
    ]
    
    # Initialize detector
    detector = UnderperformanceDetector()
    
    # Analyze individual employees
    print("\n" + "="*70)
    print("INDIVIDUAL EMPLOYEE ANALYSIS")
    print("="*70)
    
    for emp in employees:
        result = detector.detect_underperformance(emp)
        print_employee_report(result)
    
    # Analyze entire team
    team_report = detector.analyze_team(employees)
    print_team_report(team_report)
    
    # Save everything to single JSON file
    with open('team_performance_report.json', 'w') as f:
        json.dump(team_report, f, indent=2)
    
    print("\n" + "="*70)
    print("✓ Complete report saved to 'team_performance_report.json'")
    print("  This JSON contains:")
    print("  - Summary statistics")
    print("  - Priority actions list")
    print("  - All employee details (compact, LLM-ready)")
    print("="*70)


if __name__ == "__main__":
    main()