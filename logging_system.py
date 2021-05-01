## LOGGING MANAGEMENT FILE
from datetime import datetime
import logging, time, os, gc, yaml, time
# from typing_extensions import runtime
from tqdm import tqdm


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                                   Configurations                                                                                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

directory_path = r'%s' % os.getcwd().replace('\\','//')
configuration_file=directory_path + "//configuration.yaml"


#Files Directories
datasetes=directory_path + "//data//datasetes//"
logs_file_location = directory_path + '//Data//Logs//'


#paramenters   ##LOGS: DEBUG,  INFO, WARNING                #not in use: ERROR, CRITICAL 
Logging_level="DEBUG"

#Max number of logs to save, if all = False 
nr_of_log_to_save= 10

#Define if the logs are printed in the terminal while running
print_log_in_terminal=True
Terminal_printting_level="INFO"

#Run tests before simulations
Run_tests=True

# print(logs_file_location)

#create the log file
logging.basicConfig(filename=logs_file_location+'log_'+time.strftime("%Y%m%d_%H-%M-%S", time.localtime())+'.log', 
        level=Logging_level,
         format='%(asctime)s %(levelname)s %(message)s')



getattr(logging, Logging_level.lower() )("---> Started   <----")

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                                   Funcions                                                                                                  |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+




def log(debug_msg = None, info_msg = None, warning_msg = None):
    #Receive the logging level from envirement
    log_level = logging.root.level

    if debug_msg == None and info_msg != None:
        debug_msg=info_msg
        
    if debug_msg == None and info_msg == None and warning_msg != None:
        debug_msg=warning_msg

    #check veriable for printing
    if print_log_in_terminal == True:
        if Terminal_printting_level == "WARNING" and warning_msg !=None:
            print(warning_msg)        
        elif Terminal_printting_level == "INFO" and info_msg !=None:
            print(info_msg)        
        elif Terminal_printting_level == "DEBUG":
            print(debug_msg)
    
    #records log        
    if  log_level == 30 and warning_msg != None:
        logging.warning(str(warning_msg))
    
    
    elif log_level == 20 and info_msg != None:
        logging.info(str(info_msg))
        if warning_msg != None:
            logging.warning(str(warning_msg))
    
    
    elif log_level == 10 and debug_msg != None :
        logging.debug(str(debug_msg))
        if warning_msg != None:
            logging.warning(str(warning_msg))
        if info_msg != None:
            logging.info(str(info_msg))
        


#this funcion delete old logs, to avoid excessive trash        
def delete_old_logs(nr_of_files):
    arr = os.listdir(logs_file_location)
        
    if nr_of_files == all:
        return
    for el in range(0,len(arr)-nr_of_files):
        try:
            os.remove(logs_file_location+arr[el])
        except:
            pass


def show_object_attributes(object):
    from pprint import pprint
    print(3*"\n","Attributes of",object,"\n")
    pprint(vars(object))
    print(3*"\n")

def open_object(object):
    print(10*"======","\n\n DIR:")
    for el in dir(object):
        print(el)
    print(10*"======","\n\n VARS")
    for el in vars(object):
        print(el)

    print(10*"======","\n\n\n")

def get_variables(var=None):
    if var == "globals":
        for el in globals():
            print(el)       
    if var == "locals":
        for el in locals():
            print(el)     

    else:
        print("\n GLOBALS \n")
        for el in globals():
            print(el) 

        print("\n LOCALS \n")
        for el in locals():
            print(el)   


def save_all_objects():
    filename="All_objects_"+time.strftime("%Y%m%d_%H-%M-%S", time.localtime())+".txt"
    with open(filename, 'w') as filehandle:
        errors=0
        for el in gc.get_objects():
            try:
                filehandle.write( str(el)+'\n')
            except:
                errors+=1
        filehandle.write( '\n and more '+str(errors)+" Errors")

def get_runtime(start_time):
    sec = time.perf_counter()  - start_time
    min = sec/60
    hor = min/60

    print("Runtime in",int(hor),"h  ",int(min),"m  ",int(sec),"s" )
    

delete_old_logs(nr_of_log_to_save)

