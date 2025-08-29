import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# pd.set_option('display.max_rows', None)  # Tüm satırları göster
# pd.set_option('display.max_columns', None)  # Tüm sütunları göster
# pd.set_option('display.width', None)  # Terminal genişliğini sınırlama
# pd.set_option('display.max_colwidth', None)  # Sütun içeriğini kısaltma

# q: bu sayfadaki tüm fonksiyonların adlar
# a: fetch_alternatif, fetch_faiz_bono, fetch_emtia, fetch_altin, fetch_dunya_borsalari
# fetch_doviz, fetch_borsa, fetch_kripto, fetch_alternatif_ve_baltik



#TODO ##########################################################



def fetch_alternatif_ve_baltik():
    # URL'yi belirle
    url = "https://www.bloomberght.com/alternatif"

    # Sayfayı çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Alternatif ve Baltık tablolarını bul
    tables = soup.find_all('table', {'data-type': 'table-type1'})

    # Her tablo için işlem yap
    for table in tables:
        # Tablo başlığını bul
        header = table.find_previous('h2').text.strip()
        
        # Sadece Alternatif ve Baltık tablolarını işle
        if header in ['Alternatif', 'Baltık']:
            # Tablo satırlarını bul
            rows = table.find_all('tr')
            
            # Her satır için işlem yap
            for row in rows[1:]:  # İlk satır başlık olduğu için atlanır
                cols = row.find_all('td')
                
                # İlk sütunu ikiye böl
                first_col = cols[0].text.strip()
                split_col = first_col.split(maxsplit=1)
                col1 = split_col[0] if len(split_col) > 0 else "0"
                col2 = split_col[1] if len(split_col) > 1 else "0"
                
                # Diğer sütunları al ve boş veya NaN değerleri 0 ile değiştir
                col3 = cols[1].text.strip() if cols[1].text.strip() else "0"
                col4 = cols[2].text.strip() if cols[2].text.strip() else "0"
                
                # Veriyi listeye ekle
                data.append([col1, col2, col3, col4])

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=['Kod', 'Açıklama', 'Son', '% Değişim'])

    return df

def fetch_alternatif():
    # URL'yi belirle
    url = "https://www.bloomberght.com/alternatif"

    # Sayfayı çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 'ALTERNATİF' başlıklı tabloyu bul
    table = soup.find('h2', string='Alternatif').find_next('table')

    # Tablo başlıklarını çek
    headers = [header.text.strip() for header in table.find_all('th')]

    # Tablo verilerini çek
    rows = []
    for row in table.find_all('tr')[1:]:  # İlk satır başlık olduğu için atlanır
        cols = row.find_all('td')
        cols = [col.text.strip() if col.text.strip() else "0" for col in cols]  # Boş değerleri '0' yap
        rows.append(cols)

    # DataFrame oluştur
    df = pd.DataFrame(rows, columns=headers)

    # İlk sütunu ikiye böl ve yeni sütunlar ekle
    df[['Kod', 'Açıklama']] = df['ALTERNATİF'].str.split(n=1, expand=True)

    # İstenen sütunları seç ve yeniden adlandır
    df = df[['Kod', 'Açıklama', 'SON', '%']]
    df.columns = ['Kod', 'Açıklama', 'Son', '% Değişim']

    return df



#TODO ##########################################################



def fetch_faiz_bono():
    # HTML sayfasını çek
    url = "https://www.bloomberght.com/faiz-bono"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tahvil ve Repo tablolarını bul
    tables = soup.find_all('table', {'data-type': 'table-type1'})

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Her tablo için işlem yap
    for table in tables:
        # Tablo başlığını bul
        header = table.find_previous('h2').text.strip()
        
        # Sadece Tahvil ve Repo tablolarını işle
        if header in ['Tahvil', 'Repo', 'Eurobondlar', 'Uluslararası Tahviller']:
            # Tablo satırlarını bul
            rows = table.find_all('tr')
            
            # Her satır için işlem yap
            for row in rows[1:]:  # İlk satır başlık olduğu için atlanır
                cols = row.find_all('td')
                
                # İlk sütunu ikiye böl
                first_col = cols[0].text.strip()
                split_col = first_col.split(maxsplit=1)
                col1 = split_col[0] if len(split_col) > 0 else "0"
                col2 = split_col[1] if len(split_col) > 1 else "0"
                
                # Diğer sütunları al ve boş veya NaN değerleri 0 ile değiştir
                col3 = cols[1].text.strip() if cols[1].text.strip() else "0"
                col4 = cols[2].text.strip() if cols[2].text.strip() else "0"
                
                # Veriyi listeye ekle
                data.append([col1, col2, col3, col4])

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=['Kod', 'Açıklama', 'Son', '% Değişim'])

    return df



