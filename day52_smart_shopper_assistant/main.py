import os
from dotenv import load_dotenv
from google import genai
from agent_tools import common_information_tool, product_recommendation_tool

load_dotenv()

# Inisialisasi Google GenAI SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def run_smart_shopper_agent(user_query: str):
    print(f"\nUser Query: {user_query}")
    
    # Pengaturan System Prompt dan Routing otomatis
    prompt = f"""
    Kamu adalah Personalized SmartShopper Assistant, sebuah AI Agent e-commerce yang cerdas.
    Tugasmu adalah membantu pembeli dengan memilih tindakan yang tepat:
    1. Jika pengguna bertanya tentang rekomendasi barang, pakaian, atau produk, gunakan product_recommendation_tool.
    2. Jika pengguna bertanya tentang aturan toko, pengiriman, cara bayar, atau refund, gunakan common_information_tool.
    
    Pertanyaan Pengguna: {user_query}
    """
    
    # Menggunakan Gemini Model untuk memproses agent
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        # Mengintegrasikan tools buatan kita
        config={
            'tools': [common_information_tool, product_recommendation_tool]
        }
    )
    
    print("Agent Response:")
    print(response.text)

if __name__ == "__main__":
    # Pengujian dan Validasi (Sesuai Poin 7 Detail Assignment)
    run_smart_shopper_agent("Bagaimana cara saya melakukan refund barang yang rusak?")
    run_smart_shopper_agent("Tolong rekomendasikan sepatu yang bagus untuk olahraga.")