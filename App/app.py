from flask import Flask, render_template, request
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
    # Get the absolute path to the current directory
    current_directory = os.getcwd()
    
    # Construct the absolute path to the image file
    image_path = os.path.join(current_directory, UPLOAD_FOLDER, image_filename)
    
    # Print the absolute path
    print("Expected image path:", image_path)
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print("Error: Image file does not exist at the expected path.")
        return
    
    # Now you can proceed to generate the PDF with the image
    
    c = canvas.Canvas('report.pdf', pagesize=letter)
    c.drawString(100, 750, f'Club Name: {club_name}')
    c.drawString(100, 730, f'Event Name: {event_name}')
    c.drawString(100, 710, f'Event Description: {event_description}')
    c.drawString(100, 690, f'Attendance: {attendance}')
    c.drawString(100, 670, f'Date: {date}')
    c.drawString(100, 650, f'Time: {time}')
    c.drawString(100, 630, f'Venue: {venue}')
    if image_filename is not None:
        c.drawImage(image_path, 100, 500, width=200, height=200)
    c.save()

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    club_name = request.form['club_name']
    event_name = request.form['event_name']
    event_description = request.form['event_description']
    attendance_str = request.form['attendance']  # Get the attendance value as string
    date = request.form['date']
    time = request.form['time']
    venue = request.form['venue']

    # Ensure the 'uploads' directory exists
    ensure_upload_dir_exists()

    # Handle file upload
    file = request.files['image']
    if file and file.filename != '':
        filename = file.filename
        print("Image filename:", filename)  # Add this line to print the filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None

    try:
        # Convert attendance string to integer, provide default value if empty
        attendance = int(attendance_str) if attendance_str else 0
    except ValueError:
        # Handle the case where the attendance value is not a valid integer
        print("Invalid value for attendance, setting it to 0")
        attendance = 0

    # Generate PDF report
    generate_pdf(club_name, event_name, event_description, attendance, date, time, venue, filename)

    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
