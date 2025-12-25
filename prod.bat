@echo off
REM Production Helper Script

if "%1"=="" goto help
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="build" goto build
goto help

:start
echo Starting production services (all in Docker)...
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
echo.
echo Production services started!
echo Access at: http://localhost
goto end

:stop
echo Stopping production services...
docker-compose -f docker-compose.prod.yml down
goto end

:restart
echo Restarting production services...
docker-compose -f docker-compose.prod.yml --env-file .env.production restart
goto end

:logs
docker-compose -f docker-compose.prod.yml logs -f %2
goto end

:build
echo Building and starting production services...
docker-compose -f docker-compose.prod.yml --env-file .env.production up --build -d
goto end

:help
echo Usage: prod.bat [command]
echo.
echo Commands:
echo   start    - Start all production services
echo   stop     - Stop all production services
echo   restart  - Restart production services
echo   logs     - Show service logs (add service name for specific logs)
echo   build    - Build and start services
goto end

:end
