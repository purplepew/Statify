import tkinter as tk
from tkinter import messagebox

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def box_plot_graph(*groups):
    prepared_groups = []

    for group in groups:
        values = []
        for value in group:
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                pass
        if values:
            prepared_groups.append(values)

    if not prepared_groups:
        messagebox.showwarning("Box Plot", "No valid numeric data was found for the box plot.")
        return

    figure = Figure(figsize=(8.5, 4.5), dpi=100)
    axis = figure.add_subplot(111)

    df = pd.DataFrame(
        [
            (f"Group {index + 1}", value)
            for index, values in enumerate(prepared_groups)
            for value in values
        ],
        columns=["Group", "Value"]
    )

    sns.boxplot(
        x="Group",
        y="Value",
        data=df,
        color="lightblue",
        width=0.4,
        showfliers=False,
        showmeans=True,
        ax=axis,
        meanprops={
            "marker": "^",
            "markerfacecolor": "white",
            "markeredgecolor": "gray",
            "markersize": 6,
        },
    )

    sns.stripplot(x="Group", y="Value", data=df, color="purple", alpha=0.6, jitter=True, size=6, ax=axis)

    all_values = [value for group in prepared_groups for value in group]
    y_min, y_max = min(all_values), max(all_values)
    data_range = y_max - y_min if y_max != y_min else 1

    spacing = data_range * 0.12
    padding = data_range * 0.1

    for index, values in enumerate(prepared_groups):
        series = pd.Series(values)
        mean_val = series.mean()
        median_val = series.median()
        mode_values = series.mode()
        mode_val = mode_values.iloc[0] if not mode_values.empty else mean_val

        axis.scatter(index, mode_val, color="red", marker="D", s=36, zorder=5)

        y_start = series.max() + (spacing * 0.5)
        label_style = dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9)

        axis.text(index, y_start, f"Mode: {mode_val:.2f}", ha="center", color="red",
                  bbox={**label_style, 'edgecolor': 'red'}, fontsize=7)
        axis.text(index, y_start + spacing, f"Median: {median_val:.2f}", ha="center", color="black",
                  bbox={**label_style, 'edgecolor': 'black'}, fontsize=7)
        axis.text(index, y_start + (spacing * 2), f"Mean: {mean_val:.2f}", ha="center", color="gray",
                  bbox={**label_style, 'edgecolor': 'gray'}, fontsize=7)

    axis.set_ylim(y_min - padding, y_max + (spacing * 3.5))

    legend_elements = [
        Line2D([0], [0], color="black", lw=1.5, label="Median"),
        Line2D([0], [0], marker="^", color="white", markeredgecolor="gray", markersize=6, linestyle="None", label="Mean"),
        Line2D([0], [0], marker="D", color="red", markersize=6, linestyle="None", label="Mode"),
        Line2D([0], [0], marker="o", color="purple", alpha=0.6, markersize=6, linestyle="None", label="Data Point"),
    ]
    axis.legend(handles=legend_elements, loc="upper left")
    axis.yaxis.set_major_locator(MaxNLocator(nbins=10))
    axis.tick_params(axis="y", which="major", labelsize=10)
    axis.grid(axis="y", alpha=0.2, linestyle="--")
    figure.tight_layout()
    return figure


