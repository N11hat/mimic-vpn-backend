from aiogram.fsm.state import State, StatesGroup


class PromoState(StatesGroup):
    # Бот ждёт, пока пользователь введёт промокод текстом
    waiting_for_promo = State()


class TopUpState(StatesGroup):
    # Бот ждёт, пока пользователь введёт сумму пополнения текстом
    waiting_for_amount = State()

class BroadcastState(StatesGroup):
    waiting_for_text = State()
    waiting_for_confirm = State()
