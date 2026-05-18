import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function AttritionChart({ token }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('https://talentiq-rs7t.onrender.com/attrition-by-dept', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setData(data));
  }, []);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Attrition Rate by Department</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="department" angle={-35} textAnchor="end" tick={{ fontSize: 11 }} />
          <YAxis tickFormatter={(v) => `${v}%`} />
          <Tooltip formatter={(value) => `${value}%`} />
          <Bar dataKey="attrition_rate" fill="#1F4E79" radius={[4, 4, 0, 0]} />
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
  },
  title: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#1F4E79',
    marginBottom: '16px',
  },
};

export default AttritionChart;