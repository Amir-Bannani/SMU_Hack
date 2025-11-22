import React, { useEffect, useState } from 'react';
import { getTasks, getStats, getInsights } from '../services/taskService';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const ManagerDashboard = () => {
    const [tasks, setTasks] = useState([]);
    const [stats, setStats] = useState(null);
    const [insights, setInsights] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const tasksData = await getTasks();
                setTasks(tasksData);
                const statsData = await getStats();
                setStats(statsData);
                const insightsData = await getInsights();
                setInsights(insightsData);
            } catch (error) {
                console.error("Failed to load data");
            }
        };

        fetchData();
    }, []);

    const COLORS = ['#facc15', '#60a5fa', '#4ade80'];

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>Manager Dashboard</h1>
                <p>Welcome, Manager</p>
            </header>

            <div className="dashboard-grid">
                <div className="card task-database">
                    <h2>IT Task Database</h2>
                    <div className="task-list">
                        {tasks.length === 0 ? (
                            <p>No tasks available</p>
                        ) : (
                            <table className="task-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Title</th>
                                        <th>Status</th>
                                        <th>Assignee</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tasks.map(task => (
                                        <tr key={task.id}>
                                            <td>{task.id}</td>
                                            <td>{task.title}</td>
                                            <td>
                                                <span className={`status-badge ${task.status.toLowerCase().replace(' ', '-')}`}>
                                                    {task.status}
                                                </span>
                                            </td>
                                            <td>{task.assignee}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>

                <div className="card employee-stats">
                    <h2>Employee Statistics</h2>
                    {stats ? (
                        <div className="charts-container">
                            <div className="chart-wrapper">
                                <h3>Performance Trend</h3>
                                <ResponsiveContainer width="100%" height={200}>
                                    <BarChart data={stats.performance}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                        <XAxis dataKey="name" stroke="#94a3b8" />
                                        <YAxis stroke="#94a3b8" />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                            itemStyle={{ color: '#e2e8f0' }}
                                        />
                                        <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>

                            <div className="chart-wrapper">
                                <h3>Task Distribution</h3>
                                <ResponsiveContainer width="100%" height={200}>
                                    <PieChart>
                                        <Pie
                                            data={stats.taskDistribution}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {stats.taskDistribution.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                            itemStyle={{ color: '#e2e8f0' }}
                                        />
                                        <Legend />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    ) : (
                        <p>Loading statistics...</p>
                    )}
                </div>

                <div className="card ai-insights">
                    <h2>AI Insights</h2>
                    {insights ? (
                        <div className="insights-content">
                            <div className="insight-item">
                                <h3>Productivity Analysis</h3>
                                <p>{insights.productivity}</p>
                            </div>
                            <div className="insight-item">
                                <h3>Risk Assessment</h3>
                                <p>{insights.risk}</p>
                            </div>
                            <div className="insight-item">
                                <h3>Recommendation</h3>
                                <p>{insights.recommendation}</p>
                            </div>
                        </div>
                    ) : (
                        <p>Generating AI insights...</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ManagerDashboard;
