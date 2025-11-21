import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import ChatInterface from './ChatInterface';
import StatsChart from './StatsChart';
import { FaBolt, FaChartBar, FaMapMarkerAlt, FaSync, FaToggleOn, FaToggleOff, FaCheckCircle, FaClock } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
  const { username, logout } = useAuth();
  const [stats, setStats] = useState(null);
  const [period, setPeriod] = useState('week');
  const [loading, setLoading] = useState(true);
  const [showCharts, setShowCharts] = useState(true);
  const [regionProfiles, setRegionProfiles] = useState(null);
  const [loadingRegions, setLoadingRegions] = useState(false);
  const [showRegions, setShowRegions] = useState(false);
  const [autoMode, setAutoMode] = useState(true); // Default to automatic mode
  const [autoLogStats, setAutoLogStats] = useState({ total: 0, lastUpdate: null });

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get(`/stats?period=${period}`);
      setStats(response.data);
      
      // Calculate auto-generated log stats
      if (response.data && response.data.events) {
        const autoLogs = response.data.events.filter(event => event.auto_generated === true);
        const lastAutoLog = autoLogs.length > 0 ? autoLogs[autoLogs.length - 1] : null;
        setAutoLogStats({
          total: autoLogs.length,
          lastUpdate: lastAutoLog ? new Date(lastAutoLog.timestamp) : null
        });
      }
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
          {/* Auto-Logging Status Banner */}
          <div className={`auto-logging-banner ${autoMode ? 'active' : 'inactive'}`}>
            <div className="auto-logging-content">
              <div className="auto-logging-status">
                <FaSync className={`auto-sync-icon ${autoMode ? 'spinning' : ''}`} />
                <div className="auto-logging-text">
                  <strong>Automatic Logging: {autoMode ? 'ACTIVE' : 'INACTIVE'}</strong>
                  {stats?.region?.name && (
                    <span className="region-tracking-label">
                      Tracking region: <strong>{stats.region.name}</strong>
                      {Array.isArray(stats.region.states) && stats.region.states.length > 0 && (
                        <> • Coverage: {stats.region.states.join(', ')}</>
                      )}
                    </span>
                  )}
                  {autoMode && (
                    <span className="auto-logging-details">
                      {autoLogStats.total > 0 ? (
                        <>
                          {autoLogStats.total} auto-logged events
                          {autoLogStats.lastUpdate && (
                            <> • Last update: {autoLogStats.lastUpdate.toLocaleTimeString()}</>
                          )}
                        </>
                      ) : (
                        <>Waiting for first automatic log...</>
                      )}
                    </span>
                  )}
                </div>
              </div>
              <div className="mode-toggle-container">
                <label className="mode-toggle-label">
                  <span className="mode-label-text">{autoMode ? 'Automatic' : 'Manual'}</span>
                  <button
                    className={`mode-toggle ${autoMode ? 'auto-active' : 'manual-active'}`}
                    onClick={() => setAutoMode(!autoMode)}
                    aria-label={autoMode ? 'Switch to manual mode' : 'Switch to automatic mode'}
                  >
                    {autoMode ? <FaToggleOn /> : <FaToggleOff />}
                  </button>
                </label>
              </div>
            </div>
            {autoMode && (
              <div className="auto-logging-info">
                <FaCheckCircle className="info-icon" />
                <span>Power events are automatically logged based on your region's schedule. You can still log manually anytime.</span>
              </div>
            )}
          </div>

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

          {/* Power Schedule Information Section */}
          <div className="region-profiles-section" style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #e0e0e0' }}>
            <div className="stats-header">
              <h2>
                <FaMapMarkerAlt style={{ marginRight: '8px' }} />
                Your Power Schedule Information
              </h2>
              <button
                className={`toggle-charts-btn ${showRegions ? 'active' : ''}`}
                onClick={() => {
                  setShowRegions(!showRegions);
                  if (!showRegions && !regionProfiles) {
                    fetchRegionProfiles();
                  }
                }}
                aria-label="Toggle power schedule information"
              >
                {showRegions ? (
                  <>
                    <FaClock style={{ marginRight: '5px' }} />
                    Hide Schedule
                  </>
                ) : (
                  <>
                    <FaClock style={{ marginRight: '5px' }} />
                    View Schedule
                  </>
                )}
              </button>
            </div>
            
            {!showRegions && (
              <div className="schedule-preview" style={{ 
                marginTop: '15px', 
                padding: '15px', 
                backgroundColor: '#f8f9fa', 
                borderRadius: '8px',
                border: '2px solid #e0e0e0',
                transition: 'all 0.3s ease'
              }}>
                <p style={{ margin: 0, color: '#666', fontSize: '14px' }}>
                  <FaMapMarkerAlt style={{ marginRight: '8px', color: '#667eea' }} />
                  <strong>Your power schedule</strong> is automatically determined based on your location and regional power distribution data from NERC Q2 2025.
                  {autoMode && (
                    <> Power events are logged automatically according to this schedule.</>
                  )}
                </p>
              </div>
            )}
            
            {showRegions && (
              <div className="region-profiles-content">
                {loadingRegions ? (
                  <div className="loading">Loading region profiles...</div>
                ) : regionProfiles && regionProfiles.length > 0 ? (
                  <div className="regions-list">
                    <div className="regions-summary" style={{ 
                      marginBottom: '15px', 
                      padding: '15px', 
                      backgroundColor: '#e8f4f8', 
                      borderRadius: '8px',
                      border: '2px solid #667eea',
                      animation: showRegions ? 'pulse 2s ease-in-out infinite' : 'none'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <FaCheckCircle style={{ color: '#28a745', fontSize: '18px' }} />
                        <div>
                          <strong style={{ color: '#333', fontSize: '16px' }}>Power Schedule Active</strong>
                          <p style={{ margin: '5px 0 0 0', color: '#666', fontSize: '14px' }}>
                            {regionProfiles.length} distribution companies monitored • Based on NERC Q2 2025 data
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="regions-grid" style={{ 
                      display: 'grid', 
                      gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                      gap: '15px', 
                      maxHeight: '500px', 
                      overflowY: 'auto',
                      padding: '10px 0'
                    }}>
                      {regionProfiles.map((region) => (
                        <div key={region.id} className="region-card" style={{ 
                          padding: '15px', 
                          border: '2px solid #e0e0e0', 
                          borderRadius: '8px',
                          backgroundColor: '#fff',
                          transition: 'all 0.3s ease',
                          position: 'relative',
                          overflow: 'hidden'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.borderColor = '#667eea';
                          e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.2)';
                          e.currentTarget.style.transform = 'translateY(-2px)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.borderColor = '#e0e0e0';
                          e.currentTarget.style.boxShadow = 'none';
                          e.currentTarget.style.transform = 'translateY(0)';
                        }}
                        >
                          <div style={{ 
                            position: 'absolute', 
                            top: '10px', 
                            right: '10px',
                            width: '8px',
                            height: '8px',
                            borderRadius: '50%',
                            backgroundColor: '#28a745',
                            animation: 'pulse 2s ease-in-out infinite'
                          }}></div>
                          <h4 style={{ margin: '0 0 12px 0', fontSize: '15px', fontWeight: 'bold', color: '#333' }}>
                            {region.disco_name}
                          </h4>
                          <div style={{ fontSize: '13px', color: '#666', lineHeight: '1.6' }}>
                            <div style={{ marginBottom: '6px' }}>
                              <strong style={{ color: '#667eea' }}>Coverage:</strong> {Array.isArray(region.states) ? region.states.join(', ') : 'N/A'}
                            </div>
                            {region.schedule_template && Array.isArray(region.schedule_template) && region.schedule_template.length > 0 && (
                              <div style={{ 
                                marginTop: '10px', 
                                padding: '8px',
                                backgroundColor: '#f8f9fa',
                                borderRadius: '4px',
                                border: '1px solid #e0e0e0'
                              }}>
                                <strong style={{ color: '#667eea' }}>Schedule Blocks:</strong> {region.schedule_template.length}
                                <div style={{ fontSize: '11px', color: '#888', marginTop: '4px' }}>
                                  Power availability times configured
                                </div>
                              </div>
                            )}
                            <div style={{ marginTop: '8px', fontSize: '11px', color: '#888' }}>
                              Utilization: {region.utilisation_percent?.toFixed(1) || 'N/A'}% • 
                              Daily: {region.estimated_daily_mwh?.toFixed(0) || 'N/A'} MWh
                            </div>
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
          <ChatInterface onLogEvent={fetchStats} autoMode={autoMode} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

