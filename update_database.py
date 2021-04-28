import import_data_functions as ipt
import os, json
from datetime import timedelta , date, datetime

config_file = ipt.get_configurations()

db_location = config_file["database_path"] 



# print(days_in_history[2])
def get_files_in_db(path):
    file_list = os.listdir(path)
    return file_list


def sort_days(days_list):
    #for a list like this:  ['crypto_2021-04-27_5.json'...]
    def get_day(file_name):
        return(file_name[7:18])

    return sorted(days_list, key = get_day) 


def get_last_day_filename(file_path): 
    sorted_days=sort_days(get_files_in_db(db_location))
    return sorted_days[-1]


def check_new_data():
    last_day_stored = get_last_day_filename(db_location)[7:17]
    print("\n Last day in history:" , last_day_stored)
    

    if last_day_stored == str(  str(date.today()  -  timedelta(days=1))):
        print("\n History updated! \n")
    else:
        ipt.get_history( start  =str(  datetime.strptime(last_day_stored, '%Y-%m-%d').date() + timedelta(days=1)),
                         finish = str(date.today()    - timedelta(days=1)))


check_new_data()

  