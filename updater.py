import requests
import pandas as pd
from git import Repo
import os

url = "https://api.globe.gov/search/v1/measurement/protocol/measureddate/?protocols=mosquito_habitat_mapper&startdate=2020-06-01&enddate=2020-07-04&geojson=FALSE&sample=TRUE"

response = requests.get(url)
globe_data = response.json()["results"]
globe_data_df = pd.DataFrame(globe_data)
data_df = pd.DataFrame(globe_data_df["data"].to_dict())
data_df = data_df.transpose()
mosquito_data_df = globe_data_df.join(data_df)
mosquito_data_df.drop(["data"], axis=1)
mosquito_data_df[["mosquitohabitatmapperLarvaeCount", "latitude", "longitude"]].fillna(0)


mosquito_data_df.to_csv("mosquito_data.csv")

repo = Repo(os.getcwd())

file_list = [
    "mosquito_data.csv"
]
commit_message = 'Automated data commit of GLOBE data'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push("master")