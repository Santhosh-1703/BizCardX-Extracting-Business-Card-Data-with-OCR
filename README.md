# BizCardX-Extracting-Business-Card-Data-with-OCR

BizCardX Project Overview:

Purpose: Automate extraction of business card details for further analysis.
Technology Stack:
Streamlit
EasyOCR
OpenCV
Regular Expressions
MySQL Database

EasyOCR:
Simple installation with a single pip command.
Minimal dependencies for easy configuration.
Only one import statement needed in the project.
Two lines of code to perform OCR using the readtext function.

Features:
Extracts text using EasyOCR.
Utilizes OpenCV for image preprocessing.
Uses regex to parse and extract specific fields.
Stores data in a MySQL database.
Streamlit-based user-friendly interface.

Workflow:
Install required libraries (Streamlit, mysql.connector, pandas, easyocr).
Three menu options: HOME, UPLOAD & EXTRACT, MODIFY.
Extracted data classified using regex.
User review and editing of extracted data.
Upload to MySQL database with a click

Usage:
Access the app through the Streamlit interface.
Upload business cards, extract, and manage data easily.

Data Modification:
Read, update, and delete operations available in the MODIFY menu.
