#!/bin/sh
# Скрипт запуска wake_bot.py в screen

SCREEN_NAME=wakebot
PYTHON=/usr/bin/python3   # путь к python3, уточни через `which python3`
BOT_PATH=/root/wake_bot.py
LOG_PATH=/root/wake_bot.log

# Загружаем переменные окружения из файла
[ -f /root/.wakebot_env ] && . /root/.wakebot_env

# Проверяем, есть ли уже запущенный screen
if ! screen -list | grep -q "$SCREEN_NAME"; then
    echo "Запускаем wake_bot.py в screen..."
    screen -dmS "$SCREEN_NAME" $PYTHON $BOT_PATH > $LOG_PATH 2>&1
else
    echo "wake_bot уже запущен"
fi