def bar_graph(*groups):
    prepared_groups = []

    for group in groups:
        values = []
        for value in group:
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                pass
        if values:
            prepared_groups.append(values)

    if not prepared_groups:
        messagebox.showwarning("Bar Graph", "No valid numeric data was found for the bar graph.")
        return None

    # Calculate statistics for each group
    stats = []
    for values in prepared_groups:
        series = pd.Series(values)
        stats.append({
            "mean": series.mean(),
            "median": series.median(),
            "std_dev": series.std()
        })

    # Prepare data for plotting
    group_labels = [f"Group {i+1}" for i in range(len(prepared_groups))]
    means = [s["mean"] for s in stats]
    medians = [s["median"] for s in stats]
    std_devs = [s["std_dev"] for s in stats]

    figure = Figure(figsize=(10, 6), dpi=100)
    axis = figure.add_subplot(111)

    # Set up bar positions
    x = np.arange(len(group_labels))
    width = 0.35

    # Create bars
    bars1 = axis.bar(x - width/2, means, width, label="Mean", color="#6c0987", alpha=0.8)
    bars2 = axis.bar(x + width/2, medians, width, label="Median", color="#d871f5", alpha=0.8)

    # Labels and title
    axis.set_xlabel("Groups", fontsize=12, fontweight="bold")
    axis.set_ylabel("Value", fontsize=12, fontweight="bold")
    axis.set_title("Mean and Median Comparison by Group", fontsize=14, fontweight="bold")
    axis.set_xticks(x)
    axis.set_xticklabels(group_labels)
    axis.legend(fontsize=11)
    
    # Add more granular y-axis ticks
    axis.yaxis.set_major_locator(MaxNLocator(nbins=10))
    axis.grid(axis="y", alpha=0.3, linestyle="--", which="both")
    axis.tick_params(axis="y", which="major", labelsize=10)

    figure.tight_layout()
    return figure

def scatter_plot(*groups):
    prepared_groups = []
    for group in groups[:2]:  # Only take the first two groups for scatter plot
        values = []
        for value in group:
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                pass
        if values:
            prepared_groups.append(values)

    if len(prepared_groups) < 2:
        messagebox.showwarning("Scatter Plot", "At least two groups with valid numeric data are required for a scatter plot.")
        return None

    figure = Figure(figsize=(8, 8), dpi=100)
    axis = figure.add_subplot(111)

    axis.scatter(prepared_groups[0], prepared_groups[1], color="#6c0987", alpha=0.7, edgecolor="white", s=80)
    
    axis.set_xlabel("Group 1", fontsize=8, fontweight="bold")
    axis.set_ylabel("Group 2", fontsize=8, fontweight="bold")
    axis.set_title("Scatter Plot of Groups", fontsize=14, fontweight="bold")
    #axis.legend(fontsize=11)
    axis.grid(alpha=0.3, linestyle="--")
    figure.tight_layout()
    return figure


def _prepare_groups(*groups):
    prepared = []
    for group in groups:
        values = []
        for value in group:
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                pass
        if values:
            prepared.append(values)
    return prepared


def central_tendency_figure(*groups):
    plt.close('all')
    prepared = _prepare_groups(*groups)
    if not prepared:
        messagebox.showwarning("Central Tendency", "No valid numeric data found.")
        return None

    # Build metrics DataFrame
    rows = []
    for i, vals in enumerate(prepared, start=1):
        s = pd.Series(vals)
        mode_val = s.mode().iloc[0] if not s.mode().empty else s.mean()
        rows.append({
            'Group': f'Group {i}',
            'Mean': s.mean(),
            'Median': s.median(),
            'Mode': mode_val,
        })

    df = pd.DataFrame(rows)
    df_melt = df.melt(id_vars=['Group'], value_vars=['Mean', 'Median', 'Mode'], var_name='Metric', value_name='Value')

    fig = Figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(111)

    if df['Group'].nunique() > 1:
        sns.barplot(data=df_melt, x='Metric', y='Value', hue='Group', ax=ax)
    else:
        sns.barplot(data=df_melt, x='Metric', y='Value', ax=ax)
        leg = ax.get_legend()
        if leg:
            leg.remove()

    ax.set_title('Central Tendency (Mean / Median / Mode)')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
    fig.tight_layout()
    return fig


