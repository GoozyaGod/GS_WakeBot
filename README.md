# 🛰 Wake Bot for OpenWrt

Wake Bot — это лёгкий скрипт для удалённого включения компьютеров в локальной сети через Wake-on-LAN, работающий прямо на роутере OpenWrt.  
Бот написан на Python и может работать как сервис, автоматически поднимающийся после перезагрузки устройства.

## 📦 Состав проекта

- **wake_bot.py** — основной Python-скрипт, обрабатывающий запросы на включение устройств (Wake-on-LAN).  
- **start_wakebot.sh** — shell-скрипт для запуска `wake_bot.py` в отдельной screen-сессии.  
- **install_wakebot.sh** — установщик, который настраивает среду, создаёт `.wakebot_env` и запускает бота в screen.  

## ⚙️ Установка

1. Склонируйте репозиторий на роутер:

    ```bash
    cd /root
    git clone https://github.com/GoozyaGod/GS_WakeBot.git
    cd GS_WakeBot
    ```

2. Создайте файл токена `.wakebot_env` (установщик предложит ввести токен):

    ```bash
    WAKEBOT_TOKEN=твой_новый_токен
    ```

    > Файл `.wakebot_env` **не добавляется в Git**, он указан в `.gitignore`.  

3. Запустите установщик:

    ```bash
    sh install_wakebot.sh
    ```

Установщик выполнит:

- установку зависимостей (`python3`, `pip3`, `etherwake`);
- создание файла `.wakebot_env` с токеном;
- запуск бота в screen;
- настройку автозапуска через init.d (если нужно).

---

## 🚀 Управление ботом

**Запуск вручную**:

```bash
sh start_wakebot.sh
```

**Просмотр логов**:

```bash
tail -f /root/wake_bot.log
```

**Остановка бота**:

```bash
# Через screen
screen -r wakebot   # войти
Ctrl+C              # остановить
Ctrl+A, затем K     # закрыть screen
```

или:

```bash
killall python3
```

---

## 🔁 Автозапуск при старте роутера

Если используется init.d-скрипт (создаётся установщиком):

```bash
chmod +x /etc/init.d/wakebot
/etc/init.d/wakebot enable
/etc/init.d/wakebot start
```

---

## 📝 Примечание

Бот поддерживает авторизацию по Telegram ID и позволяет включать устройства по MAC-адресам через `etherwake`.  
Все настройки безопасно хранятся в `.wakebot_env` и не попадают в GitHub.

---

## 📝 Лицензия

MIT License © 2025 Goozya
