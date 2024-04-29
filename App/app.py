from flask import Flask, render_template, request, jsonify, send_file
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ensure_upload_dir_exists():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def generate_pdf(club_name, event_name, event_description, attendance, date, time, venue, image_filename):
    current_directory = os.getcwd()
    report_filename = 'report.pdf'

    if image_filename:
        image_path = os.path.join(current_directory, UPLOAD_FOLDER, image_filename)
        if not os.path.exists(image_path):
            print("Error: Image file does not exist at the expected path.")
            return

        with canvas.Canvas(os.path.join(app.config['UPLOAD_FOLDER'], report_filename), pagesize=letter) as c:
            c.drawString(100, 750, f'Club Name: {club_name}')
            c.drawString(100, 730, f'Event Name: {event_name}')
            c.drawString(100, 710, f'Event Description: {event_description}')
            c.drawString(100, 690, f'Attendance: {attendance}')
            c.drawString(100, 670, f'Date: {date}')
            c.drawString(100, 650, f'Time: {time}')
            c.drawString(100, 630, f'Venue: {venue}')
            c.drawImage(image_path, 100, 500, width=200, height=200)

def save_uploaded_file(file):
    if file and file.filename != '':
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    club_name = request.form['club_name']
    event_name = request.form['event_name']
    event_description = request.form['event_description']
    attendance_str = request.form['attendance']
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']

    ensure_upload_dir_exists()

    image_filename = save_uploaded_file(request.files['image'])

    try:
        attendance = int(attendance_str) if attendance_str else 0
    except ValueError:
        print("Invalid value for attendance, setting it to 0")
        attendance = 0

    generate_pdf(club_name, event_name, event_description, attendance, date, time, venue, image_filename)

    response_data = {'message': 'Report submitted successfully!'}
    return jsonify(response_data)

@app.route('/download_report', methods=['GET'])
def download_report():
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf')
    return send_file(report_path, as_attachment=True)

@app.route('/preview_report', methods=['GET'])
def preview_report():
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'report.pdf')
    return send_file(report_path, mimetype='application/pdf')

@app.route('/next_page.html')
def next_page():
    return render_template('next_page.html')

if __name__ == '__main__':
    app.run(debug=True)
