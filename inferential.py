import tkinter as tk
from tkinter import ttk
import statistics
import stat_basic
import visualization

import pyglet
import os
import scipy.stats
from config import DEFAULT_GROUPS

pyglet.font.add_file(os.path.abspath("Safira-March.ttf"))


class Inferential(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Data Lab")

        # ---------------- WINDOW ----------------
        window_width = 1000
        window_height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.configure(bg="#B9B0EB")

        # ---------------- GRID DATA ----------------
        self.entries = []
        self.extract_buttons = []
        self.total_rows = 5
        self.total_cols = DEFAULT_GROUPS

        # ---------------- NAVIGATION ----------------
        nav_frame = tk.Frame(self, bg="#38476e", height=60)
        nav_frame.pack(side="top", fill="x")
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Statify",
            font=("Safira March Personal Use Only", 10, "bold"),
            fg="white",
            bg="#38476e",
            padx=20
        ).pack(side="left")

        tk.Button(
            nav_frame,
            text="Data Lab",
            bg="#38476e",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold")
        ).pack(side="right", padx=15)

        tk.Button(
            nav_frame,
            text="Stats Basics",
            bg="#38476e",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold"),
            command=lambda: stat_basic.StatBasic(self)
        ).pack(side="right", padx=15)

        tk.Button(
            nav_frame,
            text="Home",
            bg="#38476e",
            fg="white",
            relief="flat",
            font=("Verdana", 10, "bold"),
            command=self.destroy
        ).pack(side="right", padx=15)

        # ---------------- WORKSPACE ----------------
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

        # ---------------- BUILD GRID ----------------
        self.build_grid()

        # ---------------- CONTROLS ----------------
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

        tk.Label(
            control_frame,
            text="Alpha:",
            bg="#B9B0EB",
            font=("Georgia", 12)
        ).pack(side="left", padx=10)

        self.significance = self._create_numeric_entry(control_frame, width=10)

        self.significance.pack(side="left", padx=5)
        self.significance.bind("<KeyRelease>", self._on_input_change, add="+")

        self.significance.insert(0, "0.05")  # Default to 0.05

        # Container for all extract buttons located below control_frame
        button_frame = tk.Frame(self, bg="#B9B0EB")
        button_frame.pack(pady=10)

        self.anova_button = tk.Button(
            button_frame,
            text="Extract Data (ANOVA)",
            command=self.anova_analysis,
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat",
            state="disabled"
        )
        self.anova_button.pack(side="left", padx=5)
        self.extract_buttons.append(self.anova_button)

        self.correlation_button = tk.Button(
            button_frame,
            text="Extract Data (Correlation)",
            command=self.correlation_analysis,
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat",
            state="disabled"
        )
        self.correlation_button.pack(side="left", padx=5)
        self.extract_buttons.append(self.correlation_button)

        self.confidence_button = tk.Button(
            button_frame,
            text="Extract Data (Confidence)",
            command=self.confidence_analysis,
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat",
            state="disabled"
        )
        self.confidence_button.pack(side="left", padx=5)
        self.extract_buttons.append(self.confidence_button)

        self.chisquare_button = tk.Button(
            button_frame,
            text="Extract Data (Chi-Square)",
            command=self.chisquare_analysis,
            fg="white",
            bg="#38476e",
            font=("Verdana", 10, "bold"),
            padx=10,
            pady=8,
            relief="flat",
            state="disabled"
        )
        self.chisquare_button.pack(side="left", padx=5)
        self.extract_buttons.append(self.chisquare_button)

        self.update_extract_button_state()

        self.parent = parent

        def on_close():
            root.destroy()

        self.protocol("WM_DELETE_WINDOW", on_close)

    def _is_valid_number(self, value):
        if value == "":
            return True

        try:
            float(value)
            return True
        except ValueError:
            return False

    def _create_numeric_entry(self, parent, width=18):
        validate_command = self.register(self._is_valid_number)
        return tk.Entry(
            parent,
            width=width,
            relief="flat",
            highlightbackground="gray80",
            highlightthickness=1,
            justify="center",
            validate="key",
            validatecommand=(validate_command, "%P")
        )

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
                bg="#38476e",
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

                entry = self._create_numeric_entry(self.grid_frame)

                entry.grid(
                    row=row,
                    column=col,
                    padx=1,
                    pady=1,
                    sticky="nsew"
                )

                entry.bind("<KeyRelease>", self._on_input_change, add="+")

                row_entries.append(entry)

            self.entries.append(row_entries)

    # =========================================================
    # ADD ROW
    # =========================================================

    def add_row(self):

        row_entries = []

        row_num = self.total_rows + 1

        for col in range(self.total_cols):

            entry = self._create_numeric_entry(self.grid_frame)

            entry.grid(
                row=row_num,
                column=col,
                padx=1,
                pady=1,
                sticky="nsew"
            )

            entry.bind("<KeyRelease>", self._on_input_change, add="+")

            row_entries.append(entry)

        self.entries.append(row_entries)

        self.total_rows += 1
        self.update_extract_button_state()

    # =========================================================
    # ADD COLUMN
    # =========================================================

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
        ).grid(
            row=0,
            column=new_col,
            padx=1,
            pady=1,
            sticky="nsew"
        )

        for row in range(self.total_rows):

            entry = self._create_numeric_entry(self.grid_frame)

            entry.grid(
                row=row + 1,
                column=new_col,
                padx=1,
                pady=1,
                sticky="nsew"
            )

            entry.bind("<KeyRelease>", self._on_input_change, add="+")

            self.entries[row].append(entry)

        self.total_cols += 1
        self.update_extract_button_state()

    def _on_input_change(self, event=None):
        self.update_extract_button_state()

    def update_extract_button_state(self):
        # Check if any entry across the grid contains a value
        has_group_values = any(
            entry.get().strip()
            for row_entries in self.entries
            for entry in row_entries
        )

        # Count how many groups (columns) have at least one non-empty value
        groups_with_values = 0
        for col in range(self.total_cols):
            col_has_value = any(self.entries[row][col].get().strip() for row in range(self.total_rows))
            if col_has_value:
                groups_with_values += 1

        has_significance = bool(self.significance.get().strip())

        # General enable: any data present and significance provided
        should_enable_general = has_group_values and has_significance

        # Correlation requires at least two groups with values
        should_enable_correlation = groups_with_values >= 2 and has_significance

        for button in self.extract_buttons:
            if button is self.correlation_button:
                button.config(state="normal" if should_enable_correlation else "disabled")
            else:
                button.config(state="normal" if should_enable_general else "disabled")

    # =========================================================
    # GET DATA
    # =========================================================

    def get_all_data(self):
        '''return [{"group":1, "values":['70', '75', '80']},
                {"group":2, "values":['85', '88', '90']},
                {"group":3, "values":['60', '65', '70']}]''' # Preset for ANOVA
        
        '''return [{"group":1, "values":['1', '2', '3', '4', '5']},
                {"group":2, "values":['50', '55', '65', '70', '80']}]''' # Preset for Pearson Correlation
        
        '''return [{"group":1, "values":['200', '220', '240', '260', '280']},
                {"group":2, "values":['300', '350', '400', '450', '500']},
                {"group":3, "values":['100', '130', '170', '220', '230']}]''' # Preset for Confidence Intervals
        
        '''return [{"group":1, "values":['30', '40', '20']},
                {"group":2, "values":['50', '30', '10']},
                {"group":3, "values":['20', '10', '10']}]''' # Preset for Chi-Square Test

        all_data = []

        for col in range(self.total_cols):

            values = []

            for row in range(self.total_rows):
                if self.entries[row][col].get() != "":
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
        print(data)

        # ANOVA F Test calculations
        group_means = self.__compute_group_means(data)
        grand_mean = self.__compute_grand_mean(data)
        ss_between = self.__compute_ss_between(data, group_means, grand_mean)
        ss_within = self.__compute_ss_within(data, group_means)

        # Groups and Observations, including degrees of freedom
        k = len(data)
        N = sum(len(group["values"]) for group in data)
        df_between = k - 1
        df_within = N - k

        MS_between = ss_between / df_between if df_between > 0 else 0
        MS_within = ss_within / df_within if df_within > 0 else 0

        F_value = MS_between / MS_within if MS_within > 0 else 0

        # Get alpha or Level of Significance taken from User Input, default to 0.05 if invalid
        alpha = 0.05
        try:
            alpha = float(self.significance.get())
        except:
            pass

        crit_F = self.__f_critical_value(df_between, df_within, alpha)

        q_value = self.__q_value(k, df_within, alpha)
        HSD = q_value * (MS_within/k) ** 0.5 if q_value is not None and MS_within > 0 else None

        compare_group = self.__compare_groups(data, group_means, HSD)

        self.anova_results = {
            "data": data,
            "group_means": group_means,
            "grand_mean": grand_mean,
            "ss_between": ss_between,
            "ss_within": ss_within,
            "df_between": df_between,
            "df_within": df_within,
            "MS_between": MS_between,
            "MS_within": MS_within,
            "F_value": F_value,
            "crit_F": crit_F,
            "alpha": alpha,
            "q_value": q_value,
            "HSD": HSD,
            "compare_group": compare_group,
            "significant": crit_F is not None and F_value > crit_F,
        }

        self.open_extracted_anova_data_page()

    # =========================================================
    # CORRELATION (PEARSON)
    # =========================================================

    def correlation_analysis(self):
        data = self.get_all_data()

        x_values = list(map(float, data[0]["values"]))
        y_values = list(map(float, data[1]["values"]))
        xsquared = list(map(lambda x: x**2, x_values))
        ysquared = list(map(lambda y: y**2, y_values))
        xy = list(map(lambda x, y: x * y, x_values, y_values))

        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xsquared = sum(xsquared)
        sum_ysquared = sum(ysquared)
        sum_xy = sum(xy)
        n = len(x_values)

        r_numerator = n * sum_xy - (sum_x * sum_y)
        r_denominator = ((n * sum_xsquared - (sum_x ** 2)) * (n * sum_ysquared - (sum_y ** 2))) ** 0.5
        r = r_numerator / r_denominator if r_denominator != 0 else 0

        t_value = (r * (n - 2) ** 0.5) / ((1 - r ** 2) ** 0.5) if n > 2 and r ** 2 != 1 else 0

        # Get alpha or Level of Significance taken from User Input, default to 0.05 if invalid
        alpha = 0.05
        try:
            alpha = float(self.significance.get())
        except:
            pass

        t_crit = self.__t_critical_value(n - 2, alpha)

        p_value = self.__p_value_from_t(t_value, n - 2)

        self.correlation_result = {
            "data": data,
            "x_values": x_values,
            "y_values": y_values,
            "xsquared": xsquared,
            "ysquared": ysquared,
            "xy": xy,
            "sum_x": sum_x,
            "sum_y": sum_y,
            "sum_xsquared": sum_xsquared,
            "sum_ysquared": sum_ysquared,
            "sum_xy": sum_xy,
            "r": r,
            "t_value": t_value,
            "t_crit": t_crit,
            "p_value": p_value
        }
        self.open_extracted_correlation_data_page()

    # =========================================================
    # CONFIDENCE INTERVALS
    # =========================================================

    def confidence_analysis(self):
        data = self.get_all_data()

        alpha = 0.05
        try:
            alpha = float(self.significance.get())
        except:
            pass
        
        confidence_level = alpha

        sample_means = []
        std_devs = []
        group_dfs = []
        for group in data:
            nums = []
            for v in group["values"]:
                try:
                    nums.append(float(v))
                except:
                    pass
            if len(nums) > 1:
                std_devs.append(statistics.stdev(nums))
            else:
                std_devs.append(0)

            if len(nums) > 0:
                sample_means.append(statistics.mean(nums))
            else:
                sample_means.append(0)

            group_dfs.append(len(nums) - 1)

        t_scores = []
        for df in group_dfs:
            t_score = self.__t_critical_value(df, confidence_level)
            t_scores.append(t_score)

        t_distributions = []
        t_ranges = []
        for i, group in enumerate(data):
            nums = []
            for v in group["values"]:
                try:
                    nums.append(float(v))
                except:
                    pass
            std_over_sqrt = std_devs[i] / (len(nums) ** 0.5) if len(nums) > 0 else 0
            t_dist = t_scores[i] * std_over_sqrt

            t_lower = sample_means[i] - t_dist
            t_higher = sample_means[i] + t_dist
            t_distributions.append(t_dist)
            t_ranges.append((t_lower, t_higher))

        self.confidence_results = {
            "sample_means": sample_means,
            "std_devs": std_devs,
            "group_dfs": group_dfs,
            "t_scores": t_scores,
            "t_distributions": t_distributions,
            "t_ranges": t_ranges
        }

        self.open_extracted_confidence_data_page()

    # =========================================================
    # CHI SQUARE TEST
    # =========================================================

    def chisquare_analysis(self):
        data = self.get_all_data()

        alpha = 0.05
        try:
            alpha = float(self.significance.get())
        except:
            pass

        group_totals = []
        for group in data:
            nums = []
            for v in group["values"]:
                try:
                    nums.append(float(v))
                except:
                    pass
            group_totals.append(sum(nums))

        row_totals = []
        for i in range(len(data[0]["values"])):
            row_sum = 0
            for group in data:
                try:
                    row_sum += float(group["values"][i])
                except:
                    pass
            row_totals.append(row_sum)

        grand_total = sum(group_totals)

        square_list = []
        for group_index in range(len(group_totals)):
            for row_index in range(len(row_totals)):
                expected = (group_totals[group_index] * row_totals[row_index]) / grand_total if grand_total > 0 else 0
                observed = data[group_index]["values"][row_index] if row_index < len(data[group_index]["values"]) else 0
                try:
                    observed = float(data[group_index]["values"][row_index])
                except:
                    pass

                chisquare_component = ((observed - expected) ** 2) / expected if expected > 0 else 0
                square_list.append(chisquare_component)

                print(f"Group {group_index + 1}, Row {row_index + 1}: Observed={observed}, Expected={expected:.2f}, Component={chisquare_component:.4f}")

        print(square_list)
        chisquare_statistic = sum(square_list)

        df = (len(group_totals) - 1) * (len(row_totals) - 1)
        critical_chisquare = scipy.stats.chi2.ppf(1 - alpha, df) if df > 0 else 0
        p_value = self.__p_value_from_chisquare(df, alpha)

        significant = critical_chisquare is not None and chisquare_statistic > critical_chisquare

        self.chisquare_results = {
            "chisquare_statistic": chisquare_statistic,
            "df": df,
            "critical_chisquare": critical_chisquare,
            "p_value": p_value,
            "significant": significant
        }

        self.open_extracted_chisquare_data_page()

    # =========================================================
    # COMPUTATIONS
    # =========================================================

    def __compute_group_means(self, data):
        # Compute mean for each group
        group_means = []
        for group in data:
            nums = []
            for v in group["values"]:
                try:
                    nums.append(float(v))
                except:
                    pass
            if len(nums) > 0:
                mean = statistics.mean(nums)
            else:
                mean = 0
            group_means.append(mean)
        return group_means
    
    def __compute_grand_mean(self, data):
        # Compute mean of all values across all groups
        all_nums = []
        for group in data:
            for v in group["values"]:
                try:
                    all_nums.append(float(v))
                except:
                    pass
        if len(all_nums) > 0:
            grand_mean = statistics.mean(all_nums)
        else:
            grand_mean = 0
        return grand_mean
    
    def __compute_ss_between(self, data, group_means, grand_mean):
        # Compute summation of squares between groups
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
    
    def __compute_ss_within(self, data, group_means):
        # Compute summation of squares within groups
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
    
    def __f_critical_value(self, df_between, df_within, alpha):
        # Return the critical F value for given degrees of freedom and alpha.
        try:
            return scipy.stats.f.ppf(1 - alpha, df_between, df_within)
        except ImportError:
            f_table = {
                (1, 10): {0.05: 4.9646, 0.01: 10.042},
                (2, 10): {0.05: 3.2253, 0.01: 5.7246},
                (3, 10): {0.05: 2.9787, 0.01: 5.0257},
                (1, 20): {0.05: 4.3515, 0.01: 7.4333},
                (2, 20): {0.05: 3.0863, 0.01: 4.8508},
                (3, 20): {0.05: 2.8669, 0.01: 4.3989},
            }
            return f_table.get((df_between, df_within), {}).get(alpha, None)
        
    def __q_value(self, k, df_within, alpha):
        try:
            return scipy.stats.studentized_range.ppf(1 - alpha, k, df_within)
        except ImportError:
            q_table = {
                (3, 10): {0.05: 3.77, 0.01: 5.34},
                (4, 10): {0.05: 4.34, 0.01: 6.16},
                (5, 10): {0.05: 4.94, 0.01: 7.01},
                (3, 20): {0.05: 3.46, 0.01: 4.96},
                (4, 20): {0.05: 3.96, 0.01: 5.68},
                (5, 20): {0.05: 4.53, 0.01: 6.46},
            }
            return q_table.get((k, df_within), {}).get(alpha, None)
        
    def __compare_groups(self, data, group_means, HSD):
        comparisons = []
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                mean_diff = abs(group_means[i] - group_means[j])
                significant = HSD is not None and mean_diff > HSD
                comparisons.append({
                    "group1": data[i]["group"],
                    "group2": data[j]["group"],
                    "mean_diff": mean_diff,
                    "significant": significant
                })
        return comparisons
    
    def __t_critical_value(self, df, alpha):
        try:
            return scipy.stats.t.ppf(1 - alpha/2, df)
        except ImportError:
            t_table = {
                1: {0.05: 12.706, 0.01: 63.657},
                2: {0.05: 4.303, 0.01: 9.925},
                3: {0.05: 3.182, 0.01: 5.841},
                4: {0.05: 2.776, 0.01: 4.604},
                5: {0.05: 2.571, 0.01: 4.032},
                10: {0.05: 2.228, 0.01: 3.169},
                20: {0.05: 2.086, 0.01: 2.845},
                30: {0.05: 2.042, 0.01: 2.750},
            }
            return t_table.get(df, {}).get(alpha, None)
        
    def __p_value_from_t(self, t_value, df):
        try:
            p_value = (1 - scipy.stats.t.cdf(abs(t_value), df)) * 2
            return p_value
        except ImportError:
            return None
        
    def __p_value_from_chisquare(self, df, alpha):
        try:
            p_value = 1 - scipy.stats.chi2.cdf(df, alpha)
            return p_value
        except ImportError:
            return None

    # =========================================================
    # RESULT WINDOW
    # =========================================================

    def open_extracted_anova_data_page(self):
        win = tk.Toplevel(self)
        win.title("Inferential Results (ANOVA)")
        win.geometry("700x500")
        win.configure(bg="#B9B0EB")

        tk.Label(
            win,
            text="ANOVA Results",
            font=("Safira March Personal Use Only", 24, "bold"),
            bg="#38476e",
            fg="white",
            pady=15
        ).pack(fill="x")

        results = self.anova_results

        result_frame = tk.Frame(win, bg="#B9B0EB")

        result_frame.pack(expand=True)

        tk.Label(
            result_frame,
            text=f"F Value: {results['F_value']:.2f}",
            bg="#B9B0EB",
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
            bg="#B9B0EB",
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
            bg="#B9B0EB",
            fg="#38476e",
            font=("Georgia", 16, "bold")
        ).pack(pady=10)

        result_frame2 = tk.Frame(win, bg="#B9B0EB")
        result_frame2.pack(fill="x", expand=True)

        tk.Label(
            result_frame2,
            text="Tukey Pairwise Comparisons",
            font=("Safira March Personal Use Only", 24, "bold"),
            bg="#38476e",
            fg="white",
            pady=15
        ).pack(fill="x")
        
        comparison_frame_inner = tk.Frame(result_frame2, bg="#B9B0EB")
        comparison_frame_inner.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tk.Label(comparison_frame_inner, text=f"HSD threshold: {results['HSD']:.2f}", bg="#B9B0EB", font=("Georgia", 12, "italic")).pack(anchor="w", pady=(8, 4))
        tk.Label(comparison_frame_inner, text="Mean difference vs HSD", bg="#B9B0EB", font=("Georgia", 12, "bold")).pack(anchor="w", pady=(8, 4))

        if results['compare_group']:
            for comp in results['compare_group']:
                sign_text = "Significant" if comp['significant'] else "Not Significant"
                text_color = "#38476e" if comp['significant'] else "black"
                tk.Label(
                    comparison_frame_inner,
                    text=f"Group {comp['group1']} vs Group {comp['group2']}: Δ={comp['mean_diff']:.2f}, HSD={results['HSD']:.2f} → {sign_text}",
                    bg="#B9B0EB",
                    fg=text_color,
                    wraplength=380,
                    justify="left"
                ).pack(anchor="w", pady=2)
        else:
            tk.Label(comparison_frame_inner, text="No pairwise comparisons available.", bg="#B9B0EB").pack(anchor="w", pady=4)
        
        # ---------------- FOOTER ----------------
        footer_frame = tk.Frame(win, bg="#B9B0EB")
        footer_frame.pack(fill="x")

        button_row = tk.Frame(footer_frame, bg="#B9B0EB")
        button_row.pack(pady=10)

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
            command=lambda: self.export_results_csv(results, "anova_results.csv")
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#B9B0EB").pack(expand=True)

    def open_extracted_correlation_data_page(self):
        win = tk.Toplevel(self)
        win.title("Inferential Results (Correlation)")
        win.geometry("700x650")
        win.configure(bg="#B9B0EB")

        tk.Label(
            win,
            text="Correlation Results",
            font=("Safira March Personal Use Only", 24, "bold"),
            bg="#38476e",
            fg="white",
            pady=8
        ).pack(fill="x", pady=(0, 10))

        results = self.correlation_result

        result_frame = tk.Frame(win, bg="#B9B0EB")

        result_frame.pack(fill="x", expand=False, pady=5)

        # Table of values including summations and correlation coefficient
        table_frame = tk.Frame(result_frame, bg="#B9B0EB")
        table_frame.pack(pady=(0, 10))
        headers = ["X", "Y", "X²", "Y²", "XY"]
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, bg="#38476e", fg="white", font=("Verdana", 10, "bold"), width=12).grid(row=0, column=col, padx=1, pady=1)        
        for i in range(len(results['x_values'])):
            tk.Label(table_frame, text=f"{results['x_values'][i]:.2f}", bg="white", font=("Georgia", 12), width=12).grid(row=i+1, column=0, padx=1, pady=1)
            tk.Label(table_frame, text=f"{results['y_values'][i]:.2f}", bg="white", font=("Georgia", 12), width=12).grid(row=i+1, column=1, padx=1, pady=1)
            tk.Label(table_frame, text=f"{results['xsquared'][i]:.2f}", bg="white", font=("Georgia", 12), width=12).grid(row=i+1, column=2, padx=1, pady=1)
            tk.Label(table_frame, text=f"{results['ysquared'][i]:.2f}", bg="white", font=("Georgia", 12), width=12).grid(row=i+1, column=3, padx=1, pady=1)
            tk.Label(table_frame, text=f"{results['xy'][i]:.2f}", bg="white", font=("Georgia", 12), width=12).grid(row=i+1, column=4, padx=1, pady=1)

        tk.Label(table_frame, text="─" * 50, bg="#B9B0EB").grid(row=len(results['x_values']) + 1, column=0, columnspan=5, pady=(4, 4))
        tk.Label(table_frame, text=f"ΣX: {results['sum_x']:.2f}", bg="white", font=("Georgia", 10, "bold"), width=12).grid(row=len(results['x_values']) + 2, column=0, padx=1, pady=1)
        tk.Label(table_frame, text=f"ΣY: {results['sum_y']:.2f}", bg="white", font=("Georgia", 10, "bold"), width=12).grid(row=len(results['x_values']) + 2, column=1, padx=1, pady=1)
        tk.Label(table_frame, text=f"ΣX²: {results['sum_xsquared']:.2f}", bg="white", font=("Georgia", 10, "bold"), width=12).grid(row=len(results['x_values']) + 2, column=2, padx=1, pady=1)
        tk.Label(table_frame, text=f"ΣY²: {results['sum_ysquared']:.2f}", bg="white", font=("Georgia", 10, "bold"), width=12).grid(row=len(results['x_values']) + 2, column=3, padx=1, pady=1)
        tk.Label(table_frame, text=f"ΣXY: {results['sum_xy']:.2f}", bg="white", font=("Georgia", 10, "bold"), width=12).grid(row=len(results['x_values']) + 2, column=4, padx=1, pady=1)

        tk.Label(
            result_frame,
            text=f"Correlation Coefficient: {results['r']:.2f}",
            bg="#B9B0EB",
            font=("Georgia", 14)
        ).pack(pady=10)

        interpretation = "None" # Default interpretation
        if results['r'] < 0:
            if results['r'] > -0.3:
                interpretation = "Weak Negative Correlation"
            elif results['r'] > -0.5:
                interpretation = "Low Negative Correlation"
            elif results['r'] > -0.7:
                interpretation = "Moderate Negative Correlation"
            elif results['r'] > -0.9:
                interpretation = "High Negative Correlation"
            else:
                interpretation = "Very High Negative Correlation"
        else:
            if results['r'] < 0.3:
                interpretation = "Weak Positive Correlation"
            elif results['r'] < 0.5:
                interpretation = "Low Positive Correlation"
            elif results['r'] < 0.7:
                interpretation = "Moderate Positive Correlation"
            elif results['r'] < 0.9:
                interpretation = "High Positive Correlation"
            else:
                interpretation = "Very High Positive Correlation"

        tk.Label(
            result_frame,
            text=f"Interpretation: {interpretation}",
            bg="#B9B0EB",
            fg="#38476e",
            font=("Georgia", 16, "bold")
        ).pack(pady=10)

        # Compare t-value with critical t-value to determine significance
        significance_text = "Reject H₀" if abs(results['t_value']) > results['t_crit'] else "Fail to Reject H₀"
        tk.Label(
            result_frame,
            text=f"t-value: {results['t_value']:.2f} | Critical t-value: {results['t_crit']:.2f} → {significance_text}",
            bg="#B9B0EB",
            font=("Georgia", 12, "italic")
        ).pack(pady=(5,0))

        # Compare p-value with alpha to determine significance
        alpha = float(self.significance.get())
        p_significance_text = "Reject H₀" if results['p_value'] < alpha else "Fail to Reject H₀"
        tk.Label(
            result_frame,
            text=f"p-value: {results['p_value']:.4f} | α: {float(alpha)} → {p_significance_text}",
            bg="#B9B0EB",
            font=("Georgia", 12, "italic")
        ).pack(pady=(0,5))

        # Button at footer to display the scatter plot of the data points

        tk.Button(
            result_frame,
            text="Show Scatter Plot",
            command=lambda: visualization.VisualizationScatterPlotExclusive(self),
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            padx=12,
            pady=8,
            relief="flat"
        ).pack(pady=(20, 0))

        # ---------------- FOOTER ----------------
        footer_frame = tk.Frame(win, bg="#B9B0EB")
        footer_frame.pack(fill="x")

        button_row = tk.Frame(footer_frame, bg="#B9B0EB")
        button_row.pack(pady=10)

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
            command=lambda: self.export_results_csv(results, "correlation_results.csv")
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#B9B0EB").pack(expand=True)

    def open_extracted_confidence_data_page(self):
        win = tk.Toplevel(self)
        win.title("Confidence Interval Results")
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
            text="Confidence Interval Analysis",
            font=("Safira March Personal Use Only", 28, "bold"),
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

        data = self.confidence_results

        # ---------------- GROUP CARDS ----------------
        for i in range(len(data["sample_means"])):

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
                text=f"Group {i + 1}",
                font=("Georgia", 18, "bold"),
                bg="white", pady=10
            ).pack(anchor="center")

            tk.Label(
                group_frame,
                text=f"Sample Size: {data['group_dfs'][i] + 1}",
                bg="white",
                font=("Georgia", 12)
            ).pack(anchor="w", padx=10)

            tk.Label(
                group_frame,
                text=f"Sample Mean: {data['sample_means'][i]:.2f}",
                bg="white",
                font=("Georgia", 12)
            ).pack(anchor="w", padx=10)

            tk.Label(
                group_frame,
                text=f"STDEV/Standard Error: {data['std_devs'][i]:.2f}",
                bg="white",
                font=("Georgia", 12)
            ).pack(anchor="w", padx=10)

            tk.Label(
                group_frame,
                text=f"T-Score: {data['t_scores'][i]:.2f}",
                bg="white",
                font=("Georgia", 12)
            ).pack(anchor="w", padx=10)

            # CONFIDENCE INTERVAL AND RANGES
            tk.Label(
                group_frame,
                text=f"Margin of Error: {data['t_distributions'][i]:.2f}",
                bg="white",
                font=("Georgia", 12)
            ).pack(anchor="w", padx=10)

            tk.Label(
                group_frame,
                text=f"{data['t_ranges'][i][0]:.2f} - {data['t_ranges'][i][1]:.2f}",
                bg="white",
                fg="#38476e",
                font=("Georgia", 16, "bold")
            ).pack(anchor="w", padx=10)

        # ---------------- FOOTER ----------------
        footer_frame = tk.Frame(win, bg="#B9B0EB")
        footer_frame.pack(fill="x")

        button_row = tk.Frame(footer_frame, bg="#B9B0EB")
        button_row.pack(pady=10)

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
            command=lambda: self.export_results_csv(data, "confidence_results.csv")
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#B9B0EB").pack(expand=True)

    def open_extracted_chisquare_data_page(self):
        calculated_height = 400 + len(self.get_all_data()[0]["values"]) * 50

        win = tk.Toplevel(self)
        win.title("Chi-Square Results")
        win.geometry(f"700x{calculated_height}")
        win.configure(bg="#B9B0EB")

        tk.Label(
            win,
            text="Chi-Square Results",
            font=("Safira March Personal Use Only", 24, "bold"),
            bg="#38476e",
            fg="white",
            pady=15
        ).pack(fill="x")

        results = self.chisquare_results

        result_frame = tk.Frame(win, bg="#B9B0EB")

        result_frame.pack(expand=True)

        input_data = self.get_all_data()

        # Display a table of input data with group totals, row totals, and grand total
        table_frame = tk.Frame(result_frame, bg="#B9B0EB")
        table_frame.pack(pady=15)

        # Calculate totals
        group_totals = []
        for group in input_data:
            nums = []
            for v in group["values"]:
                try:
                    nums.append(float(v))
                except:
                    pass
            group_totals.append(sum(nums))

        row_totals = []
        if input_data and input_data[0]["values"]:
            num_rows = len(input_data[0]["values"])
            for i in range(num_rows):
                row_sum = 0
                for group in input_data:
                    try:
                        row_sum += float(group["values"][i])
                    except:
                        pass
                row_totals.append(row_sum)

        grand_total = sum(group_totals)

        # Header row - Row Number label
        tk.Label(
            table_frame,
            text="Row #",
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=12,
            pady=5
        ).grid(row=0, column=0, padx=2, pady=2)

        # Header row (Group 1, Group 2, etc. + Row Total)
        for col in range(len(input_data)):
            tk.Label(
                table_frame,
                text=f"Group {col + 1}",
                bg="#38476e",
                fg="white",
                font=("Verdana", 10, "bold"),
                width=12,
                pady=5
            ).grid(row=0, column=col + 1, padx=2, pady=2)
        
        tk.Label(
            table_frame,
            text="Row Total",
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=12,
            pady=5
        ).grid(row=0, column=len(input_data) + 1, padx=2, pady=2)

        # Data rows
        for row_idx in range(len(row_totals)):
            # Row number column
            tk.Label(
                table_frame,
                text=f"Row {row_idx + 1}",
                bg="#38476e",
                fg="white",
                font=("Verdana", 10, "bold"),
                width=12,
                pady=3
            ).grid(row=row_idx + 1, column=0, padx=2, pady=2)
            
            for col_idx in range(len(input_data)):
                value = input_data[col_idx]["values"][row_idx] if row_idx < len(input_data[col_idx]["values"]) else "0"
                tk.Label(
                    table_frame,
                    text=str(value),
                    bg="white",
                    font=("Verdana", 10, "bold"),
                    width=12,
                    pady=3
                ).grid(row=row_idx + 1, column=col_idx + 1, padx=2, pady=2)
            
            # Row total column
            tk.Label(
                table_frame,
                text=f"{row_totals[row_idx]:.0f}",
                bg="white",
                fg="#38476e",
                font=("Verdana", 10, "bold"),
                width=12,
                pady=3
            ).grid(row=row_idx + 1, column=len(input_data) + 1, padx=2, pady=2)

        # Column totals row
        last_row = len(row_totals) + 1
        tk.Label(
            table_frame,
            text="Column Total",
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=12
        ).grid(row=last_row, column=0, padx=2, pady=2)
        
        for col_idx in range(len(input_data)):
            tk.Label(
                table_frame,
                text=f"{group_totals[col_idx]:.0f}",
                bg="white",
                fg="#38476e",
                font=("Verdana", 10, "bold"),
                width=12,
                pady=3
            ).grid(row=last_row, column=col_idx + 1, padx=2, pady=2)
        
        # Grand total
        tk.Label(
            table_frame,
            text=f"{grand_total:.0f}",
            bg="#38476e",
            fg="white",
            font=("Verdana", 10, "bold"),
            width=12,
            pady=3
        ).grid(row=last_row, column=len(input_data) + 1, padx=2, pady=2)

        tk.Label(
            result_frame,
            text=f"Chi-Square Value: {results['chisquare_statistic']:.2f}",
            bg="#B9B0EB",
            font=("Georgia", 14)
        ).pack(pady=10)

        crit_text = (
            f"{results['critical_chisquare']:.2f}"
            if results['critical_chisquare'] is not None
            else "N/A"
        )

        tk.Label(
            result_frame,
            text=f"Critical Chi-Square: {crit_text}",
            bg="#B9B0EB",
            font=("Georgia", 14)
        ).pack(pady=10)

        tk.Label(
            result_frame,
            text=f"p-value: {results['p_value']:.4f}",
            bg="#B9B0EB",
            font=("Georgia", 14)
        ).pack(pady=10)

        tk.Label(
            result_frame,
            text=f"Chi-Square Statistic: {results['chisquare_statistic']:.2f} | Critical Value: {crit_text} → {'Reject H0' if results['significant'] else 'Fail to Reject H0'}",
            bg="#B9B0EB",
            font=("Georgia", 12, "italic")
        ).pack(pady=(5, 0))

        tk.Label(
            result_frame,
            text=f"p-value: {results['p_value']:.4f} | α: {float(self.significance.get())} → {'Reject H0' if results['p_value'] < float(self.significance.get()) else 'Fail to Reject H0'}",
            bg="#B9B0EB",
            font=("Georgia", 12, "italic")
        ).pack(pady=(0, 10))

        decision = (
            "Reject H0"
            if results['significant']
            else "Fail to Reject H0"
        )

        tk.Label(
            result_frame,
            text=f"Decision: {decision}",
            bg="#B9B0EB",
            fg="#38476e",
            font=("Georgia", 16, "bold")
        ).pack(pady=10)

        result_frame2 = tk.Frame(win, bg="#B9B0EB")
        result_frame2.pack(fill="x", expand=True)

        # ---------------- FOOTER ----------------
        footer_frame = tk.Frame(win, bg="#B9B0EB")
        footer_frame.pack(fill="x")

        button_row = tk.Frame(footer_frame, bg="#B9B0EB")
        button_row.pack(pady=10)

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
            command=lambda: self.export_results_csv(results, "chisquare_results.csv")
        ).pack(side="left", padx=8)

        tk.Label(footer_frame, bg="#B9B0EB").pack(expand=True)

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    app = Inferential(root)

    root.mainloop()
