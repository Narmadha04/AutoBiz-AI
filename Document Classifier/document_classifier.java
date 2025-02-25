package com.mycompany.document;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import okhttp3.*;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class document_classifier {

    private static final String INPUT_FOLDER = "invoices";
    private static final String OUTPUT_FOLDER = "sorted_invoice";
    private static final String API_KEY = "YOUR_API_KEY"; // Replace with your API key
    private static final String API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY;

    public static void main(String[] args) {
        File folder = new File(INPUT_FOLDER);
        if (!folder.exists() || !folder.isDirectory()) {
            System.out.println("Input folder not found!");
            return;
        }

        File[] files = folder.listFiles((dir, name) -> name.toLowerCase().endsWith(".pdf"));
        if (files == null || files.length == 0) {
            System.out.println("No PDF files found!");
            return;
        }

        new File(OUTPUT_FOLDER).mkdirs();

        for (File file : files) {
            System.out.println("Processing: " + file.getName());

            String text = extractTextFromPdf(file);
            if (text == null) continue;

            String companyName = getShipToParty(text);
            if (companyName == null || companyName.isEmpty()) {
                System.out.println("Skipping: " + file.getName() + " (No company name found)");
                continue;
            }

            moveFileToCompanyFolder(file, companyName);
        }

        System.out.println("Classification completed!");
    }

    private static String extractTextFromPdf(File file) {
        try (PDDocument document = PDDocument.load(file)) {
            PDFTextStripper pdfStripper = new PDFTextStripper();
            return pdfStripper.getText(document);
        } catch (IOException e) {
            System.err.println("Error reading PDF: " + file.getName() + " - " + e.getMessage());
            return null;
        }
    }

    private static String getShipToParty(String text) {
        try {
            OkHttpClient client = new OkHttpClient();
            String jsonBody = "{ \"contents\": [{ \"parts\": [{ \"text\": \"Extract the 'Ship To Party' company name from the following invoice text:\\n\\n" + text + "\\n\\nOnly return the company name without extra details.\" }]}]}";

            RequestBody body = RequestBody.create(jsonBody, MediaType.get("application/json; charset=utf-8"));
            Request request = new Request.Builder().url(API_URL).post(body).build();

            Response response = client.newCall(request).execute();
            if (!response.isSuccessful()) throw new IOException("API request failed");

            String responseBody = response.body().string();
            JsonObject jsonResponse = JsonParser.parseString(responseBody).getAsJsonObject();
            return jsonResponse.getAsJsonArray("candidates").get(0)
                    .getAsJsonObject().getAsJsonObject("content")
                    .getAsJsonArray("parts").get(0).getAsJsonObject()
                    .get("text").getAsString().trim();

        } catch (IOException e) {
            System.err.println("Error extracting company name: " + e.getMessage());
            return null;
        }
    }

    private static void moveFileToCompanyFolder(File file, String companyName) {
        try {
            File companyFolder = new File(OUTPUT_FOLDER + File.separator + companyName);
            if (!companyFolder.exists()) companyFolder.mkdirs();

            Path sourcePath = file.toPath();
            Path targetPath = companyFolder.toPath().resolve(file.getName());
            Files.move(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Moved: " + file.getName() + " -> " + companyFolder.getName());

        } catch (IOException e) {
            System.err.println("Error moving file: " + file.getName() + " - " + e.getMessage());
        }
    }
}
