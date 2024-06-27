import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.dispatcher import filters
import time
from aiogram import Bot
import asyncio
from aiogram import types, exceptions


from db import *
timeout = aiohttp.ClientTimeout(total=60)
session = aiohttp.ClientSession(timeout=timeout)
AdminID = 6587289494
ChaneDB = "-1002094268618"
ChaneMovie = "-1001557014193"
# Bot tokenini o'zgartiring
API_TOKEN = "7131296605:AAHQ6ZLsz0zsbwzLZIurqbwEUS9jpO1DTKQ"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class OrderStates(StatesGroup):
    add_admin = State()
    code_movie = State()
    add_reklama = State()
    add_chanel = State()
    posts = State()
    edit_url_chanel = State()


# admindi tekshirish
def is_admin(chat_id):
    admins = view_admin_bot_table()
    chat_ids = [tup[1] for tup in admins]
    chat_ids.append(AdminID)
    return chat_id in chat_ids


def inline_buttons(channels):
    markup = InlineKeyboardMarkup(row_width=1)
    for i, channel in enumerate(channels, start=1):
        chanel_url = InlineKeyboardButton(f"{i} - {channel[2]}", url=channel[3])
        markup.row(chanel_url)
    markup.row(InlineKeyboardButton("✅ A'zo bo'ldim", callback_data="subdone"))

    return markup


@dp.callback_query_handler(lambda call: call.data == "subdone")
async def check_sub(callback: types.CallbackQuery):
    chat_ids = view_chanel_bot_table()
        
    for chat_id in chat_ids:
        if "https://" in chat_id[1]:
            print("instagram")
        else:
            check_sub_channel = await bot.get_chat_member( chat_id=chat_id[1], user_id=callback.from_user.id )
            
            if check_sub_channel.status == "left":
                await bot.answer_callback_query(
                    callback_query_id=callback.id,
                    text="❌ Kechirasiz,  kanalga azo bo'lmadingiz",
                    show_alert=True,
                )
                return

    increment_all_chanel_bot_counts()
    await callback.message.answer(
        f"<b>👋 Assalomu alaykum {callback.from_user.first_name}, kino kodini yuboring.</b>",
        parse_mode="HTML",
    )
    
    await bot.delete_message(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id
    )



@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    result = view_user_bot_table_id(message.chat.id)

    if result or (result and str(result[0][1]) == str(message.chat.id)):
        print("mavjud")
    else:
        insert_user_bot_row(message.chat.id, message.chat.first_name)

    await message.answer(
        f"👋 Assalomu aleykum {message.from_user.first_name}!\n\n"
        f"🍿 Botimiz orqali siz o'zingizga kerakli kinoni yuklab ko'rishishingiz mumkin.\n\n"
        f"📊 Bot buyruqlari:\n"
        f"/start - Botni yangilash ♻️\n"
        f"/dev - Bot dasturchisi 👨‍💻\n"
        f"/help - Bot qo'llanmasi 📑\n\n"
        f"#️⃣ Kinoni kod orqali yuklashingiz ham mumkin. Marhamat, kino kodini yuboring:"
    )


@dp.message_handler(lambda message: message.text.isdigit())
async def handle_admin_button(message: types.Message):
    
    chanel = (view_chanel_bot_table())
    for channel in chanel:
        chat_id = channel[1]
        if "https://" in chat_id:
            print("Instagram")
        else:
            try:
                chat_member = await bot.get_chat_member(chat_id=int(chat_id), user_id=message.chat.id)
                if chat_member.status == "left":
                    return await message.answer(
                        "❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.",
                        reply_markup=inline_buttons(chanel),)
            except Exception as e:
                print(f"Error occurred while checking channel {chat_id}: {e}")

    chanel = view_chanel_bot_table()
    movie_info = view_movie_id(message.text)
    
    if movie_info:
        keyBot = types.InlineKeyboardMarkup()
        keyBot.row(types.InlineKeyboardButton(text="👨‍💻 Admin bilan bog'lanish", url="https://t.me/feruz_mamatov"))
        keyBot.row(types.InlineKeyboardButton(text="🔁 Boshqa kinolar", url="https://t.me/kinofilim_tv"))
        
        await bot.copy_message(chat_id=message.chat.id, from_chat_id=ChaneDB, message_id=movie_info[0][1], reply_markup=keyBot)
    else:
        await message.answer(f"📛 {message.text} kodli kino mavjud emas!")


