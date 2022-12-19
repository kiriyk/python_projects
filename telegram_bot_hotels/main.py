from bot.bot import bot, bot_handler

from loguru import logger

logger.add('Logs/log.log', level='DEBUG', backtrace=False, catch=False)
bot_handler(bot)

logger.info('Бот запущен!')

bot.infinity_polling(skip_pending=True)

