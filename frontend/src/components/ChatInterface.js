import React, { useState, useEffect, useRef } from 'react';
import api from '../services/api';
import './ChatInterface.css';

const ChatInterface = ({ onLogEvent }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
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
      setLoading(true);
      const response = await api.get('/report');
      const report = response.data;
      
      const userMessage = {
        id: Date.now(),
        text: 'report',
        timestamp: new Date().toLocaleString(),
        type: 'user',
        isUser: true
      };
      setMessages(prev => [...prev, userMessage]);
      
      // Format report message
      const lastEventText = report.summary.last_event.type 
        ? `Last event: Power ${report.summary.last_event.type.toUpperCase()} (${report.summary.last_event.hours_ago} hours ago)`
        : 'No events logged yet';
      
      const reportText = `📊 ELECTRICITY REPORT

Today: ${report.summary.today_hours} hours
This Week: ${report.summary.week_hours} hours
This Month: ${report.summary.month_hours} hours
Average Daily: ${report.summary.avg_daily_hours} hours/day

${lastEventText}

Total Events:
• Today: ${report.totals.today_events}
• This Week: ${report.totals.week_events}
• This Month: ${report.totals.month_events}`;
      
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          text: reportText,
          timestamp: new Date().toLocaleString(),
          type: 'report',
          isUser: false
        };
        setMessages(prev => [...prev, botMessage]);
      }, 500);
      
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
    }
  };

  const logPowerEvent = async (eventType) => {
    try {
      setLoading(true);
      await api.post('/log-power', { event_type: eventType });
      
      const newMessage = {
        id: Date.now(),
        text: `Power turned ${eventType.toUpperCase()}`,
        timestamp: new Date().toLocaleString(),
        type: eventType,
        isUser: true
      };
      
      setMessages(prev => [...prev, newMessage]);
      
      // Add bot confirmation
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          text: `✓ Logged! Power is now ${eventType === 'on' ? 'ON' : 'OFF'}`,
          timestamp: new Date().toLocaleString(),
          type: 'info',
          isUser: false
        };
        setMessages(prev => [...prev, botMessage]);
      }, 500);
      
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
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const lowerInput = input.toLowerCase().trim();
    
    if (lowerInput === 'report' || lowerInput === 'summary') {
      fetchReport();
      setInput('');
    } else if (lowerInput.includes('power on') || (lowerInput.includes('on') && !lowerInput.includes('off'))) {
      logPowerEvent('on');
      setInput('');
    } else if (lowerInput.includes('power off') || lowerInput.includes('off')) {
      logPowerEvent('off');
      setInput('');
    } else {
      const userMessage = {
        id: Date.now(),
        text: input,
        timestamp: new Date().toLocaleString(),
        type: 'user',
        isUser: true
      };
      setMessages(prev => [...prev, userMessage]);
      
      // Bot response
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          text: 'Type "power on" or "power off" to log electricity events. Type "report" for a summary. Or use the buttons below.',
          timestamp: new Date().toLocaleString(),
          type: 'info',
          isUser: false
        };
        setMessages(prev => [...prev, botMessage]);
      }, 500);
      
      setInput('');
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
              <div className="message-text">{message.text}</div>
              <div className="message-timestamp">{message.timestamp}</div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="quick-actions">
        <button
          onClick={() => logPowerEvent('on')}
          disabled={loading}
          className="action-btn power-on"
        >
          💡 Power ON
        </button>
        <button
          onClick={() => logPowerEvent('off')}
          disabled={loading}
          className="action-btn power-off"
        >
          ⚫ Power OFF
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type 'power on', 'power off', or 'report'..."
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading || !input.trim()} className="send-btn">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;

