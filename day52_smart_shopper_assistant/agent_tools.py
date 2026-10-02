import os
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["smart_shopper_db"]
collection = db["common_information"]

@tool
def common_information_tool(query: str) -> str:
    """
    Gunakan tools ini untuk menjawab pertanyaan umum seputar proses jual-beli e-commerce, 
    seperti informasi pengiriman, kebijakan refund, metode pembayaran, dan syarat ketentuan toko.
    """
    # Pencarian teks sederhana di MongoDB (Strategi Retrieval RAG)
    results = collection.find({"$text": {"$search": query}}, {"_id": 0})
    results_list = list(results)
    
    if not results_list:
        # Fallback pencarian regex jika text index belum aktif
        all_docs = collection.find({}, {"_id": 0})
        matched = [doc for doc in all_docs if any(word in doc['question'].lower() for word in query.lower().split())]
        if matched:
            results_list = matched
        else:
            return "Maaf, informasi mengenai hal tersebut tidak ditemukan di kebijakan toko kami."

    response_text = "Informasi Terkait:\n"
    for item in results_list:
        response_text += f"- Q: {item['question']}\n  A: {item['answer']}\n\n"
        
    return response_text

@tool
def product_recommendation_tool(preference: str) -> str:
    """
    Gunakan tools ini khusus untuk memberikan rekomendasi produk berdasarkan preferensi atau kategori barang yang dicari pengguna.
    """
    # Simulasi database produk rekomendasi
    products = {
        "baju": "Rekomendasi: Kaos Polos Premium (Rp 75.000) dan Kemeja Flanel Casual (Rp 150.000).",
        "sepatu": "Rekomendasi: Sepatu Sneakers Running Sporty (Rp 350.000) dan Loafers Kulit Formal (Rp 450.000)."
    }
    
    for key, val in products.items():
        if key in preference.lower():
            return val
    return "Rekomendasi Umum: Jaket Denim Casual (Rp 250.000) yang sedang diskon 20% hari ini!"