def variability_overview_figure(*groups):
    plt.close('all')
    prepared = _prepare_groups(*groups)
    if not prepared:
        messagebox.showwarning("Variability Overview", "No valid numeric data found.")
        return None

    rows = []
    for i, vals in enumerate(prepared, start=1):
        s = pd.Series(vals)
        rows.append({'Group': f'Group {i}', 'Range': max(vals) - min(vals), 'Variance': s.var(), 'StdDev': s.std()})

    df = pd.DataFrame(rows)
    df_melt = df.melt(id_vars=['Group'], value_vars=['Range', 'Variance', 'StdDev'], var_name='Metric', value_name='Value')

    fig = Figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(111)

    if df['Group'].nunique() > 1:
        sns.lineplot(data=df_melt, x='Metric', y='Value', hue='Group', marker='o', ax=ax)
    else:
        sns.lineplot(data=df_melt, x='Metric', y='Value', marker='o', ax=ax)
        leg = ax.get_legend()
        if leg:
            leg.remove()

    ax.set_title('Variability Overview (Range / Variance / StdDev)')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
    fig.tight_layout()
    return fig


def frequency_breakdown_figure(*groups):
    plt.close('all')
    prepared = _prepare_groups(*groups)
    if not prepared:
        messagebox.showwarning("Frequency Breakdown", "No valid numeric data found.")
        return None

    n = len(prepared)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    # normalize axes to iterable
    if n == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if hasattr(axes, 'flatten') else list(axes)

    for idx, vals in enumerate(prepared):
        ax = axes[idx]
        series = pd.Series(vals)
        freq = series.value_counts(normalize=True).sort_index() * 100
        labels = [str(l) for l in freq.index]
        sizes = freq.values
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(f'Group {idx+1} Frequency (%)')

    # convert plt figure to Matplotlib Figure instance for Tk embedding
    # fig is a pyplot.Figure; convert by returning it directly
    return fig


