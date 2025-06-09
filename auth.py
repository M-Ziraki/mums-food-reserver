import requests
from config import BASE_URL, LOGIN_API, CAPTCHA_URL


class ESSSession(requests.Session):
    """جلسهٔ HTTP که از requests.Session به ارث می‌برد."""

    def load_captcha(self):
        """کپچا را دریافت و برمی‌گرداند به صورت باینری."""
        resp = self.get(BASE_URL + CAPTCHA_URL)
        resp.raise_for_status()
        return resp.content

    def login(self, username: str, password: str, captcha: str) -> dict:
        """
        عملیات لاگین را انجام می‌دهد.
        خروجی: دیتای JSON پاسخ (شامل Key/Value).
        """
        payload = {
            'username': username,
            'password': password,
            'captcha': captcha
        }
        resp = self.post(BASE_URL + LOGIN_API, json=payload)
        resp.raise_for_status()
        return resp.json().get('d', {})
