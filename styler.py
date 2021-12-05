
import os, configparser
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

class Styler(object):

    def __init__(self, app):
        self.icons = {}  

        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))
        if not os.path.exists('styles'):
            os.mkdir('styles')
        
        app.currentStyleName = config['style']['current']
        style_file_path = os.path.join('styles', app.currentStyleName+'.css' )
        

        app.currentStyle     = open(style_file_path, 'r').read() + open(os.path.join('styles','BASE_STYLE.css'), 'r').read()

    def get_icon(self, name):
        if name in self.icons:
            return self.icons[name]
        else:
            icon	= QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join('INSLPCModel', 'icons',name+'.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.icons[name] = icon
            return icon
	
        
