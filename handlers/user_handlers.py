from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, CommandObject
from keyboards import main_menu_kb, cabinet_kb, connect_kb, sub_balance_kb, tariffs_kb, top_up_kb, top_up_presets_kb, android_setup_kb, ios_setup_kb, win10_setup_kb, macos_setup_kb, win7_setup_kb, linux_setup_kb, huawei_setup_kb, android_tv_setup_kb, apple_tv_setup_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.requests import get_or_create_user, get_balance, get_discount, apply_promocode, count_referrals
from aiogram.types import FSInputFile
from utils.messages import safe_edit

class PromoState(StatesGroup):
    waiting_for_promo = State()
class TopUpState(StatesGroup):
    waiting_for_amount = State()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject):
    # Парсим реферера из ссылки ?start=ref_12345
    referrer_id = None
    args = command.args
    if args and args.startswith("ref_"):
        try:
            referrer_id = int(args.split("_")[1])
        except (ValueError, IndexError):
            pass

    # Регистрируем (или находим) юзера в БД
    user, is_new = await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        referrer_id=referrer_id,
    )

    # Приветствие
    text = (
        "👋 Добро пожаловать в <b>Rumbush VPN</b>!\n\n"
        "Безопасный и быстрый интернет без границ."
    )

    # Бонус приветствия по реферальной ссылке (только новым юзерам)
    if is_new and user.referrer_id:
        text += "\n\n🎁 <i>Вы приглашены пользователем нашей сети!</i>"

    await message.answer(text, reply_markup=main_menu_kb, parse_mode="HTML")

# Обработка нажатия на "Личный кабинет"
@router.callback_query(F.data == "cabinet")
async def open_cabinet(callback: types.CallbackQuery):
    # Указываем путь к картинке. 
    # Убедись, что папка images лежит в корне твоего проекта
    # и картинка называется точно так же: cabinet_banner.jpg (или .png)
    photo = FSInputFile("images/cabinet_banner.jpg")
    
    # Текст, который будет под картинкой
    text = (
        "<b>Личный кабинет</b>\n\n"
        "Тут будет твой баланс и статус."
    )
    
    # Так как мы не можем просто "изменить текст" на "картинку с текстом" в одном сообщении,
    # мы удаляем старое сообщение с текстом...
    await callback.message.delete()
    
    # ...и отправляем новое сообщение уже с фоткой и нашей клавиатурой!
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=cabinet_kb,
        parse_mode="HTML"
    )
    
    # Закрываем всплывающее уведомление-часики на кнопке
    await callback.answer()

# Обработка нажатия на "Подключиться"
@router.callback_query(F.data == "connect")
async def open_connect(callback: types.CallbackQuery):
    await safe_edit(callback, " <b>Выберите ваше устройство:</b>", reply_markup=connect_kb, parse_mode="HTML")

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await safe_edit(callback, " Главное меню:", reply_markup=main_menu_kb)

# Обработка нажатия на "Подписка и баланс"
@router.callback_query(F.data == "sub_balance")
async def open_sub_balance(callback: types.CallbackQuery):
    await safe_edit(callback,
        "💳 <b>Управление подпиской и балансом</b>\n\n"
        "Здесь вы можете пополнить внутренний счет или выбрать подходящий тарифный план.",
        reply_markup=sub_balance_kb,
        parse_mode="HTML"
    )

# Обработка нажатия на "Приобрести подписку"
@router.callback_query(F.data == "buy_sub")
async def open_tariffs(callback: types.CallbackQuery, state: FSMContext):
    # Достаем данные пользователя из памяти (есть ли там скидка)
    discount = await get_discount(callback.from_user.id)
    # Базовые цены
    p_7d, p_1m, p_3m, p_6m = 99, 250, 750, 1250
    
    # Если есть скидка, пересчитываем
    if discount > 0:
        p_7d = int(p_7d * (1 - discount / 100))
        p_1m = int(p_1m * (1 - discount / 100))
        p_3m = int(p_3m * (1 - discount / 100))
        p_6m = int(p_6m * (1 - discount / 100))
        discount_text = f"\n🎁 <i>Применена скидка {discount}% по промокоду!</i>\n"
    else:
        discount_text = "\n"

    text = (
        "📈 <b>Выберите срок подписки на сервис</b>\n\n"
        "👛 Текущий баланс: <b>0₽</b>\n"
        f"{discount_text}\n"
        f"💥 7 дней — {p_7d}₽\n"
        f"✨ 1 месяц — {p_1m}₽\n"
        f"❤️‍🔥 3 месяца — {p_3m}₽\n"
        f"🔥 6 месяцев — {p_6m}₽\n\n"
        "ℹ️ <i>Оплата будет списана с вашего личного счёта в Личном Кабинете.</i>\n\n"
        "🔒 <i>Выберите подходящий срок подписки и защитите свои данные уже сегодня!</i>"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=tariffs_kb,
        parse_mode="HTML"
    )

    # --- 1. Нажатие на кнопку "Промокоды" ---
