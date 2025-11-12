import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import { FaLightbulb, FaPowerOff, FaCheckCircle, FaChartBar } from 'react-icons/fa';
import './ChatInterface.css';

const ChatInterface = ({ onLogEvent }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    fetchRecentEvents();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchRecentEvents = async () => {
    try {
      const response = await api.get('/recent-events?limit=20');
      const events = response.data.events.reverse();
      
      const formattedMessages = events.map(event => ({
        id: event.timestamp,
        text: `Power turned ${event.event_type === 'on' ? 'ON' : 'OFF'}`,
        timestamp: new Date(event.timestamp).toLocaleString(),
        type: event.event_type,
        isUser: true
      }));

      if (formattedMessages.length === 0) {
        setMessages([{
          id: 'welcome',
          text: 'Welcome! Use the buttons below or type "power on" / "power off" to log electricity events. Type "report" for a summary.',
          timestamp: new Date().toLocaleString(),
          type: 'info',
          isUser: false
        }]);
      } else {
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  const fetchReport = async () => {
    try {
      setIsProcessing(true);
      setLoading(true);
      
      const userMessage = {
        id: Date.now(),
        text: 'report',
        timestamp: new Date().toLocaleString(),
        type: 'user',
        isUser: true
      };
      setMessages(prev => [...prev, userMessage]);
      
      // Show loading indicator for a moment
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const response = await api.get('/report');
      const report = response.data;
      
      // Format report message
      const lastEventText = report.summary.last_event.type 
        ? `Last event: Power ${report.summary.last_event.type.toUpperCase()} (${report.summary.last_event.hours_ago} hours ago)`
        : 'No events logged yet';
      
      const reportText = `ELECTRICITY REPORT

Today: ${report.summary.today_hours} hours
This Week: ${report.summary.week_hours} hours
This Month: ${report.summary.month_hours} hours
Average Daily: ${report.summary.avg_daily_hours} hours/day

${lastEventText}

Total Events:
• Today: ${report.totals.today_events}
• This Week: ${report.totals.week_events}
• This Month: ${report.totals.month_events}`;
      
      const botMessage = {
        id: Date.now() + 1,
        text: reportText,
        timestamp: new Date().toLocaleString(),
        type: 'report',
        isUser: false,
        icon: <FaChartBar />
      };
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        text: 'Error fetching report. Please try again.',
        timestamp: new Date().toLocaleString(),
        type: 'error',
        isUser: false
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setIsProcessing(false);
    }
  };

  const logPowerEvent = async (eventType) => {
    try {
      setIsProcessing(true);
      setLoading(true);
      
      const newMessage = {
        id: Date.now(),
        text: `Power turned ${eventType.toUpperCase()}`,
        timestamp: new Date().toLocaleString(),
        type: eventType,
        isUser: true
      };
      
      setMessages(prev => [...prev, newMessage]);
      
      // Show loading indicator for a moment
      await new Promise(resolve => setTimeout(resolve, 800));
      
      await api.post('/log-power', { event_type: eventType });
      
      // Add bot confirmation
      const botMessage = {
        id: Date.now() + 1,
        text: `Logged! Power is now ${eventType === 'on' ? 'ON' : 'OFF'}`,
        timestamp: new Date().toLocaleString(),
        type: 'info',
        isUser: false,
        icon: <FaCheckCircle />
      };
      setMessages(prev => [...prev, botMessage]);
      
      if (onLogEvent) {
        onLogEvent();
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        text: 'Error logging event. Please try again.',
        timestamp: new Date().toLocaleString(),
        type: 'error',
        isUser: false
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setIsProcessing(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading || isProcessing) return;

    const lowerInput = input.toLowerCase().trim();
    const userInput = input.trim();
    
    // Save user message immediately
    const userMessage = {
      id: Date.now(),
      text: userInput,
      timestamp: new Date().toLocaleString(),
      type: 'user',
      isUser: true
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    // Show loading indicator
    setIsProcessing(true);
    
    // Small delay to show loading state
    await new Promise(resolve => setTimeout(resolve, 600));
    
    if (lowerInput === 'report' || lowerInput === 'summary') {
      await fetchReport();
    } else if (lowerInput.includes('power on') || (lowerInput.includes('on') && !lowerInput.includes('off'))) {
      await logPowerEvent('on');
    } else if (lowerInput.includes('power off') || lowerInput.includes('off')) {
      await logPowerEvent('off');
    } else {
      // Bot response for unrecognized commands
      const botMessage = {
        id: Date.now() + 1,
        text: 'Type "power on" or "power off" to log electricity events. Type "report" for a summary. Or use the buttons below.',
        timestamp: new Date().toLocaleString(),
        type: 'info',
        isUser: false
      };
      setMessages(prev => [...prev, botMessage]);
      setIsProcessing(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Power Logging</h2>
        <p>Log your electricity supply events</p>
      </div>
      
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.isUser ? 'user-message' : 'bot-message'} ${message.type}`}
          >
            <div className="message-content">
              <div className="message-text">
                {message.icon && <span className="message-icon">{message.icon}</span>}
                <span>{message.text}</span>
              </div>
              <div className="message-timestamp">{message.timestamp}</div>
            </div>
          </div>
        ))}
        {isProcessing && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="message-text">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="quick-actions">
        <button
          onClick={() => logPowerEvent('on')}
          disabled={loading}
          className="action-btn power-on"
        >
          <FaLightbulb className="action-icon" />
          Power ON
        </button>
        <button
          onClick={() => logPowerEvent('off')}
          disabled={loading}
          className="action-btn power-off"
        >
          <FaPowerOff className="action-icon" />
          Power OFF
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type 'power on', 'power off', or 'report'..."
          disabled={loading || isProcessing}
          className="chat-input"
        />
        <button type="submit" disabled={loading || isProcessing || !input.trim()} className="send-btn">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;

