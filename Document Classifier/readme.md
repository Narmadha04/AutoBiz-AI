# 📄Document Classification System

## Project Overview
This AI-powered document classification system automates invoice processing by extracting company names and sorting invoices into respective folders. It combines Google AI (Gemini API) with machine learning (ML) techniques to ensure high-accuracy text classification while providing a robust backup mechanism using local ML-based classification.

## Features & Enhancements

- **Hybrid AI-ML Approach** – Uses Google Gemini API for AI-based text classification and local ML models for backup predictions.
- **Smart Invoice Sorting** – Extracts company names and automatically organizes invoices into company-specific folders.
- **High Accuracy NLP & ML** – Uses Named Entity Recognition (NER), TF-IDF, and Word2Vec to enhance classification.
- **Optimized File Handling** – Efficiently processes large volumes of PDFs with Apache PDFBox.
- **Resilient System** – Implements error handling, logging, and backup classification methods to ensure reliability.  

---

## How It Works

- **Extracts text from invoices** using **Apache PDFBox**.
-  **Sends extracted text to Google Gemini API** to predict the "Ship To Party" (Company Name).
-   **ML-Based Backup Classification:** If the AI output is uncertain, the system uses **local ML classification models** (TF-IDF, keyword-based, Named Entity Recognition).
- **Confidence Scoring Mechanism** – AI & ML predictions are compared, and the most reliable classification is chosen.
- **Automated File Sorting** – Invoices are moved to **company-specific folders** for easy retrieval.  

## Technologies Used

- **Programming Language:** Java (Maven Project)  
- **Cloud AI Services:** Google Gemini API (for NLP-based classification)  
- **Machine Learning Models:** TF-IDF, Named Entity Recognition (NER), Word2Vec  
- **Text Extraction:** Apache PDFBox (for parsing PDFs)  
- **Networking:** OkHttp (HTTP requests for API interaction)  
- **File Handling:** Java NIO & IO (for optimized file operations)  

---

## 📂 Folder Structure

```plaintext
/document-classification
├── src/                        # Source code
├── invoices/                   # Input PDF files
├── sorted_invoice/             # AI-sorted output files
├── pom.xml                     # Maven dependencies & configurations
└── tests/                      # Unit & integration test cases
```

---

## Setup & Execution

### 1) Install Dependencies
Ensure **Java 11+** and **Maven** are installed, then run:
```bash
mvn clean install
```

### 2) Run the Application
Place invoices inside the `/invoices/` folder, then execute:
```bash
mvn exec:java -Dexec.mainClass="com.mycompany.document.InvoiceClassifier"
```

**Invoices will be automatically classified and sorted into company-specific folders.**  

---

## Code Breakdown & Enhancements

###  `document_classifier.java` – Core Classification Logic
- **Extracts text from PDFs** using **Apache PDFBox**.
- **Sends text to Google Gemini API** to extract the "Ship To Party" (Company Name).
- **Implements ML-based backup classification** if AI confidence is low.
- **Uses a confidence scoring mechanism** to resolve conflicting predictions.
- **Moves invoices to appropriate folders** based on classification results.  

###  `pom.xml` – Maven Configuration & Dependencies
- **Integrates Google Gemini API** via **OkHttp & GSON**.
- **Uses Apache PDFBox** for **text extraction** from invoices.
- **Includes Java 11 compiler settings** for compatibility.  