@router.callback_query(F.data == "promo")
async def enter_promo_code(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer() # <--- ДОБАВИТЬ СЮДА
    await safe_edit(
        callback,
        "🎁 <b>Активация промокода</b>\n\n"
        "Отправьте ваш промокод ответным сообщением:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Отмена", callback_data="cabinet")]
        ]),
    )
     # Переводим бота в режим ожидания текста
    await state.set_state(PromoState.waiting_for_promo)

# --- 2. Ловим текст промокода ---
@router.message(PromoState.waiting_for_promo)
async def process_promo_code(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()
    discount = await apply_promocode(message.from_user.id, code)

    if discount is not None:
        await message.answer(
            f"✅ <b>Промокод успешно активирован!</b>\n\n"
            f"Вы получили скидку <b>{discount}%</b> на все тарифы. Перейдите к покупке подписки.",
            reply_markup=cabinet_kb,
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "❌ <b>Промокод не найден, истёк или уже использован.</b>\n\n"
            "Проверьте правильность ввода или вернитесь в кабинет.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="↩️ Вернуться в кабинет", callback_data="cabinet")]
            ]),
            parse_mode="HTML",
        )

    await state.set_state(None)

@router.callback_query(F.data == "partner") # Укажи тут свой callback_data от кнопки партнёрки
async def open_partner_program(callback: types.CallbackQuery):
    await callback.answer() # <--- ДОБАВИТЬ СЮДА
    user_id = callback.from_user.id
    
    # Чтобы бот сам подставлял свой юзернейм (например, @rumbush_vpn_bot)
    bot_info = await callback.bot.get_me()
    bot_username = bot_info.username
    
    # Формируем персональную ссылку
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    
    partner_balance = await get_balance(user_id)
    referrals_count = await count_referrals(user_id)
    
    text = (
        "🤝 <b>Партнёрская программа</b>\n\n"
        "Приглашайте друзей и зарабатывайте <b>20%</b> с каждой их покупки на свой баланс!\n\n"
        f"Ваш текущий баланс: <b>{partner_balance}₽</b>\n\n"
	f"👥 Приглашено друзей: <b>{referrals_count}</b>\n\n"
        "🔗 <b>Ваша персональная ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "<i>(Нажмите на ссылку, чтобы скопировать)</i>"
    )
    
    await safe_edit(
        callback,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="↩️ Вернуться в кабинет", callback_data="cabinet")]
        ]),
    )


    # --- Пополнение баланса: Открытие главного меню ---
@router.callback_query(F.data == "top_up_balance")
async def open_top_up_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None) # Сбрасываем состояния, если они были
    
    balance = await get_balance(callback.from_user.id)
    
    text = (
        "📈 <b>Пополнение личного счёта</b>\n\n"
        f"👛 Текущий баланс: <b>{balance}₽</b>\n\n"
        "ℹ️ Пополнение баланса — разовая операция, не подписка. "
        "Ваши платежные данные остаются в безопасности.\n\n"
        "🎯 <b>Вы можете:</b>\n"
        "• Выбрать готовую сумму из списка ниже\n"
        "• Ввести любую сумму от <b>50₽</b> до <b>15.000₽</b>\n\n"
        "👇 <i>Выберите сумму для пополнения баланса</i>"
    )
    
    await safe_edit(callback, text, reply_markup=top_up_kb, parse_mode="HTML")

