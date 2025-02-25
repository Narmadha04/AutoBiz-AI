import google.generativeai as genai
import pandas as pd
from forex_python.converter import CurrencyRates

# Load CSV files containing transaction records and currency exchange rates
bank_records = pd.read_csv("bank_transactions.csv")  # Bank-provided transaction records
internal_records = pd.read_csv("internal_transactions.csv")  # Internal accounting records
vendor_invoices = pd.read_csv("vendor_invoices.csv")  # Invoices from vendors
currency_rates = pd.read_csv("currency_rates.csv")  # Exchange rates for currency conversion

# Convert date columns to datetime format for consistency across datasets
for df in [bank_records, internal_records, vendor_invoices]:
    df["Date"] = pd.to_datetime(df["Date"])


def convert_to_inr(amount, currency):
    """
    Convert transaction amounts to INR using exchange rates from currency_rates.csv.
    - If the currency rate exists, convert the amount.
    - If not found, return the original amount (assuming it is already in INR).
    """
    rate = currency_rates.loc[currency_rates["Currency"] == currency, "Rate (to INR)"].values
    return amount * rate[0] if len(rate) > 0 else amount  # Default to same amount if rate not found


# Apply currency conversion to all transaction datasets
for df in [bank_records, internal_records, vendor_invoices]:
    df["Amount (INR)"] = df.apply(lambda x: convert_to_inr(x["Amount"], x["Currency"]), axis=1)


# Merge datasets to identify discrepancies (missing, extra, or mismatched transactions)
merged_records = pd.merge(
    bank_records, internal_records,
    on=["Date", "Amount (INR)", "Description"], 
    how="outer",  # Keeps all records from both datasets and marks differences
    indicator=True  # Adds a column indicating source of the transaction
)


# AI setup for Google AI Studio (Gemini API)
API_KEY = "YOUR_API_KEY"  # Replace with actual API key
genai.configure(api_key=API_KEY)


# Convert merged data to string format for AI analysis
data_text = merged_records.to_string()


# AI Prompt for Google Gemini AI
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


# Generate AI-powered financial reconciliation insights
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(prompt)


# Format the response to remove markdown-style formatting for better readability
formatted_response = response.text.replace("**", "").replace("__", "")  # Remove markdown formatting


# Save AI-generated insights to a text file for easy review
with open("reconciliation_report.txt", "w") as f:
    f.write(formatted_response)


# Confirmation message after reconciliation process is complete
print("Reconciliation complete! Check 'reconciliation_report.txt' for insights.")
