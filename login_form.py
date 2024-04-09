import customtkinter as ctk
import tkinter.messagebox as tkmb

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

def login():
    username = "thesis"
    password = "silog"
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    
    if entered_username == username and entered_password == password:
        tkmb.showinfo(title="Login Successful", message="You have logged in successfully!")
        clear_entries()
    else:
        tkmb.showerror(title="Login Failed", message="Invalid username or password.")


def clear_entries():
    username_entry.delete(0, ctk.END)
    password_entry.delete(0, ctk.END)


def show_registration_form():
    registration_window = ctk.CTkToplevel(app)
    registration_window.title("Registration")

    def register():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        confirm_password = reg_confirm_password_entry.get()

        if password != confirm_password:
            tkmb.showerror(title="Error", message="Passwords do not match.")
        else:
            tkmb.showinfo(title="Registration Successful", message="Registration successful!")
            registration_window.destroy()  # Close registration window after successful registration

    reg_username_label = ctk.CTkLabel(registration_window, text='Username')
    reg_username_label.pack(pady=12, padx=10)

    reg_username_entry = ctk.CTkEntry(registration_window, placeholder_text="Enter Username")
    reg_username_entry.pack(pady=12, padx=10)

    reg_password_label = ctk.CTkLabel(registration_window, text='Password')
    reg_password_label.pack(pady=12, padx=10)

    reg_password_entry = ctk.CTkEntry(registration_window, placeholder_text="Enter Password", show="*")
    reg_password_entry.pack(pady=12, padx=10)

    reg_confirm_password_label = ctk.CTkLabel(registration_window, text='Confirm Password')
    reg_confirm_password_label.pack(pady=12, padx=10)

    reg_confirm_password_entry = ctk.CTkEntry(registration_window, placeholder_text="Confirm Password", show="*")
    reg_confirm_password_entry.pack(pady=12, padx=10)

    reg_button = ctk.CTkButton(registration_window, text='Register', command=register)
    reg_button.pack(pady=12, padx=10)


app = ctk.CTk()
app.geometry("400x450")
app.title("Login Form")

main_label = ctk.CTkLabel(app, text="Welcome to our Modern Login System")
main_label.pack(pady=20)

login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=20, padx=40)

username_label = ctk.CTkLabel(login_frame, text='Username')
username_label.pack(pady=12, padx=10)

username_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter Username")
username_entry.pack(pady=12, padx=10)

password_label = ctk.CTkLabel(login_frame, text='Password')
password_label.pack(pady=12, padx=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter Password", show="*")
password_entry.pack(pady=12, padx=10)

login_button = ctk.CTkButton(login_frame, text='Login', command=login)
login_button.pack(pady=12, padx=10)

register_button = ctk.CTkButton(app, text='Register', command=show_registration_form)
register_button.pack(pady=10)

app.mainloop()
