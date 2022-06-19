from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json, os
from INSLPCModel import configuration_ini


def open_preferences_window(app):
    
    app.UI.subwindow = QtWidgets.QDialog()

    app.UI.subwindow.Form = uic.loadUi(os.path.join('INSLPCModel','preferences.ui'), app.UI.subwindow)
    app.UI.subwindow.setProperty('form_type', 'subwindow')
    app.UI.subwindow.setStyleSheet(app.currentStyle)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
    app.UI.subwindow.languages = json.loads(config['languages']['set'])


    #######################################################################
    for language in app.UI.subwindow.languages:
            app.UI.subwindow.Languages_Box.addItem( list(language.keys())[0], list(language.values())[0] )

    current_language = app.current_language_name
    if app.UI.subwindow.Languages_Box.findText( str(current_language) )>-1:
            app.UI.subwindow.Languages_Box.setCurrentIndex( app.UI.subwindow.Languages_Box.findText(str(current_language)))

    themes = [ i.split('.')[0] for i in os.listdir(os.path.join('styles')) if i.split('.')[-1] and i!='BASE_STYLE.css' ]
    for theme in themes:
            app.UI.subwindow.Themes_Box.addItem(theme)
            
    current_theme = app.currentStyleName
    if app.UI.subwindow.Themes_Box.findText( str(current_theme) )>-1:
            app.UI.subwindow.Themes_Box.setCurrentIndex( app.UI.subwindow.Themes_Box.findText(str(current_theme)))

    def add_style(window, app, Form):
            added_theme = app.Styler.add_style(Form)
            if added_theme != None:
                window.Themes_Box.insertItem(0,added_theme)
                window.Themes_Box.setCurrentIndex( app.UI.subwindow.Themes_Box.findText(added_theme))
 
    i_index=0
    app.UI.subwindow.fields = { i:app.settings_constants[i]['ui_field'] for i in app.settings_constants }
    app.UI.subwindow.edit_mode = False
    for constant in app.settings_constants:
    	field = app.settings_constants[constant]['ui_field'].UI_Field(app.UI.subwindow.tab_2)
    	field.setValue(int(config[app.settings_constants[constant]['ini_name'][0]][app.settings_constants[constant]['ini_name'][1]]))
    	field.setStyleSheet('color:rgb(255,255,255);')
    	app.settings_constants[constant]['ui_field'].ui_field = field
    	app.UI.subwindow.gridLayout_3.addWidget(field, i_index, 1, 1, 1)
        
    	label = QtWidgets.QLabel(app.UI.subwindow.tab_2)
    	label.setObjectName(constant+"label")
    	label.setText( app.translate(constant).replace('_',' ').title()+':')
                
    	if app.current_language_layout_direction == 'RTL':
            label.setAlignment(Qt.AlignLeft)
    	else:
            label.setAlignment(Qt.AlignRight)

    	app.UI.subwindow.gridLayout_3.addWidget(label, i_index, 0, 1, 1, Qt.AlignVCenter)

    	i_index+=1

    def apply_constants(app):
        configuration_ini.get_data(['INSLPCModel','settings.ini'])
        for constant in app.settings_constants:
            constant_data = app.settings_constants[constant]['ui_field'].Get_Data()
            config[app.settings_constants[constant]['ini_name'][0]][app.settings_constants[constant]['ini_name'][1]] = str(constant_data)
            setattr(app, app.settings_constants[constant]['app_variable'], constant_data)
        
        config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))

    app.UI.subwindow.apply_constants.clicked.connect(lambda:apply_constants(app))
    #connection
    #######################################################################
    app.UI.subwindow.Languages_Box.currentIndexChanged.connect(lambda: app.translator.set_language(app, app.UI.subwindow))
    app.UI.subwindow.Themes_Box.currentIndexChanged.connect(lambda: app.Styler.change_style(app.UI.subwindow.Themes_Box.currentText()))
    app.UI.subwindow.Add_Language_btn.clicked.connect(lambda: app.translator.add_language(app, app.UI.subwindow))
    app.UI.subwindow.Add_Theme_btn.clicked.connect(lambda: add_style(app.UI.subwindow, app, app.UI.subwindow.ui))


    app.UI.subwindow.show()

