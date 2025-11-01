"""API клиент для Sim2M."""
import requests


class Sim2MAPI:
    """API клиент для работы с sim2m.ru."""

    def __init__(self, refresh_token: str):
        """Инициализация API клиента."""
        self.refresh_token = refresh_token
        self.session = requests.Session()
        self.session.cookies.set('clientAppRefreshToken', refresh_token, domain='sim2m.ru')

    def get_access_token(self) -> str | None:
        """Получает access token."""
        try:
            resp = self.session.get('https://pay.sim2m.ru/api/refreshTokens', timeout=10)
            if resp.status_code == 200:
                return resp.json().get('accessToken')
        except Exception:
            return None
        return None

    def get_data(self, account_id: str) -> dict | None:
        """Получает все данные аккаунта."""
        access_token = self.get_access_token()
        if not access_token:
            return None

        self.session.headers['Authorization'] = f"Bearer {access_token}"

        # Получаем данные аккаунта
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

        try:
            resp = self.session.post('https://pay.sim2m.ru/api/ql', json=query, timeout=10)
            if resp.status_code != 200:
                return None

            result = resp.json()
            if 'errors' in result:
                return None

            account = result['data']['getPrivateScoreById']

            # Получаем трафик
            if account.get('simCard'):
                msisdn = account['simCard']['msisdn']
                traffic_resp = self.session.get(
                    f'https://api.sim2m.ru/sim/getSimTraffic/{msisdn}',
                    timeout=10
                )

                if traffic_resp.status_code == 200:
                    account['traffic'] = traffic_resp.json()

            return account

        except Exception:
            return None
