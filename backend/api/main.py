from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import joblib
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TalentIQ — HR Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── JWT Config ─────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("JWT_SECRET", "talentiq_secret_key_shreya_2024")
ALGORITHM  = "HS256"
security   = HTTPBearer()

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── Load Data ──────────────────────────────────────────────────────────────────
def get_df():
    return pd.read_csv('exports/employees.csv')

def get_model():
    return joblib.load('backend/ml_models/attrition_model.pkl')

# ── Auth Models ────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

class PredictRequest(BaseModel):
    nationality: str
    department: str
    job_title: str
    salary: float
    age: int
    years_of_experience: int
    performance_score: float
    manager_rating: float

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "TalentIQ HR Analytics API", "status": "running"}

# Login
@app.post("/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "talentiq2024":
        token = create_token(req.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# KPIs
@app.get("/kpis")
def get_kpis(user=Depends(verify_token)):
    df = get_df()
    return {
        "total_employees": len(df),
        "avg_salary": round(df['salary'].mean(), 2),
        "attrition_rate": round(df['attrition'].mean() * 100, 2),
        "avg_performance": round(df['performance_score'].mean(), 2),
        "top_department": df['department'].value_counts().idxmax(),
        "top_nationality": df['nationality'].value_counts().idxmax()
    }

# Employees with filters
@app.get("/employees")
def get_employees(
    department: Optional[str] = None,
    nationality: Optional[str] = None,
    attrition: Optional[int] = None,
    page: int = 1,
    limit: int = 50,
    user=Depends(verify_token)
):
    df = get_df()
    if department:
        df = df[df['department'] == department]
    if nationality:
        df = df[df['nationality'] == nationality]
    if attrition is not None:
        df = df[df['attrition'] == attrition]
    start = (page - 1) * limit
    end   = start + limit
    return {
        "total": len(df),
        "page": page,
        "data": df.iloc[start:end].to_dict(orient='records')
    }

# Attrition by department
@app.get("/attrition-by-dept")
def attrition_by_dept(user=Depends(verify_token)):
    df = get_df()
    result = df.groupby('department').agg(
        total=('employee_id', 'count'),
        attrition=('attrition', 'sum')
    ).reset_index()
    result['attrition_rate'] = (result['attrition'] / result['total'] * 100).round(2)
    return result.to_dict(orient='records')

# Salary distribution
@app.get("/salary-distribution")
def salary_distribution(user=Depends(verify_token)):
    df = get_df()
    result = df.groupby('department')['salary'].agg(['min', 'max', 'mean']).reset_index()
    result.columns = ['department', 'min', 'max', 'avg']
    result = result.round(2)
    return result.to_dict(orient='records')

# Nationality breakdown
@app.get("/nationality-breakdown")
def nationality_breakdown(user=Depends(verify_token)):
    df = get_df()
    result = df['nationality'].value_counts().reset_index()
    result.columns = ['nationality', 'count']
    return result.to_dict(orient='records')

# Predict attrition
@app.post("/predict-attrition")
def predict_attrition(req: PredictRequest, user=Depends(verify_token)):
    from sklearn.preprocessing import LabelEncoder
    df = get_df()
    model = get_model()

    le = LabelEncoder()
    nat = le.fit_transform(df['nationality'].tolist() + [req.nationality])[-1]
    dep = le.fit_transform(df['department'].tolist() + [req.department])[-1]
    job = le.fit_transform(df['job_title'].tolist() + [req.job_title])[-1]

    features = [[nat, dep, job, req.salary, req.age,
                 req.years_of_experience, req.performance_score, req.manager_rating]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "attrition_risk": int(prediction),
        "probability": round(float(probability) * 100, 2),
        "risk_level": "High" if probability > 0.6 else "Medium" if probability > 0.3 else "Low"
    }

# Generate report
@app.get("/generate-report")
def generate_report(user=Depends(verify_token)):
    from backend.reports.excel_report import generate_excel_report
    generate_excel_report()
    return {"message": "Report generated", "path": "exports/excel/TalentIQ_HR_Report.xlsx"}