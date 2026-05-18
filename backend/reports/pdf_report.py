from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, Image, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from datetime import datetime

# ── Colors ─────────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor('#1F4E79')
BLUE    = colors.HexColor('#2E86AB')
LIGHT   = colors.HexColor('#D6E4F0')
RED     = colors.HexColor('#e74c3c')
GREEN   = colors.HexColor('#27ae60')
WHITE   = colors.white
GRAY    = colors.HexColor('#888888')

os.makedirs('exports/pdf', exist_ok=True)
os.makedirs('exports/charts', exist_ok=True)

# ── Generate Charts for PDF ────────────────────────────────────────────────────
def generate_charts(df):
    # Attrition by dept
    att = df.groupby('department')['attrition'].mean() * 100
    plt.figure(figsize=(8, 4))
    att.sort_values().plot(kind='barh', color='#1F4E79')
    plt.title('Attrition Rate by Department (%)')
    plt.xlabel('Attrition Rate (%)')
    plt.tight_layout()
    plt.savefig('exports/charts/pdf_attrition.png', dpi=150)
    plt.close()

    # Salary by dept
    sal = df.groupby('department')['salary'].mean()
    plt.figure(figsize=(8, 4))
    sal.sort_values().plot(kind='barh', color='#2E86AB')
    plt.title('Average Salary by Department (AED)')
    plt.xlabel('Avg Salary (AED)')
    plt.tight_layout()
    plt.savefig('exports/charts/pdf_salary.png', dpi=150)
    plt.close()

    print("Charts generated for PDF.")

# ── Executive Summary ──────────────────────────────────────────────────────────
def generate_summary(df):
    total       = len(df)
    avg_salary  = round(df['salary'].mean(), 0)
    attrition   = round(df['attrition'].mean() * 100, 1)
    avg_perf    = round(df['performance_score'].mean(), 2)
    top_dept    = df['department'].value_counts().idxmax()
    top_nat     = df['nationality'].value_counts().idxmax()
    high_risk   = len(df[df['attrition'] == 1])

    summary = (
        f"TalentIQ HR Analytics report for the period ending {datetime.now().strftime('%B %Y')}. "
        f"The organization currently employs {total:,} staff members across 10 departments, "
        f"with an average monthly salary of AED {avg_salary:,.0f}. "
        f"The overall attrition rate stands at {attrition}%, with {high_risk:,} employees "
        f"having departed during the review period. "
        f"\n\n"
        f"The {top_dept} department represents the largest workforce segment, while {top_nat} "
        f"nationals form the most represented nationality group. "
        f"Average employee performance is rated at {avg_perf} out of 5.0, indicating a "
        f"{'strong' if avg_perf >= 3.5 else 'moderate'} overall performance culture. "
        f"\n\n"
        f"Key recommendations: Focus retention efforts on high-attrition departments, "
        f"review salary benchmarks for underpaid employee segments, and implement "
        f"structured performance improvement programs to elevate average scores above 4.0."
    )
    return summary

# ── Build PDF ──────────────────────────────────────────────────────────────────
def generate_pdf_report():
    df = pd.read_csv('exports/employees.csv')
    generate_charts(df)

    path = 'exports/pdf/TalentIQ_HR_Report.pdf'
    doc  = SimpleDocTemplate(path, pagesize=A4,
                             rightMargin=40, leftMargin=40,
                             topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    story  = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    title_style = ParagraphStyle('title', fontSize=28, textColor=NAVY,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold',
                                  spaceAfter=8)
    sub_style   = ParagraphStyle('sub', fontSize=13, textColor=BLUE,
                                  alignment=TA_CENTER, spaceAfter=4)
    date_style  = ParagraphStyle('date', fontSize=10, textColor=GRAY,
                                  alignment=TA_CENTER)

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("TalentIQ ", title_style))
    story.append(Paragraph("HR & Workforce Analytics Report", sub_style))
    story.append(Paragraph(datetime.now().strftime("%B %Y"), date_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY))
    story.append(Spacer(1, 0.3 * inch))

    # ── KPI Table ──────────────────────────────────────────────────────────────
    section_style = ParagraphStyle('section', fontSize=14, textColor=NAVY,
                                    fontName='Helvetica-Bold', spaceAfter=10,
                                    spaceBefore=16)
    story.append(Paragraph("Key Performance Indicators", section_style))

    total      = len(df)
    avg_salary = round(df['salary'].mean(), 0)
    attrition  = round(df['attrition'].mean() * 100, 1)
    avg_perf   = round(df['performance_score'].mean(), 2)
    top_dept   = df['department'].value_counts().idxmax()
    top_nat    = df['nationality'].value_counts().idxmax()

    kpi_data = [
        ['Metric', 'Value'],
        ['Total Employees', f'{total:,}'],
        ['Average Salary', f'AED {avg_salary:,.0f}'],
        ['Attrition Rate', f'{attrition}%'],
        ['Avg Performance Score', f'{avg_perf} / 5.0'],
        ['Largest Department', top_dept],
        ['Top Nationality', top_nat],
    ]

    kpi_table = Table(kpi_data, colWidths=[3 * inch, 3 * inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 11),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE',   (0, 1), (-1, -1), 10),
        ('PADDING',    (0, 0), (-1, -1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Executive Summary ──────────────────────────────────────────────────────
    story.append(Paragraph("Executive Summary", section_style))
    body_style = ParagraphStyle('body', fontSize=10, leading=16,
                                 textColor=colors.black, spaceAfter=8)
    for para in generate_summary(df).split('\n\n'):
        story.append(Paragraph(para.strip(), body_style))
    story.append(Spacer(1, 0.2 * inch))

    # ── Charts ─────────────────────────────────────────────────────────────────
    story.append(Paragraph("Attrition Analysis", section_style))
    story.append(Image('exports/charts/pdf_attrition.png', width=5.5*inch, height=2.8*inch))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Salary Analysis", section_style))
    story.append(Image('exports/charts/pdf_salary.png', width=5.5*inch, height=2.8*inch))
    story.append(Spacer(1, 0.2 * inch))

    # ── Attrition Table ────────────────────────────────────────────────────────
    story.append(Paragraph("Attrition by Department", section_style))
    att_df = df.groupby('department').agg(
        Total=('employee_id', 'count'),
        Left=('attrition', 'sum')
    ).reset_index()
    att_df['Rate %'] = (att_df['Left'] / att_df['Total'] * 100).round(1)

    att_data = [['Department', 'Total', 'Left', 'Rate %']]
    for _, row in att_df.iterrows():
        att_data.append([row['department'], str(row['Total']),
                         str(row['Left']), f"{row['Rate %']}%"])

    att_table = Table(att_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    att_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, WHITE]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE',   (0, 0), (-1, -1), 9),
        ('PADDING',    (0, 0), (-1, -1), 7),
    ]))
    story.append(att_table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Footer ─────────────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=NAVY))
    footer_style = ParagraphStyle('footer', fontSize=8, textColor=GRAY,
                                   alignment=TA_CENTER, spaceBefore=6)
    story.append(Paragraph(
        f"Generated by TalentIQ UAE HR Analytics Platform — {datetime.now().strftime('%d %B %Y')}",
        footer_style
    ))

    doc.build(story)
    print(f"PDF report saved to {path}")
    return path

if __name__ == "__main__":
    generate_pdf_report()