from . import DB


class Local(object):
    
    def __init__(self, DB_PATH, Data_controller, **kwargs):
        self.DataBase = DB.DataBase(DB_PATH, Data_controller.APP, Data_controller.APP.tables)
        

    def get_model_data(self, model):
        table_name = model.__class__.__name__
        return self.DataBase.get_table_data(table_name)


    def add_item(self, model, data):
        table_name = model.__class__.__name__
        return self.DataBase.add_item(table_name, data)

    def edit_item(self, item_obj):
        # data {
        #       table: str, 
        #       data: dict, 
        #       id: INT 
        # }
        
        item_data = {}
        for var in item_obj.data.vars:
            item_data[var] = getattr(item_obj.data, var)
        

        data = {
            'table' : item_obj.model.__class__.__name__,
            'data'  : item_data,
            'id'    : item_obj.id
        }

        self.DataBase.edit_item( data)

    def delete(self):
        pass


class API(object):

    def chack_table(self):
        pass

    def insert(self):
        pass

    def edit(self):
        pass
    
    def delete(self):
        pass


class API_and_Local(object):

    def chack_table(self):
        pass

    def insert(self):
        pass

    def edit(self):
        pass
    
    def delete(self):
        pass