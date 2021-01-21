from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging
from CommandAnalyzer import *

def main():

    updater = Updater("1533725125:AAEtbFSzER39mljSCCKda6ybvpb6K1NrpRY", use_context=True)
    CommandAnalyzer.bot = Bot("1533725125:AAEtbFSzER39mljSCCKda6ybvpb6K1NrpRY")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(["start", "main_menu"], CommandAnalyzer.handle_new_message))
    dp.add_handler(CallbackQueryHandler(CommandAnalyzer.handle_new_callback, pattern=None))

    dp.add_handler(MessageHandler(Filters.text, CommandAnalyzer.handle_new_message))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()


