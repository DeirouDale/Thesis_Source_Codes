import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from reportlab.lib.pagesizes import legal, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(client_id, consultation_date, assessment_num, phase_data_dict, landscape_mode=False):
    try:
        # Generate PDF
        orientation = landscape(legal) if landscape_mode else legal
        pdf_filename = f"PDF/{client_id}_{consultation_date}_{assessment_num}_data.pdf"
        
        doc = SimpleDocTemplate(pdf_filename, pagesize=orientation, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

        # Create Paragraph objects for client_id and assessment_num
        styles = getSampleStyleSheet()
        client_id_text = Paragraph(f"",styles['Normal'])


        # Additional paragraph
        question_style = styles['Normal']
        question_style.fontSize = 12  # Set font size to 12 (adjust as needed)
        question_text = Paragraph("Based on the Image, is the Insole Output Possible?", question_style)

        # Build PDF
        content = [client_id_text, Spacer(1, 10), question_text, Spacer(1, 10)]

        # Right Side
        side_text = Paragraph("<b>Right Side</b>", styles['Normal'])
        content.extend([side_text, Spacer(1, 10)])

        # Iterate over phases and their data to create tables for Right Side
        for phase, (table_data, columns) in phase_data_dict['Right'].items():
            # Create Paragraph for phase
            phase_text = Paragraph(f"<b>Phase:</b> {phase}", styles['Normal'])
            content.extend([phase_text, Spacer(1, 10)])

            # Exclude 'Side' and 'Phase' columns from table headers and data
            columns_without_side_phase = [col for col in columns if col not in ['Side', 'Phase','Hips','Knees','Ankle','Frame']]

            # Add headers to the table (excluding 'Side' and 'Phase')
            table_headers = [Paragraph(header, styles['Normal']) for header in columns_without_side_phase]

            # Add two blank columns for "Yes" and "No"
            table_headers.extend([Paragraph("Yes", styles['Normal']), Paragraph("No", styles['Normal'])])

            # Create table with data
            table_with_headers = [table_headers]  # Add headers as the first row
            for row in table_data:
                table_row = []
                for index, cell in enumerate(row):
                    if columns[index] not in ['Side', 'Phase','Hips','Knees','Ankle','Frame']:  # Exclude 'Side' and 'Phase' columns
                        if columns[index] == 'Image':
                            # Display the image directly
                            image_path = cell  # Assuming cell contains the path to the image
                            table_row.append(Image(image_path, width=100, height=100))
                        elif columns[index] == 'Insole':
                            # Fetch the 'side' value from the fetched data
                            side = row[columns.index('Side')]
                            # Construct image path based on numerical data and side
                            image_path = f"/home/silog/Thesis_Source_Codes/Data Inputs/insole_rep/{side}/{cell}.jpg"  # Adjust the path as per your directory structure
                            table_row.append(Image(image_path, width=100, height=100))
                        else:
                            table_row.append(str(cell))  # Convert cell to string
                # Add two blank cells for "Yes" and "No"
                table_row.extend(['', ''])
                table_with_headers.append(table_row)

            # Define column widths for the blank columns
            col_widths = [None] * len(columns_without_side_phase) + [40, 40]  # Adjust the width as needed

            table = Table(table_with_headers, colWidths=col_widths)

            # Add style to table (same as before)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Header background color
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # All cells alignment
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data background color
                ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Gridlines color
            ])
            table.setStyle(style)
            content.append(table)
            content.append(Spacer(1, 10))


        # Left Side
        side_text = Paragraph("<b>Left Side</b>", styles['Normal'])
        content.extend([side_text, Spacer(1, 10)])

        # Iterate over phases and their data to create tables for Left Side
        for phase, (table_data, columns) in phase_data_dict['Left'].items():
            # Create Paragraph for phase
            phase_text = Paragraph(f"<b>Phase:</b> {phase}", styles['Normal'])
            content.extend([phase_text, Spacer(1, 10)])

            # Exclude 'Side' and 'Phase' columns from table headers and data
            columns_without_side_phase = [col for col in columns if col not in ['Side', 'Phase','Hips','Knees','Ankle','Frame']]

            # Add headers to the table (excluding 'Side' and 'Phase')
            table_headers = [Paragraph(header, styles['Normal']) for header in columns_without_side_phase]

            # Add two blank columns for "Yes" and "No"
            table_headers.extend([Paragraph("Yes", styles['Normal']), Paragraph("No", styles['Normal'])])

            # Create table with data
            table_with_headers = [table_headers]  # Add headers as the first row
            for row in table_data:
                table_row = []
                for index, cell in enumerate(row):
                    if columns[index] not in ['Side', 'Phase','Hips','Knees','Ankle','Frame']:  # Exclude 'Side' and 'Phase' columns
                        if columns[index] == 'Image':
                            # Display the image directly
                            image_path = cell  # Assuming cell contains the path to the image
                            table_row.append(Image(image_path, width=100, height=100))
                        elif columns[index] == 'Insole':
                            # Fetch the 'side' value from the fetched data
                            side = row[columns.index('Side')]
                            # Construct image path based on numerical data and side
                            image_path = f"/home/silog/Thesis_Source_Codes/Data Inputs/insole_rep/{side}/{cell}.jpg"  # Adjust the path as per your directory structure
                            table_row.append(Image(image_path, width=100, height=100))
                        else:
                            table_row.append(str(cell))  # Convert cell to string
                # Add two blank cells for "Yes" and "No"
                table_row.extend(['', ''])
                table_with_headers.append(table_row)

            # Define column widths for the blank columns
            col_widths = [None] * len(columns_without_side_phase) + [40, 40]  # Adjust the width as needed

            table = Table(table_with_headers, colWidths=col_widths)

            # Add style to table (same as before)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Header background color
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # All cells alignment
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data background color
                ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Gridlines color
            ])
            table.setStyle(style)
            content.append(table)
            content.append(Spacer(1, 10))


        # Build PDF
        doc.build(content)

        messagebox.showinfo("PDF Created", f"PDF '{pdf_filename}' has been successfully created!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def fetch_image_path(image_id):
    # Placeholder function to fetch image path from database based on image ID
    # Replace this with your actual method of fetching image paths
    return "path/to/image.jpg"  # Dummy path, replace with actual path


def fetch_consultation_dates(client_id):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",  # Updated port number
            user="gaitrpi",  # Default XAMPP MySQL username
            password="gait123",  # Default XAMPP MySQL password is empty
            database="gaitdata"  # Replace with your database name
        )

        # Create cursor
        cursor = conn.cursor()

        # Fetch distinct consultation dates for the given client ID
        cursor.execute(f"SELECT DISTINCT date_time FROM assessment WHERE client_id = {client_id}")
        consultation_dates = [date[0] for date in cursor.fetchall()]

        # Close cursor and connection
        cursor.close()
        conn.close()

        return consultation_dates

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_assessment_numbers(client_id, consultation_date):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",  # Updated port number
            user="gaitrpi",  # Default XAMPP MySQL username
            password="gait123",  # Default XAMPP MySQL password is empty
            database="gaitdata"  # Replace with your database name
        )

        # Create cursor
        cursor = conn.cursor()

        # Fetch distinct assessment numbers for the given client ID and consultation date
        cursor.execute(f"SELECT DISTINCT assessment_num FROM assessment WHERE client_id = {client_id} AND date_time = '{consultation_date}'")
        assessment_numbers = [num[0] for num in cursor.fetchall()]

        # Close cursor and connection
        cursor.close()
        conn.close()

        return assessment_numbers

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_phase_data(client_id, consultation_date, assessment_num):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="gaitrpi",
            password="gait123",
            database="gaitdata"
        )

        # Create cursor
        cursor = conn.cursor()

        # Fetch phases and their corresponding data for the given client ID, consultation date, and assessment number
        cursor.execute(f"SELECT DISTINCT phase FROM assessment WHERE client_id = {client_id} AND date_time = '{consultation_date}' AND assessment_num = {assessment_num} ORDER BY phase ASC")
        phases = [phase[0] for phase in cursor.fetchall()]

        # Initialize dictionaries to store table data for each phase and side
        phase_data_dict = {'Right': {}, 'Left': {}}

        # Iterate over each phase
        for phase in phases:
            # Fetch data from the selected table for the current phase, selecting all columns including 'side'
            query = f"SELECT image, frame, hips, knees, ankle, insole, side FROM assessment WHERE client_id = {client_id} AND date_time = '{consultation_date}' AND assessment_num = {assessment_num} AND phase = '{phase}'"
            cursor.execute(query)
            data = cursor.fetchall()

            # Iterate over the fetched data
            for row in data:
                side = row[-1]  # Get the side from the fetched data
                if side in phase_data_dict:
                    if phase not in phase_data_dict[side]:
                        phase_data_dict[side][phase] = ([], ['Image', 'Frame', 'Hips', 'Knees', 'Ankle', 'Insole', 'Side'])
                    phase_data_dict[side][phase][0].append(row)

        # Close cursor and connection
        cursor.close()
        conn.close()

        return phase_data_dict

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def on_generate_pdf():
    try:
        selected_client_id = client_id_var.get()
        selected_consultation_date = consultation_var.get()
        selected_assessment_num = assessment_num_var.get()
        phase_data_dict = fetch_phase_data(selected_client_id, selected_consultation_date, selected_assessment_num)
        if phase_data_dict:
            landscape_mode = var_orientation.get() == 1
            generate_pdf(selected_client_id, selected_consultation_date, selected_assessment_num, phase_data_dict, landscape_mode)
        else:
            messagebox.showerror("Error", "No data found for the selected client ID, consultation date, and assessment number.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating PDF: {e}")

