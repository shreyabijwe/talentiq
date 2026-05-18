import React, { useState, useEffect } from 'react';

function EmployeeTable({ token }) {
  const [employees, setEmployees] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [department, setDepartment] = useState('');
  const [search, setSearch] = useState('');

  const departments = ['', 'Finance', 'HR', 'IT', 'Operations', 'Sales',
    'Marketing', 'Legal', 'Customer Service', 'Logistics', 'Management'];

  const fetchEmployees = () => {
    let url = `https://talentiq-rs7t.onrender.com/employees?page=${page}&limit=10`;
    if (department) url += `&department=${department}`;
    fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        setEmployees(data.data);
        setTotal(data.total);
      });
  };

  useEffect(() => { fetchEmployees(); }, [page, department]);

  const filtered = search
    ? employees.filter(e => e.name.toLowerCase().includes(search.toLowerCase()))
    : employees;

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Employee Directory</h3>

      <div style={styles.controls}>
        <input
          style={styles.search}
          placeholder="Search by name..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select
          style={styles.select}
          value={department}
          onChange={e => { setDepartment(e.target.value); setPage(1); }}
        >
          {departments.map(d => (
            <option key={d} value={d}>{d || 'All Departments'}</option>
          ))}
        </select>
      </div>

      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr>
              {['ID', 'Name', 'Nationality', 'Department', 'Job Title', 'Salary (AED)', 'Performance', 'Attrition'].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((emp, i) => (
              <tr key={emp.employee_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                <td style={styles.td}>{emp.employee_id}</td>
                <td style={styles.td}>{emp.name}</td>
                <td style={styles.td}>{emp.nationality}</td>
                <td style={styles.td}>{emp.department}</td>
                <td style={styles.td}>{emp.job_title}</td>
                <td style={styles.td}>{Number(emp.salary).toLocaleString()}</td>
                <td style={styles.td}>{emp.performance_score}</td>
                <td style={styles.td}>
                  <span style={{
                    ...styles.badge,
                    background: emp.attrition === 1 ? '#ffe0e0' : '#e0ffe0',
                    color: emp.attrition === 1 ? '#c0392b' : '#27ae60',
                  }}>
                    {emp.attrition === 1 ? 'Left' : 'Active'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={styles.pagination}>
        <button style={styles.pageBtn} onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>
          ← Prev
        </button>
        <span style={styles.pageInfo}>Page {page} — {total.toLocaleString()} total</span>
        <button style={styles.pageBtn} onClick={() => setPage(p => p + 1)} disabled={page * 10 >= total}>
          Next →
        </button>
      </div>
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
  controls: {
    display: 'flex',
    gap: '12px',
    marginBottom: '16px',
  },
  search: {
    flex: 1,
    padding: '8px 12px',
    borderRadius: '6px',
    border: '1px solid #ddd',
    fontSize: '13px',
  },
  select: {
    padding: '8px 12px',
    borderRadius: '6px',
    border: '1px solid #ddd',
    fontSize: '13px',
  },
  tableWrapper: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '13px',
  },
  th: {
    background: '#1F4E79',
    color: '#fff',
    padding: '10px 12px',
    textAlign: 'left',
    fontWeight: '600',
    whiteSpace: 'nowrap',
  },
  td: {
    padding: '9px 12px',
    borderBottom: '1px solid #f0f0f0',
    whiteSpace: 'nowrap',
  },
  badge: {
    padding: '3px 8px',
    borderRadius: '12px',
    fontSize: '11px',
    fontWeight: '600',
  },
  pagination: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '16px',
    marginTop: '16px',
  },
  pageBtn: {
    padding: '6px 16px',
    background: '#1F4E79',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
  },
  pageInfo: {
    fontSize: '13px',
    color: '#666',
  },
};

export default EmployeeTable;