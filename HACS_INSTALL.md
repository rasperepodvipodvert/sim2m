# Установка в HACS - Пошаговая инструкция

## Способ 1: Через меню HACS (новый интерфейс)

### Шаг 1: Откройте меню HACS

1. В Home Assistant откройте боковое меню
2. Нажмите на **HACS**
3. В правом верхнем углу нажмите на **три точки (⋮)** или **профиль**
4. Выберите **Custom repositories**

### Шаг 2: Добавьте репозиторий

1. В поле **Repository** введите: `https://github.com/rasperepodvipodvert/sim2m`
2. В поле **Category** выберите: `Integration`
3. Нажмите **Add**

### Шаг 3: Установите интеграцию

1. Вернитесь в HACS → Integrations
2. В поиске введите: `Sim2M`
3. Нажмите на карточку Sim2M
4. Нажмите **Download**
5. Перезапустите Home Assistant

### Шаг 4: Настройте интеграцию

1. Settings → Devices & Services
2. Нажмите **+ Add Integration** (справа внизу)
3. Найдите `Sim2M`
4. Введите:
   - **Refresh Token**: ваш токен из браузера
   - **Account ID**: ID счета (например, `95143`)
5. Submit

---

## Способ 2: Если не нашли Custom repositories

### Через файловую систему Home Assistant

1. Откройте File Editor или SSH
2. Перейдите в `.storage/`
3. Отредактируйте файл `hacs.repositories`
4. Добавьте:
   ```json
   {
     "repository": "rasperepodvipodvert/sim2m",
     "category": "integration"
   }
   ```
5. Перезапустите Home Assistant
6. Интеграция появится в HACS

---

## Способ 3: Ручная установка (без HACS)

Если HACS не установлен или не работает:

### Через SSH или File Editor

1. Подключитесь к Home Assistant по SSH
2. Перейдите в папку config:
   ```bash
   cd /config
   ```
3. Создайте папку для интеграции:
   ```bash
   mkdir -p custom_components/sim2m
   ```
4. Скачайте файлы:
   ```bash
   cd custom_components/sim2m
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/__init__.py
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/api.py
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/config_flow.py
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/const.py
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/manifest.json
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/sensor.py
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/strings.json

   mkdir translations
   cd translations
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/translations/ru.json
   wget https://raw.githubusercontent.com/rasperepodvipodvert/sim2m/main/custom_components/sim2m/translations/en.json
   ```
5. Перезапустите Home Assistant
6. Settings → Devices & Services → Add Integration → Sim2M

---

## Как получить Refresh Token

### Пошагово:

1. **Откройте браузер** (Chrome, Safari, Firefox)
2. **Перейдите на** https://pay.sim2m.ru
3. **Войдите на сайт:**
   - Введите телефон
   - Введите код из SMS
   - Дождитесь загрузки личного кабинета
4. **Откройте DevTools:**
   - Нажмите `F12` (или `Cmd+Option+I` на Mac)
5. **Перейдите в раздел Application:**
   - Вкладка **Application** (или **Приложение**)
   - Слева: **Storage** → **Cookies** → `https://pay.sim2m.ru`
6. **Найдите cookie:** `clientAppRefreshToken`
7. **Скопируйте значение** (двойной клик → Cmd+C)
   - Начинается с `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - Длинная строка (~300+ символов)

### Скриншот процесса:

```
DevTools → Application → Cookies → pay.sim2m.ru
┌────────────────────────────────────────────┐
│ Name                    │ Value            │
├────────────────────────────────────────────┤
│ _ym_uid                 │ 1762001681...    │
│ clientAppRefreshToken   │ eyJhbGciOiJ... ← ЭТО!
│ _ym_d                   │ 1762001681...    │
└────────────────────────────────────────────┘
```

---

## Как узнать Account ID

### На сайте:

1. Зайдите на https://pay.sim2m.ru
2. Откройте свой счет
3. Посмотрите URL в адресной строке:
   ```
   https://pay.sim2m.ru/cabinet/private-score/95143
                                                ^^^^^ ваш ID
   ```

### Или запустите парсер:

```bash
cd /path/to/sim2m
source venv/bin/activate
python parser.py
```

Парсер покажет:
```
📋 Доступные лицевые счета:
   • Счет 827907 → используйте ID: 95143
   • Счет 864545 → используйте ID: 139507
```

Используйте **ID** (не номер счета!)

---

## Проблемы?

### "Cannot find Sim2M integration"

- Убедитесь, что создали Release на GitHub (нужен тег v1.0.0)
- Перезапустите Home Assistant
- Проверьте логи: Settings → System → Logs

### "Cannot connect to API"

- Проверьте токен (скопирован полностью?)
- Проверьте Account ID (это ID, а не номер счета)
- Токен действителен ~1 год, обновите при необходимости

### "Integration not showing in HACS"

- Подождите 5-10 минут после добавления
- Обновите список: HACS → Integrations → Refresh (справа вверху)
- Попробуйте ручную установку (Способ 3)

---

## Альтернатива: File Sensor (без интеграции)

Если не получается установить через HACS, используйте простой file sensor:

1. Настройте cron для запуска `parser.py` каждый час
2. В `configuration.yaml`:
   ```yaml
   sensor:
     - platform: file
       name: "Sim2M Баланс"
       file_path: /path/to/sim2m/traffic_data.json
       value_template: "{{ value_json.data.balance }}"
   ```

Подробнее в [HOMEASSISTANT.md](HOMEASSISTANT.md)

---

**Нужна помощь?** Создайте Issue на GitHub: https://github.com/rasperepodvipodvert/sim2m/issues
