import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function SalaryChart({ token }) {
  const [data, setData] = useState([]);
// eslint-disable-next-line
  useEffect(() => {
    fetch('https://talentiq-rs7t.onrender.com/salary-distribution', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setData(data));
  }, []);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Salary Distribution by Department (AED)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="department" angle={-35} textAnchor="end" tick={{ fontSize: 11 }} />
          <YAxis tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
          <Tooltip formatter={(value) => `AED ${value.toLocaleString()}`} />
          <Legend verticalAlign="top" />
          <Bar dataKey="min" name="Min Salary" fill="#A8D8EA" radius={[4, 4, 0, 0]} />
          <Bar dataKey="avg" name="Avg Salary" fill="#1F4E79" radius={[4, 4, 0, 0]} />
          <Bar dataKey="max" name="Max Salary" fill="#2E86AB" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

const styles = {
  card: {
    background: '#fff',
    borderRadius: '10px',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.07)',
    marginBottom: '24px',
  },
  title: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#1F4E79',
    marginBottom: '16px',
  },
};

export default SalaryChart;