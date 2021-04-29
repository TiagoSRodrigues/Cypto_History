from sys import dont_write_bytecode, platform
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
        el={"day"  : day,
                "pages": len(file_list)}
        index["days"].append(el)


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
    # datadata_file["data"][-1]["cmc_rank"]

# import_to_df()
# file=json.load(config_yaml["database_path"]+file_list[0])
# df = pd.read_json(file)



def extract_coin_data(file_index):
    day=file_list[file_index][7:17]
    columns=[
        #identificação
            "id", "name", "symbol", "slug", 
        #mercado
            "num_market_pairs", "date_added", "max_supply","circulating_supply","total_supply",
        #tags
            "tags",
        #tech    
            "platform", "platform_name", "platform_symbol",  
        #Ranking    
            "cmc_rank","last_updated",
        #prices    
            "BTC_price","BTC_volume_24h","BTC_percent_change_1h","BTC_percent_change_24h","BTC_percent_change_7d","BTC_market_cap","BTC_last_updated",
            "EUR_price","EUR_volume_24h","EUR_percent_change_1h","EUR_percent_change_24h","EUR_percent_change_7d","EUR_market_cap","EUR_last_updated",
            "USD_price","USD_volume_24h","USD_percent_change_1h","USD_percent_change_24h","USD_percent_change_7d","USD_market_cap","USD_last_updated"]

    mini_col=["id", "name", "symbol", "slug", ]
    #Abre o ficheiro
    
    with open(  config_yaml["database_path"] + file_list[file_index]   ) as file:    
        data_file = json.load(file) 
    

    #create the dataframe
    raw_data = []
    price_data = []
    
    # print(data_file["data"][1])
    for el in  range(0, len(data_file["data"])-1, 1 ):
        platform_name, platform_symbol = None, None

        c_id                    , name                   = data_file["data"][el]["id"]                     , data_file["data"][el]["name"]
        c_symbol                , slug                   = data_file["data"][el]["symbol"]                 , data_file["data"][el]["slug"]
        num_market_pairs        , date_added             = data_file["data"][el]["num_market_pairs"]       , data_file["data"][el]["date_added"]
        tags                    , max_supply             = data_file["data"][el]["tags"]                   , data_file["data"][el]["max_supply"]
        circulating_supply      , total_supply           = data_file["data"][el]["circulating_supply"]     , data_file["data"][el]["total_supply"]
        platform_info           , cmc_rank               = data_file["data"][el]["platform"]               , data_file["data"][el]["cmc_rank"]

        if isinstance( platform_info, dict): 
            platform_name           , platform_symbol        = data_file["data"][el]["platform"]["name"]       , data_file["data"][el]["platform"]["symbol"]

        last_updated            , BTC_price              = data_file["data"][el]["last_updated"]                       , data_file["data"][el]["quote"]["BTC"]["price"]
        BTC_volume_24h          , BTC_percent_change_1h  = data_file["data"][el]["quote"]["BTC"]["volume_24h"]         , data_file["data"][el]["quote"]["BTC"]["percent_change_1h"]
        BTC_percent_change_24h  , BTC_percent_change_7d  = data_file["data"][el]["quote"]["BTC"]["percent_change_24h"] , data_file["data"][el]["quote"]["BTC"]["percent_change_7d"]           
        BTC_market_cap          , BTC_last_updated       = data_file["data"][el]["quote"]["BTC"]["market_cap"]         , data_file["data"][el]["quote"]["BTC"]["last_updated"]
        EUR_price               , EUR_volume_24h         = data_file["data"][el]["quote"]["EUR"]["price"]              , data_file["data"][el]["quote"]["EUR"]["volume_24h"]
        EUR_percent_change_1h   , EUR_percent_change_24h = data_file["data"][el]["quote"]["EUR"]["percent_change_1h"]  , data_file["data"][el]["quote"]["EUR"]["percent_change_24h"]
        EUR_percent_change_7d   , EUR_market_cap         = data_file["data"][el]["quote"]["EUR"]["percent_change_7d"]  , data_file["data"][el]["quote"]["EUR"]["market_cap"]
        EUR_last_updated        , USD_price              = data_file["data"][el]["quote"]["EUR"]["last_updated"]       , data_file["data"][el]["quote"]["EUR"]["price"]
        USD_volume_24h          , USD_percent_change_1h  = data_file["data"][el]["quote"]["USD"]["volume_24h"]         , data_file["data"][el]["quote"]["USD"]["percent_change_1h"]
        USD_percent_change_24h  , USD_percent_change_7d  = data_file["data"][el]["quote"]["USD"]["percent_change_24h"] , data_file["data"][el]["quote"]["USD"]["percent_change_7d"]
        USD_market_cap          , USD_last_updated       = data_file["data"][el]["quote"]["USD"]["market_cap"]         , data_file["data"][el]["quote"]["USD"]["last_updated"]

        raw_data.append ([            
                c_id                     , name                 
                ,c_symbol                , slug                 
                ,num_market_pairs        , date_added           
                ,tags                    , max_supply           
                ,circulating_supply      , total_supply         
                ,platform_info           , cmc_rank             
                ,platform_name           , platform_symbol  
                ,last_updated            , BTC_price            
                ,BTC_volume_24h          , BTC_percent_change_1h
                ,BTC_percent_change_24h  , BTC_percent_change_7d
                ,BTC_market_cap          , BTC_last_updated     
                ,EUR_price               , EUR_volume_24h       
                ,EUR_percent_change_1h   , EUR_percent_change_24h
                ,EUR_percent_change_7d   , EUR_market_cap       
                ,EUR_last_updated        , USD_price            
                ,USD_volume_24h          , USD_percent_change_1h
                ,USD_percent_change_24h  , USD_percent_change_7d
                ,USD_market_cap          , USD_last_updated     
                ])
        
        price_data.append([day,c_id,c_symbol,USD_price,EUR_price,BTC_price])

    
    price_df=pd.DataFrame(price_data,columns=["date","coin_id","Symbol","USD","EUR","BTC"])
    raw_df=pd.DataFrame(raw_data,columns=columns)
    
    price_df.to_csv("raw_price_data.csv",sep=";")
    raw_df.to_csv("raw_data.csv",sep=";")  
            
extract_coin_data(-1)