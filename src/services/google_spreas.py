import re, requests

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
    return out