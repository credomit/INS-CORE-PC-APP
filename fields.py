
from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
import configparser, os, json, datetime

class Fields(object):

    class Field(object):
        properties_func = None
        default = None
        editable = True
        def __init__(self, visible_on_add = True, visible_on_edit = True, **kwargs ):

            self.visible_on_add     = visible_on_add
            self.visible_on_edit    = visible_on_edit
            

            for var in kwargs.keys(): # defind all variabels in kwargs 
                setattr(self, var, kwargs[var])

        def view(self, UI, Form, field_name, position_index, field_obj = None):
                setattr(UI, field_name, UI.fields[field_name].UI_Field(Form) )
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)

                self.ui_field.setEnabled(self.editable)
                
                for pr in UI.fields[field_name].properties:
                    getattr(self.ui_field, pr['property_name'])(pr['value'])
                
                if UI.edit_mode:
                    if UI.obj_mode:
                        field_value = UI.fields[field_name].TYPE(getattr(UI.item_obj, field_name) )
                    else:

                        field_value = UI.fields[field_name].TYPE(UI.dict_data[field_name])

                    getattr(self.ui_field, UI.fields[field_name].Set_UI_Value_Function )(field_value)

                UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                if self.properties_func != None:
                    self.properties_func(self.ui_field)


        def get_data(self):

            data = getattr( self.ui_field, self.Get_UI_Value_Function)()
            return data
            



    class CharField(Field):
        field_type              = 'CharField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QLineEdit
        Get_UI_Value_Function   = 'text'
        Set_UI_Value_Function   = 'setText'
        default                 =  ''
        properties              = []
    
    class TextField(Field):
        field_type              = 'TextField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QTextEdit
        Get_UI_Value_Function   = 'toPlainText'
        Set_UI_Value_Function   = 'setPlainText'
        default                 =  ''
        properties              = []

    class IntegerField(Field):
        field_type              = 'IntegerField'
        TYPE                    = int
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QSpinBox
        Get_UI_Value_Function   = 'value'
        Set_UI_Value_Function   = 'setValue'
        default                 =  0
        properties              = [
            {
                'property_name' : 'setMaximum',
                'value'         : 2147483647
            }
        ]
        
    class FloatField(Field):
        field_type              = 'FloatField'
        TYPE                    = float
        data_base_type          = 'REAL'
        UI_Field                = QtWidgets.QDoubleSpinBox
        Get_UI_Value_Function   = 'value'
        Set_UI_Value_Function   = 'setValue'
        default                 =  0.0
        properties              = [
            {
                'property_name' : 'setMaximum',
                'value'         : 2147483647
            }
        ]
        def properties_func(self, ui_field):
            self.ui_field.setDecimals(5)


    class BoolField(Field):
        field_type              = 'BoolField'
        TYPE                    = bool
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QCheckBox
        Get_UI_Value_Function   = 'isChecked'
        Set_UI_Value_Function   = 'setChecked'
        default                 =  False
        properties              = []

        def view(self, UI, Form, field_name, position_index, field_obj = None):
                setattr(UI, field_name, UI.fields[field_name].UI_Field(Form) )
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                self.ui_field.setEnabled(self.editable)
                for pr in UI.fields[field_name].properties:
                    getattr(self.ui_field, pr['property_name'])(pr['value'])
                
                if UI.edit_mode:
                    if UI.obj_mode:
                        field_value = UI.fields[field_name].TYPE(int(getattr(UI.item_obj, field_name) ))
                    else:

                        field_value = UI.fields[field_name].TYPE(int(UI.dict_data[field_name]))

                    getattr(self.ui_field, UI.fields[field_name].Set_UI_Value_Function )(field_value)

                UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                if self.properties_func != None:
                    self.properties_func(self.ui_field)


    class DateField(Field):
        field_type              = 'DateField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QDateEdit
        default                 =  None
        properties              = []


        def get_data(self):
            data = self.ui_field.date().toPyDate().isoformat()
            return data
            

        def view(self, UI, Form, field_name, position_index, field_obj = None, field_gridLayout = None, view_on_main_window = False):
                if view_on_main_window:
                    setattr(UI, field_name, field_obj.UI_Field(Form) )
                else:
                    setattr(UI, field_name, UI.fields[field_name].UI_Field(Form) )
                    
                
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
                        field_value = str(getattr(UI.item_obj, field_name))
                    else:
                        field_value = UI.dict_data[field_name]
                    self.ui_field.setDate(datetime.date.fromisoformat(field_value))

                if not view_on_main_window:
                    UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)

                else:
                    field_gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)


    class ListField(Field):
        field_type              = 'ListField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 = []
        items_list              = []
        data_from_DictField     = None
        properties              = []
        on_change               = None
        def view(self, UI, Form, field_name, position_index, field_obj = None):                
                setattr(UI, field_name, QtWidgets.QComboBox(Form) )
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                self.ui_field.setEnabled(self.editable)

                for item in UI.fields[field_name].items_list:# set all items
                    self.ui_field.addItem(item)

                if UI.fields[field_name].data_from_DictField != None:
                    
                    DictField_obj = UI.model.fields[UI.fields[field_name].data_from_DictField]
                    current_DF_Text = getattr(UI.pui,UI.fields[field_name].data_from_DictField ).currentText()
                    
                    for item in DictField_obj.item_dict[current_DF_Text]:# set all items
                        self.ui_field.addItem(item)

                if UI.edit_mode:# set current item
                    if UI.obj_mode:
                        current_item_text = getattr(UI.item_obj,field_name)

                    else:
                        current_item_text = UI.dict_data[field_name]

                    if self.ui_field.findText( current_item_text )>-1:
                        self.ui_field.setCurrentIndex( self.ui_field.findText(current_item_text ))

                UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)

                if UI.fields[field_name].on_change != None:
                    self.ui_field.currentIndexChanged.connect(partial(UI.fields[field_name].on_change, UI, self.ui_field, ui_loaded = True))
                    return {'on_load_function':[partial(UI.fields[field_name].on_change, UI, self.ui_field, ui_loaded = False),] }


    class CustomListField(Field):
        field_type              = 'CustomListField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 = []
        items_list              = []
        data_from_DictField     = None
        properties              = []

        def view(self, UI, Form, field_name, position_index, field_obj = None):

                config = configparser.ConfigParser()
                config.read( os.path.join('INSLPCModel','settings.ini'))

                setattr(UI, field_name+'LayoutWidget', QWidget(Form) )
                horizontalLayoutWidget = getattr(UI, field_name+'LayoutWidget')
                horizontalLayoutWidget.setEnabled(self.editable)

                horizontalLayoutWidget = QWidget(Form)
                horizontalLayoutWidget.setObjectName(field_name+"horizontalLayoutWidget")

                setattr(UI, field_name+'Layout', QHBoxLayout(horizontalLayoutWidget) )
                horizontalLayout = getattr(UI, field_name+'Layout')
                horizontalLayout.setObjectName(field_name+"horizontalLayout")
                horizontalLayout.setContentsMargins(0, 0, 0, 0)
                horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)

                setattr(UI, field_name, QComboBox(horizontalLayoutWidget))
                comboBox = getattr(UI, field_name)
                comboBox.setObjectName(field_name)
                self.ui_field = comboBox

                
                if UI.fields[field_name].list_name not in config['CustomLists']:
                    config['CustomLists'][ UI.fields[field_name].list_name  ] = '[]'
                    config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
                
                list_items = json.loads(config['CustomLists'][ UI.fields[field_name].list_name  ])
                for it in list_items:
                    comboBox.addItem(it)

                if UI.edit_mode:# set current item
                    if UI.obj_mode:
                        current_item_text = getattr(UI.item_obj,field_name)
                    else:
                        current_item_text = UI.dict_data[field_name]

                    if comboBox.findText( current_item_text )>-1:
                        comboBox.setCurrentIndex( comboBox.findText(current_item_text ))

                    else:
                        UI.add_customlist_item( UI.fields[field_name].list_name  , current_item_text, comboBox)

                horizontalLayout.addWidget(comboBox)

                setattr(UI, field_name+'add_btn', QPushButton(horizontalLayoutWidget))
                pushButton = getattr(UI, field_name+'add_btn')
                pushButton.setObjectName( field_name+"add_btn")
                pushButton.setMinimumSize(QSize(25, 25))
                pushButton.setMaximumSize(QSize(25, 25))
                pushButton.setIcon(UI.app.Styler.get_icon('add'))
                getattr(UI, field_name+'add_btn').clicked.connect(partial(add_costomlist_item_Window, UI, UI.add_customlist_item, UI.fields[field_name].list_name, comboBox))
                horizontalLayout.addWidget(pushButton)
                UI.gridLayout.addWidget(horizontalLayoutWidget, position_index, 1, 1, 1)



    class DictField(Field):
        field_type              = 'DictField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 =  ''
        properties              = []



        def view(self, UI, Form, field_name, position_index, field_obj = None):

                setattr(UI, field_name, QtWidgets.QComboBox(Form) )
                self.ui_field = vars(UI)[field_name]
                self.ui_field.setObjectName(field_name)
                self.ui_field.setEnabled(self.editable)

                for item in UI.fields[field_name].item_dict:#set all dict items
                    self.ui_field.addItem(str(item))

                if UI.edit_mode:# select current item
                    if UI.obj_mode:
                        item_text = getattr(UI.item_obj, field_name)
                    
                    else:
                        item_text = UI.dict_data[field_name]

                    if type(item_text) == str:
                        item_text = item_text

                    else:
                        item_text = str(item_text)


                    if self.ui_field.findText( item_text )>-1:
                        self.ui_field.setCurrentIndex( self.ui_field.findText( item_text ) )

                subfields = UI.fields[field_name].subfields
                dictlist_4_sublist = []
                for subfield in subfields:
                    dictlist_4_sublist.append({
                                'subfield_name' : subfield,
                                'mainfield_name':field_name,
                            })


                self.ui_field.currentIndexChanged.connect(partial(UI.change_subdict_field, [field_name, UI.fields[field_name].subfields, UI.fields]))
                UI.gridLayout.addWidget(self.ui_field, position_index, 1, 1, 1)
                return {'dictlist_4_sublist':dictlist_4_sublist }



    class OneToOneField(Field):
        field_type              = 'OneToOneField'
        TYPE                    = int
        data_base_type          = 'int'
        UI_Field                = QtWidgets.QComboBox
        default                 =  ''
        properties              = []
        on_change               = None

        def view(self, UI, Form, field_name, position_index, field_obj = None):

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
                        current_item_text = getattr(UI.model.INSApp, UI.fields[field_name].model).get(id = getattr(UI.item_obj, field_name))

                    else:
                        current_item_text = UI.dict_data[field_name]

                    if ui_field.findText( str(current_item_text) )>-1:
                        ui_field.setCurrentIndex( ui_field.findText(str(current_item_text)))

                if UI.fields[field_name].on_change != None:
                    ui_field.currentIndexChanged.connect(partial(UI.fields[field_name].on_change, UI, ui_field, ui_loaded = True))
                    
                UI.gridLayout.addWidget(ui_field, position_index, 1, 1, 1)
                if UI.fields[field_name].on_change != None:
                    return {'on_load_function':[partial(UI.fields[field_name].on_change, UI, ui_field, ui_loaded = False)] }
        
        def get_data(self):
                return self.ui_field.currentData()

    class ManyToManyField(Field):
        add_conditions          = {'statement':'True','error_msg':''}
        call_add_conditions     = {'statement':'True','error_msg':''}
        field_type              = 'ManyToManyField'
        TYPE                    = list
        data_base_type          = 'BLOB'
        default                 =  []
        on_add                  = None
        before_add              = None
        on_edit                 = None
        on_delete               = None
        properties              = []
        tooltip                 = '""'
        single_view             = False

        def view(self, UI, Form, field_name, position_index, field_obj = None):
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


                label = QtWidgets.QLabel(Form)
                label.setObjectName(field_name+"label")
                label.setAlignment(Qt.AlignCenter)
                label.setText( UI.translate(field_name.replace('_',' ').title()))
                gridLayout.addWidget(label, 0, 0, 1, 3)

                setattr(UI, field_name+'_add_button', QPushButton(gridLayoutWidget))              
                add_button = vars(UI)[field_name+'_add_button']
                add_button.setObjectName(field_name+"add_button")
                add_button.setToolTip(UI.translate('add'))
                add_button.setIcon(UI.app.Styler.get_icon('add'))
                add_button.setMinimumSize(QSize(25, 25))
                add_button.setMaximumSize(QSize(25, 25))
                add_button.clicked.connect( partial(UI.call_add_subitem_window, [UI.fields[field_name].subfields, field_name,UI.fields[field_name] ]) )
                gridLayout.addWidget(add_button, 1, 2, 1, 1)

                setattr(UI, field_name+'_remove_button', QPushButton(gridLayoutWidget))
                remove_button = vars(UI)[field_name+'_remove_button']
                remove_button.setObjectName(field_name+"_remove_button")
                remove_button.setToolTip(UI.translate('remove'))
                remove_button.setIcon(UI.app.Styler.get_icon('delete'))
                remove_button.setMinimumSize(QSize(25, 25))
                remove_button.setMaximumSize(QSize(25, 25))
                remove_button.setProperty('btn_type','delete')
                remove_button.clicked.connect( partial(UI.remove_subitem, field_name))
                gridLayout.addWidget(remove_button, 1, 1, 1, 1)

                setattr(UI, field_name+'_listWidget', QListWidget(gridLayoutWidget))
                if UI.obj_mode:
                    setattr(UI.item_obj, field_name+'_data', [])
                else:
                    UI.dict_data[field_name+'_data'] = []

                self.listWidget = vars(UI)[field_name+'_listWidget']
                self.listWidget.setObjectName(field_name+'_listWidget')
                self.listWidget.setMinimumSize(QSize(100, 100))
                self.listWidget.itemDoubleClicked.connect(partial(UI.call_edit_subitem_window, self.listWidget, field_name ))

                self.listWidget.setDragDropMode(QAbstractItemView.DragOnly)
                self.listWidget.setDefaultDropAction(Qt.MoveAction)
                self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
                self.listWidget.setMovement(QListView.Free)

                gridLayout.addWidget(self.listWidget, 2, 0, 1, 3)


                if UI.edit_mode:
                    if UI.obj_mode:
                        fields_data = getattr(UI.item_obj, field_name)
                    else:
                        fields_data = UI.dict_data[field_name]

                    if type(fields_data) == str:
                        print('dd',fields_data)
                        fields_data = json.loads(fields_data.replace("'",'"')) 

                    if UI.obj_mode:
                        setattr(UI.item_obj, field_name+'_data',fields_data )
                        dict_data = getattr(UI.item_obj, field_name+'_data')

                    else:
                        UI.dict_data[field_name] = fields_data
                        dict_data = UI.dict_data[field_name]


                    for subfield in dict_data:
                        view_name = UI.fields[field_name].view_name
                        
                        
                        view_name = replace_variable_value(view_name, data = subfield)
                        if type(view_name) not in [str, int]:
                            view_name = ''.join([ str(i) for i in view_name])

                        view_name = str(view_name)

                        item_ui = QtWidgets.QListWidgetItem()
                        item_ui.setText(view_name)
                        item_ui.setToolTip(replace_variable_value( UI.fields[field_name].tooltip,data = subfield))
                        item_ui.setData(6,subfield)
                        self.listWidget.addItem(item_ui)

                else: # creation mode
                    if UI.obj_mode:
                        setattr(UI.item_obj, field_name+'_data', [])

                    else:
                        UI.dict_data[field_name] = []
                
                if UI.ManyToManyField_pos == 1:
                    position_index-=1

                if UI.fields[field_name].single_view:
                    UI.gridLayout.addWidget(gridLayoutWidget, position_index, 0, 1, 2)

                else:
                    UI.gridLayout.addWidget(gridLayoutWidget, position_index, UI.ManyToManyField_pos, 1, 1)
                    UI.ManyToManyField_pos = (UI.ManyToManyField_pos * (-1)) +1


        def get_data(self):
            if self.UI.obj_mode:
                data = getattr(self.UI.item_obj, self.field_name+'_data')
            else:
                data = self.UI.dict_data[self.field_name]

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
