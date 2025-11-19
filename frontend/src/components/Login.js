import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { FaBolt, FaEnvelope, FaPhone, FaMapMarkerAlt, FaFacebook, FaTwitter, FaLinkedin, FaGithub } from 'react-icons/fa';
import LocationAutocomplete from './LocationAutocomplete';
import './Login.css';

const Login = () => {
  const [searchParams] = useSearchParams();
  const mode = searchParams.get('mode'); // 'register' or 'login' or null
  const [isLogin, setIsLogin] = useState(mode !== 'register');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [location, setLocation] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  // Email verification temporarily disabled - kept for easy restoration
  // const [verificationCode, setVerificationCode] = useState('');
  // const [showVerification, setShowVerification] = useState(false);
  // const [verificationType, setVerificationType] = useState('email');
  // const [fallbackCode, setFallbackCode] = useState('');
  // const [emailSent, setEmailSent] = useState(true);
  const { login } = useAuth();
  const navigate = useNavigate();
  const cardRef = useRef(null);
  const illustrationRef = useRef(null);

  // Update isLogin state when URL parameter changes
  useEffect(() => {
    if (mode === 'register') {
      setIsLogin(false);
    } else if (mode === 'login') {
      setIsLogin(true);
    }
    // If no mode parameter, default to login (isLogin = true, which is the default)
  }, [mode]);

  const handleLocationSelect = (locationData) => {
    setLocation(locationData.address);
    // Store location data for future API usage
    console.log('Location selected:', locationData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login flow - device verification temporarily disabled
        const deviceId = localStorage.getItem('deviceId');
        // Send username field - backend will check both username and email
        const response = await api.post('/login', { 
          username: username.trim(),  // Can be username or email
          password,
          deviceId: deviceId || null
        });
        
        // Login directly - no device verification needed
        login(response.data.token, response.data.username);
        navigate('/dashboard');
      } else {
        // Registration flow - email verification temporarily disabled
        const response = await api.post('/register', { 
          username, 
          email, 
          password, 
          location 
        });
        
        if (response.data.message === 'Registration successful' || response.data.token) {
          // Store device ID if provided
          if (response.data.deviceId) {
            localStorage.setItem('deviceId', response.data.deviceId);
          }
          // Login directly - no email verification needed
          login(response.data.token, response.data.username);
          navigate('/dashboard');
        }
      }
    } catch (err) {
      // Improved error handling - show actual error messages from API
      if (err.response?.data?.error) {
        // Backend returned an error message
        setError(err.response.data.error);
      } else if (err.message) {
        // Error object has a message (from our interceptor)
        setError(err.message);
      } else if (err.response?.data) {
        // Backend returned data but no error field
        const data = err.response.data;
        if (typeof data === 'string') {
          setError(data);
        } else if (data.message) {
          setError(data.message);
        } else {
          setError(`Server error: ${JSON.stringify(data)}`);
        }
      } else if (err.request && !err.response) {
        // Network error - no response from server
        const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
        setError(`Cannot connect to backend server. Please check if the backend is running at ${apiUrl}.`);
      } else {
        // Unknown error
        setError(err.message || 'An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Email verification handlers temporarily disabled - kept for easy restoration
  // const handleDeviceVerification = async () => { ... }
  // const handleResendCode = async () => { ... }

  return (
    <div className="login-container">
      {/* Simple Navbar */}
      <nav className="login-navbar">
        <div className="login-navbar-container">
          <div className="login-navbar-brand">
            <FaBolt className="login-navbar-icon" />
            <span>Electricity Logger</span>
          </div>
          <button 
            className="login-navbar-home"
            onClick={() => navigate('/')}
          >
            Home
          </button>
        </div>
      </nav>

      <div className="login-card-wrapper">
        <div className="login-card" ref={cardRef}>
        <div className="login-illustration" ref={illustrationRef}>
          <div className="illustration-bg">
            <img 
              src="/images/Currency Crush - Analytics (1).png" 
              alt="Analytics Dashboard" 
              className="analytics-image"
            />
          </div>
        </div>

        <div className="login-content">
          <div className="login-header">
            <div className="login-header-brand">
              <FaBolt className="login-header-icon" />
              <h1>Electricity Logger</h1>
            </div>
            <p>{isLogin ? 'Welcome back! Sign in to continue tracking your electricity supply.' : 'Create your account to start monitoring your electricity data'}</p>
          </div>
          
          {/* Email verification UI temporarily disabled - kept for easy restoration */}
            <form onSubmit={handleSubmit} className="login-form">
              <div className="form-group">
                <input
                  type="text"
                  placeholder={isLogin ? "Email or Username" : "Username"}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              
              {!isLogin && (
                <>
                  <div className="form-group">
                    <input
                      type="email"
                      placeholder="Email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <LocationAutocomplete
                      value={location}
                      onChange={setLocation}
                      onSelect={handleLocationSelect}
                      placeholder="Enter your location (e.g., Lagos, Nigeria)"
                      required
                    />
                  </div>
                </>
              )}
              
              <div className="form-group">
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              
              {error && <div className="error-message">{error}</div>}
              
              <button type="submit" disabled={loading} className="submit-btn">
                {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register')}
              </button>
            </form>
          
          <div className="toggle-auth">
            <p>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <span onClick={() => {
                setIsLogin(!isLogin);
                setError('');
                // setShowVerification(false);
                // setVerificationCode('');
                // setFallbackCode('');
                // setEmailSent(true);
                setEmail('');
                setLocation('');
              }} className="toggle-link">
                {isLogin ? 'Register' : 'Login'}
              </span>
            </p>
          </div>
        </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="login-footer">
        <div className="login-footer-container">
          <div className="login-footer-section">
            <div className="login-footer-brand">
              <FaBolt className="login-footer-brand-icon" />
              <span>Electricity Logger</span>
            </div>
            <p className="login-footer-description">
              Track and analyze your electricity supply patterns with precision.
            </p>
            <div className="login-footer-social">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><FaFacebook /></a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter"><FaTwitter /></a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><FaLinkedin /></a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" aria-label="GitHub"><FaGithub /></a>
            </div>
          </div>
          <div className="login-footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/#features">Features</a></li>
              <li><a href="/privacy">Privacy Policy</a></li>
              <li><a href="/terms">Terms of Service</a></li>
            </ul>
          </div>
          <div className="login-footer-section">
            <h4>Contact</h4>
            <ul className="login-footer-contact">
              <li><FaEnvelope /> support@electricitylogger.com</li>
              <li><FaPhone /> +229 98 59 72 34</li>
              <li><FaMapMarkerAlt /> ESTAM UNIVERSITY TUNDE MOTORS</li>
            </ul>
          </div>
        </div>
        <div className="login-footer-bottom">
          <p>&copy; {new Date().getFullYear()} Salomon Ridwan and Ebenezer of ESTAM University. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Login;
