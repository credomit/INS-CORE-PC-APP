
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .fields import Fields
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, configparser, json
from functools import partial

from .Statements import *
import datetime


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
            l_ui.close()
            self.app.run_main_window()

    def create_INSPP_file(self,l_ui):

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))

        file_name=QFileDialog.getSaveFileName(l_ui,self.app.translate(f"create { self.app.app_file_type } file"),config['settings']['last_opened_location'],f"{ self.app.app_file_type } Files (*.{ self.app.app_file_type })")
        
        if len(file_name[1])>0:
            self.open.setVisible(False)
            self.create.setVisible(False)
            self.exit.setVisible(False)
            config['settings']['last_opened_location']=file_name[0]
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
            
            
            self.app.database_path = file_name[0]
            l_ui.close()
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
        self.progressBar.setObjectName("progressBar")
        self.frame = QtWidgets.QFrame(login_2)
        self.frame.setGeometry(QtCore.QRect(10, -10, 781, 481))
        self.frame.setStyleSheet("border-radius: 10px;background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 0), stop:1 rgba(255, 255, 255, 0));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.exit = QtWidgets.QPushButton(self.frame)
        self.exit.setGeometry(QtCore.QRect(139, 75, 30, 30))
        self.exit.setMinimumSize(QtCore.QSize(30, 30))
        self.exit.setMaximumSize(QtCore.QSize(30, 30))
        self.exit.setObjectName("exit")
        self.exit.setText('X')
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
        self.open = QtWidgets.QPushButton(self.frame)
        self.open.setGeometry(QtCore.QRect(360, 370, 160, 40))
        self.open.setText("")
        self.open.setObjectName("open")
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
    
    app.LoadinWindow = QtWidgets.QDialog()
    app.LoadinWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.LoadinWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    qtRectangle = app.LoadinWindow.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    app.LoadinWindow.move(qtRectangle.topLeft())

    app.LoadinWindow.setAttribute(Qt.WA_TranslucentBackground)

    loading_cover = os.path.join('loading-covers', 'l1.png')

    



    ui = Loading_UI()
    ui.setupUi(app.LoadinWindow)
    ui.app = app

    app.LoadinWindow.setStyleSheet(app.qss_style+'''
    #frame{
	        background-image: url("l1.png");
			background-repeat: no-repeat;
			background-position: center;  
	}'''+app.currentStyle)

    ui.open.setText(app.translate('Open'))
    ui.create.setText(app.translate('Create new file'))

    ui.open.clicked.connect( lambda: ui.open_INSPP_file(app.LoadinWindow) )
    ui.create.clicked.connect( lambda: ui.create_INSPP_file(app.LoadinWindow) )
    ui.exit.clicked.connect(lambda: app.LoadinWindow.close() )

    app.LoadinWindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.LoadinWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
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

            self.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.subwindow.show()


    def add_subitem(self, data, main_field):
        main_field_obj = self.fields[main_field]

        if chack_static_statement_status(main_field_obj.add_conditions, self.model.INSApp, self.item_obj, data = vars(self)|data):
            o_data = getattr(self, main_field+'_data')
            o_data.append(data)
            setattr(self, main_field+'_data', o_data )

            list_ui   = getattr(self, main_field+'_listWidget')
            view_name = self.model.fields[main_field].view_name
            view_name = replace_variable_value(view_name, self.item_obj, data)

            if type(view_name) in [list, set, tuple]:# fixing view name if it comeup as list or tuple...
                view_name = ''.join(list([ str(i) for i in view_name]))

            item = QtWidgets.QListWidgetItem()
            item.setText(view_name)
            item.setData(6,data)
            list_ui.addItem(item)
            
            if self.model.fields[main_field].on_add != None:
                self.model.fields[main_field].on_add(data = data)

            self.subwindow.close()
        

    def remove_subitem(self,field):
        
        current_item = getattr(self, field+'_listWidget').currentItem()
        list_ui = getattr(self, field+'_listWidget')
        item_data = list_ui.currentItem().data(6)
        list_ui.takeItem(list_ui.currentRow())
        getattr(self, field+'_data').remove(current_item.data(6))

        if self.model.fields[field].on_delete != None:
            self.model.fields[field].on_delete(data = item_data)


    def edit_subitem(self, form):
        

        data = {}
        for field in form.fields.keys():

            if form.fields[field].field_type == 'OneToOneField':
                data[field] = vars(form)[field].currentData()

            elif form.fields[field].field_type == 'ManyToManyField':
                dict_data = getattr(form, field+'_data')
                data[field] =  dict_data

            elif form.fields[field].field_type == 'DateField':
                data[field] = vars(form)[field].date().toPyDate().isoformat()
                

            else:
                data[field] = getattr(vars(form)[field] , form.fields[field].Get_UI_Value_Function  )()

        old_data =  getattr(self, form.main_field+'_data')
        
        old_data.remove(form.dict_data)
        old_data.append(data)
        setattr(self, form.main_field+'_data', old_data)
        
        ui_item =  getattr(self, form.main_field+'_listWidget').currentItem()
        ui_item.setData(6,data)

        view_name = self.fields[form.main_field].view_name

        view_name = replace_variable_value(view_name, data = data)
        if type(view_name) not in [str, int]:
            view_name = ''.join([ str(i) for i in view_name])
        ui_item.setText(view_name)

        if self.fields[form.main_field].on_edit != None:
            self.fields[form.main_field].on_edit(old_data = form.dict_data, edited_data =data )


        form.Form.close()

        

    def call_edit_subitem_window(self, ui_list, field):
        self.subwindow = QtWidgets.QDialog()

        ui = View_Item_Ui_Form()
        ui.setupUi(self.subwindow ,  self.model, self.fields[field].subfields, title = field , app = self.model.INSApp , data_receiver = self.edit_subitem , main_field = field,is_subitem = True, edit_mode = True, pui = self, obj_mode = False, dict_data = ui_list.currentItem().data(6))
        self.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.subwindow.show()

        
    def add_customlist_item(self,list_name, item, ui_list, sub_ui = None):
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        customlist = json.loads(config['CustomLists'][list_name])
        customlist.append(item)
        customlist = list(set(customlist))
        config['CustomLists'][list_name] = json.dumps(customlist)
        config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
        ui_list.insertItem(0,item)
        ui_list.setCurrentIndex(0)
        
        if sub_ui != None:
            sub_ui.close()

    def add_item(self,  model, Form, is_subitem, data_receiver, main_field):
        
            data = {}
            for field in self.fields.keys():
                
                if self.fields[field].field_type == 'OneToOneField':
                    data[field] = vars(self)[field].currentData()

                elif self.fields[field].field_type == 'ManyToManyField':
                    data[field] =  getattr(self, field+'_data')

                elif self.fields[field].field_type == 'DateField':
                    data[field] =  getattr(self, field).date().toPyDate().isoformat()

                else:
                    data[field] = getattr(vars(self)[field] , self.fields[field].Get_UI_Value_Function  )()
                    
            if (not is_subitem):
                if chack_static_statement_status(model.add_conditions, self.model.INSApp, self.item_obj, data = data):
                    model.create(dict_inner_data = data)
                    Form.close()

            else:
                data_receiver(data, main_field)
                Form.close()

    def edit_item(self, Form, item):
        data = {}
        for field in item.model.fields.keys():

            if item.model.fields[field].field_type == 'OneToOneField':
                setattr( item, field, vars(self)[field].currentData())

            elif item.model.fields[field].field_type == 'ManyToManyField':
                dict_data = getattr(self, field+'_data')
                setattr(self.item_obj, field, dict_data)

            elif item.model.fields[field].field_type == 'DateField':
                setattr(self.item_obj, field, vars(self)[field].date().toPyDate().isoformat())
                

            else:
                setattr( item, field, getattr(vars(self)[field] , item.model.fields[field].Get_UI_Value_Function  )())

        item.save(call_on_edit = True)
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


    def cancel_op(self):
        ansower = QtWidgets.QMessageBox.question(self.Form , self.translate('Cancel Confirm') , self.translate('are you sure you want to exit?')+'\n'+self.translate('your changes will not be saves'))
        if ansower==QtWidgets.QMessageBox.Yes:
            self.Form.close()


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

        if obj_mode:
            self.translate = model.INSApp.translate

        else:
            self.translate = app.translate
            

        if not edit_mode and obj_mode:
            self.item_obj = model.temporary_item()

        Form.setObjectName("Form")
        Form.resize(400, 300)
        if obj_mode:
            Form.setWindowTitle(self.translate('add '+model.__class__.__name__.replace('_',' ').title() ))
            Form.setStyleSheet(model.INSApp.qss_style)

        else:
            Form.setWindowTitle(app.translate(title))
            Form.setStyleSheet(app.qss_style)
        
        
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        if edit_mode:
            self.edit_btn = QtWidgets.QPushButton(Form)
            self.edit_btn.setObjectName(u"edit_btn")
            self.edit_btn.setToolTip(self.translate('edit'))
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

            self.gridLayout_2.addWidget(self.add_btn, 1, 2, 1, 1)

        
        self.cancel_btn = QtWidgets.QPushButton(Form)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setToolTip(self.translate('cancel'))
        self.cancel_btn.clicked.connect(self.cancel_op)
        self.cancel_btn.setMinimumSize(QSize(30, 30))
        self.cancel_btn.setMaximumSize(QSize(30, 30))

        self.gridLayout_2.addWidget(self.cancel_btn, 1, 1, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        position_index = 0
        fields_list = []
        current_field_index = 0
        dictlist_4_sublist = [] # to make sure that sublist loaded into ui
        for field in self.fields.keys():
            
            fields_list.append(field)
            current_field_index +=1
            
            #fields 
            ########################################################################
            ########################################################################

            if self.fields[field].field_type == 'ListField':
                setattr(self, field, QtWidgets.QComboBox(Form) )
                ui_field = vars(self)[field]
                ui_field.setObjectName(field)

                item_text = ''
                for item in self.fields[field].items_list:# set all items
                    ui_field.addItem(item)

                if self.fields[field].data_from_DictField != None:
                    
                    DictField_obj = self.model.fields[self.fields[field].data_from_DictField]
                    current_DF_Text = getattr(self.pui,self.fields[field].data_from_DictField ).currentText()
                    
                    for item in DictField_obj.item_dict[current_DF_Text]:# set all items
                        ui_field.addItem(item)

                if edit_mode:# set current item
                    if obj_mode:
                        current_item_text = getattr(item_obj,field)

                    else:
                        current_item_text = dict_data[field]

                    if ui_field.findText( current_item_text )>-1:
                        ui_field.setCurrentIndex( ui_field.findText(current_item_text ))

                self.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)


            elif self.fields[field].field_type == 'CustomListField':
                
                
                setattr(self, field+'LayoutWidget', QWidget(Form) )
                horizontalLayoutWidget = getattr(self, field+'LayoutWidget')

                horizontalLayoutWidget = QWidget(Form)
                horizontalLayoutWidget.setObjectName(field+"horizontalLayoutWidget")

                setattr(self, field+'Layout', QHBoxLayout(horizontalLayoutWidget) )
                horizontalLayout = getattr(self, field+'Layout')
                horizontalLayout.setObjectName(field+"horizontalLayout")
                horizontalLayout.setContentsMargins(0, 0, 0, 0)

                setattr(self, field, QComboBox(horizontalLayoutWidget))
                comboBox = getattr(self, field)
                comboBox.setObjectName(field)

                
                if self.fields[field].list_name not in config['CustomLists']:
                    config['CustomLists'][ self.fields[field].list_name  ] = '[]'
                    config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
                
                list_items = json.loads(config['CustomLists'][ self.fields[field].list_name  ])
                for it in list_items:
                    comboBox.addItem(it)

                if edit_mode:# set current item
                    if obj_mode:
                        current_item_text = getattr(item_obj,field)
                    else:
                        current_item_text = dict_data[field]

                    if ui_field.findText( current_item_text )>-1:
                        ui_field.setCurrentIndex( ui_field.findText(current_item_text ))

                    else:
                        self.add_customlist_item( self.fields[field].list_name  , current_item_text, ui_field)

                horizontalLayout.addWidget(comboBox)

                setattr(self, field+'add_btn', QPushButton(horizontalLayoutWidget))
                pushButton = getattr(self, field+'add_btn')
                pushButton.setObjectName( field+"add_btn")
                pushButton.setMinimumSize(QSize(25, 25))
                pushButton.setMaximumSize(QSize(25, 25))
                getattr(self, field+'add_btn').clicked.connect(partial(add_costomlist_item_Window, self, self.add_customlist_item, self.fields[field].list_name, comboBox))
                horizontalLayout.addWidget(pushButton)
                self.gridLayout.addWidget(horizontalLayoutWidget, position_index, 1, 1, 1)





            elif self.fields[field].field_type == 'DictField':

                setattr(self, field, QtWidgets.QComboBox(Form) )
                ui_field = vars(self)[field]
                ui_field.setObjectName(field)
                
                for item in self.fields[field].item_dict:#set all dict items
                    ui_field.addItem(str(item))

                if edit_mode:# select current item
                    if obj_mode:
                        item_text = getattr(item_obj, field)
                    
                    else:
                        item_text = dict_data[field]

                    if type(item_text) == str:
                        item_text = item_text

                    else:
                        item_text = str(item_text)


                    if ui_field.findText( item_text )>-1:
                        ui_field.setCurrentIndex( ui_field.findText( item_text ) )

                subfields = self.fields[field].subfields
                for subfield in subfields:
                    dictlist_4_sublist.append({
                                'subfield_name' : subfield,
                                'mainfield_name':field,
                            })
                            

                ui_field.currentIndexChanged.connect(partial(self.change_subdict_field, [field, self.fields[field].subfields, self.fields]))
                self.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)

            elif self.fields[field].field_type == 'OneToOneField':

                setattr(self, field, QtWidgets.QComboBox(Form) )
                ui_field = vars(self)[field]
                ui_field.setObjectName(field)
                
                objs = getattr(model.INSApp, self.fields[field].model).objects
                
                item_text = ''
                for obj in objs:
                    ui_field.addItem(str(obj), obj.id)

                if edit_mode:# set current item
                    if obj_mode:
                        current_item_text = getattr(model.INSApp, self.fields[field].model).get(id = getattr(item_obj, field))

                    else:
                        current_item_text = dict_data[field]

                    if ui_field.findText( str(current_item_text) )>-1:
                        ui_field.setCurrentIndex( ui_field.findText(str(current_item_text)))


                self.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)

            elif self.fields[field].field_type == 'ManyToManyField':

                setattr(self, field+'_gridLayoutWidget', QWidget() )
                gridLayoutWidget = vars(self)[field+'_gridLayoutWidget']
                gridLayoutWidget.setObjectName(field+"_gridLayoutWidget")

                setattr(self, field+'_gridLayout',  QGridLayout(gridLayoutWidget))
                gridLayout = vars(self)[field+'_gridLayout']
                gridLayout.setObjectName(field+'_gridLayout')
                gridLayout.setContentsMargins(2, 2, 2, 2)

                setattr(self, field+'_add_button', QPushButton(gridLayoutWidget))              
                add_button = vars(self)[field+'_add_button']
                add_button.setObjectName(field+"add_button")
                add_button.setToolTip(self.translate('add'))
                add_button.clicked.connect( partial(self.call_add_subitem_window, [self.fields[field].subfields, field,self.fields[field] ]) )
                gridLayout.addWidget(add_button, 0, 2, 1, 1)

                setattr(self, field+'_remove_button', QPushButton(gridLayoutWidget))
                remove_button = vars(self)[field+'_remove_button']
                remove_button.setObjectName(field+"_remove_button")
                remove_button.setToolTip(self.translate('remove'))
                remove_button.clicked.connect( partial(self.remove_subitem, field))
                gridLayout.addWidget(remove_button, 0, 1, 1, 1)

                setattr(self, field+'_listWidget', QListWidget(gridLayoutWidget))
                listWidget = vars(self)[field+'_listWidget']
                listWidget.setObjectName(field+'_listWidget')
                listWidget.itemDoubleClicked.connect(partial(self.call_edit_subitem_window, listWidget, field ))

                gridLayout.addWidget(listWidget, 1, 0, 1, 3)


                if edit_mode:
                    if obj_mode:
                        fields_data = getattr(self.item_obj, field)
                    else:
                        fields_data = dict_data[field]

                    if type(fields_data) == str:
                        setattr(self, field+'_data', json.loads(fields_data.replace("'",'"')) )
                    else:
                        setattr(self, field+'_data', fields_data)

                    dict_data = getattr(self, field+'_data')

                    for subfield in dict_data:
                        view_name = item_obj.model.fields[field].view_name
                        
                        
                        view_name = replace_variable_value(view_name, data = subfield)
                        if type(view_name) not in [str, int]:
                            view_name = ''.join([ str(i) for i in view_name])

                        view_name = str(view_name)

                        item_ui = QtWidgets.QListWidgetItem()
                        item_ui.setText(view_name)
                        item_ui.setToolTip(replace_variable_value( item_obj.model.fields[field].tooltip,data = subfield))
                        item_ui.setData(6,subfield)
                        listWidget.addItem(item_ui)

                else: # creation mode
                    setattr(self, field+'_data', [])

                self.gridLayout.addWidget(gridLayoutWidget, position_index, 1, 1, 1)
               

            
            elif self.fields[field].field_type == 'DateField':
                setattr(self, field, self.fields[field].UI_Field(Form) )
                ui_field = vars(self)[field]
                ui_field.setObjectName(field)
                ui_field.setDisplayFormat('MM/dd/yyyy')
                
                if edit_mode:
                    if obj_mode:
                        field_value = str(getattr(self.item_obj, field))
                    else:
                        field_value = dict_data[field]

                    ui_field.setDate(datetime.date.fromisoformat(field_value))

                self.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)


            else:
                setattr(self, field, self.fields[field].UI_Field(Form) )
                ui_field = vars(self)[field]
                ui_field.setObjectName(field)
                for pr in self.fields[field].properties:
                    getattr(ui_field, pr['property_name'])(pr['value'])
                
                if edit_mode:
                    if obj_mode:
                        field_value = self.fields[field].TYPE(getattr(self.item_obj, field) )
                    else:
                        field_value = self.fields[field].TYPE(dict_data[field])

                    getattr(ui_field, self.fields[field].Set_UI_Value_Function )(field_value)

                self.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)

            # label
            self.label = QtWidgets.QLabel(Form)
            self.label.setObjectName(field+"label")
            self.label.setText( self.translate(field.replace('_',' ').title()))
            self.gridLayout.addWidget(self.label, position_index, 0, 1, 1)

            position_index+=1
        print(dictlist_4_sublist)
        for DL_subfield in dictlist_4_sublist:
                DL_ui_field = vars(self)[DL_subfield['mainfield_name']]
                DL_items    = self.fields[DL_subfield['mainfield_name']].item_dict
                SF          = vars(self)[DL_subfield['subfield_name']]
                

                SF.clear()
                for i in DL_items[DL_ui_field.currentText()]:
                    SF.addItem(i)
                if edit_mode and obj_mode:
                    current_SF  = vars(self.item_obj)[DL_subfield['subfield_name']]
                    if SF.findText( current_SF )>-1:
                        SF.setCurrentIndex( SF.findText( current_SF ) )
                    

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 3)

        




