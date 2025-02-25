# 📧 AI-Powered Invoice Reminder System

## Project Overview
This AI-powered email reminder system automates the process of sending invoice payment reminders using Google AI (Gemini API) and Gmail API.  
It reads unpaid invoices from a CSV file, generates personalized AI-powered email content, and sends reminders automatically.

---

## Features & Enhancements

- **AI-Generated Email Content** – Uses Google Gemini API to craft polite, personalized reminder emails.
- **Automated Invoice Tracking** – Reads unpaid invoices from a CSV file and sends reminders accordingly.
- **Seamless Gmail Integration** – Sends emails securely using the Gmail API.
- **Optimized Email Formatting** – Generates professional, structured emails based on invoice details.
- **Secure Authentication** – Uses OAuth 2.0 for Gmail API access, ensuring data privacy.  

## How It Works

- **Reads unpaid invoices** from a **CSV file** (`reminders.csv`).
- **Generates AI-crafted email content** for each unpaid invoice using **Google Gemini API**.
- **Authenticates Gmail API** and establishes a secure connection.
- **Sends automated reminders** to customers who haven’t paid.  

## Technologies Used

- **Programming Language:** Python
- **Cloud AI Services:** Google Gemini API (for AI-generated emails)  
- **Google APIs:** Gmail API (for email automation)  
- **Data Processing:** Pandas (for handling invoice data)  
- **OAuth Authentication:** Google Auth Library (for secure access)  

---

## 📂 Folder Structure

```plaintext
/email-reminder-system
├── src/                          # Source code
│   ├── email_sender.py           # Handles email generation & sending
│   ├── requirements.txt          # Required Python dependencies
│
├── data/                          # Stores invoice data
│   ├── reminders.csv              # CSV file with invoice details
│
├── credentials/                   # Stores Google API credentials
│   ├── client_secret.json         # API credentials file (not to be shared)
│   ├── credentials.json           # Counsole credentials file (not to be shared)
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

### 2)  Authenticate Gmail API
i) **Obtain Google API Credentials**:  
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)  
   - Enable the **Gmail API** and create OAuth credentials.  
   - Download the **client_secret.json** file and place it in the `credentials/` folder.  

ii) **Authenticate OAuth**:  
   Run the script once to authenticate and generate a **token file**:
   ```bash
   python main.py
   ```

### 3) Run the Invoice Reminder Script
```bash
python main.py
```
---

## Code Breakdown & Enhancements

### `main.py` – Core Automation Script
- **Reads invoice data** from `reminders.csv`.
- **Generates AI-powered email content** using Google Gemini API.
- **Authenticates Gmail API** via OAuth 2.0.
- **Sends email reminders** to customers who haven't paid.  

### `authentication.py` – Secure OAuth Handling
- **Manages Gmail API authentication** securely.
- **Refreshes OAuth tokens** when expired.
- **Stores authentication tokens** locally for reusability.  

### `email_sender.py` – AI Email Generation & Sending
- **Uses Gemini API** to craft **polite, professional email reminders**.
- **Formats email content** based on invoice details.
- **Sends emails securely** using the **Gmail API**.  
