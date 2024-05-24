import customtkinter as ctk
import tkinter.messagebox as tkmb

# Set GUI appearance and color theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

# Create the main application window
app = ctk.CTk()
app.geometry("400x400")
app.title("Modern Login UI using Customtkinter")

# Function for handling login button click
def login():
    username = "Geeks"
    password = "12345"
    entered_username = user_entry.get()
    entered_password = user_pass.get()
    
    if entered_username == username and entered_password == password:
        tkmb.showinfo(title="Login Successful", message="You have logged in successfully!")
        show_welcome_message()
    elif entered_username == username and entered_password != password:
        tkmb.showwarning(title='Wrong Password', message='Please check your password.')
    elif entered_username != username and entered_password == password:
        tkmb.showwarning(title='Wrong Username', message='Please check your username.')
    else:
        tkmb.showerror(title="Login Failed", message="Invalid username and password.")

# Function to show a welcome message in a new window upon successful login
def show_welcome_message():
    welcome_window = ctk.CTkToplevel(app)
    welcome_window.title("Welcome!")
    welcome_message = "GeeksforGeeks is the best for learning ANYTHING!!"
    ctk.CTkLabel(welcome_window, text=welcome_message).pack(pady=20, padx=30)

# Main UI components
main_label = ctk.CTkLabel(app, text="Welcome to our Modern Login System")
main_label.pack(pady=20)

login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=20, padx=40)

login_label = ctk.CTkLabel(login_frame, text='Login')
login_label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(login_frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

login_button = ctk.CTkButton(login_frame, text='Login', command=login)
login_button.pack(pady=12, padx=10)

remember_checkbox = ctk.CTkCheckBox(login_frame, text='Remember Me')
remember_checkbox.pack(pady=12, padx=10)

# Run the application
app.mainloop()
