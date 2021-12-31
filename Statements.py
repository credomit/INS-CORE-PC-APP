from typing import NewType
import notifiers, re
from . import Statements


def replace_variable_value(self, text):
  
        view_vars = re.findall('\{.*?\}' , text)
        returned_view_name = text

        for var in view_vars:
            obs_var = var[1:-1] # remove  { }  
            if obs_var in vars(self): # direct variable
                data_r = vars(self)[obs_var]
                


            elif obs_var.split('.')[0] in vars(self): 
                main_obj = self
                final_value = ''
                for splited_var in obs_var.split('.'):
                    final_value = getattr(main_obj, splited_var)
                    main_obj = final_value
                
                data_r = final_value
                    


            else:
                if obs_var[-5:] == 'sigma':
                    data_r = 0
                else:
                    data_r = ''
                setattr(self, obs_var ,data_r )
                print(f'\033[31mERROR {var} field not existing in view_name \033[93m field place will leave as {data_r} \033[0m ')




            returned_view_name = returned_view_name.replace(var , str(data_r))

        return returned_view_name


def Equality_If_Statement(args):
    return float(eval(args['value_1'])) == float(eval(args['value_2']))


def Bigger_Num_If_Statement(args):
    return float(eval(args['bigger_num'])) > float(eval(args['smaller_num']))



def Bigger_Or_Equal_Num_If_Statement( args ):
    return float(eval(args['bigger_num'])) >= float(eval(args['smaller_num']))




def chack_static_statement_status(statement, app, item = None , data= None):
    status = True
    if statement != {}:
        ed_statement = str(statement['statement'])
        status = eval(ed_statement)
        if not status:
            error_msg = statement.get('error_msg')
            if error_msg !=None:
                notifiers.Notification( app.translate(statement.get('error_msg')),app.translate(error_msg) ,app.app_logo ).show()

    return status
        

