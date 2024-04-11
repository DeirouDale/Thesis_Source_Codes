import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Establishing connection to MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="registration"
)

# Function to create a new patient record
def create_patient():
    patient_number = patient_number_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    birthdate = birthdate_entry.get()
    address = address_entry.get()

    cursor = db_connection.cursor()
    insert_query = "INSERT INTO patients (patient_number, name, age, gender, birthdate, address) VALUES (%s, %s, %s, %s, %s, %s)"
    patient_data = (patient_number, name, age, gender, birthdate, address)
    
    try:
        cursor.execute(insert_query, patient_data)
        db_connection.commit()
        messagebox.showinfo("Success", "Patient created successfully!")
        clear_fields()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating patient: {err}")
    
    cursor.close()

# Function to update an existing patient record
def update_patient():
    patient_id = update_id_entry.get()
    new_address = new_address_entry.get()

    cursor = db_connection.cursor()
    update_query = "UPDATE patients SET address = %s WHERE id = %s"
    
    try:
        cursor.execute(update_query, (new_address, patient_id))
        db_connection.commit()
        messagebox.showinfo("Success", "Patient updated successfully!")
        clear_update_fields()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating patient: {err}")
    
    cursor.close()

# Function to delete an existing patient record
def delete_patient():
    patient_id = delete_id_entry.get()

    cursor = db_connection.cursor()
    delete_query = "DELETE FROM patients WHERE id = %s"
    
    try:
        cursor.execute(delete_query, (patient_id,))
        db_connection.commit()
        messagebox.showinfo("Success", "Patient deleted successfully!")
        delete_id_entry.delete(0, tk.END)  # Clear the entry field after deletion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error deleting patient: {err}")
    
    cursor.close()

# Function to clear entry fields for creating a new patient
def clear_fields():
    patient_number_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_var.set("Male")
    birthdate_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Function to clear entry fields for updating a patient
def clear_update_fields():
    update_id_entry.delete(0, tk.END)
    new_address_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Patient Management System")

# Create labels and entry fields for patient details
tk.Label(root, text="Patient Number:").grid(row=0, column=0, padx=10, pady=5)
patient_number_entry = tk.Entry(root)
patient_number_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Age:").grid(row=2, column=0, padx=10, pady=5)
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Gender:").grid(row=3, column=0, padx=10, pady=5)
gender_var = tk.StringVar(root)
gender_var.set("Male")
gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female", "Other")
gender_menu.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Birthdate (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
birthdate_entry = tk.Entry(root)
birthdate_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Contact Number:").grid(row=5, column=0, padx=10, pady=5)
address_entry = tk.Entry(root)
address_entry.grid(row=5, column=1, padx=10, pady=5)

# Create buttons for CRUD operations (Create, Update, Delete)
tk.Button(root, text="Create", command=create_patient).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="Clear", command=clear_fields).grid(row=6, column=1, padx=10, pady=10)

# Create labels and entry fields for updating a patient
tk.Label(root, text="Patient ID to Update:").grid(row=7, column=0, padx=10, pady=5)
update_id_entry = tk.Entry(root)
update_id_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="New Contact Number:").grid(row=8, column=0, padx=10, pady=5)
new_address_entry = tk.Entry(root)
new_address_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Button(root, text="Update", command=update_patient).grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Create labels and entry field for deleting a patient
tk.Label(root, text="Patient ID to Delete:").grid(row=10, column=0, padx=10, pady=5)
delete_id_entry = tk.Entry(root)
delete_id_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Button(root, text="Delete", command=delete_patient).grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Run the main event loop
root.mainloop()

# Close the database connection
db_connection.close()
