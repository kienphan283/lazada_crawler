import pandas as pd
import csv 

df = pd.read_csv("name_tablet.txt", sep='\s\s+', engine='python', quoting=csv.QUOTE_MINIMAL, on_bad_lines='skip')

df.to_csv("name_tablets.csv", index=False)