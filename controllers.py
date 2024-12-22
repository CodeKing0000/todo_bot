from telebot import types
from views import View
import sqlite3

class Controller:
    def __init__(self, bot):
        self.bot = bot

    def register_handlers(self):
        @self.bot.message_handler(commands=["start", "help"])
        def send_welcome(message):
            self.bot.reply_to(
                message,
                "Добро пожаловать в RecipeBot! Напишите /find чтобы начать",
            )

        @self.bot.message_handler(commands=["find"])
        def r(message):
            msg = self.bot.reply_to(message, "Введите название блюда:")
            self.bot.register_next_step_handler(msg,find)
        def find(message):
            name = message.text
            connection = sqlite3.connect("data.db")
            cursor = connection.execute(
                f""" 
                SELECT recipe,image 
                FROM food 
                WHERE name = '{name}' 
                """
            )
            result = cursor.fetchone()
            if result is not None:
                recipe, image = result
                self.bot.send_message(message.chat.id, f"Рецепт: {recipe}")
                if image:
                    self.bot.send_photo(message.chat.id, image)
            else:
                self.bot.send_message(message.chat.id, "К сожалению, рецепт не найден.")
            connection.commit()
            connection.close()