# dasturchi
@dp.message_handler(commands=["dev"])
async def dev(message: types.Message):
    keyBot = types.InlineKeyboardMarkup()
    keyBot.row(
        types.InlineKeyboardButton(
            text="👨‍💻 Bot dasturchisi", url="https://t.me/feruz_mamatov"
        )
    )
    keyBot.row(
        types.InlineKeyboardButton(text="🔁 Boshqa botlar", url="https://t.me/feruz_mamatov")
    )

    await message.answer(
        "<b>👨‍💻 Botimiz dasturchisi:</b> <a href='https://t.me/feruz_mamatov'>@feruz_mamatov</a>\n\n"
        "<i>🤖 Sizga ham shu kabi botlar kerak bo‘lsa bizga buyurtma berishingiz mumkin. Sifatli botlar tuzib beramiz.</i>\n\n",
        reply_markup=keyBot,
        parse_mode="HTML",
    )


# yordam
@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    keyBot = types.InlineKeyboardMarkup()
    keyBot.row(
        types.InlineKeyboardButton(
            text="🔎 Kino kodlarini qidirish", url="https://t.me/kinofilim_tv"
        )
    )

    await message.answer(
        "<b>📊 Botimiz buyruqlari:</b>\n/start - Botni yangilash ♻️\n\n/dev - Bot dasturchisi 👨‍💻\n/help - Bot buyruqlari 🔁\n\n"
        "<b>🤖 Ushbu bot orqali kinolarni osongina qidirib topishingiz va yuklab olishingiz mumkin. Kinoni yuklash uchun kino kodini yuborishingiz kerak. Barcha kino kodlari pastdagi kanalda jamlangan.</b>",
        reply_markup=keyBot,
        parse_mode="HTML",
    )


# admin panel
@dp.message_handler( lambda message: message.text in ["admin", "a", "panel", "p", "◀️ Ortga qaytish"])
async def send_admin_panel(message: types.Message):
    buttons = [
        ["📊 Statistika"],
        ["🎬 Kinoni ko'rish", "👨‍💼 Adminlar"],
        ["💬 Kanallar", "✍️ Post xabar"],
        ["🚪 Paneldan chiqish"],
    ]
    panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in buttons:
        panel.row(*[types.KeyboardButton(text) for text in row])
    if is_admin(message.chat.id):
        await message.answer(
            "<b>👨🏻‍💻 Boshqaruv paneliga xush kelibsiz.</b>\n\n<i>Nima  ish bajaramiz?</i>",
            reply_markup=panel,
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "❌ <i>Siz admin emassiz, shuningdek bu buyruqni ishlatishingiz mumkin emas.</i>",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )



@dp.message_handler(lambda message: message.text == "💬 Kanallar")
async def handle_chanels(message: types.Message):
    if is_admin(message.chat.id):
        chanel = view_chanel_bot_table()

        callback_data = CallbackData("chanel_list", "id_chanel")

        # Klaviatura yaratish
        keyboard = InlineKeyboardMarkup(row_width=4)
        text = "💬 Kanallar Ro'yxati\n\n"
        i = 0
        for admin in chanel:
            i += 1
            text += f"{i} ) {admin[2]} || Qo'shildi {admin[4]} ta" + "\n"
            button_text = f"{i}"
            callback_data_value = callback_data.new(id_chanel=admin[0])
            button = types.InlineKeyboardButton(button_text, callback_data=callback_data_value)

            if i % 6:
                keyboard.insert(button
                )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
            else:
                keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
        add_chanel_button = types.InlineKeyboardButton(
            "➕ Kanal qo'shish", callback_data="add_chanel"
        )
        # "Admin qo'shish" tugmasini klaviaturaga qo'shish
        keyboard.add(add_chanel_button)
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        # Foydalanuvchi admin emasligi haqida xabarni yuboring
        await message.answer(
            "❌ <i>Siz admin emassiz, shuningdek bu buyruqni ishlatishingiz mumkin emas.</i>",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )

chanel_callback = CallbackData("chabel_delete", "id_chanel", "action")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("chanel_list"))
async def handle_unique_action(callback_query: types.CallbackQuery):
    callback_data = callback_query.data
    id_chanel = callback_data.replace("chanel_list:", "")
    chanel = view_chanel_bot_table_id(id_chanel)  # Assuming this returns a list of tuples

    # Create keyboard
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Define buttons with the appropriate callback data
    delete_button = InlineKeyboardButton(
        "❌ O'chirish", 
        callback_data=chanel_callback.new(id_chanel=chanel[0][0], action="delete")
    )
    edit_button = InlineKeyboardButton(
        "🔗 URL ozgartrish", 
        callback_data=chanel_callback.new(id_chanel=chanel[0][0], action="edit")
    )

    back_button = InlineKeyboardButton(
        "⬅️ Ortga qaytish", 
        callback_data="close_chanel"
    )
    
    keyboard.add(delete_button, edit_button)
    keyboard.add(back_button)

    # Send the message
    await bot.send_message(
        callback_query.message.chat.id, 
        f"💬 Kanal {chanel[0][2]}", 
        reply_markup=keyboard
    )
    # Delete the old message
    await bot.delete_message(
        callback_query.message.chat.id, 
        callback_query.message.message_id
    )




