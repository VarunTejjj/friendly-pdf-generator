from flask import Flask, request, send_file, send_from_directory
from fpdf import FPDF
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/data/data/com.termux/files/home/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Yo lo sé, ¿tú lo sabes?', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'By Varun Tej', align='C')

    def add_photo(self, photo_path):
        if os.path.exists(photo_path):
            self.image(photo_path, x=65, w=80)  # center-aligned image
            self.ln(85)

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
    if 'photo' in request.files:
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)
    else:
        photo_path = None

    data = request.form

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

    pdf = PDF()
    pdf.add_page()

    if photo_path:
        pdf.add_photo(photo_path)

    for title, content in sections.items():
        pdf.add_section(title, content)

    filename = f"friend_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("/data/data/com.termux/files/home", filename)
    pdf.output(filepath)

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)