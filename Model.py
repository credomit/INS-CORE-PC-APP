# -*- coding: utf-8 -*-
from ast import arg
import re, sys, json, configparser,os
import sqlite3 as sql
from typing import Dict, Set, Tuple
from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtChart import QPieSeries, QChart, QChartView
from .windows_creator import *
from .translator import translator
from .export_csv import *
from pathlib import Path
from .preferences import *
import pyqtgraph as pg
import sys, random
from .styler import Styler
from pyqtgraph import QtCore as QtCoregraph
from pyqtgraph import QtGui as QtGuigraph
from types import MethodType
from .IN import *
from . import windows, DB,data_controller, windows_creator

import platform, threading
from INSLPCModel import configuration_ini
if platform.system() == 'Windows':
    from win10toast import ToastNotifier
else:
    import notify2


def replace_variable_value(item, text):
    if text != '':
        re_text = eval(text)
        if type(re_text) in [list, tuple, set]:
            re_text = list(re_text)
            re_text = [ str(i) for i in  re_text ]
            re_text = ''.join(list(re_text))

    else:
        re_text = ''
    return re_text






class INSAPP(object):

    

    def __init__(self, app_name, app_version, translateable_labels_and_buttons, translateable_tap_widgets ,app_file_type, app_logo, edition = 'standard' ,  preferences_call_btn = 'PREFERENCES_ACTION', taps_icons = {}):

        
        self.listed_items           = []
        self.translateable_labels   = translateable_labels_and_buttons
        self.translateable_tap_widgets = translateable_tap_widgets
        self.taps_icons             = taps_icons
        self.app_name               = app_name
        self.app_version            = app_version
        self.app_logo               = os.path.join(os.path.join(os.path.dirname( __file__ )),'..',app_logo)
        self.qss_style              = ''
        self.app_file_type          = app_file_type
        self.edition                = edition
        self.ModelClass             = Model
        self.windows_creator        = windows_creator
        
        self.UI_file                = 'main.ui'
        
        self.pyqt5_app              = QtWidgets.QApplication(sys.argv)
        
        self.MainWindow             = QtWidgets.QMainWindow()
        self.MainWindow.app         = self
        
        self.UI                     = uic.loadUi(self.UI_file, self.MainWindow)
        self.UI.setWindowTitle(app_name)
        self.UI.window_obj = self.UI
        
        self.MainWindow.closeEvent  = MethodType(self.closeEvent,self.MainWindow)
        self.Dicimal_Round          = int(configuration_ini.get_data(['INSLPCModel','settings.ini'])['default']['dicimal_round'])

        
        self.translator             = translator(self)
        self.translate              = self.translator.translate
        

        
        

        self.preferences_call_btn_name = preferences_call_btn
        self.preferences_call_btn   = getattr(self.UI, preferences_call_btn)
        self.preferences_call_btn.triggered.connect(lambda: open_preferences_window(self))
        self.UI.export_csv_button.triggered.connect(lambda: open_export_csv_window(self))
        self.Styler                 = Styler(self)
        
        if platform.system() == 'Windows':
            self.notifier = ToastNotifier()
        else:
            notify2.init(self.app_name)
        
        self.notify( title = 'notify' ,message = 'notify', type = 'notify', view_in_notifications_list = True)


        for tap_widget in self.taps_icons:
            for tap_index in self.taps_icons[tap_widget]:
                getattr(self.UI, tap_widget).setTabIcon(tap_index, self.Styler.get_icon(self.taps_icons[tap_widget][tap_index]))
        
        

        #dockWidgetContents_right, #dockWidgetContents_left{

        shadow_effects = {}
        shadowed_widgets = [self.UI.dockWidgetContents_right, self.UI.dockWidgetContents_left, self.UI.DashboardHandler]

        for widget in shadowed_widgets:
            shadow_effects[widget] = QtWidgets.QGraphicsDropShadowEffect()
            
            shadow_effects[widget].setBlurRadius(10.0)
            shadow_effects[widget].setColor(QColor(0, 0, 0, 60))
            shadow_effects[widget].setOffset(0)
            widget.setGraphicsEffect(shadow_effects[widget])

        

        

    def notify(self, title = 'notify' ,message = 'notify', type = 'notify', view_in_notifications_list = True):
        if platform.system() == 'Windows':
            threading.Thread(target= self.notifier.show_toast, args = (title,message, os.path.join(os.path.join(os.path.dirname( __file__ )),'..','main.ico'))).start()
        else:
            notify2.Notification(title,message, os.path.join(os.path.join(os.path.dirname( __file__ )),'..','main.ico')).show()
        
        if view_in_notifications_list:

            item_ui = QtWidgets.QListWidgetItem()
            item_ui.setText(title+'\n'+message)
            self.UI.notifications_list.addItem(item_ui)
        
    def closeEvent(self,r, event):
            close = QtWidgets.QMessageBox.question(self.UI,
	                                         "QUIT",
	                                         self.translate(f'Are you sure want to close {self.app_name}?'),
	                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def run(self):
        back_connections(self)
        INSCI(self)
        
        
        self.tables = {}
        for i in self.listed_items:
            
            self.tables[i.__name__] = list(i.fields.keys())+i.extra_DB_columns

        
        self.DataController         = data_controller.DataController(self)
        
        #loading_window(self)

        self.pyqt5_app.exec_()




    def run_main_window(self):
        
        step_value = int(100 / len(self.listed_items))
        for item in self.listed_items:
            self.LoadinWindow.ui.progressBar.setValue(self.LoadinWindow.ui.progressBar.value() + step_value)
            setattr(self, item.__name__ , item(INSApp = self ))
        
        self.LoadinWindow.hide()
        self.Styler.apply_style()
        self.UI.show()
        


class SubItem(object):
    def __init__(self, fields, model):
        self.model = model
        for var in fields.keys():
            setattr(self, var , fields[var] )
            
            if var in self.model.fields and self.model.fields[var].field_type == 'ManyToManyField':
                setattr(self, var+'_data' , [] )



class Item(object):

    ui_items = []
    ui_obj   = None
    UI_Forms = []
    
    def __init__(self, fields, model):
        
        self.model = model

        unloaded_fields = []
        for field in model.fields:
            if field not in list(fields.keys()):
                unloaded_fields.append(field)

        for field in unloaded_fields:
            fields[field] = ""

        self.data = self.data_class(fields.keys())
        self.data.item = self
        self.data.vars = fields.keys()
        
        for var in fields.keys():

            
            setattr(self.data, var, fields[var] )
            
            if var in self.model.fields and self.model.fields[var].field_type == 'ManyToManyField':# to remove
                setattr(self, var+'_data' , fields[var] )# to remove




    class data_class:
        def __init__(self, vars = []) -> None:
            for v in vars:
                
                setattr(self, v, None)

        def edit(self, data):
            new_data = data
            old_data = { bit: getattr(self, bit) for bit in self.vars}
            if self.item.model.before_save == None or self.item.model.before_save(new_data = new_data,  old_data = old_data,item = self.item):
                for field in list(new_data.keys()):
                    setattr(self, field, new_data.get(field))
                
                if self.item.model.on_edit != None:
                    self.item.model.on_edit(new_data = new_data, old_data = old_data, item = self.item)
            
            self.item.ui_obj.setText(self.item.__str__())
            self.item.model.INSApp.DataController.edit_item(self.item)

            for form in self.item.UI_Forms:
                form.set_data(new_data)


    def __str__(self):
        if self.model.custom_str != None:
            obj_text = self.model.custom_str(self)
        else:
            obj_text = replace_variable_value(self, self.model.view_name)
            



        return obj_text


    def get(self, field):
        field_obj = getattr(self, field)
        return getattr(field_obj, field_obj.Get_UI_Value_Function )()

    def delete(self):
        if self.model.before_delete == None or self.model.before_delete():
            ansower = QtWidgets.QMessageBox.question(self.model.INSApp.UI , self.model.INSApp.translate('Delete Confirm') , self.model.INSApp.translate('Are you sure do you want to delete')+' '+  str(self) +'?')

            if ansower==QtWidgets.QMessageBox.Yes:
                if self.model.before_delete==None or self.model.before_delete(self):
                    db_connection = sql.connect(self.model.INSApp.database_path)
                    db_connection.execute(f''' DELETE from {self.model.DBTableName} where id = {self.id} ''')
                    db_connection.commit() 
                    db_connection.close()
                    item_data = vars(self)
                    self.model.objects.remove(self)
                    print(self.model.ui_lists)
                    for lst in self.model.ui_lists.values():
                        lst.takeItem(lst.row(self.ui_obj))
                    
                    if self.model.on_delete != None:
                        self.model.on_delete(data = item_data, item = self)
                
        
        if self.model.on_delete != None:
            self.model.on_delete(item = self)

    def save(self, call_on_edit = False, call_before_edit = False):
        
            

        db_connection = sql.connect(self.model.INSApp.database_path)

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
                    value = json.dumps(value)
                    

                db_connection.execute(f''' UPDATE {self.model.DBTableName} set {field} = ? where id = {self.id} ''', [value,])
                new_data[field] = value

        if self.model.before_edit == None or (call_on_edit and self.model.before_edit(old_data = old_data, new_data = new_data)):
            db_connection.commit() 
            db_connection.close()
            
            self.ui_obj.setText(self.__str__())
            if self.model.on_edit != None and call_on_edit:
                self.model.on_edit(old_data = old_data, new_data = new_data )

            #update dashboard
            for mode in self.model.GRAPH_MODES:
                if getattr(self.model , "dashboard_frame_items_"+mode).currentData() == self:
                    getattr(self.model, mode+'_refresh_graph')()
            
            for mode in self.model.PIE_GRAPH_MODES:
                if getattr(self.model , "dashboard_pie_items_"+mode).currentData() == self:
                    getattr(self.model, mode+'_refresh_pie')()
            
            return True

        else:
            db_connection.commit() 
            db_connection.close()
            return False
        
        


class Model(object):

    
    view_name           = ' f" {item.model.__class__.__name__} object ({item.id})"'
    tooltip             = ''
    
    GRAPH_MODES         = []
    PIE_GRAPH_MODES     = []
    view_data_fields    = {}

    on_add              = None
    on_edit             = None
    on_delete           = None

    before_add          = None
    before_save         = None # before edit
    before_delete       = None

    search_bar          = None
    ui_list_info        = None
    filters             = {}
    dashboard           = None
    custom_str          = None
    before_edit         = None

    extra_DB_columns    = []
    # ui objects   (ui : object)
    add_buttons             = {}
    delete_buttons          = {}
    ui_lists                = {}
    search_bars             = {}
    ui_list_info_labels     = {}

    



    def __init__(self, INSApp):
        self.PW_Window = INSApp.UI    
        #fields      = []
        self.INSApp      = INSApp
        self.objects     = []
        self.ui_lists    = {}
        self.DBTableName = self.__class__.__name__
        self.CategoryViewName = self.DBTableName.replace('_', ' ').title()
        
        self.INSApp      = INSApp
        
        self.create_items_objects()
        
        
        try:
            #connections

            

            self.defind_model_list_and_btns('main_'+self.DBTableName, 
                list_ui_object      = getattr(self.INSApp.UI, self.__class__.__name__+'_Items_List'),
                search_bar          = getattr(self.INSApp.UI, self.__class__.__name__+'_Search_Bar'), 
                add_btn             = getattr(self.INSApp.UI, self.__class__.__name__+'_Add_Button'), 
                delete_btn          = getattr(self.INSApp.UI, self.__class__.__name__+'_Delete_Button'), 
                ui_list_info_label  = self.ui_list_info
                )

            if self.dashboard != None:
                self.dashboard.setWidgetResizable(True)
                self.dashboardAreaWidgetContents = QWidget()
                self.dashboardAreaWidgetContents.setObjectName(self.DBTableName+"dashboardAreaWidgetContents")
                self.dashboardAreaWidgetContents.setGeometry(QRect(0, 0, 868, 876))
                self.dashboardGridLayout = QGridLayout(self.dashboardAreaWidgetContents)
                self.dashboardGridLayout.setObjectName(self.DBTableName+"dashboardGridLayout")
                pg.setConfigOption('background', None)
                i = 0
                for mode in self.GRAPH_MODES:
                    setattr(self, "dashboard_frame_"+mode, QFrame(self.dashboardAreaWidgetContents))
                    frame = getattr(self, "dashboard_frame_"+mode)
                    frame.setObjectName(mode+"_dashboard_frame_")
                    frame.setProperty('frame_type', 'graph')

                    frame.setMinimumSize(QSize(0, 482))
                    frame.setFrameShape(QFrame.StyledPanel)

                    setattr(self, "dashboard_frame_gridLayout_"+mode,QGridLayout(frame))
                    dashboard_frame_gridLayout = getattr(self, "dashboard_frame_gridLayout_"+mode)
                    dashboard_frame_gridLayout.setObjectName("dashboard_frame_gridLayout_"+mode)

                    setattr(self, "dashboard_frame_graph_"+mode,pg.GraphicsWindow())
                    graph = getattr(self, "dashboard_frame_graph_"+mode)
                    graph.setObjectName(u"frame_"+mode)
                    graph.setFrameShape(QFrame.StyledPanel)
                    graph.setFrameShadow(QFrame.Raised)

                    setattr(self, "dashboard_frame_items_"+mode, QComboBox(frame))
                    items_combo = getattr(self, "dashboard_frame_items_"+mode)
                    items_combo.setObjectName(u"comboBox")
                    items_combo.setMaximumSize(QSize(175, 16777215))
                    for item in self.objects: 
                        items_combo.addItem(str(item), item)

                    extra_fields_dict = self.GRAPH_MODES[mode]['extra_fields']

                    field_index = 2
                    for field in extra_fields_dict:
                        setattr(self, "dashboard_extrafield_label_"+mode+'_'+field, QLabel(frame))
                        info = getattr(self, "dashboard_extrafield_label_"+mode+'_'+field)
                        info.setObjectName("dashboard_extrafield_label_"+mode+'_'+field)
                        info.setText(INSApp.translate(field))
                        dashboard_frame_gridLayout.addWidget(info, field_index, 0, 1, 1)
                        extra_fields_dict[field].view(UI = self, Form = self.INSApp.MainWindow, field_name = field, position_index = field_index, field_obj = extra_fields_dict[field], field_gridLayout = dashboard_frame_gridLayout, view_on_main_window = True )
                        setattr(self, 'dashboard_extrafield_'+mode+'_'+field, extra_fields_dict[field])
                        field_index+=1
                        
                    if field_index > 2:
                        setattr(self, "dashboard_extrafield_apply_btn"+mode, QPushButton(frame))
                        apply_btn = getattr(self, "dashboard_extrafield_apply_btn"+mode)
                        apply_btn.setObjectName("dashboard_extrafield_apply_btn"+mode)
                        apply_btn.setText(self.INSApp.translate('APPLY'))
                        apply_btn.setStyleSheet('padding:8px;')
                        apply_btn.clicked.connect(partial(  self.View_Graph, mode, extra_fields_dict,  dashboard_frame_gridLayout ))
                        dashboard_frame_gridLayout.addWidget(apply_btn, field_index, 0, 1, 1)

                    setattr(self, mode+'_refresh_graph', partial(  self.View_Graph, mode, extra_fields_dict,  dashboard_frame_gridLayout , refresh_fields = True))
                    setattr(self, "dashboard_frame_info_"+mode, QLabel(frame))
                    info = getattr(self, "dashboard_frame_info_"+mode)
                    info.setObjectName("label_info_"+mode)
                    info.setText('')
                    dashboard_frame_gridLayout.addWidget(info, field_index+2, 0, 1, 3)
                    dashboard_frame_gridLayout.addWidget(graph, field_index+3, 0, 1, 4)
                    if len(self.objects):
                        self.View_Graph(mode, extra_fields_dict,  dashboard_frame_gridLayout , refresh_fields = True)
                        
                    items_combo.currentIndexChanged.connect(partial(  self.View_Graph, mode, extra_fields_dict,  dashboard_frame_gridLayout , refresh_fields = True ))

                    setattr(self, "dashboard_main_label_"+self.__class__.__name__, QLabel(frame))
                    model_name_label = getattr(self, "dashboard_main_label_"+self.__class__.__name__)
                    model_name_label.setText(INSApp.translate(self.__class__.__name__.replace('_',' ')))


                    dashboard_frame_gridLayout.addWidget(model_name_label, 1, 0, 1, 1)
                    dashboard_frame_gridLayout.addWidget(items_combo, 1, 1, 1, 1)

                    setattr(self, "dashboard_frame_title_"+mode, QLabel(frame))
                    label = getattr(self, "dashboard_frame_title_"+mode)
                    label.setObjectName("label_title_"+mode)
                    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
                    label.setSizePolicy(sizePolicy)
                    font = QFont()
                    font.setPointSize(18)
                    label.setFont(font)
                    label.setText(INSApp.translate(mode.title()))


                    dashboard_frame_gridLayout.addWidget(label, 0, 0, 1, 2)
                    self.dashboardGridLayout.addWidget(frame , i, 0, 1, 1)

                    i+=1


                for mode in self.PIE_GRAPH_MODES:
                    setattr(self, "dashboard_pie_frame_"+mode, QFrame(self.dashboardAreaWidgetContents))
                    frame = getattr(self, "dashboard_pie_frame_"+mode)
                    frame.setObjectName(mode+"dashboard_pie_frame_")
                    frame.setProperty('frame_type', 'graph')
                    

                    
                    frame.setFrameShape(QFrame.StyledPanel)

                    setattr(self, "dashboard_pie_gridLayout_"+mode,QGridLayout(frame))
                    dashboard_frame_gridLayout = getattr(self, "dashboard_pie_gridLayout_"+mode)
                    dashboard_frame_gridLayout.setObjectName("dashboard_pie_gridLayout_"+mode)

                    setattr(self, "dashboard_frame_pie_"+mode,QPieSeries())
                    pie = getattr(self, "dashboard_frame_pie_"+mode)
                    pie.setObjectName(u"frame_"+mode)

                    chart = QChart()
                    chart.addSeries(pie)
                    chart.setAnimationOptions(QChart.SeriesAnimations)
                    view_title = mode.replace('_', ' ').title()
                    chart.setTitle(f'<span style=\"color: #ffffff;\">{ INSApp.translate(view_title) }</span>')
                    chart.setBackgroundVisible(False)

                    chartview = QChartView(chart)
                    chartview.setStyleSheet('color:white;')
                    chartview.setMinimumSize(QSize(0, 482))

                    setattr(self, "dashboard_pie_items_"+mode, QComboBox(frame))
                    items_combo = getattr(self, "dashboard_pie_items_"+mode)
                    items_combo.setObjectName(u"comboBox")
                    items_combo.setMaximumSize(QSize(175, 16777215))
                    for item in self.objects: 
                        items_combo.addItem(str(item), item)

                    extra_fields_dict = self.PIE_GRAPH_MODES[mode]['extra_fields']

                    field_index = 2
                    for field in extra_fields_dict:
                        setattr(self, "dashboard_pie_extrafield_label_"+mode+'_'+field, QLabel(frame))
                        info = getattr(self, "dashboard_pie_extrafield_label_"+mode+'_'+field)
                        info.setObjectName("dashboard_pie_extrafield_label_"+mode+'_'+field)
                        info.setText(INSApp.translate(field))
                        dashboard_frame_gridLayout.addWidget(info, field_index, 0, 1, 1)
                        extra_fields_dict[field].view(UI = self, Form = self.INSApp.MainWindow, field_name = field, position_index = field_index, field_obj = extra_fields_dict[field], field_gridLayout = dashboard_frame_gridLayout, view_on_main_window = True )
                        setattr(self, 'dashboard_pie_extrafield_'+mode+'_'+field, extra_fields_dict[field])
                        field_index+=1

                    if field_index > 2:
                        setattr(self, "dashboard_pie_extrafield_apply_btn"+mode, QPushButton(frame))
                        apply_btn = getattr(self, "dashboard_pie_extrafield_apply_btn"+mode)
                        apply_btn.setObjectName("dashboard_pie_extrafield_apply_btn"+mode)
                        apply_btn.setText(self.INSApp.translate('APPLY'))
                        apply_btn.setStyleSheet('padding:8px;')
                        setattr(self, mode+'_refresh_pie', partial(  self.View_Pie, mode, extra_fields_dict,  dashboard_frame_gridLayout , refresh_fields = True))
                        apply_btn.clicked.connect(partial(  self.View_Pie, mode, extra_fields_dict,  dashboard_frame_gridLayout ))
                        dashboard_frame_gridLayout.addWidget(apply_btn, field_index, 0, 1, 1)

                    setattr(self, "dashboard_pie_info_"+mode, QLabel(frame))
                    info = getattr(self, "dashboard_pie_info_"+mode)
                    info.setObjectName("dashboard_pie_info_"+mode)
                    info.setText('')

                    if len(self.objects):
                        self.View_Pie(mode, extra_fields_dict,  dashboard_frame_gridLayout )
                        
                    items_combo.currentIndexChanged.connect(partial(  self.View_Pie, mode,extra_fields_dict,  dashboard_frame_gridLayout, refresh_fields = True ))

                    setattr(self, "dashboard_main_label_"+self.__class__.__name__, QLabel(frame))
                    model_name_label = getattr(self, "dashboard_main_label_"+self.__class__.__name__)
                    model_name_label.setText(self.__class__.__name__.replace('_',' ').title())


                    dashboard_frame_gridLayout.addWidget(model_name_label, 1, 0, 1, 1)
                    dashboard_frame_gridLayout.addWidget(chartview, field_index+2, 0, 1, 5)
                    dashboard_frame_gridLayout.addWidget(info,  field_index+3, 0, 1, 3)

                    dashboard_frame_gridLayout.addWidget(items_combo, 1, 1, 1, 1)
                    self.dashboardGridLayout.addWidget(frame , i, 0, 1, 1)

                    i+=1

                self.dashboard.setProperty('frame_type', 'handler')
                self.dashboard.setWidget(self.dashboardAreaWidgetContents)
                try:
                    frame.setStyleSheet(self.INSApp.currentStyle)
                except:
                    pass
        except Exception as a:
            pass


    def add_item(self, data):
        Adding_Status = False
        print('self.before_add', self.before_add)
        if self.before_add == None or self.before_add(data = data):
            
            added_data = self.INSApp.DataController.add_item(self, data)
            if added_data != None:
                self.create_item_object(added_data)
                Adding_Status = True
        
            if self.on_add != None:
                self.on_add(data = data)

        return Adding_Status



    def adding_window_func(self, extra_data_for_added_items, After_Add_FUNC = None):
        window_title = 'Add '+self.CategoryViewName+' Itam'
        
        self.adding_window = windows.Form(self.PW_Window ,  model = self, item = None, title = window_title, extra_data_for_adding= extra_data_for_added_items )
        
        self.current_window = self.adding_window
        fields = {}
        
        for field in self.fields:
            if self.fields[field].field_type != 'OneToManyField':
                fields[field] = self.fields[field]


        self.adding_window.set_fields( fields = fields)
        self.adding_window.set_buttons(add_button=True)
        self.adding_window.After_Add_FUNC = After_Add_FUNC
        self.adding_window.show()


    def editing_window_func(self, list_widget, extra_data_for_added_items):
        window_title = 'Edit '+self.CategoryViewName+f' Itam ({list_widget.currentItem().data(6)})'
        self.editing_window = windows.Form(self.PW_Window ,  model = self, item = list_widget.currentItem().data(6) , title=window_title, UIs_list = list_widget.currentItem().data(6).UI_Forms)

        self.editing_window.item_obj = list_widget.currentItem().data(6)

        self.current_window = self.editing_window
        Data = {}
        for field in self.fields:
            Data[field] = getattr(self.editing_window.item_obj.data , field)

        
        self.editing_window.set_fields( fields = self.fields, Data = Data)
        self.editing_window.set_buttons(edit_button=True)
        self.editing_window.show()

    def defind_add_button(self, add_btn, def_name, extra_data_for_added_items = {}, After_Add_FUNC = None):
        self.add_buttons[def_name] = add_btn
        add_btn.clicked.connect(partial(self.adding_window_func, extra_data_for_added_items, After_Add_FUNC))
        add_btn.setText('')
        add_btn.setIcon(self.INSApp.Styler.get_icon('add'))
        

    def defind_delete_button(self, delete_btn, def_name, list_ui_object):

        self.delete_buttons[def_name] = delete_btn
        
        delete_btn.clicked.connect(partial(self.delete_selected, list_ui_object))
        delete_btn.setText('')
        delete_btn.setIcon(self.INSApp.Styler.get_icon('delete'))
        delete_btn.setProperty('btn_type','delete')


    def defind_ui_list(self, list_ui_object, def_name, fillout = True):
        self.ui_lists[def_name] = list_ui_object
        list_ui_object.itemDoubleClicked.connect(partial(self.editing_window_func, list_ui_object))

        if fillout:
            self.fillout_list(list_ui_object)

    def defind_model_list_and_btns(self, def_name, list_ui_object = None,search_bar = None, add_btn = None, delete_btn = None, ui_list_info_label = None):
        #connections
        
        if add_btn != None:
            self.defind_add_button(add_btn, def_name)

        if delete_btn != None:
            self.defind_delete_button(delete_btn, def_name, list_ui_object)

        if list_ui_object != None:
            self.defind_ui_list(list_ui_object, def_name)
            

        if search_bar != None:
            self.search_bars[def_name] = search_bar
            search_bar.textChanged.connect(partial(self.search, search_bar))

            fields_filters_text = [ f'@{f}:' for f in self.fields.keys() ]
            self.filters_compliter =  QCompleter(list(self.filters.keys()) + fields_filters_text )
            self.filters_compliter.setObjectName('Completer')
            self.filters_compliter.popup().setStyleSheet('background-color:rgba(0,0,0,0.6);color:rgb(225,225,225);')

            search_bar.setCompleter(self.filters_compliter)
            search_bar.list_ui_object =list_ui_object
            search_bar.setPlaceholderText(self.INSApp.translate('Search (Word, #, @)'))



        if ui_list_info_label != None:
            self.ui_list_info_labels[def_name] = ui_list_info_label
            self.ui_list_info.setText(f'{len(self.objects)} item')


    def point_clicked(self, item, current_item):
        info_label      = getattr(self, "dashboard_frame_info_"+item.mode)
        info_label.setText(item.point_data[current_item[0].pos().x()])

    def View_Graph(self, mode, extra_fields_dict,  dashboard_frame_gridLayout, refresh_fields = False):

        if refresh_fields:
            field_index = 2
            for field in extra_fields_dict:
                extra_fields_dict[field].view(UI = self, Form = self.INSApp.MainWindow, field_name = field, position_index = field_index, field_obj = extra_fields_dict[field], field_gridLayout = dashboard_frame_gridLayout, view_on_main_window = True )
                field_index+=1

        graph = getattr(self, "dashboard_frame_graph_"+mode)
        items_combo = getattr(self, "dashboard_frame_items_"+mode)
        
        extra_fields_dict = self.GRAPH_MODES[mode]['extra_fields']
        extra_data = {}
        for field in extra_fields_dict:
            ui_field = getattr(self, 'dashboard_extrafield_'+mode+'_'+field)
            extra_data[field] = ui_field.get_data()
            if ui_field.field_type == 'ListField':
                extra_data[field+'_data'] = ui_field.ui_field.currentData()

        
        graph_data = self.GRAPH_MODES[mode]['function'](item = items_combo.currentData(), extra_data = extra_data)
        x       = graph_data['x'] 
        xdict   = dict(enumerate(graph_data['x-keys']))
        y       = graph_data['y']
        ydict   = dict(enumerate(graph_data['y-keys']))

        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        stringaxis_y = pg.AxisItem(orientation='left')
        stringaxis_y.setTicks([ydict.items()])


        graph.clear()
        plot = graph.addPlot(axisItems={'bottom': stringaxis, 'left': stringaxis_y})
        plot.showGrid(x = True, y = True, alpha = 0.5)
        
        line = plot.plot(x,y,  symbol ='o', symbolPen ='g', symbolBrush = 1.5, name ='green', width = 1,  pen=pg.mkPen('g', width=2.5))

        line.installSceneEventFilter(plot)
        line.setAcceptHoverEvents(True)
        plot.setAcceptHoverEvents(True)
        line.sigPointsClicked.connect(self.point_clicked)
        line.mode           = mode
        line.main_plot      = plot
        line.stringaxis     = list(xdict)
        line.point_data     = graph_data['point-data']
        
    def View_Pie(self, mode, extra_fields_dict,  dashboard_frame_gridLayout, refresh_fields = False):
        if refresh_fields:
            field_index = 2
            for field in extra_fields_dict:
                extra_fields_dict[field].view(UI = self, Form = self.INSApp.MainWindow, field_name = field, position_index = field_index, field_obj = extra_fields_dict[field], field_gridLayout = dashboard_frame_gridLayout, view_on_main_window = True )
                field_index+=1

        pie  = getattr(self, "dashboard_frame_pie_"+mode)
        items_combo = getattr(self, "dashboard_pie_items_"+mode)

        extra_fields_dict = self.PIE_GRAPH_MODES[mode]['extra_fields']
        extra_data = {}
        for field in extra_fields_dict:
            ui_field = getattr(self, 'dashboard_pie_extrafield_'+mode+'_'+field)
            extra_data[field] = ui_field.get_data()
            if ui_field.field_type == 'ListField':
                extra_data[field+'_data'] = ui_field.ui_field.currentData()

        all_info = self.PIE_GRAPH_MODES[mode]['function'](item = items_combo.currentData(),extra_data = extra_data )
        data = all_info['data']
        if all_info.get('extra_info') != None:
            info = getattr(self, "dashboard_pie_info_"+mode)
            info.setText(all_info.get('extra_info'))

        pie.clear()
        for a_slice in  data:
            sl = pie.append( a_slice , data[a_slice] )
            sl.setBorderWidth(1.5)
            sl.setBorderColor(QColor(200,200,200))

        for slice in pie.slices():
            oldLabel=slice.label()
            slice.setLabel(( f'<span style=\"color: #ffffff;\">{oldLabel}: %({round(slice.percentage()*100, 2)})</span>'))
        

        def s_hovered(pie, current_slice):
            for unhovered_slice  in pie.slices():
                if unhovered_slice != current_slice:
                    unhovered_slice.setExploded(False)
                    unhovered_slice.setLabelVisible(False)
            current_slice.setExploded(True)
            current_slice.setLabelVisible(True)
 	
        pie.hovered.connect(partial(s_hovered, pie))

 
    def search(self, search_bars):
        text = search_bars.text()
        search_bars.list_ui_object.clear()
        filtered_objects = []
        if text != '':


            if text[0] =='#':#custom filters
                if text.split(':')[0]+':' in self.filters.keys():

                    if ':' in text : # have values
                        value = ':'.join(text.split(':')[1:])
                        filtered_objects = self.filters[text.split(':')[0]+':'](self, self.objects, value = value)
                    else:
                        filtered_objects = self.filters[text.split(':')[0]+':'](self, self.objects)

            elif text[0] =='@':#fields filters
                try:
                    field           = text[1:].split(':')[0]
                    field_value    = ':'.join(text[1:].split(':')[1:])
                    
                    for obj in self.objects:
                        if (self.fields[field].field_type == 'OneToOneField' and field_value in str(getattr(obj.data, field+'__obj'))) or field_value in str(getattr(obj.data, field)):
                            filtered_objects.append(obj)

                except:
                    pass
                
            else:
                text_words = set(text.split(' '))
                if '' in text_words:
                    text_words.remove('')

                for item_object in self.objects:
                    obj_data = list(vars(item_object.data).values())
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
                        filtered_objects.append(item_object)
                    
                    else:
                        ex_status = True
                        for word in text_words:
                            obj_words_str = [ str(i) for i in obj_words if type(i) in [float,bool,str,int,list, tuple, dict, set] ]
                            if word not in ' '.join(obj_words_str):
                                ex_status = False

                        if ex_status:
                            filtered_objects.append(item_object)


            for item_object in filtered_objects:
                self.add_item_to_list(item_object)
            self.ui_list_info.setText(f'{len(filtered_objects)}/{len(self.objects)} item found')
            
        else:
            for item_object in self.objects:
                self.add_item_to_list(item_object, list_target=search_bars.list_ui_object)
            self.ui_list_info.setText(f'{len(self.objects)} item')

        




    def create_item_object(self, data):
            
        item_obj = Item(data, self)
        item_obj.id = data.get('id')

        self.objects.append(item_obj)
        self.add_item_to_list( item_obj)


    def create_items_objects(self):
        b_data = self.INSApp.DataController.get_model_data(self)
        
        for item in b_data:
            self.create_item_object(item)


    def fillout_list(self, ui_list):
        for obj in self.objects:
            self.add_item_to_list(obj, list_target = ui_list)
        

    def add_item_to_list(self, obj, list_target = 'ALL'):
        if obj.ui_obj == None:
            item = QtWidgets.QListWidgetItem()
            item.setData(2,str(obj))
            item.setToolTip(replace_variable_value(obj, self.tooltip))
            item.setData(6,obj)
            obj.ui_obj = item
        else: 
            item = obj.ui_obj

        if list_target == 'ALL':
            for ui_list in self.ui_lists.values():
                ui_list.addItem(item)
        else:
            list_target.addItem(item)




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
                    if vars(item.data)[var_name[:-4]] in fields[var_name] : 
                        fields_values[key] = vars(item.data)[var_name[:-4]]

                    item_values.append(vars(item.data)[var_name[:-4]])

                else:
                    item_values.append(vars(item.data)[var_name])

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



    def create(self,dict_inner_data = None,  **inner_data):
        if dict_inner_data != None:
            inner_data = dict_inner_data

        t_item = self.temporary_item()
        for bit in inner_data:
            setattr(t_item, bit, inner_data[bit])

        if self.before_add == None or self.before_add(t_item):
            
            fields  = []
            data    = []
            for field in inner_data.keys():
                fields.append(str(field))
                if type(inner_data[field]) in [list, set, dict, tuple]:
                    inner_data[field] = json.dumps(inner_data[field])
                data.append(inner_data[field])
            

            for not_set_field in set(self.fields.keys()).difference(set(inner_data.keys())):
                field_obj = self.fields[not_set_field]
                data.append(str(field_obj.default))


            fields_str = ', '.join(list(fields) + list(set(self.fields.keys()).difference(set(inner_data.keys()))))
            

            db_connection = sql.connect(self.INSApp.database_path)

            data_str_f = ', '.join((['?',]* len(data)))

            item = db_connection.execute(f"""INSERT INTO {self.DBTableName} ({fields_str}) values ({data_str_f}) """, data )
            
            db_connection.commit()
            db_connection.close()



            data_n = { fields[i]:data[i] for i in range(len(data)) }
            data_n['view_name'] = self.view_name
            data_n['id'] = int(item.lastrowid)
            data_n['Model'] = self
            item_object = Item(data_n, self)
            self.objects.append(item_object)
            self.add_item_to_list(item_object)




            for mode in self.GRAPH_MODES:
                getattr(self , "dashboard_frame_items_"+mode).addItem(str(item_object),item_object)
            
            for mode in self.PIE_GRAPH_MODES:
                getattr(self , "dashboard_pie_items_"+mode).addItem(str(item_object), item_object)

            return item_object
        else:
            False
            

        
    def delete_selected(self, ui_list):
        item = ui_list.currentItem()
        
        if item != None:
            item.data(6).delete()


                

class HoverableCurveItem(pg.PlotCurveItem):
    sigCurveHovered = QtCoregraph.Signal(object, object)
    sigCurveNotHovered = QtCoregraph.Signal(object, object)

    def __init__(self, hoverable=True, *args, **kwargs):
        super(HoverableCurveItem, self).__init__(*args, **kwargs)
        self.hoverable = hoverable
        self.setAcceptHoverEvents(True)

    def hoverEvent(self, ev):
        if self.hoverable:
            if self.mouseShape().contains(ev.pos()):
                self.sigCurveHovered.emit(self, ev)
            else:
                self.sigCurveNotHovered.emit(self, ev)