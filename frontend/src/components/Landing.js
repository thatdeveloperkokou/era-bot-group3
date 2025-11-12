import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
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

gsap.registerPlugin(ScrollTrigger);

// Accordion Component for How It Works
const AccordionSteps = () => {
  const [activeIndex, setActiveIndex] = useState(0);

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
    const interval = setInterval(() => {
      setActiveIndex((prevIndex) => (prevIndex + 1) % steps.length);
    }, 4000); // Switch every 4 seconds

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="accordion-container">
      {steps.map((step, index) => (
        <div
          key={index}
          className={`accordion-card ${activeIndex === index ? 'active' : ''}`}
          onClick={() => setActiveIndex(index)}
        >
          <div className="accordion-header">
            <div className="accordion-number">{step.number}</div>
            <h3 className="accordion-title">{step.title}</h3>
          </div>
          <div className="accordion-content">
            <p>{step.description}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

const Landing = () => {
  const navigate = useNavigate();
  const heroRef = useRef(null);
  const featuresRef = useRef(null);
  const titleRef = useRef(null);
  const subtitleRef = useRef(null);
  const ctaRef = useRef(null);
  const statsRef = useRef(null);

  useEffect(() => {
    // CSS animations handle hero section (transform only, no opacity changes)
    // GSAP only for scroll-triggered animations (features, stats)

    // Capture ref values at the start of the effect
    const featuresElement = featuresRef.current;
    const statsElement = statsRef.current;

    // Features animation (scroll-triggered, so opacity animation is OK)
    if (featuresElement && featuresElement.children) {
      gsap.fromTo(featuresElement.children,
        {
          y: 40,
          opacity: 0
        },
        {
          duration: 1,
          y: 0,
          opacity: 1,
          stagger: 0.15,
          delay: 0.3,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: featuresElement,
            start: 'top 85%',
            toggleActions: 'play none none reverse'
          },
          onComplete: function() {
            // Ensure final opacity is 1
            this.targets().forEach(target => {
              if (target) {
                target.style.setProperty('opacity', '1', 'important');
              }
            });
          }
        }
      );
    }

    // Stats animation (scroll-triggered)
    if (statsElement && statsElement.children) {
      gsap.fromTo(statsElement.children,
        {
          scale: 0.9,
          opacity: 0,
          y: 20
        },
        {
          duration: 1,
          scale: 1,
          opacity: 1,
          y: 0,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: statsElement,
            start: 'top 85%',
            toggleActions: 'play none none reverse'
          },
          onComplete: function() {
            this.targets().forEach(target => {
              if (target) {
                target.style.setProperty('opacity', '1', 'important');
              }
            });
          }
        }
      );
    }

    return () => {
      // Clean up any GSAP animations using captured values
      if (featuresElement) gsap.killTweensOf(featuresElement.children);
      if (statsElement) gsap.killTweensOf(statsElement.children);
    };
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
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-container">
          <div className="navbar-brand">
            <FaBolt className="brand-icon" />
            <span>Electricity Logger</span>
          </div>
          <div className="navbar-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#use-cases">Use Cases</a>
            <button 
              className="navbar-link-button"
              onClick={() => navigate('/login?mode=login')}
            >
              Sign In
            </button>
            <button 
              className="navbar-cta"
              onClick={() => navigate('/login?mode=register')}
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section 
        className="hero-section" 
        ref={heroRef}
        style={{
          backgroundImage: `url('/images/2025-11-12%2012.29.png')`
        }}
      >
        <div className="hero-content">
          <h1 className="hero-title" ref={titleRef}>
            Take Control of Your Electricity Supply
          </h1>
          <p className="hero-subtitle" ref={subtitleRef}>
            The most advanced electricity tracking platform for monitoring power outages, 
            analyzing supply patterns, and making data-driven decisions. Trusted by thousands 
            of users to track and optimize their electricity consumption.
          </p>
          <div className="hero-cta" ref={ctaRef}>
            <button 
              className="cta-button primary"
              onClick={() => navigate('/login?mode=register')}
            >
              Start Free Trial
            </button>
          </div>
          <div className="hero-trust">
            <p>Trusted by leading organizations</p>
            <div className="trust-badges">
              <span><FaLock className="trust-icon" /> Secure</span>
              <span><FaCheckCircle className="trust-icon" /> Verified</span>
              <span><FaStar className="trust-icon" /> 4.9/5 Rating</span>
            </div>
          </div>
        </div>
        <div className="hero-image">
          <div className="illustration-container">
            <img 
              src="/images/2025-11-13 00.05(1).jpeg" 
              alt="Solar Energy House" 
              className="country-svg"
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container" ref={statsRef}>
          {stats.map((stat, index) => (
            <div key={index} className="stat-item">
              <div className="stat-number">{stat.number}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section 
        id="features" 
        className="features-section"
        style={{
          backgroundImage: `url('/images/2025-11-12%2013.48%20(1).jpg')`
        }}
      >
        <div className="section-header">
          <h2 className="section-title">Powerful Features for Modern Electricity Management</h2>
          <p className="section-subtitle">
            Everything you need to track, analyze, and optimize your electricity supply 
            in one comprehensive platform
          </p>
        </div>
        <div className="features-grid" ref={featuresRef}>
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section - Accordion */}
      <section id="how-it-works" className="how-it-works">
        <div className="section-header">
          <h2 className="section-title">Simple Setup, Powerful Results</h2>
          <p className="section-subtitle">
            Get started in minutes and begin tracking your electricity supply immediately
          </p>
        </div>
        <AccordionSteps />
      </section>

      {/* Use Cases Section */}
      <section 
        id="use-cases" 
        className="use-cases-section"
        style={{
          backgroundImage: `url('/images/2025-11-12%2013.48.jpg')`
        }}
      >
        <div className="section-header">
          <h2 className="section-title">Built for Everyone</h2>
          <p className="section-subtitle">
            Whether you're a homeowner, business owner, or researcher, our platform adapts to your needs
          </p>
        </div>
        <div className="use-cases-grid">
          <div className="use-case-card">
            <FaHome className="use-case-icon" />
            <h3>Homeowners</h3>
            <p>Track your home's electricity supply, plan your daily activities around power availability, and hold utility companies accountable with accurate data.</p>
          </div>
          <div className="use-case-card">
            <FaBriefcase className="use-case-icon" />
            <h3>Businesses</h3>
            <p>Monitor power outages affecting your operations, generate reports for insurance claims, and optimize your business continuity planning.</p>
          </div>
          <div className="use-case-card">
            <FaUserGraduate className="use-case-icon" />
            <h3>Researchers</h3>
            <p>Collect comprehensive data for electricity supply research, analyze regional patterns, and contribute to grid reliability studies.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2>Ready to Transform Your Electricity Tracking?</h2>
        <p>Join thousands of users who are already taking control of their electricity supply data</p>
        <button 
          className="cta-button primary large"
          onClick={() => navigate('/login?mode=register')}
        >
          Get Started Today
        </button>
        <p className="cta-note">No credit card required • Free forever plan available</p>
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
