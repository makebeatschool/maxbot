from maxapi.types import ButtonsPayload, CallbackButton


def yes_no_keyboard():
    return ButtonsPayload(buttons=[
        [
            CallbackButton(text="Да", payload="kid_yes"),
            CallbackButton(text="Нет", payload="kid_no")
        ]
    ]).pack()