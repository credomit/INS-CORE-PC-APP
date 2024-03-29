from PyQt5 import QtWidgets, uic
import requests, configparser, os, json
from INSLPCModel import configuration_ini
from getmac import get_mac_address 
from .windows_creator import *
import threading, socket

def back_connections(app):
    config = configuration_ini.get_data(['INSLPCModel','settings.ini'])

    def back_check_key(app):
        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])

        device      = socket.gethostname()
        app_name    = app.app_name
        app_version = app.app_version
        key = config['settings']['key']

        if True:
            try:
                mac_addr    = get_mac_address()
                con = requests.post('http://credom.herokuapp.com/check_product_key/',{'key':key, 'app':app_name, 'version':app_version, 'mac-addr':mac_addr,'device':device})
                if not int(json.loads(con.content).get('status')):
                    config['settings']['insci'] = '0'
                    config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
                    try:
                        app.LoadinWindow.destroy()        
                    except:
                        pass
                    try:
                        app.MainWindow.destroy()
                    except:
                        pass
                    INSCI(app)
                
                pass
            except:
                pass
    if int(config['settings']['insci']):
        pass
        #threading.Thread(target=lambda: back_check_key(app)).start()

def check_INSCI(app):
    device      = socket.gethostname()
    app_name    = app.app_name
    app_version = app.app_version
    key = app.INSCI_UI.key_field.text()
    try:
        mac_addr    = get_mac_address()
        app.INSCI_UI.status_label.setText('Loading...')
        app.INSCI_UI.status_label.update()
        app.INSCI_UI.update()
        con = requests.post('http://credom.herokuapp.com/check_product_key/',{'key':key, 'app':app_name, 'version':app_version, 'mac-addr':mac_addr,'device':device})
        app.INSCI_UI.status_label.setText(str(con.content))
        app.INSCI_UI.status_label.setText( json.loads(con.content).get('msg'))
        if  json.loads(con.content).get('status'):
            app.INSCI_UI.close()
            config = configuration_ini(['INSLPCModel','settings.ini'])
            config['settings']['INSCI'] = '1'
            config['settings']['KEY']   =  key
            config.write(open(os.path.join('INSLPCModel','settings.ini'),'w'))
            
            loading_window(app)

        
    except Exception as a:
        app.INSCI_UI.status_label.setText('No internet connection')


def INSCI(self):
    config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
    INSCI_status = int(config['settings']['INSCI'])
    if not INSCI_status:
        self.getkey                 = os.path.join('INSLPCModel','get_product_key.ui')
        self.get_key_window              = QtWidgets.QDialog()
        self.INSCI_UI               = uic.loadUi(self.getkey, self.get_key_window)
        self.INSCI_UI.app_logo.setIcon(self.Styler.get_icon('main_logo'))
        self.get_key_window.setWindowTitle('INS Warehouse')
        self.get_key_window.setProperty('form_type', 'subwindow')
        self.get_key_window.setStyleSheet(self.currentStyle)
        self.get_key_window.show()
        self.INSCI_UI.OK.clicked.connect(lambda:check_INSCI(self))

    else:
        loading_window(self)


#requests.post('http://127.0.0.1:8000/check_product_key/',{'key':'test-key', 'app':'INS Server', 'version':'1.1', 'mac-addr':'112233','device':'philip test'}).content