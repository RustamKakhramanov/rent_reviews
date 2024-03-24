from app.apps.core.bot.middlewares.main import MainMiddleware
from app.apps.core.bot.middlewares.language import LanguageMiddleware
from app.apps.core.bot.middlewares.has_tariff import HasTariffMiddleware

route_middlewares = (
    HasTariffMiddleware,
    MainMiddleware,
    LanguageMiddleware
)
