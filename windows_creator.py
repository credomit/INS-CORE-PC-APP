# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .fields import Fields
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os, configparser, json
from functools import partial
from types import MethodType
from .Statements import *
import datetime
from . import windows

def replace_variable_value(text, item = None , data= None):
    return eval(text)


class Loading_UI(object):
    def open_INSPP_file(self, l_ui):

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))

        file_name=QFileDialog.getOpenFileName(l_ui, self.app.translate(f"open { self.app.app_file_type } file"),config['settings']['last_opened_location'],f"{ self.app.app_file_type } Files (*.{ self.app.app_file_type })")
        
        if len(file_name[1])>0:
            self.open.setVisible(False)
            self.create.setVisible(False)
            self.exit.setVisible(False)

            config['settings']['last_opened_location']=file_name[0]
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))

            self.app.database_path = file_name[0]
            self.app.DataController.DB_PATH = file_name[0]
            self.app.DataController.init_mode()
            self.app.run_main_window()

        

    def create_INSPP_file(self,l_ui):

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'), 'UTF-8')

        file_name=QFileDialog.getSaveFileName(l_ui,self.app.translate(f"create { self.app.app_file_type } file"),config['settings']['last_opened_location'],f"{ self.app.app_file_type } Files (*.{ self.app.app_file_type })")
        
        if len(file_name[1])>0:
            self.open.setVisible(False)
            self.create.setVisible(False)
            self.exit.setVisible(False)
            config['settings']['last_opened_location']=file_name[0]
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
            
            
            self.app.database_path = file_name[0]
            
            self.app.run_main_window()

    def setupUi(self, login_2):
        login_2.setObjectName("login_2")
        login_2.resize(921, 542)
        login_2.setStyleSheet("")
        self.progressBar = QtWidgets.QProgressBar(login_2)
        self.progressBar.setGeometry(QtCore.QRect(140, 480, 610, 25))
        self.progressBar.setStyleSheet("border-width:0px;")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("Loading_win_ProgressBar")
        self.progressBar.setMinimumSize(QtCore.QSize(625, 30))
        self.progressBar.setMaximumSize(QtCore.QSize(625, 30))
        self.frame = QtWidgets.QLabel(login_2)
        self.frame.setGeometry(QtCore.QRect(0, 0, 781, 481))
        self.frame.setStyleSheet("#frame{border-radius: 10px;background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 0), stop:1 rgba(255, 255, 255, 0));}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        pixmap = QPixmap(u"l1.png")
        style_icon_colors = configparser.ConfigParser()
        style_icon_colors.read( os.path.join('INSLPCModel','styles.ini'))
        for color in style_icon_colors[self.app.currentStyleName]:
                print(color)
                mask = pixmap.createMaskFromColor(QtGui.QColor('#'+color), QtCore.Qt.MaskOutColor)
                pen = QtGui.QPainter(pixmap)
                pen.setPen(QtGui.QColor('#'+style_icon_colors[self.app.currentStyleName][color]))
                pen.drawPixmap(pixmap.rect(), mask, mask.rect())
                pen.end()
        
        self.frame.setPixmap(pixmap)
        self.frame.setScaledContents(True)
        self.exit = QtWidgets.QPushButton(self.frame)
        self.exit.setGeometry(QtCore.QRect(139, 75, 30, 30))
        self.exit.setMinimumSize(QtCore.QSize(20, 20))
        self.exit.setMaximumSize(QtCore.QSize(20, 20))
        self.exit.setObjectName("exit")
        self.exit.setIcon(self.app.Styler.get_icon('exit'))
        self.exit.setProperty('btn_type','exit')
        self.msg = QtWidgets.QLabel(self.frame)
        self.msg.setGeometry(QtCore.QRect(350, 370, 160, 17))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.msg.setFont(font)
        self.msg.setStyleSheet("color: rgb(211, 215, 207);")
        self.msg.setText("")
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        self.msg.setObjectName("msg")
        self.create = QtWidgets.QPushButton(self.frame)
        self.create.setGeometry(QtCore.QRect(360, 323, 160, 40))
        self.create.setText("")
        self.create.setObjectName("create")
        self.create.setProperty('btn_type','border_only')
        self.open = QtWidgets.QPushButton(self.frame)
        self.open.setGeometry(QtCore.QRect(360, 370, 160, 40))
        self.open.setText("")
        self.open.setObjectName("open")
        self.open.setProperty('btn_type','border_only')
        self.loading_label = QtWidgets.QLabel(self.frame)
        self.loading_label.setGeometry(QtCore.QRect(280, 280, 301, 161))
        self.loading_label.setText("")
        self.loading_label.setScaledContents(True)
        self.loading_label.setObjectName("loading_label")
        self.loading_label.raise_()
        self.exit.raise_()
        self.msg.raise_()
        self.create.raise_()
        self.open.raise_()
        self.frame.raise_()
        self.progressBar.raise_()

        QtCore.QMetaObject.connectSlotsByName(login_2)



def loading_window(app):

    def open_INSPP_file(ui):

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))

        file_name=QFileDialog.getOpenFileName(ui, ui.app.translate(f"open { ui.app.app_file_type } file"),config['settings']['last_opened_location'],f"{ ui.app.app_file_type } Files (*.{ ui.app.app_file_type })")
        
        if len(file_name[1])>0:
            ui.open_btn.setVisible(False)
            ui.create_btn.setVisible(False)
            ui.exit_btn.setVisible(False)

            config['settings']['last_opened_location']=file_name[0]
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))

            ui.app.database_path = file_name[0]
            ui.app.DataController.DB_PATH = file_name[0]
            ui.app.DataController.init_mode()
            ui.app.run_main_window()

        

    def create_INSPP_file(ui):

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'), 'UTF-8')

        file_name=QFileDialog.getSaveFileName(ui,ui.app.translate(f"create { ui.app.app_file_type } file"),config['settings']['last_opened_location'],f"{ ui.app.app_file_type } Files (*.{ ui.app.app_file_type })")
        
        if len(file_name[1])>0:
            ui.open_btn.setVisible(False)
            ui.create_btn.setVisible(False)
            ui.exit_btn.setVisible(False)
            config['settings']['last_opened_location']=file_name[0]
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
            
            
            ui.app.database_path = file_name[0]
            
            ui.app.run_main_window()

    app.LoadinWindow = QtWidgets.QDialog()
    app.LoadinWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.LoadinWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    qr = app.LoadinWindow.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    app.LoadinWindow.move(qr.topLeft())
    app.LoadinWindow.setAttribute(Qt.WA_TranslucentBackground)

    ui = uic.loadUi(os.path.join(os.path.join(os.path.dirname( __file__ )), 'UIs', 'Loading_window.ui'),app.LoadinWindow  )
    ui.app = app


    app.LoadinWindow.ui = ui
    app.LoadinWindow.setStyleSheet(app.qss_style+'''
    #frame{
			background-repeat: no-repeat;
			background-position: center;  
	}'''+app.currentStyle)

    pixmap = QPixmap(u"l1.png")
    style_icon_colors = configparser.ConfigParser()
    style_icon_colors.read( os.path.join('INSLPCModel','styles.ini'))
    for color in style_icon_colors[app.currentStyleName]:
                mask = pixmap.createMaskFromColor(QtGui.QColor('#'+color), QtCore.Qt.MaskOutColor)
                pen = QtGui.QPainter(pixmap)
                pen.setPen(QtGui.QColor('#'+style_icon_colors[app.currentStyleName][color]))
                pen.drawPixmap(pixmap.rect(), mask, mask.rect())
                pen.end()
        
    ui.frame.setPixmap(pixmap)
    ui.frame.setScaledContents(True)

    ui.open_btn.setText(app.translate('Open'))
    ui.create_btn.setText(app.translate('Create new file'))

    ui.progressBar.setStyleSheet("border-width:0px;")
    ui.progressBar.setObjectName("Loading_win_ProgressBar")


    ui.open_btn.setProperty('btn_type','border_only')
    ui.create_btn.setProperty('btn_type','border_only')

    ui.open_btn.clicked.connect( lambda: open_INSPP_file(ui) )
    ui.create_btn.clicked.connect( lambda: create_INSPP_file(ui) )
    ui.exit_btn.clicked.connect(lambda: app.LoadinWindow.close() )

    app.LoadinWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.LoadinWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    print('showing')
    app.LoadinWindow.show()




