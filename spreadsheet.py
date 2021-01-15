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


class SpreadSheetHandler():
    word_col = 1
    translation_col = 2
    remaining_day_col = 3
    box_no_col = 4
    wrong_answers_col = 5
    boxes_days_dict = {1:1, 2:2, 3:4, 4:8, 5:15, 6:100}
    def __init__(self, owner_controller, api_file_name="client_secret", gfile_name="saved_words"):
        self.owner_controller = owner_controller
        self.api_file_name = api_file_name
        self.gfile_name = gfile_name
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('{}.json'.format(api_file_name), self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.gfile_name).get_worksheet(0)
        self.current_row = 1

    def update_sheet(self):
        self.sheet = self.client.open(self.gfile_name)[self.sheet_name]

    def new_card(self):
        word = self.sheet.cell(self.current_row, SpreadSheetHandler.word_col).value
        translation = self.sheet.cell(self.current_row, SpreadSheetHandler.translation_col).value
        return(word, translation)

    def change_card_state(self, was_correct= True):
        ''' description: this function will change remaining_day and box_num after user answer it
                 move card to box1 if answer was wrong
                 move to next box (add days depending on box_num) '''

        if was_correct:
            box_no = int(self.sheet.cell(self.current_row, SpreadSheetHandler.box_no_col).value)
            if(box_no in SpreadSheetHandler.boxes_days_dict):
                box_no += 1
                day_to_add = SpreadSheetHandler.boxes_days_dict[box_no]
                self.sheet.update_cell(self.current_row, SpreadSheetHandler.remaining_day_col, day_to_add)
                self.sheet.update_cell(self.current_row, SpreadSheetHandler.box_no_col, box_no)

        else:
            self.sheet.update_cell(self.current_row,SpreadSheetHandler.remaining_day_col, 1)
            self.sheet.update_cell(self.current_row,SpreadSheetHandler.box_no_col, 1)

    def iterate_on_sheet(self):
        for i in range(self.current_row+1 , len(self.sheet.col_values(1))+1):
            if self.sheet.cell(i, SpreadSheetHandler.box_no_col).value in ["1", "2" , "3", "4", "5"]:
                cell = self.sheet.cell(i, SpreadSheetHandler.remaining_day_col).value
                if cell in ['', '1']:
                    if cell =='':
                        self.sheet.update_cell(i, SpreadSheetHandler.remaining_day_col, "1")
                    self.current_row = i
                    return(1)
                else:
                    remaining_day = int(cell) - 1
                    self.sheet.update_cell(i, SpreadSheetHandler.remaining_day_col, remaining_day)

        self.owner_controller.finishing_day()
        return (0)






    def reduce_remaining_day(self, row_no):
        pass



