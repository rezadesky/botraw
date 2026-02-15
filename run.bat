@echo off
setlocal enabledelayedexpansion

:: Master Launcher for Highrise Bot
:: Usage: run.bat [number] OR run.bat all

set "OPT=%1"
if "!OPT!"=="" set "OPT=all"

if "!OPT!"=="all" (
    echo Starting all bot instances in background...
    start "Bot 1" cmd /k "%~f0 1"
    start "Bot 2" cmd /k "%~f0 2"
    exit /b
)

:: Individual Bot Logic
set "BOT_NUM=!OPT!"
title Bot Instance !BOT_NUM! - Highrise
set "ENV_FILE=instances/bot_!BOT_NUM!/.env"
set "DATABASE_URL=sqlite://database/bot_!BOT_NUM!.db"

:: Check for virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate

:: Dependency Installation
echo Checking and fixing dependencies for Bot !BOT_NUM!...
pip install tortoise-orm aiosqlite httpx loguru python-dotenv --quiet
pip install highrise-bot-sdk==24.1.0 --no-deps --quiet
pip install aiohttp cattrs click pendulum quattro --quiet
pip install typing-extensions>=4.12.2 --upgrade --quiet

:: Ensure database directory exists
if not exist "database" mkdir database

:: Start the bot
echo Starting Bot Instance !BOT_NUM!...
:loop
python -m core.bot
echo Bot !BOT_NUM! crashed or stopped. Restarting in 5 seconds...
timeout /t 5
goto loop
