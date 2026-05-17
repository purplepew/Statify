import tkinter as tk
from tkinter import ttk
import statistics
from collections import Counter
import visualization


class Descriptive(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Data Lab")

        # Window size and centering
        window_width = 1000
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#d871f5")

        self.groups = []

        # --- Top Navigation ---
        nav_frame = tk.Frame(self, bg="#6c0987", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="Statistics Calc",font=("Georgia",10,"bold"),fg="white", bg="#6c0987", padx=20).pack(side="left")

        tk.Button(nav_frame, text="Data Lab", bg="#6c0987", fg="white",
                  relief="flat", font=("Verdana", 10, "bold")).pack(side="right", padx=15)

        tk.Button(nav_frame, text="Stats Basics", bg="#6c0987", fg="white",
                  relief="flat", font=("Verdana", 10, "bold")).pack(side="right", padx=15)

        tk.Button(nav_frame, text="Home", bg="#6c0987", fg="white",
                  relief="flat", font=("Verdana", 10, "bold"),
                  command=self.destroy).pack(side="right", padx=15)

        # --- Main Workspace ---
        self.workspace = tk.Frame(self, bg="#d871f5")
        self.workspace.pack(fill="both", expand=True, padx=20, pady=20)

        self.h_scroll_container = tk.Frame(self.workspace, bg="#d871f5")
        self.h_scroll_container.pack(side="left", fill="both", expand=True)

        self.group_canvas = tk.Canvas(self.h_scroll_container, bg="#d871f5", highlightthickness=0)

        self.h_scrollbar = ttk.Scrollbar(
            self.h_scroll_container,
            orient="horizontal",
            command=self.group_canvas.xview
        )

        self.groups_container = tk.Frame(self.group_canvas, bg="#d871f5")

        self.group_canvas.create_window((0, 0), window=self.groups_container, anchor="nw")
        self.group_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.group_canvas.pack(side="top", fill="both", expand=True)
        self.h_scrollbar.pack(side="bottom", fill="x")

        self.groups_container.bind(
            "<Configure>",
            lambda e: self.group_canvas.configure(
                scrollregion=self.group_canvas.bbox("all")
            )
        )

        self.setup_bottom_buttons()
        self.add_group()

        #try
        self.result_frame = tk.Frame(self, bg="white")
        self.result_frame.pack(side="right", fill="y")

    def get_all_data(self):
        all_data = []

        for i, group in enumerate(self.groups, start=1):
            values = []

            for entry in group["entries"]:
                val = entry.get()
                values.append(val)

            all_data.append({
                "group": i,
                "values": values
            })

        return all_data


    def add_row_all_groups(self):
        for group in self.groups:
            self.add_row(group["rows_container"], group["entries"])

    # ---------------- GROUP ----------------
    def add_group(self):
        group_idx = len(self.groups) + 1

        group_col = tk.Frame(self.groups_container, bg="#d871f5", padx=10)
        group_col.pack(side="left", anchor="n")

        tk.Label(
            group_col,
            text=f"Group {group_idx}",
            font=("Georgia", 13, "bold"),
            bg="#d871f5",
            fg="white"
        ).pack()

        scroll_container = tk.Frame(group_col, bg="#d871f5")
        scroll_container.pack(pady=5)

        canvas = tk.Canvas(scroll_container, bg="white", width=120, height=300, highlightthickness=0)

        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)

        rows_container = tk.Frame(canvas, bg="white")

        rows_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=rows_container, anchor="nw", width=120)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both")
        scrollbar.pack(side="right", fill="y")

        entries = []

        for _ in range(3):
            self.add_row(rows_container, entries)

        # ADD ROW
        tk.Button(
            group_col,
            text="Add row",
            command=lambda: self.add_row(rows_container, entries),
            bg="#6c0987",
            fg="white",
            font=("Verdana", 9, "bold"),
            relief="flat"
        ).pack(pady=5)

        # ADD GROUP button
        if hasattr(self, 'current_add_group_btn'):
            self.current_add_group_btn.destroy()

        self.current_add_group_btn = tk.Button(
            self.groups_container,
            text="Add group",
            command=self.add_group,
            bg="#6c0987",
            fg="white",
            font=("Verdana", 9, "bold"),
            relief="flat"
        )
        self.current_add_group_btn.pack(side="left", padx=10, pady=150)

        self.groups.append({
            "entries": entries,
            "canvas": canvas,
            "rows_container": rows_container
        })

    # ---------------- ROW ----------------
    def add_row(self, container, entry_list):
        new_entry = tk.Entry(
            container,
            width=15,
            relief="flat",
            highlightbackground="gray80",
            highlightthickness=1
        )
        new_entry.pack(fill="x", pady=1)
        entry_list.append(new_entry)

    def open_extracted_data_page(self):
        win = tk.Toplevel(self)
        win.title("Statistical Results")
        window_width = 1000
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        win.configure(bg="white")
        # ---------------- TITLE ----------------
        title_frame = tk.Frame(win, bg="#d871f5")
        title_frame.pack(fill="x")

        tk.Label(
            title_frame,
            text="Statistical Analysis",
            font=("Georgia", 28, "bold"),
            fg="white",
            bg="#d871f5"
        ).pack(pady=10)
        tk.Label(title_frame, bg="#d871f5").pack(expand=True)
        
        # ---------------- HORIZONTAL SCROLL CONTAINER ----------------
        container = tk.Frame(win, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#d871f5", highlightthickness=0)
        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        scroll_frame = tk.Frame(canvas, bg="#d871f5")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(xscrollcommand=h_scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True)
        h_scrollbar.pack(side="bottom", fill="x")


        data = self.get_all_data()

        # ---------------- GROUP CARDS ----------------
        for group in data:
            stats = self.analyze_group(group["values"])

            # GROUP FRAME (300x600 CARD)
            group_frame = tk.Frame(
                scroll_frame,
                bg="white",
                width=300,
                height=380,
                highlightbackground="gray",
                highlightthickness=1
            )
            group_frame.pack(side="left", padx=5, pady=5)
            group_frame.pack_propagate(False)

            tk.Label(
                group_frame,
                text=f"Group {group['group']}",
                font=("Georgia", 14, "bold"),
                bg="white",pady=10
            ).pack(anchor="center")
            
            if stats is None:
                tk.Label(group_frame, text="No valid numeric data", bg="white").pack()
                continue

            # CENTRAL TENDENCY
            tk.Label(group_frame, text="Measure of Central Tendency", bg="white", font=("Georgia",12,"bold")).pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Mean: {stats['mean']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Median: {stats['median']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Mode: {stats['mode']}", bg="white").pack(anchor="w", padx=20)

            # DISPERSION
            tk.Label(group_frame, text="Measure of Central Tendency", bg="white", font=("Georgia",12,"bold")).pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Range: {stats['range']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Variance: {stats['variance']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Std Dev: {stats['std_dev']}", bg="white").pack(anchor="w", padx=20)

            # FREQUENCY TABLE
            tk.Label(
                group_frame,
                text="Frequency Table:",
                bg="white",
                font=("Georgia",12,"bold")
            ).pack(anchor="w", padx=20, pady=10)

            freq = stats["frequency"]

            highest_count = max(freq.values())

            if highest_count == 1:
                tk.Label(
                    group_frame,
                    text="Frequency: Not Applicable",
                    bg="white"
                ).pack(anchor="w", padx=40)

            else:
                highest_values = []

                for value, count in freq.items():
                    if count == highest_count:
                        highest_values.append(value)

                tk.Label(
                    group_frame,
                    text=f"Highest Frequency: {highest_values} → {highest_count}",
                    bg="white"
                ).pack(anchor="w", padx=40)
        # ---------------- FOOTER ----------------
    
        footer_frame = tk.Frame(win, bg="#d871f5")
        footer_frame.pack(fill="x")
        
        button_row = tk.Frame(footer_frame, bg="#d871f5")
        button_row.pack(pady=10)

        tk.Button(
            button_row,
            text="Show Visualization",
            fg="white",
            bg="#6c0987",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=lambda: visualization.VisualizationWindow(self)
        ).pack(side="left", padx=8)

        tk.Button(
            button_row,
            text="BACK",
            fg="white",
            bg="#6c0987",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=lambda: [self.destroy(), Descriptive(root)]
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#d871f5").pack(expand=True)

      
       
    def analyze_group(self, values):
        # convert to numbers (ignore blanks)
        nums = []
        for v in values:
            try:
                nums.append(float(v))
            except:
                pass

        if len(nums) == 0:
            return None

        result = {}

        # --- Central Tendency ---
        result["mean"] = statistics.mean(nums)
        result["median"] = statistics.median(nums)

        try:
            result["mode"] = statistics.mode(nums)
        except:
            result["mode"] = "No unique mode"

        # --- Dispersion ---
        result["range"] = max(nums) - min(nums)

        if len(nums) > 1:
            result["variance"] = statistics.variance(nums)
            result["std_dev"] = statistics.stdev(nums)
        else:
            result["variance"] = 0
            result["std_dev"] = 0

        # --- Frequency Table ---
        freq = Counter(nums)
        result["frequency"] = dict(freq)

        return result
    
    # ---------------- BOTTOM ----------------
    def setup_bottom_buttons(self):
        btn_frame = tk.Frame(self, bg="#d871f5")
        btn_frame.pack(side="bottom", pady=15)
            

        tk.Button(
            btn_frame,
            text="Add Row (All Groups)",
            command=self.add_row_all_groups,
            fg="#6c0987",
            bg="white",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=10,
            relief="flat"
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="Extract Data",
            command=self.open_extracted_data_page,
            fg="white",
            bg="#6c0987",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=10,
            relief="flat"
        ).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Descriptive(root)
    root.mainloop()