@dp.callback_query_handler( lambda callback_query: callback_query.data.startswith("close_chanel")
)
async def handle_unique_action(callback_query: types.CallbackQuery):
    # Ma'lumotlar bazasidan adminlar ro'yxatini olish
    chanels = view_chanel_bot_table()

    # CallbackData obyektini yaratish
    callback_data = CallbackData("chanel_list", "id_chanel")

    # Klaviatura yaratish
    keyboard = InlineKeyboardMarkup(row_width=4)
    text = "💬 Kanallar Ro'yxati\n\n"
    i = 0
    for chanel in chanels:
        i += 1
        text += f"{i} ) {chanel[2]}" + "\n"
        button_text = f"{i}"
        callback_data_value = callback_data.new(id_chanel=chanel[0])
        button = InlineKeyboardButton(button_text, callback_data=callback_data_value)
        if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
            keyboard.insert(
                button
            )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
        else:
            keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi

    # "Admin qo'shish" tugmasini klaviaturaga qo'shish
    add_admin_button = InlineKeyboardButton(
        "➕ Kanal qo'shish", callback_data="add_chanel"
    )
    keyboard.add(add_admin_button)

    # Foydalanuvchiga adminlar ro'yxatini yuborish
    await bot.send_message(
        callback_query.message.chat.id, text, parse_mode="HTML", reply_markup=keyboard
    )
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )






@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("chabel_delete"))
async def handle_unique_action(callback_query: types.CallbackQuery):

    callback_data = callback_query.data
    id_chanels = callback_data.replace("chabel_delete:", "")

    if ":delete" in id_chanels:
        id_chanel = callback_data.replace("chabel_delete:", "").replace(":delete", "")
        admin = delete_chanel_bot_row(id_chanel)
        if admin == True:
            chanels = view_chanel_bot_table()
            callback_data = CallbackData("chanel_list", "id_chanel")
            keyboard = InlineKeyboardMarkup(row_width=4)
            text = "✅ Kanal muvaffaqiyatli o'chirildi\n\n💬 Kanallar Ro'yxati\n\n"
            i = 0
            for chanel in chanels:
                i += 1
                text += f"{i} ) {chanel[2]}" + "\n"
                button_text = f"{i}"
                callback_data_value = callback_data.new(id_chanel=chanel[0])
                button = InlineKeyboardButton(
                    button_text, callback_data=callback_data_value
                )
                if i % 6:
                    keyboard.insert(button) 
                else:
                    keyboard.row(button)


            add_admin_button = InlineKeyboardButton("➕ Kanal qo'shish", callback_data="add_chanel")
            keyboard.add(add_admin_button)

            await bot.send_message(
                callback_query.message.chat.id,
                text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            await bot.delete_message(
                callback_query.message.chat.id, callback_query.message.message_id
            )
    else:
        id_chanel = callback_data.replace("chabel_delete:", "").replace(":edit", "")
        global  ChanelID
        ChanelID = id_chanel
        buttons = [
            "◀️ Ortga qaytish",
        ]
        panel = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for button_text in buttons:
            panel.add(button_text)

        await bot.send_message(
            callback_query.message.chat.id,
            f"Yangi URL yuboring",
            parse_mode="HTML",
            reply_markup=panel
        )
        await bot.delete_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )   
        await OrderStates.edit_url_chanel.set()

# admin qo'shish
@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("add_chanel")
)
async def handle_unique_action(callback_query: types.CallbackQuery):
    # Klaviatura tugmalari
    buttons = [
        "◀️ Ortga qaytish",
    ]
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_text in buttons:
        panel.add(KeyboardButton(button_text))

    await bot.send_message(
        callback_query.message.chat.id,
        "❗️ Eslatma URL kiritsangiz majburiy obuna ishlamaydi majburiy obuna faqat Gruh yoki Kanal ID sini kiritsangiz ishlaydi!\n\n🆔 Kanal ID si yoki URL kiriting",
        reply_markup=panel,
        parse_mode="HTML",
    )
    await OrderStates.add_chanel.set()
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )


@dp.message_handler(state=OrderStates.edit_url_chanel, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    if message.text == "◀️ Ortga qaytish":
        if is_admin(message.chat.id):
            buttons = [
                ["📊 Statistika"],
                ["🎬 Kinoni ko'rish", "👨‍💼 Adminlar"],
                ["💬 Kanallar", "✍️ Post xabar"],
                ["🚪 Paneldan chiqish"],
            ]
            panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for row in buttons:
                panel.row(*[types.KeyboardButton(text) for text in row])
           
            await message.answer("Nima ish bajaramiz?", parse_mode="HTML", reply_markup=panel)
            await state.finish()
    else:
       result = update_channel_bot_url(ChanelID, message.text)
       if result == True:
            buttons = [
                ["📊 Statistika"],
                ["🎬 Kinoni ko'rish", "👨‍💼 Adminlar"],
                ["💬 Kanallar", "✍️ Post xabar"],
                ["🚪 Paneldan chiqish"],
            ]
            panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for row in buttons:
                panel.row(*[types.KeyboardButton(text) for text in row])
            await message.answer(f"✅ URL muvafaqiyatli o'zgartirildi", parse_mode="HTML", reply_markup=panel)
            await state.finish()


    
@dp.message_handler(state=OrderStates.add_chanel, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    if "https://" in message.text:
            insert_chanel_bot_row(message.text, "Obuna bo'ling", message.text)
            await state.finish()
            admins = view_chanel_bot_table()
            # CallbackData obyektini yaratish
            callback_data = CallbackData("chanel_list", "id_chanel")
            # Klaviatura yaratish
            keyboard = InlineKeyboardMarkup(row_width=4)
            text = "Kanallar Ro'yxati\n\n"
            i = 0
            for admin in admins:
                i += 1
                text += f"{i} ) {admin[2]}" + "\n"
                button_text = f"{i}"
                callback_data_value = callback_data.new(id_chanel=admin[0])
                button = types.InlineKeyboardButton(
                    button_text, callback_data=callback_data_value
                )
                if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                    keyboard.insert(
                        button
                    )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
                else:
                    keyboard.row(
                        button
                    )  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
            add_admin_button = types.InlineKeyboardButton(
                "➕ Kanal qo'shish", callback_data="add_chanel"
            )
            # "Admin qo'shish" tugmasini klaviaturaga qo'shish
            keyboard.add(add_admin_button)
            return await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        
    try:
        chat = await bot.get_chat(str(message.text))
        if chat.invite_link:
            insert_chanel_bot_row(chat.id, chat.title, chat.invite_link)

            admins = view_chanel_bot_table()

            # CallbackData obyektini yaratish
            callback_data = CallbackData("chanel_list", "id_chanel")

            # Klaviatura yaratish
            keyboard = InlineKeyboardMarkup(row_width=4)
            text = f"✅ <b>{chat.title}</b> Kanallar ro'yxatiga qo'shildi \n\n💬 Kanallar Ro'yxati\n\n"
            i = 0
            for admin in admins:
                i += 1

                text += f"{i} ) {admin[2]}" + "\n"
                button_text = f"{i}"
                callback_data_value = callback_data.new(id_chanel=admin[0])
                button = types.InlineKeyboardButton(
                    button_text, callback_data=callback_data_value
                )
                if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                    keyboard.insert(
                        button
                    )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
                else:
                    keyboard.row(
                        button
                    )  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
            add_admin_button = types.InlineKeyboardButton(
                "➕ Kanal qo'shish", callback_data="add_chanel"
            )
            # "Admin qo'shish" tugmasini klaviaturaga qo'shish
            keyboard.add(add_admin_button)
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
            await state.finish()
        else:
            return await message.answer("❌ Xatolik ushun Kanal botni admin qilmagan")
    except Exception as e:
        if message.text == "◀️ Ortga qaytish":
            await state.finish()
            admins = view_chanel_bot_table()
            # CallbackData obyektini yaratish
            callback_data = CallbackData("chanel_list", "id_chanel")
            # Klaviatura yaratish
            keyboard = InlineKeyboardMarkup(row_width=4)
            text = "Kanallar Ro'yxati\n\n"
            i = 0
            for admin in admins:
                i += 1
                text += f"{i} ) {admin[2]}" + "\n"
                button_text = f"{i}"
                callback_data_value = callback_data.new(id_chanel=admin[0])
                button = types.InlineKeyboardButton(
                    button_text, callback_data=callback_data_value
                )
                if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                    keyboard.insert(
                        button
                    )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
                else:
                    keyboard.row(
                        button
                    )  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
            add_admin_button = types.InlineKeyboardButton(
                "➕ Kanal qo'shish", callback_data="add_chanel"
            )
            # "Admin qo'shish" tugmasini klaviaturaga qo'shish
            keyboard.add(add_admin_button)
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await message.answer(f"❌ Xatolik ushun Kanal botni admin qilmagan {e}")


@dp.message_handler(lambda message: message.text == "👨‍💼 Adminlar")
async def handle_admin_button(message: types.Message):
    if is_admin(message.chat.id):
        admins = view_admin_bot_table()
        # CallbackData obyektini yaratish
        callback_data = CallbackData("admin_list", "id_admin")

        # Klaviatura yaratish
        keyboard = InlineKeyboardMarkup(row_width=4)
        text = "👨‍💼 Adminlar Ro'yxati\n\n"
        i = 0
        for admin in admins:
            i += 1
            text += f"{i} ) {admin[2]}" + "\n"
            button_text = f"{i}"
            callback_data_value = callback_data.new(id_admin=admin[0])
            button = types.InlineKeyboardButton(
                button_text, callback_data=callback_data_value
            )
            if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                keyboard.insert(
                    button
                )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
            else:
                keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
        add_admin_button = types.InlineKeyboardButton(
            "➕ Admin qo'shish", callback_data="add_admin"
        )
        # "Admin qo'shish" tugmasini klaviaturaga qo'shish
        keyboard.add(add_admin_button)
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        # Foydalanuvchi admin emasligi haqida xabarni yuboring
        await message.answer(
            "❌ <i>Siz admin emassiz, shuningdek bu buyruqni ishlatishingiz mumkin emas.</i>",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )


# id admin click bo'lganda
@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("admin_list")
)
async def handle_unique_action(callback_query: types.CallbackQuery):
    # Callback tugmasi orqali yuborilgan ma'lumotni olish

    callback_data = callback_query.data
    id_admin = callback_data.replace("admin_list:", "")  # "admin_list:" kısmını kaldır
    admin = view_admin_bot_table_id(id_admin)

    # CallbackData obyektini yaratish
    callback_data = CallbackData("admin_delete", "id_admin")
    # Tarqatma (keyboard) yaratish
    keyboard = InlineKeyboardMarkup(row_width=2)
    # Birinchi tugmani yaratish
    delete_button = types.InlineKeyboardButton(
        "❌ O'chirish", callback_data=callback_data.new(id_admin=admin[0][0])
    )
    # Ikkinchi tugmani yaratish
    back_button = types.InlineKeyboardButton(
        "⬅️ Ortga qaytish", callback_data="close_admin"
    )
    # Tarqatmaga tugmalarni qo'shish
    keyboard.add(delete_button, back_button)
    # Xabarni yuborish
    await bot.send_message(
        callback_query.message.chat.id,
        f"👨‍✈️ Admin {admin[0][2]}",
        reply_markup=keyboard,
    )
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )


