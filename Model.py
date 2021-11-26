import re, sys, json, configparser,os
import sqlite3 as sql
from typing import Dict, Tuple
from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from .windows_creator import *
from .translator import translator
import notify2
from pathlib import Path
from .preferences import *


def replace_variable_value(item, text):
    re_text = eval(text)
    if type(re_text) in [list, tuple, set]:
        re_text = list(re_text)
        re_text = [ str(i) for i in  re_text ]
        re_text = ''.join(list(re_text))

    return re_text






class INSAPP(object):

    def __init__(self, app_name, translateable_labels_and_buttons,app_file_type, app_logo ,  preferences_call_btn = 'PREFERENCES_ACTION'):
        
        notify2.init(app_name)
        self.translateable_labels   = translateable_labels_and_buttons
        self.app_name               = app_name
        self.app_logo               = os.path.join(os.path.join(os.path.dirname( __file__ )),'..',app_logo)
        self.qss_style              = ''
        self.app_file_type          = app_file_type
        
        self.UI_file                = 'main.ui'
        self.pyqt5_app              = QtWidgets.QApplication(sys.argv)
        MainWindow                  = QtWidgets.QMainWindow()
        self.UI                     = uic.loadUi(self.UI_file, MainWindow)
        self.UI.setWindowTitle(app_name)
        self.UI.setStyleSheet(self.qss_style)

        self.translator             = translator(self)
        self.translate              = self.translator.translate
        self.preferences_call_btn   = getattr(self.UI, preferences_call_btn)

        
        self.preferences_call_btn.triggered.connect(lambda: open_preferences_window(self))
        

    def run(self):
        loading_window(self)

        self.pyqt5_app.exec_()

    def run_main_window(self):

        for item in self.listed_items:
            setattr(self, item.__name__ , item(INSApp = self ))

        self.UI.show()
            

        



        
        

class Item(object):

    

    def __init__(self, fields, model):
        self.model = model
        for var in fields.keys():
            setattr(self, var , fields[var] )


    def __str__(self):
        
        return replace_variable_value(self, self.model.view_name)


    def get(self, field):
        field_obj = getattr(self, field)
        return getattr(field_obj, field_obj.Get_UI_Value_Function )()

    def delete(self):
        ansower = QtWidgets.QMessageBox.question(self.model.INSApp.UI , self.model.INSApp.translate('Delete Confirm') , self.model.INSApp.translate('Are you sure do you want to delete')+' '+  str(self) +'?')

        if ansower==QtWidgets.QMessageBox.Yes:
            db_connection = sql.connect(self.Model.INSApp.database_path)
            db_connection.execute(f''' DELETE from {self.Model.DBTableName} where id = {self.id} ''')
            db_connection.commit() 
            db_connection.close()
            self.Model.objects.remove(self)
            
            self.model.ui_list.takeItem(self.model.ui_list.row(self.ui_obj))
            
        

    def save(self, call_on_edit = False):
        db_connection = sql.connect(self.Model.INSApp.database_path)

        #get old data as dict
        cursor        = db_connection.cursor()
        data          = cursor.execute(f'''SELECT * FROM {self.model.DBTableName}  where id = {self.id} ''')
        columns       = [ i[0] for i in data.description]
        old_data      = [ i for i in data ][0]
        old_data      = {columns[i]: old_data[i] for i in range(len(columns)) }

        new_data = {}
        for field in self.model.fields.keys():
            if field !=None :
                value =  getattr(self, field)

                if value == None:
                    value = '""'
                elif type(value) in [list, set, dict, tuple]:
                    if self.model.fields[field].field_type == 'ManyToManyField':
                        value =  getattr(self, field,'_data')

                    value = json.dumps(value)
                db_connection.execute(f''' UPDATE {self.model.DBTableName} set {field} = ? where id = {self.id} ''', [value,])
                new_data[field] = value

        db_connection.commit() 
        db_connection.close()
        self.ui_obj.setText(self.__str__())
        if self.model.on_edit != None and call_on_edit:
            self.model.on_edit(old_data = old_data, new_data = new_data )
        


