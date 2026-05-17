import tkinter as tk
from tkinter import ttk
import statistics

import pyglet
import os

pyglet.font.add_file(os.path.abspath("Safira-March.ttf"))


class Inferential(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Data Lab")

        # ---------------- WINDOW ----------------
        window_width = 1000
        window_height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#d871f5")

        # ---------------- GRID DATA ----------------
        self.entries = []
        self.total_rows = 5
        self.total_cols = 3

        # ---------------- NAVIGATION ----------------
        nav_frame = tk.Frame(self, bg="#6c0987", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Statistics Calc",
            font=("Georgia", 10, "bold"),
            fg="white",
            bg="#6c0987",
            padx=20
        ).pack(side="left")

        tk.Button(
            nav_frame,
            text="Data Lab",
            bg="#6c0987",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold")
        ).pack(side="right", padx=15)

        tk.Button(
            nav_frame,
            text="Stats Basics",
            bg="#6c0987",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold")
        ).pack(side="right", padx=15)

        tk.Button(
            nav_frame,
            text="Home",
            bg="#6c0987",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold"),
            command=self.destroy
        ).pack(side="right", padx=15)

        # ---------------- WORKSPACE ----------------
        self.workspace = tk.Frame(self, bg="#d871f5")
        self.workspace.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(
            self.workspace,
            bg="#d871f5",
            highlightthickness=0
        )

        self.v_scroll = ttk.Scrollbar(
            self.workspace,
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

        # ---------------- BUILD GRID ----------------
        self.build_grid()

        # ---------------- CONTROLS ----------------
        control_frame = tk.Frame(self, bg="#d871f5")
        control_frame.pack(pady=10)

        tk.Button(
            control_frame,
            text="Add Row",
            command=self.add_row,
            bg="#6c0987",
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
            bg="#6c0987",
            fg="white",
            font=("Verdana", 10, "bold"),
            relief="flat",
            padx=10,
            pady=8
        ).pack(side="left", padx=5)

        tk.Label(
            control_frame,
            text="Level of Significance (alpha) in %:",
            bg="#d871f5",
            font=("Georgia", 12)
        ).pack(side="left", padx=10)

        self.significance = tk.Entry(
            control_frame,
            width=10,
            relief="flat",
            highlightbackground="gray80",
            highlightthickness=1
        )

        self.significance.pack(side="left", padx=5)

        tk.Button(
            control_frame,
            text="Extract Data (ANOVA)",
            command=self.anova_analysis,
            fg="white",
            bg="#6c0987",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat"
        ).pack(side="left", padx=5)

        self.parent = parent

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # =========================================================
    # GRID
    # =========================================================

    def build_grid(self):

        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # ---------- HEADERS ----------
        for col in range(self.total_cols):

            tk.Label(
                self.grid_frame,
                text=f"Group {col + 1}",
                bg="#6c0987",
                fg="white",
                font=("Verdana", 10, "bold"),
                width=15,
                pady=5
            ).grid(
                row=0,
                column=col,
                padx=1,
                pady=1,
                sticky="nsew"
            )

        # ---------- ENTRIES ----------
        for row in range(1, self.total_rows + 1):

            row_entries = []

            for col in range(self.total_cols):

                entry = tk.Entry(
                    self.grid_frame,
                    width=18,
                    relief="flat",
                    highlightbackground="gray80",
                    highlightthickness=1,
                    justify="center"
                )

                entry.grid(
                    row=row,
                    column=col,
                    padx=1,
                    pady=1,
                    sticky="nsew"
                )

                row_entries.append(entry)

            self.entries.append(row_entries)

    # =========================================================
    # ADD ROW
    # =========================================================

    def add_row(self):

        row_entries = []

        row_num = self.total_rows + 1

        for col in range(self.total_cols):

            entry = tk.Entry(
                self.grid_frame,
                width=18,
                relief="flat",
                highlightbackground="gray80",
                highlightthickness=1,
                justify="center"
            )

            entry.grid(
                row=row_num,
                column=col,
                padx=1,
                pady=1,
                sticky="nsew"
            )

            row_entries.append(entry)

        self.entries.append(row_entries)

        self.total_rows += 1

    # =========================================================
    # ADD COLUMN
    # =========================================================

    def add_column(self):

        new_col = self.total_cols

        tk.Label(
            self.grid_frame,
            text=f"Group {new_col + 1}",
            bg="#6c0987",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=15,
            pady=5
        ).grid(
            row=0,
            column=new_col,
            padx=1,
            pady=1,
            sticky="nsew"
        )

        for row in range(self.total_rows):

            entry = tk.Entry(
                self.grid_frame,
                width=18,
                relief="flat",
                highlightbackground="gray80",
                highlightthickness=1,
                justify="center"
            )

            entry.grid(
                row=row + 1,
                column=new_col,
                padx=1,
                pady=1,
                sticky="nsew"
            )

            self.entries[row].append(entry)

        self.total_cols += 1

    # =========================================================
    # GET DATA
    # =========================================================

    def get_all_data(self):

        all_data = []

        for col in range(self.total_cols):

            values = []

            for row in range(self.total_rows):
                values.append(self.entries[row][col].get())

            all_data.append({
                "group": col + 1,
                "values": values
            })

        return all_data

    # =========================================================
    # ANOVA
    # =========================================================

    def anova_analysis(self):

        data = self.get_all_data()

        group_means = self.__compute_group_means(data)

        grand_mean = self.__compute_grand_mean(data)

        ss_between = self.__compute_ss_between(
            data,
            group_means,
            grand_mean
        )

        ss_within = self.__compute_ss_within(
            data,
            group_means
        )

        k = len(data)

        N = sum(len(group["values"]) for group in data)

        df_between = k - 1
        df_within = N - k

        MS_between = ss_between / df_between if df_between > 0 else 0
        MS_within = ss_within / df_within if df_within > 0 else 0

        F_value = MS_between / MS_within if MS_within > 0 else 0

        alpha = 0.05

        try:
            alpha = (100 - float(self.significance.get())) / 100
        except:
            pass

        crit_F = self.__f_critical_value(
            df_between,
            df_within,
            alpha
        )

        self.anova_results = {
            "F_value": F_value,
            "crit_F": crit_F,
            "significant": crit_F is not None and F_value > crit_F
        }

        self.open_extracted_anova_data_page()

    # =========================================================
    # COMPUTATIONS
    # =========================================================

    def __compute_group_means(self, data):

        group_means = []

        for group in data:

            nums = []

            for v in group["values"]:

                try:
                    nums.append(float(v))
                except:
                    pass

            mean = statistics.mean(nums) if nums else 0

            group_means.append(mean)

        return group_means

    def __compute_grand_mean(self, data):

        all_nums = []

        for group in data:

            for v in group["values"]:

                try:
                    all_nums.append(float(v))
                except:
                    pass

        return statistics.mean(all_nums) if all_nums else 0

    def __compute_ss_between(
        self,
        data,
        group_means,
        grand_mean
    ):

        ss_between = 0

        for i, group in enumerate(data):

            nums = []

            for v in group["values"]:

                try:
                    nums.append(float(v))
                except:
                    pass

            n = len(nums)

            ss_between += n * (group_means[i] - grand_mean) ** 2

        return ss_between

    def __compute_ss_within(
        self,
        data,
        group_means
    ):

        ss_within = 0

        for i, group in enumerate(data):

            nums = []

            for v in group["values"]:

                try:
                    nums.append(float(v))
                except:
                    pass

            for num in nums:
                ss_within += (num - group_means[i]) ** 2

        return ss_within

    def __f_critical_value(
        self,
        df_between,
        df_within,
        alpha
    ):

        try:
            from scipy.stats import f

            return f.ppf(
                1 - alpha,
                df_between,
                df_within
            )

        except ImportError:
            return None

    # =========================================================
    # RESULT WINDOW
    # =========================================================

    def open_extracted_anova_data_page(self):

        win = tk.Toplevel(self)

        win.title("Inferential Results (ANOVA)")

        win.geometry("700x400")

        win.configure(bg="white")

        tk.Label(
            win,
            text="ANOVA Results",
            font=("Georgia", 24, "bold"),
            bg="#6c0987",
            fg="white",
            pady=15
        ).pack(fill="x")

        results = self.anova_results

        result_frame = tk.Frame(win, bg="white")

        result_frame.pack(expand=True)

        tk.Label(
            result_frame,
            text=f"F Value: {results['F_value']:.2f}",
            bg="white",
            font=("Georgia", 14)
        ).pack(pady=10)

        crit_text = (
            f"{results['crit_F']:.2f}"
            if results['crit_F']
            else "N/A"
        )

        tk.Label(
            result_frame,
            text=f"Critical F: {crit_text}",
            bg="white",
            font=("Georgia", 14)
        ).pack(pady=10)

        decision = (
            "Reject H0"
            if results['significant']
            else "Fail to Reject H0"
        )

        tk.Label(
            result_frame,
            text=f"Decision: {decision}",
            bg="white",
            fg="#6c0987",
            font=("Georgia", 16, "bold")
        ).pack(pady=20)


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    app = Inferential(root)

    root.mainloop()