import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# Global variables for GUI components
e1 = None  # Patient Number
e2 = None  # Name
e3 = None  # Age
e4 = None  # Gender
e5 = None  # Birthdate
e6 = None  # Contact Number
listBox = None
gender_var = None

def GetValue(event):
    global e1, e2, e3, e4, e5, e6, listBox
    
    # Clear existing entry values
    ClearEntries()

    # Retrieve selected row values
    selected_item = listBox.focus()
    if selected_item:
        values = listBox.item(selected_item)['values']
        if values:
            e1.insert(0, values[0])  # Patient Number
            e2.insert(0, values[1])  # Name
            e3.insert(0, values[2])  # Age
            e4.set(values[3])       # Gender
            e5.set_date(values[4])   # Birthdate
            e6.insert(0, values[5])  # Contact Number

def Add():
    global e1, e2, e3, e4, e5, e6, listBox, gender_var
    
    patient_number = e1.get()
    name = e2.get()
    age = e3.get()
    gender = gender_var.get()
    birthdate = e5.get_date().strftime('%Y-%m-%d') if e5.get_date() else None
    contact_number = e6.get()

    # Connect to MySQL database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="registration")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO patients (patient_number, name, age, gender, birthdate, contact_number) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (patient_number, name, age, gender, birthdate, contact_number)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Patient added successfully...")
        ClearEntries()
        show()
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Failed to add patient.")
        mysqldb.rollback()
    finally:
        mysqldb.close()

def ClearEntries():
    global e1, e2, e3, e4, e5, e6
    
    if e1:
        e1.delete(0, tk.END)
    if e2:
        e2.delete(0, tk.END)
    if e3:
        e3.delete(0, tk.END)
    if e4:
        e4.set('Male')  # Default gender
    if e5:
        e5.set_date(None)  # Clear DateEntry widget
    if e6:
        e6.delete(0, tk.END)

    if e1:
        e1.focus_set()

def show():
    global listBox
    
    # Connect to MySQL database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="registration")
    mycursor = mysqldb.cursor()
    
    try:
        listBox.delete(*listBox.get_children())  # Clear previous data
        mycursor.execute("SELECT * FROM patients")
        records = mycursor.fetchall()

        for record in records:
            listBox.insert("", "end", values=record)
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Failed to fetch patients.")
    finally:
        mysqldb.close()

# GUI setup
root = tk.Tk()
root.geometry("800x500")
root.title("Patient Registration")

tk.Label(root, text="Patient Registration", fg="red", font=(None, 30)).place(x=250, y=5)

tk.Label(root, text="Patient Number").place(x=10, y=50)
tk.Label(root, text="Name").place(x=10, y=80)
tk.Label(root, text="Age").place(x=10, y=110)
tk.Label(root, text="Gender").place(x=10, y=140)
tk.Label(root, text="Birthdate").place(x=10, y=170)
tk.Label(root, text="Contact Number").place(x=10, y=200)

e1 = tk.Entry(root)
e1.place(x=140, y=50)

e2 = tk.Entry(root)
e2.place(x=140, y=80)

e3 = tk.Entry(root)
e3.place(x=140, y=110)

gender_var = tk.StringVar(root)
gender_var.set('Male')  # Default gender
gender_option = ttk.Combobox(root, textvariable=gender_var, values=['Male', 'Female', 'Other'])
gender_option.place(x=140, y=140)

e5 = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
e5.place(x=140, y=170)

e6 = tk.Entry(root)
e6.place(x=140, y=200)

tk.Button(root, text="Add", command=Add).place(x=30, y=240)
tk.Button(root, text="Clear", command=ClearEntries).place(x=140, y=240)

cols = ('ID','Patient Number', 'Name', 'Age', 'Gender', 'Birthdate', 'Contact Number')
listBox = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=280)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()
