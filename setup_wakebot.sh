#!/bin/sh
# ======================================
#  Автоматическая настройка Wake-on-LAN Telegram Bot
# ======================================

# === Настройки ===
PYTHON=/usr/bin/python3
BOT_PATH=/root/wake_bot.py
START_SCRIPT=/root/start_wakebot.sh
INIT_SCRIPT=/etc/init.d/wakebot
LOG_PATH=/root/wake_bot.log
SCREEN_NAME=wakebot

echo "==> Обновляем пакеты..."
opkg update

echo "==> Устанавливаем необходимые пакеты..."
opkg install python3 python3-pip screen etherwake

echo "==> Проверяем установку python3 и screen..."
which python3
which screen

echo "==> Устанавливаем python-библиотеки..."
$PYTHON -m pip install --no-cache-dir python-telegram-bot==13.15 APScheduler

echo "==> Создаём init-скрипт..."
cat << 'EOF' > $INIT_SCRIPT
#!/bin/sh /etc/rc.common
# /etc/init.d/wakebot
START=99
STOP=10

start() {
    echo "Запуск wake_bot..."
    /root/start_wakebot.sh &
}

stop() {
    echo "Остановка wake_bot..."
    screen -S wakebot -X quit 2>/dev/null
}
EOF

chmod +x $INIT_SCRIPT
/etc/init.d/wakebot enable

echo "==> Проверяем наличие стартового скрипта..."
if [ ! -f "$START_SCRIPT" ]; then
    echo "⚠️  Файл start_wakebot.sh не найден. Создаю пример..."
    cat << 'EOF' > $START_SCRIPT
#!/bin/sh
SCREEN_NAME=wakebot
PYTHON=/usr/bin/python3
BOT_PATH=/root/wake_bot.py
LOG_PATH=/root/wake_bot.log

if ! screen -list | grep -q "\$SCREEN_NAME"; then
    echo "Запускаем wake_bot.py в screen..."
    screen -dmS "\$SCREEN_NAME" \$PYTHON \$BOT_PATH > \$LOG_PATH 2>&1
else
    echo "wake_bot уже запущен"
fi
EOF
    chmod +x $START_SCRIPT
fi

echo "==> Настройка завершена!"
echo "Бот будет запускаться при старте системы."
