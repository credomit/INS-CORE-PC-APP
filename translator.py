import configparser, os, json, notifiers, codecs
from INSLPCModel import configuration_ini
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

class translator(object):
    
    def __init__(self, app):
        if not os.path.exists('languages'):
            os.mkdir('languages')

        
        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        self.language = config['default']['default-language']
        
        
        self.apply_language(app)


    def apply_language(self,app):
        language = configuration_ini.get_data(['languages', f'{self.language}.ini'])

        if len(language._sections) == 0: #new file
            language['language_info'] = { 'language_shortcut': self.language, 'language_name': ''}  
            language['dictionary'] = {}  
            language.write(open(os.path.join('languages', f'{self.language}.ini'),'w'))

        # apply on main ui labels
        for label in app.translateable_labels:
            try:
                label_obj = getattr(app.UI, label)
                label_obj.setText( self.translate( label ) )
            except:
                print(f'\033[31mLabel "{label}" Not Found!  \033[0m')    
                exit()
       
        for tab_widget in app.translateable_tap_widgets:
           tab_index = 0
           while True:
                try:
                    getattr(app.UI, tab_widget).setTabText(tab_index, self.translate(getattr(app.UI, tab_widget).widget(tab_index).accessibleName()))    
                    tab_index+=1
                except:
                    break
        # 
        if 'Layout_direction' in language['language_info']:
            app.current_language_layout_direction = language['language_info']['Layout_direction']
            app.UI.Layout_direction = language['language_info']['Layout_direction']
            if language['language_info']['Layout_direction'] == 'RTL':
                app.UI.setLayoutDirection(QtCore.Qt.RightToLeft)

            else:
                app.UI.setLayoutDirection(QtCore.Qt.LeftToRight)

        else:
            language_sh = language['language_info']['language_shortcut']
            print(f'\033[31m{ language_sh } language layout direction  Not Set!  \033[0m')  



        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        languages =  json.loads(config['languages']['set'])

        app.current_language = self.language
        app.current_language_name = [ list(i.keys())[0] for i in languages if list(i.values())[0] == self.language ][0]  
  



    def set_language(self, app, p_ui):
        app.current_language = p_ui.Languages_Box.currentData()
        self.language = p_ui.Languages_Box.currentData()
        self.apply_language(app)
        

    def add_language(self, app, p_ui):
        config = configuration_ini.get_data(['INSLPCModel','settings.ini'])
        file_name=QFileDialog.getOpenFileName(p_ui.Form, self.translate(f"Add language"),config['settings']['last_opened_location'],f"Language Files (*.{ app.app_file_type }l)")
        if len(file_name[0])>0:
            try:
                new_language = configuration_ini.get_data(file_name[0].replace('/','\\').split('\\'))
                languages_set = json.loads(config['languages']['set'])
                new_lang_name = new_language['language_info']['language_name']
                new_lan_shortcut = new_language['language_info']['language_shortcut']

                if { new_lang_name : new_lan_shortcut } not in languages_set:
                    languages_set += [{ new_lang_name : new_lan_shortcut },]
                
                configuration_ini.set_data(['INSLPCModel','settings.ini'], 'languages', 'set', json.dumps(languages_set))
                configuration_ini.set_data(['INSLPCModel','settings.ini'], 'default', 'default-language', new_language['language_info']['language_shortcut'])

                new_language_file = configuration_ini.get_data(['languages', new_language['language_info']['language_shortcut']+'.ini' ])
                new_language_file.write(open(file_name[0],'w'))
                config.write(open('settings.ini','w'))
                notifiers.Notification( self.translate("Success"),self.translate("Language added successfully") ,app.app_logo ).show()
                self.apply_language(app)

            except:
                notifiers.Notification( self.translate("Error"),self.translate("Error while loading language file \ n try to redownload it from credom.it") ,app.app_logo ).show()

            
            
            


    def translate(self, text):
        language = configuration_ini.get_data(['languages', f'{self.language}.ini'])

        if text.lower() in language._sections['dictionary'].keys():
            return language['dictionary'][text]

        else:
            configuration_ini.set_data(['languages', f'{self.language}.ini'], 'dictionary', text, text.lower())
            
            
            print(f'\033[31m TEXT "{text}" not founded in { self.language } language file \033[93m text added automatically with empty value to languages/{self.language}.ini \033[0m ')
            return text.lower()