#TODO ##########################################################



def fetch_emtia():
    # URL'yi belirle
    url = "https://www.bloomberght.com/emtia"

    # Sayfayı çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tabloları bul
    tables = soup.find_all('table', {'data-type': 'table-type1'})

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Her bir tablo için işlem yap
    for table in tables:
        # Tablo başlığını al
        header = table.find_previous('h2').text.strip()
        
        # "Serbest Piyasada Altın" tablosunu atla
        if header == "Serbest Piyasada Altın":
            continue
        
        # Tablo satırlarını al
        rows = table.find_all('tr')
        
        # Her bir satır için işlem yap
        for row in rows[1:]:  # İlk satır başlık olduğu için atlanır
            columns = row.find_all('td')
            if len(columns) >= 3:  # En az 3 sütun olduğundan emin ol
                name = columns[0].text.strip()
                last_price = columns[1].text.strip()
                change = columns[2].text.strip()
                
                # Boş veya NaN değerleri "0" olarak değiştir
                last_price = last_price if last_price else "0"
                change = change if change else "0"
                
                # Veriyi listeye ekle (Başlık sütunu eklenmiyor)
                data.append([name, name, last_price, change])

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=['Emtia', 'Emtia Kopyası', 'Son Fiyat', 'Değişim'])

    return df



#TODO ##########################################################



def fetch_altin():
    # URL'yi belirle
    url = "https://www.bloomberght.com/altin"

    # Sayfayı çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tüm 'economy-table-type3' tablolarını bul
    tables = soup.find_all('div', {'data-widget-type': 'economy-table-type3'})

    # İkinci tabloyu seç (Python'da indeksler 0'dan başlar, bu yüzden 1 kullanılır)
    if len(tables) > 1:
        table = tables[1].find('table', {'data-type': 'table-type1'})
    else:
        raise ValueError("İkinci tablo bulunamadı.")

    # Tablo başlıklarını çek
    headers = [header.text.strip() for header in table.find_all('th')]

    # Verileri çek
    rows = []
    for row in table.find_all('tr')[1:]:  # İlk satır başlık olduğu için atlanır
        cols = row.find_all('td')
        
        # İlk sütundaki veriyi çek (Kod ve İsim)
        first_col = cols[0].find('div', {'class': 'font-bold'})
        kod = first_col.text.strip() if first_col else "Bilinmiyor"
        
        # Kod ve İsim sütunları aynı verileri içerecek
        isim = kod
        
        # Diğer sütunları çek
        other_cols = [col.text.strip() if col.text.strip() else "0" for col in cols[1:]]
        
        # Tüm sütunları birleştir
        rows.append([kod, isim] + other_cols)

    # DataFrame oluştur
    df = pd.DataFrame(rows, columns=['Kod', 'İsim', 'ALIŞ', 'SATIŞ', '%', 'SAAT'])
    
    # İstenmeyen sütunları kaldır
    df = df.drop(columns=['ALIŞ', 'SAAT'])
    
    return df



#TODO ##########################################################



def fetch_dunya_borsalari():
    # URL'yi belirle
    url = "https://www.bloomberght.com/borsa/dunya-borsalari"

    # Sayfayı çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tüm tabloları bul
    tables = soup.find_all('table', {'data-type': 'table-type1'})

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Her bir tablo için işlem yap
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # İlk satır başlık olduğu için atlanır
            cols = row.find_all('td')
            if len(cols) >= 3:  # En az 3 sütun olduğundan emin ol
                # Borsa kodunu ve açıklamasını al
                borsa_kodu = cols[0].find('div', class_='font-bold').get_text(strip=True)
                borsa_adi = cols[0].find('div', class_='text-ellipses').get_text(strip=True)
                
                # Son ve % değişim değerlerini al
                son = cols[1].get_text(strip=True)
                yuzde = cols[2].get_text(strip=True)
                
                # Boş veya NaN değerleri 0 ile değiştir
                son = son if son.strip() else "0"
                yuzde = yuzde if yuzde.strip() else "0"
                
                # Veriyi listeye ekle
                data.append([borsa_kodu, borsa_adi, son, yuzde])

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=["Borsa Kodu", "Borsa Adı", "Son", "% Değişim"])

    return df



