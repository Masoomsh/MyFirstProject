@echo off
rem Starts the LiteLLM proxy on port 4000 with the variables from .env loaded.
cd /d "%~dp0"
for /f "usebackq eol=# tokens=1,* delims==" %%a in (".env") do set "%%a=%%b"
set PYTHONIOENCODING=utf-8
".venv\Scripts\litellm.exe" --config liteLLM_config.yaml --port 4000
