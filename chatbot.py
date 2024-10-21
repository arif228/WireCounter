import telebot
from PIL import Image
import numpy as np
import io
import cv2



bot = telebot.TeleBot("7715029163:AAG4coB9rwQh4JuIcovGXgKfX8guoWxQwX0")          # Задаём токен

image = None

@bot.message_handler(commands=['start'])                                         # При получении команды /start
def message(message):
    bot.send_message(message.chat.id, "Жду фотку провода")


@bot.message_handler(func=lambda message: True,content_types=['photo'])         #  При получении фотографии
def default_command(message):
    global image
    image = message.photo[-1]                                                    # -1 означает наибольшее разрешение
    file_info = bot.get_file(image.file_id)
    file_bytes = bot.download_file(file_info.file_path)                             # Получаем файл в виде байтового объекта
    image_bit = Image.open(io.BytesIO(file_bytes))                                    # Открываем изображение из байтового потока
    image = np.array(image_bit)                                                      # Преобразуем изображение в массив NumPy
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)                                   # Преобразуем цветовое пространство из BGR в RGB (PIL по умолчанию использует RGB, а OpenCV BGR)
    bot.send_message(message.chat.id, "Принял")

bot.infinity_polling()


print("готово")