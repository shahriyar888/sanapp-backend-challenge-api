@echo off
REM Development Helper Script

if "%1"=="" goto help
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="clean" goto clean
if "%1"=="setup" goto setup
goto help

:start
echo Starting development services (PostgreSQL, Redis, MinIO)...
docker-compose -f docker-compose.dev.yml --env-file .env.development up -d
echo.
echo Waiting for PostgreSQL to be ready...
timeout /t 3 /nobreak >nul
echo.
echo Services started! Now run Django locally:
echo   python manage.py migrate
echo   python manage.py runserver
goto end

:stop
echo Stopping development services...
docker-compose -f docker-compose.dev.yml down
goto end

:restart
echo Restarting development services...
docker-compose -f docker-compose.dev.yml --env-file .env.development restart
goto end

:logs
docker-compose -f docker-compose.dev.yml logs -f
goto end

:clean
echo Stopping and removing all containers and volumes...
docker-compose -f docker-compose.dev.yml down -v
goto end

:setup
echo Setting up development environment...
echo.
echo 1. Copying environment file...
if not exist .env (
    copy .env.development .env
    echo .env created from .env.development
) else (
    echo .env already exists, skipping...
)
echo.
echo 2. Starting services...
docker-compose -f docker-compose.dev.yml --env-file .env.development up -d
echo.
echo 3. Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul
echo.
echo 4. Running migrations...
python manage.py migrate
echo.
echo Setup complete! Start Django with:
echo   python manage.py runserver
goto end

:help
echo Usage: dev.bat [command]
echo.
echo Commands:
echo   setup    - First time setup (copy .env, start services, migrate)
echo   start    - Start development services (db, redis, minio)
echo   stop     - Stop development services
echo   restart  - Restart development services
echo   logs     - Show service logs
echo   clean    - Stop services and remove volumes
echo.
echo First time? Run: dev.bat setup
echo After that, use: python manage.py runserver
goto end

:end
