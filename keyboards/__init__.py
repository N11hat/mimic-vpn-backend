# Этот файл делает папку keyboards/ пакетом Python и
# переэкспортирует все клавиатуры наружу.
# Благодаря ему в других файлах можно писать:
#   from keyboards import main_menu_kb
# вместо:
#   from keyboards.main import main_menu_kb

from keyboards.main import main_menu_kb, cabinet_kb, connect_kb
from keyboards.subscription import sub_balance_kb, tariffs_kb
from keyboards.topup import top_up_kb, top_up_presets_kb
from keyboards.setup import (
    android_setup_kb,
    ios_setup_kb,
    win10_setup_kb,
    macos_setup_kb,
    win7_setup_kb,
    linux_setup_kb,
    huawei_setup_kb,
    android_tv_setup_kb,
    apple_tv_setup_kb,
)
