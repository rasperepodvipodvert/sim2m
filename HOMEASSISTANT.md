# Интеграция с Home Assistant

## Способы интеграции

### Способ 1: Command Line Sensor (самый простой)

Запускает Python скрипт и читает вывод.

#### Конфигурация

Добавьте в `configuration.yaml`:

```yaml
sensor:
  - platform: command_line
    name: "Sim2M Баланс"
    command: "cd /Users/ifilatov/Projects/home/sim2m && source venv/bin/activate && python parser.py | grep 'Баланс:' | awk '{print $2}' | tr -d '₽'"
    unit_of_measurement: "₽"
    scan_interval: 3600  # Обновление каждый час

  - platform: command_line
    name: "Sim2M Трафик Использовано"
    command: "cd /Users/ifilatov/Projects/home/sim2m && source venv/bin/activate && python parser.py | grep 'Использовано:' | awk '{print $2}'"
    scan_interval: 3600

  - platform: command_line
    name: "Sim2M Трафик Осталось"
    command: "cd /Users/ifilatov/Projects/home/sim2m && source venv/bin/activate && python parser.py | grep 'Осталось:' | head -1 | awk '{print $2}'"
    scan_interval: 3600
```

**Плюсы:** Просто
**Минусы:** Запускает парсер для каждого сенсора (медленно)

---

### Способ 2: File Sensor (рекомендуется)

Парсер сохраняет JSON, сенсор читает файл.

#### 1. Настройте cron для запуска парсера

```bash
crontab -e
```

Добавьте:
```
0 * * * * cd /Users/ifilatov/Projects/home/sim2m && source venv/bin/activate && python parser.py > /dev/null 2>&1
```

#### 2. Добавьте в `configuration.yaml`

```yaml
sensor:
  - platform: file
    name: "Sim2M Data"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ value_json.data.balance }}"
    scan_interval: 300

  - platform: file
    name: "Sim2M Баланс"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ value_json.data.balance }}"
    unit_of_measurement: "₽"
    scan_interval: 300

  - platform: file
    name: "Sim2M Трафик Лимит"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ (value_json.data.traffic.limit / 1024) | round(2) }}"
    unit_of_measurement: "ГБ"
    scan_interval: 300

  - platform: file
    name: "Sim2M Трафик Использовано"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ (value_json.data.traffic.used / 1024) | round(2) }}"
    unit_of_measurement: "ГБ"
    scan_interval: 300

  - platform: file
    name: "Sim2M Трафик Осталось"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ (value_json.data.traffic.remain / 1024) | round(2) }}"
    unit_of_measurement: "ГБ"
    scan_interval: 300

  - platform: file
    name: "Sim2M Трафик Процент"
    file_path: /Users/ifilatov/Projects/home/sim2m/traffic_data.json
    value_template: "{{ ((value_json.data.traffic.used / value_json.data.traffic.limit) * 100) | round(1) }}"
    unit_of_measurement: "%"
    scan_interval: 300
```

**Плюсы:** Быстро, один запуск парсера
**Минусы:** Требует cron

---

### Способ 3: RESTful Sensor через Flask API

Создайте простой API сервер.

#### 1. Создайте `api_server.py`

```python
#!/usr/bin/env python3
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/sim2m')
def get_sim2m_data():
    try:
        with open('traffic_data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({'error': 'No data'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
```

#### 2. Запустите сервер

```bash
pip install flask
python api_server.py &
```

#### 3. Home Assistant `configuration.yaml`

```yaml
sensor:
  - platform: rest
    name: "Sim2M Баланс"
    resource: http://localhost:5555/api/sim2m
    value_template: "{{ value_json.data.balance }}"
    unit_of_measurement: "₽"
    scan_interval: 300

  - platform: rest
    name: "Sim2M Трафик Использовано"
    resource: http://localhost:5555/api/sim2m
    value_template: "{{ (value_json.data.traffic.used / 1024) | round(2) }}"
    unit_of_measurement: "ГБ"
    scan_interval: 300
```

**Плюсы:** Профессиональный подход
**Минусы:** Требует Flask сервер

---

### Способ 4: MQTT (для продвинутых)

Публикуйте данные в MQTT broker.

#### 1. Установите зависимости

```bash
pip install paho-mqtt
```

#### 2. Модифицируйте `parser.py`

Добавьте в конец:

```python
import paho.mqtt.client as mqtt

# Публикуем в MQTT
client = mqtt.Client()
client.connect("localhost", 1883)

client.publish("sim2m/balance", data.get('balance'))
client.publish("sim2m/traffic/used", data['traffic'].get('used'))
client.publish("sim2m/traffic/remain", data['traffic'].get('remain'))

client.disconnect()
```

#### 3. Home Assistant `configuration.yaml`

```yaml
mqtt:
  sensor:
    - name: "Sim2M Баланс"
      state_topic: "sim2m/balance"
      unit_of_measurement: "₽"

    - name: "Sim2M Трафик Использовано"
      state_topic: "sim2m/traffic/used"
      unit_of_measurement: "МБ"
```

**Плюсы:** Real-time обновления
**Минусы:** Требует MQTT broker

---

## Рекомендация

**Для начала используйте Способ 2 (File Sensor):**

1. Настройте cron для запуска парсера каждый час
2. Home Assistant читает `traffic_data.json`
3. Просто и надежно

## Пример Dashboard

```yaml
type: entities
title: Sim2M
entities:
  - entity: sensor.sim2m_balance
    name: Баланс
  - entity: sensor.sim2m_traffic_limit
    name: Лимит трафика
  - entity: sensor.sim2m_traffic_used
    name: Использовано
  - entity: sensor.sim2m_traffic_remain
    name: Осталось
  - type: custom:bar-card
    entity: sensor.sim2m_traffic_percent
    name: Использование трафика
    max: 100
```

## Автоматизации

```yaml
automation:
  - alias: "Sim2M - Низкий баланс"
    trigger:
      - platform: numeric_state
        entity_id: sensor.sim2m_balance
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Баланс Sim2M меньше 100₽!"

  - alias: "Sim2M - Мало трафика"
    trigger:
      - platform: numeric_state
        entity_id: sensor.sim2m_traffic_remain
        below: 50
    action:
      - service: notify.mobile_app
        data:
          message: "Осталось меньше 50 ГБ трафика!"
```
