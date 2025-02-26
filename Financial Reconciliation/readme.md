# 📊 AI-Powered Financial Reconciliation System

## Project Overview
This AI-powered financial reconciliation system automates the matching of bank transactions, internal records, and vendor invoices while converting foreign currencies to INR. It leverages Google AI (Gemini API) and Forex Exchange Data to identify discrepancies, detect potential fraud, and classify transactions with structured insights.  

---

## Features & Enhancements

- **AI-Powered Analysis** – Uses Google Gemini API to detect mismatches, fraud, and missing transactions.
- **Automated Currency Conversion** – Converts all transactions to INR using Forex Exchange Rates.
- **Seamless Data Merging** – Combines bank records, internal transactions, and vendor invoices for analysis.
- **Fraud Detection & Classification** – AI classifies transactions into Salaries, Vendor Payments, Refunds, or Fraud.
- **Structured Financial Insights** – Generates an AI-powered reconciliation report in Notepad-friendly format.  

## How It Works

- **Loads transaction data** from CSV files (`bank_transactions.csv`, `internal_transactions.csv`, `vendor_invoices.csv`).  
- **Converts foreign currency transactions** into INR using Forex rates (`currency_rates.csv`).  
- **Merges and reconciles records** from multiple sources(Bank, Internal, Vendor).  
- **AI analyzes discrepancies** and generates a detailed reconciliation report.  
- **Detects fraudulent activity** like duplicate refunds or mismatched amounts.  

## Technologies Used

- **Programming Language:** Python  
- **AI & NLP:** Google Gemini API (for AI-powered reconciliation insights)  
- **Data Processing:** Pandas (for handling transaction data)  
- **Forex Conversion:** Forex-Python (for real-time currency conversion)  
- **File Handling:** CSV files for financial data storage  

---

## 📂 Folder Structure

```plaintext
/financial-reconciliation
├── src/                          # Source code
│   ├── financial_reconciliation.py         # Main script for reconciliation
│   ├── forex_converter.py        # Handles currency conversion
│   ├── ai_analysis.py            # AI-powered transaction analysis
│   ├── requirements.txt          # Required Python dependencies
│
├── data/                          # Stores financial records
│   ├── bank_transactions.csv      # Bank transaction data
│   ├── internal_transactions.csv  # Internal transaction records
│   ├── vendor_invoices.csv        # Vendor payment invoices
│   ├── currency_rates.csv         # Forex conversion rates
│
├── reports/                       # Stores AI-generated reconciliation reports
│   ├── reconciliation_report.txt  # AI-generated insights
│
├── README.md                      # Documentation file
```

---

## Setup & Execution

### 1) Install Dependencies
Ensure **Python 3.8+** is installed, then install dependencies:
```bash
pip install -r requirements.txt
```

### 2) Configure API Key
Replace `YOUR_API_KEY` in `financial_reconciliation.py` with your **Google Gemini API Key**.

### 4) Run the Reconciliation Script
```bash
python financial_reconciliation.py
```
**AI will analyze transactions, detect mismatches, and generate a reconciliation report (`reconciliation_report.txt`).**  

---

## Code Breakdown
### 1) `reconciliation.py` – Core Reconciliation Script**
-  **Loads transaction records** from CSV files.
-  **Converts foreign currency transactions** into INR using Forex rates.
-  **Merges data from multiple sources** (Bank, Internal, Vendor).  -
-  **Uses AI to analyze discrepancies** and classify transactions.  
- **Saves AI-generated insights** into `reconciliation_report.txt`.
