# Statify — Statistical Analysis Toolkit

Statify is a small Python toolkit for performing common statistical analyses and creating simple visualizations. It's designed for students and quick data exploration, providing modular functions for descriptive and inferential statistics and basic plotting utilities.

## Key Features

- **Descriptive statistics:** summary measures, distributions ([descriptive.py](descriptive.py)).
- **Inferential statistics:** hypothesis tests and confidence intervals ([inferential.py](inferential.py)).
- **Basic statistics helpers:** reusable functions used across modules ([stat_basic.py](stat_basic.py)).
- **Data lab utilities:** data loading and preprocessing helpers ([data_labs.py](data_labs.py)).
- **Visualizations:** simple plots for analysis and reporting ([visualization.py](visualization.py)).

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python main_python.py
```

## Project layout

- [main_python.py](main_python.py) — program entry / UI launcher
- [config.py](config.py) — configuration and constants
- [descriptive.py](descriptive.py) — descriptive stat routines
- [inferential.py](inferential.py) — inferential stat routines
- [stat_basic.py](stat_basic.py) — core helper functions
- [data_labs.py](data_labs.py) — data utilities and examples
- [visualization.py](visualization.py) — plotting helpers
- images/ — sample images and output

See [README.md](README.md) for additional context and examples.
