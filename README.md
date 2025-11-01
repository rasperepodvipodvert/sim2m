# Sim2M Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Интеграция для мониторинга баланса и трафика на sim2m.ru в Home Assistant.

## Возможности

- 📊 Баланс лицевого счета
- 📈 Использованный трафик
- 📉 Остаток трафика
- 💯 Процент использования
- 🔄 Автоматическое обновление каждый час

## Установка через HACS

1. Откройте HACS в Home Assistant
2. Перейдите в "Integrations"
3. Нажмите на три точки справа вверху
4. Выберите "Custom repositories"
5. Добавьте URL: `https://github.com/rasperepodvipodvert/sim2m`
6. Категория: `Integration`
7. Нажмите "Add"
8. Найдите "Sim2M" в списке и установите

## Установка вручную

1. Скопируйте папку `custom_components/sim2m` в папку `custom_components` вашего Home Assistant
2. Перезапустите Home Assistant

## Настройка

### 1. Получите Refresh Token

1. Откройте https://pay.sim2m.ru в браузере
2. Войдите на сайт (телефон + SMS код)
3. Откройте DevTools (F12)
4. Перейдите: Application → Cookies → https://pay.sim2m.ru
5. Найдите cookie `clientAppRefreshToken`
6. Скопируйте его значение (начинается с `eyJhbG...`)

### 2. Добавьте интеграцию

1. В Home Assistant: Settings → Devices & Services → Add Integration
2. Найдите "Sim2M"
3. Введите:
   - **Refresh Token**: скопированное значение
   - **Account ID**: ваш ID счета (например, `95143`)

### 3. Готово!

Появятся 5 сенсоров:
- `sensor.sim2m_XXXXX_balance` - Баланс (₽)
- `sensor.sim2m_XXXXX_traffic_limit` - Лимит трафика (ГБ)
- `sensor.sim2m_XXXXX_traffic_used` - Использовано (ГБ)
- `sensor.sim2m_XXXXX_traffic_remain` - Осталось (ГБ)
- `sensor.sim2m_XXXXX_traffic_percent` - Использовано (%)

## Как узнать Account ID?

После авторизации на сайте посмотрите URL:
```
https://pay.sim2m.ru/cabinet/private-score/95143
                                              ^^^^^ это ваш ID
```

Или запустите standalone парсер:
```bash
python parser.py
# Покажет доступные счета
```

## Dashboard пример

```yaml
type: entities
title: Sim2M
entities:
  - entity: sensor.sim2m_827907_balance
    name: Баланс
  - entity: sensor.sim2m_827907_traffic_used
    name: Использовано
  - entity: sensor.sim2m_827907_traffic_remain
    name: Осталось
  - entity: sensor.sim2m_827907_traffic_percent
    name: Процент
```

## Автоматизации

```yaml
automation:
  - alias: "Sim2M - Низкий баланс"
    trigger:
      platform: numeric_state
      entity_id: sensor.sim2m_827907_balance
      below: 100
    action:
      service: notify.mobile_app
      data:
        message: "Баланс Sim2M ниже 100₽"

  - alias: "Sim2M - Мало трафика"
    trigger:
      platform: numeric_state
      entity_id: sensor.sim2m_827907_traffic_remain
      below: 50
    action:
      service: notify.mobile_app
      data:
        message: "Осталось меньше 50 ГБ"
```

## Standalone использование

Можно использовать парсер отдельно без Home Assistant:

```bash
# Создайте .env
REFRESH_TOKEN=your_token
ACCOUNT_ID=95143

# Запустите
python parser.py
```

Результат в `traffic_data.json`.

## Обновление токена

Refresh token действует ~1 год. При ошибках:
1. Получите новый токен из браузера
2. Обновите интеграцию в Home Assistant

## Технические детали

- **Опрос:** Каждый час
- **API:** `pay.sim2m.ru/api/*` и скрытый `api.sim2m.ru/sim/getSimTraffic/*`
- **Авторизация:** JWT токены (refresh → access)

## Лицензия

MIT
