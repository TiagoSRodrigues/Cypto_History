from sys import dont_write_bytecode
from typing import Counter
from requests.api import get
import import_data_functions as idf, os, json
import pandas as pd    

config_yaml=idf.get_configurations()

def get_files_in_db(path):
    return os.listdir(path)
    
file_list=get_files_in_db(config_yaml["database_path"])    

def update_index():
    index={"days":[]}
    
    days_in_list=get_days_in_db()


    def get_files_from_day(day):
        files_from_day=[]
        for file in file_list:
            if file[7:17] == day:
                files_from_day.append(file)
        return files_from_day

    def add_day_to_json(day):
        file_list=get_files_from_day(day)
        element={"day"  : day,
                "pages": len(file_list)}
        index["days"].append(element)


    for day in days_in_list:
        add_day_to_json(day)

    with open('index.json', 'w') as outfile:
        json.dump(index, outfile)

    
def get_days_in_db():
    days_in_list=[]
    for dayfile in file_list:
        if dayfile[7:17] not in days_in_list:
            days_in_list.append(dayfile[7:17])
    return days_in_list

update_index()




def import_to_df():

    def get_coin_data(day,pages):
        with open("index.json", "r") as read_file:
            coin_data = json.load(open(read_file))

        # df = pd.DataFrame(data["result"] 

        df = coin_data# pd.read_json(coin_data)

        print(day, pages,type(df))



    with open("index.json", "r") as read_file:
        index = json.load(read_file)

    for i in range(10):#:len(index["days"])):
        day=index["days"][0]["day"]
        pages=index["days"][0]["pages"]
        
        while pages > 0 :
            get_coin_data(day, pages)
            pages-=1

        



    # json.loads(coin_data)
    # data["data"][-1]["cmc_rank"]

# import_to_df()
# file=json.load(config_yaml["database_path"]+file_list[0])
# df = pd.read_json(file)

# xx="C:\Crypto\price_db\crypto_2021-04-27_5.json"
xx= json.load(open("C://Crypto//price_db//crypto_2021-04-27_5.json"))
df = pd.read_json(xx)
print(df)

# print(config_yaml["database_path"]+file_list[0])
