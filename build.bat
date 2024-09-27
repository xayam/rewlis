@echo off

venv39\Scripts\python.exe -m PyInstaller rewlis-client.spec

venv39\Scripts\python.exe -m PyInstaller rewlis-creator.spec
