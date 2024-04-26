from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def generate_pdf(club_name, event_name, attendance, budget_spent, filename, orientation='portrait', background_color=None):
    # Set the page size and orientation
    if orientation == 'landscape':
        page_size = landscape(letter)
    else:
        page_size = letter

    # Create a PDF document
    doc = SimpleDocTemplate(filename, pagesize=page_size)

    # Content for the PDF
    content = []

    # Sample text content
    text = f"Club Name: {club_name}\nEvent Name: {event_name}\nAttendance: {attendance}\nBudget Spent: {budget_spent}"
    content.append(Paragraph(text, styles["Normal"]))

    # Add more content as needed

    # Set background color if specified
    if background_color:
        doc.pagesize = landscape(letter)
        doc.setFillColor(background_color)
        doc.rect(0, 0, doc.width, doc.height, fill=True)

    # Build the PDF document
    doc.build(content)

# Define styles for text
styles = getSampleStyleSheet()
styles["Normal"].fontName = "Helvetica"
styles["Normal"].fontSize = 12
styles["Normal"].textColor = colors.black
