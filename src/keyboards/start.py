from maxapi.types import ButtonsPayload, CallbackButton, LinkButton
from texts import TEXT_START_FROM_GROUP, TEXT_START_BTN
from env import id_bot

# на всякий случай получение контактов
# def start_keyboard():
#     return ButtonsPayload(
#         buttons=[
#             [RequestContactButton(text=text_start_btn)]
#         ]
#     ).pack()
def start_keyboard():
    return ButtonsPayload(
        buttons=[ [CallbackButton(text=TEXT_START_BTN, payload="start_bot")] ]
    ).pack()
def start_from_group_keyboard():
    return ButtonsPayload(
        buttons=[
            [ LinkButton( text=TEXT_START_FROM_GROUP,
                    url=f"https://max.ru/{id_bot}" )]
        ]
    ).pack()