def create_item_window(app, model):
    
    app.UI.subwindow = QtWidgets.QDialog()

    ui = View_Item_Ui_Form()
    ui.setupUi(app.UI.subwindow, model = model , fields = model.fields, pui= app.UI)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()




def edit_item_window(item):
    app = item.data(6).model.INSApp
    app.UI.subwindow = QtWidgets.QDialog()

    ui = View_Item_Ui_Form()
    ui.setupUi(app.UI.subwindow, model = item.data(6).model , fields= item.data(6).model.fields  , item_obj = item.data(6), edit_mode=True, pui= app.UI)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()




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
        self.gridLayout.addWidget(self.item, 0, 0, 1, 1)
        self.add_btn = QtWidgets.QPushButton(Form)
        self.add_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(lambda: data_receiver(list_name, self.item.text(), ui_list, Form))
        self.gridLayout.addWidget(self.add_btn, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_btn.setText(_translate("Form", "ADD"))


def add_costomlist_item_Window(main_ui, data_receiver, list_name, ui_list):
    
    main_ui.subwindow = QtWidgets.QDialog()

    ui = add_costomlist_item_Form()
    ui.setupUi(main_ui.subwindow, data_receiver, list_name, ui_list)

    main_ui.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    main_ui.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    main_ui.subwindow.show()



