## MEMUNCULKAN WIDGET UNTUK MENENTUKAN KEYWORD, TANGGAL AWAL, DAN TANGGAL AKHIR <HARUS BEDA CELL>##
import ipywidgets as widgets
from IPython.display import display

# Input teks untuk nama kolom
keywords = widgets.Text(description='Keyword: ')
Tanggal_Mulai = widgets.DatePicker(description='Tanggal Awal: ')
Tanggal_Akhir = widgets.DatePicker(description='Tanggal Akhir: ')

display(keywords, Tanggal_Mulai, Tanggal_Akhir)

## UNTUK SCRAPPING JUDUL DENGAN BASIS ISIAN WIDGET TERSEBUT ##
from bs4 import BeautifulSoup as bs
import requests as req
import csv
import urllib.parse


base_url = 'https://www.detik.com/search/searchall?query'
page_num = 1
nomor = 1
result = []
keywords = keywords.get_interact_value() #Mengubah struktur widget ke struktur text
tanggal1 = Tanggal_Mulai.value.strftime("%d/%m/%Y") #Mengubah struktur widget ke struktur tanggal
tanggal2 = Tanggal_Akhir.value.strftime("%d/%m/%Y") #Mengubah struktur widget ke struktur tanggal
query = urllib.parse.quote(keywords) #Mengganti spasi dengan %20

#Judul untuk 1 halaman yang sama
while True:
    url = f'{base_url}={query}&page={page_num}&fromdatex={tanggal1}&todatex={tanggal2}'
    response = req.get(url)

    #Menghentikan loop ketika halaman tidak bisa diakses
    if response.status_code!=200:
        print(f'Gagal mengambil kata tahu pada halaman {page_num}')
        break

    soup = bs(response.text, 'html.parser')
    page_block = soup.find_all('article', class_='list-content__item')

    #Menghentikan loop saat halaman sudah kosong
    if not page_block:
        print(f'Tidak ada berita setelah halaman {page_num-1}')
        break
    
    #Mengambil setiap judul
    for block in page_block:
        judul_block = block.find('h3', class_='media__title')
        judul = judul_block.get_text(strip=True)

        #kategori_block = block.find('h2', class_='media__subtitle')
        #kategori = kategori_block.get_text(strip=True)

        result.append({'Judul': judul})
    
    page_num += 1

#Memanggil jumlah judul yang ada di halaman ini
print(f'Banyak Judul: {len(result)}')

for item in result:
    print(f'{nomor}: {item['Judul']}')
    nomor += 1

#Simpan Judul
with open(f"Detik_{keywords}.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Nomor", "Judul"]
    writer= csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, item in enumerate(result, start=1):
        item['Nomor'] = i
        writer.writerow(item)
