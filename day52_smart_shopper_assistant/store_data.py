import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Koneksi ke MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_shopper_db"]
collection = db["common_information"]

def store_json_to_mongo():
    # Membaca file data
    with open("data/common_info.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Menghapus data lama agar tidak duplikat, lalu masukkan data baru
    collection.delete_many({})
    collection.insert_many(data)
    print(f"Berhasil menyimpan {len(data)} dokumen Common Information ke MongoDB Atlas!")

if __name__ == "__main__":
    store_json_to_mongo()