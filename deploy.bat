@echo off
setlocal DisableDelayedExpansion
cd /d "%~dp0"

set DJANGO_SETTINGS_MODULE=web_smknj.production_settings
rem Secrets come from deploy.env (gitignored). Format: KEY=value per line.
for /f "usebackq tokens=1,* delims==" %%A in ("%~dp0deploy.env") do set "%%A=%%B"
set DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
set DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
set DJANGO_DB_NAME=smknj
set DJANGO_DB_USER=areybra
set DJANGO_DB_HOST=127.0.0.1
set DJANGO_DB_PORT=3306
set DJANGO_HTTPS=0

env\Scripts\python.exe manage.py collectstatic --noinput
if errorlevel 1 exit /b 1

env\Scripts\waitress-serve.exe --host=0.0.0.0 --port=8000 web_smknj.wsgi:application
