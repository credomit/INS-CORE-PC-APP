from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, configparser
from types import MethodType
from . import fields


class Form(object):

    def __init__(self, PW, model, item, title, extra_data_for_adding = {}, app = None, ui_file_path = None, UIs_list = None) -> None:
        
        self.UIs_list = UIs_list
        if UIs_list != None:
            UIs_list.append(self)


        
        if PW != None:
             
            PW.subwindow = QtWidgets.QDialog()
            PW.subwindow_obj = self
            print('pw', PW, PW.subwindow)
            self.dialog = PW.subwindow
            self.app = PW.app
            self.translate = PW.app.translate
            self.style = PW.app.currentStyle
            self.PW = PW
        else:
            
            self.dialog = QtWidgets.QDialog()
            self.app = app
            self.translate = app.translate
            self.style = app.currentStyle

        self.model = model
        self.item = item
        self.extra_data_for_adding = extra_data_for_adding
        self.general_method = 'ADD'




        self.dialog.closeEvent = MethodType(self.closeEvent,self.dialog )

        if ui_file_path == None:
            self.ui = uic.loadUi(os.path.join(os.path.join(os.path.dirname( __file__ )), 'UIs', 'widget.ui'), self.dialog)
            
            self.dialog.scrollAreaWidgetContents.setProperty('widget_type','scrollarea_widget')

        else:
            self.ui = uic.loadUi(ui_file_path, self.dialog)
            

        self.ui.out_frame.setProperty('form_type', 'subwindow')
                

        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.dialog.setProperty('form_type', 'subwindow-dialog')
        self.dialog.setAttribute(Qt.WA_TranslucentBackground)
        
        self.ui.title_bar.mousePressEvent = self.mousePressEvent
        self.ui.title_bar.mouseMoveEvent = self.mouseMoveEvent
        self.ui.window_title.mousePressEvent = self.mousePressEvent
        self.ui.window_title.mouseMoveEvent = self.mouseMoveEvent

        self.ui.window_title.setText(title.title())

        self.ui.close_form_button.clicked.connect(self.close)
        self.ui.title_bar.setProperty('form_type', 'title-bar')

        self.dialog.setStyleSheet(self.style)


        self.set_shadow()



    def closeEvent(self,r, event):
        if self.UIs_list != None:
            self.UIs_list.remove(self)

        


    def set_shadow(self):
        hover_effect = QtWidgets.QGraphicsDropShadowEffect()
        hover_effect.setBlurRadius(90.0)
        hover_effect.setColor(QColor(0, 0, 0, 160))
        hover_effect.setOffset(0)
        self.dialog.setGraphicsEffect(hover_effect)
        
        
    def mousePressEvent(self, event):   
                                     
        self.dragPos = event.globalPos()

    def close(self):
        self.dialog.close()

    def mouseMoveEvent(self, event):                                  
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dialog.move(self.dialog.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


    def show(self):
        self.dialog.show()
        
        

    def set_fields(self, fields, Data = None):
        try:
            if Data == None:
                setData = False
            
            else:
                setData = True

            config = configparser.ConfigParser()
            config.read( os.path.join('INSLPCModel','settings.ini'), "utf8")
            position_index = 0
            fields_list = []
            current_field_index = 0
            dictlist_4_sublist = [] # to make sure that sublist loaded into ui
            on_load_function = [] # function need to run when window is loaded

            self.ManyToManyField_pos = 0
            self.fields = fields
            self.edit_mode = False

            
    

            self.fields_On_Add_To_UI_functions = []
            for field in self.fields:
                fields_list.append(field)
                current_field_index +=1
                self.fields[field].name     = field
                self.fields[field].label    = field
                self.fields[field].APP      = self.app
                self.fields[field].model    = self.model
                self.fields[field].item_obj = self.item
                self.fields[field].main_ui  = self


                
                try:
                    field_widget = self.fields[field].Create_UI_Widget()
                    setattr(self.ui, field, field_widget)
                    field_widget.frame.parent = self.dialog.scrollAreaWidgetContents
                    field_widget.frame.parentUI = self
                    self.dialog.scrollArea_gridLayout.addWidget(field_widget.frame, position_index, 1, 1, 1, Qt.AlignVCenter)

                    # to remove
                    

                    ###########
                    
                
                except Exception as a:
                    print(field, a)
                    OLF = self.fields[field].view(self, self.dialog.scrollAreaWidgetContents, field, position_index,  gridLayout = False, another_layout =self.dialog.scrollArea_gridLayout ) # on load function
                    if OLF != None:
                        if OLF.get('on_load_function') != None:
                            on_load_function    +=  OLF.get('on_load_function')

                        if OLF.get('dictlist_4_sublist') != None:
                            dictlist_4_sublist  +=  OLF.get('dictlist_4_sublist')
                            
                position_index+=1
            
            for field in self.fields:
                
                self.fields[field].On_Add_To_UI()

                if setData:
                    try:
                        self.fields[field].Set_Data(Data.get(field))
                    except Exception as a:
                        print(a)
            
            self.dialog.scrollArea.setWidget(self.dialog.scrollAreaWidgetContents)
            
            self.dialog.setStyleSheet(self.app.currentStyle)

        except Exception as a :
            print(a)
        
    def set_data(self, data):
        for field in data:
            self.fields[field].Set_Data(data.get(field))

    def get_form_data(self):
        data = {}
        for field in self.fields:
            data[field] = self.fields[field].Get_DB_Data()

        return data

    def submit(self, close = True):
        op_status = True
        data = self.get_form_data()
        
        if self.general_method == 'ADD':
            op_status = self.model.add_item(data | self.extra_data_for_adding)

            if self.After_Add_FUNC != None:
                self.After_Add_FUNC(op_status)
            

        if self.general_method == 'EDIT':
            edited_data = { field:self.fields[field].Get_Data() for field in self.fields}
            self.item_obj.data.edit(edited_data)


        if op_status and close:
            self.dialog.close()



    def set_buttons(self, add_button = False, edit_button = False ):

        if add_button:
            self.add_button = QPushButton(self.dialog)
            self.add_button.setObjectName(u"form_add_button")
            self.add_button.setIcon(self.app.Styler.get_icon('add'))
            self.add_button.setText(self.app.translate('add'))
            self.add_button.setProperty('btn_type','add')
            self.add_button.setProperty('btn_style','Rectangle_siz_1')
            self.add_button.clicked.connect(lambda: self.submit())
            self.general_method = 'ADD'

            self.dialog.buttonsLayout.addWidget(self.add_button, 0, 0, 1, 1)

        if edit_button:
            self.edit_button = QPushButton(self.dialog)
            self.edit_button.setObjectName(u"form_edit_button")
            self.edit_button.setIcon(self.app.Styler.get_icon('edit'))
            self.edit_button.setText(self.app.translate('edit'))
            self.edit_button.setProperty('btn_type','edit')
            self.edit_button.setProperty('btn_style','Rectangle_siz_1')
            self.edit_button.clicked.connect(lambda: self.submit())
            self.general_method = 'EDIT'

            self.dialog.buttonsLayout.addWidget(self.edit_button, 0, 1, 1, 1)

    def get_fields_data(self):
        data = {}  # field name: data
        for field in self.fields:
            try:
                data[field] = self.fields[field].Get_Data()
            except Exception as a:
                print(a)

        return data



        