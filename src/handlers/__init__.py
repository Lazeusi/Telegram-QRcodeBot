from .start import router as start_router
from .admin import router as admin_router
from .channel import router as channel_router
from .force_join import router as force_join_router
from .QRcode_handlers.plain_text import router as plain_text_router
from .QRcode_handlers.link import router as link_router

from src.logger import get_logger

log = get_logger()

def setup_handlers(dp):
    try:
        dp.include_router(start_router)
        dp.include_router(admin_router)
        dp.include_router(channel_router)
        dp.include_router(force_join_router)
        dp.include_router(plain_text_router)
        dp.include_router(link_router)
        
    except Exception as e:
        log.error(f"We got an error: {e}")
