import pandas as pd,  os, json, csv, datetime, time
# os.system('cls' if os.name == 'nt' else 'clear')
from requests.api import get
import import_data_functions as idf, logging_system as logs, warnings_functions as wf


config_file = idf.get_configurations()
directory_path = r'%s' % os.getcwd().replace('\\','//') 
start_time = time.perf_counter()
coin_db_location =  config_file["coin_database_path"] 
db_location = config_file["database_path"]    
datasets_location = config_file["data_sets"]    


def get_files_in_dir(path):
    return os.listdir(path)
    


file_list=get_files_in_dir(coin_db_location)    


def update_index():
    logs.log(debug_msg = "[funcion called],"+" "+"update_index")
    index={"days":[]}
    
    days_in_list=get_days_in_db()


    def get_files_from_day(day):
        logs.log(debug_msg = "[funcion called],"+" "+"get_files_from_day arg:"+str(day))

        files_from_day=[]
        for file in file_list:
            if file[7:17] == day:
                files_from_day.append(file)
        return files_from_day

    def add_day_to_json(day):
        logs.log(debug_msg = "[funcion called],"+" "+"add_day_to_json arg:"+str(day))
        file_list=get_files_from_day(day)
        el={"day"  : day,
                "pages": len(file_list)}
        index["days"].append(el)


    for day in days_in_list:
        add_day_to_json(day)

    with open('index.json', 'w') as outfile:
        json.dump(index, outfile)

    
def get_days_in_db():
    logs.log(debug_msg = "[funcion called],"+" "+"get_days_in_db arg:")
    days_in_list=[]
    for dayfile in file_list:
        if dayfile[7:17] not in days_in_list:
            days_in_list.append(dayfile[7:17])
    return days_in_list


def save_list_to_csv(filename,rows, headers=None ):
    with open(filename,"w",   newline='',) as file:
        write=csv.writer(file, delimiter=";")
        if headers != None:
            write.writerow(headers)
        write.writerows(rows)



#n me lembro o que isto faz

def import_to_df():
    logs.log(debug_msg = "[funcion called],"+" "+"import_to_df arg:")
    def get_coin_data(day,pages):
        with open("index.json", "r") as read_file:
            coin_data = json.load(read_file)

    with open("index.json", "r",  ) as read_file:
        index = json.load(read_file)

    for i in range(10):#:len(index["days"])):
        day=index["days"][0]["day"]
        pages=index["days"][0]["pages"]
        
        while pages > 0 :
            get_coin_data(day, pages)
            pages-=1



def check_days_in_cache():
    logs.log(debug_msg = "[funcion called],"+" "+"check_days_in_cache arg:")
    
    files_in_cache = get_files_in_dir(db_location+"temp//")
    
    days_in_cache=set()
    
    for file in files_in_cache:
        days_in_cache.add((file[-14:-4]))
    return days_in_cache


