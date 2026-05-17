import tkinter as tk
import data_labs

class StatBasic(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stats Basics")

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
        nav_frame = tk.Frame(self, bg="#6c0987", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="Statistics Calc",font=("Georgia",10,"bold"),fg="white", bg="#6c0987", padx=20).pack(side="left")

        data_lab_btn = tk.Button(nav_frame, text="Data Lab", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#6c0987", command=lambda: data_labs.DataLabWindow(self))
        data_lab_btn.pack(side="right", padx=15)

        data_lab_btn = tk.Button(nav_frame, text="Stats Basics", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#6c0987")
        data_lab_btn.pack(side="right", padx=15)

        data_lab_btn = tk.Button(nav_frame, text="Home", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#6c0987", command=self.destroy)
        data_lab_btn.pack(side="right", padx=15)

        main_content = tk.Frame(self, bg="#d871f5")
        main_content.pack(expand=True, fill="both")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.mainloop()
