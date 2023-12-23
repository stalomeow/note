@echo off
call .\env\Scripts\activate.bat
python .\scripts\blog_helper.py %*
call .\env\Scripts\deactivate.bat