
from ctypes.wintypes import PINT
from socket import create_connection
from tkinter import N
from typing import Type
from webbrowser import get
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5 import Qt as PyQt5_Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import  os, json, datetime
from . import configuration_ini
from .frame import FrameWidget
import string, random
from .windows import Form as Core_UI_Form


class Fields(object):

    class Field(object):
        properties_func = None
        default = None
        editable = True
        Base_input_field_size = [110, 27]
        input_field_size = Base_input_field_size
        custom_init = None
        create_connections = None




        def __init__(self, **kwargs ):


            for var in kwargs.keys(): # defind all variabels in kwargs 
                setattr(self, var, kwargs[var])
            
            if self.custom_init != None:
                self.custom_init()


            

        def view(self, UI, Form, field_name, position_index, field_obj = None, gridLayout = True, another_layout = None):
                setattr(UI, field_name, UI.fields[field_name].UI_Field(Form) )
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                self.UI = UI
                self.ui_field.setEnabled(self.editable)
                
                
                if UI.edit_mode:
                    if UI.obj_mode:
                        field_value = UI.fields[field_name].TYPE(getattr(UI.item_obj.data, field_name) )
                    else:

                        field_value = UI.fields[field_name].TYPE(UI.dict_data[field_name])

                    getattr(self.ui_field, UI.fields[field_name].Set_UI_Value_Function )(field_value)

                if gridLayout:
                    UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                else:
                    another_layout.addWidget(self.ui_field, position_index, 1, 1, 1)
                


        def get_data(self):
            try:
                data = getattr( self.ui_field, self.Get_UI_Value_Function)()
            except:
                data = '2002-12-12'

            return data

        def Get_Data(self):
            return ''

        def Get_DB_Data(self):
            return self.Get_Data()


        def On_Add_To_UI(self):

            if self.create_connections:
                self.create_connections()



    class TextField(Field):
        field_type              = 'TextField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QLineEdit
        default                 =  ''

        def Create_UI_Widget(self):
            common_field_design_1(self, QtWidgets.QLineEdit)
            getattr(self.frame, self.name+'_input_field').setClearButtonEnabled(True)
            return self.frame

        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setText(str(data))

        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').text()

    class TextBox(Field):
        field_type              = 'TextBox'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QTextEdit
        default                 =  ''
        def Create_UI_Widget(self):
            common_field_design_2(self, QtWidgets.QTextEdit)
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type',
                    'text-align': 'right',
                },
                {
                    'position'  : [1,0,0,0],
                    'name'      : self.name+'_input_field',
                    'object'    : QtWidgets.QTextEdit,
                    'type'      : 'Qt-type',
                    
                }
            ]
            #FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(self.frame, self.name+'_label').setText(self.label)
            self.frame = self.frame
            return self.frame

        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setPlainText(str(data))

        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').toPlainText()

    class IntegerField(Field):
        field_type              = 'IntegerField'
        TYPE                    = int
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QSpinBox
        default                 =  0
        
        def Create_UI_Widget(self):
            common_field_design_1(self, QtWidgets.QSpinBox)
            getattr(self.frame, self.name+'_input_field').setMaximum(2147483647)

            return self.frame
        
        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setValue(int(data))

        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').value()
     
    class FloatField(Field):
        field_type              = 'FloatField'
        TYPE                    = float
        data_base_type          = 'REAL'
        UI_Field                = QtWidgets.QDoubleSpinBox
        default                 =  0.0
        
        def Create_UI_Widget(self):
            Field = common_field_design_1(self, QtWidgets.QDoubleSpinBox)
            getattr(self.frame, self.name+'_input_field').setDecimals(self.APP.Dicimal_Round)
            getattr(self.frame, self.name+'_input_field').setMaximum(2147483647)

            return Field

        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setValue(float(data))

        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').value()


    class RadioButtonsField(Field):
        field_type              = 'RadioButtonsField'
        TYPE                    = str
        data_base_type          = 'STRING'
        UI_Field                = QtWidgets.QRadioButton
        Get_UI_Value_Function   = 'isChecked'
        Set_UI_Value_Function   = 'setChecked'
        default                 =  False
        properties              = []

        Radio_Buttons           = []


        

        def Create_UI_Widget(self):
            
            self.ui_objects_list = []
            row = 0
            for button in self.Radio_Buttons:
                self.ui_objects_list.append(
                    {
                    'position'  : [row,0,0,0],
                    'name'      : button+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type',
                    'text-align': 'right',
                })
                self.ui_objects_list.append({
                    'position'  : [row,1,0,0],
                    'name'      : button+'_input_field',
                    'object'    : QtWidgets.QRadioButton,
                    'type'      : 'Qt-type',
                })

                row+=1

            FrameW = FrameWidget(self.name, self.ui_objects_list, self.APP)
            FrameW.core_field = self
            for button in self.Radio_Buttons:
                getattr(FrameW, button+'_label').setText(button)
            
            self.frame = FrameW
            return FrameW
            

        def Set_Data(self, data):
            getattr(self.frame, data+'_input_field').setChecked(True)

        def Get_Data(self):
            for button in self.Radio_Buttons:
                if getattr(self.frame, button+'_input_field').isChecked():
                    return button
        
        def status_changed(self):
            for button in self.Radio_Buttons:
                for field in self.Radio_Buttons[button]:
                    self.frame.frame.parentUI.fields[field].frame.frame.setVisible(getattr(self.frame, button+'_input_field').isChecked())

        def create_connections(self):
            for button in self.Radio_Buttons:
                getattr(self.frame, button+'_input_field').clicked.connect(self.status_changed)
            self.status_changed()

            


    class BoolField(Field):
        field_type              = 'BoolField'
        TYPE                    = bool
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QCheckBox
        default                 =  False

        On_True_View            = []
        On_False_View           = []


        

        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QCheckBox)
            getattr(self.frame, self.name+'_input_field').setChecked(bool(self.default))
            return field

        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setChecked(bool(data))

        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').isChecked()




        
        def status_changed(self, status):
            for field in self.On_True_View:
                self.frame.frame.parentUI.fields[field].frame.frame.setVisible(status)

        def create_connections(self):
            getattr(self.frame, self.name+'_input_field').clicked.connect(self.status_changed)
            self.status_changed(getattr(self.frame, self.name+'_input_field').isChecked())

    class DateField(Field):
        field_type              = 'DateField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QDateEdit
        default                 = ''
        properties              = []


        def get_data(self):
            data = self.ui_field.date().toPyDate().isoformat()
            return data

        def Get_Data(self):
            data = getattr(self.frame, self.name+'_input_field').date().toPyDate().isoformat()
            return data
            
        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setDate(datetime.date.fromisoformat(data))

        def view(self, UI, Form, field_name, position_index, field_obj = None, field_gridLayout = None, view_on_main_window = False, gridLayout = True, another_layout = None):
                setattr(UI, field_name, QtWidgets.QDateEdit(Form) )
              
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                self.ui_field.setDisplayFormat('dd/MM/yyyy')
                self.ui_field.setEnabled(self.editable)


                if self.default == None:
                    self.ui_field.setDate(datetime.date.today())
                else:
                    self.ui_field.setDate(self.default)

                if not view_on_main_window and UI.edit_mode:
                    if UI.obj_mode:
                        field_value = str(getattr(UI.item_obj.data, field_name))
                    else:
                        field_value = UI.dict_data[field_name]
                    self.ui_field.setDate(datetime.date.fromisoformat(field_value))

                if not view_on_main_window:
                    if gridLayout:
                        UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                    else:
                        another_layout.addWidget(self.ui_field, position_index, 1, 1, 1)

                else:
                    field_gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)


        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QDateEdit)
            getattr(field, self.name+'_input_field').setDisplayFormat('dd/MM/yyyy')
            getattr(field, self.name+'_input_field').setDate(datetime.date.today())
            return field


    class TimeField(Field):
        field_type              = 'TimeField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QTimeEdit
        default                 = ''
        properties              = []


        def get_data(self):
            data = self.ui_field.time().toPyTime().isoformat()
            return data


        def Get_Data(self):
            data = getattr(self.frame, self.name+'_input_field').time().toPyTime().isoformat()
            return data
            
        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setTime(datetime.time.fromisoformat(data))


        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QTimeEdit)
            getattr(field, self.name+'_input_field').setDisplayFormat('hh:mm AP')
            getattr(field, self.name+'_input_field').setTime(datetime.datetime.now().time())
            return field
            

        def view(self, UI, Form, field_name, position_index, field_obj = None, field_gridLayout = None, view_on_main_window = False, gridLayout = True, another_layout = None):
                setattr(UI, field_name, QtWidgets.QTimeEdit(Form) )
              
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                
                self.ui_field.setEnabled(self.editable)

                if UI.app.UI.Layout_direction == 'RTL':
                    self.ui_field.setDisplayFormat('ap mm:hh')
                else:
                    self.ui_field.setDisplayFormat('hh:mm ap')
                

                if self.default == None:
                    self.ui_field.setTime(datetime.datetime.now().time())
                else:
                    self.ui_field.setTime(self.default)

                if not view_on_main_window and UI.edit_mode:
                    try:
                        if UI.obj_mode:
                            field_value = str(getattr(UI.item_obj.data, field_name))
                        else:
                            field_value = UI.dict_data[field_name]
                    except:
                        field_value = datetime.datetime.now().time().isoformat()
                        
                    self.ui_field.setTime(datetime.time.fromisoformat(field_value))

                if not view_on_main_window:
                    if gridLayout:
                        UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                    else:
                        another_layout.addWidget(self.ui_field, position_index, 1, 1, 1)

                else:
                    field_gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)

    class DateTimeField(Field):
        field_type              = 'DateTimeField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QDateTimeEdit
        default                 = ''
        properties              = []

        def Get_Data(self):
            data = getattr(self.frame, self.name+'_input_field').dateTime().toPyDateTime().isoformat()
            return data
            
        def Set_Data(self, data):
            getattr(self.frame, self.name+'_input_field').setDateTime(datetime.datetime.fromisoformat(data))


        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QDateTimeEdit)
            getattr(field, self.name+'_input_field').setDisplayFormat('dd/MM/yyyy | hh:mm AP')
            getattr(field, self.name+'_input_field').setDateTime(datetime.datetime.now())
            return field
            
    class DropdownField(Field):
        field_type              = 'DropdownField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 = []
        items_list              = []
        subfields               = []
        data_from_DictField     = None
        data_from_function      = None
        properties              = []
        on_change               = None

        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QComboBox)

            if self.data_from_function != None:
                self.items_list = self.data_from_function(self, self.main_ui)

            for item in self.items_list:# set all items
                getattr(field, self.name+'_input_field').addItem(item)

            return field

        def Get_Data(self):
            data = getattr(self.frame, self.name+'_input_field').currentText()
            return data
            
        def Set_Data(self, data):
            try:
                getattr(self.frame, self.name+'_input_field').setCurrentIndex( getattr(self.frame, self.name+'_input_field').findText(data ))
            except:
                pass

        def change_subfields_content(self):
            try:
                current_item = getattr(self.frame, self.name+'_input_field').currentText()
                data = self.items_list.get(current_item)
                for field in self.subfields:
                    ui_object = self.frame.frame.parentUI.fields[field].input_field
                    ui_object.clear()
                    for bit in data:
                        ui_object.addItem(bit)
            except:
                pass

        def create_connections(self):
            if self.subfields != [] and type(self.items_list) == dict:
                getattr(self.frame, self.name+'_input_field').currentIndexChanged.connect(self.change_subfields_content)
            
            self.change_subfields_content()

        def view(self, UI, Form, field_name, position_index, field_obj = None, field_gridLayout = None, view_on_main_window = False, gridLayout = True, another_layout = None):        
                
                
                setattr(UI, field_name , QtWidgets.QComboBox(Form) )
                self.ui_field = vars(UI)[field_name  ]

                self.ui_field.setObjectName(field_name)
                self.ui_field.setEnabled(self.editable)

                for item in self.items_list:# set all items
                    self.ui_field.addItem(item)

                if self.data_from_DictField != None:
                    
                    DictField_obj = UI.model.fields[self.data_from_DictField]
                    current_DF_Text = getattr(UI.pui,self.data_from_DictField ).currentText()
                    
                    for item in DictField_obj.item_dict[current_DF_Text]:# set all items
                        self.ui_field.addItem(item)

                elif self.data_from_function!=None:
                    try:
                        items = self.data_from_function(field = self, main_ui =  UI)

                        if type(items) == dict:
                            
                            for item in items:# set all items
                                self.ui_field.addItem(item, items[item])

                        else:
                            for item in items:# set all items
                                self.ui_field.addItem(item)
                    except Exception as error:
                        print(error)

                    

                if (not view_on_main_window) and UI.edit_mode:# set current item
                    if UI.obj_mode:
                        current_item_text = getattr(UI.item_obj.data,field_name)

                    else:
                        current_item_text = UI.dict_data[field_name]

                    if self.ui_field.findText( current_item_text )>-1:
                        self.ui_field.setCurrentIndex( self.ui_field.findText(current_item_text ))


                if not view_on_main_window:
                    another_layout.addWidget(self.ui_field, position_index, 1, 1, 1)

                else:
                    field_gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)

                    if self.on_change != None:
                        self.ui_field.currentIndexChanged.connect(partial(self.on_change, UI, self.ui_field, ui_loaded = True))
                        return {'on_load_function':[partial(self.on_change, UI, self.ui_field, ui_loaded = False),] }

    class CustomDropdownField(Field):
        field_type              = 'CustomListField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 = []
        list_name               = 'default_list'
        


        def Get_Data(self):
            return getattr(self.frame, self.name+'_input_field').currentText()

        def Set_Data(self, data):
            item_index = getattr(self.frame, self.name+'_input_field').findText(data )
            if item_index != -1:
                
                getattr(self.frame, self.name+'_input_field').setCurrentIndex( item_index)
            else:
                self.add_item(data)
                getattr(self.frame, self.name+'_input_field').addItem(data)
                getattr(self.frame, self.name+'_input_field').setCurrentIndex(getattr(self.frame, self.name+'_input_field').count()-1)


        def Create_UI_Widget(self):
            self.input_field_size        = [self.input_field_size[0]-67, self.input_field_size[1]]

            buttons = [
                {
                    'name'      : self.name+'_add_item_button',
                    'type'      : 'Qt-type',
                    'icon'      : 'add',
                    'UIproperty': {'btn_type': 'add'},
                },
                {
                    'name'      : self.name+'_settings_button',
                    'type'      : 'Qt-type',
                    'icon'      : 'settings',
                    'UIproperty': {'btn_type': 'settings'},
                    
                }
            ]
            
            common_field_design_1(self, QtWidgets.QComboBox, buttons = buttons )
           
            
            current_data = configuration_ini.get_data(file_path=['INSLPCModel','settings.ini'])['CustomLists'].get(self.list_name)
            
            if current_data != None:
                current_data = json.loads(current_data)
            
            self.add_items_to_list()       

            getattr(self.frame, self.name+'_label').setText(self.label)
            self.input_field = getattr(self.frame, self.name+'_input_field')

            return self.frame

        def add_item(self, item):
            current_data = configuration_ini.get_data(file_path=['INSLPCModel','settings.ini'])['CustomLists'].get(self.list_name)
            if current_data == None:
                current_data = []

            else:
                current_data = json.loads(current_data)
            
            current_data.append(item)
            configuration_ini.set_data(file_path=['INSLPCModel','settings.ini'], category = 'CustomLists', variable = self.list_name, value = json.dumps(current_data))
            

        def open_add_item_window(self):            

            def adding_proccess(self):
                item = self.subwindow.ui.item_name.text()
                self.add_item(item)
                getattr(self.frame, self.name+'_input_field').addItem(item)
                getattr(self.frame, self.name+'_input_field').setCurrentIndex(getattr(self.frame, self.name+'_input_field').count()-1)
                self.subwindow.ui.close()



            self.subwindow = Core_UI_Form(None, self.model, None, self.model.INSApp.translate('Add Item'), app=self.model.INSApp, ui_file_path=os.path.join(os.path.dirname( __file__ ), 'UIs', 'add-CustomDropdownField-item.ui'))
            
            self.subwindow.ui.item_name.setPlaceholderText(self.APP.translate('item name...'))

            self.subwindow.ui.add_item.setIcon(self.APP.Styler.get_icon('add'))
            self.subwindow.ui.add_item.setProperty('btn_type','add') 
            self.subwindow.ui.add_item.clicked.connect(partial(adding_proccess, self))
            
            self.subwindow.show()
            

        def add_items_to_list(self):
            current_data = configuration_ini.get_data(file_path=['INSLPCModel','settings.ini'])['CustomLists'].get(self.list_name)
            if current_data == None:
                current_data = []

            else:
                current_data = json.loads(current_data)
            
            getattr(self.frame, self.name+'_input_field').clear()
            for item in current_data:
                getattr(self.frame, self.name+'_input_field').addItem(item)

        def open_items_settings_window(self):            

            

            def edit_list(self):
                data_list = []
                for i in range(0, self.subwindow.ui.items_table.rowCount()-1):
                    print(i, 0)
                    data_list.append(self.subwindow.ui.items_table.item(i, 0).text())
                configuration_ini.set_data(file_path=['INSLPCModel','settings.ini'], category = 'CustomLists', variable = self.list_name, value = json.dumps(data_list))

                self.add_items_to_list()
                self.subwindow.close()

            def remove_item(self):
                for i in self.subwindow.ui.items_table.selectionModel().selectedRows():
                    self.subwindow.ui.items_table.removeRow(i.row())

            def add_item_to_ui_list(self, item):
                self.subwindow.ui.items_table.insertRow(0)
                self.subwindow.ui.items_table.setItem(0, 0,  QtWidgets.QTableWidgetItem(self.model.INSApp.translate('new item')))
                

            self.subwindow = Core_UI_Form(None, self.model, None, self.model.INSApp.translate('Add Item'), app=self.model.INSApp, ui_file_path=os.path.join(os.path.dirname( __file__ ), 'UIs', 'CustomDropdownField-settings.ui'))
            
            self.subwindow.ui.items_table.setProperty('widget_type','scrollarea_widget')
            self.subwindow.ui.items_table.setStyleSheet('border-radius: 20px;')

            self.subwindow.ui.setProperty('form_type', 'subwindow')
            self.subwindow.ui.setStyleSheet(self.APP.currentStyle)
            self.subwindow.ui.setWindowModality(QtCore.Qt.ApplicationModal)
            self.subwindow.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose)


            self.subwindow.ui.save_btn.setIcon(self.APP.Styler.get_icon('save'))
            self.subwindow.ui.save_btn.setProperty('btn_type','save') 
            self.subwindow.ui.save_btn.clicked.connect(partial(edit_list, self))


            self.subwindow.ui.add_btn.setIcon(self.APP.Styler.get_icon('add'))
            self.subwindow.ui.add_btn.setProperty('btn_type','add') 
            self.subwindow.ui.add_btn.clicked.connect(partial(add_item_to_ui_list, self, 'New item'))


            self.subwindow.ui.remove_btn.setIcon(self.APP.Styler.get_icon('delete'))
            self.subwindow.ui.remove_btn.setProperty('btn_type','delete') 
            self.subwindow.ui.remove_btn.clicked.connect(partial(remove_item, self))


            current_data = configuration_ini.get_data(file_path=['INSLPCModel','settings.ini'])['CustomLists'].get(self.list_name)
            if current_data != None:
                current_data = json.loads(current_data)

            self.subwindow.ui.item_font = QFont()
            self.subwindow.ui.item_font.setPointSize(20)
            for i in range(len(current_data)):
                self.subwindow.ui.items_table.insertRow(i)
                self.subwindow.ui.items_table.setItem(i, 0,  QtWidgets.QTableWidgetItem(current_data[i]))
                

            self.subwindow.ui.show()



        def create_connections(self):
            getattr(self.frame, self.name+'_add_item_button').clicked.connect(self.open_add_item_window)
            getattr(self.frame, self.name+'_settings_button').clicked.connect(self.open_items_settings_window)

    class ManyToOneField(Field):
        field_type              = 'ManyToOneField'
        TYPE                    = int
        data_base_type          = 'INT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentData'
        default                 = -1

        def Create_UI_Widget(self):
            field = common_field_design_1(self, QtWidgets.QComboBox)
            
            for item in getattr(self.APP, self.sub_model).objects:# set all items
                getattr(field, self.name+'_input_field').addItem(str(item), item.id)


            return field

        def Get_Data(self):
            data = getattr(self.frame, self.name+'_input_field').currentData()
            if data==None:
                data = 0
            return data

        def Set_Data(self, data):
            ui_field = getattr(self.frame, self.name+'_input_field')
            ui_field.setCurrentIndex(ui_field.findData(str(data)))
            

    class OneToManyField(Field):
        field_type              = 'OneToManyField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        default                 = []

        on_add          = {}
        on_edit         = {}
        on_delete       = {}
        before_add      = {}
        before_save     = {}
        before_delete   = {}

        Table_Name = 'unnamed'

        def custom_init(self):
            self.submodelClass = type(self.Table_Name, (self.INSApp.ModelClass, ), {})
            
            self.submodelClass.fields = self.subfields
            self.submodelClass.extra_DB_columns = ['model_id']
            self.submodelClass.view_name = self.view_name
            
            
            self.submodelClass.on_add              = self.on_add.get('function')
            self.submodelClass.on_edit             = self.on_edit.get('function')
            self.submodelClass.on_delete           = self.on_delete.get('function')
            self.submodelClass.before_add          = self.before_add.get('function')
            self.submodelClass.before_save         = self.before_save.get('function')
            self.submodelClass.before_delete       = self.before_delete.get('function')

            self.INSApp.listed_items.insert(0, self.submodelClass)
            
            

        def Get_Data(self):
            return "[]"

        def get_DB_data(self):
            return "[]"

        def Create_UI_Widget(self):
            self.submodel = getattr(self.INSApp, self.Table_Name)
            buttons = [
                {
                    'name'      : self.name+'_add_item_button',
                    'type'      : 'Qt-type',
                },
                {
                    'name'      : self.name+'_remove_button',
                    'type'      : 'Qt-type',
                    
                }
            ]
            field = common_field_design_2(self, QtWidgets.QListWidget, buttons = buttons)
            self.field = field
            self.submodel.PW_Window = self.main_ui
            #window = getattr(field, self.name+'_add_item_button').clicked.connect(lambda: self.INSApp.windows.Form(self.submodelClass))
            
            self.submodel.defind_add_button( add_btn =getattr(field, self.name+'_add_item_button'),def_name= 'sub', extra_data_for_added_items = {'model_id': self.item_obj.data.id})
            self.submodel.defind_delete_button( delete_btn =getattr(field, self.name+'_remove_button'),def_name= 'sub', list_ui_object =getattr(field, self.name+'_input_field'))
            self.submodel.defind_ui_list( list_ui_object =getattr(field, self.name+'_input_field'),def_name= 'sub', fillout = False)

            return field

        

 
        def Set_Data(self, data):
            
            for obj in self.submodel.filter(model_id = self.item_obj.data.id):               
                self.submodel.add_item_to_list(obj, list_target = getattr(self.field, self.name+'_input_field'))

            


