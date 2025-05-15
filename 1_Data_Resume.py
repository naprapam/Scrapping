from pandas import read_csv
import cohere
from langchain.schema import Document
import os
from dotenv import load_dotenv
import time

nomor = 1
#set API key dan setup alat resume
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)
result = []

#Ambil data
Berita = read_csv(f"{Media}_{keywords}.csv")
alamat = Berita['Link']

if Berita['Media'][1] == 'Detik':
    for i in range(0,len(Berita)):               
        res = req.get(alamat[i])
        sop = bs(res.text, "html.parser")
        isi = sop.find('div', class_='detail__body-text itp_bodycontent')
        isi_teks = isi.get_text(strip=True) if isi else ""

        #Merangkum isi berita
        doc = [Document(page_content=isi_teks)]
        resume = co.chat(model='command-r', message=f'Ringkas isi berita berikut:\n{doc}')
        ringkasan = resume.text
        time.sleep(6)

        result.append({'Tanggal': Berita['Tanggal'][i], 'Judul': Berita['Judul'][i], 'Link': Berita['Link'][i], 'Ringkasan': ringkasan})
        
        print(f'{Berita['Media'][i]}, Tanggal: {Berita['Tanggal'][i]}, Judul: {Berita['Judul'][i]}, Link:{Berita['Link'][i]}, Ringkasan: {ringkasan}') #untuk melihat proses berjalan

        #Simpan ke csv
        for item in result:        
            nomor+=1

elif Berita['Media'][1] == 'Kompas':
    for i in range(0,len(Berita)):               
        res = req.get(alamat[i])
        sop = bs(res.text, "html.parser")
        isi = sop.find('div', class_='read__content')
        isi_teks = isi.get_text(strip=True) if isi else ""

        #Merangkum isi berita
        doc = [Document(page_content=isi_teks)]
        resume = co.chat(model='command-r', message=f'Ringkas isi berita berikut:\n{doc}')
        ringkasan = resume.text
        time.sleep(6)

        result.append({'Tanggal': Berita['Tanggal'][i], 'Judul': Berita['Judul'][i], 'Link': Berita['Link'][i], 'Ringkasan': ringkasan})
        
        print(f'{Berita['Media'][i]}, Tanggal: {Berita['Tanggal'][i]}, Judul: {Berita['Judul'][i]}, Link:{Berita['Link'][i]}, Ringkasan: {ringkasan}') #untuk melihat proses berjalan

        #Simpan ke csv
        for item in result:        
            nomor+=1

with open(f"Ringkasan {Media}_{keywords}.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Nomor", "Tanggal", "Judul", "Link", "Ringkasan"]
    writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
            
    for j, item in enumerate(result, start=1):
        item['Nomor'] = j
        writer.writerow(item)
