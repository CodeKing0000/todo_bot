import telebot
import sqlite3

con = sqlite3.connect("ChristmasProject.db")

TOKEN = '7570041216:AAEjllhAk-aOIXO7AE0kugI2MMbAnCrPi4Q'

bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.InlineKeyboardMarkup()

button_1 = telebot.types.InlineKeyboardButton('Продолжить', callback_data='continue')
keyboard1.add(button_1)

keyboard2 = telebot.types.InlineKeyboardMarkup()

button_1 = telebot.types.InlineKeyboardButton('Продолжить', callback_data='continue')
button_2 = telebot.types.InlineKeyboardButton('Готово', callback_data='result')
keyboard2.add(button_1)



@bot.message_handler(commands=['start'])
def handle_command_start(message):
    bot.send_message(message.chat.id, "Привет меня зовут ChristmasBot!", reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def handle_command_help(message):
    bot.send_message(message.chat.id, "Этот бот поможет тебе с заказом продуктов на новый год!")

@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    if callback.data == 'continue':
        bot.send_message(callback.message.chat.id, f"Напишите название продукта: ")
        def message(message):
          global name
          name = message.text
          bot.register_next_step_handler(message, message2)     
        def message2(message):
          global quantity
          quantity = message.text
          bot.send_message(callback.message.chat.id, f"Напишите сколько хотите купить: ")
          bot.register_next_step_handler(message, message3)
        def message3(message):
          global price
          price = message.text
          bot.send_message(callback.message.chat.id, f"Напишите цену продукта: ")
          bot.register_next_step_handler(callback.message, message4, reply_markup=keyboard2)



        def message4(message):
          SQL_UPDATE_TABLE = f"""

          INSERT INTO Orders(name, quantity, price) 
          VALUES 
          ("{name}", "{quantity}","{price}")
        
          """
          con.execute(SQL_UPDATE_TABLE)


          SQL_UPDATE_TABLE1 = f"""

            SELECT price * quantity
            FROM Orders

          """
          con.execute(SQL_UPDATE_TABLE)



        bot.register_next_step_handler(message.chat.id, f"Итого: {price * quantity}")
    
print('Сервер запущен.')

bot.polling(
    non_stop=True, 
    interval=0.5
)

# 7570041216:AAEjllhAk-aOIXO7AE0kugI2MMbAnCrPi4Q