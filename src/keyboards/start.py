from maxapi.types import ButtonsPayload, CallbackButton, LinkButton
from config import TEXT_START_FROM_GROUP, text_start_btn, id_bot

# def start_keyboard():
#     return ButtonsPayload(
#         buttons=[
#             [RequestContactButton(text=text_start_btn)]
#         ]
#     ).pack()
def start_keyboard():
    return ButtonsPayload(
        buttons=[
            [CallbackButton(text=text_start_btn, payload="start_bot")]
        ]
    ).pack()
def start_from_group_keyboard():
    return ButtonsPayload(
        buttons=[
            [ LinkButton( text=TEXT_START_FROM_GROUP,
                    url=f"https://max.ru/{id_bot}" )]
        ]
    ).pack()