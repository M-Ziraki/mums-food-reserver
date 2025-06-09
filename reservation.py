from bs4 import BeautifulSoup
from config import BASE_URL, RESERVE_PATH
import requests


def collect_hidden(soup: BeautifulSoup) -> dict:
    """همهٔ hidden inputs را به یک دیکشنری می‌ریزد."""
    return {
        inp['name']: inp.get('value', '')
        for inp in soup.find_all('input', {'type': 'hidden'})
        if inp.get('name')
    }


def fetch_page(session: requests.Session, last_html: str, action: str = None, meal_value: str = None) -> str:
    """
    صفحهٔ رزرو را GET یا POST می‌کند و HTML جدید را برمی‌گرداند.
    - action: 'prev', 'next', 'meal' یا None
    - meal_value: در صورت تغییر وعده، مقدار value آن
    """
    if action is None or action == 'today':
        resp = session.get(BASE_URL + RESERVE_PATH)
    else:
        soup = BeautifulSoup(last_html, 'html.parser')
        data = collect_hidden(soup)
        if action == 'prev':
            data['ctl00$body$btnlastWeek'] = 'هفته قبل'
        elif action == 'next':
            data['ctl00$body$btnNextWeek'] = 'هفته بعد'
        elif action == 'meal':
            data['ctl00$body$dpFoodMeal'] = meal_value or ''
            data['__EVENTTARGET'] = 'ctl00$body$dpFoodMeal'
            data['__EVENTARGUMENT'] = ''
        resp = session.post(BASE_URL + RESERVE_PATH, data=data)
    resp.raise_for_status()
    return resp.text


def parse_panels(html: str) -> list[dict]:
    """
    HTML صفحه را پارس می‌کند و برای هر روز یک دیکشنری شامل:
    - title: عنوان روز (مثلاً "1404/03/19 - دوشنبه")
    - reserved_label: متن غذا در صورت رزرو
    - caf_options: لیست گزینه‌های سلف (text, value)
    """
    soup = BeautifulSoup(html, 'html.parser')
    panels = []
    hdrs = soup.select("div[id^='body_rptFoodDiet_dvHeader_']")
    for idx, hdr in enumerate(hdrs):
        title = hdr.select_one(
            f"#body_rptFoodDiet_lblDayDate_{idx}").text.strip()
        container = hdr.find_parent('div', class_='Panel')
        body = container.find('div', class_='panel-body')
        # اگر رادیوباتن checked باشد یعنی رزرو شده
        reserved_input = body.find('input', attrs={'checked': 'checked'})
        reserved_label = None
        if reserved_input:
            reserved_label = reserved_input.find_next(
                'label').get_text(strip=True)
        # سلف‌ها
        sel = soup.find(id=f'body_rptFoodDiet_dpSelf_{idx}')
        caf_options = []
        if sel:
            for o in sel.find_all('option'):
                caf_options.append((o.text, o['value']))
        panels.append({
            'title': title,
            'reserved_label': reserved_label,
            'caf_options': caf_options
        })
    return panels
