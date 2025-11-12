import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import ChatInterface from './ChatInterface';
import StatsChart from './StatsChart';
import { FaBolt, FaChartBar } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
  const { username, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [period, setPeriod] = useState('week');
  const [loading, setLoading] = useState(true);
  const [showCharts, setShowCharts] = useState(window.innerWidth > 768);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get(`/stats?period=${period}`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  }, [period]);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [fetchStats]);

  useEffect(() => {
    const handleResize = () => {
      // On desktop, always show charts; on mobile, keep current state
      if (window.innerWidth > 768) {
        setShowCharts(true);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>
            <FaBolt className="header-icon" />
            Electricity Logger
          </h1>
          <div className="header-actions">
            <span className="username">Welcome, {username}</span>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="stats-panel">
          <div className="stats-header">
            <h2>Statistics</h2>
            <div className="period-selector">
              <button
                className={period === 'day' ? 'active' : ''}
                onClick={() => setPeriod('day')}
              >
                Today
              </button>
              <button
                className={period === 'week' ? 'active' : ''}
                onClick={() => setPeriod('week')}
              >
                Week
              </button>
              <button
                className={period === 'month' ? 'active' : ''}
                onClick={() => setPeriod('month')}
              >
                Month
              </button>
            </div>
          </div>
          
          {loading ? (
            <div className="loading">Loading statistics...</div>
          ) : stats ? (
            <div className="stats-content">
              <div className="total-hours">
                <h3>Total Light Hours</h3>
                <p className="hours-value">{stats.total_hours} hours</p>
                <p className="period-text">in the last {period}</p>
              </div>
              <button
                className="toggle-charts-btn"
                onClick={() => setShowCharts(!showCharts)}
                aria-label="Toggle charts"
              >
                <FaChartBar className="toggle-icon" />
                {showCharts ? 'Hide Charts' : 'Show Charts'}
              </button>
              {showCharts && <StatsChart data={stats.daily_stats} />}
            </div>
          ) : (
            <div className="no-data">No data available</div>
          )}
        </div>

        <div className="chat-panel">
          <ChatInterface onLogEvent={fetchStats} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

