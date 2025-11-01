#!/usr/bin/env python3
"""
Парсер sim2m.ru - читает токен из .env
"""

import requests
import json
from datetime import datetime
import os


def load_env():
    """Загружает переменные из .env файла"""
    env = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key] = value
        return env
    except FileNotFoundError:
        return None


def format_traffic(mb):
    """МБ → ГБ"""
    if mb == 0:
        return "0 МБ"
    gb = mb / 1024
    return f"{gb:.2f} ГБ" if gb >= 1 else f"{mb} МБ"


def get_data(refresh_token, account_id):
    """Получает все данные"""

    session = requests.Session()
    session.cookies.set('clientAppRefreshToken', refresh_token, domain='sim2m.ru')

    # 1. Access token
    resp = session.get('https://pay.sim2m.ru/api/refreshTokens')
    if resp.status_code != 200:
        print(f"❌ Ошибка получения токена: {resp.status_code}")
        return None

    access_token = resp.json()['accessToken']
    session.headers['Authorization'] = f"Bearer {access_token}"

    # 2. Данные аккаунта
    query = {
        "query": """query getPrivateScoreById($id: ID!) {
            getPrivateScoreById(id: $id) {
                score
                balance
                simCard {
                    msisdn
                    icc
                    operator
                    rate {
                        name
                        ap
                    }
                }
            }
        }""",
        "variables": {"id": account_id}
    }

    resp = session.post('https://pay.sim2m.ru/api/ql', json=query)
    if resp.status_code != 200:
        print(f"❌ Ошибка API: {resp.status_code}")
        return None

    result = resp.json()
    if 'errors' in result:
        print(f"❌ {result['errors'][0]['message']}")
        return None

    account = result['data']['getPrivateScoreById']

    # 3. Трафик
    if account.get('simCard'):
        msisdn = account['simCard']['msisdn']
        traffic_resp = session.get(f'https://api.sim2m.ru/sim/getSimTraffic/{msisdn}')

        if traffic_resp.status_code == 200:
            account['traffic'] = traffic_resp.json()

    return account


def main():
    import sys

    # Загружаем .env
    env = load_env()

    if env:
        refresh_token = env.get('REFRESH_TOKEN')
        account_id = env.get('ACCOUNT_ID', '95143')
        print("✓ Токен загружен из .env")
    else:
        # Из аргументов
        if len(sys.argv) < 2:
            print("❌ Файл .env не найден и токен не передан")
            print("\nИспользование:")
            print("  python parser.py <refresh_token> [account_id]")
            print("\nИли создайте .env файл:")
            print("  REFRESH_TOKEN=ваш_токен")
            print("  ACCOUNT_ID=95143")
            return

        refresh_token = sys.argv[1]
        account_id = sys.argv[2] if len(sys.argv) > 2 else "95143"

    print(f"Лицевой счет: {account_id}\n")

    # Получаем данные
    data = get_data(refresh_token, account_id)

    if not data:
        return

    # Выводим
    print("="*60)
    print(f"Счет: {data.get('score')}")
    print(f"Баланс: {data.get('balance')} ₽")

    if data.get('simCard'):
        s = data['simCard']
        print(f"\nSIM: {s.get('icc')}")
        print(f"Номер: {s.get('msisdn')}")
        print(f"Оператор: {s.get('operator')}")

        if s.get('rate'):
            print(f"\nТариф: {s['rate'].get('name')}")
            print(f"Абонплата: {s['rate'].get('ap')} ₽/мес")

    if data.get('traffic'):
        t = data['traffic']
        print(f"\nТРАФИК:")
        print(f"Лимит: {format_traffic(t.get('limit'))}")
        print(f"Использовано: {format_traffic(t.get('used'))}")
        print(f"Осталось: {format_traffic(t.get('remain'))}")

        if t.get('limit', 0) > 0:
            print(f"Процент: {(t.get('used', 0) / t['limit']) * 100:.1f}%")

    print("="*60)

    # Сохраняем
    with open('traffic_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'account_id': account_id,
            'data': data
        }, f, ensure_ascii=False, indent=2)

    print("\n✓ Сохранено в traffic_data.json")


if __name__ == "__main__":
    main()
