import React, { useEffect, useState } from 'react';
import { getWeeklySummary } from '../services/taskService';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Simple Markdown Renderer Component
const MarkdownRenderer = ({ content }) => {
    if (!content) return null;

    const sections = content.split(/###\s+/).filter(Boolean);

    return (
        <div className="markdown-content">
            {sections.map((section, index) => {
                const [title, ...bodyParts] = section.split('\n');
                const body = bodyParts.join('\n');

                // Parse bold text
                const parseBold = (text) => {
                    const parts = text.split(/(\*\*.*?\*\*)/g);
                    return parts.map((part, i) => {
                        if (part.startsWith('**') && part.endsWith('**')) {
                            return <strong key={i}>{part.slice(2, -2)}</strong>;
                        }
                        return part;
                    });
                };

                return (
                    <div key={index} className="md-section">
                        <h3 className="md-title">{title.trim()}</h3>
                        <div className="md-body">
                            {body.split('\n').map((line, i) => {
                                if (!line.trim()) return null;

                                // List items
                                if (line.trim().startsWith('*') || line.trim().startsWith('-') || line.trim().match(/^\d+\./)) {
                                    return (
                                        <div key={i} className="md-list-item">
                                            {parseBold(line.replace(/^[\*\-\d\.]+\s*/, ''))}
                                        </div>
                                    );
                                }

                                // Regular paragraphs
                                return <p key={i}>{parseBold(line)}</p>;
                            })}
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

const ManagerDashboard = () => {
    const [summaryData, setSummaryData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getWeeklySummary();
                setSummaryData(data);
                setLoading(false);
            } catch (err) {
                setError("Failed to load weekly summary. Please ensure the backend pipeline has been run.");
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <div className="loading">Loading Dashboard...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!summaryData) return <div className="no-data">No data available</div>;

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div>
                    <h1>Manager Dashboard</h1>
                    <p className="subtitle">Team Performance & Burnout Analytics</p>
                </div>
                <div className="header-actions">
                    <button
                        className="btn-process"
                        onClick={async () => {
                            if (confirm("Process data for the next week? Ensure 'new_week_input.csv' is ready.")) {
                                try {
                                    const res = await fetch('http://localhost:5000/api/process-week', { method: 'POST' });
                                    if (res.ok) {
                                        alert("Week processed successfully! Refreshing...");
                                        window.location.reload();
                                    } else {
                                        alert("Error processing week.");
                                    }
                                } catch (e) {
                                    console.error(e);
                                    alert("Failed to connect to backend.");
                                }
                            }
                        }}
                    >
                        ⏩ Process Next Week
                    </button>
                    <span className="date-badge">{summaryData.week_id}</span>
                </div>
            </header>

            <div className="dashboard-grid">
                {/* Burnout Risk Analysis */}
                <div className="card burnout-section">
                    <div className="card-header">
                        <h3>🔥 Burnout Risk Analysis</h3>
                        <span className="card-subtitle">Predicted risk based on workload & difficulty</span>
                    </div>
                    <div className="risk-list">
                        {summaryData?.burnout_analysis?.map((emp, index) => (
                            <div key={index} className="risk-item">
                                <div className="risk-info">
                                    <span className="emp-name">{emp.Name}</span>
                                    <span className={`risk-label ${emp['Burnout Rate'] > 0.7 ? 'critical' : emp['Burnout Rate'] > 0.5 ? 'warning' : 'normal'}`}>
                                        {(emp['Burnout Rate'] * 100).toFixed(0)}% Risk
                                    </span>
                                </div>
                                <div className="risk-meter">
                                    <div
                                        className="risk-fill"
                                        style={{
                                            width: `${emp['Burnout Rate'] * 100}%`,
                                            backgroundColor: emp['Burnout Rate'] > 0.7 ? '#ef4444' : emp['Burnout Rate'] > 0.5 ? '#f59e0b' : '#22c55e'
                                        }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Attention Required */}
                <div className="card attention-section">
                    <div className="card-header">
                        <h3>⚠️ Attention Required</h3>
                    </div>
                    <div className="attention-list">
                        {summaryData?.underperformance_report?.priority_actions?.length > 0 ? (
                            summaryData.underperformance_report.priority_actions.map((action, index) => (
                                <div key={index} className={`attention-item ${action.priority.toLowerCase()}`}>
                                    <div className="attention-header">
                                        <span className="employee-name">{action.employee}</span>
                                        <span className={`priority-badge ${action.priority.toLowerCase()}`}>
                                            {action.priority}
                                        </span>
                                    </div>
                                    <p className="attention-reason">{action.reason}</p>
                                    <div className="recommendation-box">
                                        <strong>Recommended Action:</strong>
                                        <p>{action.action}</p>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <p>No urgent actions required.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* AI Executive Summary */}
            <div className="card ai-section">
                <div className="card-header">
                    <h3>🤖 AI Executive Summary</h3>
                </div>
                <div className="ai-content">
                    <MarkdownRenderer content={summaryData?.ai_insights} />
                </div>
            </div>

            {/* Team Overview Table */}
            <div className="card team-section">
                <div className="card-header">
                    <h3>👥 Team Performance Overview</h3>
                </div>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Role</th>
                            <th>Performance</th>
                            <th>Workload</th>
                            <th>Difficulty</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {summaryData?.underperformance_report?.individuals?.map((emp) => (
                            <tr key={emp.employee_id} className={`row-${emp.severity.toLowerCase()}`}>
                                <td>{emp.name}</td>
                                <td>{emp.metrics.designation_level}</td>
                                <td>
                                    <div className="score-bar-container">
                                        <div
                                            className="score-bar"
                                            style={{
                                                width: `${emp.performance_score * 10}%`,
                                                backgroundColor: emp.performance_score > 7 ? '#10b981' : emp.performance_score > 4 ? '#f59e0b' : '#ef4444'
                                            }}
                                        />
                                        <span>{emp.performance_score}</span>
                                    </div>
                                </td>
                                <td>{emp.metrics.resource_allocation}/10</td>
                                <td>
                                    <span className={`status-dot ${emp.metrics.fatigue_score > 7 ? 'critical' : emp.metrics.fatigue_score > 5 ? 'warning' : 'good'}`}></span>
                                    {emp.metrics.fatigue_score}
                                </td>
                                <td>
                                    <span className={`badge ${emp.severity.toLowerCase()}`}>
                                        {emp.severity}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ManagerDashboard;
