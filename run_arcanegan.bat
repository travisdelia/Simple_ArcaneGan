@echo off
:: Activate the environment
call arcane\Scripts\activate.bat
echo Environment 'arcane' activated.
echo Running ArcaneGan
python MainGan.py
echo process complete
pause
:: Deactivate the environment
call arcane\Scripts\deactivate.bat
echo Environment 'arcane' deactivated.
pause