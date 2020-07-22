import requests
import pandas as pd
import os
from datetime import date

ids = pd.read_csv('IDs.txt', sep=" ", header=None)
id_list = (ids[0].tolist())
today = date.today()
protocols = ["mosquito_habitat_mapper", "land_covers"]

for protocol in protocols:
    main_df = pd.DataFrame()
    for user_id in id_list:
        url = f"https://api.globe.gov/search/v1/measurement/protocol/measureddate/userid/?protocols={protocol}&startdate=2020-06-01&enddate={today}&userid={user_id}&geojson=FALSE&sample=FALSE"
        response = requests.get(url)
        #print(response.content)
        data = response.json()["results"]
        
        temp_data_df = pd.DataFrame(data)
        if not temp_data_df.empty:
            temp_data_df["data"]
            data_df = pd.DataFrame(temp_data_df["data"].to_dict())
            data_df = data_df.transpose()
            temp_data_df = temp_data_df.join(data_df)
            temp_data_df.drop(["data"], axis=1)
            main_df = main_df.append(temp_data_df)
    main_df.to_csv(f"results/{protocol}{today}.csv")