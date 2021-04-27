# https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?convert=USD,BTC&date=2020-04-28&limit=5000&start=201

# get Cryp
# tocurrency Historical Data Snapshot
import  requests, json, datetime, os, yaml 
from bs4 import BeautifulSoup
from datetime import timedelta 
 

 
# url="https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?convert=USD,BTC&date=2021-04-26&limit=10&start=1"

day_zero=20130428

#print(base_url+str(day_zero))

def next_day(day):
    day=str(day)
    y,m,d = day[:4],day[4:6],day[6:]
    return datetime.datetime(int(y), int(m), int(d)) + timedelta(days = 1)

def get_data_table(url):
    table_MN = pd.read_html(url)
    df = table_MN[2]
    print(df.describe())
    # print("1\n",table_MN)
    # print("2\n\n\n\n",f'Total tables: {len(table_MN)}')

#Import Configurations
def get_configurations():
    directory_path = r'%s' % os.getcwd().replace('\\','//')

    configuration_file=directory_path + "//configuration.yaml"

    with open(configuration_file) as file:
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)
    return config_yaml 





def get_day_data(day):
    response = requests.get(url)
    if response.status_code != 200:
        print("something is wrong")

    soup = BeautifulSoup(response.content, "html.parser")
    soup_text=soup.text
    data_json=json.loads(soup_text)

    if get_last_element(data_json) > 4999:
        print("Day",day,"has more than 5000 coins")
    save_json_to_file("Teste",data_json)
    print("Erro: ")#,data_json)




def get_last_element(data):
    return data["data"][-1]["cmc_rank"]



def save_json_to_file(filename,json_data):
    with open(str(filename)+'.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

# base_url=config_file["base_url"]
# url= base_url+str(day_zero)
print("URL:",url)


def prepare_request(config_file, convert, date, limit, start):
    base_url=config_file["base_url"]
    convert=str(convert)
    date=str(date)
    limit=str(limit)
    start=str(start)
    return base_url + "historical?" + 'convert=' + convert +"&date="+ date +"&limit="+ limit +"&start="+ start




# https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?convert=USD,BTC&date=20-02-2020&limit=5&start=2

def get_history():
    config_file=get_configurations()

    for i in range:
        
    prepare_request(config_file, "USD,EUR,BTC", date, limit, start)