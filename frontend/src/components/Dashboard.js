import React, { useState, useEffect } from 'react';
import KPICards from './KPICards';
import AttritionChart from './AttritionChart';
import SalaryChart from './SalaryChart';
import NationalityChart from './NationalityChart';
import EmployeeTable from './EmployeeTable';

function Dashboard({ token, onLogout }) {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  useEffect(() => {
    fetch('https://talentiq-rs7t.onrender.com/kpis', { headers })
      .then(res => res.json())
      .then(data => { setKpis(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <div style={styles.sidebar}>
        <div style={styles.logo}>
          <h2 style={styles.logoText}>TalentIQ</h2>
          <p style={styles.logoSub}>UAE HR Analytics</p>
        </div>
        <nav style={styles.nav}>
          {['Dashboard', 'Employees', 'Attrition', 'Salary', 'Reports'].map(item => (
            <div key={item} style={styles.navItem}>{item}</div>
          ))}
        </nav>
        <button onClick={onLogout} style={styles.logout}>Logout</button>
      </div>

      {/* Main Content */}
      <div style={styles.main}>
        <div style={styles.topbar}>
          <h1 style={styles.pageTitle}>HR Analytics Dashboard</h1>
          <p style={styles.date}>{new Date().toDateString()}</p>
        </div>

        {loading ? (
          <p style={{ padding: '40px' }}>Loading dashboard...</p>
        ) : (
          <>
            <KPICards kpis={kpis} />
            <div style={styles.row}>
              <AttritionChart token={token} />
              <NationalityChart token={token} />
            </div>
            <SalaryChart token={token} />
            <EmployeeTable token={token} />
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    minHeight: '100vh',
  },
  sidebar: {
    width: '220px',
    background: '#1F4E79',
    color: '#fff',
    display: 'flex',
    flexDirection: 'column',
    padding: '24px 0',
    position: 'fixed',
    height: '100vh',
  },
  logo: {
    padding: '0 24px 24px',
    borderBottom: '1px solid rgba(255,255,255,0.1)',
  },
  logoText: {
    fontSize: '22px',
    fontWeight: '700',
  },
  logoSub: {
    fontSize: '11px',
    opacity: 0.7,
    marginTop: '4px',
  },
  nav: {
    flex: 1,
    padding: '16px 0',
  },
  navItem: {
    padding: '12px 24px',
    cursor: 'pointer',
    fontSize: '14px',
    opacity: 0.85,
    transition: 'background 0.2s',
  },
  logout: {
    margin: '16px',
    padding: '10px',
    background: 'rgba(255,255,255,0.1)',
    color: '#fff',
    border: '1px solid rgba(255,255,255,0.2)',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '13px',
  },
  main: {
    marginLeft: '220px',
    flex: 1,
    padding: '24px',
  },
  topbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '24px',
  },
  pageTitle: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#1F4E79',
  },
  date: {
    color: '#888',
    fontSize: '13px',
  },
  row: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '24px',
    marginBottom: '24px',
  },
};

export default Dashboard;