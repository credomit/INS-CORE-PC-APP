from PyQt5 import QtWidgets, QtCore, Qt
import sys

class Model_Form(object):
    def __init__(self, fields) -> None:
        self.fields = self.fields_class(self, fields)
        

    class fields_class:
        def __init__(self, form, fields):
            self.__form__ = form

            # fields = {field_name : field_obj }
            for field in fields:
                setattr(self, field, fields[field])


class FrameWidget(object):
    def __init__(self, frame_name, ui_objects, app):

        self.frame  = QtWidgets.QFrame()
        self.APP    = app

        self.frame.setObjectName(frame_name)
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName(frame_name+"_gridLayout")


        for obj in ui_objects:
            self.add_ui_object(obj)    



    
    def add_ui_object(self, obj):
            if {'name', 'object', 'position', 'type'}.issubset(set(obj.keys())):
                
                if obj.get('type') == 'Qt-type':
                    try:
                        setattr(self, obj.get('name'), obj.get('object')(self.frame))
                    except:
                        setattr(self, obj.get('name'), obj.get('object'))

                    try:
                        getattr(self, obj.get('name')).setObjectName(obj.get('name'))
                    except:
                        pass
                
                elif obj.get('type') == 'FrameWidget-object':
                    setattr(self, obj.get('name'), obj.get('object').frame)
                    

                if obj.get('size') != None:
                    getattr(self, obj.get('name')).setMaximumSize(Qt.QSize(obj.get('size')[0], obj.get('size')[1]))
                    getattr(self, obj.get('name')).setMinimumSize(Qt.QSize(obj.get('size')[0], obj.get('size')[1]))
                    
                if obj.get('Min-size') != None:
                    getattr(self, obj.get('name')).setMinimumSize(Qt.QSize(obj.get('Min-size')[0], obj.get('Min-size')[1]))
                    
                if obj.get('Max-size') != None:
                    getattr(self, obj.get('name')).setMaximumSize(Qt.QSize(obj.get('Max-size')[0], obj.get('Max-size')[1]))
                    

                if obj.get('text-align') != None:
                   
                    if obj.get('text-align') == 'right':
                        getattr(self, obj.get('name')).setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

                    elif obj.get('text-align') == 'left':
                        getattr(self, obj.get('name')).setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                        
                    elif obj.get('text-align') == 'center':
                        getattr(self, obj.get('name')).setAlignment(QtCore.Qt.AlignCenter)

                pos = obj.get('position')
                self.gridLayout.addWidget(getattr(self, obj.get('name')), pos[0], pos[1], pos[3], pos[2])    

                if obj.get('UIproperty') != None:
                    for i in obj.get('UIproperty'):
                        getattr(self, obj.get('name')).setProperty(i, obj.get('UIproperty')[i])            

                if obj.get('icon') != None:
                    getattr(self, obj.get('name')).setIcon(self.APP.Styler.get_icon(obj.get('icon')))

                


            else:
                missed_info = str({'name', 'object', 'position'} - set(obj.keys()))
                exit()

