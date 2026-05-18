import React from 'react';
import AttritionChart from './AttritionChart';

function AttritionPage({ token }) {
  return (
    <div>
      <h2 style={styles.title}>Attrition Analysis</h2>
      <AttritionChart token={token} />
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

export default AttritionPage;