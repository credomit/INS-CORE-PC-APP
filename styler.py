
import os, configparser


class Styler(object):

    def __init__(self, app):
        config = configparser.ConfigParser()
        config.read( os.path.join('INSLPCModel','settings.ini'))

        if not os.path.exists('styles'):
            os.mkdir('styles')
        
        app.currentStyleName = config['style']['current']

        style_file_path = os.path.join('styles', app.currentStyleName+'.qss' )
        print(os.path.isfile(style_file_path))
        open(style_file_path, 'w')
        open(os.path.join('styles','BASE_STYLE.qss'), 'w')

        app.currentStyle     = open(style_file_path, 'r').read() + open(os.path.join('styles','BASE_STYLE.qss'), 'r').read()
        
