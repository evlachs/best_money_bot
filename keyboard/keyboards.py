from aiogram import types

operations_button = types.InlineKeyboardButton('перейти к операциям', callback_data='operations')
main_screen_button = types.InlineKeyboardButton('переход на главный экран', url='https://t.me/BestMoneySolution')
chat_button = types.InlineKeyboardButton('переход в чат', url='https://t.me/solution_best_money_flood')
reviews_button = types.InlineKeyboardButton('посмотреть отзывы', url='https://t.me/+vp9cJ0usakI3MDUy')
info_button = types.InlineKeyboardButton('информация', callback_data='info')
make_a_post_button = types.InlineKeyboardButton('создать пост', callback_data='post')
cancel_button = types.InlineKeyboardButton('отмена', callback_data='cancel')
confirm_post_button = types.InlineKeyboardButton('отправить пост', callback_data='confirm_post')
cancel_photo_button = types.InlineKeyboardButton('пост без фото', callback_data='cancel_photo')
grn_to_rub_button = types.InlineKeyboardButton('обмен ГРН на РУБ', callback_data='grn_to_rub')
transfer_abroad_button = types.InlineKeyboardButton('перевод за границу', callback_data='transfer_abroad')
go_to_bot_button = types.InlineKeyboardButton('перейти в бот для совершения операции', url='https://t.me/test_bestapi_bot')
rules_button = types.InlineKeyboardButton('правила и оферта', callback_data='rules')
security_button = types.InlineKeyboardButton('о безопасности', callback_data='security')
about_us_button = types.InlineKeyboardButton('о нас', callback_data='about_us')

location_button = types.KeyboardButton('Поделиться контаком', request_contact=True)

location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(location_button)


user_keyboard = types.InlineKeyboardMarkup()
user_keyboard.add(operations_button).add(main_screen_button).add(chat_button).add(reviews_button).add(info_button)

admin_keyboard = types.InlineKeyboardMarkup()
admin_keyboard.add(operations_button).add(main_screen_button).add(chat_button).add(reviews_button).add(info_button).add(make_a_post_button)

cancel_keyboard = types.InlineKeyboardMarkup()
cancel_keyboard.add(cancel_button)

confirm_post_keyboard = types.InlineKeyboardMarkup()
confirm_post_keyboard.add(confirm_post_button).add(cancel_button)

make_a_post_keyboard = types.InlineKeyboardMarkup()
make_a_post_keyboard.add(make_a_post_button)

cancel_photo_keyboard = types.InlineKeyboardMarkup()
cancel_photo_keyboard.add(cancel_photo_button).add(cancel_button)

operations_keyboard = types.InlineKeyboardMarkup()
operations_keyboard.add(grn_to_rub_button).add(transfer_abroad_button)


operations_chat_keyboard = types.InlineKeyboardMarkup()
operations_chat_keyboard.add(go_to_bot_button)

info_keyboard = types.InlineKeyboardMarkup()
info_keyboard.add(rules_button).add(security_button).add(about_us_button)
