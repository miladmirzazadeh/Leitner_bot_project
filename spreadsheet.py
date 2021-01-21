import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
# use creds to create a client to interact with the Google Drive API
# scope = ['https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#
# client = gspread.authorize(creds)
#
# # Find a workbook by name and open the first sheet
# # Make sure you use the right name here.
# sheet = client.open("saved_words").sheet1
#
# # Extract and print all of the values
# list_of_hashes = sheet.get_all_records()


class SpreadSheetHandler():
    batch_size =10
    word_col = 1
    translation_col = 2
    remaining_day_col = 3
    box_no_col = 4
    wrong_answers_col = 5
    boxes_days_dict = {1:1, 2:2, 3:4, 4:8, 5:15, 6:100}
    def __init__(self, owner_controller=None, api_file_name="client_secret", gfile_name="saved_words"):
        self.owner_controller = owner_controller
        self.api_file_name = api_file_name
        self.gfile_name = gfile_name
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.api_file_name, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.gfile_name).get_worksheet(0)
        self.current_array_row = 0 # np array indexes start with 0
        self.current_file_row = 1 # spreadsheet file indexes start with 1
        self.local_words_array = []


    def update_sheet(self):
        self.sheet = self.client.open(self.gfile_name)[self.sheet_name]

    def new_card(self):
        if len(self.local_words_array) == 0:
            self.get_new_batch()
        if len(self.local_words_array[self.current_array_row]) == 4 and self.local_words_array[self.current_array_row][SpreadSheetHandler.remaining_day_col-1] in ["", "1"]:
            word = self.local_words_array[self.current_array_row][SpreadSheetHandler.word_col-1]
            translation = self.local_words_array[self.current_array_row][SpreadSheetHandler.translation_col - 1]
            return(word, translation)
        else:
            return("", "")

    def change_card_state(self, was_correct= True):
        ''' description: this function will change remaining_day and box_num after user answer it
                 move card to box1 if answer was wrong
                 move to next box (add days depending on box_num) '''

        if was_correct:
            box_no = int(self.local_words_array[self.current_array_row][SpreadSheetHandler.box_no_col-1])
            if(box_no in SpreadSheetHandler.boxes_days_dict):
                box_no += 1
                day_to_add = SpreadSheetHandler.boxes_days_dict[box_no]
                self.local_words_array[self.current_array_row][SpreadSheetHandler.remaining_day_col-1] = str(day_to_add)
                self.local_words_array[self.current_array_row][SpreadSheetHandler.box_no_col-1] = str(box_no)
                # self.sheet.update_cell(self.current_row, SpreadSheetHandler.wrong_answers_col,)

        else:
            self.local_words_array[self.current_array_row][SpreadSheetHandler.remaining_day_col-1] = "1"
            self.local_words_array[self.current_array_row][SpreadSheetHandler.box_no_col - 1] = "1"

    def iterate_on_words(self):
        for i in range(self.current_array_row+1, len(self.local_words_array)):
            if len(self.local_words_array[i]) < 4:
                for q in range(len(self.local_words_array[i]), 4):
                    self.local_words_array[i].append("")
            box_no = self.local_words_array[i][SpreadSheetHandler.box_no_col-1]
            if box_no in ["","1", "2" , "3", "4", "5"]:
                remaining_day = self.local_words_array[i][SpreadSheetHandler.remaining_day_col-1] # we reduce 1 from remaining_day_col because indexes in np array are different with gfile indexes
                if box_no == "":
                    self.local_words_array[i][SpreadSheetHandler.box_no_col-1] = "1"
                if remaining_day in ['', '1']:
                    if remaining_day =='':
                        self.local_words_array[i][SpreadSheetHandler.remaining_day_col - 1] = "1"
                    self.current_array_row = i
                    print(self.current_array_row)
                    return(1)
                else:
                    new_remaining_day = int(remaining_day) - 1
                    self.local_words_array[i][SpreadSheetHandler.remaining_day_col - 1] = str(new_remaining_day)
        return(self.get_new_batch())
    def get_new_batch(self): # and update previous batch in gfile
        print("from", self.current_file_row, "hasd;kfja;sdlkfja;sldkfja;dlkfj;aslkdfja;ldkfja;slkdfj;aslkdfjs;dlfkjas;dlkfjasdf")
        print("getttttttttttttttttttt newwwwwwwwwwwwwwwwwwww")
        self.current_array_row = 0
        arr_len = len(self.local_words_array)
        if arr_len>1:
            self.sheet.update("A{}:D{}".format(self.current_file_row-arr_len, self.current_file_row-1), self.local_words_array) #updating gfile
        batch_size = min(SpreadSheetHandler.batch_size, len(self.sheet.col_values(1))-(self.current_file_row-1))
        print("batch size calculated to :         " , batch_size)
        if batch_size > 0 :
            self.local_words_array = self.sheet.get("A{}:D{}".format(self.current_file_row, self.current_file_row+batch_size-1))
            print("local_words_array changed to : ", self.local_words_array)
            self.current_file_row = self.current_file_row+ batch_size
            return(1)
        else: # end of the file
            self.owner_controller.finishing_day()
            return(0)







    def reduce_remaining_day(self, row_no):
        pass



