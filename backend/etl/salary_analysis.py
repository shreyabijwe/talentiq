import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# ── UAE Market Benchmarks (AED/month) ─────────────────────────────────────────
BENCHMARKS = {
    'Finance': 25000,
    'HR': 18000,
    'IT': 28000,
    'Operations': 16000,
    'Sales': 20000,
    'Marketing': 18000,
    'Legal': 30000,
    'Customer Service': 12000,
    'Logistics': 15000,
    'Management': 45000
}

os.makedirs('exports/charts', exist_ok=True)
os.makedirs('exports/excel', exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv('exports/employees.csv')
    return df

# ── 1. Salary Distribution ─────────────────────────────────────────────────────
def plot_salary_distribution(df):
    plt.figure(figsize=(10, 5))
    sns.histplot(df['salary'], bins=50, kde=True, color='steelblue')
    plt.title('Overall Salary Distribution — UAE Employees')
    plt.xlabel('Salary (AED)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('exports/charts/salary_distribution.png', dpi=150)
    plt.close()
    print("Salary distribution chart saved.")

# ── 2. Box Plot by Department ──────────────────────────────────────────────────
def plot_boxplot_by_dept(df):
    plt.figure(figsize=(14, 6))
    order = df.groupby('department')['salary'].median().sort_values().index
    sns.boxplot(data=df, x='department', y='salary', order=order, palette='Blues')
    plt.title('Salary Distribution by Department')
    plt.xlabel('Department')
    plt.ylabel('Salary (AED)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('exports/charts/salary_boxplot.png', dpi=150)
    plt.close()
    print("Box plot saved.")

# ── 3. Salary Heatmap ─────────────────────────────────────────────────────────
def plot_salary_heatmap(df):
    df['exp_band'] = pd.cut(df['years_of_experience'],
                            bins=[0, 3, 7, 12, 25],
                            labels=['0-3 yrs', '4-7 yrs', '8-12 yrs', '13+ yrs'])
    heatmap_data = df.groupby(['department', 'exp_band'])['salary'].mean().unstack()
    plt.figure(figsize=(12, 7))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5)
    plt.title('Avg Salary Heatmap — Department vs Experience Band')
    plt.tight_layout()
    plt.savefig('exports/charts/salary_heatmap.png', dpi=150)
    plt.close()
    print("Salary heatmap saved.")

# ── 4. Correlation Analysis ───────────────────────────────────────────────────
def correlation_analysis(df):
    cols = ['salary', 'age', 'years_of_experience', 'performance_score', 'manager_rating']
    corr = df[cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('exports/charts/correlation_matrix.png', dpi=150)
    plt.close()

    r, p = stats.pearsonr(df['years_of_experience'], df['salary'])
    print(f"\nPearson Correlation (Experience vs Salary): r={r:.4f}, p={p:.4f}")
    print("Correlation matrix saved.")

# ── 5. Linear Regression ──────────────────────────────────────────────────────
def linear_regression(df):
    slope, intercept, r, p, se = stats.linregress(df['years_of_experience'], df['salary'])
    print(f"\nLinear Regression — Experience → Salary")
    print(f"  Slope     : {slope:.2f} AED per year of experience")
    print(f"  Intercept : {intercept:.2f}")
    print(f"  R²        : {r**2:.4f}")

    plt.figure(figsize=(10, 5))
    plt.scatter(df['years_of_experience'], df['salary'], alpha=0.3, color='steelblue')
    x = np.linspace(df['years_of_experience'].min(), df['years_of_experience'].max(), 100)
    plt.plot(x, slope * x + intercept, color='red', linewidth=2, label='Regression Line')
    plt.title('Salary vs Years of Experience')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary (AED)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('exports/charts/salary_regression.png', dpi=150)
    plt.close()
    print("Regression chart saved.")

# ── 6. Underpaid / Overpaid Flagging ─────────────────────────────────────────
def flag_employees(df):
    df = df.copy()
    df['benchmark'] = df['department'].map(BENCHMARKS)
    df['underpaid'] = df['salary'] < df['benchmark'] * 0.85
    df['overpaid']  = df['salary'] > df['benchmark'] * 1.20
    df['status'] = 'Fair'
    df.loc[df['underpaid'], 'status'] = 'Underpaid'
    df.loc[df['overpaid'],  'status'] = 'Overpaid'

    print(f"\nSalary Status:")
    print(df['status'].value_counts())

    summary = df.groupby('department')['status'].value_counts().unstack(fill_value=0)
    print("\nBy Department:")
    print(summary)

    df.to_csv('exports/salary_analysis.csv', index=False)
    print("\nSalary analysis saved to exports/salary_analysis.csv")
    return df

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading data...")
    df = load_data()

    print("Generating salary distribution...")
    plot_salary_distribution(df)

    print("Generating box plots...")
    plot_boxplot_by_dept(df)

    print("Generating salary heatmap...")
    plot_salary_heatmap(df)

    print("Running correlation analysis...")
    correlation_analysis(df)

    print("Running linear regression...")
    linear_regression(df)

    print("Flagging underpaid/overpaid employees...")
    flag_employees(df)

    print("\nPhase 4 complete.")