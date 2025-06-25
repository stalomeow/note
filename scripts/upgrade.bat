@echo off
setlocal

set projectDir=%~dp0..
set scriptDir=%projectDir%\scripts
set pythonExe=%projectDir%\env\Scripts\python.exe

pushd "%projectDir%"
"%pythonExe%" -m pip install --upgrade pip
"%pythonExe%" -m pip install --upgrade --force-reinstall mkdocs-material
"%pythonExe%" -m pip freeze > requirements.txt
popd