def distribution_summary_figure(*groups):
    plt.close('all')
    prepared = _prepare_groups(*groups)
    if not prepared:
        messagebox.showwarning("Distribution Summary", "No valid numeric data found.")
        return None

    # Create wide DataFrame (one column per group)
    data = {f'Group {i+1}': pd.Series(vals) for i, vals in enumerate(prepared)}
    df = pd.DataFrame(data)

    fig = Figure(figsize=(9, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Seaborn accepts wide-form DataFrame for boxplot
    sns.boxplot(data=df, ax=ax)
    sns.stripplot(data=df, color='purple', alpha=0.4, size=4, ax=ax)

    ax.set_title('Distribution Summary (Box-and-Whisker by Group)')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
    fig.tight_layout()
    return fig

class VisualizationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.source_window = parent
        self.title("Visualization")

        window_width = 900
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(bg="#d871f5")

        self.subcategories_visible = False

        header_frame = tk.Frame(self, bg="#6c0987", height=60)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Show Visualization",
            font=("Georgia", 14, "bold"),
            fg="white",
            bg="#6c0987"
        ).pack(side="left", padx=20)

        content_frame = tk.Frame(self, bg="#d871f5")
        content_frame.pack(fill="both", expand=True)

        self.chart_frame = tk.Frame(content_frame, bg="white", highlightbackground="gray80", highlightthickness=1)
        self.chart_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(20, 10))

        self.chart_placeholder = tk.Label(
            self.chart_frame,
            text="Select a visualization to display the chart here.",
            bg="white",
            fg="#6c0987",
            font=("Verdana", 11, "bold")
        )
        self.chart_placeholder.pack(expand=True)

        self.footer_frame = tk.Frame(content_frame, bg="#d871f5")
        self.footer_frame.pack(side="bottom", fill="x", pady=20)

        tk.Label(self.footer_frame, bg="#d871f5").pack(expand=True)

        tk.Button(
            self.footer_frame,
            text="Show Visualization",
            fg="white",
            bg="#6c0987",
            font=("Verdana", 10, "bold"),
            padx=20,
            pady=10,
            command=self.toggle_subcategories
        ).pack(pady=5)

        self.subcategory_frame = tk.Frame(self.footer_frame, bg="#d871f5")

        tk.Button(
            self.subcategory_frame,
            text="Central Tendency",
            fg="#6c0987",
            bg="white",
            font=("Verdana", 10, "bold"),
            padx=12,
            pady=8,
            command=self.show_central_tendency
        ).pack(side="left", padx=5)

        tk.Button(
            self.subcategory_frame,
            text="Variability Overview",
            fg="#6c0987",
            bg="white",
            font=("Verdana", 10, "bold"),
            padx=12,
            pady=8,
            command=self.show_variability_overview
        ).pack(side="left", padx=5)

        tk.Button(
            self.subcategory_frame,
            text="Frequency Breakdown",
            fg="#6c0987",
            bg="white",
            font=("Verdana", 10, "bold"),
            padx=12,
            pady=8,
            command=self.show_frequency_breakdown
        ).pack(side="left", padx=5)

        tk.Button(
            self.subcategory_frame,
            text="Distribution Summary",
            fg="#6c0987",
            bg="white",
            font=("Verdana", 10, "bold"),
            padx=12,
            pady=8,
            command=self.show_distribution_summary
        ).pack(side="left", padx=5)

        tk.Label(self.footer_frame, bg="#d871f5").pack(expand=True)

    def toggle_subcategories(self):
        if self.subcategories_visible:
            self.subcategory_frame.pack_forget()
        else:
            self.subcategory_frame.pack(pady=10)
        self.subcategories_visible = not self.subcategories_visible

    def show_box_plot(self):
        self.display_figure(box_plot_graph(*[group["values"] for group in self.source_window.get_all_data()]))

    def show_bar_graph(self):
        self.display_figure(bar_graph(*[group["values"] for group in self.source_window.get_all_data()]))

    def show_scatter_plot(self):
        self.display_figure(scatter_plot(*[group["values"] for group in self.source_window.get_all_data()]))

    def show_central_tendency(self):
        groups = [group["values"] for group in self.source_window.get_all_data()]
        fig = central_tendency_figure(*groups)
        self.display_figure(fig)

    def show_variability_overview(self):
        groups = [group["values"] for group in self.source_window.get_all_data()]
        fig = variability_overview_figure(*groups)
        self.display_figure(fig)

    def show_frequency_breakdown(self):
        groups = [group["values"] for group in self.source_window.get_all_data()]
        fig = frequency_breakdown_figure(*groups)
        self.display_figure(fig)

    def show_distribution_summary(self):
        groups = [group["values"] for group in self.source_window.get_all_data()]
        fig = distribution_summary_figure(*groups)
        self.display_figure(fig)

    def display_figure(self, figure):
        if figure is None:
            return

        for child in self.chart_frame.winfo_children():
            child.destroy()

        self.chart_figure = figure
        self.chart_canvas = FigureCanvasTkAgg(self.chart_figure, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)


class VisualizationScatterPlotExclusive(tk.Toplevel):
    '''A simplified visualization window that only shows the scatter plot,
    without the option to switch between different visualizations.
    This is used specifically for the "Show Scatter Plot" button in the inferential statistics results window.'''

    def __init__(self, parent):
        super().__init__(parent)
        self.source_window = parent
        self.title("Visualization (Scatter Plot Only)")

        window_width = 900
        window_height = 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(bg="#d871f5")

        header_frame = tk.Frame(self, bg="#6c0987", height=60)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Correlation Scatter Plot",
            font=("Georgia", 14, "bold"),
            fg="white",
            bg="#6c0987"
        ).pack(side="left", padx=20)

        content_frame = tk.Frame(self, bg="#d871f5")
        content_frame.pack(fill="x", expand=True)

        self.chart_frame = tk.Frame(content_frame, bg="white", highlightbackground="gray80", highlightthickness=1)
        self.chart_frame.pack(side="top", fill="x", expand=True, padx=20, pady=(20, 10))

        self.show_scatter_plot()

    def show_scatter_plot(self):
        self.display_figure(scatter_plot(*[group["values"] for group in self.source_window.get_all_data()][:2]))

    def display_figure(self, figure):
        if figure is None:
            return

        for child in self.chart_frame.winfo_children():
            child.destroy()

        self.chart_figure = figure
        self.chart_canvas = FigureCanvasTkAgg(self.chart_figure, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

