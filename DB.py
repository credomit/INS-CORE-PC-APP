import sqlite3 as sql

colors = {
    True : 48,
    False: 1
}


class DataBase(object):
    def __init__(self, path, app, tables):
        self.path = path
        self.app  = app
        self.tables = tables
        self.check_all_tables_creation_status()


    def check_all_tables_creation_status(self):
        
        for table in self.tables:

            print("Checking table "+table, end='')
            s = self.check_table_creation_status(table)
            print(" \033[92m Done \033[0m")

    def check_table_creation_status(self, table_name) -> bool:

        conn = sql.connect(self.path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type ='table'").fetchall()
        tables = [ i[0] for i in tables ]
        
        columns = self.tables[table_name]
        

        STATUS = True

        if table_name not in tables:
            columns_str = ', '.join([ f'{name} ' for name in columns ])
            print(" \033[94m Creating table \033[0m", end='')
            conn.execute(f"create table { table_name } ({columns_str}, id integer primary key autoincrement)")
            
            STATUS = False

        else:
            current_columns = ( bit[0] for bit in conn.execute(f'select * from {table_name}').description )
            current_columns = [i for i in current_columns]
            reqested_columns = columns
            
            new_Columns =  list(set( reqested_columns ) - set(current_columns))
            
            for new_column in new_Columns:
                print(" \033[94m Add New column \033[0m", end='')
                try:
                    conn.execute(f"ALTER TABLE {table_name} ADD {new_column}")

                    STATUS = False
                except:
                    pass

                
        conn.close()
        

        return STATUS

    def get_table_data(self, table):
        conn = sql.connect(self.path)
        columns = list( bit[0] for bit in conn.execute(f'select * from {table}').description )
        data = conn.execute(f'SELECT * from {table}').fetchall()
        dict_data = []
        for bit in data:
            dict_data.append({ columns[i]:bit[i] for i in range(len(columns)) })

        print(table, data)
        conn.close()
        return dict_data


    def add_item(self, table, data):
        conn = sql.connect(self.path)
        columns = '"'+'", "'.join(list(data.keys()))+'"'
        columns = columns.replace(' None', ' ""')
        values = str(list(data.values()))[1:-1].replace("'",'"')

        print((f'''insert into {table} ({columns}) values ({values})'''))
        adding = conn.execute(f'''insert into {table} ({columns}) values ({values})''')
        data['id'] = adding.lastrowid
        
        conn.commit()
        conn.close()

        return data

    def edit_item(self, data):
        # data {
        #       table: str, 
        #       data: dict, 
        #       id: INT 
        # }
        
        table = data.get('table')

        conn = sql.connect(self.path)

        columns = list(data.get('data').keys())
        
        
        for i in range(len(columns)):
            bit = data.get("data")[columns[i]]
            try:
                bit = int(bit)
            except:
                bit = '"'+str(bit).replace('"', "'")+'"'
            
            conn.execute(f'''update {table} set "{columns[i]}" = {bit} where id = {data.get("id")}''')
        
        
        conn.commit()
        conn.close()

        return data