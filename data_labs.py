import tkinter as tk
from tkinter import ttk
import descriptive
import inferential
import stat_basic

class DataLabWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # --- Create main window ---
        self.title("Statistics Calculator")

        # Window size
        window_width = 1000
        window_height = 600

        # Get screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Compute center position
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        # Set window position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # --- UI Layout ---
        nav_frame = tk.Frame(self, bg="#38476e", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="Statistics Calc",font=("Georgia",10,"bold"),fg="white", bg="#38476e", padx=20).pack(side="left")

        data_lab_btn = tk.Button(nav_frame, text="Data Lab", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#38476e")
        data_lab_btn.pack(side="right", padx=15)

        data_lab_btn = tk.Button(
            nav_frame,
            text="Stats Basics",
            relief="flat",
            font=("Verdana",10,"bold"),
            fg="white",
            bg="#38476e",
            command=self.open_stat_basic
        )
        data_lab_btn.pack(side="right", padx=15)

        data_lab_btn = tk.Button(nav_frame, text="Home", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#38476e", command=self.destroy)
        data_lab_btn.pack(side="right", padx=15)

        main_content = tk.Frame(self, bg="#B9B0EB")
        main_content.pack(expand=True, fill="both")

        tk.Label(main_content, bg="#B9B0EB").pack(expand=True)
        tk.Label(main_content, text="Select Analysis Type", font=("Georgia", 50, "bold"), fg="white", bg="#B9B0EB").pack()
        tk.Label(main_content, bg="#B9B0EB").pack(pady=10)
        tk.Button(main_content, text="Descriptive Statistics",fg = "white",bg = "#38476e",font=("Verdana",10,"bold"), padx=10, pady=10,command=lambda: descriptive.Descriptive(self)).pack()
        tk.Label(main_content, bg="#B9B0EB").pack(pady=1)
        tk.Button(main_content, text="Inferential Statistics",fg = "white",bg = "#38476e",font=("Verdana",10,"bold"), padx=11, pady=10, command=lambda: inferential.Inferential(self)).pack()
        tk.Label(main_content, bg="#B9B0EB").pack(expand=True)

        
    def open_stat_basic(self):
        stat_basic.StatBasic(self.master)
        self.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    root.mainloop()
