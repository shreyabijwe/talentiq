import React, { useState, useEffect } from 'react';
import KPICards from './KPICards';
import AttritionChart from './AttritionChart';
import SalaryChart from './SalaryChart';
import NationalityChart from './NationalityChart';
import EmployeeTable from './EmployeeTable';
import EmployeesPage from './EmployeesPage';
import AttritionPage from './AttritionPage';
import SalaryPage from './SalaryPage';
import ReportsPage from './ReportsPage';

function Dashboard({ token, onLogout }) {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activePage, setActivePage] = useState('Dashboard');

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  // eslint-disable-next-line
  useEffect(() => {
    fetch('https://talentiq-rs7t.onrender.com/kpis', { headers })
      .then(res => res.json())
      .then(data => { setKpis(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const renderPage = () => {
    switch (activePage) {
      case 'Employees': return <EmployeesPage token={token} />;
      case 'Attrition': return <AttritionPage token={token} />;
      case 'Salary': return <SalaryPage token={token} />;
      case 'Reports': return <ReportsPage token={token} />;
      default: return (
        <>
          <KPICards kpis={kpis} />
          <div style={styles.row}>
            <AttritionChart token={token} />
            <NationalityChart token={token} />
          </div>
          <SalaryChart token={token} />
          <EmployeeTable token={token} />
        </>
      );
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <div style={styles.logo}>
          <h2 style={styles.logoText}>TalentIQ</h2>
          <p style={styles.logoSub}>HR Analytics</p>
        </div>
        <nav style={styles.nav}>
          {['Dashboard', 'Employees', 'Attrition', 'Salary', 'Reports'].map(item => (
            <div
              key={item}
              onClick={() => setActivePage(item)}
              style={{
                ...styles.navItem,
                background: activePage === item ? 'rgba(255,255,255,0.15)' : 'transparent',
                fontWeight: activePage === item ? '700' : 'normal',
              }}
            >
              {item}
            </div>
          ))}
        </nav>
        <button onClick={onLogout} style={styles.logout}>Logout</button>
      </div>

      <div style={styles.main}>
        <div style={styles.topbar}>
          <h1 style={styles.pageTitle}>{activePage === 'Dashboard' ? 'HR Analytics Dashboard' : activePage}</h1>
          <p style={styles.date}>{new Date().toDateString()}</p>
        </div>

        {loading ? (
          <p style={{ padding: '40px' }}>Loading dashboard...</p>
        ) : (
          renderPage()
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
    borderRadius: '6px',
    margin: '2px 8px',
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