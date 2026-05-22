import tkinter as tk
import data_labs
from PIL import ImageTk, Image
import os

class StatBasic(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stats Basics")
        self.img_files = []
        self.img_cache = {}
        self.current_img_index = 0
        self.back_btn = None
        self.next_btn = None
        
        self.img_display_width = 1000
        self.img_display_height = 480
        self.img_dir = "images"

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

        data_lab_btn = tk.Button(nav_frame, text="Home", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#6c0987", command=self.on_home)
        data_lab_btn.pack(side="right", padx=15)

        main_content = tk.Frame(self, bg="#d871f5")
        main_content.pack(expand=True, fill="both")
        self.main_content = main_content
        if os.path.isdir(self.img_dir):
            # Get sorted list of image files (without loading them yet)
            self.img_files = sorted([f for f in os.listdir(self.img_dir) if f.endswith(".png")],
                                    key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)

        if self.img_files:
            self.my_label = tk.Label(main_content, bg="#d871f5")
            self.my_label.pack(fill="both", expand=True)

            # Button frame
            button_frame = tk.Frame(main_content, bg="#d871f5", height=60)
            button_frame.pack(side="bottom", fill="x")
            button_frame.pack_propagate(False)

            self.back_btn = tk.Button(button_frame, text="Back", font=("Verdana", 10, "bold"), fg="white", bg="#6c0987", padx=20, pady=10, command=self.show_previous_image)
            self.back_btn.pack(side="left", padx=30, pady=10)

            self.next_btn = tk.Button(button_frame, text="Next", font=("Verdana", 10, "bold"), fg="white", bg="#6c0987", padx=20, pady=10, command=self.show_next_image)
            self.next_btn.pack(side="right", padx=30, pady=10)

            # Load and display the first image
            self.load_and_display_image(0)
            self.update_button_states()

            self.protocol("WM_DELETE_WINDOW", self.on_closing)
        else:
            tk.Label(
                main_content,
                text="Stats Basics content is not available in this version.",
                font=("Safira March", 24, "bold"),
                fg="white",
                bg="#d871f5"
            ).pack(expand=True)

            tk.Label(
                main_content,
                text="No images folder was found for the old project layout.",
                font=("Verdana", 11),
                fg="white",
                bg="#d871f5"
            ).pack(pady=(0, 20))

            tk.Button(
                main_content,
                text="Back",
                font=("Verdana", 10, "bold"),
                fg="white",
                bg="#6c0987",
                padx=20,
                pady=10,
                command=self.on_home
            ).pack(pady=(0, 30))

    def on_home(self):
        self.master.deiconify()
        self.destroy()

    def load_and_display_image(self, index):
        if index not in self.img_cache and 0 <= index < len(self.img_files):
            file_path = os.path.join(self.img_dir, self.img_files[index])
            img = Image.open(file_path)
            img.thumbnail((self.img_display_width, self.img_display_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.img_cache[index] = img_tk
        
        if index in self.img_cache:
            self.my_label.config(image=self.img_cache[index])
    
    def update_button_states(self):
        if self.back_btn and self.next_btn:
            self.back_btn.config(state="disabled" if self.current_img_index == 0 else "normal")
            self.next_btn.config(state="disabled" if self.current_img_index == len(self.img_files) - 1 else "normal")
    
    def show_next_image(self):
        if self.img_files and self.current_img_index < len(self.img_files) - 1:
            self.current_img_index += 1
            self.load_and_display_image(self.current_img_index)
            self.update_button_states()
    
    def show_previous_image(self):
        if self.img_files and self.current_img_index > 0:
            self.current_img_index -= 1
            self.load_and_display_image(self.current_img_index)
            self.update_button_states()
    
    def on_closing(self):
        self.img_cache.clear()
        self.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.mainloop()
