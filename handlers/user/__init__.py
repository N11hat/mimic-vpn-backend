from aiogram import Router

from handlers.user.start import router as start_router
from handlers.user.cabinet import router as cabinet_router
from handlers.user.subscription import router as subscription_router
from handlers.user.balance import router as balance_router
from handlers.user.instructions import router as instructions_router

# Главный роутер модуля — включает все дочерние
router = Router()
router.include_router(start_router)
router.include_router(cabinet_router)
router.include_router(subscription_router)
router.include_router(balance_router)
router.include_router(instructions_router)
