import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ManagerDashboard from './pages/ManagerDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="main-nav">
          <div className="nav-logo">Responsible Leadership</div>
          <ul className="nav-links">
            <li><Link to="/manager">Manager</Link></li>
            <li><Link to="/hr">HR</Link></li>
            <li><Link to="/employee">Employee</Link></li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/manager" element={<ManagerDashboard />} />
            <Route path="/hr" element={<div className="placeholder-page">HR Dashboard (Coming Soon)</div>} />
            <Route path="/employee" element={<div className="placeholder-page">Employee Dashboard (Coming Soon)</div>} />
            <Route path="/" element={
              <div className="landing-page">
                <h1>Welcome to the Responsible Leadership Platform</h1>
                <p>Select your role to continue.</p>
                <div className="role-cards">
                  <Link to="/manager" className="role-card">Manager</Link>
                  <Link to="/hr" className="role-card">HR</Link>
                  <Link to="/employee" className="role-card">Employee</Link>
                </div>
              </div>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