def on_client_select():
    selected_client_id = client_id_var.get()
    consultation_dates = fetch_consultation_dates(selected_client_id)
    consultation_var.set("")  # Clear previous selection
    consultation_menu['values'] = consultation_dates

def on_consultation_date_select(*args):
    selected_client_id = client_id_var.get()
    selected_consultation_date = consultation_var.get()
    assessment_numbers = fetch_assessment_numbers(selected_client_id, selected_consultation_date)
    assessment_num_var.set("")  # Clear previous selection
    assessment_num_menu['values'] = assessment_numbers

# Connect to MySQL database to get client IDs
def fetch_client_ids():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",  # Updated port number
            user="gaitrpi",  # Default XAMPP MySQL username
            password="gait123",  # Default XAMPP MySQL password is empty
            database="gaitdata"  # Replace with your database name
        )

        # Create cursor
        cursor = conn.cursor()

        # Fetch distinct client IDs
        cursor.execute("SELECT DISTINCT client_id FROM assessment")
        client_ids = [client_id[0] for client_id in cursor.fetchall()]

        # Close cursor and connection
        cursor.close()
        conn.close()

        return client_ids

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create Tkinter GUI
root = tk.Tk()
root.title("PDF Generator")

# Dropdown menu to select client ID
client_id_var = tk.StringVar(root)
client_id_var.trace('w', on_client_select)
client_id_menu = ttk.Combobox(root, textvariable=client_id_var, state="readonly")
client_id_menu.pack(pady=5)
client_ids = fetch_client_ids()
client_id_menu['values'] = client_ids

