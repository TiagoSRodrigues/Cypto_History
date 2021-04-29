# Cypto_History
Web scrapper to get crypto prices history

## Files:
### import_data_functions.py
> functions to get the information from website's api  

### get_all_price_history.py
Automatically get all the past history from all coins  


### update_database.py
Checks the last day in the database and if is older then a day gets the new information  


### ETL.py
Get the data from seperated json for each day and compile in panda's dataframes
