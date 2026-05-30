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
    for h in range(17,21):
        t = f"{h:02d}:00"
        row.append(CallbackButton(text=f"{t} МСК", payload=f"time:{t}"))
        if len(row) == 2:
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
