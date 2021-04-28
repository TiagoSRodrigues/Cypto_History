
import  requests, json, datetime, os, yaml , time, random
from bs4 import BeautifulSoup
from datetime import timedelta , date
 
def next_day(day):
    day=str(day)
    y,m,d = day[0:4],day[5:7],day[8:10]
    return datetime.date(int(y), int(m), int(d)) + timedelta(days = 1)

#Import Configurations
def get_configurations():
    directory_path = r'%s' % os.getcwd().replace('\\','//')

    configuration_file=directory_path + "//configuration.yaml"
    with open(configuration_file) as file:
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)
    
    return config_yaml 

def get_day_data(day, start=1, limit=1000, page=1):
    
    
    print("day",day," start", start, "limit", limit," page", page)
    
    
    url = prepare_request(config_file, "USD,EUR,BTC", day, limit, 1)
    response = requests.get(url)

    #sleep randomly to avoid blocking
    time.sleep(random.randint(2, 5)) 


    if response.status_code != 200:
        print("\n\n\n\n ATTENTION: something is wrong with day:",day,"\n\n\n")

    soup = BeautifulSoup(response.content, "html.parser")
    soup_text=soup.text
    data_json=json.loads(soup_text)
    save_json_to_file("crypto_" + str(day) + "_" + str(page), data_json)
    
    last_coin=get_last_element(data_json)
    
    if last_coin == limit:
        get_day_data(day, start=last_coin + 1, limit=last_coin + 1000, page = page+1)

def get_last_element(data):
    return data["data"][-1]["cmc_rank"]

def save_json_to_file(filename,json_data):
    # location=directory_path = r'%s' % os.getcwd().replace('\\','//')+ "//data//"
    location = "E://Crypto_hystory//"
    with open(location+str(filename)+'.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

def prepare_request(config_file, convert, date, limit, start):
    base_url=config_file["base_url"]
    convert=str(convert)
    date=str(date)
    limit=str(limit)
    start=str(start)
    return base_url + "historical?" + 'convert=' + convert +"&date="+ date +"&limit="+ limit +"&start="+ start


def get_history(start,finish):
    day = start

    while str(day) <=  str(finish):
        if finish >  str(date.today() - timedelta(days=1)):
            print("I can not predict the future!")
            break
        get_day_data(day)
        day=next_day(day)
        
 

# get configurations
config_file=get_configurations()
get_history(start=config_file["first_day"], finish = str(date.today() - timedelta(days=1)))
# get_history(start="2021-04-27", finish = str(date.today() - timedelta(days=1)))