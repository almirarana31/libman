import customtkinter
from tkinter import messagebox
from app import LibraryApp

class LoginPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("400x250")

        # Create login form
        self.username_label = customtkinter.CTkLabel(self, text="Username")
        self.username_label.pack(pady=10)

        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.pack(pady=5)

        self.password_label = customtkinter.CTkLabel(self, text="Password")
        self.password_label.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.check_credentials)
        self.login_button.pack(pady=20)

    def check_credentials(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()


        correct_username = "admin"  
        correct_password = "password" 

        if username == correct_username and password == correct_password:
            self.destroy()  
            app = LibraryApp() 
            app.mainloop()  
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
