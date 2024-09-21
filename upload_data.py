from pymongo.mongo_client import MongoClient
import pandas as pd
import json

url = "mongodb+srv://supriyosarkar25111992:12345@cluster0.j7bf0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(url)

DB_NAME = "pwskills"
CONNECTION_NAME = "wafer_fault"

data_path = "C:\Project Sensor Fault\notebooks\wafer_23012020_041211.csv"
df = pd.read_csv(data_path)
df.drop("Unnamed: 0", axis = 1, inplace=True)

json_records = list(json.loads(df.T.to_json()).values())

db1 = client[DB_NAME][CONNECTION_NAME]
db1.insert_many(json_records)