def extract_coin_data(file_index):
    logs.log(debug_msg = "[funcion called],"+" "+"extract_coin_data:")
    try:
    # for i in range(0,1,1):    
        day=file_list[file_index][7:17]
        logs.log(debug_msg = "[Extract_coin_data of day:"+str(day))

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

        
        with open(  coin_db_location + file_list[file_index]  , ) as file:    
            data_file = json.load(file) 
        

        #create the dataframe
        raw_data = [columns]
        # price_data = [["date","coin_id","Symbol","USD","EUR","BTC"]]
        price_data = []
        errors = []
        counter=0
        status_code=data_file["status"]["error_code"]
        if  status_code == 0:
            # print("|"+str(status_code)+"|")
            for el in  range(0, len(data_file["data"]), 1 ):
                
                platform_name, platform_symbol = None, None

                c_id                    , name                   = data_file["data"][el]["id"]                     , data_file["data"][el]["name"]
                c_symbol                , slug                   = data_file["data"][el]["symbol"]                 , data_file["data"][el]["slug"]
                num_market_pairs        , date_added             = data_file["data"][el]["num_market_pairs"]       , data_file["data"][el]["date_added"]
                tags                    , max_supply             = data_file["data"][el]["tags"]                   , data_file["data"][el]["max_supply"]
                circulating_supply      , total_supply           = data_file["data"][el]["circulating_supply"]     , data_file["data"][el]["total_supply"]
                platform_info           , cmc_rank               = data_file["data"][el]["platform"]               , data_file["data"][el]["cmc_rank"]

                if isinstance( platform_info, dict): 
                    platform_name           , platform_symbol    = data_file["data"][el]["platform"]["name"]       , data_file["data"][el]["platform"]["symbol"]

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
                        c_id, name, c_symbol, slug, num_market_pairs, date_added, max_supply, circulating_supply, total_supply, tags, platform, platform_name,
                        platform_symbol, cmc_rank, last_updated, BTC_price, BTC_volume_24h, BTC_percent_change_1h, BTC_percent_change_24h, BTC_percent_change_7d,
                        BTC_market_cap, BTC_last_updated, EUR_price, EUR_volume_24h, EUR_percent_change_1h, EUR_percent_change_24h, EUR_percent_change_7d,
                        EUR_market_cap, EUR_last_updated, USD_price, USD_volume_24h, USD_percent_change_1h, USD_percent_change_24h, USD_percent_change_7d,
                        USD_market_cap, USD_last_updated
                        ])
                
                price_data.append([day,c_id,c_symbol,USD_price,EUR_price,BTC_price])

            save_list_to_csv(filename=db_location +"temp//"+ "raw_price_data"+str(day) + ".csv", rows=price_data, headers=["date","coin_id","Symbol","USD","EUR","BTC"])
            save_list_to_csv(filename=db_location +"temp//"+ "raw_data"+str(day) + ".csv", rows=raw_data)
        if  status_code != 0:
            errors.append([day,data_file["status"]])
        # return errors
        elif len(errors)>0:
            with open("//data//Error_logs.logs//Error_coin_data_extract "+str(datetime.datetime.now())[:10]+"_"+
                        str(datetime.datetime.now())[11:13]+"h"+
                        str(datetime.datetime.now())[14:16]+"m"+
                        str(datetime.datetime.now())[22:24]+"s.txt", "w",  "utf-8") as txt_file:
                for el in errors:
                    txt_file.write("".join(str(el)) + "\n") # works with any number of elements in a line
    except:
       logs.log(debug_msg= " [Critical Error], Error in extraction funcion on day"+str(day)) 

def complete_history_ETL(): 
    logs.log(debug_msg = "[funcion called],"+" "+"complete_history_ETL arg:")
    files_in_cache=check_days_in_cache()
    logs.log(debug_msg = "files_in_cache,"+ str(files_in_cache))
    
    for file_index in range( 0, len( file_list )  , 1):
        if file_index % 200 == 0: 
           print(file_index)
            
        
        if file_list[file_index][-14:-4] in files_in_cache: 
            logs.log(debug_msg="[file already in cache]"+str(file_list[file_index]))
            continue
        if file_list[file_index] not in files_in_cache: 
            extract_coin_data(file_index)



def combine_files():
    files = get_files_in_dir(db_location + "temp//")

    logs.log(debug_msg = "[funcion called],"+" "+"combine_files arg:"+ str(files))  
   
    def separate_files():
        # First the files are separeted
        raw_data , raw_price, Errors = [], [], []

        for file in files:
            if   file[0:8] == "raw_data" : raw_data.append(file)
            elif file[0:9] == "raw_price": raw_price.append(file)
            else:Errors.append(file)
        if len(Errors) > 0 : print("Attention!!!, Files not considerated: ", Errors)
        return raw_data, raw_price
    
    raw_data_files, raw_price_files = separate_files()
    
    def create_mega_list(raw_input , filename=None):
        logs.log(debug_msg = "[funcion called],"+" "+"create_mega_list arg:"+ str(raw_input))
        mega_list=[]

        def get_data_to_apped(file):
            logs.log(debug_msg = "[funcion called],"+" "+"get_data_to_apped arg:"+ str(file))

            with open(db_location + "temp//"+ file ) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                data = list(csv_reader)
            return data
        #get headers
        def get_headers(raw_input):
            
            return  get_data_to_apped(raw_input[0])[0] 
        
        def get_rows(raw_input):
            return get_data_to_apped(raw_input)[1:]
        
        mega_list.append(get_headers(raw_input))
        

        #get 1st data
        for file in range(0,len(raw_input),1):
            mega_list.append(get_rows(raw_input[file]))
            # mega_list.append(get_rows(raw_input[file]))
        #append next files w/o headers
        return mega_list

    save_list_to_csv(datasets_location+"Mega_data.csv",create_mega_list(raw_data_files))
    save_list_to_csv(datasets_location+"Mega_price.csv",create_mega_list(raw_price_files))


# combine_files(get_files_in_dir(db_location + "temp//"))


# import update_database as ud
# ud.check_new_data()


# update_index()
# complete_history_ETL()


combine_files()



#ENDIND
logs.get_runtime(start_time)
# wf.play_warnning_sound()
# wf.show_messagem_box("Finished","All done")