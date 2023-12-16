@echo off
:: Activate the environment
call arcane\Scripts\activate.bat
echo Environment 'arcane' activated.
echo Running ArcaneGan
python BulkGan.py
echo process complete
:: Deactivate the environment
call arcane\Scripts\deactivate.bat
echo Environment 'arcane' deactivated.