# close admin
@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("close_admin")
)
async def handle_unique_action(callback_query: types.CallbackQuery):
    # Ma'lumotlar bazasidan adminlar ro'yxatini olish
    admins = view_admin_bot_table()

    # CallbackData obyektini yaratish
    callback_data = CallbackData("admin_list", "id_admin")

    # Klaviatura yaratish
    keyboard = InlineKeyboardMarkup(row_width=4)
    text = "👨‍💼 Adminlar Ro'yxati\n\n"
    i = 0
    for admin in admins:
        i += 1
        text += f"{i} ) {admin[2]}" + "\n"
        button_text = f"{i}"
        callback_data_value = callback_data.new(id_admin=admin[0])
        button = InlineKeyboardButton(button_text, callback_data=callback_data_value)
        if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
            keyboard.insert(
                button
            )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
        else:
            keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi

    # "Admin qo'shish" tugmasini klaviaturaga qo'shish
    add_admin_button = InlineKeyboardButton(
        "➕ Admin qo'shish", callback_data="add_admin"
    )
    keyboard.add(add_admin_button)

    # Foydalanuvchiga adminlar ro'yxatini yuborish
    await bot.send_message(
        callback_query.message.chat.id, text, parse_mode="HTML", reply_markup=keyboard
    )
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )


