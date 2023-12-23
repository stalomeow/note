@echo off
call .\env\Scripts\activate.bat
mkdocs serve
call .\env\Scripts\deactivate.bat