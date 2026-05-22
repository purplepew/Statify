import tkinter as tk
import data_labs
import stat_basic

import pyglet
import os

pyglet.font.add_file(os.path.abspath("Safira-March.ttf"))

def open_how_it_works():
    # Create the secondary window
    how_window = tk.Toplevel()
    how_window.title("How it works")
    
    # Secondary window dimensions and centering logic
    h_width = 1000
    h_height = 600
    sw = how_window.winfo_screenwidth()
    sh = how_window.winfo_screenheight()
    hx = int((sw / 2) - (h_width / 2))
    hy = int((sh / 2) - (h_height / 2))
    how_window.geometry(f"{h_width}x{h_height}+{hx}+{hy}")
    

    # --- Scrollable Content ---
    canvas = tk.Canvas(how_window, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(how_window, orient="vertical", command=canvas.yview)
    
    # Crucial: The scrollable_frame must fill the canvas width to allow centering
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Use 'window=scrollable_frame' with a set width or anchor to help centering
    canvas_frame = canvas.create_window((h_width/2, 0), window=scrollable_frame, anchor="n")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Centered Content ---
    
    # Title - Removed anchor="w"
    tk.Label(scrollable_frame, text="How it works:", font=("Arial", 24, "bold"), bg="white").pack(pady=(20, 10))
    
    body_text = (
        "Three Steps to Statistical Clarity\n\n"
        "Step 1: Input & Data Scrubbing\n"
        "Regardless of the analysis type, everything starts with clean data.\n"
        " • Input: Enter your data manually\n"
        " • Validation: Our system checks for 'dirty data' (text in numeric fields,\n"
        "   extra spaces) and prepares the array for calculation.\n\n"
        "Step 2: Choose Your Path\n"
        "This is where you decide the scope of your research."
    )

    # Body Text - Changed justify to "center" and removed anchor
    tk.Label(
        scrollable_frame, 
        text=body_text, 
        justify="center", 
        bg="white", 
        font=("Arial", 11)
    ).pack(padx=40, pady=10)

    # Home Button - Naturally centered
    tk.Button(scrollable_frame, text="Back", command=how_window.destroy, padx=20,bg="gray80").pack(pady=30)

    
def create_app():
    # --- Create main window ---
    root = tk.Tk()
    root.title("Statify - Statistics Calculator") 

    # Window size
    window_width = 1000
    window_height = 600

    # Get screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Compute center position
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    # Set window position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # --- UI Layout ---
    nav_frame = tk.Frame(root, bg="#38476e", height=60)
    nav_frame.pack(side="top", fill="x")
    nav_frame.pack_propagate(False)

  
    tk.Label(nav_frame, text="Statify",font=("Georgia",10,"bold"),fg="white", bg="#38476e", padx=20).pack(side="left")

    data_lab_btn = tk.Button(nav_frame, text="Data Lab", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#38476e", command=lambda: data_labs.DataLabWindow(root))
    data_lab_btn.pack(side="right", padx=15)

    data_lab_btn = tk.Button(nav_frame, text="Stats Basics", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#38476e", command=lambda: stat_basic.StatBasic(root))
    data_lab_btn.pack(side="right", padx=15)

    data_lab_btn = tk.Button(nav_frame, text="Home", relief="flat",font=("Verdana",10,"bold"), fg="white", bg="#38476e")
    data_lab_btn.pack(side="right", padx=15)

    main_content = tk.Frame(root, bg="#B9B0EB")
    main_content.pack(expand=True, fill="both")

    tk.Label(main_content, bg="#B9B0EB").pack(pady=90,expand=True)
    
    tk.Label(main_content, text="Statify", font=("Safira March Personal Use Only", 65, "bold"), fg="white", bg="#B9B0EB").place(relx=0.5, rely=0.5, anchor="n", y=-140)
    tk.Label(main_content, text="BSCoS 302's Special Project", font=("Times New Roman", 14, "bold", "italic"), fg="white", bg="#B9B0EB").place(relx=0.5, rely=0.5, anchor="n", y=-155)
    tk.Label(main_content, text="Instant insight from raw data", font=("Times New Roman", 14, "italic"), fg="white", bg="#B9B0EB").place(relx=0.5, rely=0.5, anchor="n", y=-30)

    tk.Label(main_content, bg="#B9B0EB").pack(pady=10)
    
    # The Trigger Link
    how_link = tk.Label(main_content, text="How it Works", fg="#38476e", bg="#B9B0EB", cursor="hand2")
    how_link.pack(pady=5)
    how_link.bind("<Button-1>", lambda e: open_how_it_works())

    tk.Button(main_content, text="Get Started",fg = "white",bg = "#38476e",font=("Verdana",10,"bold"), padx=20, pady=10, command=lambda: data_labs.DataLabWindow(root)).pack()
    tk.Label(main_content, bg="#B9B0EB").pack(expand=True)

    root.mainloop()


if __name__ == "__main__":
    create_app()
