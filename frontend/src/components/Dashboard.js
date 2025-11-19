import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import ChatInterface from './ChatInterface';
import StatsChart from './StatsChart';
import { FaBolt, FaChartBar, FaMapMarkerAlt } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
  const { username, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [period, setPeriod] = useState('week');
  const [loading, setLoading] = useState(true);
  const [showCharts, setShowCharts] = useState(window.innerWidth > 768);
  const [regionProfiles, setRegionProfiles] = useState(null);
  const [loadingRegions, setLoadingRegions] = useState(false);
  const [showRegions, setShowRegions] = useState(false);

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

  const fetchRegionProfiles = useCallback(async () => {
    try {
      setLoadingRegions(true);
      const response = await api.get('/region-profiles');
      setRegionProfiles(response.data.regions || []);
    } catch (error) {
      console.error('Error fetching region profiles:', error);
      setRegionProfiles([]);
    } finally {
      setLoadingRegions(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [fetchStats]);

  useEffect(() => {
    if (showRegions) {
      fetchRegionProfiles();
    }
  }, [showRegions, fetchRegionProfiles]);

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

          {/* Region Profiles Section */}
          <div className="region-profiles-section" style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #e0e0e0' }}>
            <div className="stats-header">
              <h2>
                <FaMapMarkerAlt style={{ marginRight: '8px' }} />
                Region Profiles
              </h2>
              <button
                className="toggle-charts-btn"
                onClick={() => {
                  setShowRegions(!showRegions);
                  if (!showRegions && !regionProfiles) {
                    fetchRegionProfiles();
                  }
                }}
                aria-label="Toggle region profiles"
              >
                {showRegions ? 'Hide' : 'Show'} Regions
              </button>
            </div>
            
            {showRegions && (
              <div className="region-profiles-content">
                {loadingRegions ? (
                  <div className="loading">Loading region profiles...</div>
                ) : regionProfiles && regionProfiles.length > 0 ? (
                  <div className="regions-list">
                    <div className="regions-summary" style={{ marginBottom: '15px', padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
                      <strong>Total Regions: {regionProfiles.length}</strong>
                    </div>
                    <div className="regions-grid" style={{ display: 'grid', gap: '10px', maxHeight: '400px', overflowY: 'auto' }}>
                      {regionProfiles.map((region) => (
                        <div key={region.id} className="region-card" style={{ 
                          padding: '12px', 
                          border: '1px solid #ddd', 
                          borderRadius: '4px',
                          backgroundColor: '#fff'
                        }}>
                          <h4 style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: 'bold' }}>
                            {region.disco_name}
                          </h4>
                          <div style={{ fontSize: '12px', color: '#666' }}>
                            <div><strong>ID:</strong> {region.id}</div>
                            <div><strong>States:</strong> {Array.isArray(region.states) ? region.states.join(', ') : 'N/A'}</div>
                            <div><strong>Avg Offtake:</strong> {region.avg_offtake_mwh_per_hour?.toFixed(2) || 'N/A'} MWh/h</div>
                            <div><strong>Avg Available PCC:</strong> {region.avg_available_pcc_mwh_per_hour?.toFixed(2) || 'N/A'} MWh/h</div>
                            <div><strong>Utilization:</strong> {region.utilisation_percent?.toFixed(2) || 'N/A'}%</div>
                            <div><strong>Estimated Daily:</strong> {region.estimated_daily_mwh?.toFixed(2) || 'N/A'} MWh</div>
                            <div><strong>Full Load Hours:</strong> {region.estimated_full_load_hours?.toFixed(2) || 'N/A'} hours</div>
                            {region.schedule_template && Array.isArray(region.schedule_template) && region.schedule_template.length > 0 && (
                              <div style={{ marginTop: '4px' }}>
                                <strong>Schedule Blocks:</strong> {region.schedule_template.length}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="no-data">No region profiles available</div>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="chat-panel">
          <ChatInterface onLogEvent={fetchStats} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

