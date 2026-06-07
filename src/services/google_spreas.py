import re, requests

groups = [
    {"name": "Группа 1", "time": "sun-19:00"},
    {"name": "Группа 2", "time": "mon-19:00"},
    {"name": "Группа 3", "time": "sun-17:00"},
    {"name": "Группа 4", "time": "sun-19:00"},
    {"name": "Группа 5", "time": "wed-19:00"},
    {"name": "Группа 6", "time": "sun-18:00"},
    {"name": "Группа 7", "time": "sun-17:00"},
    {"name": "Группа 8", "time": "sat-19:00"},
    {"name": "Группа 9", "time": "sat-18:00"},
    {"name": "Группа 10", "time": "sat-19:00"},
    {"name": "Группа 11", "time": "tue-19:00"},
    {"name": "Группа 12", "time": "thu-19:00"},
    {"name": "Группа 13", "time": "sat-19:00"},
    {"name": "Группа 14", "time": "sat-18:00"},
    {"name": "Группа 15", "time": "thu-19:00"},
    {"name": "Группа 16", "time": "thu-18:00"},
    {"name": "Группа 17", "time": "thu-20:00"},
    {"name": "Группа 18", "time": "mon-20:00"},
    {"name": "Группа 19", "time": "mon-18:00"},
    {"name": "Группа 20", "time": "tue-18:00"},
    {"name": "Группа 21", "time": "sat-17:00"},
    {"name": "Группа 22", "time": "wed-19:00"},
    {"name": "Группа 23", "time": "thu-19:00"},
    {"name": "Группа 24", "time": "sat-18:00"},
    {"name": "Группа 25", "time": "wed-20:00"},
]


def get_group_info(url):
    sheet_id = re.search(r"/d/([a-zA-Z0-9_-]+)", url).group(1)
    html = requests.get( f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit",
        headers={"User-Agent":"Mozilla/5.0"} ).text
    out = []
    for t in re.findall(r'docs-sheet-tab-caption[^>]*>(.*?)</div>', html, re.S):
        t = re.sub(r'<.*?>','',t).strip()
        m = re.search(r'группа\s*(\d+)', t, re.I)
        if not m: continue
        name = f"Группа {m.group(1)}"
        m2 = re.search(r'(пн|вт|ср|чт|пт|сб|вс)\.?\s*(\d{1,2}:\d{2})', t, re.I)
        if not m2: continue
        out.append({ "name": name, "time": f"{m2.group(1)} {m2.group(2)}" })
    return out if out else groups