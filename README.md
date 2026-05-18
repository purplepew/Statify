
# Statify: How to Run on Windows

This guide starts from a fresh VS Code installation and walks through cloning the project, installing dependencies, and launching the app.

## What You Need

- A Windows computer
- Internet access
- Visual Studio Code installed
- Git installed
- Python 3.8 or newer installed

If you do not have Git or Python yet, install them first:

- Git: https://git-scm.com/downloads
- Python: https://www.python.org/downloads/

When installing Python, make sure **Add Python to PATH** is checked.

## Step 1: Open VS Code

1. Open Visual Studio Code.
2. Open the terminal inside VS Code by selecting **Terminal > New Terminal**.

## Step 2: Clone the Project

In the VS Code terminal, run:

```powershell
git clone https://github.com/purplepew/Statify.git
```

After the download finishes, open the project folder:

```powershell
cd Statify
code .
```

If `code .` does not work, use **File > Open Folder** in VS Code and select the `Statify` folder manually.

## Step 3: Install the Dependencies

In the VS Code terminal, run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `python` is not recognized, try:

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Step 4: Run the Program

Start the app with:

```powershell
python main_python.py
```

If that does not work, try:

```powershell
py main_python.py
```

## What Should Happen

- A window titled **Statistics Calculator** should open.
- The app starts from [main_python.py](main_python.py).
- Use the buttons in the app to open the Data Lab and other features.

## If Something Goes Wrong

- If you see a missing module error, run the dependency install command again.
- If Python is not found, reinstall Python and make sure it is added to PATH.
- If the app closes immediately, always run it from the terminal instead of double-clicking the file.
- If you still get an error, copy the exact message and share it with the developer.
