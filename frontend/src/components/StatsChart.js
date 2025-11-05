import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './StatsChart.css';

const StatsChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="no-chart-data">No data to display</div>;
  }

  // Format dates for display
  const formattedData = data.map(item => ({
    ...item,
    dateLabel: new Date(item.date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    })
  }));

  return (
    <div className="stats-chart">
      <h3>Daily Hours Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis
            dataKey="dateLabel"
            stroke="#666"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            stroke="#666"
            label={{ value: 'Hours', angle: -90, position: 'insideLeft' }}
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e0e0e0',
              borderRadius: '8px',
              padding: '10px'
            }}
            formatter={(value) => [`${value} hours`, 'Light Hours']}
          />
          <Legend />
          <Bar
            dataKey="hours"
            fill="url(#colorGradient)"
            radius={[8, 8, 0, 0]}
          />
          <defs>
            <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#667eea" stopOpacity={1} />
              <stop offset="100%" stopColor="#764ba2" stopOpacity={1} />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
      
      <div className="chart-line-container">
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis
              dataKey="dateLabel"
              stroke="#666"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              stroke="#666"
              label={{ value: 'Hours', angle: -90, position: 'insideLeft' }}
              style={{ fontSize: '12px' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                padding: '10px'
              }}
              formatter={(value) => [`${value} hours`, 'Light Hours']}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="hours"
              stroke="#667eea"
              strokeWidth={3}
              dot={{ fill: '#764ba2', r: 5 }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default StatsChart;

