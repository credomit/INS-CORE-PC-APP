from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtGui import *
import json, configparser, os


def open_preferences_window(app):
    
    app.UI.subwindow = QtWidgets.QDialog()

    ui = Preferences_Ui()
    ui.setupUi(app.UI.subwindow, app)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.show()




class Preferences_Ui(object):
    def setupUi(self, Form,app):
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
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.Languages_Box = QtWidgets.QComboBox(self.tab)
        self.Languages_Box.setObjectName("Languages_Box")
        self.gridLayout_2.addWidget(self.Languages_Box, 0, 1, 1, 1)
        self.Add_Language_btn = QtWidgets.QPushButton(self.tab)
        self.Add_Language_btn.setObjectName("Add_Language_btn")
        self.gridLayout_2.addWidget(self.Add_Language_btn, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        self.languages = json.loads(config['languages']['set'])

        for language in self.languages:
            self.Languages_Box.addItem( list(language.keys())[0], list(language.values())[0] )

        current_language = app.current_language

        if self.Languages_Box.findText( str(current_language) )>-1:
            self.Languages_Box.setCurrentIndex( self.Languages_Box.findText(str(current_language)))


        #connection
        self.Languages_Box.currentIndexChanged.connect(lambda: app.translator.set_language(app, self))
        self.Add_Language_btn.clicked.connect(lambda: app.translator.add_language(app, self))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Language:"))
        self.Add_Language_btn.setText(_translate("Form", "Add"))
        self.label_2.setText(_translate("Form", "Theme:"))
        self.pushButton_2.setText(_translate("Form", "Add"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
