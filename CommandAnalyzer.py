import pandas as pd
import numpy as np

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging

from spreadsheet import SpreadSheetHandler

class Controller():
    '''
    Description:    Every instances of this class will manage a specific user works.
                    this object is an intermediary between CmdAnalyzer and userDB
    '''
    def __init__(self, user_id):
        # api_file_name = "client_secret", gfile_name= "Saved translations", sheet_name= "Saved translations"
        self.user_id = user_id
        self.db_handler = None
        self.update = None
        self.state = 0
        self.api_file_name = None
        self.gfile_name = None
        self.request = None
        self.callback = False

    def check_user_permission(self):
        allowed_users = CommandAnalyzer.allowed_users_sheet.sheet.col_values(1)
        if self.user_id in allowed_users:
            return(True)
        else:
            return(False)

    def new_message(self, message, callback=False):
        self.callback = callback # to remain that what was the last message
        if message == "/start":
            self.show_message("Welcoming :)")
            if self.check_user_permission():
                self.state = 0
                self.db_handler = None
                self.request = "gather_data"
                self.gather_data()
            else:
                self.show_message("Your telegram id is not allowed\nYou can ask @milad_mirzazadeh for access ")
        elif self.request == "gather_data":
            self.gather_data(message)
        elif self.db_handler == None:
            self.show_message("The Bot is not activated yet. \nYou can activate it by /start")

        else:
            if message == "/show_card":
                self.show_new_card(new_message=True)
            elif message == "show_translation":
                self.show_answer()
            elif message in ["correct_answer", "wrong_answer"]:
                self.check_answer(message)
            elif message == "/remaining":
                self.show_remaining_cards()
            else:
                self.show_message("Didn't understand")


    def gather_data(self, input = None):
        if self.state == 0 :
            self.state = 1
            self.show_message("What is your google_file name?")
        elif self.state == 1 :
            self.gfile_name = input
            self.show_message("Connecting ... ")
            self.gfile_name = input
            self.state = 0
            self.request = None

            try :
                # self.db_handler = SpreadSheetHandler(self, gfile_name=self.gfile_name)
                self.db_handler = SpreadSheetHandler(self, gfile_name=self.gfile_name)
                self.show_message("Connected to the sheet 😍 \nYou can start by /show_card")
            except:
                self.api_file_name = None
                self.gfile_name = None
                self.show_message("There is a problem, and I don't know what it is")




    def show_message(self, message, reply_markup=None, edit=False):
        if not edit:
            CommandAnalyzer.show_to_user(self.user_id, message, reply_markup)
        else:
            CommandAnalyzer.edit_message_text(self.user_id, message, reply_markup)

    def prepare_new_card(self):
        self.current_word, self.current_translation = self.db_handler.new_card()

    def show_new_card(self, new_message=True):
        self.prepare_new_card()
        keyboard = [[InlineKeyboardButton("see translation", callback_data='show_translation')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if self.current_word != "":
            answer_len = len(self.current_translation)
            spaces = "".join([" " for space in range (answer_len)])
            word = "{}  \n--------------- \n {}.".format(self.current_word, spaces)
            self.show_message(word, reply_markup, edit=not new_message)
        else:
            var = self.db_handler.iterate_on_words()
            if var != 0:
                self.show_new_card(new_message=not self.callback)


    def show_answer(self):
        keyboard = [[InlineKeyboardButton("I knew this word 😎", callback_data='correct_answer')],
                    [InlineKeyboardButton("Didn't know this word 🤦‍♂️", callback_data='wrong_answer')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        answer = "{}  \n--------------- \n{}".format(self.current_word, self.current_translation)
        self.show_message(answer, reply_markup, edit=True)


    def check_answer(self, user_answer):

        if user_answer == "correct_answer":
            self.db_handler.change_card_state(was_correct = True)
        elif user_answer == "wrong_answer":
            self.db_handler.change_card_state(was_correct = False)
        else:
            self.show_message("Didn't understand")
        var = self.db_handler.iterate_on_words()
        if var != 0:
            self.show_new_card(new_message=False)

    def show_remaining_cards(self):
        #there are two kinds of cards that should be asked in current day
        #the ones that their remaining day is 0 and the ones buy empty remaining day cell

        # in the local word array
        # in the gfile
        all_cells = np.array(self.db_handler.sheet.get_all_values())
        current_row = self.db_handler.current_file_row - SpreadSheetHandler.batch_size + self.db_handler.current_array_row
        remaining_days = all_cells[current_row:,2]
        remaining_cards = len(remaining_days[np.logical_or(remaining_days =='', remaining_days =='1')])
        self.show_message("{} cards has been remaining for today. \nContinue by /show_card".format(remaining_cards))

    def finishing_day(self):
        self.db_handler.current_file_row = 1
        self.db_handler.current_array_row = 0
        self.db_handler.local_words_array = np.array([])
        self.show_message("No card has remained for today:) \nYou can start next day by /show_card", edit=self.callback)





class CommandAnalyzer():
    allowed_users_sheet = SpreadSheetHandler(gfile_name="leitner_bot_allowed_users")
    user_objects = {}
    user_chatid = {}
    user_controller_objects = {}


    def handle_new_callback(update, context):
        CommandAnalyzer.handle_new_message(update, context, callback=True)

    def handle_new_message(update, context, callback=False):
        if callback:
            user_id = update.callback_query.from_user.username
        else:
            user_id = update.message.from_user.username
        if user_id not in CommandAnalyzer.user_chatid:
            CommandAnalyzer.user_chatid[user_id] = update.message.chat_id
            CommandAnalyzer.user_controller_objects[user_id] = Controller(user_id)

        if callback:
            message = update.callback_query.data
        else:
            message = update.message.text
        CommandAnalyzer.user_controller_objects[user_id].update = update
        CommandAnalyzer.user_controller_objects[user_id].new_message(message, callback)




    def show_to_user(user_id, text, reply_markup = None):
        CommandAnalyzer.bot.send_message(chat_id=CommandAnalyzer.user_chatid[user_id], text=text, reply_markup=reply_markup)





    def edit_message_text(user_id, message="hello", reply_markup=None):
        # try:
        if CommandAnalyzer.user_controller_objects[user_id].callback:
            CommandAnalyzer.user_controller_objects[user_id].update.callback_query.edit_message_text(message, reply_markup=reply_markup)
        else:
            CommandAnalyzer.user_controller_objects[user_id].update.message.edit_text(message, reply_markup=reply_markup)

        # except:
            CommandAnalyzer.user_controller_objects[user_id].show_message("It seems you have entered a wrong input")