####################################################################################################3

    class OneToOneField(Field):
        field_type              = 'OneToOneField'
        TYPE                    = int
        data_base_type          = 'int'
        UI_Field                = QtWidgets.QComboBox
        default                 =  ''
        properties              = []
        on_change               = None

        def view(self, UI, Form, field_name, position_index, field_obj = None, gridLayout = True, another_layout = None):

                setattr(UI, field_name, QtWidgets.QComboBox(Form) )
                ui_field = vars(UI)[field_name]
                ui_field.setObjectName(field_name)
                ui_field.setEnabled(self.editable)

                self.ui_field = ui_field
                
                objs = getattr(UI.model.INSApp, UI.fields[field_name].model).objects
                
                item_text = ''
                for obj in objs:
                    ui_field.addItem(str(obj), obj.id)

                if UI.edit_mode:# set current item
                    if UI.obj_mode:
                        current_item_text = getattr(UI.model.INSApp, UI.fields[field_name].model).get(id = getattr(UI.item_obj.data, field_name))

                    else:

                        current_item_text = UI.dict_data[field_name]

                    if ui_field.findText( str(current_item_text) )>-1:
                        ui_field.setCurrentIndex( ui_field.findText(str(current_item_text)))
                    else:
                        try:
                            ui_field.setCurrentIndex(ui_field.findData(str(current_item_text)))
                        except:
                            pass
                    

                if UI.fields[field_name].on_change != None:
                    ui_field.currentIndexChanged.connect(partial(UI.fields[field_name].on_change, UI, ui_field, ui_loaded = True))
                    
                if gridLayout:
                        UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                else:
                        another_layout.addWidget(self.ui_field, position_index, 1, 1, 1)
                if UI.fields[field_name].on_change != None:
                    return {'on_load_function':[partial(UI.fields[field_name].on_change, UI, ui_field, ui_loaded = False)] }
        
        def get_data(self):
                return self.ui_field.currentData()

    class ManyDataViewField(Field):
        field_type              = 'ManyDataViewField'
        data_base_type          = 'BLOB'
        data_from_function      = None
        properties              = []
        tooltip                 = '""'
        single_view             = False

        def view_item_data(self, PUI , listwidget):
            PUI.subwindow = QtWidgets.QDialog()

            ui = uic.loadUi(os.path.join('INSLPCModel','view_item_text_data.ui'), PUI.subwindow)
            PUI.subwindow.ui = ui
            PUI.subwindow.setStyleSheet(PUI.model.INSApp.currentStyle)
            PUI.subwindow.ui.setStyleSheet(PUI.model.INSApp.currentStyle)
            PUI.subwindow.ui.textBrowser.setMarkdown(listwidget.currentItem().data(6))
            PUI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
            PUI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            PUI.subwindow.show()

        def view(self, UI, Form, field_name, position_index, field_obj = None, gridLayout = True, another_layout = None):
                self.UI = UI
                self.field_name = field_name
                setattr(UI, field_name+'_gridLayoutWidget', QWidget() )
                gridLayoutWidget = vars(UI)[field_name+'_gridLayoutWidget']
                gridLayoutWidget.setObjectName(field_name+"_gridLayoutWidget")
                gridLayoutWidget.setEnabled(self.editable)

                setattr(UI, field_name+'_gridLayout',  QGridLayout(gridLayoutWidget))
                gridLayout = vars(UI)[field_name+'_gridLayout']
                gridLayout.setObjectName(field_name+'_gridLayout')
                gridLayout.setContentsMargins(2, 2, 2, 2)

                line = QFrame(Form)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setProperty('frame_type','Hline')
                gridLayout.addWidget(line, 0, 0, 1, 3)

                label = QtWidgets.QLabel(Form)
                label.setObjectName(field_name+"label")
                label.setAlignment(Qt.AlignCenter)
                label.setText( UI.translate(field_name.replace('_',' ').title()))
                gridLayout.addWidget(label, 1, 0, 1, 3)

                
                setattr(UI, field_name+'_listWidget', QListWidget(gridLayoutWidget))
                if UI.obj_mode:
                    setattr(UI.item_obj.data, field_name, [])
                else:
                    UI.dict_data[field_name] = []

                self.listWidget = vars(UI)[field_name+'_listWidget']
                self.listWidget.setObjectName(field_name+'_listWidget')
                self.listWidget.setMinimumSize(QSize(100, 125))
                self.listWidget.itemDoubleClicked.connect(partial(self.view_item_data, UI, self.listWidget  ))

                self.listWidget.setDragDropMode(QAbstractItemView.DragOnly)
                self.listWidget.setDefaultDropAction(Qt.MoveAction)
                self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
                self.listWidget.setMovement(QListView.Free)

                gridLayout.addWidget(self.listWidget, 3, 0, 1, 3)

                if self.data_from_function != None:
                    data = self.data_from_function(field = self, UI = UI)
                    for bit in data:
                        item_ui = QtWidgets.QListWidgetItem()
                        item_ui.setText(bit)
                        item_ui.setData(6,data[bit])
                        self.listWidget.addItem(item_ui)


                if UI.ManyToManyField_pos == 1:
                    position_index-=1

                if UI.view_data_fields[field_name].single_view:
                    #UI.gridLayout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)
                    #if gridLayout:
                    #    UI.gridLayout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)
                    #else:
                    another_layout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)
                else:
                #    if gridLayout:
                #        UI.gridLayout.addWidget(gridLayoutWidget, position_index, UI.ManyToManyField_pos, 1, 1)
                #    else:
                    another_layout.addWidget(gridLayoutWidget, position_index, UI.ManyToManyField_pos, 1, 1)
                    UI.ManyToManyField_pos = (UI.ManyToManyField_pos * (-1)) +1

    class ManyToManyField(Field):
        add_conditions          = {'statement':'True','error_msg':''}
        call_add_conditions     = {'statement':'True','error_msg':''}
        field_type              = 'ManyToManyField'
        TYPE                    = list
        data_base_type          = 'BLOB'
        default                 =  []
        on_add                  = None
        on_edit                 = None
        on_delete               = None
        before_add              = None
        before_edit             = None
        before_delete           = None
        addable                 = True
        removeable              = True
        editable                = True
        properties              = []
        tooltip                 = '""'
        single_view             = False

        def add_item(self, data):

            #chack_missing fields
            for field in self.subfields.keys():        
                if field not in data.keys():
                    data[field] = self.subfields[field].default


            
            if True:#self.before_add == None or self.before_add(data = data | {'item_object':self.item_obj}, main_ui = None):

                print(getattr(self.itam_obj, self.field_name+'_data'))
                data_list = getattr(self.itam_obj, self.field_name+'_data')
                data_list.append(data)
                setattr(self.itam_obj, self.field_name+'_data', data_list)
                self.itam_obj.save()

                
            #        if self.fields[main_field].on_add != None:
            #            self.fields[main_field].on_add(main_ui = self, data = data)
            #        self.subwindow.ui.saved = True
            #        self.subwindow.close()
                

        def view(self, UI, Form, field_name, position_index, field_obj = None, gridLayout = True, another_layout = None):
            try:
                self.UI = UI
                self.field_name = field_name
                setattr(UI, field_name+'_gridLayoutWidget', QWidget() )
                gridLayoutWidget = vars(UI)[field_name+'_gridLayoutWidget']
                gridLayoutWidget.setObjectName(field_name+"_gridLayoutWidget")
                gridLayoutWidget.setEnabled(self.editable)

                setattr(UI, field_name+'_gridLayout',  QGridLayout(gridLayoutWidget))
                gridLayout = vars(UI)[field_name+'_gridLayout']
                gridLayout.setObjectName(field_name+'_gridLayout')
                gridLayout.setContentsMargins(2, 2, 2, 2)

                line = QFrame(Form)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setProperty('frame_type','Hline')
                gridLayout.addWidget(line, 0, 0, 1, 3)


                label = QtWidgets.QLabel(Form)
                label.setObjectName(field_name+"label")
                label.setAlignment(Qt.AlignCenter)
                label.setText( UI.translate(field_name.replace('_',' ').title()))
                gridLayout.addWidget(label, 1, 0, 1, 3)
                if self.addable:
    
                    setattr(UI, field_name+'_add_button', QPushButton(gridLayoutWidget))              
                    add_button = vars(UI)[field_name+'_add_button']
                    add_button.setObjectName(field_name+"add_button")
                    add_button.setToolTip(UI.translate('add'))
                    add_button.setIcon(UI.app.Styler.get_icon('add'))
                    add_button.setMinimumSize(QSize(25, 25))
                    add_button.setMaximumSize(QSize(25, 25))
                    #add_button.clicked.connect( partial(UI.call_add_subitem_window, [UI.fields[field_name].subfields, field_name,UI.fields[field_name] ]) )
                    gridLayout.addWidget(add_button, 2, 2, 1, 1)
                
                if self.removeable:
                    setattr(UI, field_name+'_remove_button', QPushButton(gridLayoutWidget))
                    remove_button = vars(UI)[field_name+'_remove_button']
                    remove_button.setObjectName(field_name+"_remove_button")
                    remove_button.setToolTip(UI.translate('remove'))
                    remove_button.setIcon(UI.app.Styler.get_icon('delete'))
                    remove_button.setMinimumSize(QSize(25, 25))
                    remove_button.setMaximumSize(QSize(25, 25))
                    remove_button.setProperty('btn_type','delete')
                    #remove_button.clicked.connect( partial(UI.remove_subitem, field_name))
                    gridLayout.addWidget(remove_button, 2, 1, 1, 1)

                setattr(UI, field_name+'_listWidget', QListWidget(gridLayoutWidget))
                #if UI.obj_mode:
                #    setattr(UI.item_obj.data, field_name, [])
                #else:
                #    UI.dict_data[field_name] = []

                self.listWidget = vars(UI)[field_name+'_listWidget']
                self.listWidget.setObjectName(field_name+'_listWidget')
                self.listWidget.setMinimumSize(QSize(100, 100))
                if self.editable:
                    self.listWidget.itemDoubleClicked.connect(partial(UI.call_edit_subitem_window, self.listWidget, field_name ))

                self.listWidget.setDragDropMode(QAbstractItemView.DragOnly)
                self.listWidget.setDefaultDropAction(Qt.MoveAction)
                self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
                self.listWidget.setMovement(QListView.Free)

                gridLayout.addWidget(self.listWidget, 3, 0, 1, 3)


                if UI.edit_mode:
                    if UI.obj_mode:
                        fields_data = getattr(UI.item_obj.data, field_name)
                    else:
                        fields_data = UI.dict_data[field_name]

                    if type(fields_data) == str:
                        fields_data = json.loads(fields_data.replace("'",'"')) 

                    if UI.obj_mode:
                        setattr(UI.item_obj.data, field_name,fields_data )
                        dict_data = getattr(UI.item_obj.data, field_name)

                    else:
                        UI.dict_data[field_name] = fields_data
                        dict_data = UI.dict_data[field_name]

                    for subfield in dict_data:
                        view_name = UI.fields[field_name].view_name
                        if type(view_name) == str:
                            
                            view_name = replace_variable_value(view_name, data = subfield)
                            if type(view_name) not in [str, int]:
                                view_name = ''.join([ str(i) for i in view_name])

                            view_name = str(view_name)

                        else:
                            view_name = view_name(data = subfield, app = UI.app)

                        item_ui = QtWidgets.QListWidgetItem()
                        item_ui.setText(view_name)
                        item_ui.setToolTip(replace_variable_value( UI.fields[field_name].tooltip,data = subfield))
                        item_ui.setData(6,subfield)
                        self.listWidget.addItem(item_ui)

                else: # creation mode
                    if UI.obj_mode:
                        setattr(UI.item_obj.data, field_name, [])

                    else:
                        UI.dict_data[field_name] = []
                
                if UI.ManyToManyField_pos == 1:
                    position_index-=1


                if UI.fields[field_name].single_view:
             #       if gridLayout:
             #           UI.gridLayout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)
             #       else:
                    another_layout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)

                else:
                    #if gridLayout:
                    #    UI.gridLayout.addWidget(gridLayoutWidget, position_index, UI.ManyToManyField_pos, 1, 1)
                    #else:
                    another_layout.addWidget(gridLayoutWidget, position_index, UI.ManyToManyField_pos, 1, 1)
                    UI.ManyToManyField_pos = (UI.ManyToManyField_pos * (-1)) +1
            
            except:
                pass

        def get_data(self):
            data = []
            i=0
            while True:
                try:
                    data.append(self.listWidget.item(i).data(6))
                    i+=1
                except:
                    break


            return data
                
    
    
    
        
        

