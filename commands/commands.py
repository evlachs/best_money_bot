from aiogram.types.bot_command import BotCommand

DEFAULT_COMMANDS = [
    BotCommand('main_screen', 'переход на главный экран'),
    BotCommand('chat', 'переход в чат'),
    BotCommand('info', 'правила и оферта'),
    BotCommand('help', 'возможности бота')
]


async def set_default_commands(dp):
    await dp.bot.set_my_commands(DEFAULT_COMMANDS)
