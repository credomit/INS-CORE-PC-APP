from . import DB_Mode
from PyQt5.QtWidgets import *


class DataController(object):
    
    DB_PATH = ''


    def __init__(self, app, MODE = 'LOCAL') :
        self.MODES_NAMES = {
        'LOCAL' : DB_Mode.Local,
        }
        self.APP = app
        self.MODE_Name = MODE
        

    def init_mode(self):
        self.MODE = self.MODES_NAMES[self.MODE_Name](DB_PATH= self.DB_PATH, Data_controller= self)
        pass    

    def get_model_data(self, model):
        return self.MODE.get_model_data(model)

    def add_item(self, model, data):
        return self.MODE.add_item(model, data)

    def edit_item(self, item_obj):
        self.MODE.edit_item(item_obj)