##############################################################################
##############################################################################
##############################################################################



class View_Item_Ui_Form(object):
    
    def call_add_subitem_window(self, args):
        
        fields          = args[0]
        main_field      = args[1]
        main_field_obj  = args[2]
        passed_item     = self.item_obj

        if chack_static_statement_status(main_field_obj.call_add_conditions, self.model.INSApp, self.item_obj, data=vars(self)):
            self.subwindow = QtWidgets.QDialog()

            ui = View_Item_Ui_Form()
            ui.setupUi(self.subwindow, fields = fields, model = self.model, data_receiver = self.add_subitem, main_field = main_field ,is_subitem = True, pui = self)

            self.subwindow.ui = ui
            self.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.subwindow.show()


    def add_subitem(self, data, main_field):
        
        main_field_obj = self.fields[main_field]
        if main_field_obj.before_add == None or main_field_obj.before_add(data = data | {'item_object':self.item_obj}, main_ui = self):
            
                list_ui   = getattr(self, main_field+'_listWidget')
                view_name = self.fields[main_field].view_name
                view_name = replace_variable_value(view_name, self.item_obj, data)

                if type(view_name) in [list, set, tuple]:# fixing view name if it comeup as list or tuple...
                    view_name = ''.join(list([ str(i) for i in view_name]))

                item = QtWidgets.QListWidgetItem()
                item.setText(view_name)
                item.setData(6,data)
                list_ui.addItem(item)
            
                if self.fields[main_field].on_add != None:
                    self.fields[main_field].on_add(main_ui = self, data = data)
                self.subwindow.ui.saved = True
                self.subwindow.close()
            

    def remove_subitem(self,field):
        try:
            list_ui = getattr(self, field+'_listWidget')
            if self.fields[field].before_delete == None or self.fields[field].before_delete(item = list_ui.currentItem().data(6), main_ui = self):
                current_item = getattr(self, field+'_listWidget').currentItem()
                item_data = list_ui.currentItem().data(6)
                list_ui.takeItem(list_ui.currentRow())
                
                if self.fields[field].on_delete != None:
                        self.fields[field].on_delete(data = item_data, main_ui = self)
        except Exception as a:
            print(a)

    def edit_subitem(self, form):
        data = {}
        
        for f in form.fields:
            data[f] = form.fields[f].get_data()
            
        main_ui_field =  self.fields[form.main_field].listWidget
        old_data = main_ui_field.currentItem().data(6)

        if self.fields[form.main_field].before_edit == None or self.fields[form.main_field].before_edit(old_data = main_ui_field.currentItem().data(6), new_data = data, item_obj = self.item_obj, main_ui = self):
            main_ui_field.currentItem().setData(6, data)
            main_ui_field.currentItem().setText(replace_variable_value(self.fields[form.main_field].view_name, item = self.item_obj, data = data))
            if self.fields[form.main_field].on_edit != None:
                self.fields[form.main_field].on_edit(old_data = old_data, new_data = data, main_ui = self)

            form.saved = True
            form.Form.close()
            


    def call_edit_subitem_window(self, ui_list, field):
        self.subwindow = QtWidgets.QDialog()

        ui = View_Item_Ui_Form()
        ui.setupUi(self.subwindow ,  self.model, self.fields[field].subfields, title = field, item_obj=self.item_obj, app = self.model.INSApp , data_receiver = self.edit_subitem , main_field = field,is_subitem = True, edit_mode = True, pui = self, obj_mode = False, dict_data = ui_list.currentItem().data(6))
        self.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.subwindow.show()

        
    def add_customlist_item(self,list_name, item, ui_list, sub_ui = None):
        
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'),  "utf8")
        customlist = json.loads(config['CustomLists'][list_name])
        customlist.append(item)
        customlist = list(set(customlist))
        config['CustomLists'][list_name] = json.dumps(customlist)
        config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
        ui_list.insertItem(0,item)
        ui_list.setCurrentIndex(0)
        
        if sub_ui != None:
            sub_ui.ui.saved = True
            sub_ui.close()

    def add_item(self,  model, Form, is_subitem, data_receiver, main_field):
            data = {}
            for field in self.fields.keys():
                data[field] = self.fields[field].get_data()
            
            if (model.before_add == None) or (model.before_add(data = data)):
                        
                if (not is_subitem):
                    item = model.create(dict_inner_data = data, UI = self)
                    if item:
                        Form.ui.saved = True
                        Form.close()

                else:
                    data_receiver(data, main_field)
                    Form.ui.saved = True
                    Form.close()

                if Form.ui.saved and model.on_add != None:
                    model.on_add(item = item)



    def edit_item(self, Form, item):
        data = {}
        for field in item.model.fields.keys():
            data[field] = item.model.fields[field].get_data()

        if (item.model.before_edit == None) or (item.model.before_edit(item = item,data = data)):
                        
            for field in item.model.fields.keys():
                setattr( item, field, item.model.fields[field].get_data())

            item.save(call_on_edit = True)
            Form.ui.saved = True
            Form.close()



    def change_subdict_field(self,args):
        
        field = args[0]
        subfields = args[1]
        fields = args[2]
        for subfield in subfields:
            ui_field = vars(self)[subfield]
            ui_field.clear()
                    
            for item in fields[field].item_dict[vars(self)[field].currentText()]:
                ui_field.addItem(item)

    def closeEvent(self,r, event):
        if self.saved:
            event.accept()

        else:
            close =  self.cancel_op()
            if close :
                event.accept()
            else:
                event.ignore()

    def cancel_op(self):
        ansower = QtWidgets.QMessageBox.question(self.Form , self.translate('Cancel Confirm') , self.translate('are you sure you want to exit?')+'\n'+self.translate('your changes will not be saves'))
        if ansower==QtWidgets.QMessageBox.Yes:
            self.saved = True
            self.Form.close()
            return True
        else:
            return False


    def setupUi(self, Form, model, fields, title = '' , app = None , data_receiver = None , main_field = None, item_obj = None , is_subitem = False, edit_mode = False, pui = None, obj_mode = True, dict_data = None):
        self.model      = model
        self.fields     = fields
        self.Form       = Form
        self.main_field = main_field
        self.item_obj   = item_obj
        self.is_subitem = is_subitem
        self.edit_mode  = edit_mode
        self.pui        = pui
        self.dict_data  = dict_data
        self.obj_mode   = obj_mode
        self.saved      = False
        
        if obj_mode:
            self.app = model.INSApp
            self.view_data_fields = model.view_data_fields
        else:
            self.app = app
            self.view_data_fields = {}

        if self.app.current_language_layout_direction == 'RTL':
            self.Form.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            self.Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.translate = self.app.translate
        Form.closeEvent = MethodType(self.closeEvent,Form)
    
        if not edit_mode and obj_mode:
            self.item_obj = model.temporary_item()

        Form.setObjectName("Form")
        Form.setProperty('form_type', 'subwindow')
        #Form.resize(600, 450)
        s_width = 485
        Form.setMaximumWidth(s_width)
        Form.setMinimumWidth(s_width)

        opr = 'add'
        if edit_mode:
            opr = 'edit'

        if obj_mode:
            Form.setWindowTitle(self.translate(opr+model.__class__.__name__.replace('_',' ').title()))
            Form.setStyleSheet(model.INSApp.currentStyle)

        else:
            Form.setWindowTitle(app.translate(title))
            Form.setStyleSheet(app.currentStyle)
        
        
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        if edit_mode:
            self.edit_btn = QtWidgets.QPushButton(Form)
            self.edit_btn.setObjectName(u"edit_btn")
            self.edit_btn.setToolTip(self.translate('edit'))
            self.edit_btn.setIcon(self.app.Styler.get_icon('edit'))
            self.edit_btn.setMinimumSize(QSize(30, 30))
            self.edit_btn.setMaximumSize(QSize(30, 30))
            if obj_mode:
                self.edit_btn.clicked.connect(lambda: self.edit_item(Form, item_obj))
            
            else:
                self.edit_btn.clicked.connect(lambda: data_receiver(self))

            self.gridLayout_2.addWidget(self.edit_btn, 1, 2, 1, 1)

        else:
            self.add_btn = QtWidgets.QPushButton(Form)
            self.add_btn.setObjectName(u"add_btn")
            self.add_btn.setToolTip(self.translate('add'))
            self.add_btn.clicked.connect(lambda: self.add_item(model,Form, is_subitem,data_receiver, main_field))
            self.add_btn.setMinimumSize(QSize(30, 30))
            self.add_btn.setMaximumSize(QSize(30, 30))
            self.add_btn.setIcon(self.app.Styler.get_icon('add'))

            self.gridLayout_2.addWidget(self.add_btn, 1, 2, 1, 1)

        
        self.cancel_btn = QtWidgets.QPushButton(Form)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setToolTip(self.translate('cancel'))
        self.cancel_btn.clicked.connect(self.cancel_op)
        self.cancel_btn.setMinimumSize(QSize(30, 30))
        self.cancel_btn.setMaximumSize(QSize(30, 30))
        self.cancel_btn.setIcon(self.app.Styler.get_icon('delete'))
        self.cancel_btn.setProperty('btn_type','delete')

        self.gridLayout_2.addWidget(self.cancel_btn, 1, 1, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'), "utf8")
        position_index = 0
        fields_list = []
        current_field_index = 0
        dictlist_4_sublist = [] # to make sure that sublist loaded into ui
        on_load_function = [] # function need to run when window is loaded
        self.ManyToManyField_pos = 0
        
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrdfvbollArea")
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 3)
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setObjectName(u"vcff")
        self.scrollAreaWidgetContents.setMaximumWidth(450)
        self.scrollAreaWidgetContents.setMinimumWidth(450)
        self.scrollArea_gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea_gridLayout.setObjectName(u"gridLayout33443")

        self.fields_On_Add_To_UI_functions = []
        for field in self.fields:
            
            fields_list.append(field)
            current_field_index +=1
            self.fields[field].name = field
            self.fields[field].label = field
            self.fields[field].APP = self.app

            
            try:
                field_widget = self.fields[field].Create_UI_Widget()
                field_widget.frame.parent = self.scrollAreaWidgetContents
                field_widget.frame.parentUI = self
                
                self.scrollArea_gridLayout.addWidget(field_widget.frame, position_index, 1, 1, 1, Qt.AlignVCenter)

                try:
                    self.fields[field].Set_Data(2)
                except Exception as a:
                    print(a)
                
            
            except Exception as a:
                OLF = self.fields[field].view(self, self.scrollAreaWidgetContents, field, position_index,  gridLayout = False, another_layout =self.scrollArea_gridLayout ) # on load function
                if OLF != None:
                    if OLF.get('on_load_function') != None:
                        on_load_function    +=  OLF.get('on_load_function')

                    if OLF.get('dictlist_4_sublist') != None:
                        dictlist_4_sublist  +=  OLF.get('dictlist_4_sublist')
                        
        

            position_index+=1


        
        for field in self.fields:
            self.fields[field].On_Add_To_UI()


        for DL_subfield in []:#dictlist_4_sublist:
                DL_ui_field = vars(self)[DL_subfield['mainfield_name']]
                DL_items    = self.fields[DL_subfield['mainfield_name']].item_dict
                field_object= self.fields[DL_subfield['subfield_name']]
                SF          = getattr(field_object.frame, field_object.name+'_input_field')
                SF.clear()
                
                for i in DL_items[DL_ui_field.currentText()]:
                    SF.addItem(i)
                if edit_mode and obj_mode:
                    current_SF  = vars(self.item_obj)[DL_subfield['subfield_name']]
                    if SF.findText( current_SF )>-1:
                        SF.setCurrentIndex( SF.findText( current_SF ) )
        

        for func in on_load_function:
            func()

        for field in self.view_data_fields.keys():
            self.view_data_fields[field].view(self, self.scrollAreaWidgetContents, field, position_index,   gridLayout = False, another_layout =self.scrollArea_gridLayout) 
            position_index +=1

        #self.scrollArea.addLayout(self.scrollArea_gridLayout,0,0,1,1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 3)
        self.Form.setStyleSheet(self.app.currentStyle)

    
    def __str__(self):
        try:
            return f'< {self.model} / {self.main_field} >'        
        
        except:
            return '<Unloaded window>'




def create_item_window(app, model):
    

    
    app.UI.subwindow = windows.Form(app.UI,  model = model)
    app.UI.subwindow.set_fields( fields = model.fields,)
    app.UI.subwindow.show()

def f():
    ui = View_Item_Ui_Form()
    app.UI.subwindow.ui = ui
    ui.setupUi(app.UI.subwindow, model = model , fields = model.fields, pui= app.UI)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()




def edit_item_window(item):
    app = item.data(6).model.INSApp
    app.UI.subwindow = QtWidgets.QDialog()

    ui = View_Item_Ui_Form()
    app.UI.subwindow.ui = ui
    ui.setupUi(app.UI.subwindow, model = item.data(6).model , fields= item.data(6).model.fields  , item_obj = item.data(6), edit_mode=True, pui= app.UI)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()



