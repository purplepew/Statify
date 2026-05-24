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
    how_window.resizable(False, False)
    how_window.transient()
    how_window.grab_set()

    container = tk.Frame(how_window, bg="white")
    container.pack(fill="both", expand=True)

    text_frame = tk.Frame(container, bg="white")
    text_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))

    body_text = tk.Text(
        text_frame,
        wrap="word",
        bg="white",
        bd=0,
        highlightthickness=0,
        relief="flat",
        font=("Arial", 11),
        padx=24,
        pady=10,
    )
    body_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=body_text.yview)
    scrollbar.pack(side="right", fill="y")
    body_text.configure(yscrollcommand=scrollbar.set)

    body_text.tag_configure("heading", font=("Arial", 18, "bold"), spacing1=14, spacing3=8)
    body_text.tag_configure("section_heading", font=("Arial", 14, "bold"), spacing1=10, spacing3=6)
    body_text.tag_configure("bold", font=("Arial", 11, "bold"))
    body_text.tag_configure("indent1", lmargin1=22, lmargin2=22, spacing1=0, spacing3=0)
    body_text.tag_configure("indent2", lmargin1=48, lmargin2=48, spacing1=0, spacing3=0)
    body_text.tag_configure("space_after", spacing3=8)

    def insert_line(text, tags=()):
        body_text.insert("end", text + "\n", tags)

    insert_line("HOW IT WORKS", ("heading",))
    insert_line(
        "The Home Page serves as the central dashboard of the Statistics Calculator System. From this page, users can easily navigate to the Stat Basics theory module or the Data Lab calculation workspace. You can also access a quick operational guide by clicking the \u201cHow it Works\u201d button, which opens a pop-up overlay containing instructions for using the system. This layout allows users to access both learning materials and statistical tools directly from the main screen."
    )
    insert_line("")
    insert_line(
        "The Stat Basics page functions as the educational section of the application. Here, users can learn the fundamental concepts behind both Descriptive Statistics and Inferential Statistics. The module explains important statistical concepts and calculations such as mean, median, variance, hypothesis testing, and significance levels. This section helps users build a strong understanding of how statistical methods work before performing calculations in the Data Lab."
    )
    insert_line("")
    insert_line(
        "The Data Lab page is the main workspace of the application where users can perform statistical calculations based on their data. In this section, users can choose between Descriptive Statistics and Inferential Statistics, depending on the type of analysis needed."
    )
    insert_line("")
    insert_line("Descriptive Statistics", ("section_heading",))
    insert_line(
        "If Descriptive Statistics is selected, users will be directed to the descriptive analysis workspace."
    )
    insert_line("")
    insert_line("1. Input your data into the table provided.", ("indent1",))
    insert_line("2. Click \u201cAdd Row\u201d to enter additional data values.", ("indent1",))
    insert_line("3. Click \u201cAdd Column\u201d if you want to analyze multiple groups of data.", ("indent1",))
    insert_line("4. After entering all the data, click \u201cExtract Data.\u201d", ("indent1",))
    insert_line("5. The system will display the results, including:", ("indent1",))
    insert_line("- Measures of Central Tendency", ("indent2",))
    insert_line("- Measures of Dispersion", ("indent2",))
    insert_line("- Percentiles and Quartiles", ("indent2",))
    insert_line("- Frequency Distribution Table", ("indent2",))
    insert_line("6. Click \u201cShow Visualization\u201d to view graphical representations of the data, such as:", ("indent1",))
    insert_line("- Central Tendency Overview", ("indent2",))
    insert_line("- Variability Overview", ("indent2",))
    insert_line("- Frequency Breakdown", ("indent2",))
    insert_line("- Distribution Summary", ("indent2",))
    insert_line("7. To save a copy of the results, click \u201cExport CSV,\u201d enter a file name, and save the file to your device.", ("indent1",))
    insert_line("")
    insert_line("Inferential Statistics", ("section_heading",))
    insert_line(
        "If Inferential Statistics is selected, users will be directed to the inferential analysis workspace."
    )
    insert_line("")
    insert_line("1. Input your data into the table provided.", ("indent1",))
    insert_line("2. Click \u201cAdd Row\u201d to add more data entries.", ("indent1",))
    insert_line("3. Click \u201cAdd Column\u201d to include additional groups of data.", ("indent1",))
    insert_line("4. Enter the desired alpha value (significance level).", ("indent1",))
    insert_line("5. Choose the statistical test you want to perform. The available tests are:", ("indent1",))
    insert_line("- ANOVA: requires at least 3 groups with values.", ("indent2",))
    insert_line("- Correlation: requires 2 groups with values.", ("indent2",))
    insert_line("- Confidence Interval", ("indent2",))
    insert_line("- Chi-Square", ("indent2",))
    insert_line("6. Once a test is selected, the system will automatically display the computed results.", ("indent1",))
    insert_line("7. To save a copy of the output, click \u201cExport CSV,\u201d provide a file name, and save the file to your device.", ("indent1",))

    body_text.configure(state="disabled")

    button_frame = tk.Frame(container, bg="white")
    button_frame.pack(fill="x", padx=20, pady=(0, 16))

    def close_window():
        how_window.destroy()

    back_button = tk.Button(button_frame, text="Back", padx=20, bg="gray80", command=close_window)
    back_button.pack(side="right")

    def on_mousewheel(event):
        body_text.yview_scroll(int(-1 * (event.delta / 120)), "units")

    body_text.bind("<MouseWheel>", on_mousewheel)

    
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
