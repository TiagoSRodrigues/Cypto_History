import general_funtions as gf

config_file = gf.get_configurations()
data_sets=config_file["data_sets"]

import pandas as pd
df = pd.read_csv('data_sets.csv')
(
   df
    .groupby(by='category')
    .agg({'num': 'sum', 'char': 'count'})
    .reset_index()
)