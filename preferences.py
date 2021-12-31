from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json, configparser, os


def open_preferences_window(app):
    
    app.UI.subwindow = QtWidgets.QDialog()

    ui = Preferences_Ui()
    ui.setupUi(app.UI.subwindow, app)
    app.UI.subwindow.setProperty('form_type', 'subwindow')
    app.UI.subwindow.setStyleSheet(app.currentStyle)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()




class Preferences_Ui(object):
    def setupUi(self, Form,app):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(489, 257)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.label.setText('Language')
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.Languages_Box = QtWidgets.QComboBox(self.tab)
        self.Languages_Box.setObjectName("Languages_Box")
        self.gridLayout_2.addWidget(self.Languages_Box, 0, 1, 1, 1)
        self.Add_Language_btn = QtWidgets.QPushButton(self.tab)
        self.Add_Language_btn.setObjectName("Add_Language_btn")
        self.Add_Language_btn.setMinimumSize(QSize(30, 30))
        self.Add_Language_btn.setMaximumSize(QSize(30, 30))
        self.Add_Language_btn.setIcon(app.Styler.get_icon('add'))
        self.gridLayout_2.addWidget(self.Add_Language_btn, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.label_2.setText('Theme')
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.Themes_Box = QtWidgets.QComboBox(self.tab)
        self.Themes_Box.setObjectName("Themes_Box")
        self.gridLayout_2.addWidget(self.Themes_Box, 1, 1, 1, 1)
        self.Add_Theme_btn = QtWidgets.QPushButton(self.tab)
        self.Add_Theme_btn.setObjectName("Add_Theme_btn")
        self.Add_Theme_btn.setMinimumSize(QSize(30, 30))
        self.Add_Theme_btn.setMaximumSize(QSize(30, 30))
        self.Add_Theme_btn.setIcon(app.Styler.get_icon('add'))
        self.gridLayout_2.addWidget(self.Add_Theme_btn, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "View")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(Form)


        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        self.languages = json.loads(config['languages']['set'])

        #set languages
        for language in self.languages:
            self.Languages_Box.addItem( list(language.keys())[0], list(language.values())[0] )

        current_language = app.current_language_name

        if self.Languages_Box.findText( str(current_language) )>-1:
            self.Languages_Box.setCurrentIndex( self.Languages_Box.findText(str(current_language)))

        #set themes
        themes = [ i.split('.')[0] for i in os.listdir(os.path.join('styles')) if i.split('.')[-1] and i!='BASE_STYLE.css' ]

        for theme in themes:
            self.Themes_Box.addItem(theme)

        current_theme = app.currentStyleName

        if self.Themes_Box.findText( str(current_theme) )>-1:
            self.Themes_Box.setCurrentIndex( self.Themes_Box.findText(str(current_theme)))

        def add_style(self, app, Form):
            added_theme = app.Styler.add_style(Form)
            if added_theme != None:
                self.Themes_Box.insertItem(0,added_theme)
                self.Themes_Box.setCurrentIndex( self.Themes_Box.findText(added_theme))

        #connection
        self.Languages_Box.currentIndexChanged.connect(lambda: app.translator.set_language(app, self))
        self.Themes_Box.currentIndexChanged.connect(lambda: app.Styler.change_style(self.Themes_Box.currentText()))
        self.Add_Language_btn.clicked.connect(lambda: app.translator.add_language(app, self))
        self.Add_Theme_btn.clicked.connect(lambda: add_style(self, app, Form))


