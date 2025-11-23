import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ManagerDashboard from './pages/ManagerDashboard';
import CEODashboard from './pages/CEODashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="main-nav">
          <div className="nav-logo">
            <img src="/logo.png" alt="Logo" className="logo-img" />
            <span className="brand-name">WorkPace</span>
          </div>
          <ul className="nav-links">
            <li><Link to="/manager">Manager</Link></li>
            <li><Link to="/ceo">CEO</Link></li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/manager" element={<ManagerDashboard />} />
            <Route path="/ceo" element={<CEODashboard />} />
            <Route path="/" element={
              <div className="landing-page">
                <h1>Welcome to the Responsible Leadership Platform</h1>
                <p>Select your role to continue.</p>
                <div className="role-cards">
                  <Link to="/manager" className="role-card">Manager</Link>
                  <Link to="/ceo" className="role-card">CEO</Link>
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