# delete admin
@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("admin_delete")
)
async def handle_unique_action(callback_query: types.CallbackQuery):

    callback_data = callback_query.data
    id_admin = callback_data.replace(
        "admin_delete:", ""
    )  # "admin_list:" kısmını kaldır
    admin = delete_admin_bot_row(id_admin)
    if admin == True:
        # Ma'lumotlar bazasidan adminlar ro'yxatini olish
        admins = view_admin_bot_table()
        # CallbackData obyektini yaratish
        callback_data = CallbackData("admin_list", "id_admin")

        # Klaviatura yaratish
        keyboard = InlineKeyboardMarkup(row_width=4)
        text = "✅ Admin muvaffaqiyatli o'chirildi\n\n👨‍💼 Adminlar Ro'yxati\n\n"
        i = 0
        for admin in admins:
            i += 1
            text += f"{i} ) {admin[2]}" + "\n"
            button_text = f"{i}"
            callback_data_value = callback_data.new(id_admin=admin[0])
            button = InlineKeyboardButton(
                button_text, callback_data=callback_data_value
            )
            if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                keyboard.insert(
                    button
                )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
            else:
                keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi

        # "Admin qo'shish" tugmasini klaviaturaga qo'shish
        add_admin_button = InlineKeyboardButton(
            "➕ Admin qo'shish", callback_data="add_admin"
        )
        keyboard.add(add_admin_button)

        # Foydalanuvchiga adminlar ro'yxatini yuborish
        await bot.send_message(
            callback_query.message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await bot.delete_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )


# admin qo'shish
@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("add_admin")
)
async def handle_unique_action(callback_query: types.CallbackQuery):
    # Klaviatura tugmalari
    buttons = [
        "◀️ Ortga qaytish",
    ]
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_text in buttons:
        panel.add(KeyboardButton(button_text))

    await bot.send_message(
        callback_query.message.chat.id,
        "Adminning ID sini kriting",
        reply_markup=panel,
        parse_mode="HTML",
    )
    await OrderStates.add_admin.set()
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )


@dp.message_handler(state=OrderStates.add_admin, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    try:
        chat = await bot.get_chat(message.text)
        insert_admin_bot_row(chat.id, chat.first_name)
        admins = view_admin_bot_table()
        # CallbackData obyektini yaratish
        callback_data = CallbackData("admin_list", "id_admin")

        # Klaviatura yaratish
        keyboard = InlineKeyboardMarkup(row_width=4)
        text = f"✅ <b>{chat.first_name}</b> Adminlar ro'yxatiga qo'shildi \n\n👨‍💼 Adminlar Ro'yxati\n\n"
        i = 0
        for admin in admins:
            i += 1
            text += f"{i} ) {admin[2]}" + "\n"
            button_text = f"{i}"
            callback_data_value = callback_data.new(id_admin=admin[0])
            button = types.InlineKeyboardButton(
                button_text, callback_data=callback_data_value
            )
            if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                keyboard.insert(
                    button
                )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
            else:
                keyboard.row(button)  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
        add_admin_button = types.InlineKeyboardButton(
            "➕ Admin qo'shish", callback_data="add_admin"
        )
        # "Admin qo'shish" tugmasini klaviaturaga qo'shish
        keyboard.add(add_admin_button)
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        await state.finish()
    except Exception as e:
        if message.text == "◀️ Ortga qaytish":
            await state.finish()
            admins = view_admin_bot_table()
            # CallbackData obyektini yaratish
            callback_data = CallbackData("admin_list", "id_admin")
            # Klaviatura yaratish
            keyboard = InlineKeyboardMarkup(row_width=4)
            text = "Adminlar ro'yxatiga qo'shildi \n\n👨‍💼 Adminlar Ro'yxati\n\n"
            i = 0
            for admin in admins:
                i += 1
                text += f"{i} ) {admin[2]}" + "\n"
                button_text = f"{i}"
                callback_data_value = callback_data.new(id_admin=admin[0])
                button = types.InlineKeyboardButton(
                    button_text, callback_data=callback_data_value
                )
                if i % 6:  # Agar tugma tagma tugunlarda joylashgan bo'lsa
                    keyboard.insert(
                        button
                    )  # Tagma tugunni qo'shib, yangi tugma qatordan boshlanadi
                else:
                    keyboard.row(
                        button
                    )  # Aks holda, yangi tugma o'z qatoriga qo'shiladi
            add_admin_button = types.InlineKeyboardButton(
                "➕ Admin qo'shish", callback_data="add_admin"
            )
            # "Admin qo'shish" tugmasini klaviaturaga qo'shish
            keyboard.add(add_admin_button)
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await message.answer(
                "❌ Xatolik ushun ID botda mavjud emas", parse_mode="HTML"
            )


# Paneldan chiqish
@dp.message_handler(lambda message: message.text == "🚪 Paneldan chiqish")
async def handle_exit_button(message: types.Message):
    if is_admin(message.chat.id):
        await message.answer(
            "🚪 Siz Admin Paneldan chiqdingiz",
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode="HTML",
        )
    else:
        # Foydalanuvchi admin emasligi haqida xabarni yuboring
        await message.answer(
            "❌ <i>Siz admin emassiz, shuningdek bu buyruqni ishlatishingiz mumkin emas.</i>",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )


# Statistika
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def handle_exit_button(message: types.Message):
    if is_admin(message.chat.id):
        user_bot = len(view_auser_all_bot_table())
        movie = len(view_movie_all_bot_table())
        chanels = len(view_chanel_bot_table())

        text = (
            f"• Jami a’zolar: {user_bot} ta\n"
            f"• Jami kanallar: {chanels} ta\n"
            f"• Barcha kinolar: {movie} ta\n"
        )
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ <i>Siz admin emassiz, shuningdek bu buyruqni ishlatishingiz mumkin emas.</i>",
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )


