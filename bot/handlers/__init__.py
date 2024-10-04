from bot.dispatcher import dp
from bot.handlers.advertisement import add_router
from bot.handlers.announcement import announcement
from bot.handlers.main import main_router
from bot.handlers.updateandsendmovie import movie_router


dp.include_routers(*[
    main_router,
    movie_router,
    add_router,
    announcement
])