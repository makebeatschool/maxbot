import calendar
from datetime import datetime
from maxapi.types import CallbackButton, ButtonsPayload
from config import DAYS

def weekdays_keyboard():
    buttons = []
    row = []
    for text, value in DAYS:
        row.append( CallbackButton( text=text, payload=f"weekday:{value}" ) )
    buttons.append(row)
    return ButtonsPayload(buttons=buttons).pack()

def time_keyboard():
    buttons = []
    row = []
    for h in range(24):
        t = f"{h:02d}:00"
        row.append(CallbackButton(text=t, payload=f"time:{t}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return ButtonsPayload(buttons=buttons).pack()

def open_weekdays_keyboard():
    return ButtonsPayload(
        buttons=[ [CallbackButton(text="Хотите изменить день?", payload="change_weekday")] ]
    ).pack()
def open_time_keyboard():
    return ButtonsPayload(
        buttons=[ [CallbackButton(text="Хотите изменить время?", payload="change_time")] ]
    ).pack()

#  не используетсся (сделал а удалять жалко)
# MONTHS_RU = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
# WEEKDAYS_RU = ["Пн","Вт","Ср","Чт","Пт","Сб","Вс"]
# def shift_month(year, month, delta):
#     month += delta
#     while month < 1:
#         month += 12
#         year -= 1
#     while month > 12:
#         month -= 12
#         year += 1
#     return year, month
# def calendar_keyboard(year=None, month=None):
#     now = datetime.now()
#     year = year or now.year
#     month = month or now.month
#     cal = calendar.Calendar(firstweekday=0)
#     buttons = []
#     buttons.append([CallbackButton(text=f"{MONTHS_RU[month-1]} {year}", payload="ignore")])
#     buttons.append([CallbackButton(text=d, payload="ignore") for d in WEEKDAYS_RU])
#     for week in cal.monthdayscalendar(year, month):
#         row = []
#         for day in week:
#             if day == 0:
#                 row.append(CallbackButton(text="·", payload="ignore"))
#             else:
#                 row.append(CallbackButton(text=str(day), payload=f"day:{year}:{month}:{day}"))
#         buttons.append(row)
#     py, pm = shift_month(year, month, -1)
#     ny, nm = shift_month(year, month, 1)
#     buttons.append([
#         CallbackButton(text="⏪ -1 год", payload=f"year:{year-1}:{month}"),
#         CallbackButton(text="⬅️", payload=f"month:{py}:{pm}"),
#         CallbackButton(text="Сегодня", payload=f"today:{now.year}:{now.month}:{now.day}"),
#         CallbackButton(text="➡️", payload=f"month:{ny}:{nm}"),
#         CallbackButton(text="+1 год", payload=f"year:{year+1}:{month}")
#     ])
#     return ButtonsPayload(buttons=buttons).pack()

