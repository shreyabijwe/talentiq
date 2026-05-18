import React, { useState } from 'react';

function ReportsPage({ token }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const generateReport = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch('https://talentiq-rs7t.onrender.com/generate-report', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setMessage('✅ ' + data.message);
    } catch (err) {
      setMessage('❌ Failed to generate report. Make sure API is running.');
    }
    setLoading(false);
  };

  return (
    <div>
      <h2 style={styles.title}>Report Generator</h2>
      <div style={styles.card}>
        <h3 style={styles.cardTitle}>Monthly HR Report</h3>
        <p style={styles.desc}>Generate a complete HR analytics report including KPIs, attrition analysis, salary benchmarking and executive summary.</p>
        <button style={styles.button} onClick={generateReport} disabled={loading}>
          {loading ? 'Generating...' : '📊 Generate Excel Report'}
        </button>
        {message && <p style={styles.message}>{message}</p>}
      </div>
    </div>
  );
}

const styles = {
  title: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1F4E79',
    marginBottom: '24px',
  },
  card: {
    background: '#fff',
    borderRadius: '10px',
    padding: '32px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.07)',
    maxWidth: '500px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#1F4E79',
    marginBottom: '12px',
  },
  desc: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '24px',
    lineHeight: '1.6',
  },
  button: {
    padding: '12px 24px',
    background: '#1F4E79',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  message: {
    marginTop: '16px',
    fontSize: '14px',
    color: '#27ae60',
  },
};

export default ReportsPage;