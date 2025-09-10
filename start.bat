@echo off

REM This script uses a self-contained Python environment and a virtual environment.
REM This is a best practice for distributable applications as it avoids modifying the user's system-wide Python installation.

REM Step 1: Environment Check
IF EXIST "python" (
    echo Python is already installed.
) ELSE (
    echo Installing Python...
    REM Download python installer if it does not exist
    IF NOT EXIST "python_installer.zip" (
        echo Downloading Python installer...
        where curl >nul 2>nul
        IF %ERRORLEVEL% EQU 0 (
            echo Using curl to download...
            curl -L https://github.com/europeanplaice/distribute-embeddable-python/releases/download/v3.11.0/python-3.11.0-embed-amd64.zip -o python_installer.zip
            IF %ERRORLEVEL% NEQ 0 (
                echo curl download failed. Please check your internet connection and try again.
                pause
                exit /b 1
            )
        ) ELSE (
            echo curl not found, using powershell...
            powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/europeanplaice/distribute-embeddable-python/releases/download/v3.11.0/python-3.11.0-embed-amd64.zip' -OutFile 'python_installer.zip' -UseBasicParsing } catch { Write-Error $_; exit 1 }"
            IF %ERRORLEVEL% NEQ 0 (
                echo powershell download failed. Please check your internet connection and try again.
                pause
                exit /b 1
            )
        )
    )

    REM Check if download was successful
    IF NOT EXIST "python_installer.zip" (
        echo Failed to download Python installer. An unknown error occurred.
        pause
        exit /b 1
    )

    REM Step 2: Installation (Unzipping)
    echo Unzipping Python installer...
    powershell -ExecutionPolicy Bypass -Command "try { Expand-Archive -Path 'python_installer.zip' -DestinationPath '.' -Force } catch { Write-Host 'Error: Failed to unzip installer.'; Write-Error $_; exit 1 }"
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to unzip the Python installer. The file might be corrupt.
        echo Please delete python_installer.zip and try again.
        pause
        exit /b 1
    )
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
