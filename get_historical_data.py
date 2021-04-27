
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

def get_day_data(day, start=1, page=""):
    url = prepare_request(config_file, "USD,EUR,BTC", day, 5000, 1)
    response = requests.get(url)

    #sleep randomly to avoid blocking
    time.sleep(random.randint(2, 5)) 


    if response.status_code != 200:
        print("\n\n\n\n ATTENTION: something is wrong with day:",day,"\n\n\n")

    soup = BeautifulSoup(response.content, "html.parser")
    soup_text=soup.text
    data_json=json.loads(soup_text)
    save_json_to_file("crypto_" + str(day) + page, data_json)
    
    if get_last_element(data_json)>=4999:
        get_day_data(day, start=4999,page="pag2")
        #when they change the coins limit per page this will be out of date but ... for now it’s enough

def get_last_element(data):
    return data["data"][-1]["cmc_rank"]

def save_json_to_file(filename,json_data):
    location=directory_path = r'%s' % os.getcwd().replace('\\','//')+ "//data//"

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

    final_day=next_day(next_day(next_day(day)))


    while day <=  final_day:
        print("starting day:",day)
        get_day_data(day)
        day=next_day(day)
        
 

# get configurations
config_file=get_configurations()
get_history(start=config_file["first_day"], finish = date.today() - timedelta(days=1))