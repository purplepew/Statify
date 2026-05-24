import tkinter as tk
from tkinter import filedialog
import csv
from tkinter import ttk
import statistics
from collections import Counter
import visualization
from config import DEFAULT_GROUPS
import stat_basic

import pyglet
import os

pyglet.font.add_file(os.path.abspath("Safira-March.ttf"))


class Descriptive(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Data Lab")

        # Window size and centering
        window_width = 1000
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#B9B0EB")

        # Grid data model (rows x cols)
        self.entries = []
        self.extract_button = None
        self.total_rows = 5
        self.total_cols = DEFAULT_GROUPS

        # --- Top Navigation ---
        nav_frame = tk.Frame(self, bg="#38476e", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="Statify", font=("Georgia", 10, "bold"), fg="white", bg="#38476e", padx=20).pack(side="left")

        tk.Button(nav_frame, text="Data Lab", bg="#38476e", fg="white",
                  relief="flat", font=("Verdana", 10, "bold")).pack(side="right", padx=15)

        tk.Button(nav_frame, text="Stats Basics", bg="#38476e", fg="white",
                  relief="flat", font=("Verdana", 10, "bold"), command=lambda: stat_basic.StatBasic(self)).pack(side="right", padx=15)

        tk.Button(nav_frame, text="Home", bg="#38476e", fg="white",
                  relief="flat", font=("Verdana", 10, "bold"),
                  command=self.destroy).pack(side="right", padx=15)

        # --- Main Workspace (grid) ---
        self.workspace = tk.Frame(self, bg="#B9B0EB")
        self.workspace.pack(fill="both", expand=True, padx=20, pady=20)

        # Top frame for canvas and vertical scrollbar
        top_frame = tk.Frame(self.workspace, bg="#B9B0EB")
        top_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            top_frame,
            bg="#B9B0EB",
            highlightthickness=0
        )

        self.v_scroll = ttk.Scrollbar(
            top_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.h_scroll = ttk.Scrollbar(
            self.workspace,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.grid_frame = tk.Frame(self.canvas, bg="white")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.grid_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        # Build initial grid
        self.build_grid()

        # Controls (Add Row / Add Column / Extract)
        control_frame = tk.Frame(self, bg="#B9B0EB")
        control_frame.pack(pady=10)

        tk.Button(
            control_frame,
            text="Add Row",
            command=self.add_row,
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            relief="flat",
            padx=10,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            control_frame,
            text="Add Column",
            command=self.add_column,
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            relief="flat",
            padx=10,
            pady=8
        ).pack(side="left", padx=5)

        self.extract_button = tk.Button(
            control_frame,
            text="Extract Data",
            command=self.open_extracted_data_page,
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat",
            state="disabled"
        )
        self.extract_button.pack(side="left", padx=5)

        self.update_extract_button_state()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _is_valid_number(self, value):
        if value == "":
            return True

        try:
            float(value)
            return True
        except ValueError:
            return False

    def _create_numeric_entry(self, parent):
        validate_command = self.register(self._is_valid_number)
        return tk.Entry(
            parent,
            width=18,
            relief="flat",
            highlightbackground="gray80",
            highlightthickness=1,
            justify="center",
            validate="key",
            validatecommand=(validate_command, "%P")
        )

    # ---------------- GRID BUILD ----------------
    def build_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # Headers
        for col in range(self.total_cols):
            tk.Label(
                self.grid_frame,
                text=f"Group {col + 1}",
                bg="#38476e",
                fg="white",
                font=("Verdana", 10, "bold"),
                width=15,
                pady=5
            ).grid(row=0, column=col, padx=1, pady=1, sticky="nsew")

        # Entries
        for row in range(1, self.total_rows + 1):
            row_entries = []
            for col in range(self.total_cols):
                entry = self._create_numeric_entry(self.grid_frame)
                entry.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                entry.bind("<KeyRelease>", self._on_input_change, add="+")
                row_entries.append(entry)
            self.entries.append(row_entries)

    # ---------------- ADD ROW ----------------
    def add_row(self):
        row_entries = []
        row_num = self.total_rows + 1
        for col in range(self.total_cols):
            entry = self._create_numeric_entry(self.grid_frame)
            entry.grid(row=row_num, column=col, padx=1, pady=1, sticky="nsew")
            entry.bind("<KeyRelease>", self._on_input_change, add="+")
            row_entries.append(entry)
        self.entries.append(row_entries)
        self.total_rows += 1
        self.update_extract_button_state()

    # ---------------- ADD COLUMN ----------------
    def add_column(self):
        new_col = self.total_cols
        tk.Label(
            self.grid_frame,
            text=f"Group {new_col + 1}",
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=15,
            pady=5
        ).grid(row=0, column=new_col, padx=1, pady=1, sticky="nsew")

        for row in range(self.total_rows):
            entry = self._create_numeric_entry(self.grid_frame)
            entry.grid(row=row + 1, column=new_col, padx=1, pady=1, sticky="nsew")
            entry.bind("<KeyRelease>", self._on_input_change, add="+")
            self.entries[row].append(entry)

        self.total_cols += 1
        self.update_extract_button_state()

    def _on_input_change(self, event=None):
        self.update_extract_button_state()

    def update_extract_button_state(self):
        has_values = any(
            entry.get().strip()
            for row_entries in self.entries
            for entry in row_entries
        )

        if self.extract_button is not None:
            self.extract_button.config(state="normal" if has_values else "disabled")

    # ---------------- GET DATA (column-wise) ----------------
    def get_all_data(self):
        all_data = []
        for col in range(self.total_cols):
            values = []
            for row in range(self.total_rows):
                values.append(self.entries[row][col].get())
            all_data.append({"group": col + 1, "values": values})
        return all_data

    # ---------------- RESULTS / VISUALIZATION (preserved) ----------------
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
        title_frame = tk.Frame(win, bg="#B9B0EB")
        title_frame.pack(fill="x")

        tk.Label(
            title_frame,
            text="Statistical Analysis",
            font=("Georgia", 28, "bold"),
            fg="white",
            bg="#38476e",
            pady=10
        ).pack(pady=0, fill="x")

        # ---------------- HORIZONTAL SCROLL CONTAINER ----------------
        container = tk.Frame(win, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#B9B0EB", highlightthickness=0)
        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        scroll_frame = tk.Frame(canvas, bg="#B9B0EB")

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
                bg="white", pady=10
            ).pack(anchor="center")

            if stats is None:
                tk.Label(group_frame, text="No valid numeric data", bg="white").pack()
                continue

            # CENTRAL TENDENCY
            tk.Label(group_frame, text="Measure of Central Tendency", bg="white", font=("Georgia", 12, "bold")).pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Mean: {stats['mean']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Median: {stats['median']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Mode: {stats['mode']}", bg="white").pack(anchor="w", padx=20)

            # DISPERSION
            tk.Label(group_frame, text="Measure of Dispersion", bg="white", font=("Georgia", 12, "bold")).pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Range: {stats['range']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Variance: {stats['variance']}", bg="white").pack(anchor="w", padx=20)
            tk.Label(group_frame, text=f"Std Dev: {stats['std_dev']}", bg="white").pack(anchor="w", padx=20)

            # FREQUENCY TABLE
            tk.Label(
                group_frame,
                text="Frequency Table:",
                bg="white",
                font=("Georgia", 12, "bold")
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
        footer_frame = tk.Frame(win, bg="#B9B0EB")
        footer_frame.pack(fill="x")

        button_row = tk.Frame(footer_frame, bg="#B9B0EB")
        button_row.pack(pady=10)

        tk.Button(
            button_row,
            text="Show Visualization",
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=lambda: visualization.VisualizationWindow(self)
        ).pack(side="left", padx=8)

        tk.Button(
            button_row,
            text="BACK",
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=win.destroy
        ).pack(side="left", padx=8)

        tk.Button(
            button_row,
            text="Export CSV",
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=lambda: self.export_results_csv(data)
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#B9B0EB").pack(expand=True)

    def export_results_csv(self, data):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Statistical Results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="descriptive_results.csv"
        )

        if not file_path:
            return

        fieldnames = [
            "Group",
            "Mean",
            "Median",
            "Mode",
            "Range",
            "Variance",
            "Std Dev",
            "Highest Frequency",
            "Frequency Values"
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for group in data:
                stats = self.analyze_group(group["values"])

                if stats is None:
                    writer.writerow({
                        "Group": group["group"],
                        "Mean": "",
                        "Median": "",
                        "Mode": "",
                        "Range": "",
                        "Variance": "",
                        "Std Dev": "",
                        "Highest Frequency": "",
                        "Frequency Values": ""
                    })
                    continue

                freq = stats["frequency"]
                highest_count = max(freq.values()) if freq else ""
                highest_values = [value for value, count in freq.items() if count == highest_count] if freq else []

                writer.writerow({
                    "Group": group["group"],
                    "Mean": stats["mean"],
                    "Median": stats["median"],
                    "Mode": stats["mode"] if stats["mode"] is not None else "None",
                    "Range": stats["range"],
                    "Variance": stats["variance"],
                    "Std Dev": stats["std_dev"],
                    "Highest Frequency": highest_count,
                    "Frequency Values": highest_values
                })

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

        freq = Counter(nums)
        highest_count = max(freq.values())
        mode_values = [value for value, count in freq.items() if count == highest_count]
        result["mode"] = mode_values[0] if len(mode_values) == 1 else None

        # --- Dispersion ---
        result["range"] = max(nums) - min(nums)

        if len(nums) > 1:
            result["variance"] = statistics.variance(nums)
            result["std_dev"] = statistics.stdev(nums)
        else:
            result["variance"] = 0
            result["std_dev"] = 0

        # --- Frequency Table ---
        result["frequency"] = dict(freq)

        return result


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Descriptive(root)
    root.mainloop()
