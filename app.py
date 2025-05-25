from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Yo lo sé, ¿tú lo sabes?', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'By Varun Tej', align='C')

    def add_section(self, title, data):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 12)
        self.set_text_color(0, 0, 0)
        for key, value in data.items():
            if value:
                self.multi_cell(0, 10, f"{key}: {value}")
        self.ln(5)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Get form data
        data = request.form.to_dict()
        photo = request.files.get('photo')  # Uploaded file

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Save uploaded photo (optional)
        if photo:
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(photo_path)
        else:
            photo_path = None  # In case you want to use it later

        # Data sections
        sections = {
            "Basic Information": {
                "Full Name": data.get("fullName"),
                "Nickname": data.get("nickname"),
                "Gender": data.get("gender"),
                "Date of Birth": data.get("dob"),
                "Age": data.get("age"),
                "Blood Group": data.get("bloodGroup")
            },
            "Contact Information": {
                "Phone": data.get("phone"),
                "Email": data.get("email"),
                "Address": data.get("address"),
                "City": data.get("city"),
                "State": data.get("state"),
                "PIN Code": data.get("pin")
            },
            "Personal Info": {
                "Hobbies": data.get("hobbies"),
                "Favorite Food": data.get("favFood"),
                "Favorite Color": data.get("favColor"),
                "Favorite Game/Movie/Song": data.get("favGame"),
                "Best Friend's Name": data.get("bestFriend"),
                "Crush or Lover": data.get("crush")
            },
            "School/College Info": {
                "School/College Name": data.get("school"),
                "Class/Grade": data.get("class"),
                "Favorite Subject": data.get("favSubject"),
                "Least Favorite Subject": data.get("leastFavSubject"),
                "Achievements": data.get("achievements")
            },
            "Social Media": {
                "Instagram ID": data.get("instagram"),
                "Telegram Username": data.get("telegram"),
                "WhatsApp Number": data.get("whatsapp")
            },
            "Fun & Memories": {
                "Funniest Memory": data.get("memory"),
                "What You Like Most About Them": data.get("likes"),
                "Personal Message or Quote": data.get("message")
            }
        }

        # Create PDF
        pdf = PDF()
        pdf.add_page()
        for title, content in sections.items():
            pdf.add_section(title, content)

        filename = f"you_know_i_know_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join("/tmp", filename)
        pdf.output(filepath)

        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