##############################################################################
##############################################################################
##############################################################################




class add_costomlist_item_Form(object):
    def setupUi(self, Form, data_receiver, list_name, ui_list):
        Form.setObjectName("Form")
        Form.resize(318, 159)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.item = QtWidgets.QLineEdit(Form)
        self.item.setObjectName("item")
        self.item.setPlaceholderText(self.app.translate('Item Name...'))
        self.gridLayout.addWidget(self.item, 0, 0, 1, 1)
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.add_btn.setObjectName("add_btn")
        self.add_btn.setMinimumSize(QSize(30, 30))
        self.add_btn.setMaximumSize(QSize(30, 30))
        self.add_btn.setIcon(self.app.Styler.get_icon('add'))
        self.add_btn.clicked.connect(lambda: data_receiver(list_name, self.item.text(), ui_list, Form))
        self.gridLayout.addWidget(self.add_btn, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)

        QtCore.QMetaObject.connectSlotsByName(Form)



def add_costomlist_item_Window(main_ui, data_receiver, list_name, ui_list):
    
    main_ui.subwindow = QtWidgets.QDialog()

    ui = add_costomlist_item_Form()
    ui.app = main_ui.model.INSApp
    ui.setupUi(main_ui.subwindow, data_receiver, list_name, ui_list)
    main_ui.subwindow.ui = ui
    
    main_ui.subwindow.setProperty('form_type', 'subwindow')
    main_ui.subwindow.setStyleSheet(main_ui.model.INSApp.currentStyle)
    main_ui.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    main_ui.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    main_ui.subwindow.show()




