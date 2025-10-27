# 🛰 Wake Bot for OpenWrt

Wake Bot — это лёгкий скрипт для удалённого включения компьютеров в локальной сети через Wake-on-LAN, работающий прямо на роутере OpenWrt.  
Бот написан на Python и может работать как сервис, автоматически поднимающийся после перезагрузки устройства.

## 📦 Состав проекта

- **wake_bot.py** — основной Python-скрипт, обрабатывающий запросы на включение устройств (Wake-on-LAN).
- **start_wakebot.sh** — shell-скрипт для запуска `wake_bot.py` в отдельной screen-сессии.
- **init.d/wakebot** *(опционально)* — скрипт автозапуска для OpenWrt, чтобы бот стартовал при загрузке.

## ⚙️ Установка

```bash
cd /root  
git clone https://github.com/GoozyaGod/GS_WakeBot.git  
cd GS_WakeBot
```

Установка зависимостей:

```bash
opkg update  
opkg install python3 python3-pip  
# (если etherwake не установлен)
opkg install etherwake  
```

## 🚀 Запуск вручную

```bash
sh start_wakebot.sh  
```

После запуска создаётся screen-сессия под именем **wakebot**.

Просмотр логов:

```bash
tail -f /root/wake_bot.log  
```

Управление screen-сессией:

```bash
screen -r wakebot     # войти  
Ctrl+A, затем D       # выйти  
Ctrl+A, затем K       # закрыть  
```

## 🔁 Автозапуск при старте роутера

Если используется init.d-скрипт, нужно сделать его исполняемым и включить автозапуск:

```bash
chmod +x /etc/init.d/wakebot  
/etc/init.d/wakebot enable  
/etc/init.d/wakebot start  
```

## 🧩 Полезные команды

```bash
screen -list          # проверить, запущен ли бот  
killall python3       # остановить бота  
sh start_wakebot.sh   # перезапустить  
```

## 📘 Примечание

Бот поддерживает авторизацию по Telegram ID и позволяет включать устройства по MAC-адресам через etherwake.  
Всё работает прямо на OpenWrt без внешних серверов.

## 📝 Лицензия

MIT License © 2025 Goozya
