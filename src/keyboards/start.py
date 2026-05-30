from maxapi.types import ButtonsPayload, CallbackButton, LinkButton, RequestContactButton
from texts import TEXT_START_FROM_GROUP, TEXT_START_BTN
from env import id_bot



def start_trial_keyboard():
    return ButtonsPayload(
        buttons=[
            [RequestContactButton(text=TEXT_START_BTN, payload="start_trial_bot")]
        ]
    ).pack()


def start_keyboard():
    return ButtonsPayload(
        buttons=[ [CallbackButton(text=TEXT_START_BTN, payload="start_bot")] ]
    ).pack()
def start_from_group_keyboard(typeOfUser):
    return ButtonsPayload(
        buttons=[
            [ LinkButton( text=TEXT_START_FROM_GROUP,
                    url=f"https://max.ru/{id_bot}?start={typeOfUser}" )]
        ]
    ).pack()