
import os, configparser
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class Styler(object):

    def __init__(self, app):
        self.icons = {}  
        self.app = app

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        if not os.path.exists('styles'):
            os.mkdir('styles')
        app.currentStyleName = config['style']['current']
        self.apply_style()
        


    def get_icon(self, name):
        if name in self.icons:
            return self.icons[name]
        else:
            icon	= QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join('INSLPCModel', 'icons',name+'.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.icons[name] = icon
            return icon


    def change_style(self, style):
        
        self.app.currentStyleName = style

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        config['style']['current'] = style
        config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
        self.app.currentStyleName = config['style']['current']
        print(self.app.currentStyleName)
        self.apply_style()



    def apply_style(self):
        style_file_path = os.path.join('styles', self.app.currentStyleName+'.css' )        
        self.app.currentStyle     = open(os.path.join('styles','BASE_STYLE.css'), 'r').read() + open(style_file_path, 'r').read() 
        self.app.UI.setStyleSheet(self.app.currentStyle)
	
        
    def add_style(self, p_ui):
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        file_name=QFileDialog.getOpenFileName(p_ui, self.app.translate(f"Add language"),config['settings']['last_opened_location'],f"Theme Files (*.css)")
        if len(file_name[0])>0 :
            new_file = open(os.path.join('styles',os.path.basename(file_name[0])), 'w')
            new_file.write(open(file_name[0], 'r').read())
            new_file.close()
            return os.path.basename(file_name[0]).split('.')[0]