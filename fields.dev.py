from PyQt5 import QtWidgets
from frame import *
from functools import partial
import datetime

class Fields(object):

    # position [ x, y, x stretching, y stretching ]


    class Field(object):
        custom_init = None

        def __init__(self, **kwargs ):

            for var in kwargs.keys(): # defind all variabels in kwargs 
                setattr(self, var, kwargs[var])

            if 'label' not in vars(self):
                self.label = self.name

            if self.custom_init != None:
                self.custom_init()



    class TextField(Field):
        default = ''
        data_type = str



        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_text_field',
                    'object'    : QtWidgets.QLineEdit,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)

            return FrameW

    class TextBox(Field):
        default = ''
        data_type = str

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [1,0,0,0],
                    'name'      : self.name+'_text_box',
                    'object'    : QtWidgets.QTextEdit,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)

            return FrameW



    class IntegerField(Field):
        default = 0
        data_type = int

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_integer_field',
                    'object'    : QtWidgets.QSpinBox,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)

            return FrameW


    class FloatField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_float_field',
                    'object'    : QtWidgets.QDoubleSpinBox,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)

            return FrameW
    
    class BoolField(Field):
        default = False
        data_type = bool
        on_true_frame_fields = {}
        on_false_frame_fields = {}

        def create_ui_field(self):
            self.on_true_frame_fields = {
                    'field_1'  : Fields.TextField(name = 'Field_1'),
                    'field_2'  : Fields.IntegerField(name = 'Field_2'),
                }

            self.osn_false_frame_fields = {
                    'field_1'  : Fields.IntegerField(name = 'Field_1'),
                    'field_2'  : Fields.TextField(name = 'Field_2'),
                }
        
            
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_bool_field',
                    'object'    : QtWidgets.QCheckBox,
                    'type'      : 'Qt-type'
                },

            ]
            
            self.FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(self.FrameW, self.name+'_label').setText(self.label)

            
            ## on true frame


            self.on_true_frame_objects = []
            row = 0
            for obj_name in self.on_true_frame_fields:
                obj = self.on_true_frame_fields[obj_name]
                ui_obj = obj.create_ui_field(self.FrameW.frame)

                self.on_true_frame_objects.append({
                    'position'  : [row,0,0,0],
                    'name'      : obj.name,
                    'object'    : ui_obj,
                    'type'      : 'FrameWidget-object'
                }
                )
                row+=1


            
            
            self.on_True_FramWidget = FrameWidget(self.FrameW.frame, self.name+'_on_True_frame', self.on_true_frame_objects)
            self.FrameW.add_ui_object(
                {
                    'position'  : [1,0,1,0],
                    'name'      : self.name+'_on_true_frame',
                    'object'    : self.on_True_FramWidget,
                    'type'      : 'FrameWidget-object'
                }
            )



            ## on false frame

            self.on_false_frame_objects = []
            row = 0
            for obj_name in self.on_false_frame_fields:
                obj = self.on_false_frame_fields[obj_name]
                ui_obj = obj.create_ui_field(self.FrameW.frame)

                self.on_false_frame_objects.append({
                    'position'  : [row,0,0,0],
                    'name'      : obj.name,
                    'object'    : ui_obj,
                    'type'      : 'FrameWidget-object'
                }
                )
                row+=1


            self.on_False_FramWidget = FrameWidget(self.FrameW.frame, self.name+'_on_False_frame', self.on_false_frame_objects)
            self.FrameW.add_ui_object(
                {
                    'position'  : [2,0,1,0],
                    'name'      : self.name+'_on_false_frame',
                    'object'    : self.on_False_FramWidget,
                    'type'      : 'FrameWidget-object'
                }
            )



            def checkbox_clicked(status):
                getattr(self.FrameW, self.name+'_on_true_frame').setVisible(status)
                getattr(self.FrameW, self.name+'_on_false_frame').setVisible(status*(-1) +1)


            checkbox_obj = getattr(self.FrameW, self.name+'_bool_field')
            checkbox_obj.clicked.connect(checkbox_clicked)
            checkbox_clicked(checkbox_obj.isChecked())

            return self.FrameW


    class RadioButtonsField(Field):
        default = -1
        data_type = int
        radio_buttons = {}  # button_name: value
        buttons_fields = {} # button_value: fields

        def create_ui_field(self):
            radio_buttons = {
                'r_1' : 1,
                'r_2' : 2,
                'r_3' : 3,
                'r_4' : 4,
            }
            self.buttons_fields = { 2: {
                    'field_1'  : Fields.IntegerField(name = 'Field_1'),
                    'field_2'  : Fields.TextField(name = 'Field_2'),
            }}


            

            self.ui_objects_list = []
            row = 0
            for button in radio_buttons:
                self.ui_objects_list.append(
                    {
                        'position'  : [row,0,0,0],
                        'name'      : self.name+'_label_'+button,
                        'object'    : QtWidgets.QLabel,
                        'type'      : 'Qt-type'
                    })
                self.ui_objects_list.append(
                    {
                        'position'  : [row,1,0,0],
                        'name'      : self.name+'_button_field_'+str(radio_buttons[button]),
                        'object'    : QtWidgets.QRadioButton,
                        'type'      : 'Qt-type'
                    },
                
                )
                row+=1
            
            
            self.FrameW = FrameWidget(self.name, self.ui_objects_list)
            
            for button_value in self.buttons_fields:
                self.buttons_fields_frame_objects = []
                setattr(self, 'buttons_fields_frame_objects_'+str(button_value), [])
                row_2 = 0
                for obj_name in  self.buttons_fields[button_value]:
                    obj = self.buttons_fields[button_value][obj_name]
                    ui_obj = obj.create_ui_field(self.FrameW.frame)

                    getattr(self, 'buttons_fields_frame_objects_'+str(button_value)).append({
                        'position'  : [row,0,0,0],
                        'name'      : obj.name,
                        'object'    : ui_obj,
                        'type'      : 'FrameWidget-object'
                    }
                    )
                    row_2+=1
                
                
                setattr(self, 'radio_button_frame_value_'+str(button_value), FrameWidget(self.FrameW.frame, 'radio_button_frame_value_'+str(button_value), getattr(self, 'buttons_fields_frame_objects_'+str(button_value))))
                self.FrameW.add_ui_object(
                    {
                        'position'  : [row,0,1,0],
                        'name'      : 'radio_button_frame_value_'+str(button_value),
                        'object'    : getattr(self, 'radio_button_frame_value_'+str(button_value)),
                        'type'      : 'FrameWidget-object'
                    }
                )
                row+=1


            def radio(current_button):
                current_value = current_button.value
                
                for value in self.buttons_fields.keys():
                    frame = getattr(self, 'radio_button_frame_value_'+str(value))
                    frame.frame.setVisible(current_value == value)
                    

            for button in radio_buttons:
                getattr(self.FrameW, self.name+'_label_'+button).setText(button)

                button_obj = getattr(self.FrameW, self.name+'_button_field_'+str(radio_buttons[button]))
                button_obj.value = radio_buttons[button]
                button_obj.clicked.connect(partial( radio,button_obj))

            try:# set default checked value
                getattr(self.FrameW, self.name+'_button_field_'+str(self.default)).setChecked(True)
            except:
                pass

            return self.FrameW
    

    class DateField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_date_field',
                    'object'    : QtWidgets.QDateEdit,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)
            getattr(FrameW, self.name+'_date_field').setDisplayFormat('dd/MM/yyyy')
            getattr(FrameW, self.name+'_date_field').setDate(datetime.date.today())
            
            return FrameW
        

    class TimeField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_time_field',
                    'object'    : QtWidgets.QTimeEdit,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)
            getattr(FrameW, self.name+'_time_field').setTime(datetime.datetime.now().time())
            
            return FrameW


    class DateTimeField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_date_time_field',
                    'object'    : QtWidgets.QDateTimeEdit,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)
            getattr(FrameW, self.name+'_date_time_field').setDisplayFormat('d/M/yyyy | hh:mm AP')
            getattr(FrameW, self.name+'_date_time_field').setDateTime(datetime.datetime.now())
            
            return FrameW

    
    class DropdownField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_list_field',
                    'object'    : QtWidgets.QComboBox,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)
            
            

            for item in self.items_data:
                getattr(FrameW, self.name+'_list_field').addItem(item[0], item[1])
            

            return FrameW

    
    class Addable_DropdownField(Field):
        default = 0
        data_type = float

        def create_ui_field(self):
            self.ui_objects_list = [
                {
                    'position'  : [0,0,0,0],
                    'name'      : self.name+'_label',
                    'object'    : QtWidgets.QLabel,
                    'type'      : 'Qt-type'
                },
                {
                    'position'  : [0,1,0,0],
                    'name'      : self.name+'_list_field',
                    'object'    : QtWidgets.QComboBox,
                    'type'      : 'Qt-type'
                }
            ]
            FrameW = FrameWidget(self.name, self.ui_objects_list)
            getattr(FrameW, self.name+'_label').setText(self.label)

            for item in self.items_data:
                getattr(FrameW, self.name+'_list_field').addItem(item[0], item[1])
            
            return FrameW






#########################################################################


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(549, 492)
        
        self.main_gridLayout = QtWidgets.QGridLayout(Form)
        self.main_gridLayout.setObjectName(u"main_gridLayout")
        
        items_d = [
            ('4544',3),
            ('4545',4),
            ('4546',2),
            ('4547',6),
            
        ]

        f = Fields.DropdownField(name = 'test_field', items_data = items_d)
        fw = f.create_ui_field()
        fw.frame.parent = Form

        fw.frame.setGeometry(QtCore.QRect(13, 230, 411, 321))
        fw.frame.setStyleSheet('background-color:rgb(255,255,255);')

        self.main_gridLayout.addWidget(fw.frame, 0, 0, 1, 1)
        
        
def edit_item_window():
    app = QtWidgets.QApplication(sys.argv)
    subwindow = QtWidgets.QDialog()

    ui = Ui_Form()
    subwindow.ui = ui
    ui.setupUi(subwindow)

    subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    subwindow.show()
    app.exec_()
    
edit_item_window()