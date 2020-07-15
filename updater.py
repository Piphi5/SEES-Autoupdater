import requests
import pandas as pd
from git import Repo
import os
from datetime import date
from git import Actor


today = date.today()
url = f"https://api.globe.gov/search/v1/measurement/protocol/measureddate/?protocols=mosquito_habitat_mapper&startdate=2020-06-01&enddate={today}&geojson=FALSE&sample=FALSE"



repo = Repo(os.getcwd())
author = Actor("piphi5", "mateus.sakata@gmail.com")
committer = Actor("A committer", "mateus.sakata@gmail.com")
repo.heads.data.checkout()

response = requests.get(url)
globe_data = response.json()["results"]
globe_data_df = pd.DataFrame(globe_data)
data_df = pd.DataFrame(globe_data_df["data"].to_dict())
data_df = data_df.transpose()
mosquito_data_df = globe_data_df.join(data_df)
mosquito_data_df.drop(["data"], axis=1)
mosquito_data_df[["mosquitohabitatmapperLarvaeCount", "latitude", "longitude"]].fillna(0)


mosquito_data_df.to_csv("mosquito_data.csv")

file_list = [
    "mosquito_data.csv"
]
commit_message = 'Automated data commit of GLOBE data'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push("data")
repo.heads.master.checkout()