from tkinter import HORIZONTAL
from PyQt5 import QtCore, QtGui, QtWidgets, uic,Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import xlsxwriter, os, threading

def open_export_csv_window(app):
    
    app.UI.subwindow = QtWidgets.QDialog()

    app.UI.subwindow.ui = uic.loadUi(os.path.join('INSLPCModel','export_csv.ui'), app.UI.subwindow)
    app.UI.subwindow.setProperty('form_type', 'subwindow')
    app.UI.subwindow.setStyleSheet(app.currentStyle)

    app.UI.subwindow.setWindowModality(QtCore.Qt.ApplicationModal)
    app.UI.subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    app.UI.subwindow.ui.edit_mode = False

    app.UI.subwindow.ui.categories_dict = {i.__name__.replace('_',' ').title():i.__name__ for i in app.listed_items}
    for category in  app.UI.subwindow.ui.categories_dict:    
        app.UI.subwindow.ui.categories.addItem(app.translate(category), app.UI.subwindow.ui.categories_dict[category])
    
    for category in app.extra_excel_categories:
        app.UI.subwindow.ui.categories.addItem(app.translate(category), app.extra_excel_categories[category])

    def reverce_fields():
        fields = []
        for i in range(app.UI.subwindow.ui.category_fields.count()):
            item = app.UI.subwindow.ui.category_fields.item(i)
            fields.insert(0, [
                item.text(),
                item.data(6),
                item.checkState(),
            ])
        app.UI.subwindow.ui.category_fields.clear()

        for i in fields:
            item_ui = QtWidgets.QListWidgetItem()
            item_ui.setText(i[0])
            item_ui.setData(6, i[1])
            item_ui.setCheckState(i[2])
            app.UI.subwindow.ui.category_fields.addItem(item_ui)


    
    app.UI.subwindow.ui.reverce_fields.clicked.connect(reverce_fields)




    def category_changed(ui):
            if type(ui.categories.currentData()) == str: # model 
                current_model = getattr(app, ui.categories.currentData())
                fields = current_model.fields
                objects = current_model.objects
            
            else: # extra_excel_categories
                info = ui.categories.currentData()
                fields = info['excel_fields']
                objects = info['get_object_function'](app)
                

            app.UI.subwindow.ui.category_items.clear()
            app.UI.subwindow.ui.category_fields.clear()
                
            for field in fields:
                item_ui = QtWidgets.QListWidgetItem()
                item_ui.setText(app.translate(field))
                item_ui.setData(6, field)
                item_ui.setCheckState(2)
                app.UI.subwindow.ui.category_fields.addItem(item_ui)


            for item in objects:
                item_ui = QtWidgets.QListWidgetItem()
                item_ui.setText(str(item))
                item_ui.setData(6, item)
                item_ui.setCheckState(2)
                app.UI.subwindow.ui.category_items.addItem(item_ui)

            

    def h_r_fields_sorting_changed(ui):
        HORIZONTAL_status = False
        if app.UI.subwindow.ui.vertical_export.isChecked():
            HORIZONTAL_status = True
        if HORIZONTAL_status:
            app.UI.subwindow.ui.category_fields.setFlow(QListView.LeftToRight)
        
        else:
            app.UI.subwindow.ui.category_fields.setFlow(QListView.TopToBottom)
    
    def select_all_fields_status_changed(ui):
        for index in range(app.UI.subwindow.ui.category_fields.count()):
            app.UI.subwindow.ui.category_fields.item(index).setCheckState(app.UI.subwindow.ui.select_all_fields.isChecked()*2)
        
    def select_all_items_status_changed(ui):
        for index in range(app.UI.subwindow.ui.category_items.count()):
            app.UI.subwindow.ui.category_items.item(index).setCheckState(app.UI.subwindow.ui.select_all_items.isChecked()*2)
    
    def write_row(ui, worksheet, row_num, row_data, current_format):
        current_column = 0
        for i in range(len(row_data)):
            if type(row_data[i]) == dict:
                row_data[i]
                list_data = row_data[i]
                row_data.pop(i)
                for b in list_data.values():
                    row_data.insert(i, str(b))


            if type(row_data[i]) not in [str, int, float, bool, dict]:
                list_data = row_data[i]
                row_data.pop(i)
                if len(list_data):
                    for b in range(len(list_data[0])):
                        row_data.insert(i, '')
                        current_column +=1
                write_row(ui, worksheet, row_num+1, list_data, current_format)
            current_column +=1


        if ui.horizantel_export.isChecked():
            worksheet.write_column(0, row_num, row_data, cell_format = current_format)
        else:
            worksheet.write_row(row_num, 0, row_data, cell_format = current_format)
        

    

    def export_csv(ui):
        selected_items = []
        for index in range(app.UI.subwindow.ui.category_items.count()):
            ui_item = app.UI.subwindow.ui.category_items.item(index)
            if ui_item.checkState():
                selected_items.append(ui_item.data(6))
        
        selected_fields = []
        for index in range(app.UI.subwindow.ui.category_fields.count()):
            ui_item = app.UI.subwindow.ui.category_fields.item(index)
            if ui_item.checkState():
                selected_fields.append(ui_item.data(6))
                
        
        if type(ui.categories.currentData()) == dict: # model 
            data, headers_data = ui.categories.currentData()['get_excel_data'](selected_items, selected_fields)

        else:
            subfields = {}
            onetoone_field = {}
            current_model = getattr(app, ui.categories.currentData())
            columns_count = 0
            def get_fields_info(fields, columns_count = 0):
                out_fields = []
                for field in fields:
                    columns_count += 1
                    field_data = {'name':field}
                    if fields[field].field_type     == 'OneToOneField':
                        field_data ['type']         = 'OTO' # One To One 
                        field_data ['OTO_object']   = fields[field].model

                    elif fields[field].field_type   == 'ManyToManyField':
                        field_data ['type']         = 'MTM' # One To One 
                        field_data ['sub_fields'], columns_count = get_fields_info(fields[field].subfields, columns_count)
                        
                    else:
                        field_data ['type']         = 'Single'

                    out_fields.append(field_data)
                return out_fields, columns_count


            selected_fields = { field:current_model.fields[field] for field in selected_fields }
            fields_info, columns_count = get_fields_info(selected_fields)
            data = []
            def count_sub_field(field, count=0):
                count += 1
                if field['type'] == 'MTM':
                    for f in field['sub_fields'] :
                        count = count_sub_field(f, count = count)
                
                return count
            for item in selected_items:
                row = ['',]*columns_count
                sub_rows = []
                def fill_out_row(row, item, field, is_from_MTM = False, field_index = 0):
                    for info in field:

                        if info['type'] == 'Single':
                            if is_from_MTM:
                                row[field_index] = item[info['name']]
                            else:
                                row[field_index] = getattr(item, info['name'])

                        elif info['type'] == 'MTM':
                            if is_from_MTM:
                                data = item[info['name']]
                            else:
                                data = getattr(item, info['name'])

                            bit_index = 0
                            for bit in data:
                                if len(sub_rows) <= bit_index:
                                    sub_rows.append(['',]*columns_count)


                                sub_rows[bit_index] = fill_out_row(sub_rows[bit_index], bit, info['sub_fields'], is_from_MTM = True, field_index = int(field_index+1))
                                bit_index+=1
                            
                            field_index+=count_sub_field(info)-1
                        elif info['type'] == 'OTO':
                            if is_from_MTM:
                                row[field_index] = item[info['name']]
                            else:
                                row[field_index] = getattr(item, info['name'])

                        field_index+=1
                    return row
                
                fill_out_row(row, item, fields_info)
            
                data.append(row)
                for row in sub_rows:
                    data.append(row)
            
            def add_field_to_headers(field, headers = []):
                headers.append(field['name'])
                if field['type'] == 'MTM':
                    for f in field['sub_fields'] :
                        headers = add_field_to_headers(f, headers)
                    
                return headers

            for field in fields_info:
                headers_data = add_field_to_headers(field) 

                #headers_data.append(app.translate(field))
            data.insert(0, headers_data)


        file_name=QFileDialog.getSaveFileName(ui,app.translate(f"create excel file"),'',f"Excel Files (*.xlsx)")[0]
        
        if len(file_name)>0:
            
            if file_name[-5:] != '.xlsx':
                file_name+='.xlsx'

            workbook = xlsxwriter.Workbook(file_name)
            worksheet = workbook.add_worksheet('Main')
            if app.current_language_layout_direction == 'RTL':
                text_align = 'Right'
            else:
                text_align = 'Left'
            
            header_format = workbook.add_format({'bold': True, 'bg_color':'#3b6dad', 'align': text_align})
            data_format_1 = workbook.add_format({'bg_color':'#ffffff', 'align': text_align})
            data_format_2 = workbook.add_format({'bg_color':'#b8b8b8', 'align': text_align})

            for row_num, row_data in enumerate(data):
                if row_num == 0:
                    current_format = header_format
                elif row_num %2 == 0:
                    current_format = data_format_1
                else:
                    current_format = data_format_2

                for i in range(len(row_data)):
                    row_data[i] = str(row_data[i])

                if ui.horizantel_export.isChecked():
                    worksheet.write_column(0, row_num, row_data, cell_format = current_format)
                    worksheet.freeze_panes(0, 1)
                else:
                    worksheet.write_row(row_num, 0, row_data, cell_format = current_format)
                    worksheet.freeze_panes(1, 0)

            if ui.horizantel_export.isChecked():
                for i in range(len(headers_data)):
                    worksheet.set_row(i, i, len(headers_data[i])+5)
            else:
                for i in range(len(headers_data)):
                    worksheet.set_column(i, i, len(headers_data[i])+5)



            workbook.close()
            def open_created_file(file_name):
                try:# linux and mac
                    os.system('open '+file_name)
                except:
                    try:# windows
                        os.system('start '+file_name)
                    except:
                        ui.close()

            threading.Thread(target=open_created_file, args=(file_name,)).start()
            

    

    app.UI.subwindow.ui.select_all_fields.setChecked(2)
    app.UI.subwindow.ui.select_all_items.setChecked(2)
    app.UI.subwindow.ui.select_all_fields.clicked.connect(lambda: select_all_fields_status_changed(app.UI.subwindow.ui))
    app.UI.subwindow.ui.select_all_items.clicked.connect(lambda: select_all_items_status_changed(app.UI.subwindow.ui))
    app.UI.subwindow.ui.horizantel_export.clicked.connect(lambda: h_r_fields_sorting_changed(app.UI.subwindow.ui))
    app.UI.subwindow.ui.vertical_export.clicked.connect(lambda: h_r_fields_sorting_changed(app.UI.subwindow.ui))
    app.UI.subwindow.ui.export_btn.clicked.connect(lambda: export_csv(app.UI.subwindow.ui))
    category_changed(app.UI.subwindow.ui)
    app.UI.subwindow.ui.categories.currentIndexChanged.connect(lambda: category_changed(app.UI.subwindow.ui))
    app.UI.subwindow.show()

