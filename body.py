from telegram.ext import (Updater, CommandHandler, Filters, MessageHandler, CallbackContext)
from telegram import Update
import logging
import face_recognition
import os


# Initializating /start command

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey! U can send me a photo and i will tell u how\
                                                                     many people on it! Give it a try!")


# Processing incoming pictures from Users. If there any people on pictures - keeping them saved, if not - removing them

def picture(update: Update, context: CallbackContext):
    file_id = update.message.photo[-1]
    new_file = context.bot.get_file(file_id)
    downloaded = new_file.download()
    image = face_recognition.load_image_file(downloaded)
    face_location = face_recognition.face_locations(image)
    if face_location:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='There is a {} people on that picture!'.format(len(face_location)))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='There is no people on that picture')
        os.remove(downloaded)


def main():
    # Creating an Updater and Dispatcher

    updater = Updater(token=token_number, use_context=True)
    dispatcher = updater.dispatcher
    # Setting up a loggin module

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Register Command Handler and Massage Handler in the Dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    picture_handler = MessageHandler(Filters.photo, picture)
    dispatcher.add_handler(picture_handler)

    # Running our telegram bot
    updater.start_polling()


if __name__ == '__main__':
    main()
