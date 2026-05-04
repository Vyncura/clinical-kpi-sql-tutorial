# clinical-kpi-sql-tutorial

An advanced SQL tutorial for Healthcare Revenue Cycle Management (RCM), featuring clinical KPIs, complex query logic for junior analysts, and a specialized SQL cheat sheet.

# Clinical KPI: Healthcare RCM SQL Tutorial

## Project Goal
To demonstrate expert-level SQL techniques for analyzing medical costs and patient data, serving as a resource for junior analysts in emerging markets.

## Dataset
This project uses a medical cost dataset containing patient demographics, BMI, smoking status, and regional charges.

## Key SQL Business Insights
1. **Segmented Revenue Analysis:** Average charges by region and smoker status.
2. **Outlier Detection:** Identifying high-cost claims using SQL Window Functions.
3. **Demographic Distribution:** Revenue impact based on BMI categories.
4. **Contribution Analysis:** Percentage of regional revenue driven by specific cohorts.
5. **Cohort Analysis:** Age-based 'ticket size' trends.

## Portfolio Feature: SQL Cheat Sheet for RCM
Included in the repository is a cheat sheet covering:
- Gross Revenue Aggregations
- Denial & Adjustment Ratios
- Patient Segmentation Case Logic
- Payer Performance Metrics

## Project Documentation (README) Template

## 🏥 Project Name: Automated Healthcare Revenue Integrity Pipeline

Bridging Healthcare and Data Analytics | An open-source pipeline designed to process, clean, and analyze clinical billing files to improve health literacy and prevent revenue leakage.

## 📌 Project Overview
Healthcare organizations often generate vast amounts of billing data (EDI 837/835 files) that remain unanalyzed due to operational bottlenecks. This project demonstrates an automated ETL (Extract, Transform, Load) pipeline built with Python and SQL to parse raw EDI data, identify recoverable revenue leaks, and visualize performance metrics.

## Key Features
Automated Data Ingestion: Python script to securely parse X12/EDI healthcare files.

Data Cleansing & Modeling: Normalization of Claim Adjustment Reason Codes (CARCs).

Database Pipeline: SQLite/BigQuery schema optimization for quick analysis.

Interactive Dashboard: Looker Studio/Plotly reporting views for Practice Managers.

## 🛠️ Tech Stack & Requirements
Language: Python 3.10+

Libraries: pandas, edi-835-parser, sqlalchemy, plotly

Data Warehouse: BigQuery or SQLite

BI / Visualization: Looker Studio or Power BI

## ⚙️ Pipeline Architecture
The data flows through the following stages:

Extract: Secure extraction of 835 and 837 files from local storage/SFTP.

Transform: Parsing segments, mapping CARC codes to human-readable terms, and identifying leakage.

Load: Pushing cleaned data to the SQL database.

## 🚀 Getting Started
Prerequisites
Make sure you have installed the required libraries:

Bash
pip install pandas edi-835-parser sqlalchemy plotly
Quickstart Example
To run the primary revenue audit script:

Python
from edi_835_parser import parse
import pandas as pd

# Load the dummy dataset for demonstration
path = './data/sample_835.txt'
transaction_sets = parse(path)

# Convert to DataFrame
df = transaction_sets.to_dataframe()

# Filter for fixable denial codes (e.g., Missing Info - CARC 16)
denied_claims = df[df['adjustment_reason_code'] == '16']
print(f"Recoverable opportunities identified: {len(denied_claims)}")
## 📊 Analytics & Insights
Included in the /reports directory is the SQL query used to rank insurance payers by Net Collection Rate (NCR):

SQL

SELECT 

    payer_name,
    
    COUNT(claim_id) AS total_claims,
    
    SUM(billed_amount) AS total_billed,
    
    SUM(paid_amount) AS total_paid,
    
    SUM(CASE 
    
        WHEN adj_code IN ('16', '22', '27') THEN adj_amount 
        
        ELSE 0 
        
    END) AS recoverable_leakage
    
FROM healthcare_claims

GROUP BY payer_name

ORDER BY recoverable_leakage DESC;

## 🌍 Open Source & Impact
This pipeline is maintained as open-source to make data-driven decisions accessible to healthcare providers and data analysts in emerging markets.

## Supporting This Project
Your support covers the hosting costs for live dashboards, API subscriptions, and cloud computing investments required to build predictive models.

👉 Support this project and keep these tools free (Replace with your link)

## 📜 License
This project is licensed under the MIT License.

## 📬 Contact / Feedback
For questions, collaboration requests, or suggestions to improve health literacy reporting, please reach out via LinkedIn or file an issue on GitHub.
