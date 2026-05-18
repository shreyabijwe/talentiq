# TalentIQ — HR & Workforce Analytics Platform

A full-stack HR analytics system built for companies to track employee performance, predict attrition, analyze salaries, and generate automated Excel + PDF reports.

![Dashboard](https://via.placeholder.com/800x400?text=TalentIQ+Dashboard)

## 🔗 Live Demo
- **Frontend:** https://talentiq-jo0o98xm8-shreyabijwe52-2042s-projects.vercel.app
- **API:** https://talentiq-rs7t.onrender.com/docs
- **Login:** admin / talentiq2024

## 🚀 Features
- 5,000 realistic employee records generated with UAE workforce demographics
- Random Forest ML model predicting employee attrition (67% accuracy)
- Salary benchmarking — flags underpaid and overpaid employees vs market benchmarks
- Auto-generated Excel workbook with 6 sheets — pivot tables, charts, dashboards
- Auto-generated PDF report with executive summary and embedded charts
- React dashboard with KPI cards, attrition charts, salary analysis, nationality breakdown
- REST API with JWT authentication
- One-click report generation from the dashboard

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Generation | Python, Faker, pandas |
| Database | PostgreSQL |
| Machine Learning | scikit-learn, Random Forest |
| Backend API | FastAPI, JWT Auth |
| Excel Reports | openpyxl |
| PDF Reports | reportlab |
| Frontend | React, Recharts, Tailwind |
| Deployment | Render (API), Vercel (Frontend) |

## 📊 Project Modules

### 1. Employee Database & ETL Pipeline
- Generates 5,000 realistic employee records
- Stores in PostgreSQL
- Exports to CSV for analysis

### 2. Excel Analytics Workbook
- 6-sheet auto-generated Excel file
- Pivot tables, salary analysis, attrition breakdown
- Embedded charts and executive dashboard

### 3. Attrition Prediction ML Model
- Random Forest classifier
- Feature importance: salary, performance, manager rating, age
- Confusion matrix and classification report

### 4. Salary Benchmarking & Analysis
- Statistical analysis across departments
- Linear regression — experience vs salary
- Underpaid/overpaid employee flagging
- Correlation heatmap

### 5. FastAPI Backend
- 7 REST endpoints
- JWT authentication
- Attrition prediction endpoint

### 6. React HR Dashboard
- KPI cards, bar charts, pie charts
- Searchable employee table with filters
- Functional sidebar navigation

### 7. Automated Report Generator
- One-click Excel + PDF report
- Auto-written executive summary
- Embedded charts in PDF

## 🏃 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend
```bash
pip install -r requirements.txt
python backend/data_generation/generate_employees.py
uvicorn backend.api.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure
talentiq/
├── backend/
│   ├── api/          # FastAPI endpoints
│   ├── data_generation/  # ETL pipeline
│   ├── etl/          # Salary analysis
│   ├── ml_models/    # Attrition model
│   └── reports/      # Excel & PDF generators
├── frontend/
│   └── src/
│       └── components/  # React components
├── exports/
│   ├── excel/        # Generated Excel reports
│   └── pdf/          # Generated PDF reports
└── sql/              # SQL queries
## 👩‍💻 Author
## 👩‍💻 Author
**Shreya Bijwe**
- GitHub: [@shreyabijwe](https://github.com/shreyabijwe)
- LinkedIn: [Shreya Bijwe](https://linkedin.com/in/shreya-bijwe-4a126b299)

## 📄 License
MIT License