# Input field for Client ID
client_id_label = tk.Label(root, text="Or enter Client ID manually:")
client_id_label.pack(pady=5)
client_id_entry = tk.Entry(root)
client_id_entry.pack(pady=5)

# Button to fetch consultation dates
fetch_dates_button = tk.Button(root, text="Fetch Consultation Dates", command=on_client_select)
fetch_dates_button.pack(pady=5)

# Dropdown menu to select consultation date
consultation_var = tk.StringVar(root)
consultation_var.trace('w', on_consultation_date_select)
consultation_menu = ttk.Combobox(root, textvariable=consultation_var, state="readonly")
consultation_menu.pack(pady=5)

# Dropdown menu to select assessment number
assessment_num_var = tk.StringVar(root)
assessment_num_menu = ttk.Combobox(root, textvariable=assessment_num_var, state="readonly")
assessment_num_menu.pack(pady=5)

# Checkbox for page orientation
var_orientation = tk.IntVar(value=0)  # 0: Portrait, 1: Landscape
orientation_checkbox = tk.Checkbutton(root, text="Landscape", variable=var_orientation)
orientation_checkbox.pack(pady=5)

# Button to generate PDF
generate_button = tk.Button(root, text="Generate PDF", command=on_generate_pdf)
generate_button.pack(pady=10)

root.mainloop()
