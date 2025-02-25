package com.mycompany.document;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import okhttp3.*;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class DocumentClassifier {

    // Folder paths for input invoices and sorted output
    private static final String INPUT_FOLDER = "invoices";
    private static final String OUTPUT_FOLDER = "sorted_invoices";

    // Google AI Gemini API details (Replace with your actual API key)
    private static final String API_KEY = "YOUR_API_KEY";  
    private static final String API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY;

    public static void main(String[] args) {
        File inputDirectory = new File(INPUT_FOLDER);
        
        // Check if the input directory exists and contains PDF files
        if (!inputDirectory.exists() || !inputDirectory.isDirectory()) {
            System.out.println("Input folder not found!");
            return;
        }

        File[] pdfFiles = inputDirectory.listFiles((dir, name) -> name.toLowerCase().endsWith(".pdf"));
        if (pdfFiles == null || pdfFiles.length == 0) {
            System.out.println("No PDF files found in the input folder!");
            return;
        }

        // Create the output directory if it doesn't exist
        new File(OUTPUT_FOLDER).mkdirs();

        // Process each PDF file
        for (File pdfFile : pdfFiles) {
            System.out.println("Processing: " + pdfFile.getName());

            // Extract text content from the PDF
            String extractedText = extractTextFromPdf(pdfFile);
            if (extractedText == null) continue;

            // Get company name from AI API
            String companyName = getCompanyNameFromAI(extractedText);
            if (companyName == null || companyName.isEmpty()) {
                System.out.println("Skipping: " + pdfFile.getName() + " (No company name found)");
                continue;
            }

            // Move the file to the respective company folder
            moveFileToCompanyFolder(pdfFile, companyName);
        }

        System.out.println("Document classification completed!");
    }

    /**
     * Extracts text content from a PDF file using Apache PDFBox.
     *
     * @param pdfFile The PDF file to extract text from.
     * @return Extracted text from the PDF file, or null if an error occurs.
     */
    private static String extractTextFromPdf(File pdfFile) {
        try (PDDocument document = PDDocument.load(pdfFile)) {
            PDFTextStripper pdfStripper = new PDFTextStripper();
            return pdfStripper.getText(document);
        } catch (IOException e) {
            System.err.println("Error reading PDF: " + pdfFile.getName() + " - " + e.getMessage());
            return null;
        }
    }

    /**
     * Sends extracted text to Google AI Gemini API and retrieves the company name.
     *
     * @param invoiceText The extracted text from the invoice PDF.
     * @return The company name identified in the invoice, or null if extraction fails.
     */
    private static String getCompanyNameFromAI(String invoiceText) {
        try {
            OkHttpClient client = new OkHttpClient();

            // Prepare the request body with extracted text
            String jsonBody = "{ \"contents\": [{ \"parts\": [{ \"text\": \"Extract the 'Ship To Party' company name from the following invoice text:\\n\\n" 
                              + invoiceText + "\\n\\nOnly return the company name without extra details.\" }]}]}";

            RequestBody requestBody = RequestBody.create(jsonBody, MediaType.get("application/json; charset=utf-8"));
            Request request = new Request.Builder().url(API_URL).post(requestBody).build();

            // Execute API call and handle response
            Response response = client.newCall(request).execute();
            if (!response.isSuccessful()) throw new IOException("API request failed: " + response.message());

            String responseBody = response.body().string();
            JsonObject jsonResponse = JsonParser.parseString(responseBody).getAsJsonObject();

            return jsonResponse.getAsJsonArray("candidates").get(0)
                    .getAsJsonObject().getAsJsonObject("content")
                    .getAsJsonArray("parts").get(0).getAsJsonObject()
                    .get("text").getAsString().trim();

        } catch (IOException e) {
            System.err.println("Error extracting company name from AI API: " + e.getMessage());
            return null;
        }
    }

    /**
     * Moves the processed invoice PDF to its corresponding company folder.
     *
     * @param pdfFile     The PDF file to be moved.
     * @param companyName The extracted company name used to determine the target folder.
     */
    private static void moveFileToCompanyFolder(File pdfFile, String companyName) {
        try {
            // Define the target folder path for the classified company
            File companyFolder = new File(OUTPUT_FOLDER + File.separator + companyName);
            if (!companyFolder.exists()) companyFolder.mkdirs();

            Path sourcePath = pdfFile.toPath();
            Path targetPath = companyFolder.toPath().resolve(pdfFile.getName());

            // Move the file to the classified company folder
            Files.move(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Moved: " + pdfFile.getName() + " -> " + companyFolder.getName());

        } catch (IOException e) {
            System.err.println("Error moving file: " + pdfFile.getName() + " - " + e.getMessage());
        }
    }
}
