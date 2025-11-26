@echo off
REM Build the nonwordgen GUI as a standalone Windows executable.
REM
REM Requirements (in your Python environment):
REM   - PyInstaller
REM   - PyQt6 (the "gui" extra from pyproject.toml)
REM   - An icon file at assets\nonword-gen.ico
REM
REM The resulting executable will be placed in the "dist" folder
REM as nonwords-gen.exe.

setlocal

echo Building nonwords-gen.exe...
py -m PyInstaller nonwords-gen.spec

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed. See PyInstaller output above.
    exit /b %ERRORLEVEL%
)

echo.
echo Build complete. You can run:
echo   dist\nonwords-gen\nonwords-gen.exe

endlocal

