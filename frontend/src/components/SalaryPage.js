import React from 'react';
import SalaryChart from './SalaryChart';

function SalaryPage({ token }) {
  return (
    <div>
      <h2 style={styles.title}>Salary Analysis</h2>
      <SalaryChart token={token} />
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

export default SalaryPage;