def replace_variable_value(text, item = None , data= None):
    return eval(text)



def common_field_design_1(self, ui_object, buttons = []):
    #ut.setColumnStretch(1, 4)
    label_size = [int(self.Base_input_field_size[0]*0.5), self.Base_input_field_size[1]]
    self.input_field_size = [int(self.Base_input_field_size[0]*0.5), self.Base_input_field_size[1]]
    
    self.ui_objects_list = [

                {
                    'position'  : [0,0,1,1],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type',
                    'ColumnStretch': 1,
                    'text-align': 'left',
                    #'Min-size'      : self.input_field_size,
                    #'Max-size'      : [90000, self.input_field_size[1]],
                    'size'      : [100,27],
                    
                },
                {
                    'position'  : [0,1,1,1],
                    'name'      : self.name+'_input_field',
                    'object'    : ui_object,
                    'type'      : 'Qt-type',
                    'ColumnStretch': 1,
                    'size'      : [160 - (len(buttons)*27)  ,27],
                }
            ]

               

    button_position = 2
    for button in buttons:
        UIproperty = {'btn_style':'Square_siz_1'}
        
        if button.get('UIproperty') !=None:
            UIproperty |= button.get('UIproperty')


        self.ui_objects_list.append(
            {
                    'position'  : [0,button_position,1,1],
                    'name'      : button.get('name'),
                    'icon'      : button.get('icon'),
                    'object'    : QtWidgets.QPushButton,
                    'type'      : 'Qt-type',
                    'ColumnStretch': 1,       
                    'UIproperty'  : UIproperty,
            })


        button_position += 1 
    FrameW = FrameWidget(self.name, self.ui_objects_list, self.APP)
    FrameW.core_field = self
    getattr(FrameW, self.name+'_label').setText(self.label)
    getattr(FrameW, self.name+'_label').setToolTip(self.label)
    
    
    self.frame = FrameW
    try:

        self.frame.frame.setMaximumSize(PyQt5_Qt.QSize(300,40))
    
    except Exception as a:
        print('ss',a)

    
    #self.frame.gridLayout.setColumnMinimumWidth(1, 300)
    
    
    self.input_field = getattr(FrameW, self.name+'_input_field')

    return FrameW
    

