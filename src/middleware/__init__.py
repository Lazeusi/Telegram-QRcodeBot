from .register import RegisterMiddleware



from src.logger import get_logger

log = get_logger()


def setup_middlewares(dp):
    try:
        dp.message.middleware(RegisterMiddleware())
    except Exception as e:
        log.error(f"We got an error: {e}")