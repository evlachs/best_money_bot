import logging

from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from messages.messages import MESSAGES
from conf.config import TOKEN, CHANNEL_ID, ADMIN_ID
from commands.commands import set_default_commands
from keyboard.keyboards import user_keyboard, admin_keyboard, confirm_post_keyboard, location_keyboard,\
    make_a_post_keyboard, cancel_photo_keyboard, operations_keyboard, operations_chat_keyboard, info_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    title = State()
    description = State()
    photo = State()
    grn_to_rub = State()
    transfer_abroad = State()


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


@dp.message_handler(commands=['start', 'help'])
async def start_message(message: types.Message):
    keyboard = user_keyboard
    if message.from_user.id in ADMIN_ID:
        keyboard = admin_keyboard
    await bot.send_message(
        message.chat.id,
        MESSAGES['start'].format(message.from_user.username),
        reply_markup=keyboard
    )
    with open('data/users_id.txt', 'r+') as file:
        if not str(message.from_user.id) in file.read().split('\n'):
            file.seek(0, 2)
            file.write(str(message.from_user.id)+'\n')


@dp.message_handler(commands=['main_screen', 'chat', 'info'])
async def commands_handler(message: types.Message):
    if message.get_command() == '/main_screen':
        await bot.send_message(message.chat.id, MESSAGES['main_screen'])
    elif message.get_command() == '/chat':
        await bot.send_message(message.chat.id, MESSAGES['chat'])
    elif message.get_command() == '/info':
        await bot.send_message(message.chat.id, MESSAGES['info'], reply_markup=info_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'info')
async def delete_links_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, MESSAGES['info'], reply_markup=info_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'rules')
async def delete_links_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_document(callback_query.from_user.id, open('info/rules.pdf', 'rb'))


@dp.callback_query_handler(lambda c: c.data == 'security')
async def delete_links_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_document(callback_query.from_user.id, open('info/security.pdf', 'rb'))


@dp.callback_query_handler(lambda c: c.data == 'about_us')
async def delete_links_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_document(callback_query.from_user.id, open('info/about_us.pdf', 'rb'))


@dp.message_handler(commands=['post'])
async def make_a_post(message: types.Message):
    if message.from_user.id not in ADMIN_ID:
        return
    await Form.title.set()
    await bot.send_message(message.from_user.id, MESSAGES['set_title'])


@dp.callback_query_handler(lambda c: c.data == 'post')
async def delete_links_handler(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMIN_ID:
        return
    await bot.answer_callback_query(callback_query.id)
    await Form.title.set()
    await bot.send_message(callback_query.from_user.id, MESSAGES['set_title'])


@dp.message_handler(state=Form.title)
async def process_gender(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['title'] = f'<b>{message.text}</b>\n\n'
    await Form.description.set()
    await bot.send_message(message.from_user.id, MESSAGES['set_description'])


@dp.message_handler(state=Form.description)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await Form.photo.set()
    await bot.send_message(message.from_user.id, MESSAGES['set_photo'], reply_markup=cancel_photo_keyboard)


@dp.message_handler(state=Form.photo, content_types='photo')
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await bot.send_message(message.from_user.id, MESSAGES['confirm_post'])
    await bot.send_photo(
        message.from_user.id,
        data['photo'],
        f"{data['title']}{data['description']}",
        reply_markup=confirm_post_keyboard
    )


@dp.callback_query_handler(lambda c: c.data == 'cancel_photo', state=Form.photo)
async def confirm_post(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        data['photo'] = None
    await bot.send_message(callback_query.from_user.id, MESSAGES['confirm_post'])
    await bot.send_message(
        callback_query.from_user.id,
        f"{data['title']}{data['description']}",
        reply_markup=confirm_post_keyboard
    )


@dp.callback_query_handler(lambda c: c.data == 'cancel', state='*')
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    current_state = await state.get_state()
    if current_state is None:
        return
    elif current_state in ['Form:title', 'Form:description', 'Form:photo']:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, MESSAGES['canceled'], reply_markup=make_a_post_keyboard)
    else:
        await state.finish()
        await bot.send_message(callback_query.from_user.id, MESSAGES['canceled'])


@dp.callback_query_handler(lambda c: c.data == 'confirm_post', state='*')
async def confirm_post(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    async with state.proxy() as data:
        photo = data['photo']
        msg = f"{data['title']}{data['description']}"
    if photo:
        await bot.send_photo(CHANNEL_ID, photo, msg, reply_markup=operations_chat_keyboard)
    else:
        await bot.send_message(CHANNEL_ID, msg, reply_markup=operations_chat_keyboard)
    await state.finish()
    await bot.send_message(callback_query.from_user.id, MESSAGES['post_confirmed'])


@dp.callback_query_handler(lambda c: c.data == 'operations')
async def cancel_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, MESSAGES['choose_operation'], reply_markup=operations_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'grn_to_rub')
async def process_gender(callback_query: types.CallbackQuery):
    await Form.grn_to_rub.set()
    await bot.send_message(callback_query.from_user.id, MESSAGES['grn_to_rub'])


@dp.callback_query_handler(lambda c: c.data == 'transfer_abroad')
async def process_gender(callback_query: types.CallbackQuery):
    await Form.transfer_abroad.set()
    await bot.send_message(callback_query.from_user.id, MESSAGES['transfer_abroad'])


@dp.message_handler(state=[Form.grn_to_rub, Form.transfer_abroad])
async def cancel_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_data'] = f'имя: {message.from_user.full_name}\nid: {message.from_user.id}\n' \
                            f'url: {message.from_user.url}\nusername: @{message.from_user.username}'
        data['application_id'] = message.message_id
    await bot.send_message(message.from_user.id, MESSAGES['share_contact'], reply_markup=location_keyboard)


@dp.message_handler(content_types=['contact'], state=[Form.grn_to_rub, Form.transfer_abroad])
async def default(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact_id'] = message.message_id
    await state.finish()
    current_state = await state.get_state()
    if current_state == 'Form:grn_to_rub':
        for admin in ADMIN_ID:
            try:
                await bot.forward_message(admin, message.from_user.id, data['application_id'])
                await bot.forward_message(admin, message.from_user.id, data['contact_id'])
                await bot.send_message(admin, data['user_data'])
            except:
                continue
    else:
        for admin in ADMIN_ID:
            try:
                await bot.forward_message(admin, message.from_user.id, data['application_id'])
                await bot.forward_message(admin, message.from_user.id, data['contact_id'])
                await bot.send_message(admin, data['user_data'])
            except:
                continue
    await bot.send_message(message.from_user.id, MESSAGES['application_sent'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
