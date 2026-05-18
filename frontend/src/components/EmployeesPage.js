import React from 'react';
import EmployeeTable from './EmployeeTable';

function EmployeesPage({ token }) {
  return (
    <div>
      <h2 style={styles.title}>Employee Directory</h2>
      <EmployeeTable token={token} />
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
};

export default EmployeesPage;