# ----------------------------------KINOLAR-------------------------------------------------------------
# edit bolganda malumotni saqlaydi
@dp.edited_channel_post_handler(content_types=[types.ContentType.VIDEO])
async def handle_edited_video(message: types.Message, state: FSMContext):
    if str(message.sender_chat.id) == str(ChaneDB):
        update_movie_table_id(message.message_id, message.caption)


# create bo'lganda
@dp.channel_post_handler(content_types=types.ContentType.VIDEO)
async def handle_channel_video(message: types.Message, state: FSMContext):
    if str(message.sender_chat.id) == str(ChaneDB):
        try:
            if message["forward_from_message_id"]:
                await bot.delete_message(
                    chat_id=ChaneDB, message_id=message["message_id"]
                )
                sent_message = await bot.send_message(
                    chat_id=ChaneDB, text="❌ Xatolik, siz videoni Переслано qilgansiz"
                )
                await asyncio.sleep(
                    3
                )  # 3 saniye bekleyin (istediğiniz zaman dilimini buraya yazabilirsiniz)
                await bot.delete_message(
                    chat_id=ChaneDB, message_id=sent_message.message_id
                )
            else:
                eski_metin = (
                    message.caption
                    if message.caption
                    else "Malumotni taxrirlashiz mumkun"
                )
                code_movie = create_movie(message["message_id"], eski_metin)
                yeni_metin = f"🔢 Yuklash kodi: {code_movie}\n\n{eski_metin}"

                test = await bot.edit_message_caption(
                    chat_id=ChaneDB,
                    message_id=message["message_id"],
                    caption=yeni_metin,
                )
                await handle_edited_video(test, state)
        except Exception as e:
            print(f"Xatolik: {e}")


@dp.message_handler(lambda message: message.text == "🎬 Kinoni ko'rish")
async def handle_admin_button(message: types.Message):
    await message.answer(
        "📝 <b><i>Kino kodini yuboring</i></b>",
        parse_mode="HTML",
    )
    await OrderStates.code_movie.set()


@dp.message_handler(state=OrderStates.code_movie, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    try:
        try:
            movie_info = view_movie_id(message.text)
            send_button = types.InlineKeyboardButton(
                text="🔂 Kinoni Kanalga yuborish",
                callback_data=f"send_chanel_{movie_info[0][1]}",
            )
            delete_button = types.InlineKeyboardButton(
                text="❌ Kinoni o'chirish", callback_data=f"delete_{movie_info[0][1]}"
            )
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(delete_button, send_button)
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=ChaneDB,
                message_id=movie_info[0][1],
                reply_markup=keyboard,
            )
            await state.finish()
        except Exception as e:
            await message.answer("❌ Xatolik, Bazada bunday kino topilmadi")
            await state.finish()
    except Exception as e:
        await message.answer("❌ Xatolik, Kino topilmadi")
        await state.finish()


# Kinoni o'chirish
@dp.callback_query_handler(filters.Regexp(r"^delete_"))
async def send_to_channel(callback_query: types.CallbackQuery):
    movie_info = callback_query.data.split("_")
    movie_id = movie_info[1]
    result = delete_movie_row(movie_id)
    if result == False:
        await callback_query.answer("❌ Xatolik! Kino serverda topilmadi", True)
    else:
        await callback_query.answer("Film O'chirildi")
        await bot.delete_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )
        await bot.delete_message(chat_id=ChaneDB, message_id=movie_id)


@dp.callback_query_handler(filters.Regexp(r"^send_chanel_"))
async def send_to_channel(callback_query: types.CallbackQuery):
    movie_info = callback_query.data.split("_")
    movie_id = movie_info[2]
    global MovieID
    MovieID = movie_id
    await bot.send_message(
        callback_query.message.chat.id,
        "Kino uchun <b><i>Trailer</i></b> yoki <b><i>Photo</i></b> yuboring",
        parse_mode="HTML",
    )
    await OrderStates.add_reklama.set()


