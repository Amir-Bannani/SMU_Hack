import React, { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Service to fetch CEO data (we'll add this to taskService.js later or fetch directly)
const fetchCEOData = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/ceo-summary');
        if (!response.ok) throw new Error('Failed to fetch CEO data');
        return await response.json();
    } catch (error) {
        console.error("Error fetching CEO data:", error);
        return null;
    }
};

const CEODashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            const result = await fetchCEOData();
            setData(result);
            setLoading(false);
        };
        loadData();
    }, []);

    if (loading) return <div className="loading">Loading Executive Dashboard...</div>;
    if (!data) return <div className="error-message">Unable to load Executive Dashboard.</div>;

    // Prepare Trend Data
    const trendData = data.trends.weeks.map((week, index) => ({
        week,
        burnout: data.trends.burnout[index],
        fatigue: data.trends.fatigue[index],
        equity: data.trends.equity[index]
    }));

    return (
        <div className="dashboard-container ceo-dashboard">
            <header className="dashboard-header">
                <div>
                    <h1>Executive Overview</h1>
                    <p className="subtitle">Manager Performance & Organizational Health</p>
                </div>
                <div className="header-actions">
                    <span className="date-badge">Latest: {data.latest_week_id}</span>
                </div>
            </header>

            {/* Key Metrics Grid */}
            <div className="metrics-grid">
                <div className="metric-card">
                    <h3>Workload Equity</h3>
                    <div className="metric-value">{data.manager_performance.workload_equity}</div>
                    <p className="metric-sub">Std Dev (Lower is Better)</p>
                </div>
                <div className="metric-card">
                    <h3>Burnout Mitigation</h3>
                    <div className={`metric-value ${data.manager_performance.burnout_mitigation > 0 ? 'good' : 'bad'}`}>
                        {data.manager_performance.burnout_mitigation > 0 ? '+' : ''}{data.manager_performance.burnout_mitigation}
                    </div>
                    <p className="metric-sub">vs Previous Week</p>
                </div>
                <div className="metric-card" title="Percentage of employees with Burnout Rate > 0.7 (Critical Risk)">
                    <h3>Retention Risk ℹ️</h3>
                    <div className="metric-value">{data.manager_performance.retention_risk}</div>
                    <p className="metric-sub">Team in Critical State</p>
                </div>
                <div className="metric-card">
                    <h3>Team Size</h3>
                    <div className="metric-value">{data.manager_performance.team_size}</div>
                    <p className="metric-sub">Active Employees</p>
                </div>
            </div>

            <div className="dashboard-grid">
                {/* Burnout & Fatigue Trend */}
                <div className="card full-width">
                    <div className="card-header">
                        <h3>📉 Organizational Health Trends</h3>
                    </div>
                    <div className="chart-container" style={{ height: '300px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={trendData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis dataKey="week" stroke="#94a3b8" />
                                <YAxis yAxisId="left" stroke="#ef4444" domain={[0, 1]} />
                                <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" domain={[0, 10]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', color: '#f8fafc' }}
                                />
                                <Legend />
                                <Line yAxisId="left" type="monotone" dataKey="burnout" stroke="#ef4444" name="Avg Burnout Rate" strokeWidth={2} />
                                <Line yAxisId="right" type="monotone" dataKey="fatigue" stroke="#f59e0b" name="Avg Difficulty Score" strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Workload Equity Trend */}
                <div className="card full-width">
                    <div className="card-header">
                        <h3>⚖️ Workload Equity Evolution</h3>
                        <span className="card-subtitle">Tracking fairness in task distribution over time</span>
                    </div>
                    <div className="chart-container" style={{ height: '300px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={trendData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis dataKey="week" stroke="#94a3b8" />
                                <YAxis stroke="#3b82f6" domain={['auto', 'auto']} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', color: '#f8fafc' }}
                                />
                                <Legend />
                                <Line type="monotone" dataKey="equity" stroke="#3b82f6" name="Equity Score (Std Dev)" strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CEODashboard;
