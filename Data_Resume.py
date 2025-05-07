!pip install cohere #Wajib install cohere AI

from pandas import read_csv
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import csv
import cohere
from langchain_community.llms import _import_cohere
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
import os
from dotenv import load_dotenv
import time

result = []
nomor = 0

#set API key dan setup alat resume
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

co = cohere.Client(api_key)

#Ambil data
Berita = read_csv('Kompas_thn_Judul+Link1.csv')
alamat = Berita['Link']

for i in range(1,len(Berita):
    res = req.get(alamat[i])
    sop = bs(res.text, "html.parser")
    isi = sop.find('div', class_='read__content')
    isi_teks = isi.get_text(strip=True) if isi else ""

    #Merangkum isi berita
    doc = [Document(page_content=isi_teks)]
    resume = co.chat(model='command-r', message=f'Ringkas isi berita berikut:\n{doc}')
    ringkasan = resume.text
    time.sleep(6)

    result.append({'Tanggal': Berita['Tanggal'][i], 'Bulan': Berita['Bulan'][i], 'Judul': Berita['Judul'][i], 'Link': Berita['Link'][i], 'Ringkasan': ringkasan})

    print(f'Tanggal: {Berita['Tanggal'][i]}, Bulan: {Berita['Bulan'][i]}, Judul: {Berita['Judul'][i]}, Link:{Berita['Link'][i]},Ringkasan: {ringkasan}') #untuk melihat proses berjalan

    #Simpan ke csv
    for item in result:
        nomor+=1

    with open("Kompas_resume_1.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Nomor", "Tanggal", "Bulan", "Judul", "Link", "Ringkasan"]
        writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        for j, item in enumerate(result, start=1):
            item['Nomor'] = j
            writer.writerow(item)
