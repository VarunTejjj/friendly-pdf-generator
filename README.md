Project Title: You Know, I Know - PDF Generator  
Created By: Varun Tej 

Description:
-------------
This project is a web-based PDF generator that collects detailed information about friends through a form and generates an official-style PDF document titled "You Know, I Know". It is intended for personal or creative use, such as memory sharing, group activities, or digital scrapbooking.

Features:
----------
- HTML frontend form to collect user data
- Flask backend to process the data and generate a PDF
- Automatically styles and formats the PDF
- Footer includes: "By Varun Tej"
- Hosted locally using KSWeb or Flask server on Android

Technologies Used:
--------------------
- HTML/CSS (Frontend UI)
- Python (Flask for backend)
- PDFKit or ReportLab (for PDF generation)
- KSWeb or Termux (for local hosting on Android)

Setup Instructions:
---------------------
1. Install KSWeb or set up Flask on your mobile using Termux.
2. Place the HTML files in the KSWeb `htdocs` folder or serve using Flask.
3. Ensure all dependencies like Flask and PDF generation libraries are installed.
4. Run the Flask server and access the form via your local IP (e.g., `localhost:5000`).
5. Fill in the form and generate the PDF.

Dependencies:
--------------
- Flask (`pip install flask`)
- PDF generation library (e.g., `pdfkit`, `reportlab`)
- For mobile: KSWeb or Termux with required packages

Notes:
-------
- Ensure `wkhtmltopdf` is installed if using PDFKit.
- Output PDFs are automatically styled and saved in the project folder.
- Works best on mobile browsers or localhost.

Credits:
---------
Project idea, design, and backend development by Varun Tej 