#TODO ##########################################################



def fetch_doviz():
    # Sayfanın URL'si
    url = "https://www.bloomberght.com/doviz"

    # Sayfanın içeriğini çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Döviz kurlarının bulunduğu tabloyu bul
    table = soup.find('table', {'data-type': 'table-type1'})

    # Tablodaki satırları bul
    rows = table.find_all('tr')

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Her bir satır için döviz bilgilerini topla
    for row in rows[1:]:  # İlk satır başlık olduğu için atlanır
        columns = row.find_all('td')
        if len(columns) >= 3:
            # İlk sütunu ayır: Örneğin "USD/TRYDOLAR" -> "USD/TRY" ve "DOLAR"
            currency_full = columns[0].get_text(strip=True)
            
            # Döviz çiftini ve adını ayır
            if currency_full:
                # Döviz çifti (örneğin "USD/TRY")
                currency_pair = currency_full[:7]  # İlk 7 karakter (örneğin "USD/TRY")
                # Döviz adı (örneğin "DOLAR")
                currency_name = currency_full[7:]  # 7. karakterden sonrası
            else:
                currency_pair, currency_name = "0", "0"
            
            # Diğer sütunları al
            last_price = columns[1].get_text(strip=True) if columns[1].get_text(strip=True) else "0"
            percentage_change = columns[2].get_text(strip=True) if columns[2].get_text(strip=True) else "0"
            
            # Veriyi listeye ekle
            data.append([currency_pair, currency_name, last_price, percentage_change])

    # Verileri Pandas DataFrame'e aktar
    df = pd.DataFrame(data, columns=["Döviz Çifti", "Döviz Adı", "Son Fiyat", "Değişim"])

    return df



#TODO ##########################################################



def fetch_borsa():
    # Sayfanın URL'si
    url = "https://www.bloomberght.com/borsa"

    # Sayfanın içeriğini çek
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # BIST tablosunu bul
    bist_table = soup.find('table', {'data-type': 'table-type1'})

    # Tablodaki tüm satırları bul
    rows = bist_table.find_all('tr')

    # Verileri saklamak için boş bir liste oluştur
    data = []

    # Her satır için verileri topla
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:
            # BIST adını ve açıklamasını ayır
            bist_full = columns[0].get_text(strip=True, separator=' ')
            bist_parts = bist_full.split(maxsplit=1)  # İlk boşluğa göre böl
            bist_code = bist_parts[0] if len(bist_parts) > 0 else "0"
            bist_name = bist_parts[1] if len(bist_parts) > 1 else "0"
            
            # Diğer sütunları al ve boş değerleri "0" ile doldur
            last_price = columns[1].get_text(strip=True) if columns[1].get_text(strip=True) else "0"
            percentage_change = columns[2].get_text(strip=True) if columns[2].get_text(strip=True) else "0"
            price_change = columns[3].get_text(strip=True) if columns[3].get_text(strip=True) else "0"
            monthly_change = columns[4].get_text(strip=True) if columns[4].get_text(strip=True) else "0"
            yearly_change = columns[5].get_text(strip=True) if columns[5].get_text(strip=True) else "0"
            
            # Verileri listeye ekle
            data.append([bist_code, bist_name, last_price, percentage_change, price_change, monthly_change, yearly_change])

    # DataFrame oluştur
    df = pd.DataFrame(data, columns=["BIST Kodu", "BIST Açıklama", "Son Fiyat", "% Değişim", "Fark", "Aylık(%)", "Yıllık(%)"])
    df = df.drop(columns=['Fark','Aylık(%)','Yıllık(%)'])

    return df



#TODO ##########################################################


from binance.client import Client
import pandas as pd

def fetch_kripto_binance():
    # Binance API client'ını başlat
    client = Client(None, None)
    
    # İstenen sembolleri ve bunların isimlerini tanımla
    semboller = {
        "BTCUSDT": "BTC",
        "ETHUSDT": "ETH",
        "BNBUSDT": "BNB",
        "ETHTRY": "ETHTRY",
        "USDTTRY": "USDT"
    }
    
    # Verileri toplamak için boş liste
    data = []
    
    for symbol, code in semboller.items():
        # Son fiyat bilgisini al
        ticker = client.get_ticker(symbol=symbol)
        
        # Son fiyat ve 24 saatlik yüzde değişim
        son_fiyat = float(ticker['lastPrice'])
        yuzde_degisim = float(ticker['priceChangePercent'])
        
        data.append({
            "Kod_İsim": code,
            "İsim": symbol,
            "FİYAT($)": f"{son_fiyat:,.2f}".replace(",", "|").replace(".", ",").replace("|", "."),
            "%(24s)": f"{yuzde_degisim:.2f}"
        })
    
    # DataFrame oluştur
    df = pd.DataFrame(data)
    
    # İndeksi sıfırla
    df.reset_index(drop=True, inplace=True)
    
    return df

