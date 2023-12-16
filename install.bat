echo off

:: Create the new environment
python -m venv arcane
echo Environment 'arcane' created.

:: Activate the environment
call arcane\Scripts\activate.bat
echo Environment 'arcane' activated.


:: Run install.py script
python install.py
echo Required packages installed.


:: Deactivate the environment
call arcane\Scripts\deactivate.bat
echo Environment 'arcane' deactivated.

:: Pause to keep the window open and view any output/error messages
pause