import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';

function App() {
  const [data, setData] = useState({ rolling_bullish_score: 0, latest_news: [] });
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/sentiment/live');
        const result = await response.json();
        setData(result);
        setHistory(prev => [...prev.slice(-19), { time: new Date().toLocaleTimeString(), score: result.rolling_bullish_score }]);
      } catch (err) { console.error("API not ready yet..."); }
    };
    const interval = setInterval(fetchData, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '40px', backgroundColor: '#0f172a', color: 'white', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <h1 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Activity /> AI Market Pulse</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', marginTop: '30px' }}>
        <div style={{ padding: '20px', backgroundColor: '#1e293b', borderRadius: '12px', textAlign: 'center' }}>
          <h2>Market Sentiment</h2>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: data.rolling_bullish_score > 50 ? '#22c55e' : '#ef4444' }}>
            {data.rolling_bullish_score}%
          </div>
          <p>{data.rolling_bullish_score > 50 ? 'BULLISH' : 'BEARISH'}</p>
        </div>

        <div style={{ height: '300px', backgroundColor: '#1e293b', padding: '20px', borderRadius: '12px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none' }} />
              <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ marginTop: '40px' }}>
        <h3>Live AI Analysis Feed</h3>
        {data.latest_news.map((news, i) => (
          <div key={i} style={{ padding: '15px', borderBottom: '1px solid #334155', display: 'flex', justifyContent: 'space-between' }}>
            <span>{news.headline}</span>
            <span style={{ color: news.sentiment === 'positive' ? '#22c55e' : news.sentiment === 'negative' ? '#ef4444' : '#94a3b8', fontWeight: 'bold' }}>
              {news.sentiment.toUpperCase()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
export default App;