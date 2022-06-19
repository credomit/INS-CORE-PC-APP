
import os
from INSLPCModel import configuration_ini
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Styler(object):

    def __init__(self, app):
        self.icons = {}  
        self.app = app

        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        if not os.path.exists('styles'):
            os.mkdir('styles')
        app.currentStyleName = config['style']['current']
        self.apply_style()
        


    def get_icon(self, name):
        if name in self.icons:
            return self.icons[name]
        else:
            icon	= QtGui.QIcon()
            try:
                open(os.path.join('INSLPCModel', 'icons',name+'.png'))
                pixmap = QtGui.QPixmap(os.path.join('INSLPCModel', 'icons',name+'.png'))
            except:
                pixmap = QtGui.QPixmap(os.path.join('icons',name+'.png'))

            style_icon_colors = configuration_ini.get_data(['INSLPCModel','styles.ini'])
            for color in style_icon_colors[self.app.currentStyleName]:
                mask = pixmap.createMaskFromColor(QtGui.QColor('#'+color), QtCore.Qt.MaskOutColor)
                pen = QtGui.QPainter(pixmap)
                pen.setPen(QtGui.QColor('#'+style_icon_colors[self.app.currentStyleName][color]))
                pen.drawPixmap(pixmap.rect(), mask, mask.rect())
                pen.end()
            
            icon.addPixmap(pixmap)
            self.icons[name] = icon
            return icon


    def change_style(self, style):
        
        self.app.currentStyleName = style

        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        config['style']['current'] = style
        config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
        self.app.currentStyleName = config['style']['current']
        self.apply_style()



    def apply_style(self):
        style_file_path = os.path.join('styles', self.app.currentStyleName+'.css' )        
        self.app.currentStyle     = open(os.path.join('styles','BASE_STYLE.css'), 'r').read() + open(style_file_path, 'r').read() 
        self.app.UI.setStyleSheet(self.app.currentStyle)
	
        
    def add_style(self, p_ui):
        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        file_name=QFileDialog.getOpenFileName(p_ui, self.app.translate(f"Add language"),f"Theme Files (*.css)")
        if len(file_name[0])>0 :
            style_data = configuration_ini.get_data(os.path.basename(file_name[0]))
            new_file = open(os.path.join('styles',os.path.basename(file_name[0])), 'w')
            new_file.write(style_data.get('data').get('full-style'))
            new_file.close()

            styles = configuration_ini.get_data(['INSLPCModel','styles.ini'])
            styles[style_data.get('info').get('name')]['icon-color'] = style_data.get('info').get('icon-color')
            return os.path.basename(file_name[0]).split('.')[0]