def fetch_kripto():
    
    # Web sayfasını çek
    url = "https://www.bloomberght.com/kripto/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # KRİPTO PARA başlıklı tabloyu bul
    table = soup.find('table', {'data-type': 'table-type1'})

    # Tablo başlıklarını çek
    headers = [th.text.strip() for th in table.find_all('th')]

    # Verileri çek ve DataFrame'e aktar
    rows = []
    for row in table.find_all('tr')[1:]:  # İlk satır başlık olduğu için atlanır
        cols = row.find_all('td')
        if len(cols) > 0:
            # İlk sütundaki fazladan karakterleri kaldır (örneğin "B BTC Bitcoin" -> "BTC Bitcoin")
            crypto_name = cols[0].text.strip().split()
            crypto_code = crypto_name[1]  # İkinci eleman kodu içerir (örneğin BTC)
            crypto_full_name = ' '.join(crypto_name[1:])  # Kod ve İsim birleştirilir (BTC Bitcoin)
            
            # Diğer sütunları al ve boş veya NaN değerleri 0 olarak ayarla
            data = [crypto_code, crypto_full_name] + [
                col.text.strip() if col.text.strip() else "0" for col in cols[1:]
            ]
            rows.append(data)

    # DataFrame oluştur
    df = pd.DataFrame(rows, columns=["Kod_İsim", "İsim"] + headers[1:])

    # Sadece belirli sütunları seç (Kod_İsim, İsim, FİYAT($), %(24s))
    df = df[["Kod_İsim", "İsim", "FİYAT($)", "%(24s)"]]

    # Sonucu terminale yazdır
    return df



#TODO ##########################################################
#TODO ##########################################################
#TODO ##########################################################



# Tüm DataFrame'leri birleştir
dfs = [
    fetch_alternatif(),
    #fetch_alternatif_ve_baltik(),
    fetch_faiz_bono(),
    fetch_emtia(),
    fetch_altin(),
    fetch_dunya_borsalari(),
    fetch_doviz(),
    fetch_borsa(),
    #fetch_kripto(),
    fetch_kripto_binance()  # fetch_kripto_binance fonksiyonunu ekledik
]

# Sütun isimlerini yeniden adlandır
new_columns = ["Kod", "Aciklama", "Son_Fiyat", "Yuzde_Degisim"]
for df in dfs:
    df.columns = new_columns

# Tüm DataFrame'leri birleştir
merged_df = pd.concat(dfs, ignore_index=True)

# Son_Fiyat ve Yuzde_Degisim sütunlarını temizle ve sayısal formata dönüştür
merged_df["Son_Fiyat"] = merged_df["Son_Fiyat"].str.strip().str.replace(".", "")
merged_df["Son_Fiyat"] = merged_df["Son_Fiyat"].str.replace(",", ".").astype(float)

merged_df["Yuzde_Degisim"] = merged_df["Yuzde_Degisim"].str.strip().str.replace(",", ".").astype(float)

# ALTIN/ONS değerlerinin indexlerini bul ve değiştir
altin_indexler = merged_df[merged_df['Kod'] == 'ALTIN/ONS'].index
if len(altin_indexler) >= 2:
    merged_df.loc[altin_indexler[0], 'Kod'] = 'ALTIN/ONS-1'
    merged_df.loc[altin_indexler[1], 'Kod'] = 'ALTIN/ONS-2'

# Sira_No, Tarih ve Saat sütunlarını ekle
now = datetime.now()
merged_df.insert(0, 'Sira_No', range(1, 1 + len(merged_df)))
merged_df.insert(1, 'Tarih', now.strftime('%Y-%m-%d'))
merged_df.insert(2, 'Saat', now.strftime('%H:%M:%S'))

# Verileri Supabase'e kaydet
from database import save_data_to_supabase

save_data_to_supabase(merged_df)
