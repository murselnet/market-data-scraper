import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# .env dosyasındaki veya ortamdaki değişkenleri yükle
load_dotenv()

def init_supabase_client():
    """
    Ortam değişkenlerinden Supabase URL ve Key'i alarak
    Supabase istemcisini başlatır.
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required.")

    supabase: Client = create_client(url, key)
    return supabase

def save_data_to_supabase(df: pd.DataFrame):
    """
    Verilen DataFrame'i Supabase'deki 'market_data' tablosuna kaydeder.
    """
    try:
        supabase = init_supabase_client()
        # DataFrame'i Supabase'in beklediği format olan dict listesine çevir
        data_to_insert = df.to_dict(orient='records')

        # Veriyi tabloya ekle
        response = supabase.table('market_data').insert(data_to_insert).execute()

        # Yanıtı kontrol et (isteğe bağlı ama iyi bir pratik)
        if len(response.data) > 0:
            print(f"{len(response.data)} adet veri başarıyla Supabase'e kaydedildi.")
        else:
            # Hata detayını response'dan alabiliriz
            print("Veri Supabase'e kaydedilirken bir sorun oluştu.", response)

    except Exception as e:
        print(f"Supabase'e veri kaydı sırasında bir hata oluştu: {e}")