def common_field_design_2(self, ui_object, buttons = []):

    self.input_field_size = [self.Base_input_field_size[0], 100]
    self.ui_objects_list = [
                {
                    'position'  : [0,0,1,1],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type',
                    'text-align': 'left',
                  
                },
                {
                    'position'  : [1, 0, len(buttons)+2, 1],
                    'name'      : self.name+'_input_field',
                    'object'    : ui_object,
                    'type'      : 'Qt-type',
                    'Min-size'      : self.input_field_size,
                    'Max-size'      : [90000, 100],
                }
            ]

    button_position = 2
    for button in buttons:
        UIproperty = {'btn_style':'Square_siz_1'}
        
        if button.get('UIproperty') !=None:
            UIproperty |= button.get('UIproperty')
        
        self.ui_objects_list.append(
            {
                    'position'  : [0,button_position,1,1],
                    'name'      : button.get('name'),
                    'icon'      : button.get('icon'),
                    'object'    : QtWidgets.QPushButton,
                    'type'      : 'Qt-type',
                    'UIproperty'  : UIproperty,
            })

        button_position += 1 
    
    FrameW = FrameWidget(self.name, self.ui_objects_list, self.APP)
    FrameW.core_field = self
    getattr(FrameW, self.name+'_label').setText(self.label)
    self.frame = FrameW
    

    self.input_field = getattr(FrameW, self.name+'_input_field')

    return FrameW

