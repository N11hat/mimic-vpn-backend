from datetime import datetime, timedelta
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from sqlalchemy import select
from database.models import User, async_session
from services.vpn_api import MarzbanAPI

router = Router()

def get_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Получить тест (24ч)", callback_data="get_trial")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")]
    ])

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
        if not user:
            new_user = User(tg_id=message.from_user.id, username=message.from_user.username)
            session.add(new_user)
            await session.commit()
            
    await message.answer("Добро пожаловать в VPN! Выбери действие:", reply_markup=get_main_kb())

@router.callback_query(F.data == "get_trial")
async def process_trial(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))
        
        if user.trial_used:
            await callback.answer("Ты уже использовал тестовый период!", show_alert=True)
            return

        vpn_key = await MarzbanAPI.create_user_config(user.tg_id)
        user.trial_used = True
        user.vpn_key = vpn_key
        user.subscription_end = datetime.now() + timedelta(days=1)
        
        await session.commit()
        
        await callback.message.edit_text(
            f"✅ Твой тестовый период активирован на 24 часа!\n\n"
            f"Твой ключ доступа:\n`{vpn_key}`\n\n"
            f"Для подключения скачай клиент VLESS.",
            parse_mode="Markdown"
        )

@router.callback_query(F.data == "profile")
async def process_profile(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))
        
        if user.subscription_end and user.subscription_end > datetime.now():
            status = f"Активна до {user.subscription_end.strftime('%d.%m.%Y %H:%M')}"
            key = f"\nТвой ключ: `{user.vpn_key}`"
        else:
            status = "Неактивна ❌"
            key = ""

        await callback.message.edit_text(
            f"👤 Твой профиль\nID: {user.tg_id}\nПодписка: {status}{key}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
            ])
        )

@router.callback_query(F.data == "back_to_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text("Выбери действие:", reply_markup=get_main_kb())