class Model(object):

    
    view_name           = ' f" {item.model.__class__.__name__} object ({item.id})"'
    add_conditions      = {}
    on_add              = None
    on_edit             = None
    on_delete           = None
    search_bar          = None

    def __init__(self, INSApp):
        
        #fields      = []
        self.objects     = []
        self.DBTableName = self.__class__.__name__
        
        self.INSApp      = INSApp
        self.check_db_table()
        self.create_items_objects()
        

        #connections
        if self.add_button != None:
            self.add_button.clicked.connect(lambda: create_item_window(self.INSApp, self))

        if self.delete_button != None:
            self.delete_button.clicked.connect(self.delete_selected)

        if self.ui_list != None:
            self.ui_list.itemDoubleClicked.connect(edit_item_window)

        if self.search_bar != None:
            self.search_bar.textChanged.connect(self.search)

            
        


    def search(self, text):
        self.ui_list.clear()
        if text !='':
            text_words = set(text.split(' '))
            if '' in text_words:
                text_words.remove('')

            for item_object in self.objects:
                obj_data = list(vars(item_object).values())
                for i in range(len(obj_data)):
                    if type(obj_data[i]) == dict:
                        obj_data[i] = ''
                        obj_data += [ str(b) for b in list(obj_data[i].values())]

                    elif type(obj_data[i]) in [list, set, tuple]:
                        if len(obj_data[i])>0:
                            if type(obj_data[i][0]) == dict:
                                for item in obj_data[i]:
                                    obj_data[i] = ''
                                    obj_data += [ str(b) for b in list(item.values())]

                        else:
                            obj_data += [ str(b) for b in list(obj_data[i])]
                                
                            obj_data[i] = ''

                    elif type(obj_data[i]) == str:
                        try:
                            bit = json.loads(obj_data[i])
                            if type(bit) == dict:
                                obj_data += list(bit.values())
                            else:
                                obj_data += list(bit)
                            obj_data[i] = ''
                        except:
                            pass
                    else:
                        obj_data[i] = str(obj_data[i])


                
                obj_words = set(' '.join(obj_data).split(' ')) #convert all data to words set
                if text_words.issubset(obj_words):
                    self.add_item_to_list(item_object)
                
                else:
                    ex_status = True
                    for word in text_words:
                        obj_words_str = [ str(i) for i in obj_words if type(i) in [float,bool,str,int,list, tuple, dict, set] ]
                        if word not in ' '.join(obj_words_str):
                            ex_status = False

                    if ex_status:
                        self.add_item_to_list(item_object)
        
        else:
            for item_object in self.objects:
                self.add_item_to_list(item_object)

        


    def check_db_table(self):
        db_connection = sql.connect(self.INSApp.database_path)
        tabels = db_connection.execute("SELECT name FROM sqlite_master WHERE type ='table'").fetchall()
        tabels = [ i[0] for i in tabels ]

        if not self.DBTableName in tabels:
            columns = ['id integer primary key autoincrement',]
            for field in self.fields.keys():
                columns.append(f'{field} { self.fields[field].data_base_type }')
            columns = ','.join(columns)
            db_connection.execute(f"create table { self.DBTableName } ({columns})")

        db_connection.close()

    def create_items_objects(self):

        db_connection = sql.connect(self.INSApp.database_path)
        columns = list(self.fields.keys())+['id',]
        str_columns = ','.join(columns)
        data = db_connection.execute(f"SELECT {str_columns} from {self.DBTableName} ").fetchall()
        
        
        for item in data:
            data = {}
            for i in range(len(item)):
                data[columns[i]] = item[i]
                if columns[i]!='id' :
                    if self.fields[columns[i]].field_type == 'OneToOneField':
                        try:
                            item_id = int(item[i])
                        except:
                            item_id = None
                        data[columns[i]+'__obj'] = getattr( self.INSApp, self.fields[columns[i]].model).get(id=item_id)
                        
                    elif self.fields[columns[i]].field_type == 'ManyToManyField':
                        try:
                            data[columns[i]] = json.loads(item[i].replace("'",'"'))
                        except:
                            pass
                        



            data['view_name'] = self.view_name
            data['Model'] = self
            item_obj = Item(data, self)
            self.objects.append(item_obj)
            self.add_item_to_list( item_obj)

        db_connection.close()

    def add_item_to_list(self, obj):
        item = QtWidgets.QListWidgetItem()
        item.setData(2,str(obj))
        item.setData(6,obj)
        obj.ui_obj = item
        self.ui_list.addItem(item)


    def filter(self, dict_fields = None , **fields):
        if dict_fields != None:
            fields = dict_fields

        returned_item = []
        fields_keys     = list(fields.keys())
        for item in self.objects:
            fields_values   = list(fields.values())
            item_values     = []

            for key in range(len(fields_keys)):
                var_name = fields_keys[key]

                if var_name[-4:] == '__in':
                    if vars(item)[var_name[:-4]] in fields[var_name] : 
                        fields_values[key] = vars(item)[var_name[:-4]]

                    item_values.append(vars(item)[var_name[:-4]])

                else:
                    item_values.append(vars(item)[var_name])

            if item_values == list(fields_values):
                returned_item.append(item)

        return returned_item


    def get(self, **fields):
        returned_items = self.filter(dict_fields =fields)
        if len(returned_items) >0:
            returned_items = returned_items[0]
        else:
            returned_items = None

        return returned_items

    def temporary_item(self):
        data = {}
        for bit in self.fields:
            data[bit] = self.fields[bit]

        return Item(data, self)



    def create(self,dict_inner_data = None,  **inner_data):
        if dict_inner_data != None:
            inner_data = dict_inner_data

        print(inner_data)

        fields  = []
        data    = []
        for field in inner_data.keys():
            fields.append(str(field))


            if self.fields[field].TYPE in [ [list, dict, set] ,]:
                inner_data[field] = json.dumps(inner_data[field])
            
            inner_data[field] = str(inner_data[field])

            data.append(str(inner_data[field]))

        for not_set_field in set(self.fields.keys()).difference(set(inner_data.keys())):

            field_obj = self.fields[not_set_field]
            

            data.append(str(field_obj.default))


        fields_str = ', '.join(list(fields) + list(set(self.fields.keys()).difference(set(inner_data.keys()))))
        data_str = ', '.join(data)
        

        db_connection = sql.connect(self.INSApp.database_path)

        data_str_f = ', '.join((['?',]* len(data)))

        item = db_connection.execute(f"""INSERT INTO {self.DBTableName} ({fields_str}) values ({data_str_f}) """, data )
        db_connection.commit()
        db_connection.close()



        data_n = { fields[i]:data[i] for i in range(len(data)) }
        data_n['view_name'] = self.view_name
        data_n['id'] = int(item.lastrowid)
        data_n['Model'] = self
        itam_object = Item(data_n, self)
        self.objects.append(itam_object)
        self.add_item_to_list(itam_object)

        if self.on_add!=None:
            self.on_add(itam_object)

        return itam_object

        
    def delete_selected(self):
        item = self.ui_list.currentItem()
        item_data = vars(item.data(6))
        if item != None:
            item.data(6).delete()

            if self.on_delete != None:
                self.on_delete(data = item_data)







        
                

