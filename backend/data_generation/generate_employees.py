import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

fake = Faker()
random.seed(42)

load_dotenv()

NATIONALITIES = [
    'Emirati', 'Indian', 'Pakistani', 'Filipino', 'Egyptian',
    'Bangladeshi', 'British', 'American', 'Jordanian', 'Lebanese'
]

DEPARTMENTS = [
    'Finance', 'HR', 'IT', 'Operations', 'Sales',
    'Marketing', 'Legal', 'Customer Service', 'Logistics', 'Management'
]

JOB_TITLES = {
    'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'CFO'],
    'HR': ['HR Officer', 'HR Manager', 'Recruiter', 'HR Director'],
    'IT': ['Software Engineer', 'IT Support', 'Data Analyst', 'IT Manager'],
    'Operations': ['Operations Analyst', 'Operations Manager', 'Coordinator'],
    'Sales': ['Sales Executive', 'Sales Manager', 'Account Manager'],
    'Marketing': ['Marketing Executive', 'Brand Manager', 'Digital Marketer'],
    'Legal': ['Legal Officer', 'Compliance Manager', 'Legal Counsel'],
    'Customer Service': ['CS Representative', 'CS Supervisor', 'CS Manager'],
    'Logistics': ['Logistics Coordinator', 'Supply Chain Analyst', 'Warehouse Manager'],
    'Management': ['Team Lead', 'General Manager', 'Director', 'VP']
}

SALARY_RANGES = {
    'Finance': (8000, 45000),
    'HR': (7000, 35000),
    'IT': (9000, 50000),
    'Operations': (6000, 30000),
    'Sales': (7000, 40000),
    'Marketing': (7000, 35000),
    'Legal': (10000, 55000),
    'Customer Service': (5000, 20000),
    'Logistics': (6000, 28000),
    'Management': (15000, 80000)
}


def generate_employee(emp_id):
    department = random.choice(DEPARTMENTS)
    salary_min, salary_max = SALARY_RANGES[department]
    years_exp = random.randint(1, 25)
    salary = round(random.uniform(salary_min, salary_max), 2)
    age = random.randint(22, 60)
    performance_score = round(random.uniform(1.0, 5.0), 2)
    manager_rating = round(random.uniform(1.0, 5.0), 2)

    # Attrition logic — low salary + low performance = higher chance
    attrition_chance = 0.15
    if salary < salary_min + (salary_max - salary_min) * 0.3:
        attrition_chance += 0.2
    if performance_score < 2.5:
        attrition_chance += 0.15
    if manager_rating < 2.5:
        attrition_chance += 0.1
    attrition = 1 if random.random() < attrition_chance else 0

    join_date = datetime.now() - timedelta(days=years_exp * 365 + random.randint(0, 365))

    return {
        'employee_id': emp_id,
        'name': fake.name(),
        'nationality': random.choice(NATIONALITIES),
        'department': department,
        'job_title': random.choice(JOB_TITLES[department]),
        'salary': salary,
        'age': age,
        'years_of_experience': years_exp,
        'performance_score': performance_score,
        'manager_rating': manager_rating,
        'attrition': attrition,
        'join_date': join_date.strftime('%Y-%m-%d')
    }


def generate_all_employees(n=5000):
    print(f"Generating {n} employee records...")
    employees = [generate_employee(i + 1) for i in range(n)]
    df = pd.DataFrame(employees)
    print(f"Generated {len(df)} records successfully.")
    return df


def save_to_csv(df):
    os.makedirs('exports', exist_ok=True)
    path = 'exports/employees.csv'
    df.to_csv(path, index=False)
    print(f"Saved to {path}")


def save_to_postgres(df):
    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                nationality VARCHAR(50),
                department VARCHAR(50),
                job_title VARCHAR(100),
                salary NUMERIC(10,2),
                age INTEGER,
                years_of_experience INTEGER,
                performance_score NUMERIC(3,2),
                manager_rating NUMERIC(3,2),
                attrition INTEGER,
                join_date DATE
            )
        """))
        conn.commit()
        print("Table created successfully.")

    df.to_sql('employees', engine, if_exists='replace', index=False)
    print("Data loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    df = generate_all_employees(5000)
    save_to_csv(df)
    save_to_postgres(df)
    print("ETL complete.")