from datetime import datetime, timedelta
import re
import requests
from config import BASE_URL, HEADERS, MOSCOW

# пример работы с амо - пока нигде не используется 

def _normalize_phone(phone: str) -> str:
    return re.sub(r"\D+", "", phone or "")

def _parse_group_name(value: str) -> datetime | None:
    try:
        d, t = value.strip().split()
        return datetime(
            int(d[4:8]),
            int(d[2:4]),
            int(d[0:2]),
            int(t[0:2]),
            int(t[2:4]),
            tzinfo=MOSCOW,
        )
    except Exception:
        return None

def _fallback_tomorrow_16() -> str:
    dt = datetime.now(MOSCOW).replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return dt

def _plus_one_minute() -> str:
    return (datetime.now(MOSCOW) + timedelta(minutes=1))

def _safe_get_json(url: str, **kwargs) -> dict | None:
    try:
        resp = requests.get(url, timeout=20, **kwargs)
        if resp.status_code == 204:
            return None
        resp.raise_for_status()
        if not resp.text.strip():
            return None
        return resp.json()
    except (requests.RequestException, ValueError):
        return None

def get_trial_datetime_by_phone(phone: str) -> str:
    phone = _normalize_phone(phone)
    if not phone:
        return _fallback_tomorrow_16()
    data = _safe_get_json( f"{BASE_URL}/api/v4/contacts",
        headers=HEADERS, params={"query": phone, "with": "leads"}, )
    if not data:
        return _fallback_tomorrow_16()
    contacts = data.get("_embedded", {}).get("contacts", [])
    if not contacts:
        return _fallback_tomorrow_16()
    contact = contacts[0]
    lead_id = next(
        (l.get("id") for l in contact.get("_embedded", {}).get("leads", []) if l.get("id")),
        None, )
    if not lead_id:
        return _fallback_tomorrow_16()
    lead_data = _safe_get_json( f"{BASE_URL}/api/v4/leads/{lead_id}",
        headers=HEADERS, params={"with": "catalog_elements"}, )
    if not lead_data:
        return _fallback_tomorrow_16()
    catalog_elements = lead_data.get("_embedded", {}).get("catalog_elements", [])
    if not catalog_elements:
        return _fallback_tomorrow_16()
    catalog_element_id = catalog_elements[0].get("id")
    if not catalog_element_id:
        return _fallback_tomorrow_16()
    catalog_data = _safe_get_json(
        f"{BASE_URL}/api/v4/catalogs/12278/elements/{catalog_element_id}",
        headers=HEADERS, )
    if not catalog_data:
        return _fallback_tomorrow_16()
    dt = _parse_group_name(catalog_data.get("name", ""))
    if not dt:
        return _fallback_tomorrow_16()
    now_utc = datetime.now(MOSCOW)
    if dt.astimezone(MOSCOW) < now_utc:
        return _plus_one_minute()
    # dt = dt - timedelta(hours=3)
    # return dt.astimezone(timezone.utc).isoformat()
    return dt.astimezone(MOSCOW)