@dp.message_handler(state=OrderStates.add_reklama, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    movie = view_movie_message_id(MovieID)
    send_button = types.InlineKeyboardButton(
        text="🔂 Kinoni  yuborish", callback_data="sendchanelmovie"
    )
    delete_button = types.InlineKeyboardButton(
        text="❌ Bekor qilish", callback_data="deletemovie"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(delete_button, send_button)
    if message.video:
        await bot.send_video(
            message.chat.id,
            message.video.file_id,
            caption=movie[0][2],
            reply_markup=keyboard,
        )
    elif message.photo:  # if the message contains a photo
        await bot.send_photo(
            message.chat.id,
            message.photo[-1].file_id,
            caption=movie[0][2],
            reply_markup=keyboard,
        )
    else:
        await message.answer(
            "❌ Xatolik qaytadan urunib ko'ring",
            parse_mode="HTML",
        )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "sendchanelmovie")
async def send_channel_movie(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.forward_message(ChaneMovie, chat_id, message_id)
    await callback_query.answer("Film Kanalga yuborildi")
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )


@dp.callback_query_handler(lambda c: c.data == "deletemovie")
async def send_channel_movie(callback_query: types.CallbackQuery):
    await callback_query.answer("Film O'chirildi")
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )

# -------------------------------- POST ----------------------------
@dp.message_handler(lambda message: message.text == "✍️ Post xabar")
async def handle_admin_button(message: types.Message):
    await message.answer("Xabar matnini kriting")
    await OrderStates.posts.set()

@dp.message_handler(state=OrderStates.posts, content_types=types.ContentTypes.ANY)
async def process_media(message: types.Message, state: FSMContext):
    # Assuming 'chat_id' contains the target chat ID where you want to forward the message
    send_button = types.InlineKeyboardButton(
        text="🔂 Xabarni  yuborish", callback_data="send_post"
    )
    delete_button = types.InlineKeyboardButton(
        text="❌ Bekor qilish", callback_data="deletepost"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(delete_button, send_button)
    
    if message.text:
        await bot.send_message(message.chat.id, message.text, reply_markup=keyboard)
    elif message.photo:
         
        # Forwarding the last photo in the message with its caption and the inline keyboard
        await bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=message.caption, reply_markup=keyboard)
    elif message.video:
      
        # Forwarding the video message with its caption and the inline keyboard
        await bot.send_video(message.chat.id, message.video.file_id, caption=message.caption, reply_markup=keyboard)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "deletepost")
async def send_channel_movie(callback_query: types.CallbackQuery):
    await callback_query.answer("Post O'chirildi")
    await bot.delete_message(
        callback_query.message.chat.id, callback_query.message.message_id
    )
    
@dp.callback_query_handler(lambda c: c.data == "send_post")
async def send_channel_movie(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    
    yuborildi = 0
    yuborilmadi = 0
    
    start_time = time.time()
    users = view_auser_all_bot_table()  # Assuming this function retrieves user data
    for user in users:
        try:
            user_id_to_check = user[1]
            if user_id_to_check is not None:
                await bot.forward_message(user_id_to_check, chat_id, message_id)
                yuborildi += 1
                await bot.send_message("-1002128963767", f"Xabar yuborildi {yuborildi}")
                print(f"Xabar yuborildi {yuborildi}")
                await asyncio.sleep(5)
            else:
                yuborilmadi += 1
                await bot.send_message("-1002128963767", f"Xatolik! Xabar yuborilmadi {yuborilmadi}")
                print(f"Xatolik! Xabar yuborilmadi {yuborilmadi}")
                await asyncio.sleep(5)
        except exceptions.RetryAfter as e:
            await asyncio.sleep(e.timeout)
            await bot.send_message("-1002128963767", f"Flood control chiqqan. Yuborishni keyinroq urinib ko'ring.")
            print(f"Flood control chiqqan. Yuborishni keyinroq urinib ko'ring. {yuborilmadi}")
        except Exception as e:
            yuborilmadi += 1
            await bot.send_message("-1002128963767", f"Xatolik! Xabar yuborilmadi {e}")
            print(f"Xatolik! Xabar yuborilmadi {e} {yuborilmadi}")
            await asyncio.sleep(5)

    # End time
    end_time = time.time()

    # Total time taken
    total_time_seconds = end_time - start_time
    total_time_minutes = total_time_seconds // 60
    remaining_seconds = total_time_seconds % 60

    await bot.send_message(chat_id, f"Xabarlar yuborildi: {yuborildi} ta\nXatoliklar: {yuborilmadi} ta \nXabar yuborishning vaqti: {total_time_minutes:.0f} daqiqa va {remaining_seconds:.2f} soniya")


if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)
