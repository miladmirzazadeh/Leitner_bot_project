import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
# print(list_of_hashes)

class SpreadSheetHandler():
    def __init__(self, api_file_name, gfile_name="Saved translations", sheet_name="Saved translations"):
        self.api_file_name = api_file_name
        self.gfile_name = gfile_name
        self.sheet_name = sheet_name
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('{}.json'.format(api_file_name), self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(gfile_name)[sheet_name]
        self.current_row = 1

    def update_sheet(self):
        self.sheet = self.client.open(self.gfile_name)[self.sheet_name]

    def new_card(self):
        word = self.sheet.cell(self.current_row, 0)
        translation = self.sheet.cell(self.current_row, 1)
        return(word, translation)

    def change_card_state(self, was_correct= True):
        ''' description: this function will change remaining_day and box_num after user answer it
                 move card to box1 if answer was wrong
                 move to next box (add days depending on box_num) '''
        pass
    def iterate_on_sheet(self):
        pass
    def reduce_remaining_day(self, row_no):
        pass



