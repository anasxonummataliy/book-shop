from aiogram import Router

from .profile import router as profile_router
from .catalog import router as catalog_router
from .info import router as info_router
from .start import router as start_router


router = Router()
router.include_routers(start_router, profile_router, catalog_router, info_router)