# --- Пополнение баланса: Нажатие на "Ввести сумму" ---
@router.callback_query(F.data == "custom_amount")
async def enter_custom_amount(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    balance = await get_balance(callback.from_user.id)

    
    text = (
        f"⭐️ Текущий баланс: <b>{balance}₽</b>\n\n"
        "💰 <b>Введите сумму для пополнения Вашего баланса</b>\n\n"
        "ℹ️ Доступный диапазон: <b>от 50₽ до 15.000₽</b>. <i>Просто отправьте "
        "число в чат (например: 500)</i>"
    )
    
    await safe_edit(callback, text, reply_markup=top_up_presets_kb, parse_mode="HTML")
    # Включаем режим ожидания ввода суммы
    await state.set_state(TopUpState.waiting_for_amount)

# --- Пополнение баланса: Ловим введенный текст ---
@router.message(TopUpState.waiting_for_amount)
async def process_custom_amount(message: types.Message, state: FSMContext):
    # Пытаемся превратить текст в число
    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer("❌ <b>Ошибка:</b> Пожалуйста, отправьте только число (например: 500).", parse_mode="HTML")
        return
        
    # Проверяем диапазон (как ты и просил: от 50 до 15 000)
    if amount < 50 or amount > 15000:
        await message.answer("❌ <b>Ошибка:</b> Сумма должна быть от 50₽ до 15.000₽. Попробуйте еще раз.", parse_mode="HTML")
        return
        
    # Если всё отлично, отключаем режим ожидания и переходим к оплате
    await state.set_state(None)
    await message.answer(
        f"✅ <b>Отлично!</b> Вы выбрали пополнение на <b>{amount}₽</b>.\n\n"
        "<i>(Дальше здесь появится ссылка на платежную систему)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Вернуться в кабинет", callback_data="cabinet")]
        ]),
        parse_mode="HTML"
    )

# --- Пополнение баланса: Обработка готовых кнопок (100, 200, 500...) ---
# Фильтр F.data.startswith("pay_") ловит ВСЕ кнопки, которые начинаются на pay_
@router.callback_query(F.data.startswith("pay_"))
async def process_preset_amount(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None) # Отключаем ожидание текста, если оно было
    
    # Достаем цифру из названия кнопки (например из "pay_500" достаем "500")
    amount = int(callback.data.split("_")[1])
    
    await safe_edit(callback,
        f"✅ <b>Отлично!</b> Вы выбрали пополнение на <b>{amount}₽</b>.\n\n"
        "<i>(Дальше здесь появится ссылка на платежную систему)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Вернуться в кабинет", callback_data="cabinet")]
        ]),
        parse_mode="HTML"
    )# Обработка выбора устройства "Android"
@router.callback_query(F.data == "os_android")
async def instruction_android(callback: types.CallbackQuery):
    await callback.answer()
    
    # Временный ключ для примера (позже научим бота брать его из базы данных для каждого юзера свой)
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "🤖 Настройка <b>Rumbush VPN</b> на Android через HAPP:\n\n"
        "1️⃣ Откройте <a href='https://play.google.com/store'>Google Play Маркет</a> или скачайте APK у нас - <a href='https://clck.ru/3TP3Xe'>HAPP</a>\n\n"
        "2️⃣ Запустите приложение, скопируйте ключ доступа (нажмите 1 раз по ключу) или нажмите на кнопку ниже \"Подключить\":\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ В приложении <b>HAPP</b> нажмите \"+\" и выберите \"<b>Вставить из буфера обмена</b>\"\n\n"
        "4️⃣ Выберите нужную локацию и включите VPN\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=android_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "iOS"
