
from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt


class Fields(object):

    class Field(object):
        def __init__(self, visible_on_add = True, visible_on_edit = True, **kwargs ):
            self.visible_on_add     = visible_on_add
            self.visible_on_edit    = visible_on_edit

            for var in kwargs.keys(): # defind all variabels in kwargs 
                setattr(self, var, kwargs[var])


    class CharField(Field):
        field_type              = 'CharField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QLineEdit
        Get_UI_Value_Function   = 'text'
        Set_UI_Value_Function   = 'setText'
        default                 =  ''
    
    class TextField(Field):
        field_type              = 'TextField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QTextEdit
        Get_UI_Value_Function   = 'toPlainText'
        Set_UI_Value_Function   = 'setPlainText'
        default                 =  ''

    class IntegerField(Field):
        field_type              = 'IntegerField'
        TYPE                    = int
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QSpinBox
        Get_UI_Value_Function   = 'value'
        Set_UI_Value_Function   = 'setValue'
        default                 =  0

    class FloatField(Field):
        field_type              = 'FloatField'
        TYPE                    = float
        data_base_type          = 'REAL'
        UI_Field                = QtWidgets.QDoubleSpinBox
        Get_UI_Value_Function   = 'value'
        Set_UI_Value_Function   = 'setValue'
        default                 =  0.0

    class BoolField(Field):
        field_type              = 'BoolField'
        TYPE                    = bool
        data_base_type          = 'INTEGER'
        UI_Field                = QtWidgets.QCheckBox
        Get_UI_Value_Function   = 'isChecked'
        Set_UI_Value_Function   = 'setChecked'
        default                 =  False

    class DateField(Field):
        field_type              = 'DateField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QDateEdit
        default                 =  False


    class ListField(Field):
        field_type              = 'ListField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 = []
        items_list              = []
        data_from_DictField     = None


    class DictField(Field):
        field_type              = 'DictField'
        TYPE                    = str
        data_base_type          = 'TEXT'
        UI_Field                = QtWidgets.QComboBox
        Get_UI_Value_Function   = 'currentText'
        default                 =  ''



    class OneToOneField(Field):
        field_type              = 'OneToOneField'
        TYPE                    = int
        data_base_type          = 'int'
        UI_Field                = QtWidgets.QComboBox
        default                 =  ''
        

    class ManyToManyField(Field):
        add_conditions          = {'statement':'True','error_msg':''}
        call_add_conditions     = {'statement':'True','error_msg':''}
        field_type              = 'ManyToManyField'
        TYPE                    = list
        data_base_type          = 'BLOB'
        default                 =  []
        on_add                  = None
        on_delete               = None

    
        
        