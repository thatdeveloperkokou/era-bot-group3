import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaChartBar, 
  FaMobileAlt, 
  FaChartLine, 
  FaGlobe, 
  FaLock, 
  FaBolt,
  FaCheckCircle,
  FaStar,
  FaEnvelope,
  FaPhone,
  FaMapMarkerAlt,
  FaFacebook,
  FaTwitter,
  FaLinkedin,
  FaGithub,
  FaHome,
  FaBriefcase,
  FaUserGraduate
} from 'react-icons/fa';
import './Landing.css';
import ThunderboltCursor from './ThunderboltCursor';

const TypingHeading = ({ text, speed = 55, delay = 150 }) => {
  const [displayed, setDisplayed] = useState('');
  const spanRef = useRef(null);
  const intervalRef = useRef(null);
  const timeoutRef = useRef(null);
  const hasStartedRef = useRef(false);

  useEffect(() => {
    setDisplayed('');
    hasStartedRef.current = false;

    const startTyping = () => {
      if (hasStartedRef.current) return;
      hasStartedRef.current = true;
      let index = 0;
      timeoutRef.current = setTimeout(() => {
        intervalRef.current = setInterval(() => {
          index += 1;
          setDisplayed(text.slice(0, index));
          if (index >= text.length) {
            clearInterval(intervalRef.current);
          }
        }, speed);
      }, delay);
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            startTyping();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );

    if (spanRef.current) {
      observer.observe(spanRef.current);
    } else {
      startTyping();
    }

    return () => {
      observer.disconnect();
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [text, speed, delay]);

  return (
    <span className="typing-heading" aria-label={text} ref={spanRef}>
      {displayed}
      {displayed.length < text.length && (
        <span className="typing-caret" aria-hidden="true">|</span>
      )}
    </span>
  );
};

// Accordion Component for How It Works
const AccordionSteps = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const intervalRef = useRef(null);

  const steps = [
    {
      number: '1',
      title: 'Create Your Account',
      description: 'Sign up with your email and location. We\'ll verify your identity to ensure secure access to your data.'
    },
    {
      number: '2',
      title: 'Start Logging Events',
      description: 'Use our intuitive interface to log power ON/OFF events. Choose from quick buttons or natural language commands for maximum convenience.'
    },
    {
      number: '3',
      title: 'Analyze & Optimize',
      description: 'View comprehensive analytics, identify patterns, and make informed decisions about your electricity usage with real-time data visualization.'
    }
  ];

  useEffect(() => {
    const startInterval = () => {
      intervalRef.current = setInterval(() => {
        setActiveIndex((prevIndex) => (prevIndex + 1) % steps.length);
      }, 6000);
    };

    startInterval();

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [steps.length]);

  const handleSelect = (index) => {
    setActiveIndex(index);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = setInterval(() => {
        setActiveIndex((prevIndex) => (prevIndex + 1) % steps.length);
      }, 6000);
    }
  };

  const handleKeyDown = (event, index) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleSelect(index);
    }
  };

  const progressWidth = ((activeIndex + 1) / steps.length) * 100;

  return (
    <div className="accordion-container">
      <div className="steps-progress">
        <div className="steps-progress-label">
          <span data-grayscale-target>Step {activeIndex + 1} of {steps.length}</span>
        </div>
        <div className="steps-progress-track">
          <div
            className="steps-progress-thumb"
            style={{ width: `${progressWidth}%` }}
          />
        </div>
      </div>
      {steps.map((step, index) => (
        <div
          key={index}
          className={`accordion-card ${activeIndex === index ? 'active' : ''}`}
          onClick={() => handleSelect(index)}
          onMouseEnter={() => handleSelect(index)}
          onFocus={() => handleSelect(index)}
          onKeyDown={(event) => handleKeyDown(event, index)}
          role="button"
          tabIndex={0}
          aria-expanded={activeIndex === index}
        >
          <div className="accordion-header">
            <div className="accordion-number">{step.number}</div>
            <div className="accordion-copy">
              <p className="accordion-eyebrow" data-grayscale-target>Step {step.number}</p>
              <h3 className="accordion-title" data-grayscale-target>{step.title}</h3>
            </div>
          </div>
          <div className="accordion-content">
            <p className="accordion-description" data-grayscale-target>
              {step.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

const Landing = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const animatedElements = document.querySelectorAll('[data-animate-on-scroll]');
    if (!animatedElements.length) return;

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            obs.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
      }
    );

    animatedElements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  const handleSmoothScroll = useCallback((event, selector) => {
    event.preventDefault();
    const target = document.querySelector(selector);
    if (target) {
      const navbarOffset = 80;
      const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarOffset;
      window.scrollTo({ top: targetPosition, behavior: 'smooth' });
    }
  }, []);

  const features = [
    {
      icon: <FaChartBar />,
      title: 'Precise Power Analytics',
      description: 'Advanced data tracking and analytics engine that captures every power event with millisecond precision. Generate comprehensive reports showing daily, weekly, and monthly electricity supply patterns.'
    },
    {
      icon: <FaMobileAlt />,
      title: 'Intuitive Interface',
      description: 'Streamlined user experience designed for speed and simplicity. Log power events with a single tap or use natural language commands. Built for both technical and non-technical users.'
    },
    {
      icon: <FaChartLine />,
      title: 'Real-Time Visualization',
      description: 'Interactive charts and graphs that transform raw data into actionable insights. Identify trends, patterns, and anomalies in your electricity supply with beautiful, easy-to-understand visualizations.'
    },
    {
      icon: <FaGlobe />,
      title: 'Location-Based Intelligence',
      description: 'Regional electricity tracking powered by geographic data. Compare supply patterns across locations and prepare for future API integration with regional electricity grid monitoring systems.'
    },
    {
      icon: <FaLock />,
      title: 'Enterprise-Grade Security',
      description: 'Bank-level encryption and secure authentication protocols. Your data is protected with JWT tokens, device verification, and email confirmation. Complete privacy and data sovereignty.'
    },
    {
      icon: <FaBolt />,
      title: 'Instant Notifications',
      description: 'Real-time updates and automated reporting. Stay informed about your electricity supply status with instant notifications and comprehensive daily summaries delivered to your inbox.'
    }
  ];

  const stats = [
    { number: '10K+', label: 'Active Users' },
    { number: '500K+', label: 'Events Logged' },
    { number: '99.9%', label: 'Uptime' },
    { number: '24/7', label: 'Support' }
  ];

  return (
    <div className="landing-page">
      <ThunderboltCursor />
      
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-brand">
            <FaBolt className="brand-icon" />
            <span className="brand-text">Electricity Logger</span>
          </div>
          <div className="navbar-links">
            <a
              href="#features"
              className="nav-link"
              onClick={(event) => handleSmoothScroll(event, '#features')}
            >
              <span className="nav-link-text">Features</span>
              <FaChartBar className="nav-link-icon" />
            </a>
            <a
              href="#how-it-works"
              className="nav-link"
              onClick={(event) => handleSmoothScroll(event, '#how-it-works')}
            >
              <span className="nav-link-text">How It Works</span>
              <FaBolt className="nav-link-icon" />
            </a>
            <a
              href="#use-cases"
              className="nav-link"
              onClick={(event) => handleSmoothScroll(event, '#use-cases')}
            >
              <span className="nav-link-text">Use Cases</span>
              <FaBriefcase className="nav-link-icon" />
            </a>
            <button 
              className="navbar-link-button"
              onClick={() => navigate('/login?mode=login')}
            >
              <span className="nav-link-text">Sign In</span>
              <FaUserGraduate className="nav-link-icon" />
            </button>
            <button 
              className="navbar-cta"
              onClick={() => navigate('/login?mode=register')}
            >
              <span className="nav-link-text">Get Started</span>
              <FaBolt className="nav-link-icon" />
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section 
        className="hero-section" 
        style={{
          backgroundImage: `url(${encodeURI('/images/2025-11-12 12.29.png')})`
        }}
      >
        <div className="hero-content animate-on-scroll" data-animate-on-scroll>
          <h1 className="hero-title" data-grayscale-target>
            Take Control of Your Electricity Supply
          </h1>
          <p className="hero-subtitle" data-grayscale-target>
            The most advanced electricity tracking platform for monitoring power outages, 
            analyzing supply patterns, and making data-driven decisions. Trusted by thousands 
            of users to track and optimize their electricity consumption.
          </p>
          <div className="hero-cta">
            <button 
              className="cta-button primary hero-bounce"
              onClick={() => navigate('/login?mode=register')}
            >
              Start Free Trial
            </button>
          </div>
          <div className="hero-trust">
            <p data-grayscale-target>Trusted by leading organizations</p>
            <div className="trust-badges">
              <span data-grayscale-target><FaLock className="trust-icon" /> Secure</span>
              <span data-grayscale-target><FaCheckCircle className="trust-icon" /> Verified</span>
              <span data-grayscale-target><FaStar className="trust-icon" /> 4.9/5 Rating</span>
            </div>
          </div>
        </div>
        <div className="hero-image animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '120ms' }}>
          <div className="illustration-container">
            <img 
              src={encodeURI('/images/2025-11-13 00.05(1).jpeg')} 
              alt="Solar Energy House" 
              className="country-svg"
            />
          </div>
        </div>
        <div className="scroll-indicator animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '240ms' }}>
          <button 
            type="button" 
            className="scroll-indicator-button"
            onClick={(event) => handleSmoothScroll(event, '#features')}
          >
            Scroll to explore
          </button>
          <div className="scroll-indicator-track">
            <div className="scroll-indicator-dot"></div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section animate-on-scroll" data-animate-on-scroll>
        <div className="stats-container">
          {stats.map((stat, index) => (
            <div 
              key={index} 
              className="stat-item animate-on-scroll" 
              data-animate-on-scroll
              style={{ transitionDelay: `${index * 80}ms` }}
            >
              <div className="stat-number" data-grayscale-target>{stat.number}</div>
              <div className="stat-label" data-grayscale-target>{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section 
        id="features" 
        className="features-section animate-on-scroll"
        data-animate-on-scroll
        style={{
          backgroundImage: `url(${encodeURI('/images/2025-11-12 13.48 (1).jpg')})`
        }}
      >
        <div className="section-header animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '80ms' }}>
          <h2 className="section-title" data-grayscale-target>Powerful Features for Modern Electricity Management</h2>
          <p className="section-subtitle" data-grayscale-target>
            Everything you need to track, analyze, and optimize your electricity supply 
            in one comprehensive platform
          </p>
        </div>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div 
              key={index} 
              className="feature-card animate-on-scroll"
              data-animate-on-scroll
              style={{ transitionDelay: `${index * 100}ms` }}
            >
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title" data-grayscale-target>{feature.title}</h3>
              <p className="feature-description" data-grayscale-target>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section - Accordion */}
      <section id="how-it-works" className="how-it-works animate-on-scroll" data-animate-on-scroll>
        <div className="section-header animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '80ms' }}>
          <h2 className="section-title" data-grayscale-target>Simple Setup, Powerful Results</h2>
          <p className="section-subtitle" data-grayscale-target>
            Get started in minutes and begin tracking your electricity supply immediately
          </p>
        </div>
        <AccordionSteps />
      </section>

      {/* Use Cases Section */}
      <section 
        id="use-cases" 
        className="use-cases-section animate-on-scroll"
        data-animate-on-scroll
        style={{
          backgroundImage: `url(${encodeURI('/images/2025-11-12 13.48.jpg')})`
        }}
      >
        <div className="section-header animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '80ms' }}>
          <h2 className="section-title">Built for Everyone</h2>
          <p className="section-subtitle">
            Whether you're a homeowner, business owner, or researcher, our platform adapts to your needs
          </p>
        </div>
        <div className="use-cases-grid">
          <div className="use-case-card animate-on-scroll" data-animate-on-scroll>
            <FaHome className="use-case-icon" />
            <h3 data-grayscale-target>Homeowners</h3>
            <p data-grayscale-target>Track your home's electricity supply, plan your daily activities around power availability, and hold utility companies accountable with accurate data.</p>
          </div>
          <div className="use-case-card animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '100ms' }}>
            <FaBriefcase className="use-case-icon" />
            <h3 data-grayscale-target>Businesses</h3>
            <p data-grayscale-target>Monitor power outages affecting your operations, generate reports for insurance claims, and optimize your business continuity planning.</p>
          </div>
          <div className="use-case-card animate-on-scroll" data-animate-on-scroll style={{ transitionDelay: '200ms' }}>
            <FaUserGraduate className="use-case-icon" />
            <h3 data-grayscale-target>Researchers</h3>
            <p data-grayscale-target>Collect comprehensive data for electricity supply research, analyze regional patterns, and contribute to grid reliability studies.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section animate-on-scroll" data-animate-on-scroll>
        <h2 data-grayscale-target>
          <TypingHeading text="Ready to Transform Your Electricity Tracking?" />
        </h2>
        <p data-grayscale-target>Join thousands of users who are already taking control of their electricity supply data</p>
        <button 
          className="cta-button primary large"
          onClick={() => navigate('/login?mode=register')}
        >
          Get Started Today
        </button>
        <p className="cta-note" data-grayscale-target>No credit card required • Free forever plan available</p>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-section">
            <div className="footer-brand">
              <FaBolt className="footer-brand-icon" />
              <span>Electricity Logger</span>
            </div>
            <p className="footer-description">
              The most advanced electricity tracking platform for monitoring power outages 
              and analyzing supply patterns.
            </p>
            <div className="footer-social">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><FaFacebook /></a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter"><FaTwitter /></a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><FaLinkedin /></a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" aria-label="GitHub"><FaGithub /></a>
            </div>
          </div>
          <div className="footer-section">
            <h4>Product</h4>
            <ul>
              <li><a href="#features">Features</a></li>
              <li><a href="#how-it-works">How It Works</a></li>
              <li><a href="#use-cases">Use Cases</a></li>
              <li><a href="/login">Pricing</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li><a href="/about">About Us</a></li>
              <li><a href="/blog">Blog</a></li>
              <li><a href="/careers">Careers</a></li>
              <li><a href="/contact">Contact</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li><a href="/help">Help Center</a></li>
              <li><a href="/docs">Documentation</a></li>
              <li><a href="/privacy">Privacy Policy</a></li>
              <li><a href="/terms">Terms of Service</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <ul className="footer-contact">
              <li><FaEnvelope /> support@electricitylogger.com</li>
              <li><FaPhone /> +229 98 59 72 34</li>
              <li><FaMapMarkerAlt /> ESTAM UNIVERSITY TUNDE MOTORS</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} Salomon Ridwan and Ebenezer of ESTAM University. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
