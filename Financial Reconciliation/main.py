import google.generativeai as genai
import pandas as pd
from forex_python.converter import CurrencyRates

# Load CSV files
bank_records = pd.read_csv("bank_transactions.csv")
internal_records = pd.read_csv("internal_transactions.csv")
vendor_invoices = pd.read_csv("vendor_invoices.csv")
currency_rates = pd.read_csv("currency_rates.csv")

# Convert date columns to datetime format
for df in [bank_records, internal_records, vendor_invoices]:
    df["Date"] = pd.to_datetime(df["Date"])

# Convert all amounts to INR using forex rates
def convert_to_inr(amount, currency):
    rate = currency_rates.loc[currency_rates["Currency"] == currency, "Rate (to INR)"].values
    return amount * rate[0] if len(rate) > 0 else amount  # Default to same amount if rate not found

for df in [bank_records, internal_records, vendor_invoices]:
    df["Amount (INR)"] = df.apply(lambda x: convert_to_inr(x["Amount"], x["Currency"]), axis=1)

# Merge datasets for reconciliation
merged_records = pd.merge(bank_records, internal_records, on=["Date", "Amount (INR)", "Description"], how="outer", indicator=True)

# AI setup for Google AI Studio
API_KEY = "YOUR_API_KEY"  # Replace with actual API key
genai.configure(api_key=API_KEY)

# Convert data to text for AI processing
data_text = merged_records.to_string()

# AI Prompt for Gemini
prompt = f"""
You are a financial reconciliation expert. Analyze the following transactions in INR and:
- Identify missing or extra transactions
- Detect mismatched amounts across records
- Spot potential fraud (e.g., duplicate refunds)
- Classify transactions (Salaries, Vendor Payments, Refunds, Fraud)

Data:
{data_text}

Provide structured insights with explanations in a Notepad-friendly format:
- Use '==== Section Title ====' instead of bold
- Use clear separators and indentation for readability.
"""

# Generate AI response
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(prompt)

# Format the response
formatted_response = response.text.replace("**", "").replace("__", "")  # Remove any markdown formatting

# Save AI insights
with open("reconciliation_report.txt", "w") as f:
    f.write(formatted_response)

print("✅ Reconciliation complete! Check 'reconciliation_report.txt' for insights.")
