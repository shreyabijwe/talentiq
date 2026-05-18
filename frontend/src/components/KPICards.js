import React from 'react';

function KPICards({ kpis }) {
  if (!kpis) return null;

  const cards = [
    { label: 'Total Employees', value: kpis.total_employees.toLocaleString(), color: '#1F4E79', icon: '👥' },
    { label: 'Avg Salary (AED)', value: `${kpis.avg_salary.toLocaleString()}`, color: '#2E86AB', icon: '💰' },
    { label: 'Attrition Rate', value: `${kpis.attrition_rate}%`, color: '#e74c3c', icon: '📉' },
    { label: 'Avg Performance', value: `${kpis.avg_performance} / 5`, color: '#27ae60', icon: '⭐' },
    { label: 'Top Department', value: kpis.top_department, color: '#8e44ad', icon: '🏢' },
    { label: 'Top Nationality', value: kpis.top_nationality, color: '#e67e22', icon: '🌍' },
  ];

  return (
    <div style={styles.grid}>
      {cards.map((card, i) => (
        <div key={i} style={{ ...styles.card, borderTop: `4px solid ${card.color}` }}>
          <div style={styles.icon}>{card.icon}</div>
          <div style={styles.value}>{card.value}</div>
          <div style={styles.label}>{card.label}</div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '16px',
    marginBottom: '24px',
  },
  card: {
    background: '#fff',
    borderRadius: '10px',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.07)',
  },
  icon: {
    fontSize: '24px',
    marginBottom: '8px',
  },
  value: {
    fontSize: '22px',
    fontWeight: '700',
    color: '#1F4E79',
    marginBottom: '4px',
  },
  label: {
    fontSize: '12px',
    color: '#888',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
};

export default KPICards;