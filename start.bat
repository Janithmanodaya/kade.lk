@echo off

REM Step 1: Environment Check
IF EXIST "python" (
    echo Python is already installed.
) ELSE (
    echo Installing Python...
    REM Download python installer if it does not exist
    IF NOT EXIST "python_installer.zip" (
        echo Downloading Python installer...
        curl -L https://github.com/europeanplaice/distribute-embeddable-python/releases/download/v3.11.0/python-3.11.0-embed-amd64.zip -o python_installer.zip
    )

    REM Step 2: Silent Installation (Unzipping)
    cscript //nologo setup.vbs "powershell -ExecutionPolicy Bypass -Command \"Expand-Archive -Path 'python_installer.zip' -DestinationPath '.' -Force\""
    echo Python installation complete.
)

REM Step 3: Virtual Environment Creation
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python\python.exe -m venv venv
    echo Virtual environment created.
)

REM Step 4: Install Core Dependencies
echo Installing dependencies...
venv\Scripts\pip.exe install -r requirements.txt

REM Step 5: Launch the application
echo Starting the application...
venv\Scripts\python.exe app.py
