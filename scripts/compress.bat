@echo off
setlocal

set projectDir=%~dp0..
set scriptDir=%projectDir%\scripts
set pythonExe=%projectDir%\env\Scripts\python.exe

pushd "%projectDir%"
"%pythonExe%" "%scriptDir%\compress_image.py"
popd