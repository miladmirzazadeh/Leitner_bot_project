import pandas as pd
import numpy as np

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging

from spreadsheet import SpreadSheetHandler

class Controller():
    '''
    Description:    Every instances of this class will manage a specific user works.
                    this object is an intermediary between CmdAnalyzer and userDB
    '''
    def __init__(self, user_id, api_file_name = "client_secret.json", gfile_name= "Saved translations", sheet_name= "Saved translations" ):
        self.db_handler = SpreadSheetHandler(api_file_name, gfile_name, sheet_name)
        self.current_day = 1 # TODO:    read from spreadsheet in some way
        self.user_id = user_id
        self.current_word = None
        self.current_translation = None

    def show_message(self, message, reply_markup):
        CommandAnalyzer.show_to_user(self.user_id, message, reply_markup)

    def prepare_new_card(self):
        self.current_word, self.current_translation = self.db_handler.new_card()

    def show_new_card(self):
        self.prepare_new_card()
        keyboard = [[InlineKeyboardButton("دیدن جواب", callback_data='show_translation')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        self.show_message(self.current_word, reply_markup)

    def show_answer(self):
        keyboard = [[InlineKeyboardButton("بلد بودم", callback_data='correct_answer')],
                    [InlineKeyboardButton("بلد نبودم", callback_data='wrong_answer')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        self.show_message(self.current_translation, reply_markup)

    def finishing_day(self):
        self.db_handler.current_row = 1
    # TODO: change db_handler day


    def update_db(self):
        self.db_handler.update_sheet()





class CommandAnalyzer():
    user_objects = {}
    user_chatid = {}
    user_controller_objects = {}
    user_pass = {"milad":"milad0816", "nastaran": "nas12352"}
    def create_user():
        pass
    def pass_to_controller():
        pass

    def handle_new_message(update, context, callback=False):
        print("yesssssssssssssss")
        # if callback:
        #     user_id = update.callback_query.from_user.username
        # else:
        #     user_id = update.message.from_user.username
        # if user_id not in CommandAnalyzer.user_controller_objects:
        #     CommandAnalyzer.user_controller_objects[user_id] = Controller(user_id)
        #     CommandAnalyzer.user_chatid[user_id] = update.message.chat_id
        # user_obj = CommandAnalyzer.user_controller_objects[user_id]
        message = update.message.text

        if message == "next":
            print("start")
            CommandAnalyzer.show_to_user(update, "hiii")
            # print("sent")


    def show_to_user(update, text, user_id="milad"):
        CommandAnalyzer.bot.send_message(chat_id=update.message.chat_id, text=text)





    def edit_message_text(message, reply_markup=None):
        # print(message)
        # print(reply_markup)
        try:
            if CommandAnalyzer.callback:
                CommandAnalyzer.update.callback_query.edit_message_text(message, reply_markup=reply_markup)
            else:
                # print(message)
                CommandAnalyzer.update.message.edit_text(message, reply_markup=reply_markup)

        except:
            CommandAnalyzer.show_message("ظاهرا ورودی اشتباهی به سیستم داده شده")





