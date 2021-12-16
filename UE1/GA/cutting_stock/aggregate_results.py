import pandas as pd

table_20 = pd.read_csv("ga_table_20.csv").mean(axis=0)
table_200 = pd.read_csv("ga_table_200.csv").mean(axis=0)
table_500 = pd.read_csv("ga_table_500.csv").mean(axis=0)
print([table_20, table_200, table_500])