@router.callback_query(F.data == "os_ios")
async def instruction_ios(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики" загрузки
    
    # Временный ключ (как и в Android)
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "🍏 Настройка <b>Rumbush VPN</b> на iOS через HAPP\n\n"
        "1️⃣ Откройте <a href='https://apps.apple.com/'>App Store</a> и скачайте приложение <b>HAPP</b>\n\n"
        "2️⃣ Запустите приложение, скопируйте ваш ключ доступа (нажмите 1 раз по ключу) или используйте кнопку \"Подключить\" ниже:\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ В приложении <b>HAPP</b> нажмите \"+\" → выберите \"<b>Импорт из буфера обмена</b>\"\n\n"
        "4️⃣ Выберите нужную локацию и включите VPN"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=ios_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Windows 10+"
@router.callback_query(F.data == "os_win10")
async def instruction_win10(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики" загрузки
    
    # Временный ключ
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "💻 Настройка <b>Rumbush VPN</b> на Windows через HAPP:\n\n"
        "1️⃣ Скачайте и установите приложение <a href='https://clck.ru/3TP7C5'>HAPP</a>\n\n"
        "2️⃣ Запустите его <b>от имени администратора</b> и скопируйте ключ доступа (нажмите 1 раз по ключу):\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ При первом запуске появится окно с вводом ключа, вставьте туда скопированный ключ и нажмите \"<b>Поехали</b>\"\n\n"
        "4️⃣ После добавления ключа появится список локаций и основные кнопки. Выберите нужную локацию и нажмите на неё\n\n"
        "5️⃣ Если Вам необходим <b>VPN для Discord, Игр и т.п</b>, то внизу нажмите \"<b>TUN</b>\", а если только для браузера \"<b>Proxy</b>\"\n\n"
        "6️⃣ Нажмите на большую кнопку включения и дождитесь подключения к серверам.\n\n"
        "<i>Если у вас старая версия Windows или возникают проблемы с работой программы, скачайте и установите <a href='https://aka.ms/vs/17/release/vc_redist.x86.exe'>Microsoft Visual C++ Redistributable</a> и <a href='https://dotnet.microsoft.com/'>Microsoft .NET 6.0 Desktop Runtime</a></i>\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=win10_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "MacOS"
@router.callback_query(F.data == "os_macos")
async def instruction_macos(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики" загрузки
    
    # Временный ключ
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "💻 Настройка <b>Rumbush VPN</b> на MacOS через HAPP:\n"
        "<i>HAPP работает только на Mac с процессорами Apple (M1/M2/M3)</i>\n\n"
        "1️⃣ Скачайте <a href='https://clck.ru/3TP7i2'>HAPP</a> и установите\n\n"
        "2️⃣ Запустите приложение и скопируйте ключ доступа (нажмите 1 раз по ключу):\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ В приложении нажмите на значок \"+\" в правом нижнем углу, чтобы добавить новое подключение, и выберите \"<b>Добавить из буфера</b>\"\n\n"
        "4️⃣ Выберите нужную локацию и включите подключение\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=macos_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Windows 7"
@router.callback_query(F.data == "os_win7")
async def instruction_win7(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики"
    
    # Временный ключ
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "💻 Настройка <b>Rumbush VPN</b> на Windows 7 через HAPP:\n\n"
        "1️⃣ Скачайте и установите приложение <a href='https://clck.ru/3TPmJV'>HAPP</a>\n\n"
        "2️⃣ Запустите его <b>от имени администратора</b> и скопируйте ключ доступа (нажмите 1 раз по ключу):\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ При первом запуске появится окно с вводом ключа, вставьте туда скопированный ключ и нажмите \"<b>Поехали</b>\"\n\n"
        "4️⃣ После добавления ключа появится список локаций и основные кнопки. Выберите нужную локацию и нажмите на неё\n\n"
        "5️⃣ Если Вам необходим <b>VPN для Discord, Игр и т.п</b>, то внизу нажмите \"<b>TUN</b>\", а если только для браузера \"<b>Proxy</b>\"\n\n"
        "6️⃣ Нажмите на большую кнопку включения и дождитесь подключения к серверам.\n\n"
        "<i>Если у вас старая версия Windows или возникают проблемы с работой программы, скачайте и установите <a href='https://aka.ms/vs/17/release/vc_redist.x86.exe'>Microsoft Visual C++ Redistributable</a> и <a href='https://dotnet.microsoft.com/'>Microsoft .NET 6.0 Desktop Runtime</a></i>\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=win7_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Linux"
@router.callback_query(F.data == "os_linux")
async def instruction_linux(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики" загрузки
    
    # Временный ключ
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "🐧 Настройка <b>Rumbush VPN</b> на Linux через HAPP:\n\n"
        "1️⃣ Скачайте и установите приложение <a href='https://clck.ru/3TPmVj'>HAPP</a>\n\n"
        "2️⃣ Запустите его <b>от имени администратора</b> и скопируйте ключ доступа (нажмите 1 раз по ключу):\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ При первом запуске появится окно с вводом ключа, вставьте туда скопированный ключ и нажмите \"<b>Поехали</b>\"\n\n"
        "4️⃣ После добавления ключа появится список локаций и основные кнопки. Выберите нужную локацию и нажмите на неё\n\n"
        "5️⃣ Если Вам необходим <b>VPN для Discord, Игр и т.п</b>, то внизу нажмите \"<b>TUN</b>\", а если только для браузера \"<b>Proxy</b>\"\n\n"
        "6️⃣ Нажмите на большую кнопку включения и дождитесь подключения к серверам.\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=linux_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Huawei"
@router.callback_query(F.data == "os_huawei")
async def instruction_huawei(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики"
    
    # Временный ключ
    vpn_key = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    
    text = (
        "📱 Настройка <b>Rumbush VPN</b> на HUAWEI через HAPP:\n\n"
        "1️⃣ Скачайте APK у нас - <a href='https://clck.ru/3TPmod'>HAPP</a>\n\n"
        "2️⃣ Запустите приложение, скопируйте ключ доступа (нажмите 1 раз по ключу) или нажмите на кнопку ниже \"Подключить\":\n\n"
        f"<code>{vpn_key}</code>\n\n"
        "3️⃣ В приложении <b>HAPP</b> нажмите \"+\" и выберите \"<b>Вставить из буфера обмена</b>\"\n\n"
        "4️⃣ Выберите нужную локацию и включите VPN\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=huawei_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Android TV"
@router.callback_query(F.data == "os_android_tv")
async def instruction_android_tv(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики"
    
    text = (
        "🤖 Настройка <b>Rumbush VPN</b> на Android TV через HAPP:\n\n"
        "1️⃣ Откройте <a href='https://play.google.com/store'>Google Play Маркет</a> и введите в поиске HAPP или скачайте APK <a href='https://clck.ru/3TPmod'>HAPP</a> на флешку\n\n"
        "2️⃣ Для продолжения потребуется устройство с камерой, на котором уже установлено приложение <b>HAPP</b> с добавленной подпиской\n\n"
        "3️⃣ Откройте приложение <b>HAPP</b> на устройстве с камерой, нажмите \"+\" и выберите \"<b>QR-код</b>\"\n\n"
        "4️⃣ Отсканируйте <b>QR-код</b>, который отображается на телевизоре, затем выберите подписку и нажмите \"<b>Отправить</b>\"\n\n"
        "5️⃣ Если окно не закрылось автоматически после нажатия \"<b>Отправить</b>\", нажмите кнопку \"<b>пропустить</b>\" — должен будет открыться основной интерфейс\n\n"
        "6️⃣ Выберите нужную локацию и нажмите кнопку \"<b>подключение</b>\" и выдайте все необходимые разрешения\n\n"
    )
    
    await safe_edit(callback,
        text=text,
        reply_markup=android_tv_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
    # Обработка выбора устройства "Apple TV"
@router.callback_query(F.data == "os_apple_tv")
async def instruction_apple_tv(callback: types.CallbackQuery):
    await callback.answer() # Снимаем "часики"
    
    text = (
        "apple tv Настройка <b>Rumbush VPN</b> на Apple TV через HAPP:\n\n"
        "1️⃣ Откройте <a href='https://apps.apple.com/'>AppStore</a> и введите в поиске <b>Happ - Proxy Utility for TV</b>\n\n"
        "2️⃣ Для продолжения потребуется устройство с камерой, на котором уже установлено приложение <b>HAPP</b> с добавленной подпиской\n\n"
        "3️⃣ Откройте приложение <b>HAPP</b> на устройстве с камерой, нажмите \"+\" и выберите \"<b>QR-код</b>\"\n\n"
        "4️⃣ Отсканируйте <b>QR-код</b>, который отображается на телевизоре, затем выберите подписку и нажмите \"<b>Отправить</b>\"\n\n"
        "5️⃣ Если окно не закрылось автоматически после нажатия \"<b>Отправить</b>\", нажмите кнопку \"<b>пропустить</b>\" — должен будет открыться основной интерфейс\n\n"
        "6️⃣ Выберите нужную локацию и нажмите кнопку \"<b>подключение</b>\" и выдайте все необходимые разрешения\n\n"
    )
    await safe_edit(callback,
        text=text,
        reply_markup=apple_tv_setup_kb,
        parse_mode="HTML",
        link_preview_options=types.LinkPreviewOptions(is_disabled=True) 
    )
